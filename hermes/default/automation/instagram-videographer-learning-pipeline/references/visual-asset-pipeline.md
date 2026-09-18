# Visual Asset Pipeline — Carousel Posts & Reels

> **Key Differentiator:** For each technique, capture visual assets that make it immediately understandable without reading text.

---

## 📸 Asset Requirements per Content Type

### Reels (`/reel/`) — Video Source

#### Method A: yt-dlp (requires auth cookies)
| Asset | Purpose | Specs | Tool |
|-------|---------|-------|------|
| **Demo GIF** | Full reel demonstration | 10fps, 720px wide, full duration | `ffmpeg -vf "fps=10,scale=720:-1"` |
| **Technique Loop** | 3-second effect loop | 8fps, 480px wide, palette=64 | `ffmpeg -filter_complex "fps=8,scale=480:-1,palettegen=64"` |
| **Frame Before** | Clean frame before effect | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,0)'"` |
| **Frame During** | Peak effect moment | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,N)'`" |
| **Frame After** | Clean frame after effect | 1080p/4K PNG | `ffmpeg -vf "select='eq(n,M)'`" |
| **Comparison** | Side-by-side before/after | 2x width PNG | `ffmpeg -i before.png -i after.png -filter_complex "hstack=inputs=2"` |
| **Node Graph** | DaVinci node tree screenshot | PNG | MCP / manual |

#### Method B: Browser-Based Frame Capture (NO AUTH REQUIRED) ⭐ NEW
| Asset | Purpose | Specs | Tool |
|-------|---------|-------|------|
| **Demo GIF** | Full reel demonstration | 10fps, 720px wide | Browser: seek + canvas capture → `ffmpeg` |
| **Technique Loop** | 3-second effect loop | 8fps, 480px wide | Browser: extract segment frames → `ffmpeg` |
| **Frame Before** | Clean frame before effect | 1080p/4K PNG | Browser: `canvas.toDataURL('image/png')` |
| **Frame During** | Peak effect moment | 1080p/4K PNG | Browser: seek to peak → canvas capture |
| **Frame After** | Clean frame after effect | 1080p/4K PNG | Browser: seek to end → canvas capture |
| **Comparison** | Side-by-side before/after | 2x width PNG | `ffmpeg -i before.png -i after.png -filter_complex "hstack=inputs=2"` |
| **Node Graph** | DaVinci node tree screenshot | PNG | MCP / manual |

**Browser Frame Capture Workflow:**
```javascript
// 1. Navigate to Reel URL
await browser_navigate({url: "https://www.instagram.com/reel/XXX/"});

// 2. Find video element and wait for load
const video = document.querySelector('video');
await video.play();

// 3. Capture frame at specific timestamp
function captureFrame(video, timeMs) {
  video.currentTime = timeMs / 1000;
  return new Promise(resolve => {
    video.onseeked = () => {
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      resolve(canvas.toDataURL('image/png'));
    };
  });
}

// 4. Extract key frames
const frames = await Promise.all([
  captureFrame(video, 0),           // Frame Before
  captureFrame(video, 1500),        // Frame During (adjust per reel)
  captureFrame(video, 3000),        // Frame After
]);

// 5. Save as PNG files (via browser download or base64 → file)
// 6. Generate GIFs locally with ffmpeg
```

**Advantages:**
- ✅ Zero authentication required
- ✅ Works on any public Reel
- ✅ Can seek to exact timestamps visually
- ✅ Captures full resolution (no quality loss)
- ✅ Avoids Instagram's bot detection entirely

---

### Carousels (`/p/`) — Static Images
| Asset | Purpose | Specs | Tool |
|-------|---------|-------|------|
| **Per-Slide PNG** | Each carousel slide | Original resolution | Browser download / screenshot |
| **Carousel Combined GIF** | All slides as animation | 1fps, 720px wide | `ffmpeg -framerate 1 -i slide_%02d.png -vf "scale=720:-1"` |
| **Technique Comparison Grid** | All techniques side-by-side | Tile layout | `ffmpeg -i slide_01.png -i slide_02.png ... -filter_complex "tile=5x1"` |
| **Per-Technique Key Frame** | Representative frame per technique | 1080p/4K PNG | Vision analysis pick |

---

## 🎬 FFmpeg Recipes (Copy-Paste Ready)

### Reel Frame Extraction (10fps, 720p)
```bash
ffmpeg -i reel.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png
```

### Reel Technique Loop GIF (3s, 8fps, 480px, 64 colors)
```bash
ffmpeg -i reel.mp4 -filter_complex \
"[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \
-loop 0 technique_demo.gif
```

### Reel Key Frames (adjust frame numbers per effect)
```bash
# Before effect (usually frame 0)
ffmpeg -i reel.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png

# During effect (find peak frame visually, e.g., frame 30)
ffmpeg -i reel.mp4 -vf "select='eq(n,30)'" -vframes 1 frame_during.png

# After effect (e.g., frame 60)
ffmpeg -i reel.mp4 -vf "select='eq(n,60)'" -vframes 1 frame_after.png
```

### Before/After Comparison
```bash
ffmpeg -i frame_before.png -i frame_after.png \
-filter_complex "hstack=inputs=2" before_after_comparison.png
```

### Carousel Combined GIF (from slide PNGs)
```bash
# slides named slide_01.png, slide_02.png, etc.
ffmpeg -framerate 1 -i slide_%02d.png \
-vf "scale=720:-1:flags=lanczos" carousel_combined.gif
```

