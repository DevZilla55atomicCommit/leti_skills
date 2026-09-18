---
name: instagram-davinci-video-effects-pipeline
description: "Unified automation skill for extracting DaVinci Resolve video effects techniques from Instagram Reels and building a structured knowledge base in the Video_Effects vault folder."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Instagram, DaVinci Resolve, Video Effects, Transitions, Compositing, Motion Graphics, VFX, Automation, Learning, Vault, Skills]
---

# Instagram → DaVinci Video Effects Learning Pipeline

> **Unified automation skill** for extracting DaVinci Resolve video effects techniques from Instagram Reels and building a structured knowledge base in the `Video_Effects` vault folder.

---

## 🎯 What This Does

```text
Instagram URLs (RTF/CSV/TXT/JSON)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INSTAGRAM-DAVINCI-VIDEO-EFFECTS-PIPELINE                           │
├─────────────────────────────────────────────────────────────────────┤
│  1. Parse & Deduplicate     →  Remove already-processed URLs       │
│  2. Availability Check      →  Filter private/deleted/age-gated    │
│  3. Content Extraction      →  Browser + Vision analysis           │
│  4. Effect Classification   →  Auto-categorize by effect type      │
│  5. Visual Asset Capture    →  Screenshots/GIFs of effect demo     │
│  6. Skill Generation        →  ~/.hermes/skills/video-effects/     │
│  7. Vault Note Creation     →  Video_Effects/{category}/           │
│  8. Queue Management        →  Done / Skipped / Educational        │
│  9. Export Regeneration     →  JSON/CSV/HTML/Architecture          │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
Structured Knowledge Base + Visual Assets (GIFs/Screenshots)
```

---

## 🚀 Quick Start

```bash
# From terminal (Hermes CLI)
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json

# Dry run to preview classifications
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --dry-run

# Filter to specific creator
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --filter-creator art3.studi0

# Retry failed URLs
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --retry-failed

# Custom batch size
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --batch-size 5
```

---

## 📥 Supported Input Formats

| Format | Description | Example |
|--------|-------------|---------|
| **JSON** | Array of objects with url, creator, notes, priority | `urls.json` |
| **CSV** | `url,creator,notes,priority` headers | `urls.csv` |
| **TXT** | Plain text, one URL per line | `urls.txt` |
| **RTF** | Rich Text Format (exported from Notes, Word) | `urls.rtf` |

### JSON Example
```json
[
  {
    "url": "https://www.instagram.com/reel/DaxUaKYuhb0/",
    "creator": "art3.studi0",
    "notes": "Pro Cut Out Transition - Power Window tracking",
    "priority": "High"
  },
  {
    "url": "https://www.instagram.com/reel/DapOhb0IPxm/",
    "creator": "creator.handle",
    "notes": "Glitch transition effect",
    "priority": "Normal"
  }
]
```

### CSV Example
```csv
url,creator,notes,priority
https://www.instagram.com/reel/DaxUaKYuhb0/,art3.studi0,"Pro Cut Out Transition",High
https://www.instagram.com/reel/DapOhb0IPxm/,creator.handle,"Glitch transition",Normal
```

### RTF Example (from Apple Notes)
```rtf
{\rtf1\ansi https://www.instagram.com/reel/DaxUaKYuhb0/ @art3.studi0 Pro Cut Out Transition}
{\rtf1\ansi https://www.instagram.com/reel/DapOhb0IPxm/ @creator.handle Glitch Transition}
```

---

## ⚙️ Configuration

Edit `references/config_video_effects.yaml` to customize:

