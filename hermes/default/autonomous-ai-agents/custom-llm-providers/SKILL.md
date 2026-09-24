---
name: custom-llm-providers
description: "Configure Claude Code and other AI agents to use custom LLM providers (NVIDIA NIM, OpenAI-compatible gateways, local inference servers) via ANTHROPIC_BASE_URL and related env vars."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [claude-code, custom-providers, nvidia, nim, openai-compatible, inference]
    related_skills: [claude-code, hermes-agent]
---

# Custom LLM Providers for Claude Code

Guide for routing Claude Code CLI through non-Anthropic endpoints (NVIDIA NIM, vLLM, Ollama, LiteLLM, Together.ai, Fireworks, etc.) using the OpenAI-compatible API pattern.

## Core Concept

Claude Code supports custom endpoints via `ANTHROPIC_BASE_URL` — it sends Anthropic-format requests to whatever URL you provide. The endpoint must:
1. Accept `POST /v1/messages` (Anthropic format) OR `POST /v1/chat/completions` (OpenAI format)
2. Return responses in the expected format
3. Accept `Authorization: Bearer <key>` auth

**Most OpenAI-compatible gateways work** because Claude Code's request shape is close enough.

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `ANTHROPIC_BASE_URL` | Base URL of custom endpoint (e.g., `https://integrate.api.nvidia.com/v1`) | Yes |
| `ANTHROPIC_API_KEY` | API key for the custom endpoint | Yes |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Add a custom model to `/model` picker | Optional |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Display name in picker | Optional |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Description in picker | Optional |
| `modelOverrides` (in settings.json) | Map Anthropic aliases (sonnet/opus) → provider model IDs | Optional |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | Enable model discovery from gateway | Optional |
| `DISABLE_AUTO_COMPACT` | Force-disable auto-compaction (set to `1`) | Optional |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens (user sets `1280000` for Ollama) | Optional |

## Auto-Compact Configuration Reference

See [`references/auto-compact-configuration.md`](references/auto-compact-configuration.md) for detailed settings keys, examples, context health thresholds, and best practices for local Ollama workflows.

## Provider Examples

### NVIDIA NIM (Hosted)
```bash
export ANTHROPIC_BASE_URL="https://integrate.api.nvidia.com/v1"
export ANTHROPIC_API_KEY="nvapi-..."
export ANTHROPIC_CUSTOM_MODEL_OPTION="nvidia/nemotron-3-ultra-550b-a55b"
```

### NVIDIA NIM (Self-Hosted)
```bash
# docker run -d -p 8000:8000 nvcr.io/nim/nvidia/nemotron-3-ultra:latest
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="dummy"  # or your configured key
```

### vLLM / Local Inference
```bash
# vllm serve nvidia/nemotron-3-ultra-550b-a55b --port 8000
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="dummy"
```

### Together.ai / Fireworks
```bash
export ANTHROPIC_BASE_URL="https://api.together.xyz/v1"
export ANTHROPIC_API_KEY="together-..."
```

### Ollama
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434/v1"
export ANTHROPIC_API_KEY="ollama"
```

## Settings.json Configuration

### Project-level (`.claude/settings.json`)
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "nvapi-...",
    "ANTHROPIC_BASE_URL": "https://integrate.api.nvidia.com/v1"
  },
  "modelOverrides": {
    "sonnet": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "opus": "nvidia/nemotron-3-ultra-550b-a55b"
  },
  "model": "sonnet",
  "available_models": ["sonnet", "opus"]
}
```

### User-level (`~/.claude/settings.json`)
Same structure, applies globally.

## Common Pitfalls

### 1. Client-Side Model Validation Bug (v2.1.x) — **Blocks NVIDIA Integration**
**Symptom:** `There's an issue with the selected model (nvidia/nemotron-...). It may not exist or you may not have access to it.`

**Cause:** Claude Code validates model names against Anthropic's allowlist **even when `ANTHROPIC_BASE_URL` is set to a custom endpoint**. The docs say validation should be skipped for custom endpoints, but it's not implemented correctly in v2.1.x.

**Workarounds:**
- Use `modelOverrides` to map `sonnet`/`opus` to your model IDs
- Add `sonnet` and `opus` to `available_models`
- Try `--bare` mode with `--settings` file
- Use a fresh `HOME` directory to avoid cached settings

**Current Status:** Infrastructure ready (LiteLLM proxy tested working), waiting for Anthropic v2.1.203+ fix.

### 2. Model Name Must Match Exactly
The model ID in `modelOverrides` / `ANTHROPIC_CUSTOM_MODEL_OPTION` must exactly match what the provider's `/v1/models` returns (including `nvidia/` prefix).

### 3. Rate Limits on Free Tier
NVIDIA's hosted endpoint has strict rate limits (503 errors). Use self-hosted NIM or paid tier for production.

### 4. Auth Format
Some providers expect `Authorization: Bearer <key>`, others use `x-api-key`. NVIDIA NIM uses Bearer token.

