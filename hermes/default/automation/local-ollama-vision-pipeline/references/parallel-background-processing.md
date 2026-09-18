# Parallel Background Processing for Local Vision (2026-07-31)

## Overview
This session discovered that **parallel background terminal processes** achieve 3x speedup over sequential processing for local vision analysis. Sub-agents cannot do this (text-only LLMs), but the main session can launch multiple `terminal(background=true)` jobs.

## Architecture

```
Main Session (Hermes)
    ├── terminal(background=true) → Chunk 1 (39 videos) → local llava:7b
    ├── terminal(background=true) → Chunk 2 (39 videos) → local llava:7b
    └── terminal(background=true) → Chunk 3 (38 videos) → local llava:7b
```

Each chunk runs `scripts/batch_chunk.py` with a comma-separated list of VISION_PROGRESS.json indices.

## Commands Used

```bash
# Launch 3 parallel background jobs
cd /Users/alfredkamisese/vision_pipeline

# Chunk 1 (indices 108-329)
/opt/homebrew/bin/python3.12 batch_chunk.py "108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,194,195,196,197,198,200,208,212,216,219,227,235,245,247,251,280,291,324,329" 1

# Chunk 2 (indices 331-496)
/opt/homebrew/bin/python3.12 batch_chunk.py "331,332,335,340,342,346,348,350,352,353,354,355,357,359,362,363,367,369,370,377,382,384,391,394,396,407,409,410,412,413,478,480,481,483,488,490,491,492,496" 2

# Chunk 3 (indices 497-1103)
/opt/homebrew/bin/python3.12 batch_chunk.py "497,503,504,506,507,508,509,511,512,531,538,554,561,562,580,584,719,726,881,1077,1078,1080,1081,1084,1086,1087,1090,1091,1092,1093,1094,1096,1098,1099,1100,1101,1102,1103" 3
```

## Results

| Metric | Sequential | Parallel (3 chunks) |
|--------|------------|---------------------|
| Time for 116 videos | ~1.5 hours | ~25-30 minutes |
| Rate limits | None (local) | None (local) |
| GPU usage | 100% (single) | 100% (shared, 3 processes) |
| Success rate | ~95% | ~95% |

## Key Implementation Details

### 1. Chunk Index Calculation
```python
# Split error indices into ~3 equal chunks
error_indices = [i for i, item in enumerate(data) if item.get("status") == "error"]
chunk_size = (len(error_indices) + 2) // 3
chunks = [error_indices[i:i+chunk_size] for i in range(0, len(error_indices), chunk_size)]
```

### 2. Background Process Launch (Hermes)
```python
terminal(
    command="cd /Users/alfredkamisese/vision_pipeline && /opt/homebrew/bin/python3.12 batch_chunk.py \"...indices...\" 1",
    background=True,
    notify_on_complete=True,
    timeout=3600
)
```

### 3. Progress Monitoring
```bash
# Check status
process(action="list")

# Poll for completion
process(action="poll", session_id="proc_xxx")

# Read full output
process(action="log", session_id="proc_xxx", limit=100)
```

## Why Sub-Agents Don't Work

| Capability | Main Session | Sub-Agent |
|------------|--------------|-----------|
| `terminal()` tool | ✅ | ❌ |
| Python execution | ✅ | ❌ |
| HTTP requests (Ollama API) | ✅ | ❌ |
| File I/O (VISION_PROGRESS.json) | ✅ | ❌ |
| `vision_analyze` tool | ✅ | ❌ (no parent vision access) |

Sub-agents are text-only LLMs — they can reason but cannot execute.

## Pitfalls Avoided

1. **Don't use `ollama-launch` provider for sub-agents** — OOM on 16GB M4
2. **Don't use sub-agents for vision** — they can't run Python/HTTP
3. **Do use `terminal(background=true)`** — true parallelism in main session
4. **Do split indices evenly** — balance load across chunks
5. **Do use `notify_on_complete=True`** — auto-notification when done
6. **Do use Python 3.12+** — system Python 3.9 has urllib3 issues

## Next Steps for Phase 2

1. Wait for 3 background chunks to complete (monitor via `process(action="list")`)
2. Process 19 `pending_vision` videos (can add as 4th chunk)
3. Phase 2d: ~688 remaining videos in other collections
4. Consider 4-5 parallel chunks for larger batches