```yaml
# Processing
batch_size: 10
max_concurrent: 3

# Categories with keyword matching
categories:
  - name: "Transitions"
    keywords: ["cut out", "whip pan", "match cut", "morph", "dissolve", "wipe", "slide", "push", "iris"]
    folder: "transitions/"
  - name: "Compositing"
    keywords: ["green screen", "rotoscope", "matte", "keying", "alpha", "chroma key", "luma key"]
    folder: "compositing/"
  - name: "Motion Graphics"
    keywords: ["lower third", "kinetic type", "title", "lowerthird", "animated text"]
    folder: "motion-graphics/"
  - name: "VFX"
    keywords: ["particles", "explosion", "fire", "smoke", "sci-fi", "energy", "magic", "portal"]
    folder: "vfx/"
  - name: "Text Effects"
    keywords: ["kinetic type", "3d text", "callout", "subtitle", "typewriter"]
    folder: "text-effects/"
  - name: "Stylization"
    keywords: ["glitch", "vhs", "film damage", "halation", "film burn", "light leaks", "crt"]
    folder: "stylization/"
  - name: "Time Effects"
    keywords: ["speed ramp", "time remap", "freeze frame", "slo-mo", "frame blend"]
    folder: "time-effects/"

# Skip patterns (promo, meme, non-DaVinci, etc.)
skip_patterns:
  - "promo"
  - "preset pack"
  - "lightroom"
  - "mobile"
  - "magimir"
  - "snapseed"
  - "vsco"
  - "picsart"
  - "facetune"
  - "airbrush"
  - "meitu"
  - "beautyplus"
  - "meme"
  - "joke"
  - "funny"
  - "comment.*tutorial"
  - "guide.*promo"
  - "masterclass promo"
  - "lut pack"
  - "buy now"
  - "link in bio"
  - "discount"
  - "sale"

# Camera Theory (reclassify, don't skip)
camera_theory_keywords:
  - "raw vs log"
  - "dynamic range"
  - "sensor"
  - "bit depth"
  - "log curve"
  - "gamma curve"
  - "camera theory"
  - "raw workflow"
  - "log workflow"
  - "exposure latitude"
  - "highlight rolloff"
  - "noise floor"
  - "transfer function"

# Lightroom/Mobile Editing Keywords (Route to Photography/Lightroom/)
lightroom_mobile_keywords:
  - "lightroom mobile"
  - "lr mobile"
  - "mobile editing"
  - "iphone editing"
  - "mobile photography"
  - "photo editing"
  - "tone curve"
  - "point curve"
  - "rgb curve"
  - "color grading panel"
  - "calibration panel"
  - "hsl panel"
  - "masking"
  - "adaptive preset"
  - "preset"
  - "creative profile"
  - "magimir"
  - "snapseed"
  - "vsco"
  - "picsart"
  - "facetune"
  - "airbrush"
  - "meitu"
  - "beautyplus"
  - "mobile curves"
  - "photo editing curves"
  - "mobile photo editing"

# Output exports
exports:
  - video_effects_export.json
  - video_effects_export.csv
  - skills_export.json
  - skills_export.csv
  - ARCHITECTURE_DIAGRAM.md
  - ARCHITECTURE_DIAGRAM_INTERACTIVE.html
```

---

## 📊 Output Artifacts

### 1. Hermes Skills (`~/.hermes/skills/video-effects/`)

```bash
davinci-resolve-cut-out-transition/
├── SKILL.md          # Full skill with frontmatter
├── assets/
│   ├── demo.gif              # Full reel demonstration
│   ├── transition_demo.gif   # 3-second effect loop
│   ├── frame_before.png      # Before effect
│   ├── frame_during.png      # Mid-effect
│   ├── frame_after.png       # After effect
│   └── before_after_comparison.png
└── references/       # Source URL, creator info
```

### 2. Vault Notes (`DaVinci_Knowledge_Base/Video_Effects/`)

```text
Video_Effects/
├── 00-MASTER-INDEX.md                    # Category TOC + navigation
├── TEMPLATE-Video-Effect.md              # Template for new effects
├── VIDEO_EFFECTS_QUEUE.md                # Processing queue
├── Video_Effects_Exports/                # JSON/CSV/HTML exports
│   ├── video_effects_export.json
│   ├── video_effects_export.csv
│   ├── ARCHITECTURE_DIAGRAM.md           # Mermaid diagram
│   └── ARCHITECTURE_DIAGRAM_INTERACTIVE.html
├── assets/                               # Visual assets by category
│   ├── transitions/
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── text-effects/
│   ├── stylization/
│   └── time-effects/
├── transitions/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Effect_Name_Source_Tools.md
├── compositing/
├── motion-graphics/
├── vfx/
├── text-effects/
├── stylization/
└── time-effects/
```

### 3. Queue Tracking (`VIDEO_EFFECTS_QUEUE.md`)

```markdown
| #  | Reel Code | URL                                    | Creator    | Effect              | Category      | Status | Vault File |
|----|-----------|----------------------------------------|------------|---------------------|---------------|--------|------------|
| 1  | DaxUaKYuhb0 | instagram.com/reel/DaxUaKYuhb0/      | @art3.studi0 | Pro Cut Out Transition | Transitions | ✅ Done | transitions/01-Pro-Cut-Out-Transition_Art3Studi0_PowerWindow-Tracker.md |
| 2  | DapOhb0IPxm | instagram.com/reel/DapOhb0IPxm/      | @creator   | Glitch Transition   | Stylization | ✅ Done | stylization/02-Glitch-Transition_Creator_Tools.md |
| 3  | DaK6odIgA6I | instagram.com/p/DaK6odIgA6I/         | @creator   | Photo Carousel      | ⏭️ Skipped (Not Reel) | Not a reel |
```

