# Auto-Cleanup Workflow for Instagram Pipeline

> **Purpose:** Automatic deletion of temporary/raw media files after visual asset extraction to preserve SSD storage space.

---

## 🎯 What Gets Cleaned Up

| File Type | When Created | When Deleted | Retained Instead |
|-----------|--------------|--------------|------------------|
| **Source MP4** | `yt-dlp` download (Reels) | After all asset extraction | `demo.gif`, `technique_demo.gif` |
| **Temp Frame JPGs** | `ffmpeg` frame extraction | After comparison images built | `frame_before.png`, `frame_during.png`, `frame_after.png`, `before_after_comparison.png` |
| **Carousel Slide JPGs** | Browser download (Posts) | After carousel GIF + comparison grid built | `carousel_combined.gif`, `technique_comparison_grid.png` |
| **Intermediate GIFs** | Multiple `ffmpeg` passes | After final optimized GIF created | Final optimized `demo.gif`, `technique_demo.gif` |

---

## 🔄 Cleanup Trigger Points

### For Reels (`/reel/`)
```python
# After successful asset generation:
1. yt-dlp downloads reel.mp4
2. ffmpeg extracts frames → frame_001.png, frame_002.png...
3. ffmpeg creates demo.gif, technique_demo.gif
4. ffmpeg creates frame_before.png, frame_during.png, frame_after.png
5. ffmpeg creates before_after_comparison.png
6. ✅ CLEANUP: delete reel.mp4 + all frame_*.png
7. ✅ RETAIN: demo.gif, technique_demo.gif, frame_before.png, frame_during.png, frame_after.png, before_after_comparison.png
```

### For Carousel Posts (`/p/`)
```python
# After successful asset generation:
1. Browser downloads slide_01.jpg, slide_02.jpg... slide_N.jpg
2. ffmpeg creates carousel_combined.gif from slides
3. Vision analysis identifies per-slide techniques
4. ffmpeg creates technique_comparison_grid.png
5. ✅ CLEANUP: delete all slide_*.jpg
6. ✅ RETAIN: carousel_combined.gif, technique_comparison_grid.png + per-technique assets
```

---

## 📦 Storage Impact

| Content Type | Raw Download | Final Assets | Savings |
|--------------|--------------|--------------|---------|
| **Reel (15-60s)** | 5-50 MB MP4 | 200-800 KB GIFs + 50-200 KB PNGs | **95-99%** |
| **Carousel (6-10 slides)** | 2-10 MB JPGs | 100-300 KB GIF + 50-150 KB PNG | **90-95%** |

**Typical batch (10 Reels):** 100-500 MB raw → 2-5 MB final → **~98% reduction**

---

## ⚙️ Implementation in `run_pipeline.py`

```python
def cleanup_temp_files(asset_dir: Path, content_type: str, post_code: str):
    """Delete temp files after asset extraction."""
    if content_type == "reel":
        # Delete source MP4
        for mp4 in asset_dir.glob("*.mp4"):
            mp4.unlink(missing_ok=True)
        # Delete raw extracted frames (keep final named frames)
        for frame in asset_dir.glob("frame_*.png"):
            if not any(kw in frame.name for kw in ["before", "during", "after", "comparison"]):
                frame.unlink(missing_ok=True)
                
    elif content_type == "carousel":
        # Delete downloaded slide images
        for slide in asset_dir.glob("slide_*.jpg"):
            slide.unlink(missing_ok=True)
        for slide in asset_dir.glob("slide_*.png"):
            slide.unlink(missing_ok=True)

    # Delete intermediate GIFs (keep final optimized)
    for gif in asset_dir.glob("*_temp.gif"):
        gif.unlink(missing_ok=True)
    for gif in asset_dir.glob("*_intermediate.gif"):
        gif.unlink(missing_ok=True)
```

---

## 🛡️ Safety Guards

| Guard | Implementation |
|-------|----------------|
| **Only cleanup on success** | Cleanup runs *after* all asset generation completes without error |
| **Verify retained files exist** | Check `demo.gif`, `frame_before.png`, etc. exist before deleting source |
| **Dry-run mode** | `--dry-run` skips cleanup (for debugging) |
| **Log every deletion** | Log: `CLEANUP: deleted /path/to/temp_file.mp4` |
| **Never delete vault notes/skills** | Cleanup only touches `assets/` directories |

---

## 🔍 Verification Checklist

After pipeline processes a URL:

- [ ] Source MP4 deleted (Reels)
- [ ] Raw frame_*.png deleted (Reels)
- [ ] Slide_*.jpg/.png deleted (Carousels)
- [ ] Intermediate/temp GIFs deleted
- [ ] Final assets present:
  - [ ] `demo.gif`
  - [ ] `technique_demo.gif`
  - [ ] `frame_before.png`
  - [ ] `frame_during.png`
  - [ ] `frame_after.png`
  - [ ] `before_after_comparison.png`
  - [ ] `carousel_combined.gif` (if carousel)
  - [ ] `technique_comparison_grid.png` (if carousel)

---

## 📝 Log Example

```
[INFO] Processing https://www.instagram.com/reel/DaxUaKYuhb0/
[INFO] Downloaded reel.mp4 (23.4 MB)
[INFO] Extracted 180 frames → frame_001.png ... frame_180.png
[INFO] Created demo.gif (312 KB)
[INFO] Created technique_demo.gif (187 KB)
[INFO] Created frame_before.png (89 KB)
[INFO] Created frame_during.png (94 KB)
[INFO] Created frame_after.png (91 KB)
[INFO] Created before_after_comparison.png (178 KB)
[CLEANUP] Deleted reel.mp4 (23.4 MB)
[CLEANUP] Deleted 174 temp frame_*.png files (42.1 MB)
[SUCCESS] Retained 862 KB final assets (98.2% reduction)
```

---

*Auto-cleanup is mandatory — not optional. Raw media files are ephemeral; only compressed visual assets persist.*