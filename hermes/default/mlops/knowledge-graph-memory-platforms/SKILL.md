---
name: knowledge-graph-memory-platforms
description: Patterns for installing, configuring, and integrating open-source knowledge graph memory platforms (cognee, graphiti, etc.) with local LLMs on Apple Silicon. Covers endpoint configuration, embedding model setup, and session vs. graph memory modes.
version: 1.0.0
author: Maddie
tags:
  - memory
  - knowledge-graph
  - cognee
  - ollama
  - local-llm
  - apple-silicon
  - persistent-memory
---

# Knowledge Graph Memory Platforms — Local Integration Patterns

## Overview

This skill captures the patterns for running knowledge graph memory platforms (primarily **cognee**) on Apple Silicon with local Ollama models. The key challenge is **endpoint configuration** — Ollama exposes different paths for chat vs. embeddings, and cognee's config system requires specific env vars.

---

## Core Pattern: Cognee + Ollama on Apple Silicon

### Prerequisites
- Ollama running with at least one chat model and one embedding model
- Python 3.10+ with `pip install cognee`
- ~4 GB free RAM for smallest viable setup (qwen3.5:4b + nomic-embed-text)

### Critical Endpoint Configuration

| Service | Ollama Endpoint | Cognee Env Var |
|---------|-----------------|----------------|
| Chat/Completion | `http://localhost:11434/v1/chat/completions` or `http://localhost:11434/api/generate` | `LLM_ENDPOINT=http://localhost:11434/v1` |
| **Embeddings** | `http://localhost:11434/api/embed` | **`EMBEDDING_ENDPOINT=http://localhost:11434/api/embed`** |

> **PITFALL**: Ollama's OpenAI-compatible `/v1/embeddings` returns a different response format than cognee's `OllamaEmbeddingEngine` expects. The engine calls `/api/embed` directly and expects `{"embedding": [...]}`. Using `/v1/embeddings` causes `ContentTypeError: 404` / `405` with "unexpected mimetype: text/plain".

> **PITFALL — Graph Memory Requires Structured Output**: Cognee's graph memory (`remember()` without `session_id`) runs the `cognify` pipeline which calls `extract_graph_and_summarize` → `LLMGateway.acreate_structured_output()` → `instructor` with `Mode.JSON` (OpenAI `response_format: {type: "json_object"}`). **Local Ollama models (qwen3.5:4b, gemma4:12b, etc.) do NOT support OpenAI's structured output format** — they return 404 on `/v1/chat/completions` with `response_format`. The `instructor` library retries until timeout.
>
> **Workaround**: Use **session memory only** (`remember(text, session_id="...")`) which uses keyword search over SQLite cache — no LLM calls, works perfectly. For graph memory, you need either:
> - A local LLM with structured output support (vLLM with `guided_json`, llama.cpp server with `--json-schema`, or Ollama model that supports tools/function calling)
> - Remote LLM for extraction only: set `LLM_PROVIDER=openai` + `LLM_API_KEY=...` for cognify step only
> - Accept session-only mode (fast, persistent across restarts, no entity/relationship extraction)

### Working `.env` Template

```bash
# LLM (chat)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b              # or gemma4:12b, qwen3.5-32k
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy

# Embeddings (CRITICAL: use /api/embed, not /v1/embeddings)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768          # nomic-embed-text = 768

# Skip connection test (Ollama may be slow to respond on first call)
COGNEE_SKIP_CONNECTION_TEST=true
```

### Installation

```bash
# Base install (SQLite + Kuzu + LanceDB — zero external services)
pip install cognee

# Optional: Postgres backend for production
pip install "cognee[postgres]"
```

### Memory Modes

| Mode | Call | Use Case | LLM Calls |
|------|------|----------|-----------|
| **Session** | `remember(text, session_id="...")` | Fast, short-term context | None (keyword search) |
| **Graph** | `remember(text)` | Persistent, queryable knowledge graph | Yes (cognify: entity extraction + summarization) |

```python
import cognee, asyncio

# Session memory (fast, no LLM)
await cognee.remember("User prefers concise responses.", session_id="chat-1")
results = await cognee.recall("What does user prefer?", session_id="chat-1")

# Graph memory (persistent, uses LLM for cognify)
await cognee.remember("Alfred works on DaVinci Resolve color grading.")
results = await cognee.recall("What does Alfred work on?")
```

---

## RAM Budget (16 GB Mac mini)

| Component | Est. RAM |
|-----------|----------|
| Ollama (qwen3.5:4b + nomic-embed-text) | ~4 GB |
| Cognee (Python + Kuzu + LanceDB) | ~1 GB |
| Hermes + other tools | ~2 GB |
| **Headroom** | **~9 GB** |

