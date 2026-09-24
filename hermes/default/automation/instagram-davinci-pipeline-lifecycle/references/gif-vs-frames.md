# GIF vs Frame Storage Decision Matrix

## Purpose
Document the rationale for keeping both JPG frames and GIFs in the vault, and provide guidelines for future storage decisions.

## Comparison

| Factor | JPG Frames (1fps) | GIF (10fps full video) |
|--------|-------------------|------------------------|
| **Primary Use** | Precision reference, DaVinci import | Motion reference, quick preview |
| **Color Accuracy** | Full quality, no compression artifacts | Lossy, palette limited |
| **Zoom/Inspect** | ✅ Full detail | ❌ Lossy |
| **DaVinci Resolve** | ✅ Gallery stills, color matching | ❌ Not usable |
| **Frame-by-frame** | ✅ Exact timestamps | ❌ Hard to isolate |
| **Motion reference** | ❌ Static only | ✅ Smooth playback |
| **File size/reel** | ~5-15 MB | ~50-140 MB |
| **Total (389 reels)** | ~2-3 GB | ~3-4 GB |

## Recommendation: KEEP BOTH

### Why keep JPGs:
1. **DaVinci workflow**: Load as gallery stills for color matching
2. **Color accuracy**: Critical for skin tones, exposure reference
3. **Zoom capability**: Inspect detail (focus, noise, texture)
4. **Frame accuracy**: Exact timestamp mapping

### Why keep GIFs:
1. **Motion context**: See camera movement, transitions
2. **Quick preview**: "What does this look like in motion?"
3. **Technique demo**: Shutter speed, frame rate effects visible
4. **Convenient**: Embedded in vault notes, no external player

## Storage Optimization Options (if needed)

| Option | Savings | Trade-off |
|--------|---------|-----------|
| Reduce GIF fps to 5 | ~50% | Less smooth motion |
| Reduce GIF width to 320px | ~40% | Less detail |
| Delete GIFs > 30s | Variable | Lose long-form reference |
| Keep only key GIFs (priority reels) | ~60% | Manual curation needed |
| Compress JPGs to 80% quality | ~30% | Minor quality loss |

## Current Status (2025-07-24)

- **389 frame folders** (JPG) - KEEP
- **389 GIFs** in vault - KEEP
- **5.5 GB total** - ACCEPTABLE on 120GB SSD

## Future Pipeline Runs

```python
# In auto_processor.py, both are generated:
extract_reel() → creates frames/ + gif
generate_skill_and_vault() → copies frames to vault
regenerate_gifs() → creates GIFs alongside existing frames
```

**Never delete frames** - they are the high-fidelity reference.
**GIFs are optional but recommended** - regenerate if missing.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-07-24 | Keep both | Frames for DaVinci/color, GIFs for motion reference |
| 2025-07-24 | Regenerate missing GIFs | 246/389 missing, spent 2-3 hours re-downloading |
| 2025-07-24 | Full-frame GIFs (10fps) | Better motion reference than 5s clips |