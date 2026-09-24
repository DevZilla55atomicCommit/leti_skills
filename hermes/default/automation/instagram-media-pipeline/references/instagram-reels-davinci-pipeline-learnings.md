# Instagram Reels → DaVinci Resolve Knowledge Pipeline — Session Learnings

**Date:** 2026-07-24
**Scope:** End-to-end pipeline for 389 Instagram Reels (Photography/Videography collection)
**Source:** downreels.com (third-party, no API/cookies)

---

## Pipeline Architecture (6 Stages)

| Stage | Tool | Key Parameters | Rate Limit |
|-------|------|----------------|------------|
| 1. Download | Playwright → downreels.com | Batch 10, 4s delay | ~10 reels/min |
| 2. Extract | ffmpeg + faster-whisper | 1fps frames, 5s GIF, base model | CPU-bound |
| 3. Vision | Built-in vision model | 3 frames (start/mid/end), 3s delay | 20 RPM |
| 4. Skills | Template generation | davinci-reel-{id[:8]} | — |
| 5. Vault | Obsidian markdown | TamaZila vault structure | — |
| 6. Cleanup | shutil.rmtree | frames/mp4/gifs temp | — |

---

## Critical Technical Findings

### 1. downreels.com as Downloader
- **Works without Instagram auth** — avoids account ban risk
- **Rate limit:** ~4s between downloads, batch 10 works
- **Playwright headless** required; session persistence helps
- **Fallback:** MP4s land in `~/Downloads/reels_downreels/`

### 2. NumPy/Python 3.14 + faster-whisper Incompatibility
```
Error: No module named 'numpy._core._multiarray_umath'
Cause: numpy 2.4.6 compiled for Python 3.11, running on 3.14
Fix: Use Hermes venv (Python 3.11) for whisper; system Python 3.14 for pipeline
```
- **Transcription success rate:** ~1/389 (known limitation)
- **Workaround:** Skip transcription or use separate Python 3.11 env

### 3. Hermes Skill Installation
- **Skills must live in** `~/.hermes/skills/<category>/` to be discoverable
- **Vault copies are not enough** — copy to `~/.hermes/skills/creative/`
- **Command:** `cp -r vault_skill ~/.hermes/skills/creative/`
- **Verification:** `hermes skills list | grep davinci-reel`

### 4. Vision Analysis Rate Limiting
- **20 RPM hard limit** on vision API
- **3s delay between calls** required
- **3 frames per reel** = 9s minimum per reel
- **Batch parallelization not possible** — serial with delay

### 4. GIF Generation
- **Full-video GIF** better than 5s preview
- **Settings:** 10fps, 480px width, palettegen/paletteuse
- **Size:** ~2-5MB per reel
- **Vault placement:** alongside `_frames` folder

### 5. Temp Cleanup (Critical for Storage)
```python
# After vault copy, remove:
TEMP_DIR / "mp4" / f"{reel_id}.mp4"
TEMP_DIR / "frames" / reel_id/  # entire dir
TEMP_DIR / "gifs" / f"{reel_id}.gif"
```
- **389 reels × ~1.5GB temp** = significant if not cleaned
- **Cleanup must run per-reel**, not just at end

---

## Vault Structure (TamaZila)

```
/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
├── Vision_Reports/           # 389 JSON files
├── Instagram_Reels/
│   └── Photography/Videography/
│       ├── {reel_id}.md      # 389 vault notes
│       ├── {reel_id}.gif     # 389 full-video GIFs
│       └── {reel_id}_frames/ # 389 frame folders
├── Transcripts/              # 1 JSON (whisper mostly failed)
└── Hermes_Skills/            # REMOVED after install to ~/.hermes
```

---

## Skill Naming & Structure

```
davinci-reel-{reel_id[:8]}/
├── SKILL.md      # Full skill with node recipes, exercises, metadata
├── QUICK_REF.md  # 3-node grade, settings, keywords
```

**Frontmatter includes:** reel_id, source_url, collection, analyzed_at, educational_value, tags, references

---

## Pitfalls & Fixes

| Pitfall | Fix |
|---------|-----|
| Vision calls without delay | Async sleep(3.0) between every frame |
| Temp dirs fill disk | Cleanup per-reel in `finally` block |
| Skills not discoverable | Copy to `~/.hermes/skills/creative/` after generation |
| Whisper fails silently | Catch exception, log, continue without transcript |
| downreels.com CAPTCHA | Session persistence + human-like delays |
| Duplicate reel processing | Check `VISION_REPORTS_DIR` before download |

---

## Reusable Code Patterns

### Vision Analysis Loop
```python
async def analyze_reel_vision(reel_id, frame_paths):
    frames = [frame_paths[0], frame_paths[len//2], frame_paths[-1]]
    for fp in frames:
        result = await vision_analyze(fp, prompt)
        await asyncio.sleep(VISION_RATE_LIMIT)  # 3.0s
```

### Skill Install Helper
```python
def install_skill_to_hermes(reel_id):
    skill_name = f"davinci-reel-{reel_id[:8]}"
    src = VAULT_SKILLS_DIR / skill_name
    dst = Path("~/.hermes/skills/creative").expanduser() / skill_name
    if src.exists() and not dst.exists():
        shutil.copytree(src, dst)
```

---

## Next Batch Improvements

1. **Parallel download** (separate browser contexts) — downreels.com allows
2. **Vision batching** — if API supports multi-image, reduce calls
3. **Whisper in Python 3.11 venv** — subprocess call for transcription
4. **Progress persistence** — JSON state file for resume after crash
5. **Duplicate detection** — content hash before download