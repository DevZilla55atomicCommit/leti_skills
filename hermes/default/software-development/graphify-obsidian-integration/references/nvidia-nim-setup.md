# NVIDIA NIM Setup for Graphify

Graphify supports any OpenAI-compatible API. NVIDIA NIM provides this interface for both cloud and local models.

## Quick Start: NVIDIA Cloud API

```bash
# 1. Get API key from https://build.nvidia.com → API Keys
export NVIDIA_API_KEY="nvapi-..."

# 2. Configure OpenAI-compatible env vars
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

# 3. Test
curl -s "$OPENAI_BASE_URL/models" -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id'

# 4. Run Graphify
graphify "/path/to/vault" \
  --backend openai \
  --model "$OPENAI_MODEL" \
  --obsidian --obsidian-dir "/path/to/vault/Graphify-Output"
```

## Model Selection

| Model ID | Params | Vision? | Quality | Speed | Use Case |
|----------|--------|---------|---------|-------|----------|
| `nvidia/nemotron-3-ultra-550b-a55b` | 550B MoE | ❌ NO | ⭐⭐⭐ Best | Slow | **Text-only** extraction, naming, reasoning |
| `nvidia/nemotron-3-super-120b-a12b` | 120B MoE | ❌ NO | ⭐⭐ Great | Medium | **Text-only** balanced quality/speed |
| `nvidia/llama-3.1-nemotron-70b-instruct` | 70B | ❌ NO | ⭐⭐ Good | Fast | **Text-only** general purpose |
| **`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`** | 30B | ✅ YES | ⭐⭐ Good | Medium | **Images + text** — only Nemotron with vision |
| **`meta/llama-3.2-90b-vision-instruct`** | 90B | ✅ YES | ⭐⭐⭐ Best | Slow | **Images + text** — largest vision model |
| `meta/llama-3.2-11b-vision-instruct` | 11B | ✅ YES | ⭐⭐ Good | Fast | Lightweight vision |

> ⚠️ **CRITICAL**: If your vault contains images, GIFs, or PDFs, you MUST use a vision-capable model (marked ✅ YES above). Text-only models (Nemotron 3 Ultra/Super, Nemotron 70B) will fail on every image chunk with `400: multimodal processing not enabled` errors. The error mentions "--enable-multimodal flag" — THIS FLAG DOES NOT EXIST; it's a model capability.

## TamaZila Vault Specific — Model Choice

The TamaZila Obsidian Vault contains **large GIF files (10–100 MB)** from Instagram Reels frame extraction in the DaVinci Knowledge Base:

```bash
# For FULL vault (with images): USE VISION MODEL
export OPENAI_MODEL="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
# OR
export OPENAI_MODEL="meta/llama-3.2-90b-vision-instruct"

# For CODE-ONLY graph (no images): BEST TEXT MODEL
# export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

# Run with chosen model
graphify "/Volumes/PNY128GBLED/TamaZila Obsidian Vault" \
  --backend openai \
  --model "$OPENAI_MODEL" \
  --obsidian \
  --obsidian-dir "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Graphify-FullVault"
```

> **Note**: Large GIFs (>5 MB) are auto-skipped for inline vision analysis even with vision models — they become reference nodes only. For full frame analysis, extract key frames as <5 MB JPGs before indexing.

## Local NIM (Self-Hosted, Unlimited)

```bash
# Pull and run (requires NVIDIA GPU + Docker)
docker pull nvcr.io/nim/meta/llama-3.1-70b-instruct
docker run -d --gpus all -p 8000:8000 nvcr.io/nim/meta/llama-3.1-70b-instruct

# Configure
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="local-key"  # any non-empty string
export OPENAI_MODEL="meta/llama-3.1-70b-instruct"

# Run Graphify
graphify "/path/to/vault" --backend openai --model "$OPENAI_MODEL" --obsidian --obsidian-dir "..."
```

## Environment Variables for Persistence

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# NVIDIA Cloud
export NVIDIA_API_KEY="nvapi-..."
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

# Or Local NIM (uncomment when running local)
# export OPENAI_BASE_URL="http://localhost:8000/v1"
# export OPENAI_API_KEY="local-key"
# export OPENAI_MODEL="meta/llama-3.1-70b-instruct"
```

## TamaZila Vault Specific

```bash
# Full vault graph with Nemotron 3 Ultra
export NVIDIA_API_KEY="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"
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

graphify "/Volumes/PNY128GBLED/TamaZila Obsidian Vault" \
  --backend openai \
  --model "$OPENAI_MODEL" \
  --obsidian \
  --obsidian-dir "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Graphify-FullVault"
```

## Key Differences: Cloud vs Local

| Aspect | NVIDIA Cloud | Local NIM |
|--------|--------------|-----------|
| **API Key** | Required (`nvapi-...`) | Any string works |
| **Rate Limits** | Yes (free tier) | None |
| **GPU Required** | No | Yes (24GB+ VRAM for 70B) |
| **Latency** | Network dependent | Local, very low |
| **Cost** | Free tier / pay per token | Hardware + electricity |
| **Model Selection** | All NVIDIA models | Only what you deploy |

## Troubleshooting

```bash
# Test cloud endpoint
curl -s "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/nemotron-3-ultra-550b-a55b", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}'

# Test local NIM
curl -s "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer local-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "meta/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}'

# If model not found error:
# 1. List available models first
# 2. Use exact model ID from list
```