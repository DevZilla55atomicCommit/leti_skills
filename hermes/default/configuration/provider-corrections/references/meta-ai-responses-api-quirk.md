# Meta AI Responses API Quirk & Working Solution

## The Problem

Meta's new `api.meta.ai` endpoint uses **OpenAI's Responses API format** (`/v1/responses`), which is **incompatible** with Hermes's `custom` provider (expects standard Chat Completions `/v1/chat/completions`).

**Error when using directly:**
```
HTTP 400: `options`: unknown parameter `options`
```

## Working Solution: FastAPI Adapter Proxy

### Architecture
```
Hermes (Chat Completions) → localhost:8000/v1 → Adapter → api.meta.ai/v1/responses
```

### Adapter Features
- Translates `messages[]` → `input[]` format
- Handles Meta's event-based SSE streaming (`response.output_text.delta` events)
- Converts to OpenAI SSE format (`chat.completion.chunk`)
- Supports both streaming and non-streaming requests
- Python 3.9 compatible (`Optional[]`, `Union[]`, `ConfigDict`)

### Files
- `scripts/meta_adapter.py` — Full adapter implementation
- `templates/requirements-meta-adapter.txt` — Dependencies

### Running
```bash
cd /Users/alfredkamisese/meta-adapter && \
META_API_KEY="LLM_2218105668968325_Bx5zI9KPv1zY6kBQWPNas_jekU4" \
PYTHONPATH="/Users/alfredkamisese/Library/Python/3.9/lib/python/site-packages" \
/Library/Developer/CommandLineTools/usr/bin/python3 meta_adapter.py
```

Runs on `http://localhost:8000/v1`

### Hermes Config
```yaml
providers:
  meta-ai:
    api: http://localhost:8000/v1
    default_model: muse-spark-1.1
    models:
      - muse-spark-1.1
    name: Meta AI
```

### Usage
```bash
# Uses default model
hermes chat -q "Your prompt" --provider meta-ai

# Explicit model
hermes chat -q "Your prompt" --provider meta-ai --model muse-spark-1.1

# Model picker
hermes model  # select meta-ai → muse-spark-1.1
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

---

## Session Fixes (2026-08-11)

Two critical bugs were found and fixed in the adapter during provider testing:

### 1. Wrong Content Type for Assistant Messages
**Error:** `HTTP 400: content type "input_text" is not valid on assistant messages`

**Fix:** Use role-specific content types in `convert_messages_to_input()`:
```python
content_type = "output_text" if msg.role == "assistant" else "input_text"
```

### 2. Default max_tokens Too Low
**Problem:** Muse Spark 1.1 uses heavy internal reasoning (~300-600 tokens) before producing visible output. Default `max_tokens=16-50` left no room for actual response → empty `content` field.

**Fix:** Default to 2000 tokens if not explicitly set:
```python
effective_max_tokens = req.max_tokens if req.max_tokens is not None else 2000
meta_payload["max_output_tokens"] = effective_max_tokens
```

### Verified Working
- ✅ 5/5 consecutive requests with conversation history (name recall)
- ✅ 3/3 consecutive simple requests ("Say OK if working")
- ✅ All return populated `content` field with correct responses
- ✅ LaunchAgent auto-restart functional

The fixed adapter is in `scripts/meta-adapter.py` and deployed at `~/meta-adapter/meta_adapter.py`.