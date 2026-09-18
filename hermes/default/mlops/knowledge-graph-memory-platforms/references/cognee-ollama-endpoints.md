# Cognee + Ollama Endpoint Mapping

## The Core Problem

Ollama exposes **two different API surfaces**:

| Surface | Base URL | Embeddings Path | Response Format |
|---------|----------|-----------------|-----------------|
| **Native Ollama** | `http://localhost:11434` | `/api/embed` | `{"embedding": [...]}` |
| **OpenAI-Compatible** | `http://localhost:11434/v1` | `/embeddings` | `{"data": [{"embedding": [...]}]}` |

## What Cognee's `OllamaEmbeddingEngine` Does

```python
# In OllamaEmbeddingEngine.__init__
endpoint: str = "http://localhost:11434/api/embed"  # HARDCODED default

# In _get_embedding():
payload = {"model": self.model, "input": prompt, "dimensions": self.dimensions}
async with session.post(self.endpoint, json=payload, headers=headers) as response:
    data = await response.json()
    # Expects one of:
    # - {"embeddings": [[...]]}
    # - {"embedding": [...]}
    # - {"data": [{"embedding": [...]}]}
```

## Why `/v1/embeddings` Fails

| Attempt | URL | Result |
|---------|-----|--------|
| ❌ OpenAI-compatible | `http://localhost:11434/v1/embeddings` | Returns `{"data": [{"embedding": [...]}]}` — cognee doesn't parse this format |
| ❌ OpenAI-compatible (with /api) | `http://localhost:11434/api/embeddings` | 404 |
| ✅ **Native Ollama** | `http://localhost:11434/api/embed` | Returns `{"embedding": [...]}` — **works** |

## Correct Configuration

```bash
# Embeddings MUST use native Ollama endpoint
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed

# Chat CAN use OpenAI-compatible endpoint
LLM_ENDPOINT=http://localhost:11434/v1
```

## Verified Working Models

| Model | Dimensions | Endpoint |
|-------|------------|----------|
| `nomic-embed-text:latest` | 768 | `/api/embed` ✅ |
| `mxbai-embed-large:latest` | 1024 | `/api/embed` ✅ |
| `bge-m3:latest` | 1024 | `/api/embed` ✅ |

## Debugging

```bash
# Test native embeddings endpoint
curl -s http://localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text:latest","input":"test"}' \
  -H "Content-Type: application/json"

# Expected: {"embedding":[0.0287,0.0116,...]}
```

---

## Session Memory vs Graph Memory

| Mode | API Call | LLM Calls | Persistence | Use Case |
|------|----------|-----------|-------------|----------|
| **Session** | `remember(text, session_id="x")` | **Zero** | SQLite (survives restart) | Fast, reliable, no extraction |
| **Graph** | `remember(text)` (no session_id) | Many (cognify pipeline) | Kuzu + LanceDB | Entity/relationship extraction, cross-document reasoning |

**Recommendation for local-only setups**: Use session memory. It works perfectly, requires zero LLM calls, and survives restarts. Graph memory requires structured output support which most local Ollama models lack.

---

## Critical: Graph Memory Requires Structured Output

Cognee's graph memory (`remember()` without `session_id`) runs the `cognify` pipeline which calls:
1. `extract_graph_and_summarize` → `LLMGateway.acreate_structured_output()`
2. `instructor` with `Mode.JSON` (OpenAI `response_format: {type: "json_object"}`)
3. **Local Ollama models (qwen3.5:4b, gemma4:12b, etc.) do NOT support OpenAI's structured output format** — they return 404 on `/v1/chat/completions` with `response_format`.

The `instructor` library retries until timeout.

**Workaround**: Use **session memory only** (`remember(text, session_id="...")`) which uses keyword search over SQLite cache — no LLM calls, works perfectly. For graph memory, you need either:
- A local LLM with structured output support (vLLM with `guided_json`, llama.cpp server with `--json-schema`, or Ollama model that supports tools/function calling)
- Remote LLM for extraction only: set `LLM_PROVIDER=openai` + `LLM_API_KEY=...` for cognify step only
- Accept session-only mode (fast, persistent across restarts, no entity/relationship extraction)

---

## Instructor Mode Configuration

| Env Var | Value | Notes |
|---------|-------|-------|
| `LLM_INSTRUCTOR_MODE` | `json_mode` | Must be `json_mode` (instructor.Mode.JSON), NOT `json` |

## Complete .env Template

```bash
# LLM (chat/summarization/extraction)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_INSTRUCTOR_MODE=json_mode

# Embeddings (CRITICAL: use /api/embed, not /v1/embeddings)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

# Skip connection tests at startup
COGNEE_SKIP_CONNECTION_TEST=true
```