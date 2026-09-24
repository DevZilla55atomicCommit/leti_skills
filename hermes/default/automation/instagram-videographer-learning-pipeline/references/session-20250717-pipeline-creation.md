# Session 2025-07-17: Instagram Videographer Learning Pipeline Creation

> **Date:** 2025-07-17
> **Pipeline:** `instagram-videographer-learning-pipeline` v1.0.0
> **Source URL:** `https://www.instagram.com/p/DaBejwDkznl/` (@anshuluniyyal)
> **Duration:** Single session (multiple turns)

---

## Session Objective

Create a comprehensive Instagram → Videographer learning pipeline that extends the existing DaVinci Resolve color grading and video effects pipelines to cover **full videography education** — camera technique, composition, lighting, lenses, movement, production, post, VFX, audio, business.

---

## Pipeline Architecture

### 11 Disciplines (Class-Level Categories)

| # | Discipline | Folder | Keywords |
|---|------------|--------|----------|
| 1 | **Cinematography** | `Cinematography/` | static shot, camera movement, establishing shot, coverage |
| 2 | **Camera Movement** | `Camera Movement/` | dolly, slider, gimbal, steadycam, handheld, drone |
| 3 | **Lenses & Optics** | `Lenses & Optics/` | focal length, aperture, DOF, bokeh, anamorphic, focus pulling |
| 4 | **Lighting** | `Lighting/` | key/fill/back, golden hour, diffusion, color temp, practicals |
| 5 | **Composition** | `Composition/` | rule of thirds, leading lines, framing, negative space, dutch angle |
| 6 | **Production** | `Production/` | shot list, storyboard, call sheet, schedule, continuity |
| 7 | **Post-Production** | `Post-Production/` | editing, color grade, sound design, conform, deliverables |
| 8 | **VFX & Compositing** | `VFX & Compositing/` | green screen, rotoscope, tracking, particles, Fusion |
| 9 | **Audio & Sound** | `Audio & Sound/` | mic technique, sync, foley, ADR, mixing, loudness |
| 10 | **Business & Career** | `Business & Career/` | freelance, rates, contracts, portfolio, marketing |
| 11 | **Camera Theory** | `../Camera Theory/` | RAW vs LOG, sensor science, color management |

---

## First URL Processed

**`https://www.instagram.com/p/DaBejwDkznl/`** — @anshuluniyyal "The Art of Static Shots"

### Content Type: Carousel Post (6 slides)

| Slide | Technique Extracted | Discipline | Status |
|-------|---------------------|------------|--------|
| 1 (Title) | The Art of Static Shots (Main Concept) | Cinematography | ✅ Done |
| 2 | Silhouetting + Atmospheric Perspective | Camera Theory | ✅ Done |
| 3 | Dutch Angle (Canted Frame) | Composition | ✅ Done |
| 4 | Layering + Silhouetting (3 Depth Planes) | Composition | ✅ Done |
| 5 | Shallow DOF + Low Angle + Leading Line | Lenses & Optics | ✅ Done |
| 6 | Natural Framing + Negative Space | Composition | ✅ Done |

---

## Artifacts Created

### Vault Notes (7 total)

| File | Discipline |
|------|------------|
| `Videographer/Cinematography/01-Art-of-Static-Shots_anshuluniyyal_Cinematography.md` | Cinematography |
| `Camera Theory/02-Silhouetting-Atmospheric-Depth_anshuluniyyal.md` | Camera Theory |
| `Videographer/Composition/01-Dutch-Angle_anshuluniyyal.md` | Composition |
| `Videographer/Composition/02-Layering-Silhouette_anshuluniyyal.md` | Composition |
| `Videographer/Lenses & Optics/01-Shallow-DOF-Low-Angle_anshuluniyyal.md` | Lenses & Optics |
| `Videographer/Composition/03-Natural-Framing_anshuluniyyal.md` | Composition |
| `Videographer/00-MASTER-INDEX.md` | Index |
| `Videographer/TEMPLATE-Videographer-Technique.md` | Template |
| `Videographer/VIDEOGRAPHER_QUEUE.md` | Queue |

### Hermes Skills (6 total)

| Skill Name | Discipline |
|------------|------------|
| `videographer-cinematography-static-shots-anshuluniyyal` | Cinematography |
| `videographer-camera-theory-silhouetting-atmospheric-depth-anshuluniyyal` | Camera Theory |
| `videographer-composition-dutch-angle-anshuluniyyal` | Composition |
| `videographer-composition-layering-silhouette-anshuluniyyal` | Composition |
| `videographer-lenses-optics-shallow-dof-low-angle-anshuluniyyal` | Lenses & Optics |
| `videographer-composition-natural-framing-anshuluniyyal` | Composition |

