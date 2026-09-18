# Meta AI Responses API → OpenAI Chat Completions Adapter

## Problem
Meta's new API (`api.meta.ai/v1/responses`) uses **OpenAI's Responses API format** (`input[]` array, event-based SSE streaming), while Hermes Agent expects standard **Chat Completions format** (`messages[]` array, `chat.completion.chunk` SSE). Direct integration fails with `400: unknown parameter options`.

## Solution: FastAPI Translation Adapter

### Adapter Location
```
/Users/alfredkamisese/meta-adapter/meta_adapter.py
```

### Running the Adapter
```bash
cd /Users/alfredkamisese/meta-adapter && \
META_API_KEY="LLM_2218105668968325_Bx5zI9KPv1zY6kBQWPNas_jekU4" \
PYTHONPATH="/Users/alfredkamisese/Library/Python/3.9/lib/python/site-packages" \
/Library/Developer/CommandLineTools/usr/bin/python3 meta_adapter.py
```
Runs on `http://localhost:8000/v1`

### Hermes Provider Config
```yaml
providers:
  meta-ai:
    api: http://localhost:8000/v1
    default_model: muse-spark-1.1
    models:
      - muse-spark-1.1
    name: Meta AI
```

## Translation Logic

### Request: Chat Completions → Responses API
```python
# Input: OpenAI format
{"messages": [{"role": "user", "content": "Hello"}]}

# Output: Meta format
{"model": "muse-spark-1.1", "input": [{"role": "user", "content": [{"type": "input_text", "text": "Hello"}]}], "stream": true}
```

### Streaming Response: Meta SSE → OpenAI SSE
Meta uses event-based SSE:
```
event: response.output_text.delta
data: {"delta": "Hello", "item_id": "msg_...", ...}
```

Adapter extracts `delta` from `response.output_text.delta` events and emits OpenAI format:
```
data: {"id": "chatcmpl-...", "object": "chat.completion.chunk", "choices": [{"delta": {"content": "Hello"}, "finish_reason": null}]}
```

## Key Implementation Details

### Python 3.9 Compatibility
- Use `Optional[str]` not `str | None`
- Use `Union[str, list]` not `str | list`
- Use `ConfigDict(extra="allow")` not class-based `Config`

### Streaming Event Parsing
```python
async for line in resp.aiter_lines():
    if line.startswith("event: "):
        current_event = line[7:].strip()
        continue
    if line.startswith("data: "):
        data_str = line[6:].strip()
        if current_event == "response.output_text.delta":
            delta_text = json.loads(data_str).get("delta", "")
            # emit OpenAI chunk
```

### Non-Streaming
Simple JSON request/response translation, no SSE parsing needed.

## Usage in Hermes
```bash
hermes chat -q "Your prompt" --provider meta-ai --model muse-spark-1.1
# or with default model:
hermes chat -q "Your prompt" --provider meta-ai
```

## Generalizable Pattern
This adapter pattern applies to **any provider with non-OpenAI API format**:
- Anthropic Messages API → Chat Completions
- Google Vertex AI → Chat Completions
- Azure OpenAI (non-standard) → Chat Completions
- Cohere, AI21, etc. → Chat Completions

Build a FastAPI shim that:
1. Receives OpenAI Chat Completions request
2. Translates to provider's native format
3. Forwards to provider
4. Translates response (streaming + non-streaming) back to OpenAI format
5. Configure Hermes to point to shim endpoint