### 5. Verification Script Works But Claude Code Still Fails (This Session — 2026-07-07)
**Finding:** LiteLLM proxy at `http://localhost:40366/v1` with NVIDIA models:
- `/v1/models` returns 200 OK with `nemotron-3-ultra`, `nemotron-3-nano`, `sonnet`, `opus`
- `/v1/messages` (Anthropic format) returns 200 OK with proper responses
- **But** Claude Code v2.1.202 still rejects with validation error before making any API call

**Root Cause Confirmed:** Client-side validation in Claude Code runs before any network request. The proxy infrastructure is 100% working - just waiting for Anthropic to fix the validation bug.

## Quick-Switch Pattern for Multiple Providers (Ollama ↔ NVIDIA)

Created during this session for the user's workflow:

**Shell function + aliases (`~/.zshrc`):**
```bash
claude-run() { claude --model "$1" }
alias claude32="claude-run qwen3.5-32k:latest"
alias claude64="claude-run qwen3.5-64k:latest"
alias claude128="claude-run qwen3.5-128k:latest"
alias claude48="claude-run qwen3.5-48k:latest"
# ... etc.
```

**Switch script (`~/.claude/switch-provider.sh`):**
```bash
#!/bin/bash
# Switch between Ollama and NVIDIA providers for Claude Code
SETTINGS_FILE="$HOME/.claude/settings.json"
OLLAMA_CONFIG="$HOME/.claude/settings.json.original"
NVIDIA_CONFIG="$HOME/.claude/settings.nvidia.json"

case "$1" in
    ollama) cp "$OLLAMA_CONFIG" "$SETTINGS_FILE"; echo "✅ Switched to Ollama" ;;
    nvidia) cp "$NVIDIA_CONFIG" "$SETTINGS_FILE"; echo "✅ Switched to NVIDIA (bug may block)" ;;
    status) grep -q "integrate.api.nvidia" "$SETTINGS_FILE" && echo "NVIDIA" || echo "Ollama" ;;
    *) echo "Usage: $0 {ollama|nvidia|status}" ;;
esac
```

**Direct API wrapper (works now):**
```bash
# ~/.zshrc
nvidia-chat() {
  curl -s https://integrate.api.nvidia.com/v1/chat/completions \
    -H "Authorization: Bearer ***" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"nvidia/nemotron-3-nano-omni-30b-a3b-reasoning\",\"messages\":[{\"role\":\"user\",\"content\":\"$1\"}],\"max_tokens\":500}" \
    | jq -r '.choices[0].message.content'
}
# Usage: nvidia-chat "Explain quantum computing"
```

---

## Verification Script

`scripts/verify-nvidia-nim.sh` — Tests endpoint connectivity, model listing, and chat completion for any NVIDIA NIM endpoint.

## Integration with Hermes Agent

Hermes has native support for NVIDIA via the `nvidia` provider in `config.yaml`:
```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
```
Set `NVIDIA_API_KEY` in `~/.hermes/.env` or via `hermes auth add nvidia`.

**Note**: The config uses `${NVIDIA_API_KEY}` environment variable substitution. Ensure this env var is set in your shell (`~/.zshrc`/`~/.bashrc`) and Hermes is restarted after changes. The placeholder `nvapi-YOUR_KEY_HERE` in `.zshrc` must be replaced with a real key from https://build.nvidia.com.

## Related Skills
- `claude-code` — orchestration patterns for Claude Code CLI
- `hermes-agent` — Hermes native provider configuration
- `native-mcp` — MCP server integration for custom tooling

## Support Files
- `references/ollama-native-anthropic-compat.md` — **Ollama v0.14.0+ native Anthropic compatibility** (no proxy needed)
- `references/auto-compact-configuration.md` — **Auto-compact settings reference** (keys, scopes, env var, best practices for local Ollama workflows)
- `references/claude-code-nvidia-debugging.md` — Detailed debugging transcript from this session
- `references/session-2026-07-07-nvidia-deep-dive.md` — Full session deep-dive with configs tested, root cause, and working alternatives
- `references/session-2026-07-08-nvidia-api-key.md` — NVIDIA API key location for Hermes Agent (this session)
- `references/meta-ai-responses-api-adapter.md` — **Meta AI Responses API → OpenAI Chat Completions adapter** (translation logic, streaming SSE parsing, Hermes integration, generalizable pattern for any non-OpenAI provider)
- `templates/claude-settings-nvidia.json` — Ready-to-use settings.json for NVIDIA NIM
- `templates/requirements-meta-adapter.txt` — Python requirements for Meta adapter (fastapi, uvicorn, httpx, pydantic)
- `scripts/verify-nvidia-nim.sh` — **Enhanced verification script** (tests `/v1/models`, `/v1/chat/completions` OpenAI format, `/v1/messages` Anthropic format with configurable endpoint/model)
- `scripts/meta_adapter.py` — **Meta AI adapter** (FastAPI shim translating Chat Completions ↔ Responses API with proper SSE event parsing)

## Session Artifacts (2026-07-07)
This Session)
- Deep-dive into NVIDIA NIM + Claude Code integration
- Root cause: Client-side validation bug in Claude Code v2.1.202
- Working LiteLLM proxy infrastructure built and tested
- Multiple workarounds documented (direct API, OpenCode, custom scripts)