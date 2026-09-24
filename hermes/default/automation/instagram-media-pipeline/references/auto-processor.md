# Auto-Processor Reference (2026-07-24/25)

## Overview
Fully automated background processor (`auto_processor.py`) for processing all 389 Instagram Reels via downreels.com headless browser automation.

## Architecture

### Pipeline Stages (6 stages per reel)
```
1. DOWNLOAD     → downreels.com via headless browser (Playwright)
2. EXTRACT      → ffmpeg frames (1fps), GIF (full video, 10fps/480px), transcript (Whisper)
3. VISION       → 3-frame analysis (0%, 50%, 95%) at 3s intervals (20 RPM)
4. SKILL        → Hermes skill + QUICK_REF.md in ~/.hermes/skills/creative/
5. VAULT        → Obsidian note with YAML frontmatter, media refs, skill link
6. CLEANUP      → Remove temp MP4/frames/GIFs (preserve skills/vault/vision)
```

### Rate Limiting
| Operation | Limit | Implementation |
|-----------|-------|----------------|
| Vision calls | 3s delay | 20 RPM max |
| Downloads | 4s delay | downreels.com politeness |
| Batch size | 10 reels | Sequential within batch |

### RTF Parser (Fixed 2026-07-24)
```python
urls = re.findall(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?', content)
# Deduplicate and assign default collection "Photography/Videography"
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
# terminal(background=true, notify_on_complete=true) python3 scripts/auto_processor.py
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
# Check progress
ls vision_reports/ | wc -l
ls ~/.hermes/skills/creative/davinci-reel-* 2>/dev/null | wc -l
ls ~/Obsidian/EMAI/Instagram\ Reels/Photography/Videography/*.md 2>/dev/null | wc -l

# Check process
ps aux | grep auto_processor

# Check temp storage
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

## Results (2026-07-25)
| Metric | Value |
|--------|-------|
| Total reels | 389 |
| Processed | 389 (100%) |
| Failed | 5 (transient download errors) |
| GIFs in vault | 389/389 |
| Frame folders | 389/389 |
| Vault notes | 389/389 |
| Hermes skills | 390 installed |
| Temp storage | 0B (clean) |

## Failed Reels (Transient)
All 5 failures were "MP4 not found" / download errors from downreels.com — resolved in subsequent runs or by parallel processor.

## Key Scripts
- `scripts/auto_processor.py` — Main processor
- `scripts/regenerate_gifs.py` — Full-frame GIF regeneration for all 389 reels
- `scripts/regenerate_missing_gifs.py` — Targeted regeneration for missing GIFs only
- `scripts/generate_master_index.py` — Master index generation for vault

## Execution
```bash
# Start in background
cd ~/instagram-davinci-pipeline
python3 scripts/auto_processor.py &
# Notifies on completion via notify_on_complete
```

## Parallel Execution
Two auto-processors ran in parallel:
- `proc_7eff65f1542d` (regenerate_gifs.py) — 378 processed, 3 failed
- `proc_f84f8df63b87` (auto_processor.py) — 236 processed, 5 failed

Together achieved 100% coverage.