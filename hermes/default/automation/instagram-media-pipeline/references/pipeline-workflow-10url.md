# Pipeline Workflow Reference — 10-URL Batch via Downreels.com

**Session:** 2026-07-22  
**Context:** User accepted downreels.com as third-party downloader trade-off vs account ban. Designed full pipeline for 10-URL batches.

## Pipeline Stages (Serial, One-by-One)

```
URLS.TXT (10 lines: "URL | collection")
       │
       ▼
STAGE 1: DOWNLOAD (downreels.com via headless browser)
       • Playwright serial, 4s delay between URLs
       • Output: temp/mp4/{reel_id}.mp4 + download_manifest.json
       • State: state.json (completed[], failed{})
       │
       ▼
STAGE 2: EXTRACT (local ffmpeg + whisper.cpp)
       • 1fps frames → temp/frames/{reel_id}/
       • 5s GIF (15fps, 480p) → temp/gifs/{reel_id}.gif
       • Transcript if speech detected → temp/transcripts/
       • Output: extraction_manifest.json
       │
       ▼
STAGE 3: VISION ANALYZE (built-in vision, 20 RPM limit)
       • 3 keyframes (start/mid/end) per reel
       • Schema: techniques[], node_structure, color_grade, camera_movement
       • 3s between calls, exponential backoff on 429
       • Output: vision_reports/{reel_id}.json
       │
       ▼
STAGE 4: SKILL GENERATION (template-based)
       • Map vision report → Hermes skill template
       • Template: davinci-resolve-* technique skill
       • Output: ~/.hermes/skills/creative/davinci-reel-{id}/SKILL.md
       │
       ▼
STAGE 5: VAULT NOTE (Obsidian-ready)
       • Note: vault/Instagram Reels/{collection}/{reel_id}.md
       • Embed: GIF, transcript, vision summary, skill link
       • YAML frontmatter with tags, collection, metadata
       │
       ▼
STAGE 6: CLEANUP (verify then remove)
       • Verify: skills exist, vault notes valid, manifests complete
       • Remove: temp/mp4/, temp/frames/, temp/gifs/
       • Keep: transcripts/, vision_reports/, skills/, vault notes
```

## Rate Limit Strategy

| Stage | Limit | Implementation |
|-------|-------|----------------|
| Download | ~15/min | 4s sleep between requests |
| Vision | 20 RPM (user preference) | 3s between calls, 30s→60s→120s→240s→480s backoff on 429 |
| Extraction | Local only | No API limit |

## Key Design Decisions

1. **Serial everything** — User explicitly requested one-by-one to avoid API limits
2. **State-based resume** — Every stage writes state.json; crash = resume from last completed
3. **Manifest chain** — Each stage produces manifest linking to next stage inputs
4. **Temp isolation** — All large files (MP4, frames, GIFs) in `temp/` deleted after verification
5. **Collection from URL list** — User provides `URL | collection` pairs; no auto-classification

## File Structure

```
~/instagram-davinci-pipeline/
├── urls.txt                      # Input: 10 lines "URL | Color Grading"
├── state.json                    # Resume state across all stages
├── download_manifest.json        # Stage 1 output
├── extraction_manifest.json      # Stage 2 output
├── vision_reports/               # Stage 3 output
├── temp/
│   ├── mp4/                      # CLEANED UP
│   ├── frames/                   # CLEANED UP
│   ├── gifs/                     # CLEANED UP
│   └── transcripts/              # KEPT
├── skills/                       # Stage 4 output (symlinks to ~/.hermes/skills/)
└── vault_notes/                  # Stage 5 output (copy to Obsidian vault)
```

## Test First (Single URL)

Before batch: run full 6 stages on 1 URL (DDq6fmTR0HM | Color Grading) → verify cleanup works → then scale to 10.