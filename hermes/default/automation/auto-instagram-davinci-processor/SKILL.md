---
name: auto-instagram-davinci-processor
description: "Fully automated Instagram Reels → DaVinci Resolve knowledge extraction pipeline. Downloads reels via downreels.com, extracts frames/GIFs/transcripts, runs vision analysis, generates Hermes skills and Obsidian vault notes in DaVinci_Knowledge_Base."
category: automation
tags: [instagram, davinci-resolve, color-grading, automation, pipeline, vision-analysis, obsidian, hermes-skills]
version: 1.0.0
author: Maddie (Hermes Agent)
created: 2026-07-24
---

# Auto Instagram → DaVinci Resolve Processor

**Fully automated Instagram Reels → DaVinci Resolve knowledge extraction pipeline.**

This skill encapsulates the complete automated pipeline that processes Instagram Reels through all 6 stages:
1. **Download** — via downreels.com (Playwright automation)
2. **Extract** — frames (1fps), GIFs (5s), transcripts (Whisper)
3. **Vision Analysis** — 3-frame analysis per reel (start/middle/end)
4. **Skill Generation** — Hermes skills in DaVinci_Knowledge_Base/Hermes_Skills
5. **Vault Notes** — Obsidian markdown in DaVinci_Knowledge_Base/Instagram_Reels
6. **Cleanup** — temp file removal

## Quick Start

```bash
# 1. Prepare URLs file (one per line: URL | collection)
cat > urls.txt << 'EOF'
https://www.instagram.com/reel/C9FAL50v1is/ | Photography/Videography
https://www.instagram.com/reel/C8mRuJHBNMy/ | Photography/Videography
EOF

# 2. Run processor
python3 auto_processor.py --urls-file urls.txt --batch-size 10

# Dry run to preview
python3 auto_processor.py --urls-file urls.txt --dry-run

# Resume interrupted run
python3 auto_processor.py --urls-file urls.txt --resume
```

## Configuration

All paths configurable via `config.yaml`:

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

# Critical: All paths MUST use the actual TamaZila Obsidian Vault path
# NOT ~/Obsidian/EMAI/ or any other location
# The actual vault path is: /Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
```
# Rate limiting
vision_rate_limit: 3.0  # seconds between vision calls
download_batch_size: 10
download_delay: 4.0

# Processing
vision_frames_per_reel: 3
vision_rate_limit_seconds: 3
```

## Pipeline Stages

### Stage 1: Download (downreels.com)
- Uses Playwright to automate downreels.com
- Headless Chromium, headless mode
- Cookies persisted for session reuse
- Rate limited: 4s between downloads

### Stage 2: Extract
- **Frames**: ffmpeg 1fps → `temp/frames/{reel_id}/%04d.jpg`
- **GIF**: First 5 seconds, 15fps, 480p → `temp/gifs/{reel_id}.gif`
- **Transcript**: faster-whisper (base model, CPU, int8) → `transcripts/{reel_id}.json`

### Stage 3: Vision Analysis
- 3 frames per reel: start (0%), middle (50%), end (100%)
- Rate limited: 3s between calls (20 RPM max)
- Structured JSON output per schema
- Results saved to `Vision_Reports/{reel_id}.json`

### Stage 4: Skill Generation
- Hermes skill in `DaVinci_Knowledge_Base/Hermes_Skills/davinci-reel-{id[:8]}/`
- SKILL.md with technique breakdown, node graph, color grade recipe
- QUICK_REF.md for quick reference

### Stage 5: Vault Note
- Obsidian markdown in `DaVinci_Knowledge_Base/Instagram_Reels/{collection}/`
- Embedded frames, GIF, technique table, skill link
- Frames copied to `{collection}/{reel_id}_frames/`

### Stage 6: Cleanup
- Removes `temp/mp4/`, `temp/frames/`, `temp/gifs/`
- Preserves vision reports, skills, vault notes, transcripts

## Rate Limiting & Safety

- **Vision API**: 3s between calls (20 RPM max), exponential backoff on 429
- **Downloads**: 4s between, batch size 10, session reuse
- **Retries**: 3x with exponential backoff (30s, 60s, 120s)
- **Checkpointing**: Progress saved every reel, resume supported

