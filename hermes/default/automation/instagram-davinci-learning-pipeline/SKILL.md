---
name: instagram-davinci-learning-pipeline
description: "Unified automation skill for extracting DaVinci Resolve color grading techniques from Instagram Reels and building a structured knowledge base."
version: 1.6.1
author: Hermes
metadata:
  hermes:
    tags: [Instagram, DaVinci Resolve, Color Grading, Automation, Learning, Vault, Skills]
---

# Instagram → DaVinci Learning Pipeline

> **Unified automation skill** for extracting DaVinci Resolve color grading techniques from Instagram Reels and building a structured knowledge base.

---

## 🎯 What This Does

```text
Instagram URLs (RTF/CSV/TXT)
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│  INSTAGRAM-DAVINCI-LEARNING-PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Parse & Deduplicate    →  Remove already-processed URLs    │
│  2. Availability Check     →  Filter private/deleted reels     │
│  3. Content Extraction     →  Browser + Vision analysis        │
│  4. Technique Classification →  Auto-categorize by keywords    │
│  5. Skill Generation       →  ~/.hermes/skills/creative/       │
│  6. Vault Note Creation    →  DaVinci_Knowledge_Base/          │
│  7. Queue Management       →  Done / Skipped / Camera Theory   │
│  8. Export Regeneration    →  JSON/CSV/HTML/Architecture      │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
Structured Knowledge Base + Interactive Diagram
```

---

## 🚀 Quick Start

```bash
# From terminal (Hermes CLI)
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf

# Dry run to preview classifications
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --dry-run

# Filter to specific creator
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --filter-creator c.vladmanea

# Retry failed URLs
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --retry-failed
```

---

## 📥 Supported Input Formats

| Format | Description | Example |
|--------|-------------|---------|
| **RTF** | Rich Text Format (exported from Notes, Word) | `urls.rtf` |
| **CSV** | `url,creator,notes,priority` headers | `urls.csv` |
| **JSON** | Array of objects with url, creator, notes | `urls.json` |
| **TXT** | Plain text, one URL per line | `urls.txt` |

### RTF Example (from Apple Notes)
```rtf
{\rtf1\ansi https://www.instagram.com/reel/DKBME3_g_jD/ @gablasc White Balance Linear Mode}
{\rtf1\ansi https://www.instagram.com/reel/DKIGX5GtJjk/ @hudson_twarren Color Density HSV}
```

### CSV Example
```csv
url,creator,notes,priority
https://www.instagram.com/reel/DKBME3_g_jD/,gablasc,"White Balance Linear Mode: Luma Mix=0",High
https://www.instagram.com/reel/DKIGX5GtJjk/,hudson_twarren,"Color Density via HSV Curves",High
```

---

## ⚙️ Configuration

Edit `references/config.yaml` to customize:

```yaml
# Processing
batch_size: 10
max_concurrent: 3

# Categories with keyword matching
categories:
  - name: "Color Correction Fundamentals"
    keywords: ["white balance", "exposure", "cst", "gamut", "primary", "log"]
    folder: "Color Correction Fundamentals"
  - name: "Creative Grading & Looks"
    keywords: ["look", "cinematic", "teal", "orange", "film", "lut", "halation", "glow", "kodak", "fujifilm"]
    folder: "Creative Grading & Looks"
  - name: "Camera Theory"
    keywords: ["raw vs log", "dynamic range", "sensor", "bit depth", "camera theory", "log curve", "gamma curve", "exposure latitude", "highlight rolloff", "noise floor"]
    folder: "Camera Theory"
  - name: "Masking & Windows"
    keywords: ["power window", "mask", "qualifier", "magic mask", "tracking", "isolation"]
    folder: "Masking & Power Windows"
  - name: "Node Structures & Templates"
    keywords: ["node", "parallel", "serial", "layer mixer", "shared node", "pipeline"]
    folder: "Node Structures & Templates"
  - name: "DaVinci Resolve 20/21"
    keywords: ["color compressor", "depth map", "relight", "magic mask", "face refinement"]
    folder: "DaVinci Resolve 20"
  - name: "S-Log3 / Sony Workflows"
    keywords: ["s-log3", "slog3", "sony", "s-gamut", "a7s", "fx3", "venice"]
    folder: "Color Grading & Looks/S-Log3"
  - name: "Apple Log / iPhone"
    keywords: ["apple log", "apple log 2", "pro res", "prores", "iphone"]
    folder: "Color Grading & Looks/Apple Log 2"
  - name: "Skin Tones"
    keywords: ["skin tone", "face refinement", "vectorscope skin tone"]
    folder: "Color Grading & Looks/Skin Tones"
  - name: "Film Emulation"
    keywords: ["kodak 2383", "2383", "film emulation", "cineon", "logc"]
    folder: "Color Grading & Looks/Kodak 2383"
  - name: "Photography / Lightroom / Mobile Editing"
    keywords: ["lightroom mobile", "lr mobile", "lightroom tutorial", "point curve", "tone curve", "rgb curve", "color grading panel", "hsl panel", "calibration panel", "masking", "adaptive preset", "creative profile", "magimir", "snapseed", "vsco", "picsart", "facetune", "airbrush", "meitu", "beautyplus", "mobile editing", "iphone editing", "mobile photo editing", "photo editing curves", "mobile curves"]
    folder: "Photography/Lightroom"

# Skip patterns (promo, meme, non-DaVinci, etc.)
skip_patterns:
  - "promo"
  - "preset pack"
  - "lightroom"
  - "meme"
  - "magimir"
  - "mobile"
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
  - "preset pack"
  - "lut pack"
  - "buy now"
  - "link in bio"
  - "discount"
  - "sale"
  - "meme"
  - "joke"
  - "funny"
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
  - knowledge_base_export.json
  - knowledge_base_export.csv
  - skills_export.json
  - skills_export.csv
  - ARCHITECTURE_DIAGRAM.md
  - ARCHITECTURE_DIAGRAM_INTERACTIVE.html
```

---

## 📊 Output Artifacts

### 1. Hermes Skills (`~/.hermes/skills/creative/`)

```bash
davinci-resolve-color-correction-fundamentals-white-balance-linear-mode-gablasc/
├── SKILL.md          # Full skill with frontmatter
```

### 2. Vault Notes (`DaVinci_Knowledge_Base/`)

```text
Color Correction Fundamentals/
├── 087-White-Balance-Linear-Mode_Gablasc_Luma-Mix-Zero.md
Creative Grading & Looks/
├── 092-Cinematic-Glow_Mansour-Melouli_Glow-OFX-Soft-Light.md
Camera Theory/                    # NEW category!
├── 001-RAW-vs-LOG_Fundamentals.md
```

### 2b. Photography Vault Notes (`Photography/Lightroom/`) — *NEW*

```text
Photography/Lightroom/
├── 00-MASTER-INDEX.md
├── TEMPLATE-Technique.md
├── 01-Tone-Curve-Mastery_Magimir_Point-Curve-RGB.md
├── 02-Split-Toning_MobileEditor_Teal-Orange.md
```

### References Added in This Session
- `references/vision-analysis-phase2.md` — Phase 2 vision analysis protocol (20 RPM limit, frame sampling, prompts, output structure, clustering keywords, checkpoint/resume)

### 3. Queue Tracking (`Instagram_Learning_Queue.md`)

