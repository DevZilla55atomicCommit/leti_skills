---
name: pipeline-automation-lessons
description: |
  Lessons learned from building and running the Instagram Reels → DaVinci Resolve pipeline.
  Covers Python environment management, path configuration for vault integration,
  cleanup verification, batch processing with rate limiting, and error handling
  for numpy/Python version mismatches.
version: 1.0.0
category: software-development
tags:
  - pipeline-automation
  - python-environment
  - vault-integration
  - cleanup-verification
  - batch-processing
  - rate-limiting
  - error-handling
  - numpy-debugging
references:
  - "instagram_reels_pipeline": "Instagram Reels → DaVinci Resolve knowledge pipeline"
  - "systematic-debugging": "4-phase root cause debugging methodology"
  - "environment-setup": "Protocols for auditing, installing, and managing external dependencies"
---

# Pipeline Automation Lessons Learned

## Python Environment Management

### Problem
numpy/Python version mismatch causing `No module named 'numpy._core._multiarray_umath'` errors.

### Root Cause
Multiple Python versions (3.9, 3.11, 3.12, 3.14) with incompatible numpy builds. The hermes venv uses Python 3.11, but system Python 3.14 was being invoked.

### Solution
```bash
# Always use the correct venv Python
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -m pip install --upgrade --force-reinstall numpy
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -m pip install --upgrade --force-reinstall faster-whisper

# Verify correct environment
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -c "import numpy; print(numpy.__version__); print(numpy.__file__)"
```

### Prevention
- Always activate the correct venv before running pipeline scripts
- Never use system Python for venv-dependent packages
- Pin numpy version in requirements if needed

## Path Configuration for Vault Integration

