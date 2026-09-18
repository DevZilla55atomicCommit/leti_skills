# Ollama v0.14.0+ Native Anthropic Compatibility (No Proxy Needed)

**Discovery from this session:** Ollama v0.14.0 (Jan 16, 2026) added **native Anthropic Messages API** support. This eliminates the need for LiteLLM or any proxy when using Claude Code with Ollama.

## Key Finding

| Before (v0.13.x) | After (v0.14.0+) |
|------------------|------------------|
| Ollama spoke OpenAI format only | Ollama speaks **Anthropic format natively** |
| Required LiteLLM proxy for translation | **Direct connection works** |
| `ANTHROPIC_BASE_URL=http://localhost:11434/v1` | `ANTHROPIC_BASE_URL=http://localhost:11434` (no `/v1`) |

## Verified Working Config

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export OLLAMA_CONTEXT_LENGTH=131072  # Critical: default is 4K

claude --model qwen3-coder
```

## Supported Features (Per Ollama Docs)

- Full Messages API compatibility
- Streaming (`message_start`, `content_block_delta`, `message_stop`)
- System prompts (string & array)
- Multi-turn conversations
- Vision (base64 images)
- Tools / function calling (`tool_use`, `tool_result`)
- Thinking / extended thinking blocks
- All standard request/response fields

## Not Supported

- Prompt caching
- Token counts are approximations

## Official Sources

- Ollama Blog: https://ollama.com/blog/claude (Jan 16, 2026)
- Ollama API Docs: https://docs.ollama.com/api/anthropic-compatibility

## Impact on Custom Providers Skill

This means **Ollama is now a first-class native provider** for Claude Code — no translation layer needed. The `custom-llm-providers` skill should reference this as the recommended path for Ollama users, reserving LiteLLM for providers that DON'T speak Anthropic format (vLLM, LM Studio, llama.cpp server, etc.).

## Test Command

```bash
# Direct Anthropic-format test
curl -X POST http://localhost:11434/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ollama" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"qwen3-coder","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
```

## Related to This Session's Error

The "API Error: The response stopped arriving" error was caused by **context window overflow** (128K model vs 140K+ auto-compact trigger), NOT by format mismatch. The native endpoint works correctly — the issue is context management.