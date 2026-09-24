# Ollama Cloud Provider Fix (2026-08-28)

## Problem
The `ollama-cloud` provider in Hermes was failing with `APIConnectionError` to `api.ollama.com/v1` despite correct API key and model configuration.

## Root Causes Identified

1. **Wrong base URL in config** — User config had `api: https://api.ollama.com/v1` but Ollama Cloud API is at `https://ollama.com/v1` (the former returns 301 redirect)

2. **Incorrect model names** — Config used `-cloud` suffix (e.g., `gemma4:31b-cloud`) but the API returns clean IDs without suffix

3. **Missing code-level handling** — `ollama-cloud` is a registered provider in `PROVIDER_REGISTRY` but was not explicitly handled in:
   - `hermes_cli/runtime_provider.py` → `resolve_runtime_provider()` — fell through to generic `custom` provider
   - `agent/auxiliary_client.py` → `_PROVIDER_ALIASES` — no alias mapping

## Fixes Applied

### Config Fixes (`~/.hermes/config.yaml`)
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

### Code Patches

**1. `hermes_cli/runtime_provider.py`** (after Vertex AI block, before `custom_runtime`):
```python
# Ollama Cloud: registered provider with fixed base_url and api_key from OLLAMA_API_KEY
# Handle BEFORE custom_runtime so the registered inference_base_url is used.
if requested_provider == "ollama-cloud":
    from hermes_cli.auth import DEFAULT_OLLAMA_CLOUD_BASE_URL, PROVIDER_REGISTRY
    pconfig = PROVIDER_REGISTRY.get("ollama-cloud")
    api_key = (
        (explicit_api_key or "").strip()
        or _getenv("OLLAMA_API_KEY", "").strip()
    )
    return {
        "provider": "ollama-cloud",
        "api_mode": "chat_completions",
        "base_url": pconfig.inference_base_url if pconfig else DEFAULT_OLLAMA_CLOUD_BASE_URL,
        "api_key": api_key,
        "source": "ollama-cloud-registered",
        "requested_provider": requested_provider,
    }
```

**2. `agent/auxiliary_client.py`** (in `_PROVIDER_ALIASES`):
```python
"ollama-cloud": "ollama-cloud",
"ollama_cloud": "ollama-cloud",
```

### Cache Clearing
```bash
rm ~/.hermes/context_length_cache.yaml ~/.hermes/ollama_cloud_models_cache.json
```

## Verification
```bash
export OLLAMA_API_KEY="your_key"
hermes chat -q "hello" --provider ollama-cloud -m gemma4:31b
```

Expected: Response from model with `Endpoint: https://ollama.com/v1` in logs.

## Files Modified
- `~/.hermes/config.yaml` — Provider configuration
- `/Users/alfredkamisese/.hermes/hermes-agent/hermes_cli/runtime_provider.py` — Runtime provider resolution
- `/Users/alfredkamisese/.hermes/hermes-agent/agent/auxiliary_client.py` — Provider alias normalization

## Related Skills
- `local-ollama-troubleshooting` — Now includes Ollama Cloud section
- `provider-corrections` — Updated with Ollama Cloud correction