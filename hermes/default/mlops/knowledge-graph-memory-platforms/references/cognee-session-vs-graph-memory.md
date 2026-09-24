# Cognee Session vs Graph Memory — Tested Behavior

## What We Tested (July 16, 2026)

| Mode | Config | Works? | Notes |
|------|--------|--------|-------|
| **Session Memory** | `remember(text, session_id="...")` | ✅ | Stores in SQLite cache, keyword search, **zero LLM calls** |
| **Graph Memory (local Ollama)** | `remember(text)` + `cognify()` | ❌ | `cognify` → `extract_graph_and_summarize` → `instructor.Mode.JSON` → Ollama `/v1/chat/completions` with `response_format` → **404 Not Found** |
| **Graph Memory (NVIDIA NIM)** | `remember(text)` + `cognify()` | ✅* | NIM Llama 3.1 8B supports function calling, returns valid `tool_calls` with structured JSON |

## Session Memory Details

```python
# Works immediately, no LLM calls
await cognee.remember("Alfred prefers concise responses.", session_id="test-session")
results = await cognee.recall("What does Alfred prefer?", session_id="test-session")
# Returns: keyword-matched QA entries from SQLite
```

- **Storage**: SQLite (`~/.cognee/databases/cognee_db`)
- **Search**: Keyword token overlap (no embeddings)
- **Latency**: ~10ms
- **LLM cost**: $0

## Graph Memory (Local Ollama) — Why It Fails

```
remember(text) 
  → add()          # ok
  → cognify()      # pipeline
    → extract_graph_and_summarize
      → LLMGateway.acreate_structured_output()
        → instructor.from_openai(client, mode=Mode.JSON)
          → client.chat.completions.create(
              response_format={"type": "json_object"}
            )
            → Ollama /v1/chat/completions
              → 404 Not Found
```

**Root cause**: Ollama's `/v1/chat/completions` does not implement OpenAI's `response_format: {type: "json_object"}`. The `instructor` library retries until timeout.

## Graph Memory (NVIDIA NIM) — Works

| Model | Function Calling | JSON Mode | Notes |
|-------|------------------|-----------|-------|
| `meta/llama-3.1-8b-instruct` | ✅ | ✅ | Returns valid `tool_calls` |
| `nvidia/nemotron-3-ultra` | ✅ | ✅ | Higher quality, slower |

**Config**:
```bash
LLM_EXTRACTION_PROVIDER=nvidia_nim
LLM_EXTRACTION_MODEL=meta/llama-3.1-8b-instruct
LLM_EXTRACTION_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_EXTRACTION_API_KEY=nvapi-...
```

**Cost**: ~$0.00015 per 1K tokens extraction. ~$0.0003 per typical note.

## RAM During Testing

| Phase | Free RAM | Notes |
|-------|----------|-------|
| Idle | ~10 GB | 16 GB total |
| Session memory test | ~10 GB | No model loading |
| Graph memory (local Ollama) | ~6 GB | qwen3.5:4b + nomic-embed-text loaded |
| Graph memory (NIM) | ~10 GB | No local LLM for extraction |

## Summary

| Need | Solution |
|------|----------|
| Fast, free, persistent context | **Session memory** (works now) |
| Entity/relationship queries across sessions | **Graph memory via NIM** (~8¢/vault) |
| Local-only, no API keys | Session memory only (graph extraction broken locally) |