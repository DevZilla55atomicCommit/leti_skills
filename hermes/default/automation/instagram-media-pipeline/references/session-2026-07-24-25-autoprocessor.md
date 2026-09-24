# Session 2026-07-24/25 — Automated downreels.com Pipeline (Complete)

## Overview
Fully automated background processor (`auto_processor.py`) processed **389/389 Instagram Reels** from the Photography/Videography collection via downreels.com using Hermes browser tools. Runs unattended with `notify_on_complete=true`.

## Pipeline Execution
```bash
cd ~/instagram-davinci-pipeline && python3 scripts/auto_processor.py
# Runs in background, notifies on completion
```

## Complete 7-Stage Pipeline (Per Reel)

| Stage | Tool | Details |
|-------|------|---------|
| 1. Download | Hermes browser tools → downreels.com | Serial, 4s delay, 10-URL batches |
| 2. Extract | ffmpeg + Whisper | Frames (1fps), GIF (5s/480p), transcript (optional) |
| 3. Vision | Built-in vision model | 3 frames (0%, 50%, 95%), 3s intervals (20 RPM) |
| 4. Skill | Generate SKILL.md + QUICK_REF.md | In vault Hermes_Skills/ |
| 5. Vault | Obsidian note + YAML frontmatter | Technique breakdown, node graph template |
| 6. Install | Copy to ~/.hermes/skills/creative/ | Makes skills discoverable via `hermes skills list` |
| 7. Cleanup | Remove temp MP4/frames/GIFs | Preserves all artifacts |

## Configuration (auto_processor.py)

```python
# Rate limiting
VISION_RATE_LIMIT = 3.0      # 20 RPM max
DOWNLOAD_BATCH_SIZE = 10
DOWNLOAD_DELAY = 4.0         # 4s between downloads

# Paths (TamaZila Vault)
VISION_DIR = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports")
SKILLS_DIR = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Hermes_Skills")
VAULT_DIR = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels")
TRANSCRIPTS_DIR = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Transcripts")
```

## Skill Installation Function

```python
def install_skill_to_hermes(reel_id: str):
    """Install generated skill to Hermes skill system for discoverability."""
    skill_name = f"davinci-reel-{reel_id[:8]}"
    source_skill = SKILLS_DIR / skill_name
    target_skill = Path("~/.hermes/skills/creative").expanduser() / skill_name
    
    if source_skill.exists() and not target_skill.exists():
        try:
            shutil.copytree(source_skill, target_skill)
            log(f"Installed skill to Hermes: {skill_name}")
        except Exception as e:
            log(f"Failed to install skill {skill_name}: {e}")
    elif target_skill.exists():
        log(f"Skill already installed in Hermes: {skill_name}")
```

## Overnight Run Results (2026-07-25)

| Metric | Result |
|--------|--------|
| **Total reels processed** | **389/389 (100%)** |
| Vision reports | 389/389 |
| Hermes skills installed | 390 (discoverable via `hermes skills list`) |
| Vault notes | 389 (TamaZila Vault) |
| Transcripts | 1 (Whisper/numpy compat issue on Python 3.14) |
| Temp cleanup | ✅ 0B remaining |

## Vault Structure (DaVinci_Knowledge_Base/)

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
├── Vision_Reports/          # 389 JSON (3-frame vision analysis each)
├── Hermes_Skills/           # 390 skill folders (SKILL.md + QUICK_REF.md)
├── Instagram_Reels/
│   └── Photography/
│       └── Videography/     # 389 .md vault notes + {reel_id}_frames/ folders
├── Transcripts/             # Whisper transcripts (when available)
└── Hermes_Skills/           # Duplicate of installed skills (reference)
```

## Hermes Skills Discoverable

```bash
# List all DaVinci Reel skills
hermes skills list | grep davinci-reel
# → 390 skills, category: creative, source: local, status: enabled

# Load a specific skill
/hermes skill load davinci-reel-C02An_Ys

# View quick reference
cat ~/.hermes/skills/creative/davinci-reel-C02An_Ys/QUICK_REF.md
```

## Known Issues

| Issue | Root Cause | Status |
|-------|------------|--------|
| Transcription fails | NumPy 2.4.6 compiled for Python 3.11 on Python 3.14 | Skip gracefully |
| RTF parser returned 0 URLs | Format change / bug in parser | Fixed: regex `https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/?` |
| Vision 429 rate limit | >20 RPM calls | Increase VISION_RATE_LIMIT (min 3s) |

## Files Generated
- `auto_processor.py` — Main orchestrator
- `scripts/extract.py` — ffmpeg + Whisper extraction
- `scripts/rename_batch*.py` — MP4 renaming utilities
- Vision reports → `Vision_Reports/{reel_id}.json`
- Skills → `~/.hermes/skills/creative/davinci-reel-{ID}/` (installed + discoverable)
- Vault notes → `Instagram_Reels/Photography/Videography/{reel_id}.md`