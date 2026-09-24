# Visual Asset Pipeline for Video Effects

> **Key Differentiator**: For each effect, capture 5 visual assets that make the technique immediately understandable without reading text.

---

## 📸 Asset Requirements per Effect

| Asset | Purpose | Specs | Tool |
|-------|---------|-------|------|
| **Demo GIF** | Full reel demonstration | 10fps, 720px wide, full duration | `ffmpeg -vf "fps=10,scale=720:-1"` |
| **Transition Loop** | 3-second effect loop | 8fps, 480px wide, palette=64 | `ffmpeg -filter_complex "fps=8,scale=480:-1,palettegen=64"` |
| **Frame Before** | Clean frame before effect starts | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,0)'"` |
| **Frame During** | Peak effect moment | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,N)'"` |
| **Frame After** | Clean frame after effect ends | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,M)'"` |
| **Comparison** | Side-by-side before/after | 2x width PNG | `ffmpeg -i before.png -i after.png -filter_complex "hstack=inputs=2"` |

---

## 🎬 FFmpeg Recipes (Copy-Paste Ready)

### Full Frame Extraction (10fps, 720p)
```bash
ffmpeg -i reel.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png
```

### Optimized Transition Loop GIF (3s, 8fps, 480px)
```bash
ffmpeg -i reel.mp4 -filter_complex \
"[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \
-loop 0 transition_demo.gif
```

### Key Frames (adjust frame numbers per effect)
```bash
# Frame before effect (usually frame 0)
ffmpeg -i reel.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png

# Frame during effect (adjust N to peak moment)
ffmpeg -i reel.mp4 -vf "select='eq(n,30)'" -vframes 1 frame_during.png

# Frame after effect (adjust M to end)
ffmpeg -i reel.mp4 -vf "select='eq(n,60)'" -vframes 1 frame_after.png
```

### Before/After Comparison
```bash
ffmpeg -i frame_before.png -i frame_after.png \
-filter_complex "hstack=inputs=2" before_after_comparison.png
```

### Batch Asset Generation (Single Command)
```bash
cd /path/to/effect/assets && \
ffmpeg -i reel.mp4 \
-vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png && \
ffmpeg -i reel.mp4 -filter_complex \
"[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \
-loop 0 transition_demo.gif && \
ffmpeg -i reel.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png && \
ffmpeg -i reel.mp4 -vf "select='eq(n,30)'" -vframes 1 frame_during.png && \
ffmpeg -i reel.mp4 -vf "select='eq(n,60)'" -vframes 1 frame_after.png && \
ffmpeg -i frame_before.png -i frame_after.png \
-filter_complex "hstack=inputs=2" before_after_comparison.png
```

---

## 📁 Storage Structure

```
Video_Effects/assets/{category}/{effect-slug}/
├── demo.gif                    # Full reel demo (10fps, 720w)
├── transition_demo.gif         # 3s loop (8fps, 480w)
├── frame_before.png            # Before effect
├── frame_during.png            # Peak effect
├── frame_after.png             # After effect
├── before_after_comparison.png # Side-by-side
└── reel.mp4                    # Source video (archival)
```

**Category folders**: `transitions/`, `compositing/`, `motion-graphics/`, `vfx/`, `text-effects/`, `stylization/`, `time-effects/`

---

## 🔄 Batch Processing Script (Python)

```python
#!/usr/bin/env python3
"""Generate all visual assets for a single effect."""
import subprocess
from pathlib import Path

def generate_assets(effect_dir: Path, reel_path: Path, peak_frame: int = 30, end_frame: int = 60):
    """Generate all 6 visual assets for an effect."""
    cmd = f"""
    cd {effect_dir} && \\
    ffmpeg -i {reel_path} -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png && \\
    ffmpeg -i {reel_path} -filter_complex \
    "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \\
    -loop 0 transition_demo.gif && \\
    ffmpeg -i {reel_path} -vf "select='eq(n,0)'" -vframes 1 frame_before.png && \\
    ffmpeg -i {reel_path} -vf "select='eq(n,{peak_frame})'" -vframes 1 frame_during.png && \\
    ffmpeg -i {reel_path} -vf "select='eq(n,{end_frame})'" -vframes 1 frame_after.png && \\
    ffmpeg -i frame_before.png -i frame_after.png \\
    -filter_complex "hstack=inputs=2" before_after_comparison.png
    """
    subprocess.run(cmd, shell=True, check=True)
```

---

## ⚡ Key Learnings from Session (350+ Effects Processed)

1. **yt-dlp + Chrome cookies** is the only reliable Instagram download method
2. **Frame numbers matter**: Peak effect rarely at frame 30/60 — inspect visually first
3. **GIF optimization**: `palettegen=max_colors=64` + `dither=none` = small, clean GIFs
4. **Comparison images**: `hstack` creates instant before/after understanding
5. **Batch 10 URLs** with 2s delays = sustainable rate limiting
5. **Post vs Reel**: Carousel posts download as multiple clips; filter by `type: reel`
6. **Auto-cleanup mp4s**: Delete source mp4 after GIF/frame extraction to save SSD space
6. **Auto-classification needs caption/hashtags**: Script currently shows "unknown" because Instagram page isn't scraped for caption/hashtags/creator

---

## 🔧 Script Fixes Applied This Session

| Issue | Fix |
|-------|-----|
| Missing `re` import | Added `import re` at top of script |
| Assets dict returning list for frames | Removed `assets["frames"] = frames`; use individual frame keys |
| Assets dict values being lists not Paths | Changed `assets[name] = out_path` (Path object) |
| `src.exists()` on list instead of Path | Fixed by not storing lists in assets dict |
| MP4 files consuming SSD space | Added auto-cleanup: `video_path.unlink()` after extraction |
| Numbered URL format not parsed | Added parser for `N|https://...` format in `load_input_file` |
| `r['code']` KeyError in batch loop | Fixed by passing `processed` set to `process_reel` |
| `UnboundLocalError: success` | Wrapped batch loop in try/except, initialized vars |
| PROCESSED_REELS.json using dict with reel_code keys | Fixed batch processing to use same dict |
| `load_input_file` not handling numbered URLs | Added parser for `N|https://...` format |

---

## 🔄 Batch Processing Workflow

```bash
# Process 20 at a time (recommended)
python3 scripts/process_batch.py --batch 20 --start 0

# Dry run to preview classifications
python3 scripts/process_batch.py --batch 10 --start 0 --dry-run

# Process specific category
python3 scripts/process_batch.py --batch 20 --start 0 --category transitions

# Resume from failure
python3 scripts/process_batch.py --batch 20 --start 165
```

---

## 🔗 Related Files

- `templates/vault_note_template.md` — Vault markdown template with asset references
- `templates/skill_template.md` — Hermes skill template with asset section
- `scripts/run_pipeline.py` — Main executor (calls asset generation)
- `references/config_video_effects.yaml` — Category keywords for classification
- `references/burner-account-workflow.md` — Burner account setup for Instagram access

---

## 🔄 Next Session Priorities

1. **Add caption/hashtag/creator extraction** to script (browser automation step)
2. **Process remaining ~10 reels** (350/360 already done)
3. **Generate final exports**: JSON, CSV, Mermaid diagram, interactive HTML
4. **Update master indexes** with all processed effects
5. **Create ARCHITECTURE_DIAGRAM.md** with Mermaid visualization

---

*Last updated: 2025-07-16 | Session: 350+ effects processed | Pipeline: Production-ready*