# NVIDIA NIM Provider Configuration for Hermes

## Correct: Hermes Native Provider

**File:** `~/.hermes/config.yaml`

```yaml
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia
  base_url: https://integrate.api.nvidia.com/v1

providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: nvapi-xxxxxxxxxxxxxxxxxxxxxxxx   # Raw API key, NOT Bearer format
    default_model: nvidia/nemotron-3-ultra-550b-a55b
    name: NVIDIA
    concurrency_limit: 1          # CRITICAL: prevents burst 429s
    rate_limit_rpm: 35            # Safety buffer (< actual 40 RPM limit)
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

## Key Points

| Setting | Why |
|---------|-----|
| `concurrency_limit: 1` | NVIDIA NIM enforces strict per-key concurrency; >1 causes instant 429 |
| `rate_limit_rpm: 35` | Actual limit is 40 RPM; 35 leaves safety margin |
| `retry_on: [429, 5xx]` | Automatic backoff on rate limits & server errors |
| `api_key` format | Raw `nvapi-...` key, **not** `Bearer nvapi-...` in config |

## Wrong: LiteLLM Gateway (Don't Use)

```yaml
# ~/.config/litellm/config.yaml - AVOID FOR NVIDIA
model_list:
  - model_name: nvidia-nemotron
    litellm_params:
      model: nvidia/nemotron-3-ultra-550b-a55b
      api_key: os.environ/NVIDIA_API_KEY
      api_base: https://integrate.api.nvidia.com/v1
      custom_llm_provider: openai   # Bug: wrong provider routing
```

**Problems with LiteLLM for NVIDIA:**
1. Dual-path conflict (native + gateway both try to serve)
2. Model switching mid-session (fallback triggers)
3. `custom_llm_provider: openai` doesn't handle NVIDIA auth correctly
4. Rate limits applied per-gateway, not per-key → confusion

## Verification

```bash
# Test API key directly
curl -s -H "Authorization: Bearer $NVIDIA_API_KEY" \
  https://integrate.api.nvidia.com/v1/models | jq '.data[] | select(.id | contains("nemotron")) | .id'

# Test via Hermes
hermes chat -q "Hello" -m nvidia/nemotron-3-ultra-550b-a55b
```

## Available Models (as of 2025)

| Model ID | Params | Type | Notes |
|----------|--------|------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | 550B | Hybrid Mamba+Attn | Flagship |
| `nvidia/nemotron-3-super-120b-a12b` | 120B | Hybrid MoE | 12B active |
| `nvidia/nemotron-3-nano-omni-30b-a3b` | 30B | Multimodal | Omni (text+audio) |
| `nvidia/llama-3.1-nemotron-70b-instruct` | 70B | Llama-3.1 base | Strong reasoning |
| `nvidia/nemotron-4-340b-instruct` | 340B | Dense | Largest |
| `nvidia/nemotron-4-340b-reward` | 340B | Reward model | RLHF |

## Rate Limits (per API key)

| Tier | RPM | TPM | Notes |
|------|-----|-----|-------|
| Free/Developer | 40 | 20,000 | Standard |
| Enterprise | Custom | Custom | Contact NVIDIA |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Immediate 429 | `concurrency_limit` missing | Add `concurrency_limit: 1` |
| Model switches to qwen/llama | LiteLLM fallback active | Remove LiteLLM NVIDIA configs |
| "Invalid API key" | Bearer prefix in config | Use raw `nvapi-...` key |
| Slow first token | Cold start on NIM | Expected; subsequent tokens fast |

## References

- [NVIDIA NIM API Docs](https://docs.nvidia.com/nim/)
- [Hermes Provider Config](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- TurboQuant-MLX Nemotron support: `references/turboquant-streaming.md`