```markdown
| #  | URL                                    | Creator    | Status          | Reason                                     |
|----|----------------------------------------|------------|-----------------|--------------------------------------------|
| 86 | instagram.com/reel/DKOnyyEAApg/        | @saarvendra | ⏭️ Skipped (Not DaVinci) | Creative art/transition reel — no color grading tutorial |
| 87 | instagram.com/reel/DKBME3_g_jD/        | @gablasc   | ✅ Done         |                                            |
| 92 | instagram.com/reel/DJ7Ru81oM1W/        | @c.vladmanea| ⏭️ Skipped (Promo) | 50+ Page Color Grading Guide **promo video** (not the guide itself) |
| 118| instagram.com/reel/DHJ3KJOut4J/        | @jacob.wagler| ⏭️ Skipped (Promo) | Cinematic **Preset Pack promo** — marketing, not technique |
| 129| instagram.com/reel/DFgheS3ylWy/        | @c.vladmanea| ⏭️ Skipped (Promo / Not DaVinci) | **Lightroom Masterclass promo** — Lightroom, not DaVinci |
| 133| instagram.com/reel/DFX7MojPCHT/        | @filmsbychristian| ⏭️ Skipped (Not Educational) | Meme/joke reel — humor content |
| 134| instagram.com/p/DFkhTiNpo7f/           | @moizxmhd | ⏭️ Skipped (Not DaVinci) | Lightroom Vintage Pastel tutorial — mobile Lightroom |
| 135| instagram.com/reel/DFgheS3ylWy/        | @lowlight.co| 📚 Camera Theory | Reclassified to Camera Theory → vault note created |
```

**Explanation of Skipped Status**:  
- **8 skipped items** include duplicates across the main queue table and the completed log.  
- Items are categorized as **Promo/Marketing**, **Not DaVinci (Lightroom/Other)**, **Creative/Art (Non‑tutorial)**, or **Not Educational (Meme)**.  
- Each entry lists the specific reason for skipping, helping you understand why it was excluded from processing.

---

## 🏷️ Auto-Categorization

| Category | Keywords | Vault Folder |
|----------|----------|--------------|
| **Color Correction** | white balance, exposure, cst, gamut, primary, log, parade, vectorscope | `Color Correction Fundamentals/` |
| **Creative Grading** | look, cinematic, teal, orange, film, lut, halation, glow, kodak, fujifilm | `Creative Grading & Looks/` |
| **Camera Theory** | raw, log, sensor, dynamic range, iso, transfer function, braw, prores raw | `Camera Theory/` |
| **Masking & Windows** | power window, mask, qualifier, magic mask, tracking, isolation | `Masking & Power Windows/` |
| **Node Structures** | node, parallel, serial, layer mixer, shared node, pipeline | `Node Structures & Templates/` |
| **Resolve 20/21** | color compressor, depth map, relight, magic mask, face refinement | `DaVinci Resolve 20/` |
| **S-Log3 / Sony** | s-log3, slog3, sony, s-gamut, a7s, fx3, venice | `Color Grading & Looks/S-Log3/` |
| **Apple Log** | apple log, apple log 2, pro res, prores, iphone | `Color Grading & Looks/Apple Log 2/` |
| **Skin Tones** | skin tone, face refinement, vectorscope skin tone | `Color Grading & Looks/Skin Tones/` |
| **Film Emulation** | kodak 2383, 2383, film emulation, cineon, logc | `Color Grading & Looks/Kodak 2383/` |

### **Photography / Lightroom / Mobile Editing** (NEW)
| Category | Keywords | Vault Folder |
|----------|----------|--------------|
| **Lightroom Mobile / Desktop** | lightroom mobile, lr mobile, lightroom tutorial, point curve, tone curve, rgb curve, color grading panel, hsl panel, calibration panel, masking, adaptive preset, creative profile | `Photography/Lightroom/` |
| **Mobile Photo Editing (Non-LR)** | magimir, snapseed, vsco, picsart, facetune, airbrush, meitu, beautyplus, mobile editing, iphone editing, mobile photo editing, photo editing curves, mobile curves | `Photography/Lightroom/` |
| **Photo Color Theory** | tone curve, point curve, rgb curves, color curves, split toning, color grading photo, subtractive saturation, hue vs saturation, color density | `Photography/Lightroom/` |

