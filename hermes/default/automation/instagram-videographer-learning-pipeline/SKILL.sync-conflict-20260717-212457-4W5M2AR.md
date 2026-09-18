---
name: instagram-videographer-learning-pipeline
description: "Unified automation skill for extracting videography education content from Instagram (Reels, Posts, Carousels) and building a structured knowledge base across Camera Theory, Cinematography, Lighting, Composition, Color Grading, and DaVinci Resolve Effects."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Instagram, Videography, Cinematography, Camera Theory, Lighting, Composition, Color Grading, DaVinci Resolve, Video Effects, Automation, Learning, Vault, Skills]
---

# Instagram → Videographer Learning Pipeline

> **Unified automation skill** for extracting videography education content from Instagram Reels, Posts, and Carousels and building a structured knowledge base across multiple disciplines.

---

## 🎯 What This Does

```text
Instagram URLs (RTF/CSV/TXT/JSON)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INSTAGRAM-VIDEOGRAHER-LEARNING-PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│  1. Parse & Deduplicate     →  Remove already-processed URLs       │
│  2. Availability Check      →  Filter private/deleted/age-gated    │
│  3. Content Extraction      →  Browser + Vision analysis           │
│  4. Discipline Classification →  Auto-categorize by discipline     │
│  5. Visual Asset Capture    →  Screenshots/GIFs of key frames      │
│  6. Skill/Note Generation   →  ~/.hermes/skills/videographer/      │
│  7. Vault Note Creation     →  DaVinci_Knowledge_Base/ +          │
│                               Photography/ + Videographer/         │
│  8. Queue Management        →  Done / Skipped / Camera Theory /   │
│                               Cinematography / Lighting / etc.    │
│  9. Export Regeneration     →  JSON/CSV/HTML/Architecture         │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
Structured Knowledge Base + Visual Assets (GIFs/Screenshots)
```

---

## 🚀 Quick Start

```bash
# From terminal (Hermes CLI)
hermes skill run instagram-videographer-learning-pipeline --input urls.json

# Dry run to preview classifications
hermes skill run instagram-videographer-learning-pipeline --input urls.json --dry-run

# Filter to specific creator
hermes skill run instagram-videographer-learning-pipeline --input urls.json --filter-creator anshuluniyyal

# Retry failed URLs
hermes skill run instagram-videographer-learning-pipeline --input urls.json --retry-failed

# Custom batch size
hermes skill run instagram-videographer-learning-pipeline --input urls.json --batch-size 5
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
    "url": "https://www.instagram.com/p/DaBejwDkznl/",
    "creator": "anshuluniyyal",
    "notes": "The Art of Static Shots - Cinematography theory",
    "priority": "Normal"
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
https://www.instagram.com/p/DaBejwDkznl/,anshuluniyyal,"The Art of Static Shots",Normal
```

### RTF Example (from Apple Notes)
```rtf
{\rtf1\ansi https://www.instagram.com/reel/DaxUaKYuhb0/ @art3.studi0 Pro Cut Out Transition}
{\rtf1\ansi https://www.instagram.com/p/DaBejwDkznl/ @anshuluniyyal The Art of Static Shots}
```

---

## ⚙️ Configuration

Edit `references/config_videographer.yaml` to customize:

