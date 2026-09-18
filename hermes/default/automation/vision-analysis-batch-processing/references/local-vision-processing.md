# Local Vision Processing with llava:7b (2026-07-31)

## Overview
Replaced NVIDIA API vision analysis with local Ollama `llava:7b` model for Phase 2c/2d completion. Removes 20 RPM rate limit, enables unlimited parallel processing.

## Setup
```bash
ollama pull llava:7b  # 8.5 GB RAM, 100% GPU, 32K context
```

## Python Pipeline
Location: `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`

- Calls Ollama API at `http://localhost:11434/api/generate`
- Processes 3 frames per video (frame_0001, 0002, 0003)
- Outputs identical JSON schema to NVIDIA vision
- Schema: grading_style, camera_movement, lighting, effects, color_temperature, contrast_level, saturation, notes

## Performance
| Mode | Time/Video | Notes |
|------|------------|-------|
| Sequential (1 process) | ~35-50 sec | No GPU contention |
| 4 Parallel | ~150-200 sec | Severe GPU contention (4x 100%) |
| NVIDIA API (cloud) | ~60 sec | 20 RPM rate limit |

**Recommendation**: Run 1-2 background processes max, or sequential.

## Parallelization: Background Terminal Processes (NOT sub-agents)

**Critical Finding**: Sub-agents CANNOT run the vision pipeline - they lack terminal, Python, HTTP, and file system access. Even with llava:7b model, sub-agents are text-only LLMs.

```bash
# Launch parallel background jobs via terminal(background=true)
terminal(background=true, command="python3 batch_chunk.py 'indices...' 1", notify_on_complete=true)
terminal(background=true, command="python3 batch_chunk.py 'indices...' 2", notify_on_complete=true)
```

Each background process:
- Runs independently in its own Python process
- Reads/writes VISION_PROGRESS.json at chunk boundaries
- Processes assigned video indices
- Completes in ~25-30 min per chunk (39 videos)

## Batch Chunk Script
Location: `/Users/alfredkamisese/vision_pipeline/batch_chunk.py`

```python
# Usage
python3 batch_chunk.py "108,109,110,..." "1"
# Arguments: comma-separated indices, chunk_id
```

## Storage Crisis (2026-07-31)

**Samsung LED at 96% full (5.4 GB free)**

| Path | Size | Action |
|------|------|--------|
| `CONTENT_PROCESSING/gifs/` | **45 GB** | DELETE - regenerate from frames |
| `CONTENT_PROCESSING/frames/` | 7.9 GB | Keep only pending/error |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | Can re-extract |
| `CONTENT_PROCESSING/vault/` | 346 MB | KEEP - final output |

**Action taken**: Killed 4 background jobs, need to delete `gifs/` (45 GB savings).

## Progress Tracking
VISION_PROGRESS.json updated with `vision_model: "llava:7b"` field for local-processed videos.

| Status | Count |
|--------|-------|
| Complete | 1,030 |
| Error | 116 |
| Pending | 19 |
| Local vision | 45 |

## Key Lessons
1. **Local vision works** - llava:7b produces valid JSON, no rate limits
2. **Sub-agents cannot execute** - only background terminal processes work
3. **GPU contention is real** - 4 parallel = 4x slower per video
4. **Storage management critical** - gifs/ accumulates 45 GB, must clean periodically
5. **Background jobs write at chunk end** - VISION_PROGRESS.json not updated incrementally