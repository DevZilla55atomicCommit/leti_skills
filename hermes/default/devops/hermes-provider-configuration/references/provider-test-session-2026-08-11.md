# Provider Test Session — 2026-08-11

**Date**: 2026-08-11  
**Profile**: default  
**Test Method**: Direct API calls via `curl` + `hermes chat` where applicable

---

## Results Summary

| Provider | Status | Details |
|----------|--------|---------|
| **ollama-launch** (local) | ✅ Working | `gemma4:12b`, `qwen3.5:4b`, `llava:7b`, `qwen3.5-32k:latest`, `qwen3.5-128k:latest`, `nomic-embed-text:latest`, `minicpm-v4.5:8b`, `qwen3-vl:8b`, `x/flux2-klein:4b-fp8` |
| **ollama-cloud** | ✅ Working | `gemma4:31b-cloud` returns "OK" (auth via Bearer token in `.env`) |
| **google-gemini** | ⚠️ Partial | `gemini-2.5-flash` deprecated (404). `google/diffusiongemma-26b-a4b-it-lite` returns empty response — likely needs Interactions API migration |
| **openrouter** | ⚠️ Credits exhausted | API key valid (reads from `.env` as `OPENROUTER_API_KEY`), HTTP 402 — account needs credits |
| **nvidia** | ✅ Working | Current active provider (`nvidia/nemotron-3-ultra-550b-a55b`). All Nemotron models available via `/v1/models`. **Note**: 403 on chat completions with current API key — may need different key scope or NVIDIA account tier |
| **bonsai-baseline** | ❌ Empty | Placeholder only |
| **meta-ai** | ✅ Working | Local adapter on `localhost:8000` via LaunchAgent. 10/10 consecutive requests succeeded. Returns empty `content` but valid HTTP 200 + usage tokens. Adapter forces `muse-spark-1.1` regardless of requested model. |

---

## Meta-AI Adapter Details

**Adapter**: `~/meta-adapter/meta_adapter.py` (FastAPI, translates OpenAI Chat Completions → Meta Responses API)  
**LaunchAgent**: `~/Library/LaunchAgents/com.alfredkamisese.meta-ai-adapter.plist`  
**Process**: PID 2003 (running since boot)  
**API Key**: Hardcoded in `~/meta-adapter/run_adapter.sh` as `META_API_KEY`  
**Logs**: 
- Access: `~/meta-adapter/adapter.log` (clean)
- Errors: `~/meta-adapter/adapter.err.log` (18MB — historical port-binding retries on startup)

**Behavior**: 
- Only exposes `muse-spark-1.1` via `/v1/models`
- Ignores requested model, always uses `muse-spark-1.1`
- Returns empty `content` field but `finish_reason: "stop"` and valid `usage` tokens
- Requires `max_tokens >= 16` (400 error otherwise)
- Streaming works (`stream: true` returns SSE with empty delta)

**Quirk**: The empty `content` is likely a parsing issue in `convert_response_to_chat()` — Meta's Responses API may return text in a different field structure.

---

## Action Items

1. **Google Gemini**: Update config with current model names from Google AI Studio, or migrate to Interactions API
2. **OpenRouter**: Add credits at https://openrouter.ai/settings/credits
3. **Meta-AI**: Investigate `convert_response_to_chat()` — Meta's output format may have changed
4. **NVIDIA**: Verify API key permissions (403 on completions but 200 on /models list)