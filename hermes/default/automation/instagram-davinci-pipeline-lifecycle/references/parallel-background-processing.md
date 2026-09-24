# Parallel Background Processing for Vision Analysis

## Overview
Launch multiple background terminal processes to process video chunks in parallel. Each process runs a Python script on disjoint video index ranges.

## Pattern
```python
# Split video indices into N chunks
indices = [1, 2, 3, ..., 135]
N = 4
chunks = [indices[i::N] for i in range(N)]  # round-robin split

# Launch N background processes
for i, chunk in enumerate(chunks):
    terminal(
        background=True,
        notify_on_complete=True,
        command=f"python process_chunk.py '{','.join(map(str, chunk))}' {i+1}"
    )

# Monitor
process(action="list")
process(action="log", session_id, limit=50)
```

## process_chunk.py Template
```python
import sys
import json
import time
from pathlib import Path

# Parse chunk indices
chunk_indices = [int(x) for x in sys.argv[1].split(",")]
chunk_id = sys.argv[2]

# Load progress
with open(VISION_PROGRESS_PATH, "r") as f:
    data = json.load(f)

# Process each video in chunk
for idx in chunk_indices:
    item = data[idx]
    vid = item["video_id"]
    frame_dir = find_frame_dir(vid)
    
    if not frame_dir:
        item["status"] = "error"
        item["error"] = "No frames"
        continue
    
    start = time.time()
    result = analyze_video_frames(str(frame_dir), 3)  # local Ollama
    elapsed = time.time() - start
    
    if "error" not in result.get("aggregate", {}):
        # Update item with results
        agg = result["aggregate"]
        item["status"] = "complete"
        item["technique"] = f"{agg.get('grading_style')} grading"
        item["skill"] = "davinci-reel-{vid[:8]}"
        item["analysis"] = f"analysis/{vid}/analysis.json"
        # ... update frontmatter
        print(f"[Chunk {chunk_id}] {vid}: OK ({elapsed:.1f}s)")
    else:
        item["error"] = result["aggregate"]["error"]
        print(f"[Chunk {chunk_id}] {vid}: FAILED")
    
    time.sleep(1)

# Write back (atomic - each chunk writes its own updates)
with open(VISION_PROGRESS_PATH, "w") as f:
    json.dump(data, f, indent=2)
print(f"[Chunk {chunk_id}] Complete!")
```

## Performance
| Approach | Time | Throughput |
|----------|------|------------|
| Sequential | 1.5 hrs | 1x |
| 4 Parallel | ~25 min | 3-4x |

## GPU Contention
- Per-video time increases from ~40s (sequential) to ~150-200s (parallel)
- Net throughput still 3-4x higher
- Acceptable tradeoff for batch processing

## Monitoring
```bash
# List all background processes
process(action="list")

# Watch live output
process(action="log", session_id, limit=50)

# Wait for completion
process(action="wait", session_id, timeout=3600)
```

## Critical Constraints
1. **Each chunk writes its own updates** - atomic write at end of chunk
2. **GPU contention** - per-video time increases but net throughput wins
3. **Memory** - each process loads its own model copy (~8.5 GB each)
4. **Sub-agents CANNOT do this** - only main session can launch background terminals