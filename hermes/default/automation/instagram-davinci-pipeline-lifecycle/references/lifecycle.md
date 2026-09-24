# Instagram → DaVinci Pipeline Lifecycle Reference

## Overview
This document captures the complete lifecycle of the Instagram Reels → DaVinci Resolve knowledge extraction pipeline, from URL ingestion to permanent vault storage with Hermes skill integration.

## Pipeline Stages

### Stage 1: URL Ingestion & Deduplication
- **Input**: RTF file with Instagram Reel URLs
- **Process**: Regex extraction → deduplication → pending queue
- **Output**: Unique reel IDs with collection metadata

### Stage 2: Download (downreels.com)
- **Tool**: Playwright headless browser via `download_reels.py`
- **Rate limit**: 4s between downloads, batch size 10
- **Output**: MP4 files in `~/instagram-davinci-pipeline/temp/mp4/`

### Stage 3: Extraction
- **Frames**: ffmpeg 1fps → `temp/frames/{reel_id}/`
- **GIF**: ffmpeg 5s, 15fps, 480p → `temp/gifs/{reel_id}.gif`
- **Transcript**: faster-whisper (base model, CPU) → `transcripts/{reel_id}.json`

### Stage 4: Vision Analysis
- **Frames analyzed**: 3 per reel (start, middle, end)
- **Rate limit**: 3s between calls (20 RPM hard limit)
- **Output**: JSON vision reports in `vision_reports/`

### Stage 5: Skill & Vault Generation
- **Hermes skill**: `davinci-reel-{reel_id[:8]}/` with SKILL.md + QUICK_REF.md
- **Vault note**: Markdown with DaVinci recipe, keyframes, media table
- **Frame copy**: JPGs copied to vault for embedding

### Stage 5.5: Hermes Skill Installation
- **Auto-install**: Copy skill from vault to `~/.hermes/skills/creative/`
- **Result**: Skills discoverable via `hermes skills list`

### Stage 6: Cleanup
- **Removes**: `temp/mp4/`, `temp/frames/`, `temp/gifs/`
- **Preserves**: Vault notes, frames, GIFs, skills, vision reports

## Key Artifacts & Locations

| Artifact | Permanent Location | Temp Location |
|----------|-------------------|---------------|
| MP4 | ❌ Not stored | `temp/mp4/` |
| Frames (JPG) | `Instagram_Reels/Photography/Videography/{reel_id}_frames/` | `temp/frames/` |
| GIF | `Instagram_Reels/Photography/Videography/{reel_id}.gif` | `temp/gifs/` |
| Vision Report | `Vision_Reports/{reel_id}.json` | `vision_reports/` |
| Transcript | `Transcripts/{reel_id}.json` | `transcripts/` |
| Hermes Skill | `~/.hermes/skills/creative/davinci-reel-*/` | `Hermes_Skills/davinci-reel-*/` |
| Vault Note | `Instagram_Reels/Photography/Videography/{reel_id}.md` | - |

## Rate Limits & Constraints

| Limit | Value | Enforcement |
|-------|-------|-------------|
| Vision API | 20 RPM | 3s sleep between calls |
| Download | ~10/40s | 4s delay, batch size 10 |
| Instagram | 40 RPM | Via downreels.com |
| Storage | Samsung SSD 120GB | 70GB free |

## Storage Breakdown (389 reels)

| Type | Count | Size |
|------|-------|------|
| Frame folders (JPG) | 389 | ~2-3 GB |
| GIFs (full video) | 389 | ~3-4 GB |
| Vault notes | 389 | ~1 MB |
| Vision reports | 389 | ~1 MB |
| Hermes skills | 390 | ~5 MB |
| **Total** | | **~5.5 GB** |

## Known Issues & Workarounds

1. **Transcription failure**: numpy/Python 3.14 compatibility → only 1 transcript succeeded
2. **GIF regeneration needed**: First run missed GIF copy to vault → regenerated 246 missing
3. **MP4 cleanup**: Runs per-reel after processing, not batch
4. **Vision rate limit**: Hard 20 RPM → 3s sleep minimum
5. **Storage**: GIFs are largest (up to 140MB each); consider compression

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-24 | Initial pipeline design |
| 1.1 | 2025-07-24 | Fixed GIF copy to vault, added Hermes auto-install |
| 1.2 | 2025-07-24 | Regenerated 246 missing GIFs, updated cleanup |

## Session 2025-07-24 Summary

- **389/389 reels** fully processed
- **389 vision reports** created
- **389 vault notes** created with DaVinci recipes
- **390 Hermes skills** installed and discoverable
- **389 frame folders** with JPG keyframes
- **389 GIFs** in vault (regenerated 246 missing)
- **1 transcript** (numpy/whisper issue)
- **5.5 GB** total vault storage