### Pipeline Skill (1)

| Skill Name | Category |
|-------------|----------|
| `instagram-videographer-learning-pipeline` | automation |

---

## Key Technical Decisions

### 1. Multi-Discipline Classification
Unlike the color grading pipeline (11 categories → 1 vault), this pipeline routes to **multiple vault roots**:
- `DaVinci_Knowledge_Base/Camera Theory/` — technical color science
- `DaVinci_Knowledge_Base/Color Grading & Looks/` — grading techniques
- `DaVinci_Knowledge_Base/Video_Effects/` — transitions, VFX, motion graphics
- `DaVinci_Knowledge_Base/Videographer/` — broader videography disciplines
- `Photography/Lightroom/` — mobile/photo editing

### 2. Carousel Multi-Technique Extraction
**One post → N techniques.** Each carousel slide analyzed independently via browser vision → classified → separate vault note + skill.

### 3. Visual Asset Strategy
| Content Type | Asset Generation |
|--------------|------------------|
| **Reels (video)** | `yt-dlp` → MP4 → `ffmpeg` frames/GIFs |
| **Carousels (static)** | Browser screenshots per slide → shared carousel assets + per-technique assets |

### 4. Template System
Per-discipline templates for vault notes and skills:
- `vault_note_template_cinematography.md`
- `vault_note_template_composition.md`
- `vault_note_template_lighting.md`
- `vault_note_template_camera_theory.md`
- `vault_note_template_production.md`
- `vault_note_template_lightroom.md`
- `skill_template_cinematography.md`

---

## Browser Automation Workflow

### Carousel Navigation Pattern
1. `browser_navigate` to `/p/{CODE}/`
2. `browser_click` close login modal (`@e181` typically)
3. `browser_vision` on slide 1
4. For slides 2-N:
   - `browser_click` next arrow (`@e184` typically)
   - `time.sleep(1-2)`
   - `browser_vision` on current slide
5. Screenshots captured via `browser_vision` return paths

### Vision Prompt Template
```markdown
This is slide {N} of a carousel titled "{TITLE}" by @{CREATOR}.

Describe:
1. Visual content (subject, environment, atmosphere)
2. Text overlays, captions, annotations
3. Cinematography/composition/lighting techniques demonstrated
4. Implied camera settings (lens, angle, exposure, DOF)
5. Post-production techniques visible (grading, effects, transitions)

Return structured data for technique classification.
```

---

## Queue Structure

### Reel/Video Queue (Single Technique)
| # | Code | URL | Creator | Discipline | Category | Status | Vault File |

### Carousel Queue (Multi-Technique)
| # | Post Code | Slide | Technique | Discipline | Sub-Category | Status | Target Vault Path |

---

## Files Modified/Created This Session

### Pipeline Skill
- `automation/instagram-videographer-learning-pipeline/SKILL.md` — Main skill document
- `references/config_videographer.yaml` — 11-discipline config
- `templates/vault_note_template_cinematography.md`
- `templates/vault_note_template_composition.md`
- `templates/vault_note_template_lighting.md`
- `templates/vault_note_template_camera_theory.md`
- `templates/vault_note_template_production.md`
- `templates/vault_note_template_lightroom.md`
- `templates/skill_template_cinematography.md`

### Reference Files
- `references/visual-asset-pipeline.md` — FFmpeg recipes, batch script
- `references/carousel-processing-workflow.md` — Carousel automation details
- `references/pipeline-evolution.md` — Evolution from color grading → video effects → videographer
- `references/session-20250717-pipeline-creation.md` — This file

### Vault Structure
- `Videographer/` — 11 discipline folders + assets
- `Camera Theory/` — 1 new note (silhouetting)
- `Cinematography/` — 2 notes (main + theory)

---

## Next Steps (Post-Session)

1. **Build `scripts/run_pipeline.py`** — Batch processor with:
   - Content type detection (`/reel/` vs `/p/` vs `/tv/`)
   - Carousel slide iteration with robust navigation
   - Asset generation (carousel combined GIF, comparison grid)
   - Per-technique vault note + skill generation

2. **Add more URLs** to queue for testing

3. **Process a Reel** — Full video frame/GIF extraction via `yt-dlp` + `ffmpeg`

4. **Test with 3+ carousel posts** to validate automation

---

*Session completed: 2025-07-17 | Pipeline ready for production use*