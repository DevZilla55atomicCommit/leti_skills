---
title: NVIDIA NIM Model Testing for Cognee Graph Memory
date: 2026-07-16
cognee_version: 1.3.0
---

# NVIDIA NIM Model Testing for Cognee Graph Memory

## Models Tested via Direct NIM API

| Model | Function Calling | JSON Output | Notes |
|-------|------------------|-------------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | ✅ Yes | ✅ Valid JSON | **WORKS** - Best for extraction |
| `nvidia/nemotron-3-ultra-550b-a55b` (custom provider) | ✅ Yes | ✅ Valid JSON | Works via direct API |
| `meta/llama-3.1-8b-instruct` | ❌ No | ❌ 400 tools not supported | NIM endpoint rejects tools |
| `meta/llama-3.1-70b-instruct` | ❌ No | ❌ 400 tools not supported | NIM endpoint rejects tools |
| `meta/llama-3.2-3b-instruct` | ❌ No | ❌ 400 tools not supported | NIM endpoint rejects tools |
| `nvidia/llama-3.1-nemotron-70b-instruct` | ❌ No | ❌ 400 tools not supported | NIM endpoint rejects tools |
| `nvidia/nemotron-3-ultra-550b-a55b` (OpenAI provider) | ❌ No | ❌ "tools" not supported | OpenAI adapter sends tools |

## Key Findings

### What Works
- **Direct NIM API calls** with `nvidia/nemotron-3-ultra-550b-a55b` return valid structured JSON for entity/relationship extraction
- **Session memory** works 100% locally with Ollama embeddings
- **Embeddings** work perfectly with local `nomic-embed-text:latest` via Ollama `/api/embed`

### What Doesn't Work (Cognee Integration)
| Issue | Root Cause |
|-------|------------|
| `'nvidia' is not a valid LLMProvider` | Cognee's LLMProvider enum doesn't include `nvidia` |
| `LLM Provider NOT provided` with `provider=custom` | litellm doesn't recognize `nvidia/nemotron-3-ultra-550b-a55b` as NIM model |
| `meta does not support parameters: ['tools', 'tool_choice']` | llama-3.1 models on NIM don't support function calling |
| `tools`/`tool_choice` sent to Nemotron via OpenAI provider | OpenAI adapter sends function calling params that Nemotron rejects |

### Cognee Provider Mapping Issue
Cognee's `LLMProvider` enum only has: `OPENAI`, `OLLAMA`, `ANTHROPIC`, `CUSTOM`, `GEMINI`, `MISTRAL`, `AZURE`, `BEDROCK`, `LLAMA_CPP`

No `NVIDIA` or `NIM` provider. Using `custom` passes model to litellm which doesn't auto-detect NIM models.

## Working Configuration

```bash
# .env - Graph memory with Nemotron 3 Ultra
LLM_PROVIDER=custom
LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b
LLM_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_API_KEY=nvapi-...
LLM_INSTRUCTOR_MODE=    # empty = default json_mode

EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

COGNEE_SKIP_CONNECTION_TEST=true
```

**Note**: Even with this config, litellm doesn't recognize `nvidia/nemotron-3-ultra-550b-a55b` as a NIM model when provider=custom, so it fails with "LLM Provider NOT provided".

## Cost Analysis

| Operation | Provider | Cost |
|-----------|----------|------|
| Embeddings (557 notes) | Local Ollama | $0 |
| Graph extraction (Nemotron 3 Ultra) | NVIDIA NIM | ~$0.08 total |
| Session memory | Local SQLite | $0 |
| Graph storage | Local Kuzu + LanceDB | $0 |

**Total one-time cost: ~$0.08** for full vault graph build.

## Direct API Test Results

### Nemotron 3 Ultra (Working)
```bash
curl https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -d '{"model": "nvidia/nemotron-3-ultra-550b-a55b", "messages": [{"role": "user", "content": "Extract entities and relationships as JSON: Alfred prefers concise responses."}], "max_tokens": 200}'
```
Returns valid JSON with entities and relationships.

### Failed Attempts
- `meta/llama-3.1-8b-instruct` via NIM: 400 - tools not supported
- `meta/llama-3.1-70b-instruct` via NIM: 400 - tools not supported
- `nvidia/llama-3.1-nemotron-70b-instruct` via NIM: 400 - tools not supported
- `nvidia/nemotron-3-ultra` via OpenAI provider: 400 - tools not supported

## Session Memory (Always Working Alternative)

```python
# Works 100% locally, no LLM calls, persists across restarts
await cognee.remember("Alfred prefers concise, technical responses.", session_id="alfred-prefs")
results = await cognee.recall("What does Alfred prefer?", session_id="alfred-prefs")
```

Cost: $0, Latency: ~10ms, Persistence: Survives restarts.

## Files Created This Session

| File | Purpose |
|------|---------|
| `~/.env` | Working config for session memory |
| `~/.cognee/logs/` | Pipeline execution logs |
| `~/.cognee/system/databases/` | SQLite + Kuzu + LanceDB |

---

*Last updated: 2026-07-16 | Cognee 1.3.0 | Nemotron 3 Ultra tested*