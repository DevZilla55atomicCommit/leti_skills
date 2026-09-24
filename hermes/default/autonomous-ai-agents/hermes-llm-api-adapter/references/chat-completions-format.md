# OpenAI Chat Completions Format Reference

## Overview
The standard format Hermes expects for all LLM providers. Used by OpenAI, OpenRouter, Anthropic (via proxy), Ollama, etc.

## Request Format

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
  ],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 1.0
}
```

### Messages
- `role`: "system", "user", "assistant", "tool"
- `content`: string OR array of content parts (for multimodal)
  - `{"type": "text", "text": "..."}`
  - `{"type": "image_url", "image_url": {"url": "..."}}`

## Streaming Response Format (SSE)

Simple `data:` lines, each a complete JSON object:

```
data: {"id": "chatcmpl-abc", "object": "chat.completion.chunk", "created": 1700000000, "model": "gpt-4o", "choices": [{"index": 0, "delta": {"role": "assistant", "content": "Hello"}, "finish_reason": null}]}

data: {"id": "chatcmpl-abc", "object": "chat.completion.chunk", "created": 1700000000, "model": "gpt-4o", "choices": [{"index": 0, "delta": {"content": " world"}, "finish_reason": null}]}

data: {"id": "chatcmpl-abc", "object": "chat.completion.chunk", "created": 1700000000, "model": "gpt-4o", "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}

data: [DONE]
```

### Chunk Structure
| Field | Description |
|-------|-------------|
| `id` | `chatcmpl-<unique>` |
| `object` | `"chat.completion.chunk"` |
| `created` | Unix timestamp |
| `model` | Model name |
| `choices[].index` | Always 0 for single choice |
| `choices[].delta` | Incremental content |
| `choices[].delta.role` | Only in first chunk: `"assistant"` |
| `choices[].delta.content` | Text delta |
| `choices[].finish_reason` | `null` (streaming) or `"stop"` / `"length"` / `"tool_calls"` |

## Non-Streaming Response

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "gpt-4o",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello world"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## Key Differences from Responses API

| Aspect | Chat Completions | Responses API |
|--------|------------------|---------------|
| Endpoint | `/v1/chat/completions` | `/v1/responses` |
| Input field | `messages[]` | `input[]` |
| Content format | `content: string` or `content[]` | `content: [{type, text}]` |
| Streaming | Simple `data: {}` lines | Event-based `event:` / `data:` |
| Text delta | `choices[].delta.content` | `response.output_text.delta` |
| Final signal | `finish_reason: "stop"` | `response.completed` event |
| Usage | Top-level `usage` | In `response.completed` data |

## Adapter Translation Checklist

When building an adapter from Responses API → Chat Completions:

- [ ] Convert `messages[]` → `input[]` with `type: "input_text"`
- [ ] Strip/ignore unknown fields (Hermes sends `options`, `service_tier`, etc.)
- [ ] Parse `event: response.output_text.delta` for streaming deltas
- [ ] Emit proper SSE: `data: {json}\n\n` (double newline!)
- [ ] First chunk includes `"delta": {"role": "assistant", "content": "..."}`
- [ ] Subsequent chunks: `"delta": {"content": "..."}`
- [ ] Final chunk: `"delta": {}, "finish_reason": "stop"`
- [ ] End with `data: [DONE]\n\n`
- [ ] Map usage: `input_tokens` → `prompt_tokens`, `output_tokens` → `completion_tokens`
- [ ] Set `timeout=None` on httpx for streaming requests