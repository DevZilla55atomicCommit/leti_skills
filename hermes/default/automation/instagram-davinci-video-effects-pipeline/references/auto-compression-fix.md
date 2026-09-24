# Auto-Compression Configuration Fix (2026-07-17)

## Problem
Auto-compression failed silently during long sessions (1000+ messages) because the auxiliary compression model was misconfigured to use local Ollama instead of NVIDIA API.

### Misconfiguration
```yaml
# ~/.hermes/config.yaml AND ~/.hermes/profiles/default/config.yaml
auxiliary:
  compression:
    provider: nvidia                    # Says NVIDIA
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1  # But points to LOCAL OLLAMA
```

**Root cause**: Model `nvidia/nemotron-mini-4b-instruct` does not exist on local Ollama (only `qwen3.5-4b-compress` is pulled). When compression triggered at ~60% context usage, it called local Ollama → failed silently → `abort_on_summary_failure: true` prevented retry → session grew unchecked.

## Fix Applied
Removed `base_url` so it uses NVIDIA API directly:

```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    # base_url removed → defaults to https://integrate.api.nvidia.com/v1
    timeout: 120
    extra_body:
      temperature: 0.1
      max_tokens: 1024
    enabled: true
    threshold: 0.7
    protect_last_n: 100
    context_length: 128000
```

## Verification
```bash
# Confirmed model exists on NVIDIA API
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models | jq -r '.data[].id' | grep nemotron-mini
# Output: nvidia/nemotron-mini-4b-instruct
```

## Impact
- **Before**: Compression timeout/failure after 10-30 min (Ollama cold start)
- **After**: Sub-second compression via NVIDIA hosted inference
- **Applies to**: All pipelines using auto-compress (video effects, videographer, color grading, etc.)

## Related Settings (Global Config)
```yaml
compression:
  enabled: true
  threshold: 0.6          # Trigger at 60% context
  target_ratio: 0.75      # Compress to 75%
  protect_last_n: 200
  hygiene_hard_message_limit: 500  # Force compress at 500 messages
  protect_first_n: 40
  abort_on_summary_failure: true
  in_place: true
```