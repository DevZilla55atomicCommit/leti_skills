# Ollama Anthropic API Compatibility — Official Reference

**Source:** https://ollama.com/blog/claude (Jan 16, 2026) and https://docs.ollama.com/api/anthropic-compatibility

## What Changed

Ollama v0.14.0+ exposes a **native Anthropic Messages API** at `http://localhost:11434/v1/messages`.

## Supported Features

- Messages API (full compatibility)
- Streaming (`message_start`, `content_block_delta`, `message_stop`, etc.)
- System prompts (string or array)
- Multi-turn conversations
- Vision (images as base64)
- Tools / function calling (`tool_use`, `tool_result` blocks)
- Thinking / extended thinking blocks
- All standard request fields: `model`, `max_tokens`, `messages`, `system`, `stream`, `temperature`, `top_p`, `top_k`, `stop_sequences`, `tools`, `thinking`, `tool_choice`, `metadata`

## Not Supported / Partial

- **Prompt caching** — not supported
- Token counts are approximations based on underlying tokenizer
- `anthropic-version` header accepted but ignored
- API key accepted but not validated

## Using with Claude Code

### Quick Setup (Ollama v0.14.5+)

```bash
ollama launch claude          # Interactive model selector + auto-config + launch
ollama launch claude --model qwen3-coder
ollama launch claude --config # Configure without launching
```

### Manual Setup

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_API_KEY=""
export OLLAMA_CONTEXT_LENGTH=65536  # Critical: default is 4K

claude --model qwen3-coder
```

### Recommended Models (from Ollama docs)

| Model | Params | VRAM (Q4) | Context | Notes |
|-------|--------|-----------|---------|-------|
| `qwen3-coder` | 30B | ~24 GB | 128K | **Best for coding** |
| `glm-4.7-flash` | 9B | ~8 GB | 128K | Fast, balanced |
| `gpt-oss:20b` | 20B | ~13 GB | 128K | Strong general |
| `qwen2.5-coder:7b` | 7B | ~4 GB | 32K | Low VRAM |
| `glm-4.7:cloud` | Cloud | 0 GB | 128K | No GPU needed |

## Test Endpoint Directly

```bash
curl -X POST http://localhost:11434/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ollama" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"qwen3-coder","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
```

## Verification

```bash
# Ollama version (must be 0.14.0+)
ollama version

# List models via Anthropic-compatible endpoint
curl -s http://localhost:11434/v1/models | jq '.data[].id'

# Check model's actual context
ollama show qwen3-coder --parameters | grep num_ctx
```

## Related: Anthropic Docs

- LLM Gateways: https://docs.anthropic.com/en/docs/claude-code/llm-gateway
- Model Configuration: https://docs.anthropic.com/en/docs/claude-code/model-config
- Authentication: https://docs.anthropic.com/en/docs/claude-code/iam
- `ANTHROPIC_BASE_URL` redirects all requests
- `ANTHROPIC_AUTH_TOKEN` + empty `ANTHROPIC_API_KEY` required for gateway/proxy
- Model aliases (`sonnet`, `opus`, `haiku`, `fable`) can be mapped via `ANTHROPIC_DEFAULT_*_MODEL` env vars