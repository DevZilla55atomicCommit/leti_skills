---
name: hermes-llm-api-adapter
description: "Build adapter proxies for non-OpenAI LLM APIs for Hermes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, provider, adapter, proxy, llm-api, responses-api, chat-completions, integration]
    related_skills: [hermes-agent]
---

# Hermes LLM API Adapter Pattern

When an LLM provider uses a non-standard API format (e.g., OpenAI's **Responses API** at `/v1/responses` with `input[]`), Hermes cannot call it directly — Hermes expects the standard **Chat Completions** format (`/v1/chat/completions` with `messages[]`).

**Solution:** Deploy a lightweight FastAPI adapter proxy that translates between the two formats.

---

## When to Use

- Provider uses OpenAI Responses API (`/v1/responses`, `input` array, event-based SSE streaming)
- Provider has custom request/response format incompatible with OpenAI Chat Completions
- You have an API key but no native Hermes provider plugin exists
- You want to use a model via its native API rather than through a gateway (OpenRouter, etc.)

---

## Architecture

```
Hermes (Chat Completions) ──HTTP──► Adapter (FastAPI) ──HTTP──► Provider (Responses API / Custom)
       ▲                                                                    │
       │─────────────── translated SSE stream ──────────────────────────────┘
```

The adapter:
1. Receives `POST /v1/chat/completions` from Hermes
2. Converts `messages[]` → provider's input format
3. Forwards to provider's endpoint
4. Parses provider's streaming format (SSE events, JSON lines, etc.)
5. Emits OpenAI SSE format (`chat.completion.chunk`) back to Hermes

---

## Minimal Adapter Template

See `templates/meta_responses_adapter.py` for a production-ready example targeting Meta's `muse-spark-1.1` (Responses API).

Key translation points:

| Chat Completions | Responses API |
|------------------|---------------|
| `messages: [{role, content}]` | `input: [{role, content: [{type: "input_text", text}]}]` |
| `stream: true` | `stream: true` (but SSE format differs) |
| `choices[].delta.content` | `response.output_text.delta` events |
| `finish_reason: "stop"` | `response.completed` event |

---

## Streaming: Critical Implementation Detail

Responses API uses **event-based SSE** (`event: response.output_text.delta` + `data: {...}`), not the simple `data: {...}` lines Chat Completions expects.

```python
async def stream_provider_response(resp: httpx.Response) -> AsyncGenerator[str, None]:
    chat_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())
    first_chunk = True
    
    current_event = None
    async for line in resp.aiter_lines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("event: "):
            current_event = line[7:].strip()
            continue
        if line.startswith("data: "):
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                yield final_chunk(chat_id, created)
                yield "data: [DONE]\n\n"
                break
            try:
                event_data = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            
            if current_event == "response.output_text.delta":
                delta = event_data.get("delta", "")
                if delta:
                    yield chunk(chat_id, created, delta, first_chunk)
                    first_chunk = False
            current_event = None
```

---

## Deploy & Register with Hermes

```bash
# 1. Run adapter (background)
cd /path/to/adapter
META_API_KEY="your-key" python3 adapter.py &
# Listens on http://localhost:8000/v1

# 2. Register in Hermes config
hermes config set providers.my-provider.api "http://localhost:8000/v1"
hermes config set providers.my-provider.default_model "model-name"
hermes config set providers.my-provider.name "My Provider"

# 3. Use
hermes chat -q "Hello" --provider my-provider --model model-name
```

---

## Pitfalls & Gotchas

| Issue | Fix |
|-------|-----|
| Hermes shows `EmptyStreamError` | Adapter must emit proper SSE: `data: {...}\n\n` with `finish_reason: "stop"` final chunk |
| `options: unknown parameter` | Hermes sends `options` field; adapter must ignore/strip unknown fields (use Pydantic `extra="allow"`) |
| Python version mismatch | Meta's API needs Python 3.9+; use isolated venv with `python3 -m venv venv` |
| `pydantic_core` import errors | Reinstall in clean venv: `pip install --force-reinstall pydantic pydantic_core` |
| Streaming timeouts | Set `timeout=None` on httpx client for streaming requests |

---

## References

- `references/responses-api-format.md` — OpenAI Responses API event specification
- `references/chat-completions-format.md` — OpenAI Chat Completions SSE format
- `templates/meta_responses_adapter.py` — Production adapter for Meta `muse-spark-1.1`