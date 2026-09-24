# NVIDIA NIM Verified Function Calling Pattern (Tested 2025-07-16)

## Verified Working Configuration

| Component | Value |
|-----------|-------|
| **Endpoint** | `https://integrate.api.nvidia.com/v1` |
| **Model** | `meta/llama-3.1-8b-instruct` |
| **Auth** | `Authorization: Bearer nvapi-...` |
| **Function Calling** | ✅ Verified working |
| **JSON Mode** | ✅ Via function calling |

## Verified Function Calling Request

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer nvapi-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [
      {"role": "system", "content": "Return only valid JSON via function call."},
      {"role": "user", "content": "Extract entities and relationships as JSON with fields: entities (array of strings), relationships (array of objects with subject, predicate, object). Text: Alfred prefers concise responses."}
    ],
    "tools": [{
      "type": "function",
      "function": {
        "name": "extract",
        "description": "Extract entities and relationships",
        "parameters": {
          "type": "object",
          "properties": {
            "entities": {"type": "array", "items": {"type": "string"}},
            "relationships": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "subject": {"type": "string"},
                  "predicate": {"type": "string"},
                  "object": {"type": "string"}
                }
              }
            }
          }
        }
      }
    }],
    "tool_choice": {"type": "function", "function": {"name": "extract"}},
    "max_tokens": 300,
    "temperature": 0
  }'
```

## Verified Response Format

```json
{
  "choices": [{
    "message": {
      "tool_calls": [{
        "function": {
          "arguments": "{\"entities\":[\"Alfred\",\"concise responses\"],\"relationships\":[{\"subject\":\"Alfred\",\"predicate\":\"prefers\",\"object\":\"concise responses\"}]}",
          "name": "extract"
        }
      }]
    }
  }]
}
```

## Cost

| Operation | Tokens | Cost |
|-----------|--------|------|
| Graph extraction per note | ~2K | ~$0.0003 |
| 557 notes (full vault) | ~500K | **~$0.075** |

## Integration with Cognee

```bash
# .env for hybrid Cognee (local embeddings + NIM extraction)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_INSTRUCTOR_MODE=json_mode

# Extraction via NIM (used ONLY by cognify pipeline)
LLM_EXTRACTION_PROVIDER=nvidia_nim
LLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct
LLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_EXTRACTION_API_KEY=nvapi-...

# Embeddings (LOCAL - MUST use /api/embed)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

COGNEE_SKIP_CONNECTION_TEST=true
```

## Test Script

```python
# test_nim_extraction.py
import cognee, asyncio, os
os.environ['COGNEE_SKIP_CONNECTION_TEST'] = 'true'

async def test():
    # Graph memory (uses NIM for extraction)
    result = await cognee.remember('Alfred prefers concise, technical responses.')
    print('Graph remember:', result)
    
    results = await cognee.recall('What does Alfred prefer?')
    for r in results:
        print('Graph recall:', r)

asyncio.run(test())
```

Run: `python test_nim_extraction.py`

## Verified Models on NIM

| Model | Function Calling | JSON Mode | Notes |
|-------|------------------|-----------|-------|
| `meta/llama-3.1-8b-instruct` | ✅ | ✅ | Recommended for extraction |
| `nvidia/nemotron-3-ultra` | ✅ | ✅ | Higher quality, slower |
| `nvidia/nemotron-3-nano` | ✅ | ✅ | Fast, good quality |

## Why This Matters for Local-First Setups

Local Ollama models (qwen3.5:4b, gemma4:12b, etc.) **do not support OpenAI's structured output format** (`response_format: {type: "json_object"}`) — they return 404 on `/v1/chat/completions` with that parameter. This breaks Cognee's `cognify()` pipeline which uses `instructor.Mode.JSON`.

**Solution**: Keep embeddings + storage local, route ONLY the `cognify()` extraction step to NIM (or OpenAI) which supports function calling.