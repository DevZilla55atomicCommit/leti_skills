---
name: provider-corrections
description: User corrections to provider model names.
version: 1.0.0
tags: [provider-corrections, user-preference, configuration]
---

# User Corrections to Provider Model Names

## Ollama Cloud Provider (2026-08-28)

The Ollama Cloud API returns model IDs **without** the `-cloud` suffix:
- `gemma4:31b` (NOT `gemma4:31b-cloud`)
- `nemotron-3-ultra` (NOT `nemotron-3-ultra:cloud`)
- `glm-5.2` (NOT `glm-5.2:cloud`)
- `deepseek-v4-flash:0731` (NOT `deepseek-v4-flash:0731-cloud`)

The correct base URL is `https://ollama.com/v1` (NOT `api.ollama.com/v1`).

### Configuration
```yaml
providers:
  ollama-cloud:
    api: https://ollama.com/v1
    api_key: ${OLLAMA_API_KEY}
    default_model: deepseek-v4-flash:0731
    models:
      - nemotron-3-ultra
      - gemma4:31b
      - glm-5.2
      - deepseek-v4-flash:0731
    name: Ollama Cloud
```

### Code-Level Fixes Required (Hermes < 0.21)
Two files need patches for `ollama-cloud` to work as a registered provider:

1. **`hermes_cli/runtime_provider.py`** — In `resolve_runtime_provider()`, before `custom_runtime`:
   ```python
   if requested_provider == "ollama-cloud":
       from hermes_cli.auth import DEFAULT_OLLAMA_CLOUD_BASE_URL, PROVIDER_REGISTRY
       pconfig = PROVIDER_REGISTRY.get("ollama-cloud")
       api_key = (explicit_api_key or "").strip() or _getenv("OLLAMA_API_KEY", "").strip()
       return {
           "provider": "ollama-cloud",
           "api_mode": "chat_completions",
           "base_url": pconfig.inference_base_url if pconfig else DEFAULT_OLLAMA_CLOUD_BASE_URL,
           "api_key": api_key,
           "source": "ollama-cloud-registered",
           "requested_provider": requested_provider,
       }
   ```

2. **`agent/auxiliary_client.py`** — In `_PROVIDER_ALIASES`:
   ```python
   "ollama-cloud": "ollama-cloud",
   "ollama_cloud": "ollama-cloud",
   ```

### Verification
```bash
export OLLAMA_API_KEY="your_key"
hermes chat -q "hello" --provider ollama-cloud -m gemma4:31b
```

---

## Meta AI Provider Quirk (2026-08-04)

Meta's new `api.meta.ai` endpoint uses **OpenAI's Responses API format** (`/v1/responses`), which is **incompatible** with Hermes's `custom` provider (expects standard Chat Completions `/v1/chat/completions`).

**Error:** `HTTP 400: \`options\`: unknown parameter \`options\``

### Workarounds
1. **Use OpenRouter** (already configured) — has Meta Llama models: `meta-llama/llama-3.3-70b-instruct`, etc.
2. **Build adapter proxy** — FastAPI server translating Chat Completions → Responses API
   - Reference: `references/meta-ai-responses-api-quirk.md`
   - Template: `scripts/meta-adapter.py`
   - Run: `META_API_KEY=your_key uvicorn meta_adapter:app --port 8000`
   - Then: `hermes config set providers.meta-ai.api "http://localhost:8000/v1"`

---

## Meta AI Adapter — Session Fixes (2026-08-11)

See `references/meta-ai-session-fixes-2026-08-11.md` for detailed fixes:

### 1. Wrong Content Type for Assistant Messages
Meta's Responses API requires `output_text` for assistant messages, not `input_text`.

### 2. Default max_tokens Too Low
Muse Spark 1.1 uses heavy internal reasoning (~300-600 tokens). Default now 2000 tokens if unset.

### Verified Working
- ✅ 5/5 consecutive requests with conversation history
- ✅ 3/3 consecutive simple requests
- ✅ All return populated `content` field
- ✅ LaunchAgent auto-restart functional

### Files Updated
- `scripts/meta-adapter.py` — Fixed adapter with both fixes
- `~/meta-adapter/meta_adapter.py` — Runtime copy (manual update needed per device)