```yaml
# Processing
batch_size: 10
max_concurrent: 3
timeout_seconds: 120

# Content Type Detection
content_types:
  - name: "Reel"
    url_pattern: "/reel/"
    is_video: true
  - name: "Post/Carousel"
    url_pattern: "/p/"
    is_video: false
  - name: "TV/IGTV"
    url_pattern: "/tv/"
    is_video: true

# Discipline Categories with keyword matching
categories:
  # DaVinci Resolve Specific
  - name: "Video Effects & Transitions"
    keywords: ["cut out", "whip pan", "match cut", "morph", "dissolve", "wipe", "slide", "push", "iris", "transition", "glitch", "vhs", "film damage", "halation", "film burn", "light leaks", "crt", "particles", "explosion", "fire", "smoke", "sci-fi", "energy", "magic", "portal", "lower third", "kinetic type", "title", "animated text", "speed ramp", "time remap", "freeze frame", "slo-mo", "frame blend", "green screen", "rotoscope", "matte", "keying", "alpha", "chroma key", "luma key"]
    folder: "Video_Effects/"
    subcategories:
      - name: "Transitions"
        keywords: ["cut out", "whip pan", "match cut", "morph", "dissolve", "wipe", "slide", "push", "iris"]
        folder: "Video_Effects/transitions/"
      - name: "Compositing"
        keywords: ["green screen", "rotoscope", "matte", "keying", "alpha", "chroma key", "luma key"]
        folder: "Video_Effects/compositing/"
      - name: "Motion Graphics"
        keywords: ["lower third", "kinetic type", "title", "lowerthird", "animated text", "callout"]
        folder: "Video_Effects/motion-graphics/"
      - name: "VFX"
        keywords: ["particles", "explosion", "fire", "smoke", "sci-fi", "energy", "magic", "portal"]
        folder: "Video_Effects/vfx/"
      - name: "Text Effects"
        keywords: ["kinetic type", "3d text", "callout", "subtitle", "typewriter"]
        folder: "Video_Effects/text-effects/"
      - name: "Stylization"
        keywords: ["glitch", "vhs", "film damage", "halation", "film burn", "light leaks", "crt"]
        folder: "Video_Effects/stylization/"
      - name: "Time Effects"
        keywords: ["speed ramp", "time remap", "freeze frame", "slo-mo", "frame blend"]
        folder: "Video_Effects/time-effects/"

  - name: "Color Grading & Color Science"
    keywords: ["color grade", "color grading", "white balance", "exposure", "cst", "gamut", "primary", "log", "lut", "cinematic", "teal", "orange", "film", "halation", "glow", "kodak", "fujifilm", "s-log3", "slog3", "sony", "s-gamut", "apple log", "apple log 2", "pro res", "prores", "skin tone", "face refinement", "vectorscope", "kodak 2383", "2383", "film emulation", "cineon", "logc", "color compressor", "depth map", "relight", "magic mask", "parade", "vectorscope", "waveform", "rgb parade"]
    folder: "Color Grading & Looks/"

  - name: "Camera Theory & Color Science"
    keywords: ["raw vs log", "dynamic range", "sensor", "bit depth", "log curve", "gamma curve", "camera theory", "raw workflow", "log workflow", "exposure latitude", "highlight rolloff", "noise floor", "transfer function", "raw", "braw", "prores raw", "r3d", "arriraw", "dual gain", "native iso", "eiso", "exposure index", "aces", "dawinci wide gamut", "dwg", "rcm", "cst", "color space transform", "gamut mapping", "sensor science", "debayer", "highlight rolloff"]
    folder: "Camera Theory/"

  # Videographer Disciplines (11 granular categories)
  - name: "Cinematography & Camera Technique"
    keywords: ["static shot", "camera movement", "dolly", "slider", "gimbal", "steadycam", "handheld", "tripod", "cinematography", "camera technique", "establishing shot", "master shot", "coverage", "shot list", "storyboard", "aspect ratio", "scope", "anamorphic", "2.39:1", "16:9", "4:3"]
    folder: "Videographer/Cinematography/"

  - name: "Camera Movement"
    keywords: ["dolly", "slider", "gimbal", "steadycam", "handheld", "tripod", "crane", "jib", "drone", "aerial", "tracking shot", "push in", "pull out", "truck", "pedestal", "arc", "orbit", "follow shot", "lead room", "head room"]
    folder: "Videographer/Camera Movement/"

  - name: "Lenses & Optics"
    keywords: ["lens", "focal length", "aperture", "depth of field", "bokeh", "anamorphic", "spherical", "wide angle", "telephoto", "prime lens", "zoom lens", "focus pulling", "rack focus", "follow focus", "t-stop", "f-stop", "breathing", "flare", "coating", "vignetting", "distortion", "sharpness", "contrast"]
    folder: "Videographer/Lenses & Optics/"

  - name: "Lighting & Exposure"
    keywords: ["lighting", "key light", "fill light", "back light", "rim light", "hair light", "three point", "motivated lighting", "natural light", "available light", "golden hour", "blue hour", "magic hour", "hard light", "soft light", "diffusion", "bounce", "negative fill", "flag", "cto", "ctb", "gel", "color temperature", "kelvin", "white balance", "exposure", "incident meter", "spot meter", "zebra", "false color", "waveform", "histogram", "dynamic range", "latitude", "contrast ratio", "key to fill", "practical", "practical lighting", "led", "hmi", "tungsten", "fluorescent", "daylight", "tungsten balanced", "mixed lighting"]
    folder: "Videographer/Lighting/"

  - name: "Composition & Visual Storytelling"
    keywords: ["composition", "framing", "rule of thirds", "golden ratio", "fibonacci", "leading lines", "symmetry", "asymmetry", "balance", "negative space", "visual weight", "depth", "layers", "foreground", "middleground", "background", "frame within frame", "natural frame", "perspective", "vanishing point", "forced perspective", "scale", "juxtaposition", "contrast", "repetition", "pattern", "rhythm", "visual storytelling", "shot types", "close up", "medium shot", "wide shot", "extreme close up", "establishing shot", "insert", "cutaway", "reaction shot", "pov", "point of view", "over the shoulder", "two shot", "three shot", "group shot"]
    folder: "Videographer/Composition/"

  - name: "Production Workflow & Directing"
    keywords: ["pre production", "production", "post production", "shot list", "storyboard", "call sheet", "schedule", "budget", "crew", "director", "dp", "cinematographer", "gaffer", "key grip", "script supervisor", "continuity", "slate", "clapper", "timecode", "sync", "dailies", "rushes", "assembly", "rough cut", "fine cut", "picture lock", "deliverables", "codec", "container", "proxies", "offline", "online", "conform", "xml", "aaf", "edl", "roundtrip"]
    folder: "Videographer/Production/"

  - name: "Post-Production Workflow"
    keywords: ["editing", "timeline", "assembly", "rough cut", "fine cut", "picture lock", "sound design", "mix", "color grade", "color correction", "vfx", "compositing", "motion graphics", "titles", "lower thirds", "captions", "export", "deliverables", "codec", "container", "proxies", "offline", "online", "conform", "xml", "aaf", "edl", "roundtrip", "da vinci", "resolve", "premiere", "final cut", "avid"]
    folder: "Videographer/Post-Production/"

  - name: "VFX & Compositing"
    keywords: ["vfx", "visual effects", "compositing", "green screen", "blue screen", "rotoscope", "rotoscoping", "matte", "keying", "chroma key", "luma key", "alpha", "tracking", "matchmove", "camera tracking", "object tracking", "planar tracking", "particles", "simulation", "cgi", "3d", "integration", "plate", "clean plate", "set extension", "matte painting", "after effects", "nuke", "fusion", "resolve fusion"]
    folder: "Videographer/VFX & Compositing/"

  - name: "Audio & Sound"
    keywords: ["audio", "sound", "microphone", "mic", "lavalier", "shotgun", "boom", "field recorder", "sync sound", "dual system", "timecode", "room tone", "ambience", "foley", "adr", "dialogue", "music", "score", "sound design", "mix", "loudness", "true peak", "lufs", "dynamic range", "noise reduction", "izotope", "rx", "fairlight", "pro tools", "logic", "reaper"]
    folder: "Videographer/Audio & Sound/"

  - name: "Business & Career"
    keywords: ["freelance", "client", "contract", "invoice", "rate", "day rate", "half day", "quote", "proposal", "portfolio", "reel", "showreel", "marketing", "branding", "networking", "crew", "hiring", "assistant", "gaffer", "key grip", "dp", "director", "producer", "production company", "llc", "insurance", "permits", "location", "scouting", "budget", "schedule"]
    folder: "Videographer/Business & Career/"

  # Photography / Lightroom (Route to Photography/)
  - name: "Photography & Lightroom"
    keywords: ["lightroom mobile", "lr mobile", "lightroom tutorial", "point curve", "tone curve", "rgb curve", "color grading panel", "hsl panel", "calibration panel", "masking", "adaptive preset", "creative profile", "magimir", "snapseed", "vsco", "picsart", "facetune", "airbrush", "meitu", "beautyplus", "mobile editing", "iphone editing", "mobile photography", "photo editing", "mobile curves", "photo editing curves", "mobile photo editing", "photography", "portrait", "landscape", "street photography", "exposure", "aperture", "shutter speed", "iso", "white balance", "raw photo", "jpeg", "histogram"]
    folder: "Photography/Lightroom/"

# Skip patterns (promo, meme, non-educational, etc.)
skip_patterns:
  - "promo"
  - "preset pack"
  - "lightroom"          # Note: now routes to Photography/Lightroom/ instead of skip
  - "meme"
  - "magimir"
  - "mobile"             # Note: now routes to Photography/Lightroom/ instead of skip
  - "app"
  - "smartphone"
  - "iphone editing"
  - "lightroom mobile"
  - "snapseed"
  - "vsco"
  - "picsart"
  - "facetune"
  - "airbrush"
  - "meitu"
  - "beautyplus"
  - "lead magnet"
  - "dm for link"
  - "comment.*tutorial"
  - "guide.*promo"
  - "masterclass promo"
  - "lut pack"
  - "buy now"
  - "link in bio"
  - "discount"
  - "sale"
  - "mobile curves"
  - "photo editing curves"
  - "mobile photo editing"
  - "meme"
  - "joke"
  - "funny"
  - "parody"

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
  - "bit depth"
  - "exposure latitude"
  - "highlight rolloff"
  - "noise floor"

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
  - videographer_knowledge_base_export.json
  - videographer_knowledge_base_export.csv
  - skills_export.json
  - skills_export.csv
  - ARCHITECTURE_DIAGRAM.md
  - ARCHITECTURE_DIAGRAM_INTERACTIVE.html
```

