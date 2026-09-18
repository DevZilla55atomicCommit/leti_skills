---
name: environment-setup
description: Protocols for auditing, installing, and managing external dependencies and environment-specific configurations.
---

# Environment & Dependency Management

This skill provides a standard workflow for safely evaluating and installing third-party libraries or projects (e.g., via `pip`, `npm`, or `brew`) while ensuring system stability and handling version conflicts.

## 1. Pre-Installation Audit
Before installing any package from an external repository:
1. **Clone/Fetch**: Clone the repo to a temporary directory (`/tmp/audit-name`) rather than using direct URL installs when possible.
2. **Metadata Review**: Inspect `pyproject.toml`, `setup.cfg`, or `requirements.txt` for dependencies and Python version requirements.
3. **Security Context**: Check the license (e.g., MIT, Apache) and look for any instructions in the `README.md`.

## 2. Dependency Installation Workflow
- Use the `terminal` tool to perform installations.
- Always use a virtual environment (`~/.hermes/venvs/`) to prevent pollution of the system site-packages or affecting other projects.

## 3. Handling Version Mismatches (The "Python 3.9" Trap)
If a package requires a newer Python version than what is currently set as the default `python3` on the local system:
1. **Identify Available Versions**: Check which versions are installed (`python3.10 --version`, `python3.11 --version`).
2. **Dedicated Provisioning**: Create a new virtual environment specifically for that package using the required version.

**Example Pattern:**
If a project requires `>= 3.10` but `python3` is `3.9`:
```bash
# Create isolated venv with higher versioned binary
python3.11 -m venv ~/.hermes/venvs/<project-name>
source ~/.hermes/venvs/<project-name>/bin/activate
pip install --upgrade pip
pip install .
```

## 4. Troubleshooting Common Blocks
| Issue | Cause | Solution |
| :--- | :--- | :--- |
| Issue | Cause | Solution |

### TONY AI Agent Gateway Keeps Getting Killed (SIGKILL, exit code -9)
**Observed in this session (2026-07-08):** TONY gateway process (`node src/gateway/server.js`) started on `http://localhost:8787` / `ws://localhost:8787/ws` but repeatedly killed by macOS (SIGKILL = exit code -9 / 137).

**Likely Causes:**
1. **macOS memory pressure killer** — System has 15GB/16GB used, 226M free, heavy swap. Node process may exceed memory limit.
2. **No memory limit on Node** — Default V8 heap can grow unbounded.

**Fix Applied (Worked):**
```bash
cd /Users/alfredkamisese/TONY-AI-Agent
/Users/alfredkamisese/.hermes/node/bin/node --max-old-space-size=512 src/gateway/server.js
```
Limiting V8 heap to 512MB prevented OOM kills. If it still dies, try 256MB.

**Background Run Pattern (with notify):**
```bash
# Run in background with notification on exit
cd /Users/alfredkamisese/TONY-AI-Agent && /Users/alfredkamisese/.hermes/node/bin/node --max-old-space-size=512 src/gateway/server.js &
# Or via Hermes terminal tool with background=true, notify_on_complete=true
```

**Verification:**
- Check memory: `top -l 1 | grep PhysMem`
- Check process: `ps aux | grep "gateway/server.js"`
- Health check: `curl http://localhost:8787/health` (if endpoint exists)
| `Version Conflict` | System Python version too low | Provision a specific versioned venv (see step 3) |
| `Missing Binary` | Local system missing Node.js, gcc, etc. | Check installation requirements in `README.md` or `setup-xxx.md` |

## 5. Custom LLM Provider Configuration for Claude Code

Claude Code CLI can route requests through any **OpenAI-compatible API endpoint** via environment variables. This enables using models from NVIDIA NIM, Together.ai, Fireworks, vLLM, Ollama, LiteLLM, and other providers.

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_BASE_URL` | Redirects all API calls to this endpoint (expects OpenAI `/v1/chat/completions` format) |
| `ANTHROPIC_API_KEY` | Passed as `Authorization: Bearer <key>` to the custom endpoint |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Adds a custom model entry to the `/model` picker (skips built-in validation) |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Display name in model picker (optional) |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Description in model picker (optional) |

### NVIDIA NIM (build.nvidia.com) — Free Serverless API

```bash
# Get API key from https://build.nvidia.com → model page → "Get API Key"
export ANTHROPIC_BASE_URL="https://integrate.api.nvidia.com/v1"
export ANTHROPIC_API_KEY="nvapi-YOUR_KEY_HERE"
export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3-ultra-550b-a55b"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Nemotron 3 Ultra"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="NVIDIA Nemotron 3 Ultra via NIM API"
```

**Note for Hermes Agent users**: Hermes uses `${NVIDIA_API_KEY}` environment variable substitution in `~/.hermes/config.yaml` (see `providers.nvidia.api_key`). Set this in your shell config:
```bash
# ~/.zshrc or ~/.bashrc
export NVIDIA_API_KEY="nvapi-YOUR_ACTUAL_KEY"
```
Then reload shell: `source ~/.zshrc` and restart Hermes Agent.

Available NIM models (check https://build.nvidia.com/explore/discover for current list):
- `nvidia/nemotron-3-ultra-550b-a55b` (1M context)
- `nvidia/nemotron-3-ultra-550b-a55b-reasoning` (1M context, reasoning)
- `nvidia/nemotron-4-340b` (128K context)
- `nvidia/nemotron-3.5-8b` (128K context)

### Local NIM (Self-Hosted via Docker)

```bash
# Pull and run NIM container (requires NGC account + docker login to nvcr.io)
docker run -d -p 8000:8000 \
  -e NGC_API_KEY="your-ngc-key" \
  nvcr.io/nim/nvidia/nemotron-3-ultra-550b-a55b:latest