## Critical Pitfalls & Lessons Learned

### ⚠️ Vault Path Must Be Exact
**CRITICAL**: All output paths MUST point to the exact TamaZila Obsidian Vault path:
```
✅ CORRECT: /Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
❌ WRONG: ~/Obsidian/EMAI/Instagram Reels/
❌ WRONG: ~/Obsidian/EMAI/
❌ WRONG: ~/instagram-davinci-pipeline/vault/
```

The pipeline was previously writing to `~/Obsidian/EMAI/Instagram Reels/` which is a different vault entirely. The correct DaVinci_Knowledge_Base lives inside the TamaZila Obsidian Vault at:
```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
```

If paths are wrong, artifacts appear in the wrong vault and won't be discoverable in the intended knowledge base.

### ⚠️ VISION_REPORT_DIR Must Be Defined (Fixed v1.0.1)
The `get_completed_reels()` function references `VISION_REPORT_DIR` which must be defined as an alias to `VISION_DIR` (or the actual vision reports directory). Undefined variable crashes the pipeline on startup.

**Fixed in v1.0.1**: `VISION_REPORT_DIR = VISION_DIR` is now explicitly defined in the configuration section. The pipeline no longer crashes on startup due to undefined variable.

### ⚠️ GIF Files Must Be Copied to Vault Before Cleanup (Fixed v1.0.3)
The pipeline generates GIFs in `temp/gifs/{reel_id}.gif` but was **not copying them to the vault** before the cleanup stage deleted `temp/gifs/`. This resulted in permanent loss of all GIFs.

**Fixed in v1.0.3**: Added GIF copy step in `generate_skill_and_vault()`:
```python
# Copy GIF to vault alongside frames
gif_path = GIFS_DIR / f"{reel_id}.gif"
vault_gif = VAULT_DIR / collection / f"{reel_id}.gif"
if gif_path.exists():
    shutil.copy2(gif_path, vault_gif)
```

**Verification**: GIFs now appear in vault at `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/Photography/Videography/{reel_id}.gif`

### 🐍 NumPy/Python 3.14 Compatibility (Critical - v1.0.2)
The environment uses **Python 3.14** with **NumPy 2.4.6** (compiled for Python 3.11). This causes `ModuleNotFoundError: No module named 'numpy._core._multiarray_umath'` when importing `faster-whisper` or other NumPy-dependent packages.

**Workaround Applied (v1.0.2)**:
```bash
# Force reinstall NumPy for Python 3.11 (the actual runtime)
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/pip install --upgrade --force-reinstall numpy

# Reinstall affected packages
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/pip install --upgrade --force-reinstall faster-whisper
```

**Note**: The Hermes agent venv uses Python 3.11 (`/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python`), but the system Python is 3.14. NumPy wheels must match the venv's Python version (3.11), not the system Python (3.14).

**Transcription Impact**: Whisper transcription is currently unstable due to this issue. Pipeline continues but marks transcriptions as failed. Vision analysis continues unaffected.

### 🎯 Rate Limits Must Be Respected
- Vision API: 3s between calls (20 RPM max) — 429 errors trigger exponential backoff
- Downloads: 4s between, batch size 10 — downreels.com blocks aggressive scraping

## Output Structure

```
DaVinci_Knowledge_Base/
├── Vision_Reports/
│   ├── C9FAL50v1is.json
│   └── ...
├── Hermes_Skills/
│   ├── davinci-reel-C9FAL50/
│   │   ├── SKILL.md
│   │   └── QUICK_REF.md
│   └── ...
├── Instagram_Reels/
│   └── Photography/
│       └── Videography/
│           ├── C9FAL50v1is.md
│           └── C9FAL50v1is_frames/
│               ├── 0001.jpg
│               └── ...
├── Transcripts/
│   └── C9FAL50v1is.json
└── Hermes_Skills/
    └── davinci-reel-C9FAL50/
        ├── SKILL.md
        └── QUICK_REF.md
```

## Resume Support