---

## 📊 Output Artifacts

### 1. Hermes Skills (`~/.hermes/skills/videographer/`)

```bash
videographer-cinematography-static-shots-anshuluniyyal/
├── SKILL.md          # Full skill with frontmatter
├── assets/
│   ├── demo.gif              # Full reel demonstration
│   ├── technique_demo.gif    # 3-second technique loop
│   ├── frame_before.png      # Before technique
│   ├── frame_during.png      # Mid-technique
│   ├── frame_after.png       # After technique
│   └── before_after_comparison.png
└── references/       # Source URL, creator info
```

### 2. Vault Notes (Multiple Categories)

```text
DaVinci_Knowledge_Base/
├── Video_Effects/
│   ├── transitions/
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── text-effects/
│   ├── stylization/
│   └── time-effects/
├── Color Grading & Looks/
│   ├── Color Correction Fundamentals/
│   ├── Creative Grading & Looks/
│   ├── Camera Theory/           # ← Camera Theory content here
│   ├── Masking & Power Windows/
│   ├── Node Structures & Templates/
│   ├── DaVinci Resolve 20/
│   ├── S-Log3/
│   ├── Apple Log 2/
│   ├── Skin Tones/
│   └── Kodak 2383/
├── Camera Theory/               # ← Standalone Camera Theory
│   ├── 00-MASTER-INDEX.md
│   └── NN-Topic_Source_Tools.md

Photography/
├── Lightroom/
│   ├── 00-MASTER-INDEX.md
│   ├── TEMPLATE-Photography-Technique.md
│   └── NN-Technique_Source_Tools.md

Videographer/                    # ← NEW: Broader videography education (11 disciplines)
├── 00-MASTER-INDEX.md
├── TEMPLATE-Videographer-Technique.md
├── VIDEOGRAPHER_QUEUE.md
├── Cinematography/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Camera Movement/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Lenses & Optics/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Lighting/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Composition/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Production/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Post-Production/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── VFX & Compositing/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Audio & Sound/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
├── Business & Career/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Technique_Source_Tools.md
└── assets/ (organized by discipline)
    ├── cinematography/
    ├── camera-movement/
    ├── lenses-optics/
    ├── lighting/
    ├── composition/
    ├── production/
    ├── post-production/
    ├── vfx-compositing/
    ├── audio-sound/
    └── business-career/
```

