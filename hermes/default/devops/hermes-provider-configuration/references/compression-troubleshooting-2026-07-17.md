# Compression Troubleshooting — Real-World Case

**Session:** `20260715_203740_bc494a` (1014 messages, July 17 2026)
**Profile:** `default`
**Symptom:** Auto-compression never triggered despite session growing to 1014 messages (~60%+ of 65k context)

## Root Cause

Misconfiguration in `auxiliary.compression` block:

```yaml
# CONFIG AT TIME OF ISSUE (WRONG)
auxiliary:
  compression:
    provider: nvidia              # ❌ Points to NVIDIA cloud
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1   # ❌ But base_url is local Ollama!
    enabled: true
    threshold: 0.7
    protect_last_n: 100
    context_length: 128000
```

The `provider: nvidia` tells Hermes to use NVIDIA API format, but `base_url` points to local Ollama. The model `nvidia/nemotron-mini-4b-instruct` **does not exist on local Ollama**.

**Local Ollama models available:**
```
nomic-embed-text:latest
gemma4:12b
qwen3.5:4b
x/flux2-klein:4b-fp8
qwen3.5-32k:latest
qwen3.5-48k:latest
qwen3.5-64k:latest
qwen3.5-128k:latest
qwen3.5-4b-compress   ✅ COMPRESSION MODEL EXISTS HERE
```

## Fix Applied

```yaml
# FIXED CONFIG
auxiliary:
  compression:
    provider: ollama-launch         # ✅ Matches local Ollama provider name
    model: qwen3.5-4b-compress      # ✅ Model actually exists locally
    base_url: http://127.0.0.1:11434/v1
    extra_body:
      temperature: 0.1
      max_tokens: 1024
    enabled: true
    threshold: 0.85
    protect_last_n: 60
    context_length: 128000
```

## Key Config Keys (Two Places)

| Location | Key | Purpose | This Session |
|----------|-----|---------|--------------|
| `compression` (top-level) | `enabled` | Master toggle | `true` |
| | `threshold` | Context % to trigger (0–1) | `0.6` |
| | `target_ratio` | Target post-compression % | `0.75` |
| | `protect_last_n` | Never summarize last N msgs | `200` |
| | `hygiene_hard_message_limit` | Force hygiene at N msgs | `500` ← **Should have triggered!** |
| `auxiliary.compression` | `enabled` | Aux model enabled | `true` |
| | `threshold` | Aux trigger threshold | `0.7` → `0.85` |
| | `protect_last_n` | Aux protect recent | `100` → `60` |
| | `model` | **Must exist at `base_url`** | ❌ Wrong model |
| | `provider` + `base_url` | Must match | ❌ Mismatch |

## Why Hygiene Compression Also Didn't Fire

`hygiene_hard_message_limit: 500` — session had 1014 messages. This **should** have forced compression. Possible reasons it didn't:

1. **Aux model failure cascades** — if aux compression fails, hygiene may also skip
2. **`in_place: true`** (top-level) — compresses in-place but still needs aux model
3. **Silent failure** — no error surfaced to user, just no compression

## Debugging Commands

```bash
# 1. Check what's actually loaded
hermes config get auxiliary.compression

# 2. Verify model exists at endpoint
curl -s http://127.0.0.1:11434/api/tags | jq '.models[] | select(.name | contains("compress"))'

# 3. Health check
hermes doctor

# 4. Force manual compression in-session
/compress

# 5. Check gateway logs for aux errors
grep -i "compress\|auxiliary" ~/.hermes/logs/gateway.log | tail -20
```

## Prevention Checklist

- [ ] `auxiliary.compression.provider` matches a provider in `providers:`
- [ ] `auxiliary.compression.base_url` matches that provider's `api:` URL
- [ ] `auxiliary.compression.model` exists in `ollama list` (or `/v1/models` for cloud)
- [ ] `hermes doctor` passes after config change
- [ ] Test with `/compress` manually after long session