### Skip Auto-Detection
- Promo/marketing reels → ⏭️ Skipped (Promo)
- **Lightroom/Photoshop content** → 📸 **Route to Photography/Lightroom/** (not skipped)
- Memes/jokes → ⏭️ Skipped (Not Educational)
- **General camera theory** → 📚 **Camera Theory/** (reclassified, not skipped)
- Mobile app editing (Magimir, Snapseed, VSCO, etc.) → 📸 **Route to Photography/Lightroom/**

### Skip Auto-Detection Patterns (Enhanced)
```yaml
skip_patterns:
  - "promo"
  - "preset pack"
  - "lightroom"          # Note: now routes to Photography/Lightroom/ instead of skip
  - "mobile"             # Note: now routes to Photography/Lightroom/ instead of skip
  - "magimir"            # Mobile app
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
  - "parody"
  - "comment.*tutorial"
  - "guide.*promo"
  - "masterclass promo"
  - "preset pack"
  - "lut pack"
  - "buy now"
  - "link in bio"
  - "discount"
  - "sale"
  - "meme"
  - "joke"
  - "funny"
  - "magimir"            # Specific mobile app
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
```

### Camera Theory Keywords (Reclassify, Don't Skip)
```yaml
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
```

### Lightroom/Mobile Editing Keywords (Route to Photography/Lightroom/)
```yaml
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
```

---

## 🔧 Advanced Usage

### Resume Interrupted Run
```bash
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --resume
```

### Custom Batch Size
```bash
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --batch-size 5
```

### Force Reprocess (ignore dedup)
```bash
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --force
```

### Custom Config
```bash
hermes skill run instagram-davinci-learning-pipeline --input urls.rtf --config my-config.yaml
```

---

## 📁 Skill Structure

```text
instagram-davinci-learning-pipeline/
├── SKILL.md                          # This file
├── references/
│   ├── config.yaml                   # Main configuration
│   ├── skipped-queue-patterns.md     # Queue status patterns
│   └── skip-pattern-examples.md      # Real-world skip cases (Magimir, Lightroom promos, etc.)
├── templates/
│   ├── vault_note_template.md        # Vault markdown template
│   ├── vault_note_template_lightroom.md  # Lightroom template
│   ├── skill_template.md             # Hermes skill template
│   └── skill_template_lightroom.md   # Lightroom skill template
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

---

## 📝 Extending the Pipeline

### Add New Category
1. Edit `references/config.yaml` → add to `categories:`
2. Add keywords for auto-classification
3. Run pipeline — new folder created automatically

### Add New Skip Pattern
```yaml
skip_patterns:
  - "your new pattern"
```
**Real-world examples**: See `references/skip-pattern-examples.md` for documented cases (Magimir mobile app, Lightroom promos, meme content, camera theory reclassification) with vision analysis signals and profile-level heuristics.

### Custom Vault Template
Edit `templates/vault_note_template.md` — uses `{VARIABLE}` substitution.

### Custom Skill Template
Edit `templates/skill_template.md` — controls Hermes skill frontmatter.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No URLs extracted" | Check input format; RTF needs `textutil` on macOS |
| "Skill already exists" | Use `--force` or delete old skill first |
| "Browser timeout" | Increase `timeout_seconds` in config |
| "Classification wrong" | Add more keywords to category in config |
| "Export diagram too large" | Use "Folders Only" view in HTML |
| **Auto-compression never triggers / session grows past 500+ messages** | **Check `auxiliary.compression.base_url` matches `provider`** — model must exist at that endpoint. Common pitfall: `provider: nvidia` with `base_url: http://127.0.0.1:11434/v1` (local Ollama) but model only exists on NVIDIA API. Fix: remove `base_url` to use provider default, or use local model `qwen3.5-4b-compress` with `provider: ollama-launch`. See `references/auto-compression-troubleshooting.md`. |

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-12 | Initial release — full pipeline with 11 categories, Camera Theory, interactive HTML |
| 1.1.0 | 2025-07-14 | Added real-world skip pattern examples (Magimir app, Lightroom promos, memes, camera theory reclassification) with vision analysis signals |
| 1.2.0 | 2025-07-14 | Added Photography/Lightroom category for mobile editing (Magimir, Snapseed, VSCO, etc.) and Lightroom tutorials; Camera Theory reclassification; enhanced skip patterns |
| 1.3.0 | 2025-07-14 | Processed 161 unique URLs from user's Block 4 file; 59 available (36.6% hit rate); 34+ vault notes created; 18 skills generated; new Photography/Lightroom folder with 2 techniques; Node Structures & Templates (6) and Masking & Power Windows (4) folders created; all category indexes updated |
| 1.4.0 | 2025-07-15 | **Video Effects pipeline extension** — Added 7 Video Effects categories to config.yaml; created vault_note_template_video_effect.md and skill_template_video_effect.md; added Video Effects skip/route patterns to skip-pattern-examples.md; created implementation plan and handoffs in vault; ready for first effect (@art3.studi0 Pro Cut Out Transition) |
| 1.5.0 | 2025-07-15 | **First Video Effects URL processed end-to-end** — @art3.studi0 "Pro Cut Out Transition" (DaxUaKYuhb0); yt-dlp + Chrome cookies bypassed login wall; ffmpeg extracted 242 frames + GIFs; vault note + Hermes skill created; visual assets captured (demo GIF, transition loop, before/during/after frames, comparison); pipeline validated for Transitions category |
| 1.6.1 | 2025-07-17 | **Auto-compression fix documented** — Added troubleshooting entry for compression model endpoint mismatch (provider: nvidia with base_url pointing to local Ollama). Session 20260715_203740_bc494a grew to 1,014 messages unchecked. Fix: remove base_url to use NVIDIA API directly, or switch to local qwen3.5-4b-compress. Reference: `references/auto-compression-troubleshooting.md`. |
| 1.6.0 | 2025-07-15 | **Full batch processing complete** — 350/360 Instagram URLs processed (10 posts skipped); 12 Hermes skills generated with bundled assets (demo GIF, transition loop, before/during/after frames, before/after comparison); 557 vault notes created across 4 categories (Transitions, Compositing, Motion Graphics, Stylization); automated batch processor `scripts/process_batch.py` production-ready with Chrome cookie auth, MP4 auto-cleanup, visual asset extraction; 12 Hermes skills created under `~/.hermes/skills/video-effects/` |

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

## 📁 Support Files Added This Session

| File | Purpose |
|------|---------|
| `references/config.yaml` | **PATCHED** — Added 7 Video Effects categories (Transitions, Compositing, Motion Graphics, VFX, Text Effects, Stylization, Time Effects) |
| `references/skip-pattern-examples.md` | **PATCHED** — Added Video Effects positive signals, routing rules, and detection heuristics |
| `templates/vault_note_template_video_effect.md` | **NEW** — Detailed vault note template for video effects (with node graph, visual assets table) |
| `templates/skill_template_video_effect.md` | **NEW** — Hermes skill template for video effects (with GIF, frames, DaVinci page, effect type) |

---

## 📋 Implementation Plan

> **See vault:** `DaVinci_Knowledge_Base/Video_Effects/VIDEO_EFFECTS_PIPELINE_PLAN.md`
> **Handoffs:** `DaVinci_Knowledge_Base/Video_Effects/IMPLEMENTATION_HANDOFFS.md`

---

## 🔧 Session 20260715_203740_bc494a — Auto-Compression Failure & Pipeline Resumption Notes

**Session ID:** `20260715_203740_bc494a` (1,014 messages)

### What Happened
- Session processed 360 Instagram URLs for Video Effects pipeline (extension of Color Grading pipeline)
- Batch processing reached 251/253 URLs processed, then a background process failed at index 50 (`scripts/run_pipeline.py --batch 10 --start 50` — file not found in Videographer folder)
- **Auto-compression did NOT trigger** despite 1,014 messages (2x the `hygiene_hard_message_limit: 500`)

### Root Cause: Misconfigured Auxiliary Compression Model
```yaml
# ~/.hermes/config.yaml (global) and ~/.hermes/profiles/default/config.yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1   # LOCAL OLLAMA — MODEL NOT PRESENT
    enabled: true
    threshold: 0.7
```

**Problem:** Config points to local Ollama for `nemotron-mini-4b-instruct`, but that model doesn't exist locally (only `qwen3.5-4b-compress` is pulled). When compression triggered, it tried to call a non-existent local model → failed silently → `abort_on_summary_failure: true` prevented retry → session grew unchecked.

### Fix Applied (config.yaml)
```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: https://integrate.api.nvidia.com/v1  # NVIDIA API directly
    # removed extra_body, timeout, etc. — use defaults
```

**Verified:** `nvidia/nemotron-mini-4b-instruct` IS available on NVIDIA API (confirmed via `/v1/models`).

### Remaining Work (Video Effects Pipeline)
- **8 reels at indices 50-57** still need processing: `python3 scripts/process_batch.py --batch 10 --start 50`
- Template files created: `vault_note_template_video_effect.md`, `skill_template_video_effect.md`
- Reference files created: `video-effects-pipeline.md`, updated `skip-pattern-examples.md`

---

# 🔧 Session 20260721 — Phase 2 Vision Analysis Pipeline (Current)

**Context:** Massive Instagram Reels → DaVinci Resolve knowledge extraction pipeline. Dual Mac (Mac Mini M4 16GB + MBP), Samsung LED SSD (120GB, 70GB free) primary, PNY128GB overflow.

### Phase Status
| Phase | Status | Details |
|-------|--------|---------|
| **Phase 1: Content Processing** | ✅ Complete | 1,156/2,818 videos processed; 1,156 frame dirs (1fps); 2,312 full-duration GIFs (fps=8, scale=640, 45.9 GB); 2,312 Whisper transcripts; 1,156 analysis JSONs |
| **Phase 2a: Vision Analysis — Color Grading (336 videos)** | 🔄 In Progress | 8/336 videos analyzed; 5 frames/video (key frames: 0001, 0020, 0050, 0080, last); **Rate limit: 20 RPM** (vision_analyze) |
| Phase 2b: DaVinci Tricks (224) | ⏳ Pending | |
| Phase 2c: Cinematic (156) | ⏳ Pending | |
| Phase 2d: Drone (114) | ⏳ Pending | |
| Phase 2e: Gimbal Moves (474) | ⏳ Pending | |
| Phase 2f: Ideas for Shooting (796) | ⏳ Pending | |
| Phase 2g: Other DaVinci (~30) | ⏳ Pending | |

### Rate Limiting Protocol (CRITICAL)
- **Vision API: 20 RPM maximum** — hard limit enforced by provider
- Pace vision_analyze calls: minimum 3 seconds between calls
- If 429 received: exponential backoff (30s → 60s → 120s → 240s → 480s)
- **Do NOT batch vision calls** — they count individually against RPM
- Batch terminal/file operations freely; only vision_analyze is rate-limited

### Frame Sampling Strategy
- Extract key frames only (not all 1fps frames)
- Target: frame_0001, frame_0020, frame_0050, frame_0080, frame_last
- Skip talking-head/title frames (detected via vision analysis)
- Max 5 frames/video → ~1,680 vision calls for Color Grading collection

### Storage Layout
```
/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/
├── CONTENT_PROCESSING/
│   ├── frames/           # 1,156 video frame dirs
│   ├── gifs/             # 2,312 full-duration GIFs
│   ├── transcripts/      # 2,312 Whisper transcripts
│   └── analysis/         # 1,156 analysis JSONs
├── MASTER_INDEX_FIXED.json
└── COLLECTIONS_AND_URLS_CLEAN.md
```

### Constraints & Preferences (from user)
- Mac Mini M4 16GB — **no heavy local vision models** (ollama llava exceeds RAM)
- Use assistant's built-in vision model via `vision_analyze` tool
- Samsung LED external SSD primary; PNY128GB emergency overflow
- Instagram rate limits: max 2 concurrent downloads, exponential backoff (30s→60s→120s→240s→480s)
- Resume-safe: `--continue --no-overwrites` on yt-dlp
- **No premature "complete" claims** — only report done when actually done
- Batch size: 10 videos for safe tracking
- GIFs must be full technique duration (fps=8, scale=640, full video length)
- 40 RPM API limit sensitive → vision at 20 RPM
- Detailed pipeline docs, root-cause diagnosis, professional plans, thorough error handling
- Class-level umbrella skills with refs/templates/scripts over narrow skills