### Problem
Pipeline outputs written to wrong locations (user's default Obsidian folder instead of TamaZila Vault).

### Solution
Centralize path configuration in one place:

```python
# Single source of truth for all vault paths
VAULT_BASE = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base")
VISION_DIR = VAULT_BASE / "Vision_Reports"
SKILLS_DIR = VAULT_BASE / "Hermes_Skills"
VAULT_DIR = VAULT_BASE / "Instagram_Reels"
TRANSCRIPTS_DIR = VAULT_BASE / "Transcripts"
```

### Verification
Check paths before processing:
```bash
ls "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports/" | wc -l
```

## Cleanup Verification

### Problem
Temp directories not cleaned up, consuming 600MB+ disk space. Vault assets are NOT duplicates of pipeline temp - verify before deleting.

### Solution
Verify cleanup after each reel:

```python
def cleanup_reel(reel_id: str):
    for dir_path in [TEMP_DIR / "mp4", TEMP_DIR / "frames", TEMP_DIR / "gifs"]:
        for match in dir_path.glob(f"{reel_id}.*"):
            if match.is_file():
                match.unlink()
            elif match.is_dir():
                shutil.rmtree(match)
    log(f"Cleaned temp files for {reel_id}")

# Verify cleanup
import subprocess
result = subprocess.run(["du", "-sh", "~/instagram-davinci-pipeline/temp/"], capture_output=True, text=True)
print(f"Temp size after cleanup: {result.stdout.strip()}")
```

### Verification
```bash
du -sh ~/instagram-davinci-pipeline/temp/
# Should show small size after each batch
```

### Safe Delete Checklist
Before deleting any folder:
1. **Check what's actually in it** - `ls -la /path/to/folder`
2. **Verify vault has copies** - `find /vault/path -name "*.gif" | wc -l` vs `ls /temp/gifs/ | wc -l`
3. **Check manifest mapping** - Ensure temp frame dirs map to vault frames
4. **Test with one item first** - Delete one, verify vault still works

## Batch Processing with Rate Limiting

### Pattern
Process in batches with proper rate limiting for external APIs:

```python
async def process_batch(urls: List[tuple], batch_num: int):
    # Download batch
    downloads = download_batch(batch, batch_num)
    
    # Process each reel with rate limiting
    for item in downloads:
        success = await process_reel(reel_id, item["url"], item["collection"], mp4_path)
        await asyncio.sleep(1)  # Delay between reels
    
    # Vision analysis with rate limiting
    for reel_id in reel_ids:
        await analyze_reel_vision(reel_id, extraction)
        await asyncio.sleep(VISION_RATE_LIMIT)  # 3s for 20 RPM
    
    log(f"Batch {batch_num} complete. Waiting before next...")
    await asyncio.sleep(5)
```

### Vision Analysis Rate Limiting
- **20 RPM limit** = 3 seconds between calls
- Use `asyncio.sleep(3)` between vision calls
- Process frames in batches of 3 (start, middle, end)

### Manifest-Driven Frame Resolution
Frame directories may use downreels.com internal IDs, not Instagram short IDs. Always use manifest's `frames_dir`:

```python
# Get frame directory from manifest
frames_dir = manifest_entry.get('frames_dir', '')
if frames_dir and os.path.exists(frames_dir):
    frame_dir = Path(frames_dir)
else:
    # Fallback to short ID
    frame_dir = FRAMES_DIR / reel_id
```

### External ID Mapping
Third-party downloaders (downreels.com) use different IDs. Maintain a mapping:

```python
# Load completed downloads in order
with open('/tmp/reels_pipeline/completed.json') as f:
    completed = json.load(f)  # Instagram short IDs in download order

# Get frame directories sorted by creation time (download order)
frame_dirs = sorted(os.listdir(FRAMES_DIR), key=lambda d: os.path.getmtime(os.path.join(FRAMES_DIR, d)))

# Map: Instagram short ID -> frame directory
id_map = {short_id: frame_dir for short_id, frame_dir in zip(completed, frame_dirs)}
```

## Quick Reference: Pipeline Debugging Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| `numpy._core._multiarray_umath` import error | Check Python version matches numpy build | Use correct venv Python |
| `faster-whisper` import fails | Check numpy + Python version match | Reinstall in correct venv |
| Output to wrong directory | Check VAULT_DIR paths | Centralize path config |
| Temp disk full | Check temp dir sizes | Verify cleanup runs |
| Vision API rate limited | Check rate limit compliance | Add 3s delay between calls |
| Skills not loading | Check SKILLS_DIR path | Verify skill installation |
| Vault notes missing | Check VAULT_DIR path | Verify path config |

---

## Integration with Hermes

### Skill Installation
Generated skills need to be installed/registered with Hermes:
```bash
# After generating skill files
hermes skill install /path/to/skill
# or register via Hermes API
```

### Skill Structure
Generated skills follow the standard format:
```
.davinci-reel-{id}/
├── SKILL.md          # Full skill documentation
├── QUICK_REF.md      # Quick reference card
└── references/       # Session-specific detail files
```

---

## Quick Reference: Pipeline Debugging Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| `numpy._core._multiarray_umath` import error | Check Python version matches numpy build | Use correct venv Python |
| `faster-whisper` import fails | Check numpy + Python version match | Reinstall in correct venv |
| Output to wrong directory | Check VAULT_DIR paths | Centralize path config |
| Temp disk full | Check temp dir sizes | Verify cleanup runs |
| Vision API rate limited | Check rate limit compliance | Add 3s delay between calls |
| Skills not loading | Check SKILLS_DIR path | Verify skill installation |
| Vault notes missing | Check VAULT_DIR path | Verify path config |

---

### Lessons Summary

1. **Environment consistency is paramount** - Multiple Python versions are the #1 source of pipeline failures
2. **Centralize all paths** - Single source of truth for vault paths prevents drift
3. **Verify cleanup every batch** - Disk space issues compound silently
4. **Rate limit everything** - External APIs will throttle without delays
5. **Verify before trusting** - Always check paths, versions, and cleanup results
6. **Document failures** - Every crash teaches a lesson for the checklist
7. **Map external IDs to internal IDs** - Third-party downloaders (downreels.com) use different ID schemes; create and maintain a mapping file
6. **Vault assets ≠ pipeline outputs** - Pre-existing vault content may look like duplicates but isn't; verify with `find` before deleting
7. **Vision analysis needs async + rate limiting** - 3s delays for 20 RPM; use `asyncio.sleep()` between calls
8. **Manifest-driven frame resolution** - Use manifest's `frames_dir` path when frame directories don't match Instagram short IDs