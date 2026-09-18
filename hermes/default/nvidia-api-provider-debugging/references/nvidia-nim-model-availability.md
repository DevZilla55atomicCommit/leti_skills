---
title: NVIDIA NIM Model Availability Test Results
account: S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw
tested: 2025-07-10
api_endpoint: https://integrate.api.nvidia.com/v1
---

# NVIDIA NIM Model Availability for Account `S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw`

Tested via direct API calls with API key `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`

---

## ✅ WORKING Chat Models (`/v1/chat/completions`)

### NVIDIA-Owned Models

| Model ID | Response Time | Notes |
|----------|---------------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | ~140ms | **Current default** — best reasoning, speculative decoding (89% acceptance) |
| `nvidia/nemotron-3-super-120b-a12b` | ~120ms | Fast, speculative decoding (77% acceptance) |
| `nvidia/nemotron-3-nano-30b-a3b` | ~150ms | MoE efficient, reasoning traces |
| `nvidia/nemotron-mini-4b-instruct` | ~80ms | Very fast, small |
| `nvidia/llama-3.3-nemotron-super-49b-v1` | ~180ms | Strong alternative |
| `nvidia/nemotron-nano-12b-v2-vl` | ~150ms | Vision-language model |
| `nvidia/nvidia-nemotron-nano-9b-v2` | ~200ms | Reasoning optimized |
| `nvidia/nemotron-3-content-safety` | ~150ms | Safety classifier, returns "User Safety: safe" |
| `nvidia/nemotron-3.5-content-safety` | ~150ms | Safety classifier, returns "User Safety: safe" |
| `nvidia/nemotron-content-safety-reasoning-4b` | ~120ms | Chat model with reasoning (not just safety) |
| `google/diffusiongemma-26b-a4b-it` | ~100ms | **Diffusion-based LLM** — works as chat, non-autoregressive generation |

### Partner Models (Hosted on NVIDIA NIM)

| Provider | Model ID | Response Time | Notes |
|----------|----------|---------------|-------|
| **Meta** | `meta/llama-3.1-70b-instruct` | ~40ms | Fast, cached (32 tokens) |
| **Meta** | `meta/llama-3.1-8b-instruct` | ~12ms | Very fast, cached (32 tokens) |
| **Meta** | `meta/llama-3.2-11b-vision-instruct` | ~200ms | Vision-language |
| **Meta** | `meta/llama-3.2-90b-vision-instruct` | ~200ms | Large vision-language |
| **Google** | `google/gemma-2-2b-it` | ~50ms | Tiny, instant |
| **Qwen** | `qwen/qwen3.5-122b-a10b` | ~290ms | MoE 122B, reasoning |

---

## ⏱️ TIMEOUT Models (hung, no response after 60s)

| Model ID | Issue |
|----------|-------|
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | Timed out 2/2 tests — likely on slower GPU pool |
| `nvidia/llama-3.1-nemotron-nano-8b-v1` | Timed out 1/1 test |
| `meta/llama-3.3-70b-instruct` | Timed out 1/1 test |
| `meta/llama-3.2-1b-instruct` | Timed out 1/1 test |
| `meta/llama-3.2-3b-instruct` | Timed out 1/1 test |

---

## ❌ 404 NOT FOUND Models (not available for this account tier)

### NVIDIA-Owned

| Model ID | Error |
|----------|-------|
| `nvidia/llama-3.1-nemotron-70b-instruct` | `Function '9b96341b-9791-4db9-a00d-4e43aa192a39': Not found for account` |
| `nvidia/nemotron-4-340b-instruct` | `Function 'b0fcd392-e905-4ab4-8eb9-aeae95c30b37': Not found for account` |
| `nvidia/nemotron-4-340b-reward` | `Function 'c53ee0e9-bad9-4e09-b365-52c9d6b71254': Not found for account` |
| `nvidia/llama-3.1-nemotron-ultra-253b-v1` | `Function '84bf12ff-edbd-4435-baea-0fa6a7453d2e': Not found for account` |
| `nvidia/mistral-nemo-minitron-8b-8k-instruct` | `Function '5aa06dd2-0a02-4a5d-be4c-bf88e956965d': Not found for account` |
| `nvidia/nemotron-nano-3-30b-a3b` | Standard 404: `Model not found` |

