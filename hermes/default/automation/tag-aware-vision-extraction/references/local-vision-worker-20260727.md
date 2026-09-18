# Local Ollama Vision Worker Protocol (2026-07-27 Session)

## Context
Cloud `vision_analyze` tool has 20 RPM rate limit (3.2s/call), hitting 429 errors on 1,165 frames. Local `llava:7b` via Ollama provides **no rate limits** and runs on M4 Mac Mini (16GB RAM).

## Architecture

```
VISION_PROGRESS.json (shared state, file-locked)
         │
         ▼
┌─────────────────────────────────────────────┐
│  Local Vision Worker (Python script)        │
│  - Polls for "pending" entries              │
│  - File-locked read/write (fcntl)           │
│  - Processes 5 frames/batch with 2 workers  │
│  - Calls `ollama run llava:7b` per frame    │
│  - Atomic JSON writes via .tmp rename       │
└─────────────────────────────────────────────┘
         │
         ▼
Progress file updated with "complete" + technique JSON
```

## VISION_PROGRESS.json Schema
```json
{
  "video_id": "C-FvSX-piqT",
  "collection": "DaVinci_Core",
  "frame_to_analyze": "/Volumes/Samsung LED/.../frames/C-FvSX-piqT/frame_0001.jpg",
  "status": "pending|complete|error",
  "result": {
    "technique_name": "Dynamic Speed Ramping with Curve Smoothing",
    "resolve_page": "Edit",
    "node_graph_type": "serial",
    "key_nodes": ["Retime Curve", "Transform"],
    "parameters": {"curve_type": "bezier", "easing": "ease_in_out"},
    "steps_to_reproduce": [
      "Add Retime Curve to clip",
      "Set keyframes at speed change points",
      "Adjust Bezier handles for smooth easing"
    ],
    "difficulty": "intermediate",
    "tags": ["speed-ramp", "retime", "curve", "edit-page"]
  },
  "error": null,
  "updated_at": "2026-07-27T16:45:00Z"
}
```

## Worker Script: `scripts/local_vision_worker.py`
Key features:
- **File locking** with `fcntl` prevents corruption from concurrent access
- **Atomic writes** via seek/truncate with lock held
- **Resume capability** — reads current state, only processes `status: pending`
- **Parallel workers** — `ThreadPoolExecutor(max_workers=2)` calls Ollama subprocess
- **Timeout** — 180s per frame (llava:7b typically 15-20s)
- **Error handling** — marks `status: error` with message, doesn't block batch

## Performance (2026-07-27)
| Metric | Value |
|--------|-------|
| Model | llava:7b (4.7GB) |
| Frame time | ~15-20s |
| Batch (5 frames, 2 workers) | ~45-60s |
| Throughput | ~80-100 frames/hour |
| 1165 frames | ~12-15 hours |
| RAM usage | ~6GB (model + 2 workers) |
| Rate limits | **None** |

## Results (Session End)
- **VISION_PROGRESS.json**: 1165 entries created from frame extraction
- **Worker started**: Background process processing ~5 frames/batch
- **Progress**: 181/1165 complete (~15%)
- **Quality**: Structured JSON extraction working; llava:7b returns proper technique names, node graphs, parameters, steps

## Critical Fixes Applied
1. **JSON extraction from markdown** — llava:7b wraps JSON in ```json ``` blocks; must parse before `json.loads`
2. **Frame mapping** — VISION_PROGRESS.json uses `frame_to_analyze` field (not `frames_analyzed[0]`)
3. **File locking** — `fcntl` prevents corruption from concurrent reads/writes
4. **Atomic writes** — Seek/truncate in-place with lock held
5. **Resume capability** — Worker reads current state, only processes `status: pending`
6. **Error handling** — Failed frames marked `error` with message; don't block batch

## Integration with Pipeline
- **Upstream**: `scripts/process_all_videos.py` creates VISION_PROGRESS.json with `frame_to_analyze` paths
- **Downstream**: `scripts/generate_skills_from_vision.py` reads complete entries, generates Hermes SKILL.md files
- **Vault**: `scripts/build_vault_from_vision.py` creates Obsidian notes with embedded GIFs and technique tables

## Launch Commands
```bash
# Start worker (background, persists after session)
nohup python scripts/local_vision_worker.py > vision_worker.log 2>&1 &

# Monitor progress
watch -n 10 'python -c "
import json
with open(\"VISION_PROGRESS.json\") as f: d=json.load(f)
c=sum(1 for x in d if x.get(\"status\")==\"complete\")
p=sum(1 for x in d if x.get(\"status\")==\"pending\")
e=sum(1 for x in d if x.get(\"status\")==\"error\")
print(f\"Complete: {c}, Pending: {p}, Errors: {e}\")
"'

# Check worker log
tail -f vision_worker.log
```

## Next Session
Worker will continue overnight. Resume with:
```bash
python scripts/local_vision_worker.py
```
(Automatically resumes from `pending` entries)