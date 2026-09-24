# Auto-Processor Reference

## Overview
Fully automated background processor for Instagram Reels → DaVinci Resolve knowledge pipeline.

**File**: `scripts/auto_processor.py`  
**Entry Point**: `asyncio.run(main())`  
**Background Execution**: `notify_on_complete=true` with `background=true`

## Architecture

### Pipeline Stages (7 stages per reel)
```
1. DOWNLOAD     → downreels.com via headless browser (Hermes browser tools)
2. EXTRACT      → ffmpeg frames (1fps), GIF (5s/480p), transcript (Whisper)
3. VISION       → 3-frame analysis (0%, 50%, 95%) at 3s intervals (20 RPM)
4. SKILL        → Hermes skill + QUICK_REF.md in ~/.hermes/skills/creative/
5. VAULT        → Obsidian note with YAML frontmatter, media refs, skill link
6. INSTALL      → Copy skill to ~/.hermes/skills/creative/ (discoverable)
7. CLEANUP      → Remove temp MP4/frames/GIFs (preserve skills/vault/vision)
```

### Rate Limiting
| Operation | Limit | Implementation |
|-----------|-------|----------------|
| Vision calls | 3s delay | 20 RPM max |
| Downloads | 4s delay | downreels.com politeness |
| Batch size | 10 reels | Sequential within batch |

### RTF Parser (Fixed 2026-07-24)
```python
urls = re.findall(r'https://www\\.instagram\\.com/reel/[A-Za-z0-9_-]+/?', content)
# Deduplicate + assign default collection "Photography/Videography"
```

### Progress Tracking
```python
completed = set(f.stem for f in VISION_DIR.glob("*.json"))
pending = [(u, c) for u, c in urls if u.split("/")[-2] not in completed]
```

## Usage
```bash
# Foreground (debug)
python3 scripts/auto_processor.py

# Background (production)
python3 scripts/auto_processor.py &
# Or with notify:
python3 scripts/auto_processor.py &  # notify_on_complete=true in terminal
```

## Output Artifacts
| Location | Content |
|----------|---------|
| `vision_reports/{reel_id}.json` | 3-frame vision analysis |
| `~/.hermes/skills/creative/davinci-reel-{id}/SKILL.md` | Full Hermes skill |
| `~/.hermes/skills/creative/davinci-reel-{id}/QUICK_REF.md` | Quick reference card |
| `~/Obsidian/EMAI/Instagram Reels/{collection}/{reel_id}.md` | Obsidian note |
| `temp/` | Cleaned up after each reel |

## Monitoring
```bash
# Progress
ls vision_reports/ | wc -l
ls ~/.hermes/skills/creative/davinci-reel-* 2>/dev/null | wc -l
ls ~/Obsidian/EMAI/Instagram\\ Reels/Photography/Videography/*.md | wc -l

# Process status
ps aux | grep auto_processor
du -sh temp/
```

## Error Handling
- Failed downloads: Logged, skipped, continue batch
- Vision failures: Logged, skill/vault still generated with partial data
- Cleanup: Runs even on partial failure (best effort)
- Resume: Re-run skips already-completed (vision_report exists)

## Estimated Throughput
| Metric | Value |
|--------|-------|
| Reels/hour | ~10 |
| Vision calls/min | 20 |
| Time per reel | ~6 min (serial) |
| 389 reels | ~35-40 hours |

## 2026-07-25 Overnight Run Results
| Metric | Value |
|--------|-------|
| **Total reels processed** | **389/389 (100%)** |
| Vision reports | 389/389 |
| Hermes skills installed | 390 (discoverable via `hermes skills list`) |
| Vault notes | 389 (TamaZila Vault: DaVinci_Knowledge_Base/Instagram_Reels/) |
| Transcripts | 1 (Whisper/numpy compatibility issue) |
| Temp cleanup | ✅ 0B remaining |

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Transcription fails | NumPy/Python 3.14 compat | Known: numpy 2.4.6 compiled for 3.11 on 3.14 — skip gracefully |
| Auto-processor crashes | numpy import error | Reinstall numpy in correct venv: `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/pip install --force-reinstall numpy` |
| RTF parser returns 0 URLs | Format change | Use regex `https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?` on raw RTF text |
| Playwright timeout | Network/load | Increase timeout in config, check network |
| Vision timeout | Frame file missing | Verify frame file exists before vision call |
| Skill generation fails | SKILLS_DIR not writable | Check permissions, template exists |
| Vault note fails | VAULT_DIR not writable | Check collection folder exists |

## Key Technical Patterns

### Serial 10-URL Batch Pipeline (Validated 2026-07-23)
```python
async def process_batch(batch_urls):
    for url, collection in batch_urls:
        reel_id = extract_reel_id(url)
        mp4_path = await download_via_downreels(page, url)
        extraction = await extract_frames_gif_transcript(mp4_path)
        vision_report = await analyze_3_frames(extraction, reel_id)
        skill_path = generate_skill(vision_report)
        vault_path = generate_vault_note(vision_report, skill_path)
        install_skill_to_hermes(skill_path)  # NEW: auto-install
        cleanup_temp_files(reel_id)
```

### Auto-Install Skills to Hermes
```python
def install_skill_to_hermes(reel_id: str):
    skill_name = f"davinci-reel-{reel_id[:8]}"
    source = SKILLS_DIR / skill_name
    target = Path("~/.hermes/skills/creative").expanduser() / skill_name
    if source.exists() and not target.exists():
        shutil.copytree(source, target)
        log(f"Installed skill to Hermes: {skill_name}")
```

### RTF URL Extraction
```python
import re
content = rtf_path.read_text(encoding='utf-8', errors='ignore')
urls = re.findall(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?', content)
unique = [(u, "Photography/Videography") for u in dict.fromkeys(urls)]
```

### Vision Rate Limiting
```python
async def vision_analyze_frame(image_path, reel_id, timestamp):
    await asyncio.sleep(3.0)  # 20 RPM = 3s between calls
    # call vision model
```

## File Structure
```
instagram-davinci-pipeline/
├── scripts/
│   ├── auto_processor.py       # Main pipeline (background)
│   ├── extract.py              # ffmpeg + whisper
│   ├── rename_batch*.py        # MP4 renaming helpers
│   └── download_reels.py       # Playwright downloader
├── temp/
│   ├── mp4/                    # Downloaded MP4s (cleaned)
│   ├── frames/                 # Extracted frames (cleaned)
│   └── gifs/                   # Generated GIFs (cleaned)
├── vision_reports/             # Persistent vision JSON
├── transcripts/                # Persistent transcripts
└── extraction_manifest.json    # Pipeline state
```