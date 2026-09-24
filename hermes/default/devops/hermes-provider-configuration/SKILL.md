---
name: hermes-provider-configuration
description: "Configure Hermes Agent with multi-provider setups: primary, fallback, and auxiliary model routing. Covers NVIDIA NIM, OpenRouter, Ollama, and custom endpoints with proper YAML structure for config.yaml."
version: 1.0.0
author: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, configuration, providers, fallback, auxiliary, nvidia, ollama, openrouter]
    related_skills: [hermes-agent]
---

# Hermes Provider Configuration

This skill documents the pattern for configuring Hermes Agent with a **primary provider**, **fallback provider(s)**, and **auxiliary model routing** for vision, web extraction, compression, and other internal tasks.

## When to Use

- Setting up a new Hermes profile with a specific provider stack
- Adding fallback providers for resilience when primary API is down
- Configuring auxiliary models (vision, compression, etc.) to use local or cheaper models
- Switching between cloud and local inference

---

## Config Structure Overview

The `config.yaml` has three relevant sections:

```yaml
model:              # Primary model + provider
  default: "provider/model-name"
  provider: "provider-name"
  # ... other settings

providers:          # Provider definitions (credentials, endpoints, model lists)
  provider-name:
    api: "https://api.example.com/v1"
    api_key: "sk-..."
    default_model: "model-name"
    models: [...]
    name: "Display Name"

fallback_providers: # Ordered fallback chain
  - provider: "provider-name"
    model: "model-name"

auxiliary:          # Internal task routing
  vision:
    provider: "provider-name"
    model: "model-name"
  web_extract:
    provider: "provider-name"
    model: "model-name"
  compression:
    provider: "provider-name"
    model: "model-name"
  # ... etc
```

---

## Pattern: NVIDIA Primary + Ollama Fallback

### 1. Primary: NVIDIA NIM (Nemotron models)

```yaml
model:
  default: "nvidia/nemotron-3-ultra-550b-a55b"
  provider: "nvidia"
  ollama_num_ctx: 65536
  ollama_context_length: 65536

providers:
  nvidia:
    api: "https://integrate.api.nvidia.com/v1"
    api_key: "nvapi-..."           # from https://build.nvidia.com
    default_model: "nvidia/nemotron-3-ultra-550b-a55b"
    name: "NVIDIA"
```

**Available NVIDIA NIM models** (query via `curl -H "Authorization: Bearer $KEY" https://integrate.api.nvidia.com/v1/models`):
- Flagship: `nvidia/nemotron-3-ultra-550b-a55b`, `nvidia/nemotron-3-super-120b-a12b`, `nvidia/nemotron-4-340b-instruct`
- Specialized: `nvidia/nemotron-3-nano-30b-a3b`, `nvidia/llama-3.1-nemotron-70b-instruct`, `nvidia/llama-3.3-nemotron-super-49b-v1`
- Embedding: `nvidia/nv-embed-v1`, `nvidia/nv-embedqa-e5-v5`, `nvidia/llama-nemotron-embed-1b-v2`
- Safety: `nvidia/nemotron-3-content-safety`, `nvidia/llama-3.1-nemoguard-8b-content-safety`
- Vision: `nvidia/neva-22b`, `nvidia/vila`, `nvidia/nvclip`
- Third-party via NIM: Meta Llama 3.x, Mistral, Gemma, Qwen, DeepSeek, Phi, etc.

### 2. Fallback: Local Ollama

```yaml
fallback_providers:
  - provider: "ollama-launch"
    model: "qwen3.5:4b"

providers:
  ollama-launch:
    api: "http://127.0.0.1:11434/v1"
    default_model: "gemma4:12b"
    models:
      - "gemma4:12b"
      - "qwen3.5:4b"
      - "qwen3.5-32k:latest"
      - "nomic-embed-text:latest"
      - "minicpm-v4.5:8b"
    name: "Ollama"
```

**Requirements**: `ollama serve` running locally, models pulled (`ollama pull qwen3.5:4b`)

### 3. Auxiliary Model Routing

Route internal tasks to cheaper/local models:

```yaml
auxiliary:
  vision:
    provider: "nvidia"
    model: "google/diffusiongemma-26b-a4b-it"
    timeout: 120
    context_length: 64000
  web_extract:
    provider: "nvidia"
    model: "meta/llama-3.1-8b-instruct"
    timeout: 360
  compression:
    provider: "ollama-launch"
    model: "qwen3.5-4b-compress"
    base_url: "http://127.0.0.1:11434/v1"
    timeout: 120
    extra_body:
      temperature: 0.1
      max_tokens: 1024
    enabled: true
    threshold: 0.85
    protect_last_n: 60
    context_length: 128000
  # Other auxiliary tasks (skills_hub, approval, mcp, title_generation, etc.)
  # can also be explicitly routed or left as "auto"
```