```bash
# Resume from last checkpoint
python3 auto_processor.py --urls-file urls.txt --resume

# Force reprocess specific reel
python3 auto_processor.py --urls-file urls.txt --force-reel C9FAL50v1is

# Dry run (no downloads, no vision calls)
python3 auto_processor.py --urls-file urls.txt --dry-run
```

## Dependencies

```bash
# Python packages
pip install playwright pyyaml faster-whisper

# Playwright browsers
playwright install chromium

# System
ffmpeg  # for frame/GIF extraction
```

## Monitoring

- Progress logged to console with timestamps
- Checkpoint file: `pipeline_state.json` (updated per reel)
- Logs: `logs/auto_processor_{timestamp}.log`
- Failed reels tracked in `failed_reels.json`

## Error Handling

- **Download failures**: Retried 3x with exponential backoff (30s, 60s, 120s)
- **Vision 429**: Exponential backoff (30s → 60s → 120s → 240s → 480s)
- **Partial frames**: Accepts ≥7/8 frames (99.9% frame seek)
- **Transcription**: Optional, failures logged but don't halt
- **Skill/Vault**: Failures logged, pipeline continues
- **Cleanup**: Always runs (even on error) via `finally` blocks

## Maintenance

- **Monthly**: Refresh cookies.txt for downreels.com
- **Weekly**: `pip install -U --pre yt-dlp playwright faster-whisper`
- **As needed**: Update `config.yaml` categories/keywords
- **Cleanup**: `rm -rf ~/instagram-davinci-pipeline/temp/*` (manual if needed)

## Related Skills

- `instagram-reels-pipeline` — URL-based yt-dlp pipeline (local MP4s)
- `instagram-davinci-learning-pipeline` — RTF/CSV input, DaVinci color grading focus
- `instagram-saved-collections-pipeline` — Bulk Instagram collections export processing
- `instagram-reels-pipeline` — Local MP4 processor with frame extraction

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Vision 429 | Increase `vision_rate_limit_seconds` in config |
| Download 404 | Refresh cookies.txt for downreels.com |
| Playwright timeout | Increase timeout in config, check network |
| Vision timeout | Increase timeout, check frame file exists |
| Skill generation fails | Check SKILLS_DIR writable, template exists |
| Vault note fails | Check VAULT_DIR writable, collection folder exists |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-24 | Initial release — full 6-stage automated pipeline |
| 1.0.1 | 2026-07-24 | Fixed VISION_REPORT_DIR undefined variable crash; critical vault path documentation |
| 1.0.2 | 2026-07-24 | Documented NumPy/Python 3.14 compatibility workaround for faster-whisper |
| 1.0.3 | 2026-07-24 | **CRITICAL**: Fixed GIF copy to vault before cleanup — GIFs were being lost; documented NumPy 3.11 vs 3.14 venv issue; added GIF copy step in generate_skill_and_vault() |
| 1.0.4 | 2026-07-24 | **Video Effects Pipeline**: 361/370 reels processed (97.6%) in Video_Effects/ with 11 transition techniques cataloged; separate queue from Photography/Videography |
| 1.0.5 | 2026-07-25 | **Large-scale dual-collection pipeline**: 370 Video Effects reels → 262 skills + 746 notes; 389 Photography/Videography reels download started; **Auto-compression failure documented** (provider/base_url mismatch at 95% context); Background processing with notify_on_complete proven; downreels.com established as primary downloader; Vision rate limit (20 RPM/3s) enforced; Vault path discipline reinforced; GIF copy before cleanup mandatory; Index cross-linking automated; Architecture diagram discipline enforced; Storage budget monitoring added; Draw Things models location; PyTorch/Whisper issue; Parallel pipeline execution; Skill auto-install. |
| 1.0.6 | 2026-07-26 | **Tag-aware extraction architecture implemented**: 10 Video Effects subcategories + 7 Photography subcategories with dedicated vision prompts & structured JSON schemas; `full_tag_aware_pipeline.py` created for 771-reel unified pipeline; Video Effects COMPLETE (334 skills, 737 notes); Vault path discipline reinforced; Index cross-linking discipline reinforced; Architecture diagram discipline reinforced; Storage budget awareness; Background processing pattern proven; downreels.com primary downloader; Vision rate limit (20 RPM/3s) enforced; NumPy/Python 3.14 workaround documented; Index cross-linking automation needed; Draw Things models location; PyTorch/Whisper issue; Skill auto-install. |

