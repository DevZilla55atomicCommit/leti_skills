# Vision Analysis Phase 2c — Cinematic/Shooting Collection (Session 2026-07-30)

## Overview
Phase 2c processes the **Cinematic/Shooting** Instagram Reels collection (1,146 videos) through vision analysis to extract DaVinci Resolve techniques.

## Pipeline Position
```
Download → Frame Extraction → **Vision Analysis (Phase 2c)** → Skill Generation → Vault Build
```

## Current Status (2026-07-30 Session)
| Metric | Count | Percentage |
|--------|-------|------------|
| **Complete** | 783 | 68.3% |
| **Pending** | 222 | 19.4% |
| **Errors** | 141 | 12.3% |
| **Total** | 1,146 | 100% |

- **Processed this session**: +61 videos (722 → 783)
- **Frame extraction**: ✅ Complete for all 1,146 videos (0 missing)
- **Vision provider**: NVIDIA Gemini (`vision_analyze` tool)

## Vision Analysis Workflow

### Per-Video Process
```python
# 1. Analyze first frame via NVIDIA Gemini
result = vision_analyze(
    image_url=f"/Volumes/Samsung LED/.../frames/{VIDEO_ID}/frame_0001.jpg",
    question="Analyze this cinematic shot... return ONLY valid JSON for DaVinci Resolve technique"
)

# 2. Parse JSON response
technique = json.loads(result["analysis"].split("```json")[1].split("```")[0])

# 3. Update VISION_PROGRESS.json
update_progress(VIDEO_ID, status="complete", result=technique)
```

### VISION_PROGRESS.json Structure
```json
[
  {
    "video_id": "C81h3wkvXTH",
    "status": "complete|pending|error",
    "result": {
      "technique_name": "Golden Hour Silhouette & Glow",
      "resolve_page": "Color",
      "node_graph_type": "serial",
      "key_nodes": ["Exposure", "Primary Balance", "Color Wheels", "Qualifiers", "Glow"],
      "parameters": {"temperature": "+2500", "saturation": "1.4", ...},
      "steps_to_reproduce": [...],
      "difficulty": "intermediate",
      "tags": ["sunset", "cinematic", "silhouette", "golden-hour"]
    },
    "updated_at": "2026-07-30T..."
  }
]
```

### Progress Tracking Script
```bash
python3 -c "
import json
from pathlib import Path
p = Path('VISION_PROGRESS.json')
data = json.load(p)
complete = sum(1 for v in data if v.get('status') == 'complete')
pending = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
print(f'Progress: {complete/1146*100:.1f}%')
"
```

## Technique Categories Observed (This Session)
| Category | Examples |
|----------|----------|
| **Golden Hour / Sunset** | Silhouette & Glow, Warm Contrast, Pastel Magenta |
| **Teal & Orange Variants** | Low-Key Cinematic, Urban Night, Neon Night |
| **Cool / Desaturated** | Urban Bokeh, Moody Fitness, Industrial |
| **Minimalist / High-Contrast** | Vertical Masking, Monochrome Faded |
| **Lifestyle / Vlog** | Warm High-Key, Natural Light Fashion |
| **Commercial / Automotive** | Clean POV, Moody Fitness, Teal & Red |

## Session Limit Constraint
- **Hermes session limit**: 150 tool calls per context window
- **Manual pace**: ~1 video/minute (vision_analyze + update progress)
- **Session throughput**: ~60 videos before limit hit
- **Remaining 222 videos**: Would require 4+ sessions manually

## Sub-Agent Parallelization Strategy (Recommended)

### Configuration (config.yaml)
```yaml
delegation:
  max_concurrent_children: 6
  child_timeout_seconds: 300
  provider: "ollama-cloud"  # or "ollama-launch" fallback
```

### Sub-Agent Task Template
```python
delegate_task(
    tasks=[
        {"goal": "Process videos [C4YBBbFIALf, C84z72hobi8, ...] through vision analysis", "context": "..."},
        {"goal": "Process videos [C4-wPZYoQRM, C5QWh1yr0gE, ...] through vision analysis", "context": "..."},
        # ... up to 6 concurrent
    ]
)
```

### Expected Throughput
- **6 sub-agents × 15 videos each** = 90 videos per batch
- **3 batches** = 222 videos in ~15-20 minutes
- **Avoids 150-call limit** (sub-agents have separate contexts)

## Next Phase: 2d (Remaining Collections)
After Phase 2c complete (~1,146 videos), Phase 2d processes remaining ~688 videos from other collections using same pipeline.

## Files Referenced
- `VISION_PROGRESS.json` — Progress tracking
- `/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/` — Extracted frames
- `~/.hermes/config.yaml` — Sub-agent configuration

## Sub-Agent Parallelization Failure (Added Post-Session)

**What Was Attempted:** Launched 6 parallel sub-agents via `delegate_task` to process the 222 remaining Cinematic/Shooting videos.

**What Happened:** All 6 sub-agents timed out at 600s with only 1 API call completed each.

**Root Cause:** **`vision_analyze` uses the assistant's built-in NVIDIA vision model (Gemini), NOT local Ollama models.**

Sub-agents spawned with `ollama-launch` provider have NO access to the parent session's `vision_analyze` tool. They were trying to use local Ollama for vision, which fails on M4 16GB (OOM, timeouts, crashes).

### Correct Architecture
```
Main Session (has vision_analyze tool) → Sequential manual calls
    │
    ├── Frame extraction: ffmpeg (local, batch, fast)
    ├── Vision analysis: vision_analyze (rate-limited 20 RPM, sequential)
    ├── Skill generation: Python scripts (batch, fast)
    └── Vault build: Python scripts (batch, fast)
```

### What Works (Sequential)
- Process 10-20 videos per main session manually
- Each video: 3-5 `vision_analyze` calls (key frames)
- ~1 min/video including JSON updates
- 20 RPM = 3 sec minimum between calls
- Session tool limit (150) ≈ 75 videos max per session

### Future Parallelization Options
1. **Multiple main sessions** (separate Hermes windows) — each gets own `vision_analyze` quota
2. **Cron jobs** with `vision_analyze` in background scripts
3. **Wait for native batch API** from NVIDIA if added

### Lesson
**Never delegate `vision_analyze` to sub-agents.** They cannot access the tool. Only the main session has the NVIDIA vision model access.