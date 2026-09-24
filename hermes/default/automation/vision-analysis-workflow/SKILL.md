---
name: vision-analysis-workflow
description: NVIDIA vision for Instagram Reels to DaVinci techniques.
category: automation
tags: [vision, nvidia-api, instagram, davinci-resolve, batch-processing, reels]
version: 1.0.0
author: Maddie
created: 2026-07-30
---

# Vision Analysis Workflow

Manual batch processing workflow for analyzing Instagram Reels frames via NVIDIA API vision analysis to extract DaVinci Resolve techniques.

## Prerequisites

- Frames already extracted for all videos: `CONTENT_PROCESSING/frames/{video_id}/frame_0001.jpg`
- `VISION_PROGRESS.json` tracks status (complete/pending/error)
- NVIDIA API configured as vision provider in Hermes config (`google-gemini` / `gemini-2.0-flash`)

## Process

### 1. Get Next Pending Video

```bash
python3 -c "
import json
from pathlib import Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)
pending = [v['video_id'] for v in data if v.get('status') == 'pending']
print('Next:', pending[:10])
complete = sum(1 for v in data if v.get('status') == 'complete')
pending_count = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending_count}, Error: {error}')
print(f'Progress: {complete/1146*100:.1f}%')
"
```

### 2. Run Vision Analysis

Use `vision_analyze` tool with first frame:

```python
vision_analyze(
    image_url="/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{VIDEO_ID}/frame_0001.jpg",
    question="Analyze this cinematic shot from Instagram Reel {VIDEO_ID}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look: {\"technique_name\": \"Descriptive name\", \"resolve_page\": \"Color|Edit|Fusion|Fairlight\", \"node_graph_type\": \"serial|parallel|layer_mixer|compound\", \"key_nodes\": [\"node1\", \"node2\"], \"parameters\": {\"param1\": \"value1\"}, \"steps_to_reproduce\": [\"step1\", \"step2\"], \"difficulty\": \"beginner|intermediate|advanced\", \"tags\": [\"tag1\", \"tag2\"]}"
)
```

### 3. Update Progress

```bash
python3 -c "
import json
from pathlib import Path
from datetime import datetime

p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)

for v in data:
    if v['video_id'] == '{VIDEO_ID}':
        v['status'] = 'complete'
        v['result'] = {parsed_json_from_vision}
        v['updated_at'] = datetime.now().isoformat()
        break

tmp = p.with_suffix('.tmp')
with open(tmp, 'w') as f:
    json.dump(data, f, indent=2)
tmp.replace(p)
print('Updated {VIDEO_ID}')
"
```

### 4. Verify Progress

```bash
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
```

## Vision Analysis Prompt Template

```
Analyze this cinematic shot from Instagram Reel {VIDEO_ID}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look:
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

## Performance Notes

- NVIDIA API (gemini-2.0-flash) processes ~1 video/minute
- No rate limits encountered during manual batch processing
- All pending videos have frames extracted (no frame extraction blockers)
- Error rate: 161/1146 (14.0%) - mostly videos with no usable content (text overlays, BTS screenshots)

## Critical: Sub-Agent Parallelization FAILED

**Root Cause Identified (2026-07-30 session):** Sub-agents with local Ollama (ollama-launch/qwen3.5:4b) FAIL for vision_analyze tasks.

- 6 parallel sub-agents dispatched (37 videos each), all timed out at 600s with only 1 API call completed each
- Root cause: vision_analyze uses the parent's NVIDIA vision model (gemini-2.0-flash), NOT local Ollama models
- Sub-agents cannot access the parent's vision model — they inherit the local Ollama config but vision_analyze calls bypass to NVIDIA API
- Manual vision_analyze in main session works reliably (~1 min/video, 100% success rate)
- Sub-agents with cloud provider (ollama-cloud) may work but NOT tested — local Ollama is confirmed broken for this use case

**Do NOT use sub-agents for vision_analyze batch processing.** Manual sequential processing in main session is the only reliable path.

## Output JSON Structure

The vision analysis returns structured technique data that maps to:
- Hermes skills (`~/.hermes/skills/davinci-resolve-techniques/`)
- Obsidian vault notes (`TamaZila Obsidian Vault/.../DaVinci_Knowledge_Base/`)
- DaVinci Resolve node graphs for replication

## Session Metrics (2026-07-30)

- Starting: 722 complete, 283 pending, 141 error
- Ending: 782 complete, 223 pending, 141 error
- Processed: 60 videos in ~60 minutes
- Rate: ~1 video/minute
- Progress: +5% (63% → 68%)