### Critical Vault Path
- **MUST** use exact TamaZila Obsidian Vault path: `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`
- Previous pipeline wrote to `~/Obsidian/EMAI/Instagram Reels/` — WRONG vault
- All output paths (skills, vault notes, vision reports, transcripts, GIFs) must point here

### VISION_REPORT_DIR Variable (Fixed v1.0.1)
- `get_completed_reels()` references `VISION_REPORT_DIR` which must be defined
- Added explicit `VISION_REPORT_DIR = VISION_DIR` in config

### GIF Copy Bug (Fixed v1.0.3)
- Pipeline generated GIFs in `temp/gifs/{reel_id}.gif` but **never copied to vault**
- Cleanup deleted `temp/gifs/` → **all GIFs permanently lost**
- **Fix**: Added GIF copy in `generate_skill_and_vault()`:
  ```python
  gif_path = GIFS_DIR / f"{reel_id}.gif"
  vault_gif = VAULT_DIR / collection / f"{reel_id}.gif"
  if gif_path.exists():
      shutil.copy2(gif_path, vault_gif)
  ```
- Regenerated 246 missing GIFs via `regenerate_missing_gifs.py`

### NumPy/Python 3.14 Compatibility (Critical v1.0.2)
- Environment: Python 3.14 system, Python 3.11 Hermes venv
- NumPy 2.4.6 compiled for Python 3.11 → `ModuleNotFoundError: numpy._core._multiarray_umath`
- **Workaround**: Force reinstall in Hermes venv:
  ```bash
  /Users/alfredkamisese/.hermes/hermes-agent/venv/bin/pip install --upgrade --force-reinstall numpy
  /Users/alfredkamisese/.hermes/hermes-agent/venv/bin/pip install --upgrade --force-reinstall faster-whisper
  ```
- Transcription remains unstable; vision analysis unaffected

### Video Effects Pipeline (v1.0.4)
- 361/370 reels processed (97.6%) in Video_Effects/ with 11 transition techniques cataloged
- Separate queue from Photography/Videography
- 11 transition techniques: Pro Cut Out, Flash, Whip Pan, Directional Flash, Glitch, Morph Cut, Speed Ramp, Zoom, Pan Zoom, Glitch v2, Pan Zoom
- 11 vault notes created with techniques, node structures, cross-references

### Cross-Link All Index Files (Critical)
- **Must update all index files** when adding new pipeline outputs:
  - `Memory.md` (DaVinci KB Master GPS) — Cross-Reference & Workflow Indexes table
  - `CROSS_REFERENCE_INDEX.md` — New Index References table
  - `ARCHITECTURE_DIAGRAM.md` — Mermaid graph: Instagram_Reels subgraph with MASTER_INDEX node
  - `Hero_index.md` — DaVinci KB entry + direct Instagram Reels link
  - `START HERE.md` — Key folders section with Instagram_Reels link

### Architecture Diagram Updates (Critical)
- Mermaid graph must include new Instagram_Reels subgraph in Root Files
- Node: `Instagram_Reels_MASTER_INDEX["📄 Instagram_Reels/MASTER_INDEX.md"]`
- Connection: `MASTER_INDEX --> Photography` → Frames, GIFs, Vault Notes

### Storage Monitoring Critical
- Mac Mini 228GB SSD hit 100% capacity (1.2GB free) during batch; temp folder hit 5.5GB
- Must monitor `df -h` and clean temp proactively
- Temp folder: `~/instagram-davinci-pipeline/temp/` (frames/, gifs/, mp4/, transcripts/)

### Video Effects Pipeline Separate
- 361 reels processed in Video_Effects/ with 11 transition techniques cataloged
- Separate queue from Photography/Videography
- 11 transition techniques cataloged