### Carousel Technique Comparison Grid (5 techniques)
```bash
ffmpeg -i slide_01.png -i slide_02.png -i slide_03.png -i slide_04.png -i slide_05.png \
-filter_complex "tile=5x1" technique_comparison_grid.png
```

### Batch Asset Generation (Single Command)
```bash
cd /path/to/effect/assets && \
ffmpeg -i reel.mp4 \
-vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png && \
ffmpeg -i reel.mp4 -filter_complex \
"[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" \
-loop 0 technique_demo.gif && \
ffmpeg -i reel.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png && \
ffmpeg -i reel.mp4 -vf "select='eq(n,30)'" -vframes 1 frame_during.png && \
ffmpeg -i reel.mp4 -vf "select='eq(n,60)'" -vframes 1 frame_after.png && \
ffmpeg -i frame_before.png -i frame_after.png \
-filter_complex "hstack=inputs=2" before_after_comparison.png
```

### Carousel Batch (from slide PNGs)
```bash
cd /path/to/post/assets && \
ffmpeg -framerate 1 -i slide_%02d.png \
-vf "scale=720:-1:flags=lanczos" carousel_combined.gif && \
ffmpeg -i slide_01.png -i slide_02.png -i slide_03.png -i slide_04.png -i slide_05.png \
-filter_complex "tile=5x1" technique_comparison_grid.png
```

---

## 📁 Storage Structure

```
DaVinci_Knowledge_Base/
├── Video_Effects/assets/{category}/{effect-slug}/
│   ├── demo.gif
│   ├── technique_demo.gif
│   ├── frame_before.png
│   ├── frame_during.png
│   ├── frame_after.png
│   ├── before_after_comparison.png
│   └── reel.mp4          # archival (auto-cleanup after extraction)
│
├── Videographer/assets/
│   ├── {post-code}/              # carousel shared assets
│   │   ├── slide_01.png ... slide_N.png
│   │   ├── carousel_combined.gif
│   │   └── technique_comparison_grid.png
│   ├── cinematography/{technique-slug}/
│   ├── camera-movement/{technique-slug}/
│   ├── lenses-optics/{technique-slug}/
│   ├── lighting/{technique-slug}/
│   ├── composition/{technique-slug}/
│   ├── production/{technique-slug}/
│   ├── post-production/{technique-slug}/
│   ├── vfx-compositing/{technique-slug}/
│   ├── audio-sound/{technique-slug}/
│   └── business-career/{technique-slug}/
```

---

## ⚡ Key Learnings from Sessions

### Video Effects Pipeline (350+ effects processed)
1. **yt-dlp + Chrome cookies** = only reliable Instagram download method
2. **Frame numbers matter** — peak effect rarely at frame 30/60; inspect visually first
3. **GIF optimization** — `palettegen=max_colors=64` + `dither=none` = small, clean GIFs
4. **Comparison images** — `hstack` creates instant before/after understanding
5. **Batch 10 URLs** with 2-3s delays = sustainable rate limiting
6. **Post vs Reel** — carousels download as multiple short videos; filter by `type: reel`
7. **Auto-cleanup mp4s** — delete source mp4 after GIF/frame extraction to save SSD space
8. **Auto-classification needs caption/hashtags** — current script shows "unknown" because Instagram page isn't scraped for metadata

### Videographer Pipeline (Carousel-First)
1. **Carousels are static** — no video download; browser vision must click through slides
2. **Each slide = potential technique** → separate vault note + skill
3. **Queue tracking**: One row per slide/technique, same post code
4. **Visual assets**: Per-slide PNGs + combined carousel GIF + technique comparison grid
5. **Navigation pattern**: `browser_click` on `@e184` (next arrow) between `browser_vision` calls

---

## 🔧 Script Fixes Tracker

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
| PROCESSED_REELS.json using dict with reel_code keys | Fixed batch processing to use same dict structure |
| `load_input_file` not handling numbered URLs | Added parser for `N|https://...` format |

---

## 🔄 Batch Processing Workflow

```bash
# Process 20 at a time (recommended)
python3 scripts/run_pipeline.py --batch 20 --start 0

# Dry run to preview classifications
python3 scripts/run_pipeline.py --batch 10 --start 0 --dry-run

# Process specific discipline
python3 scripts/run_pipeline.py --batch 20 --start 0 --discipline cinematography

# Resume from failure
python3 scripts/run_pipeline.py --batch 20 --start 165

# Process carousel posts specifically
python3 scripts/run_pipeline.py --batch 10 --start 0 --content-type carousel
```

---

## 🔗 Related Files

- `templates/vault_note_template.md` — Vault markdown template with asset references
- `templates/skill_template.md` — Hermes skill template with asset section
- `scripts/run_pipeline.py` — Main executor (calls asset generation)
- `references/config_videographer.yaml` — Category keywords for classification
- `references/burner-account-workflow.md` — Burner account setup for Instagram access

---

## 🔄 Next Session Priorities

1. **Add caption/hashtag/creator extraction** to script (browser automation step)
2. **Build `scripts/run_pipeline.py`** — full batch processor for videographer pipeline
3. **Process remaining carousel slides 2-6** from @anshuluniyyal post
4. **Test with 3+ carousel posts** to validate automation
5. **Add reel processing** — full video frame/GIF extraction via yt-dlp + ffmpeg

---

*Last updated: 2025-07-17 | Session: Pipeline creation + 1 carousel post | Status: Carousel-ready, Reel-pending*