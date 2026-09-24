# Vision Batch Processing Session — 2026-07-26

**Session ID:** `20260726_165000_...`
**Date:** 2026-07-26
**Profile:** default
**Agent:** Hermes with `vision_analyze` tool

## Session Overview

Processed `vision_batch_queue.json` (20 videos) using `vision_analyze` tool at 20 RPM rate limit, updating `VISION_PROGRESS.json` with complete technique analyses.

### Input Files
- **Queue:** `/Users/alfredkamisese/vision_batch_queue.json` — 20 video entries
- **Progress:** `/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json` — 1,148 total entries

### Output
All 20 queue items updated from `status: pending` to `status: complete` with full technique metadata.

---

## Videos Processed (20)

| # | Video ID | Collection | Technique | Resolve Page | Node Graph |
|---|----------|------------|-----------|--------------|------------|
| 1 | DKnOrGYxWWk | DR_Masking | Magic Mask Tool Stacking | Color | Serial |
| 2 | DQbi1MBDfr5 | DR_Noise_Reduction | Spatial Noise Reduction | Color | Serial |
| 3 | DLkGNsWNJyG | DR_Photo_Editing | Color Space Transform RAW Photo Grading | Color | Serial |
| 4 | C8kNJ8_t7gO | DaVinci | Timeline Grading | Color | Serial |
| 5 | C9PiTBNurGk | DaVinci | Auto Captions / Subtitle Generation | Edit | N/A |
| 6 | CyisshSxkIl | DaVinci | Face Refinement / AI Face Tracking | Color | Serial |
| 7 | CyN7bCjJLqQ | DaVinci | Bend the World / Mirror Effect | Fusion | Compound |
| 8 | CyYsDqFt53g | DaVinci | Micro-Jitter Stabilization (Optical Flow / Retime) | Edit/Color | Serial |
| 9 | CwTkWzWgrh2 | DaVinci | Relight Effect (DaVinci Resolve 18.5+) | Color | Serial |
| 10 | CyBM5Ybr97R | DaVinci | Advanced Qualifier with Layer Mixer | Color | Layer Mixer |
| 11 | CxwS9v1vjPX | DaVinci | Surface Tracker (Planar Tracking) | Color/Fusion | Serial |
| 12 | Dao4SDmtKVm | DaVinci_Tricks | CST Workflow for Multi-Cam Matching | Color | Serial |
| 13 | DaLtuVlRerK | DaVinci_Tricks | Render in Place (Workflow Optimization) | Edit | N/A |
| 14 | DXNQm4gkxrP | DaVinci_Tricks | Microsoft Word QR Code Generator (Non-Resolve) | N/A | N/A |
| 15 | DXIjXgCiD09 | DaVinci_Tricks | CineFocus Depth of Field Simulation (Resolve 21) | Color | Serial |
| 16 | DW4VX8PDFYh | DaVinci_Tricks | Efficient Clip Trimming (Edit Page) | Edit | N/A |
| 17 | DSxU9OyDEgk | DaVinci_Tricks | Fix Laggy Fusion Transitions (Render Cache / Proxy) | Edit/Color | N/A |
| 18 | DWpuEGPkfB7 | DaVinci_Tricks | Timeline Navigation - Copy/Paste Across Timeline | Edit | N/A |
| 19 | DQMRGKCDbJw | DaVinci_Tricks | Three Editing Speed Tools (Shift+Space, Swap, Ripple) | Edit | N/A |
| 20 | DQCaXhDDNpI | DaVinci_Tricks | Swap Two Clips Shortcut (Option+Drag) | Edit | N/A |

---

## Rate Limiting Protocol (Critical)

### Vision API: 20 RPM Hard Limit
- **Tool:** `vision_analyze` — returns 429 Too Many Requests at >20 RPM
- **Minimum interval:** 3 seconds between calls
- **Backoff on 429:** Exponential (30s → 60s → 120s → 240s → 480s)
- **Do NOT batch vision calls** — each counts individually against RPM
- Terminal/file operations can batch freely; only `vision_analyze` is rate-limited

### Implementation Pattern
```python
import time

MIN_INTERVAL = 3.0  # seconds (20 RPM)
last_call = 0.0

def rate_limited_vision_analyze(image_url: str, prompt: str) -> dict:
    global last_call
    elapsed = time.time() - last_call
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    # Actual call via Hermes agent tool interface
    result = vision_analyze(image_url=image_url, question=prompt)
    last_call = time.time()
    return result

def handle_429_backoff(attempt: int) -> float:
    """Exponential backoff: 30s → 60s → 120s → 240s → 480s"""
    backoff = 30 * (2 ** attempt)
    print(f"429 received, backing off {backoff}s (attempt {attempt+1})")
    time.sleep(backoff)
    return backoff
```

---

## Frame Sampling Strategy

