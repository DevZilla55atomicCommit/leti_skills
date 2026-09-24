# Auto-Compression Troubleshooting

## Problem: Session Grows Past Hygiene Limits Without Compression

**Symptoms:**
- Session reaches 1000+ messages
- `hygiene_hard_message_limit: 500` (or similar) is configured but never triggers
- Context usage keeps growing unchecked
- Eventually model switches or session degrades

**Root Cause (Observed in Session 20260715_203740_bc494a):**

```yaml
# ~/.hermes/config.yaml and ~/.hermes/profiles/default/config.yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1   # LOCAL OLLAMA
    enabled: true
    threshold: 0.7
    # ... other settings
```

**What Happens:**
1. Session hits compression threshold (60% context or 500 messages)
2. Compression subsystem tries to call `nvidia/nemotron-mini-4b-instruct` via **local Ollama**
3. Model doesn't exist locally (only `qwen3.5-4b-compress` is pulled)
4. Call fails silently (or times out)
5. `abort_on_summary_failure: true` prevents fallback/retry
6. Compression aborts → session continues growing unchecked

## Fix: Point to NVIDIA API Directly

```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: https://integrate.api.nvidia.com/v1  # NVIDIA API endpoint
    enabled: true
    threshold: 0.6  # match main compression.threshold
    protect_last_n: 100
    context_length: 128000
    # Remove extra_body, timeout — use defaults
```

**Verified:** `nvidia/nemotron-mini-4b-instruct` IS available on NVIDIA API:
```bash
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models \
  | jq -r '.data[].id' | grep nemotron-mini-4b-instruct
# nvidia/nemotron-mini-4b-instruct
```

## Alternative: Use Local Compression Model

If you prefer fully local (no API calls), use the already-pulled model:

```yaml
auxiliary:
  compression:
    provider: ollama-launch
    model: qwen3.5-4b-compress
    base_url: http://127.0.0.1:11434/v1
    enabled: true
    threshold: 0.6
    protect_last_n: 100
    context_length: 128000
```

## Key Config Interactions

| Setting | Location | Role |
|---------|----------|------|
| `compression.threshold` | Root config | Context % that triggers compression (0.6 = 60%) |
| `compression.hygiene_hard_message_limit` | Root config | Message count that forces compression (500) |
| `compression.abort_on_summary_failure` | Root config | If true, failed compression = no retry |
| `auxiliary.compression.provider` | Auxiliary | Which provider to use for summarization |
| `auxiliary.compression.base_url` | Auxiliary | Endpoint for the provider |
| `auxiliary.compression.model` | Auxiliary | Model name (must exist at that endpoint) |

## Debugging Steps

1. **Check if compression model exists:**
   ```bash
   # For local Ollama
   curl -s http://127.0.0.1:11434/api/tags | jq -r '.models[].name'
   
   # For NVIDIA API
   curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models \
     | jq -r '.data[].id'
   ```

2. **Test compression manually:**
   ```bash
   hermes chat -q "/compress"
   # or check logs for "compression" messages
   ```

3. **Verify config is loaded:**
   ```bash
   hermes config get auxiliary.compression
   ```

## Prevention Checklist

- [ ] `auxiliary.compression.base_url` matches the `provider` (Ollama URL for `ollama-launch`, NVIDIA API for `nvidia`)
- [ ] Model name exists at that endpoint
- [ ] `abort_on_summary_failure: false` for graceful degradation
- [ ] `hygiene_hard_message_limit` ≤ desired max messages (300-500 recommended)
- [ ] `protect_last_n` preserves recent context (100-200)

---

**Session Reference:** 20260715_203740_bc494a (1,014 messages, Video Effects pipeline)
**Fixed In:** Config patched to use NVIDIA API directly for compression model