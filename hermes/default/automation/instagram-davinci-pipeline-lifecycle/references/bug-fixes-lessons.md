# Bug Fixes & Lessons Learned (2025-07-24 Session)

## Critical Bugs Fixed

### 1. GIFs Not Copied to Vault (MAJOR)
**Symptom**: 246/389 reels missing GIFs in vault after pipeline complete
**Root Cause**: `generate_skill_and_vault()` copied frames but NOT GIFs
```python
# BUG: Only frames copied
frames_dir = Path("~/instagram-davinci-pipeline/temp/frames").expanduser() / reel_id
vault_media = VAULT_DIR / collection / f"{reel_id}_frames"
# No GIF copy logic!
```

**Fix**: Added GIF copy in `generate_skill_and_vault()`:
```python
vault_gif = VAULT_DIR / f"{reel_id}.gif"
shutil.copy2(gif_path, vault_gif)
```

**Impact**: 246 reels required full re-download + regeneration (2-3 hours)

### 2. Auto-Compression Silent Failure
**Symptom**: Session grew to 1,014 messages without compression trigger
**Root Cause**: Config pointed to local Ollama for NVIDIA model
```yaml
# WRONG
base_url: http://127.0.0.1:11434/v1  # local Ollama
model: nvidia/nemotron-mini-4b-instruct  # not on local!
```

**Fix**: Use NVIDIA API directly
```yaml
base_url: https://integrate.api.nvidia.com/v1
```

**Lesson**: Always verify compression model exists at configured endpoint

### 3. Numpy/Python 3.14 + Whisper Incompatibility
**Symptom**: `No module named 'numpy._core._multiarray_umath'`
**Root Cause**: numpy 2.4.6 built for Python 3.11, running on 3.14
**Impact**: Only 1/389 transcripts generated
**Workaround**: Skip transcription, use vision analysis instead

### 4. Temp Cleanup Verification
**Issue**: Cleanup runs but no verification of vault copy
**Fix**: Audit pattern - always verify `ls vault/*.gif` after batch
```bash
# Quick check
ls vault/*.gif | wc -l  # Should match batch size
ls temp/gifs/ | wc -l   # Should be 0 after cleanup
```

### 5. Hermes Skills Not Auto-Discoverable
**Issue**: Skills generated in vault but not in `~/.hermes/skills/creative/`
**Fix**: `install_skill_to_hermes()` copies to `~/.hermes/skills/creative/`
**Result**: 390 skills now discoverable via `hermes skills list`

## Pipeline Improvements Made

| Improvement | File | Impact |
|-------------|------|--------|
| GIF copy to vault | `auto_processor.py` | Prevents data loss |
| Hermes skill install | `auto_processor.py` | Skills discoverable |
| GIF regeneration script | `regenerate_missing_gifs.py` | Recovered 246 GIFs |
| Full GIF regen script | `regenerate_gifs.py` | From-scratch capability |
| Lifecycle docs | `instagram-davinci-pipeline-lifecycle` skill | Future-proofing |

## Storage Decisions Validated

| Decision | Validation |
|----------|------------|
| Keep JPG frames | ✅ Essential for DaVinci color work |
| Keep full-video GIFs | ✅ Motion reference, some up to 140MB |
| Delete MP4s after extract | ✅ Re-downloadable, saves 10GB+ |
| Install skills to Hermes | ✅ Now discoverable |
| Store in TamaZila vault | ✅ Organized, searchable |

## What to Monitor Next Run

1. **Vision rate limit** - log 429s, adjust sleep if needed
2. **Temp directory** - should stay < 100MB during run
3. **GIF count** - `ls vault/*.gif | wc -l` after each batch
4. **Skill install** - verify `hermes skills list | grep davinci-reel`
5. **Transcription** - skip if numpy issue persists

## Commands for Quick Verification

```bash
# Vault health check
ls "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/Photography/Videography/" | grep -c "\.gif$"  # Should be 389

# Temp cleanup check
du -sh ~/instagram-davinci-pipeline/temp/  # Should be ~0B

# Skills check
hermes skills list | grep -c davinci-reel  # Should be 390

# Vision reports
ls "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports/" | wc -l  # Should be 389
```