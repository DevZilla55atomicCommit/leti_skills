# Auto Instagram → DaVinci Processor Architecture

## Overview
This document describes the complete architecture of the automated Instagram Reels → DaVinci Resolve knowledge extraction pipeline.

## Pipeline Stages

### Stage 1: Download (downreels.com via Playwright)
- **Tool**: Playwright Chromium headless
- **Target**: downreels.com (Instagram Reels downloader)
- **Authentication**: Session cookies persisted
- **Rate limit**: 4s between downloads
- **Output**: MP4 files in `temp/mp4/{reel_id}.mp4`

### Stage 2: Extract
- **Frames**: ffmpeg at 1fps → `temp/frames/{reel_id}/%04d.jpg`
- **GIF**: First 5 seconds, 15fps, 480p → `temp/gifs/{reel_id}.gif`
- **Transcript**: faster-whisper (base, CPU, int8) → `transcripts/{reel_id}.json`

### Stage 3: Vision Analysis
- **Frames analyzed**: 3 per reel (start, middle, end)
- **Rate limit**: 3s between calls (20 RPM max)
- **Model**: Built-in vision model via `vision_analyze` tool
- **Schema**: Structured JSON with techniques, color grade, camera movement, lighting, composition, DaVinci applicability
- **Rate limiting**: 3s between calls, exponential backoff on 429

### Stage 4: Skill Generation
- **Location**: `DaVinci_Knowledge_Base/Hermes_Skills/davinci-reel-{id[:8]}/`
- **Files**: `SKILL.md` (full), `QUICK_REF.md`
- **Template**: Jinja2-style with technique breakdown, node graph, color recipe

### Stage 5: Vault Notes
- **Location**: `DaVinci_Knowledge_Base/Instagram_Reels/{collection}/`
- **Format**: Obsidian markdown with frontmatter
- **Content**: Summary, techniques, color grade recipe, node structure, media embeds
- **Frames copied**: `frames/{reel_id}_frames/` for embedding

### Stage 6: Cleanup
- Removes: `temp/mp4/`, `temp/frames/`, `temp/gifs/`
- Preserves: Vision reports, skills, vault notes, transcripts

## Configuration

All paths in `config.yaml`:
```yaml
paths:
  rtf_file: "/Users/alfredkamisese/Documents/Photography:Videography URLs.rtf"
  pipeline_dir: "~/instagram-davinci-pipeline"
  temp_dir: "~/instagram-davinci-pipeline/temp"
  
  # Output locations (all in TamaZila Obsidian Vault)
  skills_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Hermes_Skills"
  vault_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels"
  vision_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports"
  transcripts_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Transcripts"
  skills_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Hermes_Skills"
```

## Rate Limiting

| Operation | Limit | Implementation |
|-----------|-------|----------------|
| Vision API | 20 RPM | 3s delay, exponential backoff on 429 |
| Downloads | 15/min | 4s between, batch size 10 |
| Frame extraction | N/A | Sequential per reel |

## Resume Support

- Checkpoint file: `pipeline_state.json`
- Tracks: completed reels, failed reels, current batch
- Resume flag: `--resume` skips completed reels
- Force flag: `--force-reel ID` reprocesses specific reel

## Error Handling

| Error Type | Handling |
|------------|----------|
| Download 404/403 | Logged, marked failed, continue |
| Vision 429 | Exponential backoff (30s→60s→120s→240s→480s) |
| Vision timeout | Retry once, then skip frame |
| Transcription failure | Logged, continues without transcript |
| Skill/Vault write fail | Logged, pipeline continues |
| Cleanup | Always runs via `finally` blocks |

## Monitoring

- Progress logged with timestamps
- Checkpoint file updated per reel
- Log file: `logs/auto_processor_{timestamp}.log`
- Failed reels tracked in `failed_reels.json`

## Dependencies

```bash
pip install playwright pyyaml faster-whisper
playwright install chromium
# System: ffmpeg
```