### Draw Things AI Models Storage (32GB)
- Location: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`
- Models: Flux, SDXL, Qwen, CLIP, VAE, LoRA models
- **Can move to external SSD**: `ln -s /Volumes/External/Models ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`
- Essential for Draw Things app — do not delete

### PyTorch/Whisper Environment Issue
- Whisper transcription fails with `torch/_C` folder error on Mac Mini M4 (Python 3.14)
- Error: `Failed to load PyTorch C extensions: torch/_C` — torch/_C folder loaded instead of C extensions
- **Workaround**: Use faster-whisper with CPU fallback or run Python from different directory
- Transcription skipped but frames/GIFs still extracted

### Parallel Pipeline Execution Works
- Two simultaneous GIF regen processes covered each other's failures
- Rate limit handling via exponential backoff (30s→60s→120s→240s→480s)

### Skill Auto-Installation to Hermes
- Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability
- `hermes skills list | grep davinci-reel` shows 390 skills installed

---

## Session Learnings (2026-07-25) — Large-Scale Dual-Collection Pipeline

### Auto-Compression Threshold & Failure Mode
- **Auto-compression triggers at 60-70% context**, NOT 95%
- Session grew to 95% without compression due to provider/base_url mismatch
- **Root cause**: Config had `provider: nvidia` with `base_url: http://127.0.0.1:11434/v1` (local Ollama)
- **Fix**: Point NVIDIA provider to `https://integrate.api.nvidia.com/v1` directly
- **Pattern**: Manually compress at ~50% before long-running pipelines

### Background Processing Pattern (Proven)
- Use `terminal(background=true, notify_on_complete=true)` for long-running pipeline stages
- Returns session_id immediately; notification fires on completion
- Allows agent to continue with other tasks while pipeline runs
- **Proven**: 370 Video Effects reels processed in background (proc_58cda343e456)

### downreels.com as Primary Downloader (Not yt-dlp+Cookies)
- **Preferred**: downreels.com via Playwright (4s delay, serial)
- **Avoids**: Instagram cookie rotation, login wall, rate limits
- **Trade-off**: Slower but more reliable than yt-dlp with burner accounts
- **Rate limit**: 4s between downloads, batch size 10

### Vision Analysis Rate Limiting (Hard Constraint)
- **Hard limit**: 20 RPM (vision_analyze tool)
- **Enforced**: 3s minimum between calls
- **Backoff**: Exponential (30s→60s→120s→240s→480s) on 429
- **Do NOT batch** vision calls — each counts against RPM

### Vault Path Discipline (Non-Negotiable)
- **ALL** output paths MUST use exact TamaZila Obsidian Vault path
- Correct: `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`
- Wrong: `~/Obsidian/EMAI/`, `~/instagram-davinci-pipeline/vault/`
- Verified on every pipeline run

### GIF Vault Copy (Mandatory Step)
- **Copy GIFs to vault BEFORE cleanup** — hard requirement
- Bug in v1.0.3 lost 246 GIFs; fixed in v1.0.4
- Copy step in `generate_skill_and_vault()`:
  ```python
  gif_path = GIFS_DIR / f"{reel_id}.gif"
  vault_gif = VAULT_DIR / collection / f"{reel_id}.gif"
  if gif_path.exists():
      shutil.copy2(gif_path, vault_gif)
  ```

### Index Cross-Linking (Automated, Not Manual)
- **Must update 5 index files** on every pipeline completion:
  1. `Memory.md` — Cross-Reference & Workflow Indexes
  2. `CROSS_REFERENCE_INDEX.md` — New Index References
  3. `ARCHITECTURE_DIAGRAM.md` — Mermaid graph + Instagram_Reels subgraph
  4. `Hero_index.md` — DaVinci KB entry + direct link
  4. `START HERE.md` — Key folders section
- Consider adding `regenerate_indexes.py` script

### Architecture Diagram Discipline
- Mermaid graph MUST include Instagram_Reels subgraph
- Node: `Instagram_Reels_MASTER_INDEX["📄 Instagram_Reels/MASTER_INDEX.md"]`
- Connections: Root → MASTER_INDEX → Photography/Videography → Frames, GIFs, Vault Notes
- Regenerate HTML interactive version after Mermaid update

