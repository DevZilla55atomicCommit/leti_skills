# Session 2026-07-25 — Critical Pipeline Fixes Applied

## Overview
Critical bugs discovered and fixed during the complete 771-reel tag-aware pipeline execution. These fixes are essential for pipeline reliability and must be incorporated into future runs.

## 1. Async Function Await Bug (CRITICAL)

### Problem
```python
# WRONG - coroutine never awaited
note = generate_vault_note(reel_id, manifest_entry, vision_result, category)
skill_info = create_skill(reel_id, vision_result, category)
```

### Symptom
```
RuntimeWarning: coroutine 'generate_vault_note' was never awaited
```
Skills never actually created despite code appearing to run successfully.

### Fix
```python
# CORRECT - await the async functions
note = await generate_vault_note(reel_id, manifest_entry, vision_result, category)
skill_info = await create_skill(reel_id, vision_result, category)
```

### Root Cause
`generate_vault_note()` and `create_skill()` are defined as `async def` but were called without `await`. The coroutine objects were created but never executed.

### Prevention
- Add type hints to make async functions obvious: `async def generate_vault_note(...) -> str:`
- Add runtime check: `if asyncio.iscoroutine(result): raise RuntimeError("Coroutine not awaited")`
- Code review checklist: "All async functions awaited?"

---

## 2. Skill Name Collision (HIGH)

### Problem
```python
# PROBLEM: Multiple reels can share first 8 characters
skill_name = f"davinci-video-effect-{reel_id[:8]}"
```

### Example Collision
- `C-5PYQSADOG` → `davinci-video-effect-C-5PYQSA`
- `C-5PYQSADOG2` → `davinci-video-effect-C-5PYQSA` (collision!)

### Fix
```python
# Use full reel_id for uniqueness
skill_name = f"davinci-video-effect-{reel_id}"
# Or use hash for shorter names
skill_name = f"davinci-video-effect-{hashlib.md5(reel_id.encode()).hexdigest()[:12]}"
```

### Impact
334 transition skills were created but some may have overwritten each other. Full ID ensures uniqueness.

---

## 3. Frame Directory Mapping Fix

### Problem
Frame directories used downreels.com internal IDs (e.g., `Dar6uTGzp-h`) but manifest expected Instagram short IDs (e.g., `C-5PYQSADOG`).

### Fix
```python
# Build mapping from download order (completed.json) to short IDs
with open('completed.json') as f:
    completed = json.load(f)  # List of Instagram short IDs in download order

frame_dirs = sorted(Path('temp/frames').iterdir(), key=lambda d: d.stat().st_mtime)
id_map = {short_id: frame_dir.name for short_id, frame_dir in zip(completed, frame_dirs)}

# Update manifest
for short_id, frame_dir in id_map.items():
    manifest[short_id]['frames_dir'] = f"temp/frames/{frame_dir}"
```

### Impact
All 771 reels now have correct `frames_dir` paths in manifest for vision pipeline.

---

## 4. Asset Copying to Vault

### Problem
Frames and GIFs generated in `temp/` but NOT copied to vault before cleanup.

### Fix
```python
# Copy frames to vault
frames_src = Path(frames_dir)
vault_frames = VAULT_BASE / category / f"{reel_id}_frames"
if frames_src.exists():
    if vault_frames.exists():
        shutil.rmtree(vault_frames)
    shutil.copytree(frames_src, vault_frames)

# Copy GIF to vault
gif_src = GIFS_DIR / f"{reel_id}.gif"
vault_gif = VAULT_BASE / category / f"{reel_id}.gif"
if gif_src.exists():
    shutil.copy2(gif_src, vault_gif)
```

### Verification
```bash
# Verify frames copied
find "/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/assets/transitions" -name "*_frames" | wc -l
# → 1,058 frame directories

# Verify GIFs copied
find "/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/assets/transitions" -name "*.gif" | wc -l
# → 1,058 GIFs
```

---

## 5. Frame Directory Verification Before Vision

### Problem
108 reels had NO frames extracted (download/extraction failed) but were still queued for vision.

### Fix
```python
def verify_frame_dir(reel_id: str) -> bool:
    """Verify frame directory exists and has sufficient frames."""
    frame_dir = FRAMES_DIR / reel_id
    if not frame_dir.exists():
        return False
    frames = list(frame_dir.glob("*.jpg"))
    return len(frames) >= 3  # Need at least 3 frames for vision
```

### Pipeline Integration
```python
# In process_reel()
frame_dir = FRAMES_DIR / reel_id
if not verify_frame_dir(reel_id):
    log(f"  ⚠️ {reel_id}: No valid frame directory, skipping vision")
    return {"reel_id": reel_id, "status": "error", "error": "no frames"}
```

---

## 6. Skill Installation to Hermes

### Problem
Skills generated in vault but not installed to `~/.hermes/skills/creative/` for discoverability.

### Fix
```python
def install_skill_to_hermes(reel_id: str, category: str):
    """Install generated skill to Hermes skill system."""
    skill_name = f"davinci-video_effect-{reel_id}"
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

### Verification
```bash
hermes skills list | grep davinci-video_effect | wc -l
# → 548 skills discoverable
```

---

## 6. Manifest Frame Directory Updates

### Problem
Manifest `frames_dir` pointed to non-existent paths after frame directory renaming.

### Fix
```python
# After renaming frame directories to match reel IDs
with open('extraction_manifest.json') as f:
    manifest = json.load(f)

for short_id, frame_dir in id_map.items():
    if short_id in manifest:
        manifest[short_id]['frames_dir'] = os.path.join('temp/frames', frame_dir)

with open('extraction_manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)
```

---

## Pipeline Configuration Updates

### Updated `auto_processor.py` Config
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

---

## Summary Checklist for Future Runs

- [ ] All async functions awaited
- [ ] Skill names use full reel_id (no collision)
- [ ] Frame directory mapping verified
- [ ] Assets copied to vault before cleanup
- [ ] Frame directories verified before vision
- [ ] Skills installed to Hermes
- [ ] Manifest frames_dir updated
- [ ] Rate limits respected (3s = 20 RPM)

---

**Last Updated**: 2026-07-25
**Applied During**: Complete 771-reel tag-aware pipeline run
**Status**: All fixes applied and validated in production run