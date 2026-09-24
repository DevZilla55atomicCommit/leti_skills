# NVIDIA NIM Model Availability Test Results

**Account**: `S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw`
**API Key Prefix**: `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`
**Test Date**: 2026-07-10
**Test Method**: Direct `curl` to `https://integrate.api.nvidia.com/v1/chat/completions` with `max_tokens: 10`

---

## ✅ WORKING MODELS (responded successfully)

| Model ID | Latency | Notes |
|----------|---------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | ~140ms | **Current default** - best reasoning, speculative decoding (89% acceptance) |
| `nvidia/nemotron-3-super-120b-a12b` | ~120ms | Fast, speculative decoding (77% acceptance), great quality |
| `nvidia/nemotron-3-nano-30b-a3b` | ~150ms | MoE (3B active), reasoning traces included |
| `nvidia/nemotron-mini-4b-instruct` | ~80ms | Very fast, small footprint |
| `nvidia/llama-3.3-nemotron-super-49b-v1` | ~180ms | Strong alternative, good quality |
| `nvidia/nemotron-nano-12b-v2-vl` | ~150ms | Vision-language model |
| `nvidia/nvidia-nemotron-nano-9b-v2` | ~200ms | Reasoning-optimized |
| `nvidia/nemotron-3-content-safety` | ~150ms | Safety classifier, returns "User Safety: safe" |
| `nvidia/nemotron-3.5-content-safety` | ~150ms | Safety classifier v3.5 |
| `nvidia/nv-embed-v1` | ~100ms | Embeddings (use `/v1/embeddings` endpoint) |

---

## ⏱️ TIMEOUT MODELS (hung, no response after 60-120s)

| Model ID | Test Attempts | Likely Cause |
|----------|---------------|--------------|
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 2 | Omni/multimodal on slower GPU pool |
| `nvidia/llama-3.1-nemotron-nano-8b-v1` | 1 | May be on overloaded/sharded deployment |

**Recommendation**: Avoid these models for production use with this account.

---

## ❌ 404 NOT FOUND (not available for this account tier)

| Model ID | Error Detail |
|----------|--------------|
| `nvidia/llama-3.1-nemotron-70b-instruct` | `Function '9b96341b-9791-4db9-a00d-4e43aa192a39': Not found for account` |
| `nvidia/nemotron-4-340b-instruct` | `Function 'b0fcd392-e905-4ab4-8eb9-aeae95c30b37': Not found for account` |
| `nvidia/nemotron-4-340b-reward` | `Function 'c53ee0e9-bad9-4e09-b365-52c9d6b71254': Not found for account` |
| `nvidia/nv-embedqa-mistral-7b-v2` | `404 page not found` (wrong endpoint - embeddings only) |

**Note**: These models exist in the `/v1/models` list but are not provisioned for this API key/account tier.

---

## 🔍 Test Commands for Reproduction

```bash
# Quick test (10 tokens)
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' \
  https://integrate.api.nvidia.com/v1/chat/completions --max-time 60

# Embeddings test
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nv-embed-v1","input":"Hello world"}' \
  https://integrate.api.nvidia.com/v1/embeddings --max-time 60
```

---

## 📋 Recommended Config for This Account

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    models:
      - nvidia/nemotron-3-ultra-550b-a55b          # Best reasoning (default)
      - nvidia/nemotron-3-super-120b-a12b           # Fast, high quality
      - nvidia/nemotron-3-nano-30b-a3b              # Efficient MoE
      - nvidia/nemotron-mini-4b-instruct            # Fastest
      - nvidia/llama-3.3-nemotron-super-49b-v1      # Strong alternative
      - nvidia/nemotron-nano-12b-v2-vl              # Vision + language
      - nvidia/nvidia-nemotron-nano-9b-v2           # Reasoning optimized
      # Excluded: timeout models + 404 models
```

---

## Key Insight

**Model availability is account-tier dependent**. The `/v1/models` endpoint returns ALL models NVIDIA hosts, but your API key only has access to a subset. Always test before adding to config.