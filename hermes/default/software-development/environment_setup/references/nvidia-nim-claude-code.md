# NVIDIA NIM Configuration for Claude Code

Quick reference for configuring Claude Code CLI to use NVIDIA NIM endpoints.

## NVIDIA NIM Serverless API (Free Tier)

**Base URL**: `https://integrate.api.nvidia.com/v1`
**Auth**: `Authorization: Bearer nvapi-...` (from build.nvidia.com)
**Model ID format**: `nvidia/nemotron-3-ultra-550b-a55b`

### Environment Variables

```bash
export ANTHROPIC_BASE_URL="https://integrate.api.nvidia.com/v1"
export ANTHROPIC_API_KEY="nvapi-YOUR_KEY"
export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3-ultra-550b-a55b"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Nemotron 3 Ultra"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="NVIDIA Nemotron 3 Ultra via NIM API"
```

### Available Models (as of 2025)

| Model ID | Context | Notes |
|----------|---------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | 1M | General purpose |
| `nvidia/nemotron-3-ultra-550b-a55b-reasoning` | 1M | Reasoning-optimized |
| `nvidia/nemotron-4-340b` | 128K | Larger model |
| `nvidia/nemotron-3.5-8b` | 128K | Smaller, faster |

Check current list: https://build.nvidia.com/explore/discover

---

## Local NIM (Self-Hosted)

### Docker Command

```bash
docker run -d -p 8000:8000 \
  --gpus all \
  -e NGC_API_KEY="your-ngc-api-key" \
  nvcr.io/nim/nvidia/nemotron-3-ultra-550b-a55b:latest
```

Requires:
- NGC account (https://ngc.nvidia.com)
- Docker login: `docker login nvcr.io`
- GPU with sufficient VRAM (40GB+ for 550B model)

### Environment Variables (Local)

```bash
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="dummy"  # Local NIM often doesn't require auth
export ANTHROPIC_CUSTOM_MODEL_OPTION="nemotron-3-ultra"
```

---

## Quick Verification

```bash
# List available models
curl -s "https://integrate.api.nvidia.com/v1/models" \
  -H "Authorization: Bearer nvapi-..." | jq '.data[].id'

# Test completion
curl -s "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Authorization: Bearer nvapi-..." \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-3-ultra-550b-a55b","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

---

## Persistent Settings (settings.json)

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

---

## Feature Capabilities Declaration

Since custom model IDs don't match Anthropic's patterns, declare capabilities explicitly:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTS_EXTENDED_THINKING=true
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTS_1M_CONTEXT=true
```

---

## Alternative Providers (Also OpenAI-Compatible)

| Provider | Base URL | Nemotron Model |
|----------|----------|----------------|
| Together.ai | `https://api.together.xyz/v1` | `nvidia/nemotron-3-ultra-550b` |
| Fireworks | `https://api.fireworks.ai/inference/v1` | `accounts/fireworks/models/nemotron-3-ultra` |
| vLLM (local) | `http://localhost:8000/v1` | Your served model |
| Ollama (local) | `http://localhost:11434/v1` | `nemotron3:latest` |

---

## Caveats

1. **No validation** — Model names passed through without checking
2. **No prompt caching** — Most OpenAI-compatible endpoints don't support Anthropic's `cache_control`
3. **No server-managed settings** — Organization restrictions not delivered to third-party endpoints
4. **Streaming** — Requires upstream SSE support in OpenAI format