# Session 2026-07-31: Local Vision Storage Cleanup & Migration

## Context
Samsung LED external drive reached 96% capacity (5.4 GB free / 120 GB). Pipeline working data must be migrated before continuing processing.

## Root Cause
Accumulated 54+ GB of regeneratable data:
- `CONTENT_PROCESSING/gifs/`: **45 GB** — redundant, NOT linked to vault notes
- `CONTENT_PROCESSING/frames/`: 7.9 GB — regeneratable from original MP4s
- `CONTENT_PROCESSING/transcripts/`: 1.5 GB — regeneratable
- `CONTENT_PROCESSING/analysis/`: 579 MB — regeneratable from VISION_PROGRESS.json

## What to Migrate (Keep Forever)

| Data | Size | Source | Destination |
|------|------|--------|-------------|
| Vault notes + embedded GIFs | **427 MB** (346 MB + 81 MB) | `CONTENT_PROCESSING/vault/` | `~/DaVinci_Vault/` |
| Skills (1,449+) | ~50 MB | `~/.hermes/skills/davinci-resolve-techniques/` | Already on internal ✅ |
| VISION_PROGRESS.json | 2.6 MB | `CONTENT_PROCESSING/VISION_PROGRESS.json` | `~/DaVinci_Vault/` |

## What to Delete (Regeneratable)

| Data | Size | Regenerate From |
|------|------|-----------------|
| `gifs/` | **45 GB** | Frames + ffmpeg |
| `frames/` (completed) | ~6 GB | Original MP4s + ffmpeg |
| `transcripts/` | 1.5 GB | MP4s + Whisper |
| `analysis/` | 579 MB | VISION_PROGRESS.json |

## Migration Commands (No Regeneration)

```bash
# 1. Copy vault to internal
cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault" ~/DaVinci_Vault

# 2. Copy progress tracking
cp "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json" ~/DaVinci_Vault/

# 3. Delete redundant gifs (45 GB)
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs"

# 4. Optionally clean completed frames (keep only error/pending)
# Find completed video_ids from VISION_PROGRESS.json, remove their frame dirs
python3 -c "
import json
with open('~/DaVinci_Vault/VISION_PROGRESS.json') as f:
    data = json.load(f)
completed = {d['video_id'] for d in data if d.get('status') == 'complete'}
import shutil
from pathlib import Path
frames_root = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames')
for vid in completed:
    d = frames_root / vid
    if d.exists():
        shutil.rmtree(d)
        print(f'Removed frames for {vid}')
"

# 5. Verify internal skills already safe
ls ~/.hermes/skills/davinci-resolve-techniques/ | wc -l  # Should be 1449+
```

## Result
- **Free ~54 GB** on Samsung LED (96% → ~50%)
- **All curated outputs preserved** on internal drive
- **Pipeline can continue** processing remaining 116 error + 19 pending videos

## Key Discovery: Vault Already Has Embedded GIFs
- `CONTENT_PROCESSING/vault/media/`: **81 MB** — GIFs embedded in vault notes
- `CONTENT_PROCESSING/gifs/`: **45 GB** — SEPARATE, redundant folder NOT referenced by any vault note
- **Safe to delete gifs/ entirely** — vault already self-contained