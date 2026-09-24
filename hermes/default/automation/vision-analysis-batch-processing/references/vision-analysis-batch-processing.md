# Vision Analysis Batch Processing — Detailed Reference

## Overview

This document captures the methodology and findings from the Cinematic/Shooting vision analysis batch processing (Phase 2c) of the Instagram Reels → DaVinci Resolve pipeline.

## Configuration

- **Vision Provider**: NVIDIA API (google/diffusiongemma-26b-a4b-it)
- **Model**: google/diffusiongemma-26b-a4b-it
- **Input**: Pre-extracted frames at `/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{REEL_CODE}/frame_0001.jpg`
- **Progress Tracking**: `VISION_PROGRESS.json` with fields: `video_id`, `status` (complete/pending/error), `result`, `updated_at`
- **Batch Size**: 50 videos per session
- **Rate Limit**: ~3-5 seconds per video via NVIDIA API

## Phase 2c Status (as of 2026-07-30)

| Metric | Count | Percentage |
|--------|-------|------------|
| **Complete** | 688 | 60.0% |
| **Pending** | 319 | 27.8% |
| **Errors** | 139 | 12.1% |
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
- Created 8 class-level non-Resolve skills:
  - **Cinematography** (2): `gimbal-movement-basics`, `camera-movement-transitions`
  - **Photography** (5): `architectural-photography-lighting`, `lens-selection-cinematic-look`, `gimbal-camera-movements`, `split-screen-comparison-technique`, `color-grading-theory-fundamentals`, `motion-graphics-fundamentals-fusion`
  - **Camera Hardware** (1): `camera-gear-workflow`

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