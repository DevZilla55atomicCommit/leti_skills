# NVIDIA NIM Setup for TONY

## Get API Key

1. Go to https://build.nvidia.com
2. Sign in with NVIDIA account (or create one)
3. Navigate to "API Keys" → "Generate API Key"
4. Copy the key (starts with `nvapi-`)

## Available Models (NIM) — Free Tier Status

| Model ID | Description | Context | Best For | Free Tier |
|----------|-------------|---------|----------|-----------|
| `nvidia/nemotron-3-ultra-550b-a55b` | Nemotron 3 Ultra (RECOMMENDED) | 4k | Complex reasoning, tool calling | ✅ **Works** |
| `meta/llama-3.1-70b-instruct` | Llama 3.1 70B Instruct | 128k | General reasoning, coding | ❌ **403 Forbidden** |
| `meta/llama-3.1-8b-instruct` | Llama 3.1 8B Instruct | 128k | Faster, lighter tasks | ❓ Untested |
| `nvidia/nemotron-3-ultra` | Nemotron 3 Ultra (legacy name) | 4k | Complex reasoning | ✅ Works |
| `mistralai/mistral-large` | Mistral Large | 32k | Multilingual, coding | ✅ Works |
| `google/gemma-2-27b-it` | Gemma 2 27B | 8k | Instruction following | ✅ Works |

**Default for TONY:** `nvidia/nemotron-3-ultra-550b-a55b` — confirmed working on free tier with tool calling.

## TONY Configuration

Add to `.env`:

```bash
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b
TONY_LLM_PROVIDER=nvidia
```

**Critical:** Gateway must be started with explicit `NVIDIA_API_KEY` to override inherited shell env vars:

```bash
cd ~/tony-ai-agent
NVIDIA_API_KEY=$(grep NVIDIA_API_KEY .env | cut -d= -f2) node src/gateway/server.js
```

## Rate Limits (Free Tier)

- **Requests**: 1,000/day
- **Tokens**: 100,000/day
- **Concurrent**: 5 requests
- **Models**: All NIM models available

## Paid Tier (NVIDIA AI Enterprise)

- Higher rate limits
- SLA guarantees
- Private endpoints
- Contact NVIDIA sales

## Testing NIM Connection

```bash
# List available models
curl -H "Authorization: Bearer $NVIDIA_API_KEY" \
  https://integrate.api.nvidia.com/v1/models

# Test chat completion
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3-ultra-550b-a55b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

## TONY Provider Module

Created: `src/llm/nvidia.js`
- OpenAI-compatible `/chat/completions` endpoint
- Tool/function calling support
- 120s timeout for long completions
- `isAvailable()` checks `/models` endpoint

## Fallback Chain

When NVIDIA fails (rate limit, network, auth):
1. **Ollama** (local `qwen3.5:4b-mlx`)
2. **Jan.ai** (if running on `:1337`)
3. **Mock** (deterministic test responses)

## Cost Comparison

| Provider | Cost | Speed | Privacy |
|----------|------|-------|---------|
| NVIDIA NIM | Free tier / pay | ~2-3s | Cloud |
| Ollama | Free (local HW) | ~15-20s | Full |
| Jan.ai | Free (local) | ~10-15s | Full |

## Troubleshooting

| Error | Fix |
|-------|-----|
| 401 Unauthorized | Check API key format (`nvapi-...`) |
| 429 Rate Limited | Wait, or use smaller model for higher quota |
| 503 Unavailable | NIM endpoint down; fallback to Ollama activates |
| Timeout | Reduce `TONY_MAX_CONTEXT_TOKENS` or use smaller model |
| **403 "Authorization failed"** | **Inherited shell `NVIDIA_API_KEY` placeholder overrode `.env`. Start gateway with explicit key: `NVIDIA_API_KEY=$(grep NVIDIA_API_KEY .env | cut -d= -f2) node src/gateway/server.js`** |
| **Anthropic "invalid x-api-key" despite using NVIDIA** | **Inherited `ANTHROPIC_API_KEY=ollama` (from Hermes/Claude Code) polluted provider chain. Fix: `isValidApiKey()` in `src/llm/index.js` rejects "ollama", "none", "dummy", etc. Or unset before launch: `unset ANTHROPIC_API_KEY`** |
| **Provider chain shows anthropic despite TONY_LLM_PROVIDER=nvidia** | Same as above - env var inheritance causes false truthy key. `isValidApiKey()` filter is the permanent fix. |

## Model Selection Guide

- **Nemotron 3 Ultra (550B)**: Best for complex reasoning chains, tool calling — **recommended default**
- **Nemotron 3 Ultra (legacy name)**: Same as above
- **Mistral Large**: Strong multilingual, good for non-English
- **Gemma 2 27B**: Good instruction following
- **Llama 3.1 70B**: ❌ Does NOT work on free tier (403)
- **Llama 3.1 8B**: ❓ Untested on free tier