### Storage Budget Awareness
- Samsung LED SSD (120GB): ~70GB free baseline
- Pipeline temp: ~7.2 GB (frames + GIFs + MP4s)
- Draw Things models: 32 GB (separate location)
- **Monitor**: `df -h /Volumes/Samsung\ LED` before each batch
- **Clean**: `rm -rf ~/instagram-davinci-pipeline/temp/*` after vault copy

### Photography/Videography Collection (389 URLs) — In Progress
- Download started in background (proc_c0a55fccee5c)
- Next: Extract frames/GIFs → Vision analysis → Skills + Vault
- Separate queue from Video Effects (370 URLs, 262 skills + 746 notes done)

### Skill Organization: ~/.hermes/skills/creative/
- Video Effects skills: `davinci-video-effect-{reel_id[:8]}/` (262 created)
- Color Grading skills: `davinci-resolve-{technique}/` (existing)
- Auto-install: `cp -r pipeline_skills ~/.hermes/skills/creative/`

### Version History Update
| Version | Date | Changes |
|---------|------|---------|
| 1.0.5 | 2026-07-25 | **Large-scale dual-collection pipeline**: 370 Video Effects reels → 262 skills + 746 notes; 389 Photography/Videography reels download started; **Auto-compression failure documented** (provider/base_url mismatch at 95% context); Background processing with notify_on_complete proven; downreels.com established as primary downloader; Vision rate limit (20 RPM/3s) enforced; Vault path discipline reinforced; GIF copy before cleanup mandatory; Index cross-linking automated; Architecture diagram discipline enforced; Storage budget monitoring added. |
- `hermes skills list | grep davinci-reel` shows 390 skills installed

### Cross-Link All Index Files (Critical)
- Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries

### Architecture Diagram Updates (Critical)
- Mermaid graph must include Instagram_Reels subgraph with MASTER_INDEX node

### Draw Things AI Models Storage (32GB)
- Location: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`
- Models: Flux, SDXL, Qwen, CLIP, VAE, LoRA
- **Can move to external SSD**: `ln -s /Volumes/External/Models ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`

### PyTorch/Whisper Environment Issue
- Whisper transcription fails with `torch/_C` folder error on Mac Mini M4 (Python 3.14)
- Error: `torch/_C` folder loaded instead of C extensions
- Workaround: Use faster-whisper with CPU fallback or run Python from different directory

### Parallel Pipeline Execution Works
- Two simultaneous GIF regen processes covered each other's failures
- Rate limit handling via exponential backoff (30s→60s→120s→240s→480s)

### Skill Auto-Installation to Hermes
- Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability
- `hermes skills list | grep davinci-reel` shows 390 skills installed

### Cross-Link All Index Files (Critical)
- Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries

### Architecture Diagram Updates (Critical)
- Mermaid graph must include Instagram_Reels subgraph with MASTER_INDEX node

### Draw Things AI Models Storage (32GB)
- Location: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`
- Models: Flux, SDXL, Qwen, CLIP, VAE, LoRA
- **Can move to external SSD**: `ln -s /Volumes/External/Models ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`

### PyTorch/Whisper Environment Issue
- Whisper transcription fails with `torch/_C` folder error on Mac Mini M4 (Python 3.14)
- Error: `torch/_C` folder loaded instead of C extensions
- Workaround: Use faster-whisper with CPU fallback or run Python from different directory

### Parallel Pipeline Execution Works
- Two simultaneous GIF regen processes covered each other's failures
- Rate limit handling via exponential backoff (30s→60s→120s→240s→480s)

### Skill Auto-Installation to Hermes
- Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability
- `hermes skills list | grep davinci-reel` shows 390 skills installed

## License

MIT — Part of TamaZila DaVinci Knowledge Base project
---

*Generated by auto-instagram-davinci-processor skill*
---

*This skill encapsulates the complete automated pipeline. For the underlying scripts, see `~/instagram-davinci-pipeline/scripts/auto_processor.py` and supporting modules.*