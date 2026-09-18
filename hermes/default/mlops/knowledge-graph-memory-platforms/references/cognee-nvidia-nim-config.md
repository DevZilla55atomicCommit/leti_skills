# Cognee + NVIDIA NIM Hybrid Configuration

## Complete Working `.env`

```bash
# LLM (chat only - local Ollama)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_INSTRUCTOR_MODE=json_mode

# EXTRACTION LLM (graph building only - NVIDIA NIM)
LLM_EXTRACTION_PROVIDER=nvidia_nim
LLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct
LLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_EXTRACTION_API_KEY=nvapi-...

# Embeddings (LOCAL - MUST use /api/embed)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

# Skip slow startup connection tests
COGNEE_SKIP_CONNECTION_TEST=true
```

## How It Works

| Pipeline Step | LLM Used | Where |
|---------------|----------|-------|
| `remember(text)` → add() | Local Ollama (qwen3.5:4b) | Local |
| `remember(text)` → cognify() → extract_graph_and_summarize | **NVIDIA NIM** (llama-3.1-8b) | Cloud |
| `remember(text)` → cognify() → add_data_points | Local Ollama | Local |
| Embeddings (LanceDB) | Local nomic-embed-text | Local |
| Session memory (`session_id=...`) | **Zero LLM calls** | Local SQLite |

## Verified Function Calling on NIM

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer nvapi-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role": "system", "content": "Return only valid JSON via function call."}, {"role": "user", "content": "Extract entities and relationships as JSON with fields: entities (array of strings), relationships (array of objects with subject, predicate, object). Text: Alfred prefers concise responses."}],
    "tools": [{"type": "function", "function": {"name": "extract", "description": "Extract entities and relationships", "parameters": {"type": "object", "properties": {"entities": {"type": "array", "items": {"type": "string"}}, "relationships": {"type": "array", "items": {"type": "object", "properties": {"subject": {"type": "string"}, "predicate": {"type": "string"}, "object": {"type": "string"}}}}}}]},
    "tool_choice": {"type": "function", "function": {"name": "extract"}},
    "max_tokens": 300,
    "temperature": 0
  }'
```

**Returns:** Valid `tool_calls` with structured entities/relationships JSON.

## Test Script

```python
# test_cognee_nim.py
import cognee, asyncio, os

os.environ['COGNEE_SKIP_CONNECTION_TEST'] = 'true'

async def test():
    # Graph memory (uses NIM for extraction)
    result = await cognee.remember('Alfred prefers concise, technical responses.')
    print('Graph remember:', result)
    
    results = await cognee.recall('What does Alfred prefer?')
    for r in results:
        print('Graph recall:', r)
    
    # Session memory (no LLM calls)
    result = await cognee.remember('Session test fact.', session_id='test-session')
    print('Session remember:', result)
    
    results = await cognee.recall('What was the test?', session_id='test-session')
    for r in results:
        print('Session recall:', r)

asyncio.run(test())
```

Run: `python test_cognee_nim.py`
```