### 3. Queue Tracking (`VIDEOGRAPHER_LEARNING_QUEUE.md`)

```markdown
| #  | Reel Code | URL                                    | Creator        | Discipline              | Category              | Status | Vault File |
|----|-----------|----------------------------------------|----------------|-------------------------|-----------------------|--------|------------|
| 1  | DaxUaKYuhb0 | instagram.com/reel/DaxUaKYuhb0/      | @art3.studi0   | DaVinci Effects         | Transitions           | ✅ Done | Video_Effects/transitions/01-Pro-Cut-Out-Transition.md |
| 2  | DaBejwDkznl | instagram.com/p/DaBejwDkznl/         | @anshuluniyyal | Cinematography          | Camera Technique      | ✅ Done | Videographer/Cinematography/01-Art-of-Static-Shots.md |
| 3  | DapOhb0IPxm | instagram.com/reel/DapOhb0IPxm/      | @creator       | DaVinci Effects         | Stylization           | ✅ Done | Video_Effects/stylization/02-Glitch-Transition.md |
| 4  | DaK6odIgA6I | instagram.com/p/DaK6odIgA6I/         | @creator       | Photography             | Lightroom             | 📸 Route | Photography/Lightroom/01-Mobile-Editing.md |
```

---

## 🏷️ Auto-Categorization Logic