---\n\n## Hybrid Graph Memory: NVIDIA NIM for Extraction, Local for Storage\n\nFor local-only setups where Ollama models lack structured output support, use **NVIDIA NIM** (or OpenAI) *only for the `cognify()` extraction step* while keeping embeddings and storage local.\n\n### Architecture\n\n| Component | Provider | Model | Location |\n|-----------|----------|-------|----------|\n| **Embeddings** | Local Ollama | `nomic-embed-text:latest` | Mac mini |\n| **Graph Extraction** | NVIDIA NIM | `meta/llama-3.1-8b-instruct` | Cloud (your API key) |\n| **Graph Storage** | Local Kuzu + LanceDB | — | Mac mini |\n| **Session Memory** | Local SQLite | — | Mac mini |\n\n### Working `.env`\n\n```bash\n# LLM (chat)\nLLM_PROVIDER=ollama\nLLM_MODEL=qwen3.5:4b\nLLM_ENDPOINT=http://localhost:11434/v1\nLLM_API_KEY=dummy\nLLM_INSTRUCTOR_MODE=json_mode\n\n# NEW: Extraction via NVIDIA NIM (used ONLY by cognify)\nLLM_EXTRACTION_PROVIDER=nvidia_nim\nLLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct\nLLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1\nLLM_EXTRACTION_API_KEY=nvapi-...\n\n# Embeddings (local, MUST use /api/embed)\nEMBEDDING_PROVIDER=ollama\nEMBEDDING_MODEL=nomic-embed-text:latest\nEMBEDDING_ENDPOINT=http://localhost:11434/api/embed\nEMBEDDING_DIMENSIONS=768\n\nCOGNEE_SKIP_CONNECTION_TEST=true\n```\n\n### Cost\n\n| Operation | Model | Cost |\n|-----------|-------|------|\n| Graph extraction per doc | `meta/llama-3.1-8b-instruct` | ~$0.00015 / 1K tokens |\n| Typical note (1 page) | ~2K tokens | **~$0.0003** |\n| Full vault (557 notes) | ~500K tokens | **~$0.075** |\n\n### Test NIM Function Calling\n\n```bash\ncurl -s https://integrate.api.nvidia.com/v1/chat/completions \\\n  -H \"Authorization: Bearer nvapi-...\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\n    \"model\": \"meta/llama-3.1-8b-instruct\",\n    \"messages\": [{\"role\": \"system\", \"content\": \"Return only valid JSON via function call.\"}, {\"role\": \"user\", \"content\": \"Extract entities and relationships as JSON with fields: entities (array of strings), relationships (array of objects with subject, predicate, object). Text: Alfred prefers concise responses.\"}],\n    \"tools\": [{\"type\": \"function\", \"function\": {\"name\": \"extract\", \"description\": \"Extract entities and relationships\", \"parameters\": {\"type\": \"object\", \"properties\": {\"entities\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}, \"relationships\": {\"type\": \"array\", \"items\": {\"type\": \"object\", \"properties\": {\"subject\": {\"type\": \"string\"}, \"predicate\": {\"type\": \"string\"}, \"object\": {\"type\": \"string\"}}}}}}]}],\n    \"tool_choice\": {\"type\": \"function\", \"function\": {\"name\": \"extract\"}},\n    \"max_tokens\": 300,\n    \"temperature\": 0\n  }'\n```\n\nExpected: `tool_calls` with valid JSON entities/relationships.\n\n---\n\n## Hybrid Graph Memory: NVIDIA NIM for Extraction, Local for Storage

For local-only setups where Ollama models lack structured output support, use **NVIDIA NIM** *only for the `cognify()` extraction step* while keeping embeddings and storage local.

### Architecture

| Component | Provider | Model | Location |
|-----------|----------|-------|----------|
| **Embeddings** | Local Ollama | `nomic-embed-text:latest` | Mac mini |
| **Graph Extraction** | NVIDIA NIM | `meta/llama-3.1-8b-instruct` | Cloud (your API key) |
| **Graph Storage** | Local Kuzu + LanceDB | — | Mac mini |
| **Session Memory** | Local SQLite | — | Mac mini |

### Working `.env`

```bash
# LLM (chat)
LLM_PROVIDER=ollama
LLM_MODEL=qwen3.5:4b
LLM_ENDPOINT=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_INSTRUCTOR_MODE=json_mode

# NEW: Extraction via NVIDIA NIM (used ONLY by cognify)
LLM_EXTRACTION_PROVIDER=nvidia_nim
LLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct
LLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_EXTRACTION_API_KEY=nvapi-...

# Embeddings (local, MUST use /api/embed)
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

COGNEE_SKIP_CONNECTION_TEST=true
```

### Cost

| Operation | Model | Cost |
|-----------|-------|------|
| Graph extraction per doc | `meta/llama-3.1-8b-instruct` | ~$0.00015 / 1K tokens |
| Typical note (1 page) | ~2K tokens | **~$0.0003** |
| Full vault (557 notes) | ~500K tokens | **~$0.075** |

### Verified Function Calling on NIM

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

**Returns:** Valid `tool_calls` with structured entities/relationships JSON.

### Test Script

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

---

## References

- `references/cognee-ollama-endpoints.md` — Detailed endpoint mapping and response formats
- `references/cognee-env-template.md` — Full `.env` with all options documented

## Templates

- `templates/cognee-local.env` — Ready-to-use `.env` for local Ollama
- `templates/cognee-postgres.env` — Postgres backend config

## Scripts

- `scripts/verify-cognee-install.py` — End-to-end verification (session + graph)
- `scripts/check-ollama-endpoints.sh` — Validates Ollama chat + embed endpoints