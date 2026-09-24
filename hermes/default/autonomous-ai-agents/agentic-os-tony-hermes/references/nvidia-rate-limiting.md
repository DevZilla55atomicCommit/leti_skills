# NVIDIA NIM Rate Limiting Configuration

This document captures the dual-layer rate limiting setup for NVIDIA NIM models configured during the session on 2026-07-09.

## Problem
NVIDIA NIM free tier enforces **40 RPM (requests per minute)** with 429 errors when exceeded. Multiple concurrent requests from Hermes Agent + LiteLLM proxy caused frequent 429s.

## Solution: Dual-Layer Rate Limiting

### Layer 1: Hermes Native Provider Config (`~/.hermes/config.yaml`)

```yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
    models:
      - nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
    name: NVIDIA
    rate_limit_rpm: 35          # 5 RPM safety buffer below 40
    concurrency_limit: 1        # Only 1 concurrent request
    max_retries: 5
    retry_delay: 10
    max_retry_delay: 160
    retry_on:
      - 429
      - 500
      - 502
      - 503
      - 504
    retry_jitter: 0.2
```

**Models with Hermes native rate limiting: 1**
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

### Layer 2: LiteLLM Proxy Config (`~/.config/litellm/config.yaml`)

```yaml
model_list:
  - model_name: local-ollama
    litellm_params:
      model: ollama/qwen3.5-32k:latest
      api_base: http://localhost:11434

  - model_name: nvidia-nano
    litellm_params:
      model: nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning
      api_key: os.environ/NVIDIA_API_KEY
      api_base: https://integrate.api.nvidia.com/v1
      custom_llm_provider: openai
    rpm: 35
    max_parallel_requests: 1

  - model_name: nvidia-ultra
    litellm_params:
      model: nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b
      api_key: os.environ/NVIDIA_API_KEY
      api_base: https://integrate.api.nvidia.com/v1
      custom_llm_provider: openai
    rpm: 35
    max_parallel_requests: 1

  - model_name: zai-glm-5-2
    litellm_params:
      model: z-ai/glm-5.2
      api_key: os.environ/NVIDIA_API_KEY
      api_base: https://integrate.api.nvidia.com/v1
      custom_llm_provider: openai
    rpm: 35
    max_parallel_requests: 1

litellm_settings:
  drop_params: true
```

**Models with LiteLLM rate limiting: 3**
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` (via `nvidia-nano` alias)
- `nvidia/nemotron-3-ultra-550b-a55b` (via `nvidia-ultra` alias)
- `z-ai/glm-5.2` (via `zai-glm-5-2` alias)

## Request Flow & Queue Behavior

| Layer | Rate Limit | Concurrency | Queuing Behavior |
|-------|------------|-------------|------------------|
| Hermes native | 35 RPM | 1 | Requests queue in Hermes before hitting API |
| LiteLLM proxy | 35 RPM | 1 | Requests queue in LiteLLM before hitting NVIDIA |
| NVIDIA NIM | 40 RPM | N/A | Hard limit enforced by provider |

**Effective throughput**: ~35 RPM with 1 concurrent request, providing 5 RPM buffer.

## Key Findings

1. **Hermes native path works correctly** — bypasses LiteLLM, uses exact model IDs from `/v1/models`, rate limits enforced by Hermes' built-in tracker (`rate_limit_tracker.py`)

2. **LiteLLM NVIDIA NIM provider has bugs** —
   - Without `nvidia_nim/` prefix: "LLM Provider NOT provided"
   - With `nvidia_nim/` prefix: 403 "Authorization failed" (sends wrong model name)
   - With `custom_llm_provider: openai`: Works but requires `nvidia_nim/` prefix in model name

3. **Direct NVIDIA API works** — `curl` to `https://integrate.api.nvidia.com/v1/chat/completions` with exact model ID (e.g., `z-ai/glm-5.2`) succeeds

4. **Full 122-model config generated but not persisted** — The complete list from `/v1/models` was fetched and configured but LiteLLM crashed on restart. Current minimal config has 3 test models.

## Recommendation

**Use Hermes native NVIDIA provider** for production — it:
- Uses exact model IDs from NVIDIA's `/v1/models` endpoint
- Has proper rate limiting with exponential backoff
- Bypasses LiteLLM entirely (fewer moving parts)
- Works with all 122+ NVIDIA NIM models

Only use LiteLLM for multi-provider fallback (Ollama, Anthropic, OpenRouter) where Hermes native doesn't have a provider.

## Reverting

```bash
# Restore original LiteLLM config
cp ~/.config/litellm/config.yaml.backup ~/.config/litellm/config.yaml

# Restart LiteLLM
pkill -f "litellm.*config.yaml"
litellm --config ~/.config/litellm/config.yaml --port 4000 &
```

## Files Modified This Session

| File | Change |
|------|--------|
| `~/.hermes/config.yaml` | Added `rate_limit_rpm: 35`, `concurrency_limit: 1`, retry config to `providers.nvidia` |
| `~/.config/litellm/config.yaml` | Created minimal 3-model config with `rpm: 35`, `max_parallel_requests: 1` |
| `~/.config/litellm/config.yaml.backup` | Original 2-model config preserved |