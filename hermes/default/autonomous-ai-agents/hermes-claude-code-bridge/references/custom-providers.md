# Custom Providers & LLM Gateways in Claude Code

## Overview

Claude Code does not have a traditional provider registry. Instead, it uses **environment variables to redirect API calls** to any OpenAI-compatible endpoint. This enables using models from any provider that speaks the OpenAI API format.

## Core Mechanism: Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_BASE_URL` | Redirect all API calls to a custom OpenAI-compatible endpoint (Ollama, vLLM, LiteLLM, NVIDIA NIM, custom gateway). **Primary mechanism for third-party providers.** |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` | Authentication for the custom endpoint |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Add a single custom model ID to the `/model` picker (e.g., `nvidia/nemotron-3-ultra-550b`) |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Friendly display name in picker (e.g., `Nemotron 3 Ultra`) |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Description shown in picker (e.g., `NVIDIA Nemotron 3 Ultra via custom gateway`) |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | Enable auto-discovery of models from gateway's `/v1/models` endpoint |

## How It Works

1. **Set `ANTHROPIC_BASE_URL`** to your gateway's OpenAI-compatible endpoint
   - Ollama: `http://localhost:11434/v1` (or native port `http://localhost:11434`)
   - vLLM: `http://localhost:8000/v1`
   - NVIDIA NIM: `http://localhost:8000/v1`
   - LiteLLM proxy: `http://localhost:4000/v1`

2. **Set authentication** via `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN`

3. **Claude Code passes model names through as-is** — no validation occurs on custom endpoints

4. **Use `ANTHROPIC_CUSTOM_MODEL_OPTION`** to add your model to the `/model` picker with a friendly name

## Example: NVIDIA Nemotron via vLLM or NIM

```bash
# Terminal 1: Start inference server
# Option A: vLLM
vllm serve nvidia/nemotron-3-ultra-550b --port 8000

# Option B: NVIDIA NIM (requires NVIDIA container toolkit)
docker run -d --gpus all -p 8000:8000 \
  -e NIM_MODEL_NAME=nvidia/nemotron-3-ultra-550b \
  nvcr.io/nim/nvidia/nemotron-3-ultra-550b:latest

# Terminal 2: Configure and run Claude Code
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="your-key-if-needed"
export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3-ultra-550b"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Nemotron 3 Ultra"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="NVIDIA Nemotron 3 Ultra 550B via vLLM"
claude
```

## Example: Ollama (Your Current Setup)

Your current `~/.claude/settings.json` already uses this pattern:
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_BASE_URL": "http://localhost:11434"
  }
}
```

To add Nvidia Nemotron from Ollama:
```bash
# Pull the model first
ollama pull nvidia/nemotron-3-nano-omni-30b-a3b-reasoning

# Add to picker
export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Nemotron 3 Nano"
claude
```

## `modelOverrides` in settings.json

Map Anthropic model aliases to provider-specific model IDs in `.claude/settings.json`:

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "nvidia/nemotron-3-ultra-550b",
    "claude-sonnet-4-6": "nvidia/nemotron-3-ultra-550b",
    "claude-haiku-3-5": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "claude-fable-5": "nvidia/nemotron-3-ultra-550b"
  }
}
```

When a user selects `opus` in `/model`, Claude Code sends `nvidia/nemotron-3-ultra-550b` to your gateway.

## Declaring Model Capabilities

For third-party models, Claude Code may not recognize supported features (extended thinking, 1M context, etc.). Declare capabilities via environment variables:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL="nvidia/nemotron-3-ultra-550b"
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME="Nemotron 3 Ultra"
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION="NVIDIA Nemotron 3 Ultra 550B"
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES="thinking,tools,vision,1m-context"
```

Available capabilities: `thinking`, `tools`, `vision`, `1m-context`, `computer-use`.

Same pattern works for `SONNET`, `HAIKU`, `FABLE`, and `CUSTOM_MODEL_OPTION`.

## Gateway Model Discovery

Enable auto-population of the `/model` picker from your gateway's `/v1/models` endpoint:

```bash
export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1
export ANTHROPIC_BASE_URL="http://your-gateway:port/v1"
claude
```

Requires the gateway to implement the OpenAI `/v1/models` endpoint (vLLM, LiteLLM, and NIM all do).

## Important Notes

- **No provider registration needed** — just redirect the base URL
- **Features like extended thinking** only work if declared via `_SUPPORTED_CAPABILITIES`
- **`availableModels` in settings.json** still filters the picker — include your custom model IDs there
- **`ANTHROPIC_BASE_URL` changes where requests go, not which model answers** — the model name is passed through unchanged
- **Works with `--bare` mode** for CI/scripting (requires `ANTHROPIC_API_KEY`)
- **Your current Ollama setup IS a custom provider** — you're already doing this!

## Inference Server Options for Nvidia Models

| Server | Pros | Cons | Best For |
|--------|------|------|----------|
| **vLLM** | Fast, OpenAI-compatible, supports many models | Requires GPU, Python deps | Self-hosted GPU inference |
| **NVIDIA NIM** | Optimized for Nvidia GPUs, enterprise support, containerized | Requires NVIDIA Container Toolkit, NGC account | Production Nvidia workloads |
| **LiteLLM** | Proxy for 100+ providers, load balancing, fallbacks | Extra hop, config complexity | Multi-provider routing |
| **Ollama** | Simple, local, CPU+GPU | Limited model selection, slower | Local development |

## Verification Commands

```bash
# Test gateway health
curl http://localhost:8000/v1/models

# List available models
curl -s http://localhost:8000/v1/models | jq '.data[].id'

# Test completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/nemotron-3-ultra-550b", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## Session 2026-07-21 Findings: Local Ollama on M4 16GB

### Performance Characteristics

| Model | Simple Query (1 turn) | Complex (3-5 turns) | Notes |
|-------|----------------------|---------------------|-------|
| `qwen3.5:4b` | 4-6s | 15-30s | Default in settings; good for memory writes |
| `gemma4:12b` | ~3s | ~10s | Faster reasoning, better quality |
| `qwen3.5:9b` | 6-8s | 20-40s | More capable but slower |

### Print Mode Timeout Issues

- **Symptom:** `claude -p "hi" --model qwen3.5:4b` takes 45-120s, often times out at 60s default
- **Root cause:** Local Ollama inference on M4 16GB is slow; model loading + inference
- **Workarounds:**
  - Use `--max-turns 1` for simple memory writes
  - Increase wrapper timeout to 180-300s
  - Use `gemma4:12b` for faster reasoning tasks
  - Pre-trust workspace interactively once: `cd /project && claude` → Enter → `/exit`

### Wrapper Timeout Configuration

```python
# In claude-with-memory.py, increase timeout:
result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
# Or make configurable:
parser.add_argument("--timeout", type=int, default=300, help="Subprocess timeout (default: 300s)")
```

### Memory Write Pattern

For reliable memory persistence with local Ollama:
```bash
# Use 1 turn, simple prompt
~/.claude/claude-with-memory "Remember: I prefer TypeScript" --model qwen3.5:4b --max-turns 1

# Complex reasoning should use more turns but with longer timeout
~/.claude/claude-with-memory "Analyze this architecture..." --model gemma4:12b --max-turns 5
```