| Discipline | Keywords | Vault Folder |
|------------|----------|--------------|
| **DaVinci Video Effects** | transition, glitch, vfx, compositing, keying, rotoscope, motion graphics, text effects, stylization, time effects | `Video_Effects/{subcategory}/` |
| **Color Grading** | color grade, lut, cst, gamut, log, white balance, skin tone, film emulation | `Color Grading & Looks/{subcategory}/` |
| **Camera Theory** | raw vs log, dynamic range, sensor, bit depth, transfer function, color science | `Camera Theory/` |
| **Cinematography** | static shot, camera movement, lens, focal length, composition, framing, blocking | `Videographer/Cinematography/` |
| **Lighting** | key light, fill light, three point, golden hour, diffusion, color temperature | `Videographer/Lighting/` |
| **Composition** | rule of thirds, leading lines, framing, visual storytelling, shot types | `Videographer/Composition/` |
| **Production** | pre production, shot list, storyboard, call sheet, dailies, conform | `Videographer/Production/` |
| **Photography/Lightroom** | lightroom, mobile editing, snapseed, vsco, tone curve, point curve | `Photography/Lightroom/` |

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
hermes skill run instagram-videographer-learning-pipeline --input urls.json --resume
```

### Custom Batch Size
```bash
hermes skill run instagram-videographer-learning-pipeline --input urls.json --batch-size 5
```

### Force Reprocess (ignore dedup)
```bash
hermes skill run instagram-videographer-learning-pipeline --input urls.json --force
```

### Custom Config
```bash
hermes skill run instagram-videographer-learning-pipeline --input urls.json --config my-config.yaml
```

---

## 📁 Skill Structure

```text
instagram-videographer-learning-pipeline/
├── SKILL.md                          # This file
├── references/
│   ├── config_videographer.yaml      # Main configuration
│   ├── skipped-queue-patterns.md     # Queue status patterns
│   └── skip-pattern-examples.md      # Real-world skip cases
├── templates/
│   ├── vault_note_template.md        # Vault markdown template (video effects)
│   ├── vault_note_template_cinematography.md  # Cinematography template
│   ├── vault_note_template_lighting.md        # Lighting template
│   ├── vault_note_template_composition.md     # Composition template
│   ├── vault_note_template_camera_theory.md   # Camera theory template
│   ├── vault_note_template_lightroom.md       # Lightroom template
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
- `ffmpeg` — Frame extraction, GIF creation
  - Frame extraction: `ffmpeg -i input.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" frame_%03d.png`
  - GIF creation: `ffmpeg -i input.mp4 -filter_complex "[0:v]fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=none" -loop 0 output.gif`
  - Key frames: `ffmpeg -i input.mp4 -vf "select='eq(n,0)'" -vframes 1 frame_before.png`
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

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No URLs extracted" | Check input format; RTF needs `textutil` on macOS |
| "Skill already exists" | Use `--force` or delete old skill first |
| "Browser timeout" | Increase `timeout_seconds` in config |
| "Classification wrong" | Add more keywords to category in config |
| "Download failed" | Ensure Chrome is logged into Instagram; update yt-dlp |
| "Export diagram too large" | Use "Folders Only" view in HTML |
| "Carousel post not processed" | Add carousel handling in vision analysis step |

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-17 | Initial release — full pipeline with 8 disciplines, multi-vault routing, visual assets, Hermes skills |

---

## 📸 Visual Asset Strategy (Key Differentiator)

For **each technique**, the pipeline captures:

| Asset | Description | Tool |
|-------|-------------|------|
| **Technique Demo GIF** | 2-3 sec loop from reel/post | `ffmpeg` |
| **Node Graph Screenshot** | DaVinci node graph/Fusion flow | MCP / manual |
| **Parameter Panels** | Key settings visible | Browser vision |
| **Key Frames (3-5)** | Before, during, after | Frame extraction |
| **Before/After Comparison** | Side-by-side frame | `ffmpeg hstack` |

**Storage:** `assets/{discipline}/{category}/{technique-slug}/`

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
| `instagram-davinci-video-effects-pipeline` | Original video-effects-only pipeline |

---

## 📸 Visual Asset Strategy (Key Differentiator)

For **each technique**, the pipeline captures:

| Asset | Description | Tool |
|-------|-------------|------|
| **Technique Demo GIF** | 2-3 sec loop from reel | `ffmpeg` |
| **Node Graph Screenshot** | DaVinci node graph/Fusion flow | MCP / manual |
| **Parameter Panels** | Key settings visible | Browser vision |
| **Key Frames (3-5)** | Before, during, after | Frame extraction |
| **Before/After Comparison** | Side-by-side frame | `ffmpeg hstack` |

**Storage:** `assets/{discipline}/{category}/{technique-slug}/`

---

*Part of the Videographer Knowledge Base automation suite.*  
*Generated skills follow the `videographer-{discipline}-{technique-slug}` naming convention.*