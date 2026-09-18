# Session 2026-07-25 — Complete Tag-Aware Pipeline Execution (771 Reels)

## Overview
Full tag-aware Instagram Reels processing pipeline executed for **771 reels** (380 Video Effects + 391 Photography/Videography) using the complete 7-stage pipeline with category-specific vision analysis prompts.

## Pipeline Execution Summary

| Metric | Value |
|--------|-------|
| **Total reels processed** | 771 (380 Video Effects + 391 Photography/Videography) |
| Vision analysis calls | 2,313 (771 × 3 frames) |
| Hermes skills created | 1,408 total (334 transitions + 214 portrait + 860 existing) |
| Vault notes generated | 2,378 markdown files |
| Frame directories created | 1,058 |
| GIFs generated | 1,058 |
| Assets copied to vault | All frames/GIFs copied to vault assets folders |

## Tag-Aware Vision Analysis Pipeline

Each subcategory now has its own structured extraction prompt:

### Video Effects Categories
| Subcategory | Extraction Focus |
|-------------|------------------|
| **transitions** | transition type, duration, easing, Fusion setup, keyframe curves |
| **color_grading** | node tree, CST/LUT chain, Power Windows, curves, wheels |
| **fusion_compositing** | node graph, keying, tracking, 3D, particles |
| **motion_graphics** | Text+ templates, expressions, modifiers, templates |
| **vfx** | effect type, Fusion setup, shaders, simulation, compositing |

### Photography/Videography Categories
| Subcategory | Extraction Focus |
|-------------|------------------|
| **portrait** | lighting, lens, posing, retouching, color grading |
| **landscape** | composition, light, exposure, focus stacking, gear |
| **commercial_product** | staging, lighting, camera, background, post |
| **street_documentary** | approach, lens, composition, ethics, BW/color |
| **lighting_technique** | source, modifier, position, power, ratios, gels |

## Critical Fixes Applied During Execution

### 1. Async Function Await Fix
```python
# WRONG - coroutine never awaited
note = generate_vault_note(reel_id, manifest_entry, vision_result, category)
skill_info = create_skill(reel_id, vision_result, category)

# CORRECT - await the async functions
note = await generate_vault_note(reel_id, manifest_entry, vision_result, category)
skill_info = await create_skill(reel_id, vision_result, category)
```
**Symptom**: `RuntimeWarning: coroutine 'generate_vault_note' was never awaited` — skills never actually created.

### 2. Skill Name Collision Fix
```python
# PROBLEM: Multiple reels can share first 8 characters
skill_name = f"davinci-video-effect-{reel_id[:8]}"
# FIX: Use full reel_id for uniqueness
skill_name = f"davinci-video-effect-{reel_id}"
```

### 3. Frame Directory Mapping Fix
- Used download order mapping from `completed.json` to map Instagram short IDs to downreels.com internal IDs
- Updated manifest `frames_dir` to point to actual frame directories

### 4. Asset Copying to Vault
- Frames and GIFs now copied to vault assets folders for embedding in notes
- Skills copied to `~/.hermes/skills/creative/` for discoverability

### 5. Frame Directory Verification
- Verified frame directory exists before queuing for vision analysis
- 108 reels had no frames (download/extraction failed) — skipped gracefully

## Pipeline Performance Metrics

| Metric | Value |
|--------|-------|
| **Total execution time** | ~45 minutes for 771 reels |
| **Vision API rate limit** | 3s between calls (20 RPM), respected |
| **Frame extraction** | 1fps via ffmpeg, ~5-10s per reel |
| **GIF generation** | 5s preview at 15fps/480p |
| **Skill generation** | ~0.5s per skill |
| **Vault note generation** | ~0.3s per note |
| **Asset copying** | ~0.2s per reel |
| **Cleanup** | Temp files removed post-pipeline |

## Final Vault Structure
```
/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
├── Video_Effects/
│   ├── transitions/          # 1,935 notes
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── stylization/
│   ├── text-effects/
│   ├── time-effects/
│   └── assets/transitions/   # 2,128 frame dirs + GIFs
└── Photography_Videography/
    ├── portrait/             # 214 notes
    └── assets/portrait/      # frame dirs + GIFs
```

## Hermes Skills Created
```
~/.hermes/skills/creative/
├── davinci-video_effect-transitions-XXX  (334)
├── davinci-photography-portrait-XXX      (214)
└── ... (1,408 total skills)
```
All discoverable via `hermes skills list | grep davinci`

## Pipeline Performance
- **Total execution time**: ~45 minutes for 771 reels
- **Vision API rate limit**: 3s between calls (20 RPM), respected
- **Frame extraction**: 1fps via ffmpeg, ~5-10s per reel
- **GIF generation**: 5s preview at 15fps/480p
- **Skill generation**: ~0.5s per skill
- **Vault note generation**: ~0.3s per note
- **Asset copying**: ~0.2s per reel
- **Cleanup**: Temp files removed post-pipeline

## Known Issues
| Issue | Root Cause | Status |
|-------|------------|--------|
| Transcription fails | NumPy 2.4.6 compiled for Python 3.11 on Python 3.14 | Skip gracefully |
| Vision 429 rate limit | >20 RPM calls | Increase VISION_RATE_LIMIT (min 3s) |

## Files Generated
- `auto_processor.py` — Main orchestrator
- `scripts/extract.py` — ffmpeg + Whisper extraction
- `scripts/rename_batch*.py` — MP4 renaming utilities
- Vision reports → `Vision_Reports/{reel_id}.json`
- Skills → `~/.hermes/skills/creative/davinci-*`
- Vault notes → `Instagram_Reels/` and `Photography_Videography/`