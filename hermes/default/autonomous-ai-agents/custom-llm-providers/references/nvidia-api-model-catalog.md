# NVIDIA API Model Catalog (integrate.api.nvidia.com/v1)

**Source:** Live API query from this session (2026-07-13)
**Endpoint:** `https://integrate.api.nvidia.com/v1/models`

---

## NVIDIA Models (`nvidia/*`)

| Model ID | Description |
|----------|-------------|
| `nvidia/nemotron-3-ultra-550b-a55b` | Nemotron 3 Ultra 550B (default for Hermes config) |
| `nvidia/llama-3.1-nemotron-70b-instruct` | Llama 3.1 Nemotron 70B Instruct |
| `nvidia/llama-3.1-nemotron-51b-instruct` | Llama 3.1 Nemotron 51B Instruct |
| `nvidia/llama-3.1-nemotron-nano-8b-v1` | Llama 3.1 Nemotron Nano 8B v1 |
| `nvidia/llama-3.1-nemotron-nano-vl-8b-v1` | Llama 3.1 Nemotron Nano VL 8B v1 (vision) |
| `nvidia/llama-3.1-nemoguard-8b-content-safety` | Nemotron Guard 8B Content Safety |
| `nvidia/llama-3.1-nemoguard-8b-topic-control` | Nemotron Guard 8B Topic Control |
| `nvidia/cosmos-reason2-8b` | Cosmos Reason 2 8B |
| `nvidia/ai-synthetic-video-detector` | AI Synthetic Video Detector |
| `nvidia/embed-qa-4` | Embed QA 4 (embedding) |
| `nvidia/gliner-pii` | GLiNER PII Detection |
| `nvidia/ising-calibration-1-35b-a3b` | Ising Calibration 1.35B A3B |

---

## Third-Party Models Available via NVIDIA NIM

### Meta
- `meta/llama-4-maverick-17b-128e-instruct`
- `meta/llama-3.3-70b-instruct`
- `meta/llama-3.2-90b-vision-instruct`
- `meta/llama-3.2-11b-vision-instruct`
- `meta/llama-3.2-3b-instruct`
- `meta/llama-3.2-1b-instruct`
- `meta/llama-3.1-70b-instruct`
- `meta/llama-3.1-8b-instruct`
- `meta/codellama-70b`
- `meta/llama2-70b`
- `meta/llama-guard-4-12b`

### Google
- `google/gemma-4-31b-it`
- `google/gemma-3-12b-it`
- `google/gemma-3-4b-it`
- `google/gemma-3n-e4b-it`
- `google/gemma-3n-e2b-it`
- `google/gemma-2-2b-it`
- `google/gemma-2b`
- `google/codegemma-7b`
- `google/codegemma-1.1-7b`
- `google/diffusiongemma-26b-a4b-it`
- `google/deplot`
- `google/recurrentgemma-2b`

### Mistral AI
- `mistralai/mistral-large-3-675b-instruct-2512`
- `mistralai/mistral-large-2-instruct`
- `mistralai/mistral-large`
- `mistralai/mistral-medium-3.5-128b`
- `mistralai/mistral-small-4-119b-2603`
- `mistralai/mistral-nemotron`
- `mistralai/ministral-14b-instruct-2512`
- `mistralai/mistral-7b-instruct-v0.3`
- `mistralai/codestral-22b-instruct-v0.1`
- `mistralai/mixtral-8x22b-v0.1`
- `mistralai/mixtral-8x7b-instruct-v0.1`

### Microsoft
- `microsoft/phi-4-multimodal-instruct`
- `microsoft/phi-4-mini-instruct`
- `microsoft/phi-3.5-moe-instruct`
- `microsoft/phi-3-vision-128k-instruct`
- `microsoft/kosmos-2`

### Others
- `deepseek-ai/deepseek-v4-pro`
- `deepseek-ai/deepseek-v4-flash`
- `deepseek-ai/deepseek-coder-6.7b-instruct`
- `ibm/granite-34b-code-instruct`
- `ibm/granite-8b-code-instruct`
- `ibm/granite-3.0-8b-instruct`
- `ibm/granite-3.0-3b-a800m-instruct`
- `bytedance/seed-oss-36b-instruct`
- `databricks/dbrx-instruct`
- `ai21labs/jamba-1.5-large-instruct`
- `adept/fuyu-8b`
- `abacusai/dracarys-llama-3.1-70b-instruct`
- `01-ai/yi-large`
- `moonshotai/kimi-k2.6`
- `minimaxai/minimax-m3`
- `minimaxai/minimax-m2.7`
- `aisingapore/sea-lion-7b-instruct`
- `bigcode/starcoder2-15b`
- `baai/bge-m3`

---

## Notes

- The NVIDIA NIM endpoint acts as an aggregator — it serves both NVIDIA-optimized models (Nemotron, Nemotron Guard, etc.) AND popular open models optimized for NVIDIA GPUs.
- Model IDs follow the `owner/model-name` format (OpenAI-compatible).
- Vision models: `meta/llama-3.2-90b-vision-instruct`, `meta/llama-3.2-11b-vision-instruct`, `nvidia/llama-3.1-nemotron-nano-vl-8b-v1`, `microsoft/phi-4-multimodal-instruct`, `microsoft/phi-3-vision-128k-instruct`, `adept/fuyu-8b`
- Embedding models: `nvidia/embed-qa-4`, `baai/bge-m3`
- Specialized: `nvidia/gliner-pii` (PII detection), `nvidia/ai-synthetic-video-detector`, `nvidia/llama-3.1-nemoguard-8b-*` (guardrails)

---

## Usage in Hermes

```yaml
# ~/.hermes/config.yaml
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: ${NVIDIA_API_KEY}
    default_model: nvidia/nemotron-3-ultra-550b-a55b  # or any model ID from above
```

---

## Quick Switching

```bash
# Test a model directly via API
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/llama-3.1-nemotron-70b-instruct","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'
```