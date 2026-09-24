---
name: cognee-nvidia-graph-memory
description: Configure Cognee to use NVIDIA NIM for graph memory extraction while keeping embeddings and storage local
tags:
  - cognee
  - nvidia
  - nim
  - graph-memory
  - hybrid-llm
  - session-memory
category: cognee
---

# Cognee + NVIDIA NIM Graph Memory Pattern

## Overview

This skill documents the working configuration for using Cognee's graph memory with NVIDIA NIM models, keeping embeddings and storage local while offloading graph extraction to NVIDIA's hosted models.

## Key Discovery

**Local embeddings + NVIDIA NIM graph extraction = Working hybrid architecture**

| Component | Provider | Model | Location |
|-----------|----------|-------|----------|
| Embeddings | Ollama (local) | `nomic-embed-text:latest` | Your Mac |
| Graph Extraction | NVIDIA NIM (cloud) | `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA API |
| Graph Storage | Kuzu (local) | — | Your Mac |
| Session Memory | SQLite (local) | — | Your Mac |

## Working Configuration

```bash
# .env
LLM_PROVIDER=custom
LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b
LLM_ENDPOINT=https://integrate.api.nvidia.com/v1
LLM_API_KEY=${NVIDIA_API_KEY}  # Read from Hermes .env (already set)
LLM_INSTRUCTOR_MODE=    # Empty - default json_mode works

EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_ENDPOINT=http://localhost:11434/api/embed
EMBEDDING_DIMENSIONS=768

COGNEE_SKIP_CONNECTION_TEST=true
```

## Prerequisites

1. **Ollama running locally** with `nomic-embed-text:latest` pulled
   ```bash
   ollama pull nomic-embed-text:latest
   ```

2. **NVIDIA API key** from https://integrate.api.nvidia.com

3. **Python dependencies**
   ```bash
   pip install cognee orjson
   ```

4. **Cognee v1.3.0+** installed

## Working Model

| Model | Provider String | Function Calling | Notes |
|-------|-----------------|------------------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b` | `nvidia/nemotron-3-ultra-550b-a55b` | ✅ Yes | Best for extraction |

**Failed models** (no function calling support):
- `meta/llama-3.1-8b-instruct`
- `meta/llama-3.1-70b-instruct`
- `meta/llama-3.2-3b-instruct`
- `nvidia/llama-3.1-nemotron-70b-instruct`

## Usage

```python
import cognee
import asyncio

# Graph memory (uses NVIDIA for extraction)
await cognee.remember("Alfred prefers concise, technical responses.")
results = await cognee.recall("What does Alfred prefer?")

# Session memory (local only, fast)
await cognee.remember("DaVinci node: CST → Kodak 2383 → Halation", session_id="davinci-notes")
results = await cognee.recall("What was the Davinci node tree?", session_id="davinci-notes")
```

## Cost Estimate

| Operation | Model | Cost |
|-----------|-------|------|
| Embeddings | Local `nomic-embed-text` | $0 |
| Graph extraction (per doc) | Nemotron 3 Ultra | ~$0.00015 |
| Session memory | Local SQLite | $0 |
| **557 notes vault** | One-time graph build | **~$0.08** |

## Troubleshooting

| Error | Fix |
|-------|-----|
| `'nvidia' is not a valid LLMProvider` | Use `LLM_PROVIDER=custom` |
| `LLM Provider NOT provided` | Set `LLM_PROVIDER=custom` not `nvidia` |
| `meta does not support parameters: ['tools']` | Model doesn't support function calling |
| `No module named 'orjson'` | `pip install orjson` |
| `could not load tokenizer` | `pip install transformers` or ignore (falls back to TikToken) |

## Session Memory (Always Works)

If graph memory is unavailable, session memory works 100% locally:

```python
# Fast, no LLM calls, persists across restarts
await cognee.remember("DaVinci node tree: CST → Kodak 2383 → Halation", session_id="davinci")
results = await cognee.recall("What was the node tree?", session_id="davinci")
```

### Hermes MCP Server Reload Procedure

To reload the MCP server config after changes:

1. Restart the Hermes desktop app (Cmd+R or quit/relaunch).
2. The MCP server will automatically reconnect.
3. Verify with `/graphify` or `mcp_cognee_memory_graph_remember` tools.

See `references/mcp-reload-guide.md` for detailed steps.
```

### Hermes MCP Server Reload Procedure

To reload the MCP server config after changes:

1. Restart the Hermes desktop app (Cmd+R or quit/relaunch).
2. The MCP server will automatically reconnect.
3. Verify with `/graphify` or `mcp_cognee_memory_graph_remember` tools.
```

## Files Created

| Path | Purpose |
|------|---------|
| `~/.cognee/logs/` | Pipeline execution logs |
| `~/.cognee/system/databases/` | SQLite (session) + Kuzu (graph) + LanceDB (vectors) |

## References

- Cognee docs: https://docs.cognee.ai/
- NVIDIA NIM models: https://integrate.api.nvidia.com
- Cognee GitHub: https://github.com/topoteretes/cognee
- Config reference: `references/cognee-config-reference.md` (auto-injected NVIDIA_API_KEY from Hermes)
---

*Last tested: Cognee 1.3.0, Nemotron 3 Ultra (nvidia/nemotron-3-ultra-550b-a55b)*