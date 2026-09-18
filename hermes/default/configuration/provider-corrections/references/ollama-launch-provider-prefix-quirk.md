# Ollama-Launch Provider Prefix Quirk (2026-08-19)

## Problem
When using a local Ollama model via the `ollama-launch` provider, specifying the model with the provider prefix (e.g., `ollama-launch/translategemma:4b`) causes context length resolution to fail.

### Error
```
Model ollama-launch/translategemma:4b has a context window of 8,192 tokens, 
which is below the minimum 64,000 required by Hermes Agent.
```

### Root Cause
1. User specifies model as `ollama-launch/translategemma:4b`
2. This full name gets passed to `get_model_context_length()` without stripping the provider prefix
3. `_strip_provider_prefix()` checks if `ollama-launch` is a registered provider — it's NOT (normalizes to `custom` via `_normalize_provider_alias`)
4. The prefix is **not stripped**, so lookup uses `ollama-launch/translategemma:4b`
5. Ollama's `/v1/models` returns bare names like `translategemma:4b` — no match
6. Falls through to hardcoded defaults where `gemma` → 8192 tokens (older gemma fallback)
7. Agent rejects it as below 64K minimum

### Evidence
```python
# Cache has CORRECT entry (stripped name):
'translategemma:4b@http://127.0.0.1:11434/v1': 131072

# But lookup uses UNSTRIPPED name:
'ollama-launch/translategemma:4b@http://127.0.0.1:11434/v1'  # cache miss

# _strip_matching_provider_prefix DOES work correctly:
_strip_matching_provider_prefix('ollama-launch/translategemma:4b', 'ollama-launch')  
# → 'translategemma:4b'
```

## Workarounds

### Option 1: Use bare model name (recommended)
```bash
hermes chat -m "translategemma:4b" -q "Hello"
```
The provider is inferred from the base URL.

### Option 2: Set explicit context_length in config.yaml
```yaml
model:
  translategemma:4b:
    context_length: 131072
```

### Option 3: Use model alias
```yaml
model:
  aliases:
    translate: ollama-launch/translategemma:4b
```
Then use `/model translate` or `-m translate`.

## Fix Needed (Code Level)
The model name must be normalized via `normalize_model_for_provider()` or `_strip_matching_provider_prefix()` **before** being passed to `get_model_context_length()` in `agent/agent_init.py`.

The function `hermes_cli.model_normalize._strip_matching_provider_prefix` correctly handles this — it just needs to be called in the agent initialization path where the model is first resolved for context length detection.

## Related Files
- `hermes_cli/model_normalize.py` — `_strip_matching_provider_prefix()` function
- `agent/model_metadata.py` — `_strip_provider_prefix()` and `get_model_context_length()`
- `agent/agent_init.py` — where context length is resolved during agent startup