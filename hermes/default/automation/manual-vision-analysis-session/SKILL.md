---
name: manual-vision-analysis-session
description: Manual vision analysis fallback for sub-agent timeouts.
category: automation
tags: [vision-analysis, manual-processing, instagram-reels, nvidia-gemini, sub-agent-fallback]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-30
---

# Manual Vision Analysis Session Procedure

## When to Use

When sub-agents fail to process vision analysis due to local Ollama models being unable to access the NVIDIA `vision_analyze` API. This happens because sub-agents run in isolated contexts that cannot proxy the main session's NVIDIA vision model.

**Trigger conditions:**
- Sub-agents timeout at 600s with only 1 API call completed
- Error: "Subagent timed out after 600.0s with 1 API call(s) completed"
- Local Ollama models (`ollama-launch/qwen3.5:4b`) cannot proxy NVIDIA vision API

## Procedure

### Prerequisites
- Main session has active NVIDIA provider with `vision_analyze` tool
- `VISION_PROGRESS.json` exists with pending videos
- Frames extracted and available at `/Volumes/Samsung LED/.../frames/{VIDEO_ID}/frame_0001.jpg`

### Step-by-Step

```bash
# 1. Get next pending videos
python3 -c "
import json
from pathlib import Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)
pending = [v['video_id'] for v in data if v.get('status') == 'pending'][:10]
print('Next 10 pending:', pending)
"
```

### Process Each Video (Loop)

For each `VIDEO_ID` in pending list:

```python
# 1. Vision analysis on first frame
result = vision_analyze(
    image_url=f"/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{VIDEO_ID}/frame_0001.jpg",
    question="Analyze this cinematic shot from Instagram Reel {VIDEO_ID}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look: {{\"technique_name\": \"Descriptive name\", \"resolve_page\": \"Color|Edit|Fusion|Fairlight\", \"node_graph_type\": \"serial|parallel|layer_mixer|compound\", \"key_nodes\": [\"node1\", \"node2\"], \"parameters\": {{\"param1\": \"value1\"}}, \"steps_to_reproduce\": [\"step1\", \"step2\"], \"difficulty\": \"beginner|intermediate|advanced\", \"tags\": [\"tag1\", \"tag2\"]}}"
)

# 2. Update progress JSON
import json
from pathlib import Path
from datetime import datetime

p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)

for v in data:
    if v['video_id'] == VIDEO_ID:
        v['status'] = 'complete'
        v['result'] = result['analysis']  # or parsed JSON from result
        v['updated_at'] = datetime.now().isoformat()
        break

tmp = p.with_suffix('.tmp')
with open(tmp, 'w') as f:
    json.dump(data, f, indent=2)
tmp.replace(p)

print(f'Updated {VIDEO_ID}')
```

### After Each Batch (20-30 videos)

```bash
# Check progress
python3 -c "
import json
from pathlib import Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f:
    data = json.load(f)
complete = sum(1 for v in data if v.get('status') == 'complete')
pending = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
print(f'Progress: {complete/1146*100:.1f}%')
print(f'Session: {complete - 722}')
"
```

## Expected Performance

| Metric | Value |
|--------|-------|
| Time per video | ~1 minute |
| Success rate | ~99.5% |
| Rate limit | ~20 RPM (NVIDIA) |
| Manual pace | ~1 video/minute |

## After Completion

Re-run downstream pipeline:

```bash
# Regenerate skills from updated progress
python3 ~/.hermes/scripts/generate_skills.py

# Rebuild Obsidian vault
python3 ~/.hermes/scripts/build_vault.py
```

## Key Learnings (2026-07-30 Session)

1. **Sub-agents cannot access main session's vision API** — local Ollama sub-agents cannot proxy NVIDIA `vision_analyze` calls (600s timeout, 1 API call)

2. **Manual in main session is reliable** — 236 videos processed this session (722→958), 1 error, consistent ~1 min/video

3. **Downstream pipeline is decoupled and ready** — just needs vision analysis complete

5. **Progress: 83.6% of Phase 2c done** — 958/1,146 Cinematic/Shooting videos complete, 47 pending, 142 errors

6. **Session metrics**: 236 videos processed in this session (722→958), ~1 min/video pace, 99.5% success rate

## Common Issues

| Issue | Fix |
|-------|-----|
| Vision API returns malformed JSON | Wrap in try/except, extract `analysis` field |
| Frame file not found | Check frame extraction completed; re-extract if needed |
| Progress JSON corruption | Use atomic write with `.tmp` suffix then `replace()` |
| Rate limit (429) | Wait 3 seconds between calls |

## Next Steps After Completion

1. Re-run downstream scripts: `generate_skills.py` then `build_vault.py`
2. Begin Phase 2d (remaining collections ~688 videos)