**Key auxiliary tasks to consider routing**:
| Task | Recommended Model | Reason |
|------|-------------------|--------|
| `vision` | Multimodal model (NVILA, Phi-3-Vision, LLaVA) | Needs vision capability |
| `web_extract` | Fast instruct model (8B-70B) | High volume, lower quality OK |
| `compression` | Specialized compression model | `qwen3.5-4b-compress` designed for this |
| `skills_hub` | Small fast model | Just categorization |
| `approval` | Small fast model | Binary classification |
| `title_generation` | Tiny model | Very simple task |

---

## Pattern: OpenRouter Primary + Local Fallback

```yaml
model:
  default: "anthropic/claude-sonnet-4.6"
  provider: "openrouter"

providers:
  openrouter:
    api: "https://openrouter.ai/api/v1"
    api_key: "sk-or-..."
    default_model: "anthropic/claude-sonnet-4.6"
    models:
      - "anthropic/claude-sonnet-4.6"
      - "anthropic/claude-opus-4.8"
      - "openai/gpt-5.5"
      - "deepseek/deepseek-v4-pro"
    name: "OpenRouter"
  ollama-launch:
    api: "http://127.0.0.1:11434/v1"
    default_model: "gemma4:12b"
    models: ["gemma4:12b", "qwen3.5:4b", "llama3.2:3b"]
    name: "Ollama"

fallback_providers:
  - provider: "ollama-launch"
    model: "qwen3.5:4b"
```

---

## CLI Commands for Quick Changes

```bash
# Primary model + provider
hermes config set model.default "nvidia/nemotron-3-ultra-550b-a55b"
hermes config set model.provider "nvidia"

# Fallback (requires YAML array - use config edit or Python)
hermes config edit  # then edit fallback_providers section

# Auxiliary routing
hermes config set auxiliary.vision.provider "nvidia"
hermes config set auxiliary.vision.model "google/diffusiongemma-26b-a4b-it"
hermes config set auxiliary.compression.provider "ollama-launch"
hermes config set auxiliary.compression.model "qwen3.5-4b-compress"

# Verify
hermes config show
hermes doctor
```

---

## Pitfalls & Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Fallback not working | `fallback_providers` written as JSON string instead of YAML array | Use `hermes config edit` or Python YAML to write proper array |
| Auxiliary model 404 | Model name doesn't exist on that provider | Query `/v1/models` endpoint to verify exact model ID |
| "No models provided" | Provider `api_key` missing or invalid | Check `hermes auth list <provider>` and `.env` |
| Changes not applied | Config read at startup only | Restart Hermes (`/reset` in CLI, `/restart` in gateway) |
| Vision fails silently | `auxiliary.vision.provider: auto` but no vision-capable model configured | Explicitly set provider + vision model |
| Compression loops | `compression.enabled: true` but model outputs malformed JSON | Use dedicated compression model (`qwen3.5-4b-compress`), set `temperature: 0.1` |

---

## Verification Checklist

After config changes:
- [ ] `hermes doctor` passes
- [ ] `hermes config show` shows expected values
- [ ] `hermes chat -q "test"` works with primary
- [ ] Disconnect primary API (or use invalid key) → fallback activates
- [ ] Vision task (`/image` + image) routes to vision model
- [ ] Long context triggers compression → uses compression model

---

## Related Skills

- `hermes-agent` — Core Hermes configuration reference
- `hermes-claude-code-orchestration` — Using Hermes as planner with Claude Code as builder

## References

- `references/session-config-nvidia-ollama-2026-07-13.md` — Working NVIDIA primary + Ollama fallback config
- `references/compression-troubleshooting-2026-07-17.md` — Real-world case: compression failed due to provider/model mismatch (1014-message session)
- `references/context-length-override-pitfall-2026-07-18.md` — **NEW**: Profile config `model.context_length` override incorrectly capped nemotron-3-ultra (1M) to 64K, causing API 400 errors and 12h compression cooldown
- `references/open-design-integration.md` — Complete Open Design MCP server setup for Hermes Agent (install, daemon, config, tools, troubleshooting)

---

## Pitfall: Global `model.context_length` Override Caps All Models

**Symptom**: API returns `400: This model's maximum context length is 4096/64000 tokens...` even though the model supports much more (e.g., nemotron-3-ultra = 1M).

**Cause**: `model.context_length` in profile config is a **global override** applied to *every* model in that profile, regardless of provider.

```yaml
# ~/.hermes/profiles/default/config.yaml
model:
  default: qwen3.5:4b
  provider: nvidia
  context_length: 65536   # ❌ BAD: applies to nemotron-3-ultra too!
```

**Fix**: Remove the global override, or use per-model override via `custom_providers`:

```yaml
# Option 1: Delete the line (let Hermes resolve from provider metadata)
model:
  default: qwen3.5:4b
  provider: nvidia
  # context_length: 65536  ← REMOVED

# Option 2: Per-model override (if you must)
custom_providers:
  - name: nvidia
    base_url: https://integrate.api.nvidia.com/v1
    models:
      nvidia/nemotron-3-ultra-550b-a55b:
        context_length: 1000000
```

**Verification**: After fix, `hermes doctor` passes and `/model` in-session shows correct resolved context length.