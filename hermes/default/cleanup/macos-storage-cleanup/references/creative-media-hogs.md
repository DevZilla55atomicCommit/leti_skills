# Creative Media Storage Hogs (2026-07-31)

## Instagram Reels Pipeline Specific

### CONTENT_PROCESSING/gifs/ — 45 GB
- **Source**: GIF generation for every processed reel (preview animations)
- **Regeneratable**: Yes, from frames/ via ffmpeg
- **Cleanup**: `rm -rf CONTENT_PROCESSING/gifs/` — safe, 45 GB instant recovery
- **Frequency**: Clean monthly or when disk >85%

### CONTENT_PROCESSING/frames/ — 7.9 GB
- **Source**: Extracted frames (8 per video) for 1,165+ videos
- **Retention**: Keep only for pending/error videos
- **Cleanup**: Delete frames for completed videos (1,030+)
- **Script**: `find frames/ -maxdepth 1 -type d | while read d; do if ! grep -q "$(basename $d)" VISION_PROGRESS.json; then rm -rf "$d"; fi; done`

### CONTENT_PROCESSING/transcripts/ — 1.5 GB
- **Source**: Whisper/transcription outputs
- **Regeneratable**: Yes, from source MP4s
- **Cleanup**: Safe to delete for completed videos

### CONTENT_PROCESSING/vault/ — 346 MB — **KEEP**
- Final output notes, searchable knowledge base

## DaVinci Resolve
- `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/` — Cache, render files
- `/Volumes/Samsung LED/Resolve Projects/` — Project files, render cache
- Cleanup: `DaVinci Resolve → Playback → Delete Render Cache → All`

## Ollama Models
- `~/.ollama/models/blobs/` — Model weights (deduplicated layers)
- `ollama list` shows logical size; `du` shows physical
- Remove unused: `ollama rm <model>` (frees shared blobs only if no other model uses them)

## Browser Caches
- `~/Library/Caches/Google/Chrome/` — Includes on-device AI models (~1-5 GB)
- `~/Library/Caches/com.apple.Safari/` — Protected, don't delete

## Quick Scan for This Project
```bash
# Project-specific
du -sh /Volumes/Samsung\ LED/Instagram\ Downloads/New\ Untouched\ Reels\ Download/CONTENT_PROCESSING/*

# System-wide
du -sh ~/Library/Caches/* ~/.cache/* ~/.ollama ~/.lmstudio 2>/dev/null | sort -hr
```