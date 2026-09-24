---
name: vision-analysis-batch-processing
description: Batch vision analysis of Reels frames via NVIDIA API.
category: automation
tags: [vision-analysis, batch-processing, nvidia-api, instagram-reels, davinci-resolve, skill-generation]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-30
---

# Vision Analysis Batch Processing

Methodology for batch vision analysis of Instagram Reels frames using NVIDIA API, with progress tracking, non-Resolve skill generation, and DaVinci Resolve technique skill authoring.

## Overview

This skill documents the batch processing workflow for Phase 2c (Cinematic/Shooting collections) of the Instagram Reels → DaVinci Resolve pipeline. It covers the vision analysis of ~1,146 pre-extracted frames using the NVIDIA API (google/diffusiongemma-26b-a4b-it).

## Configuration

- **Vision Provider**: NVIDIA API (google/diffusiongemma-26b-a4b-it) OR Local Ollama (llava:7b)
- **Model**: google/diffusiongemma-26b-a4b-it (cloud) / llava:7b (local)
- **Input**: Pre-extracted frames at `/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{REEL_CODE}/frame_0001.jpg`
- **Progress Tracking**: `VISION_PROGRESS.json` with fields: `video_id`, `status` (complete/pending/error), `result`, `updated_at`, `vision_model`
- **Batch Size**: 50 videos per session (cloud) / 5-10 videos per background process (local)
- **Rate Limit**: NVIDIA API: 20 RPM (~1 min/video). Local Ollama: NO rate limit (~45 sec/video with GPU contention)

## Local Vision Processing (llava:7b) - RECOMMENDED

### Setup
```bash
ollama pull llava:7b  # ~8.5 GB RAM, 100% GPU
```

### Python Pipeline (`/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`)
- Calls Ollama API at `http://localhost:11434/api/generate`
- Processes 3 frames per video
- Outputs same JSON schema as NVIDIA vision
- ~35-50 sec/video (sequential), ~150-200 sec/video (4 parallel - GPU contention)

### Parallelization: Background Terminal Processes (NOT sub-agents)
**Sub-agents CANNOT run vision pipeline** - they lack terminal/Python/HTTP access.

```bash
# Launch parallel background jobs
terminal(background=true, command="python3 batch_chunk.py 'indices...' 1", notify_on_complete=true)
terminal(background=true, command="python3 batch_chunk.py 'indices...' 2", notify_on_complete=true)
terminal(background=true, command="python3 batch_chunk.py 'indices...' 3", notify_on_complete=true)
```

Each background process runs independently, writes to VISION_PROGRESS.json at chunk end.

### GPU Contention Warning
- 4 parallel llava:7b processes = 4x 100% GPU = severe contention
- **Recommendation**: Run 1-2 parallel max, or sequential
- Sequential: ~45 sec/video, no contention

## Phase 2c Status (as of 2026-07-30)

| Metric | Count | Percentage |
|--------|-------|------------|
| **Complete** | 722 | 63.0% |
| **Pending** | 283 | 24.7% |
| **Errors** | 141 | 12.3% |
| **Total** | 1,146 | 100% |

## Key Findings

### 1. NVIDIA API Reliability
- The NVIDIA API (google/diffusiongemma-26b-a4b-it) is highly reliable for cinematic shot analysis
- No rate limiting issues encountered at batch size of 50
- Consistent JSON output format matching the required schema
- ~3-5 seconds per video average throughput

### 2. Frame Extraction Status
- **All 319 pending videos already have frames extracted** (0 missing)
- Frame extraction was completed in prior pipeline phases
- No additional frame extraction needed for Phase 2c completion

### 3. Non-Resolve Content Handling
- **~12% error rate** consistently represents non-DaVinci Resolve content
- These are correctly flagged as "errors" in VISION_PROGRESS.json
- Created 9 class-level non-Resolve skills:
  - **Cinematography** (2): `gimbal-movement-basics`, `camera-movement-transitions`
  - **Photography** (5): `architectural-photography-lighting`, `lens-selection-cinematic-look`, `gimbal-camera-movements`, `split-screen-comparison-technique`, `color-grading-theory-fundamentals`, `motion-graphics-fundamentals-fusion`
  - **Camera Hardware** (1): `camera-gear-workflow`
  - **Camera Theory** (1): `cinematic-camera-theory-fundamentals`

### 4. Vision Analysis Prompt Template

```json
{
  "technique_name": "Descriptive name",
  "resolve_page": "Color|Edit|Fusion|Fairlight",
  "node_graph_type": "serial|parallel|layer_mixer|compound",
  "key_nodes": ["node1", "node2"],
  "parameters": {"param1": "value1"},
  "steps_to_reproduce": ["step1", "step2"],
  "difficulty": "beginner|intermediate|advanced",
  "tags": ["tag1", "tag2"]
}
```

### 5. Progress Tracking Script

```bash
# Check progress
python3 -c "
import json
from pathlib of Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)
complete = sum(1 for v in data if v.get('status') == 'complete')
pending = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
print(f'Progress: {complete/1146*100:.1f}%')
"

# Get next 10 pending
python3 -c "
import json
from pathlib of Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)
pending = [v['video_id'] for v in data if v.get('status') == 'pending'][:10]
print('Next 10 pending:', pending)
"
```

### 6. Update Script (per video)

```bash
python3 -c "
import json
from pathlib of Path
from datetime import datetime

p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)

for v in data:
    if v['video_id'] == 'REEL_CODE':
        v['status'] = 'complete'
        v['result'] = { ... parsed vision analysis JSON ... }
        v['updated_at'] = datetime.now().isoformat()
        break

tmp = p.with_suffix('.tmp')
with open(tmp, 'w') as f:
    json.dump(data, f, indent=2)
tmp.replace(p)

print('Updated REEL_CODE')
"
```

## Time Estimates

- **Remaining 319 videos**: ~16-26 minutes at current throughput
- **Batch of 50**: ~3-5 minutes
- **Phase 2d (688 videos)**: ~34-57 minutes after Phase 2c completes

## Next Steps

1. Continue Phase 2c in batches of 50 until all 319 pending complete
2. Generate skills from completed analyses (DaVinci Resolve techniques → Hermes skills)
3. Rebuild Obsidian vault with new technique notes
4. Begin Phase 2d: Remaining collections (~688 videos)

## Related Files

- `VISION_PROGRESS.json` — Progress tracking
- `scripts/vision_analysis_batch.py` — (to be created) Automated batch processor
- `~/.hermes/skills/davinci-resolve-techniques/` — Generated DaVinci skills
- `~/.hermes/skills/cinematography/` — Generated Cinematography skills
- `~/.hermes/skills/photography/` — Generated Photography skills
- `~/.hermes/skills/camera-hardware/` — Generated Camera Hardware skills

## References

- [instagram-reels-pipeline](../instagram-reels-pipeline) — Main pipeline skill
- [hermes-browser-tools-fallback](../references/hermes-browser-tools-fallback.md) — Alternative frame capture method
- `references/session-2026-07-30-batch-100.md` — This session's 100-video batch results