### Partner Models

| Provider | Model ID | Error |
|----------|----------|-------|
| **Mistral AI** | `mistralai/mistral-7b-instruct-v0.3` | 404 Not Found |
| **Mistral AI** | `mistralai/mixtral-8x7b-instruct-v0.1` | 503 DEGRADED |
| **Mistral AI** | `mistralai/mistral-large-2-instruct` | 404 Not Found |
| **IBM** | `ibm/granite-3.0-8b-instruct` | 404 Not Found |
| **Google** | `google/gemma-3-12b-it` | 404 Not Found |
| **DeepSeek** | `deepseek-ai/deepseek-v4-flash` | 503 Resource Exhausted |
| **Microsoft** | `microsoft/phi-3.5-moe-instruct` | 404 Not Found |
| **Microsoft** | `microsoft/phi-4-mini-instruct` | Timed out |

---

## 🔧 Special Endpoint Models

### Embeddings (`/v1/embeddings`)

| Model ID | Status | Notes |
|----------|--------|-------|
| `nvidia/nv-embed-v1` | ✅ Works | 4096-dim embeddings, fast (~100ms) |
| `nvidia/llama-nemotron-embed-1b-v2` | ✅ Works | Requires `input_type: "query"` or `"passage"` |

### Non-Chat Models (require specific input format)

| Model ID | Endpoint | Notes |
|----------|----------|-------|
| `nvidia/nemotron-parse` | `/v1/chat/completions` | ❌ "Content cannot be a plain string. The model does not support text input." — requires document/image input |
| `nvidia/nemoretriever-parse` | `/v1/chat/completions` | ❌ Same — requires document input |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| ✅ Working NVIDIA chat models | 10 |
| ✅ Working partner chat models | 6 |
| ⏱️ Timeout models | 7 |
| ❌ 404 models | 14 |
| 🔧 Embedding models | 2 |
| 🔧 Special format models | 2 |
| **Total tested** | **41** |

---

## Recommended Config for `~/.hermes/config.yaml`

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: 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
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    models:
      # NVIDIA Nemotron
      - nvidia/nemotron-3-ultra-550b-a55b
      - nvidia/nemotron-3-super-120b-a12b
      - nvidia/nemotron-3-nano-30b-a3b
      - nvidia/nemotron-mini-4b-instruct
      - nvidia/llama-3.3-nemotron-super-49b-v1
      - nvidia/nemotron-nano-12b-v2-vl
      - nvidia/nvidia-nemotron-nano-9b-v2
      - nvidia/nemotron-3-content-safety
      - nvidia/nemotron-3.5-content-safety
      - nvidia/nemotron-content-safety-reasoning-4b
      # Partner models
      - meta/llama-3.1-70b-instruct
      - meta/llama-3.1-8b-instruct
      - meta/llama-3.2-11b-vision-instruct
      - meta/llama-3.2-90b-vision-instruct
      - google/gemma-2-2b-it
      - qwen/qwen3.5-122b-a10b
    name: NVIDIA
    rate_limit_rpm: 35
    concurrency_limit: 1
    max_retries: 5
    retry_delay: 10
    max_retry_delay: 160
    retry_on:
      - 429
      - 500
      - 502
      - 503
      - 504
```

---

## Test Commands (for re-verification)

```bash
# Test chat model
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-3-ultra-550b-a55b","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' \
  https://integrate.api.nvidia.com/v1/chat/completions --max-time 60

# Test embedding model
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nv-embed-v1","input":"Hello world"}' \
  https://integrate.api.nvidia.com/v1/embeddings --max-time 60

# Test asymmetric embedding model
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/llama-nemotron-embed-1b-v2","input":"Hello world","input_type":"query"}' \
  https://integrate.api.nvidia.com/v1/embeddings --max-time 60
```