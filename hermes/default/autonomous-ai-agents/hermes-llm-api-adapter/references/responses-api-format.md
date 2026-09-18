# OpenAI Responses API Format Reference

## Overview
The Responses API is OpenAI's newer API format (introduced 2024) that replaces Chat Completions for some models. Key differences:

- Endpoint: `POST /v1/responses` (not `/v1/chat/completions`)
- Request uses `input` array (not `messages`)
- Streaming uses **event-based SSE** with `event:` / `data:` pairs
- Response includes reasoning tokens, tool calls, and structured output

## Request Format

```json
{
  "model": "gpt-4o",
  "input": [
    {
      "role": "user",
      "content": [
        {"type": "input_text", "text": "Hello"}
      ]
    }
  ],
  "stream": true,
  "temperature": 1.0,
  "max_output_tokens": 1000
}
```

### Input Items
- `role`: "user", "assistant", "system", "developer"
- `content`: array of content parts
  - `type: "input_text"` with `text: string`
  - `type: "input_image"` with `image_url: string`
  - `type: "input_file"` with `file_data` or `file_id`

## Streaming Response Format

Responses API streams **events**, not simple data lines. Each event has:

```
event: response.created
data: {"response": {...}, "sequence_number": 0, "type": "response.created"}

event: response.in_progress
data: {...}

event: response.output_item.added
data: {"item": {"id": "...", "type": "message", "status": "in_progress", "content": []}, ...}

event: response.content_part.added
data: {"content_index": 0, "item_id": "...", "part": {"type": "output_text", "text": ""}, ...}

event: response.output_text.delta
data: {"content_index": 0, "delta": "Hello", "item_id": "...", ...}

event: response.content_part.done
data: {"content_index": 0, "item_id": "...", "part": {"type": "output_text", "text": "Hello world"}, ...}

event: response.output_item.done
data: {"item": {"id": "...", "type": "message", "status": "completed", "content": [...]}, ...}

event: response.completed
data: {"response": {..., "status": "completed", "usage": {...}}, ...}

data: [DONE]
```

### Key Events for Text Streaming
| Event | Purpose |
|-------|---------|
| `response.output_text.delta` | Incremental text delta (main streaming event) |
| `response.content_part.added` | New content part started |
| `response.content_part.done` | Content part complete with full text |
| `response.completed` | Full response done, includes usage |

## Non-Streaming Response

```json
{
  "id": "resp_abc123",
  "object": "response",
  "created_at": 1700000000,
  "status": "completed",
  "model": "gpt-4o",
  "output": [
    {
      "type": "message",
      "id": "msg_xyz",
      "role": "assistant",
      "content": [
        {"type": "output_text", "text": "Hello world", "annotations": []}
      ],
      "status": "completed"
    }
  ],
  "usage": {
    "input_tokens": 10,
    "output_tokens": 50,
    "total_tokens": 60,
    "output_tokens_details": {"reasoning_tokens": 0}
  }
}
```

## Meta AI Specifics
- Endpoint: `https://api.meta.ai/v1/responses`
- Model: `muse-spark-1.1`
- Auth: `Authorization: Bearer <key>`
- Always uses `reasoning.effort: "high"` (non-configurable)
- Returns reasoning output items before message items