---

## 🏷️ Auto-Categorization

| Category | Keywords | Vault Folder |
|----------|----------|--------------|
| **Transitions** | cut out, whip pan, match cut, morph, dissolve, wipe, slide, push, iris | `transitions/` |
| **Compositing** | green screen, rotoscope, matte, keying, alpha, chroma key, luma key | `compositing/` |
| **Motion Graphics** | lower third, kinetic type, title, lowerthird, animated text | `motion-graphics/` |
| **VFX** | particles, explosion, fire, smoke, sci-fi, energy, magic, portal | `vfx/` |
| **Text Effects** | kinetic type, 3d text, callout, subtitle, typewriter | `text-effects/` |
| **Stylization** | glitch, vhs, film damage, halation, film burn, light leaks, crt | `stylization/` |
| **Time Effects** | speed ramp, time remap, freeze frame, slo-mo, frame blend | `time-effects/` |

### Skip Auto-Detection
- Promo/marketing reels → ⏭️ Skipped (Promo)
- **Lightroom/Photoshop content** → 📸 **Route to Photography/Lightroom/** (not skipped)
- Memes/jokes → ⏭️ Skipped (Not Educational)
- **General camera theory** → 📚 **Camera Theory/** (reclassified, not skipped)
- Mobile app editing (Magimir, Snapseed, VSCO, etc.) → 📸 **Route to Photography/Lightroom/**

---

## 🔧 Advanced Usage

### Resume Interrupted Run
```bash
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --retry-failed
```

### Custom Batch Size
```bash
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --batch-size 5
```

### Custom Config
```bash
hermes skill run instagram-davinci-video-effects-pipeline --input urls.json --config my-config.yaml
```

---

## 📁 Skill Structure

```text
instagram-davinci-video-effects-pipeline/
├── SKILL.md                          # This file
├── references/
│   ├── config_video_effects.yaml     # Main configuration
│   ├── skipped-queue-patterns.md     # Queue status patterns
│   └── skip-pattern-examples.md      # Real-world skip cases
├── templates/
│   ├── vault_note_template.md        # Vault markdown template
│   └── skill_template.md             # Hermes skill template
├── scripts/
│   └── run_pipeline.py               # Main Python executor
└── assets/                           # (reserved for future)
```

---

## 🔗 Dependencies

### Required Hermes Tools
- `browser_navigate`, `browser_snapshot`, `browser_vision`, `browser_console`
- `terminal`, `search_files`, `read_file`, `write_file`, `patch`
- `skill_manage`, `execute_code`, `cronjob`

### System Dependencies
- `yt-dlp` — Instagram video download (with Chrome cookies)
  - **Critical**: Must use `--cookies-from-browser chrome` to bypass login wall
  - Run `yt-dlp -U` before batch runs to ensure latest Instagram extractor
- `ffmpeg` — Frame extraction, GIF creation
  - Frame extraction: `ffmpeg -i input.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png`
  - GIF creation: `ffmpeg -i input.mp4 -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" -loop 0 output.gif`
  - Key frames: `ffmpeg -i input.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png` (adjust n for during/after)
  - Before/after: `ffmpeg -i before.png -i after.png -filter_complex "hstack=inputs=2" comparison.png`
- `gifsicle` — GIF optimization: `gifsicle -O3 --lossy=80 input.gif -o output.gif`

### Instagram-Specific Workflow Notes
- **Login wall bypass**: yt-dlp with Chrome cookies is the only reliable method; browser automation hits rate limits
- **Rate limiting**: Process in batches of 10 with 2-3 second delays between downloads
- **Post vs Reel**: Posts (multi-image carousels) download as multiple short videos; filter by type in queue
- **Age-gated content**: Some reels require login even with cookies; mark as unavailable in queue
- **Private accounts**: Cannot be downloaded even with cookies; skip immediately
- **Burner account workflow**: Use dedicated burner Instagram account with separate Chrome profile for cookie extraction
  - Create burner email + burner phone number
  - Create isolated Chrome profile: `--user-data-dir=/tmp/ig_burner_profile`
  - Log in with burner credentials, export cookies via Cookie Editor extension
  - Save cookies to project directory, reference in yt-dlp `--cookies burner_cookies.txt`
  - **Critical**: MP4 auto-cleanup after asset extraction to preserve SSD health

### Required Skills (auto-loaded)
- `instagram-reel-availability-check` — Batch URL verification
- `instagram-unavailable-content-handling` — Log failed reels
- `regenerate_exports_and_diagram` — JSON/CSV/Mermaid/HTML generation

### Python Dependencies (for run_pipeline.py)
```bash
pip install pyyaml
# stdlib: argparse, json, csv, re, datetime, pathlib, subprocess
```

### System Dependencies
- `yt-dlp` — Instagram video download (with Chrome cookies)
  - **Critical**: Must use `--cookies-from-browser chrome` to bypass login wall
  - Run `yt-dlp -U` before batch runs to ensure latest Instagram extractor
- `ffmpeg` — Frame extraction, GIF creation, video processing
  - Frame extraction: `ffmpeg -i input.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png`
  - GIF creation: `ffmpeg -i input.mp4 -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" -loop 0 output.gif`
  - Key frames: `ffmpeg -i input.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png` (adjust n for during/after)
  - Before/after: `ffmpeg -i before.png -i after.png -filter_complex "hstack=inputs=2" comparison.png`
- `gifsicle` — GIF optimization: `gifsicle -O3 --lossy=80 input.gif -o output.gif`

### Instagram-Specific Workflow Notes
- **Login wall bypass**: yt-dlp with Chrome cookies is the only reliable method; browser automation hits rate limits
- **Rate limiting**: Process in batches of 10 with 2-3 second delays between downloads
- **Post vs Reel**: Posts (multi-image carousels) download as multiple short videos; filter by type in queue
- **Age-gated content**: Some reels require login even with cookies; mark as unavailable in queue
- **Private accounts**: Cannot be downloaded even with cookies; skip immediately

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No URLs extracted" | Check input format; RTF needs `textutil` on macOS |
| "Skill already exists" | Use `--retry-failed` or delete old skill first |
| "Browser timeout" | Increase `timeout_seconds` in config |
| "Classification wrong" | Add more keywords to category in config |
| "Download failed" | Ensure Chrome is logged into Instagram; update yt-dlp |
| "Export diagram too large" | Use "Folders Only" view in HTML |

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release — full pipeline with 7 effect categories, visual assets, Hermes skills |
| 1.6.0 | 2025-07-15 | **Full batch processing complete** — 350/360 Instagram URLs processed (10 posts skipped); 12 Hermes skills generated with bundled assets (demo GIF, transition loop, before/during/after frames, before/after comparison); 557 vault notes created across 4 categories (Transitions, Compositing, Motion Graphics, Stylization); automated batch processor `scripts/process_batch.py` production-ready with Chrome cookie auth, MP4 auto-cleanup, visual asset extraction; 12 Hermes skills created under `~/.hermes/skills/video-effects/` |

---

## 📸 Visual Asset Strategy (Key Differentiator)

For **each effect**, the pipeline captures:

| Asset | Description | Tool |
|-------|-------------|------|
| **Effect Demo GIF** | 2-3 sec loop from reel | `ffmpeg` |
| **Node Graph Screenshot** | DaVinci node graph/Fusion flow | MCP / manual |
| **Parameter Panels** | Key settings visible | Browser vision |
| **Key Frames (3-5)** | Before, during, after | Frame extraction |
| **Before/After Comparison** | Side-by-side frame | `ffmpeg hstack` |

**Storage:** `Video_Effects/assets/{category}/{effect-slug}/`

---

## 📚 Session Learnings Reference

See `references/visual-asset-pipeline.md` for:
- FFmpeg recipes (frame extraction, GIF creation, key frames, comparisons)
- Batch processing Python script
- Key session learnings (yt-dlp + Chrome cookies, frame timing, GIF optimization, batch sizing)
- Storage structure and category folders

---

## 🤝 Related Skills

| Skill | Purpose |
|-------|---------|
| `instagram-reel-availability-check` | Verify reel accessibility before processing |
| `instagram-unavailable-content-handling` | Log and categorize unavailable content |
| `regenerate_exports_and_diagram` | Generate exports + Mermaid architecture diagram |
| `video-tutorial-extraction` | YouTube equivalent (transcript-based) |
| `davinci_color_grading` | DaVinci Resolve color grading reference |

---

## 📸 Visual Asset Strategy (Key Differentiator)

For **each effect**, the pipeline captures:

| Asset | Description | Tool |
|-------|-------------|------|
| **Effect Demo GIF** | 2-3 sec loop from reel | `ffmpeg` |
| **Node Graph Screenshot** | DaVinci node graph/Fusion flow | MCP / manual |
| **Parameter Panels** | Key settings visible | Browser vision |
| **Key Frames (3-5)** | Before, during, after | Frame extraction |
| **Before/After Comparison** | Side-by-side frame | `ffmpeg hstack` |

**Storage:** `Video_Effects/assets/{category}/{effect-slug}/`

---

*Part of the DaVinci Knowledge Base automation suite.*  
*Generated skills follow the `davinci-resolve-{effect-slug}` naming convention.*