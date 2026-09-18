# Meta AI Adapter - Session Notes (2026-08-04)

## Context
User wanted to use Meta's new `muse-spark-1.1` model via their API (`https://api.meta.ai/v1/responses`). The API uses OpenAI's Responses API format, which Hermes doesn't support natively (Hermes expects Chat Completions format).

## Solution Implemented
Built a FastAPI adapter proxy at `/Users/alfredkamisese/meta-adapter/meta_adapter.py` that:
- Listens on `http://localhost:8000/v1`
- Translates Chat Completions → Responses API format
- Handles Meta's event-based SSE streaming (`response.output_text.delta` events)
- Emits proper OpenAI SSE format for Hermes

## Key Debugging Steps

### 1. Initial Provider Registration Failed
```bash
hermes config set providers.meta-ai.api "https://api.meta.ai/v1"
hermes chat -q "Hello" --provider meta-ai
# Error: HTTP 400: `options`: unknown parameter `options`
```
Root cause: Hermes sends `options` field + expects Chat Completions format; Meta expects Responses API format.

### 2. Raw Meta API Test (Confirmed Working)
```bash
curl -X POST "https://api.meta.ai/v1/responses" \
  -H "Authorization: Bearer $KEY" \
  -d '{"model": "muse-spark-1.1", "input": [...], "stream": false}'
# Returns proper response with reasoning tokens
```

### 3. Adapter v1 - Non-streaming Only
First version worked for non-streaming but failed streaming with `EmptyStreamError` because it returned full JSON instead of SSE.

### 4. Adapter v2 - Streaming with Wrong SSE Parsing
Attempted to parse simple `data:` lines but Meta uses `event:` / `data:` pairs.

### 5. Adapter v3 - Correct Event-Based SSE Parsing
```python
async for line in resp.aiter_lines():
    if line.startswith("event: "):
        current_event = line[7:].strip()
        continue
    if line.startswith("data: "):
        if current_event == "response.output_text.delta":
            delta = event_data.get("delta", "")
            yield openai_chunk(delta)
```
This worked - Hermes streamed properly.

## Hermes Configuration
```yaml
providers:
  meta-ai:
    api: http://localhost:8000/v1
    default_model: muse-spark-1.1
    name: Meta AI
```

## Verified Working
```bash
hermes chat -q "Count to 5" --provider meta-ai --model muse-spark-1.1
# Streams: 1 2 3 4 5

hermes chat -q "Write a haiku about Meta AI" --provider meta-ai
# Returns haiku

hermes chat -q "My name is Alfred. What's my name?" --provider meta-ai
# Returns: "Your name is Alfred."
```

## Runtime Requirements
- Python 3.9+ (Meta API compatibility)
- Clean venv with: `fastapi`, `uvicorn`, `httpx`, `pydantic`
- Environment: `META_API_KEY=LLM_2218105668968325_Bx5zI9KPv1zY6kBQWPNas_jekU4`
- Run: `PYTHONPATH=/path/to/site-packages python3 meta_adapter.py`

## Files Created
- `/Users/alfredkamisese/meta-adapter/meta_adapter.py` - Production adapter
- Template saved to skill: `templates/meta_responses_adapter.py`