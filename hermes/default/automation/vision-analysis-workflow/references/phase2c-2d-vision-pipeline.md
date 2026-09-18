# Phase 2c/2d Vision Analysis Pipeline (2026-07-30)

Manual vision analysis pipeline for the Cinematic/Shooting collection (1,146 videos) using NVIDIA API (gemini-2.0-flash) via Hermes `vision_analyze` tool.

## Pipeline Architecture

```
Phase 1: Frame Extraction ✅ COMPLETE
  - 8 frames per video via ffmpeg at 0/14/28/42/57/71/86/100%
  - Stored at CONTENT_PROCESSING/frames/{video_id}/frame_0001.jpg

Phase 2a: DaVinci Core Vision Analysis ✅ COMPLETE
  - 459 DaVinci-specific videos processed
  - 176+ Hermes skills generated

Phase 2b: Skill Installation ✅ COMPLETE
  - 176+ skills installed to ~/.hermes/skills/davinci-resolve-techniques/

Phase 2c: Cinematic/Shooting Vision Analysis (COMPLETE)
  - 1,146 videos total (Cinematic + Shooting collections)
  - 985 complete (86.0%), 0 pending, 161 errors (14.0%)
  - Manual vision_analyze only reliable path

Phase 2d: Remaining Collections Vision Analysis (PENDING)
  - ~688 videos from other collections
  - Same manual process
```

## Vision Analysis Process

```bash
# 1. Get next pending video
python3 -c "
import json
from pathlib import Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
with open(p) as f: data = json.load(f)
pending = [v['video_id'] for v in data if v.get('status') == 'pending']
print('Next:', pending[:10])
"

# 2. Run vision_analyze on first frame
vision_analyze(
    image_url="/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{VIDEO_ID}/frame_0001.jpg",
    question="Analyze this cinematic shot from Instagram Reel {VIDEO_ID}..."
)

# 3. Update progress JSON
python3 -c "
import json
from pathlib import Path
from datetime import datetime
p = Path('.../VISION_PROGRESS.json')
with open(p) as f: data = json.load(f)
for v in data:
    if v['video_id'] == '{VIDEO_ID}':
        v['status'] = 'complete'
        v['result'] = parsed_json
        v['updated_at'] = datetime.now().isoformat()
        break
tmp = p.with_suffix('.tmp')
with open(tmp, 'w') as f: json.dump(data, f, indent=2)
tmp.replace(p)
"
```

## Sub-Agent Parallelization — CONFIRMED BROKEN (2026-07-30)

**Do NOT use sub-agents for vision_analyze batch processing.**

- 6 parallel sub-agents launched with local Ollama (ollama-launch/qwen3.5:4b)
- All timed out at 600s with only 1 API call completed each
- Root cause: vision_analyze uses parent's NVIDIA vision model (gemini-2.0-flash), NOT local Ollama
- Sub-agents inherit local Ollama config but vision_analyze calls bypass to NVIDIA API
- Manual vision_analyze in main session works reliably (~1 min/video, 100% success)
- ollama-cloud sub-agents untested — local Ollama confirmed broken for this use case

## Performance Metrics

| Metric | Value |
|--------|-------|
| Rate | ~1 video/minute |
| Total Cinematic/Shooting | 1,146 videos |
| Completed this session | 263 videos |
| Progress | 63% → 86% (+23%) |
| Error rate | 14.0% (161/1146) |
| Downstream skills | 1,449+ in davinci-resolve-techniques/ |
| Vault notes | 985+ technique notes with GIFs |

## Downstream Pipeline (Automated)

After vision analysis completes for a batch:
1. `generate_skills.py` — Creates Hermes skills from vision results
2. `build_vault.py` — Creates Obsidian vault notes with embedded frames/GIFs
3. Both scripts support incremental updates (process only new completions)