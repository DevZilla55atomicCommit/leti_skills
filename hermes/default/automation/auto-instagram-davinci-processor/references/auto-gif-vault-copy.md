# GIF Vault Copy Fix — auto-instagram-davinci-processor v1.0.3

## Problem
The pipeline generates GIFs in `temp/gifs/{reel_id}.gif` but was **not copying them to the vault** before the cleanup stage deleted `temp/gifs/`. This resulted in permanent loss of all GIFs.

**Impact**: 389 reels processed, 0 GIFs in vault.

## Root Cause
In `generate_skill_and_vault()`, the code only copied frames:
```python
# Frames copied to vault
vault_media = VAULT_DIR / collection / f"{reel_id}_frames"
for f in frames_dir.glob("*.jpg"):
    shutil.copy2(f, vault_media / f.name)

# GIF NOT copied — left in temp/gifs/ then deleted by cleanup_reel()
```

## Fix (v1.0.3)
Added GIF copy step in `generate_skill_and_vault()`:
```python
# Copy GIF to vault alongside frames
gif_path = GIFS_DIR / f"{reel_id}.gif"
vault_gif = VAULT_DIR / collection / f"{reel_id}.gif"
if gif_path.exists():
    shutil.copy2(gif_path, vault_gif)
```

## Verification
After fix, GIFs appear in vault at:
```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/Photography/Videography/{reel_id}.gif
```

## Regeneration for Already-Processed Reels
For the 389 reels already processed (246 missing GIFs):
1. Re-download MP4s from downreels.com
2. Regenerate GIFs with `regenerate_missing_gifs.py`
3. Copy to vault
4. Cleanup temp

See `scripts/regenerate_missing_gifs.py` for the regeneration pipeline.