# Configure Claude Code
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="dummy"  # Local NIM may not require auth
export ANTHROPIC_CUSTOM_MODEL_OPTION="nemotron-3-ultra"
```

### Ollama (Local) — Anthropic API Compatible (v0.14.0+)

Ollama v0.14.0+ exposes an Anthropic Messages API-compatible endpoint at `http://localhost:11434/v1`. This allows Claude Code to run entirely on local models.

```bash
# Ensure Ollama listens on all interfaces
pkill ollama
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

# Pull a coding model with 32K+ context
ollama pull qwen3.5-128k:latest
# or
ollama pull qwen3-coder

# Configure Claude Code to use Ollama
export ANTHROPIC_BASE_URL="http://localhost:11434/v1"
export ANTHROPIC_API_KEY="ollama"
export ANTHROPIC_AUTH_TOKEN="ollama"

# Run with local model
claude --model qwen3.5-128k:latest
```

#### Auto-Mode Classifier Optimization (CRITICAL)

The auto-mode safety classifier (which approves bash commands) uses the **haiku tier** model. Large local models (qwen3.5-128k, qwen3-coder) are too slow for this — they cause "timed out, so auto mode cannot determine the safety" errors.

**Solution: Use a fast Ollama cloud model for the classifier, local model for coding.**

```bash
# Fast cloud model for classifier (zero local resources, ~0.5s response)
export ANTHROPIC_DEFAULT_HAIKU_MODEL=gemma4:31b-cloud
export ANTHROPIC_DEFAULT_SONNET_MODEL=gemma4:31b-cloud
export ANTHROPIC_DEFAULT_OPUS_MODEL=gemma4:31b-cloud

# Your coding model (local, full context)
claude --model qwen3.5-128k:latest
```

| Tier | Purpose | Recommended Model |
|------|---------|-------------------|
| Haiku | Auto-mode classifier, quick summaries | `gemma4:31b-cloud` (cloud, free, ~0.5s) |
| Sonnet | Default coding | Your local model (`qwen3.5-128k:latest`) |
| Opus | Complex reasoning | Your local model or `nemotron-3-ultra:cloud` |

**Pitfall:** Do not set the classifier to a large local model — it will timeout on every bash command approval, blocking auto-mode entirely.

### Other OpenAI-Compatible Providers

| Provider | Base URL | Example Model |
|----------|----------|---------------|
| Together.ai | `https://api.together.xyz/v1` | `nvidia/nemotron-3-ultra-550b` |
| Fireworks | `https://api.fireworks.ai/inference/v1` | `accounts/fireworks/models/nemotron-3-ultra` |
| vLLM (local) | `http://localhost:8000/v1` | Whatever model you serve |
| Ollama (local) | `http://localhost:11434/v1` | `nemotron3:latest` (if available) |
| LiteLLM proxy | `http://localhost:4000/v1` | Any model LiteLLM routes to |

### Persistent Configuration (settings.json)

Add to `~/.claude/settings.json` or `.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://integrate.api.nvidia.com/v1",
    "ANTHROPIC_API_KEY": "nvapi-...",
    "ANTHROPIC_CUSTOM_MODEL_OPTION": "nvidia/nemotron-3-ultra-550b-a55b",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_NAME": "Nemotron 3 Ultra",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION": "NVIDIA Nemotron 3 Ultra via NIM API"
  },
  "model": "nvidia/nemotron-3-ultra-550b-a55b",
  "available_models": [
    "nvidia/nemotron-3-ultra-550b-a55b",
    "nvidia/nemotron-3-ultra-550b-a55b-reasoning",
    "claude-sonnet-4-6",
    "claude-opus-4-6"
  ],
  "modelOverrides": {
    "opus": "nvidia/nemotron-3-ultra-550b-a55b",
    "sonnet": "nvidia/nemotron-3-ultra-550b-a55b"
  }
}
```

### Important Caveats

- **No Anthropic-format validation** — When `ANTHROPIC_BASE_URL` points to a non-Anthropic endpoint, Claude Code passes model names through without checking. Typos only surface at request time.
- **Feature detection via model ID patterns** — Claude Code enables extended thinking, 1M context, etc. based on model ID patterns (e.g., `claude-sonnet-4-6`, `sonnet[1m]`). Custom model IDs won't match these patterns. Declare capabilities explicitly:
  ```bash
  export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTS_EXTENDED_THINKING=true
  export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTS_1M_CONTEXT=true
  ```
- **No server-managed settings** — On third-party endpoints, organization-level model restrictions (`availableModels`, `modelOverrides` from admin console) are not delivered. Use local `available_models` in settings.json instead.
- **Prompt caching** — Works only if the upstream provider supports Anthropic's `cache_control` extension (most OpenAI-compatible endpoints don't). Expect no cache savings.
- **Streaming** — Requires the upstream to support SSE streaming in OpenAI format.

### Quick Test Before Using

```bash
# Verify endpoint works
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer nvapi-..." | jq '.data[].id'

# Test chat completion
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer nvapi-..." \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-3-ultra-550b-a55b","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

## Pitfalls & Warnings
- **Never** install major libraries directly into the base system environment unless explicitly requested by the user for a specific global reason.
- **Safe Mode**: For any suspicious repository, always run `pip install --dry-run` (if available) or inspect the `install.md` before proceeding.
- **Environment Persistence**: Ensure that any commands installed via `pip` are verified to be accessible in the current shell path.