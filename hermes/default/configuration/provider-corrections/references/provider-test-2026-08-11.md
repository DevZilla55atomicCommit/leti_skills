# Provider Testing Session — 2026-08-11

## Summary
Tested all 7 configured Hermes providers for basic functionality.

| # | Provider | Status | Notes |
|---|----------|--------|-------|
| 1 | **ollama-launch** (local) | ✅ Working | `gemma4:12b`, `qwen3.5:4b`, `llava:7b` all respond |
| 2 | **ollama-cloud** | ✅ Working | `gemma4:31b-cloud` returns responses, conversation history works |
| 3 | **google-gemini** | ⚠️ Partial | `gemini-2.5-flash` deprecated; `diffusiongemma` returns empty — needs model list update |
| 4 | **openrouter** | ⚠️ Credits exhausted | API key valid but account needs credits (HTTP 402) |
| 5 | **nvidia** | ✅ Working | Current default provider — confirmed via live session |
| 6 | **bonsai-baseline** | ❌ Empty | Placeholder only |
| 7 | **meta-ai** (local gateway) | ✅ Working | Fixed adapter bugs (content type + token default); 5/5 consecutive requests work |

## Meta AI Fixes Applied
See `references/meta-ai-session-fixes-2026-08-11.md` for details.

## Ollama Cloud
No issues found. Works correctly with `gemma4:31b-cloud` model. The `-cloud` suffix is a local alias resolved by Ollama Cloud.

## Google Gemini
Needs investigation — the configured model `google/diffusiongemma-26b-a4b-it-lite` returns empty responses. May need:
- Updated model names from Google AI Studio
- Migration to new Interactions API

## OpenRouter
Account needs credits. Add at https://openrouter.ai/settings/credits

## Commands Used for Testing
```bash
# Test local Ollama
curl -s http://127.0.0.1:11434/api/tags
curl -s -X POST http://127.0.0.1:11434/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"gemma4:12b","messages":[{"role":"user","content":"Say OK"}],"max_tokens":20}'

# Test Ollama Cloud
curl -s -X POST https://ollama.com/api/chat -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"gemma4:31b-cloud","messages":[{"role":"user","content":"Say OK"}],"stream":false,"options":{"num_predict":50}}'

# Test NVIDIA
curl -s -X POST https://integrate.api.nvidia.com/v1/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"nvidia/nemotron-3-ultra-550b-a55b","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'

# Test Google Gemini
curl -s -X POST https://generativelanguage.googleapis.com/v1beta/models/google/diffusiongemma-26b-a4b-it-lite:generateContent -H "x-goog-api-key: $KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Say OK"}]}],"generationConfig":{"maxOutputTokens":50}}'

# Test OpenRouter
curl -s -X POST https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"anthropic/claude-sonnet-4.6","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'

# Test Meta AI adapter
curl -s -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"muse-spark-1.1","messages":[{"role":"user","content":"Say OK"}]}'
```