### Key Frames Only (Max 5 per Video)
| Frame | Purpose | Heuristic |
|-------|---------|-----------|
| `frame_0001.jpg` | Opening/title — identifies technique, page, context | First frame |
| `frame_0020.jpg` | Early demo — tools/nodes being introduced | ~20% |
| `frame_0050.jpg` | Core technique — main workflow being shown | ~50% |
| `frame_0080.jpg` | Parameters/settings — specific values visible | ~80% |
| `frame_last.jpg` | Result/comparison — before/after or final look | Last frame |

### Skip Heuristics (Detected via Vision)
- Talking head frames — person on camera, no UI
- Title/transition frames — large text overlay, no Resolve UI
- Duplicate frames — visually identical to previous sample
- Outro/CTA frames — "follow me", "save this", social handles

---

## Vision Analysis Prompt Template

```text
Analyze this DaVinci Resolve technique reel frame.

Context:
- Video ID: {video_id}
- Collection: {collection}
- Caption: {caption}
- Known techniques: {techniques}
- Transcript: {transcript}

Identify the specific Resolve technique. Return ONLY valid JSON with:
{
  "technique_name": "...",
  "resolve_page": "Color|Fusion|Edit|Fairlight",
  "node_graph_type": "Serial|Parallel|Layer Mixer|Compound",
  "key_nodes": ["..."],
  "parameters": {...},
  "steps_to_reproduce": ["..."]
}
```

---

## VISION_PROGRESS.json Update Protocol

After each `vision_analyze` call:

```python
import json
from datetime import datetime

VISION_PROGRESS_PATH = "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json"

def update_progress(video_id: str, result: dict):
    with open(VISION_PROGRESS_PATH) as f:
        progress = json.load(f)

    for item in progress:
        if item['video_id'] == video_id:
            item['technique'] = result.get('technique_name', '')
            item['resolve_page'] = result.get('resolve_page', '')
            item['node_graph'] = result.get('node_graph_type', '')
            item['key_nodes'] = result.get('key_nodes', [])
            item['parameters'] = result.get('parameters', {})
            item['steps'] = result.get('steps_to_reproduce', [])
            item['status'] = 'complete'
            item['analyzed_at'] = datetime.utcnow().isoformat() + 'Z'
            break

    # Atomic write
    tmp_path = VISION_PROGRESS_PATH + '.tmp'
    with open(tmp_path, 'w') as f:
        json.dump(progress, f, indent=2)
    import os
    os.replace(tmp_path, VISION_PROGRESS_PATH)
```

---

## Batch Processing Script

Created: `scripts/process_vision_queue.py`

Features:
- Resumable: skips already-complete items
- Rate-limited: 3s minimum between vision calls
- Exponential backoff on 429 errors
- Atomic progress file updates
- Detailed logging

Usage:
```bash
python3 scripts/process_vision_queue.py \
    --queue vision_batch_queue.json \
    --progress VISION_PROGRESS.json \
    --batch-size 10
```

---

## Hardware Constraints (Mac Mini M4 16GB)

- **No heavy local vision models** (ollama llava exceeds RAM)
- Use assistant's built-in vision model via `vision_analyze` tool
- Samsung LED external SSD primary; PNY128GB emergency overflow

---

## No Premature Completion Claims

- Only report done when actually done
- Verify output files exist
- Batch size: 10 videos for safe tracking

---

## Integration with Learning Pipeline

This session's protocol feeds into:
- `instagram-davinci-learning-pipeline` — Main orchestrator
- `tag-aware-vision-extraction` — Phase 2 vision protocol
- `regenerate_exports_and_diagram` — Post-processing

---

## Phase 2 Progress Tracking

| Phase | Collection | Total | Complete | Remaining |
|-------|------------|-------|----------|-----------|
| 2a | Color Grading | 336 | 28 | 308 |
| 2b | DaVinci Tricks | 224 | 0 | 224 |
| 2c | Cinematic | 156 | 0 | 156 |
| 2d | Drone | 114 | 0 | 114 |
| 2e | Gimbal Moves | 474 | 0 | 474 |
| 2f | Ideas for Shooting | 796 | 0 | 796 |
| 2g | Other DaVinci | ~30 | 0 | ~30 |

---

## Pitfalls to Avoid

1. **Generic prompts** → Use category-specific prompts (5-10x more useful data)
2. **Wrong frame directory** → Always verify manifest mapping; fallback to download-order map
3. **Skipping reels** → Process all; flag missing frames but continue
4. **Batching vision calls** → 20 RPM is strict; 3s minimum interval
5. **Premature completion claims** → Verify output files exist
6. **Generic skill templates** → Use category-specific templates with relevant metadata
7. **Missing frame mapping** → downreels.com IDs ≠ Instagram short IDs

---

## Next Actions

1. Continue Phase 2a Color Grading vision analysis (28/336 complete)
2. Apply same pattern to remaining collections
3. Run `scripts/process_vision_queue.py` for automated batch processing
4. After each phase, run `regenerate_exports_and_diagram` to update exports