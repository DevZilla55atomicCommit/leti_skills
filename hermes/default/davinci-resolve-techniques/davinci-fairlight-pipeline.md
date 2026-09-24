---
name: davinci-fairlight-pipeline
description: FVPM - Fairlight VFX Pipeline Management for post-production workflows integrating Color, Fusion, and Fairlight
category: davinci-resolve
tags: [fairlight, pipeline, vfx, color-grading, post-production, audio-sync, roundtrip, project-management]
trigger: Use when user asks about Fairlight VFX pipeline, cross-page workflow management, Color→Fusion→Fairlight roundtrip, or post-production project organization
---

# DaVinci Resolve FVPM - Fairlight VFX Pipeline Management

Professional post-production pipeline management using Fairlight as the central hub, coordinating Color, Fusion, and Fairlight pages for VFX-heavy projects.

## Technique Included

### FVPM (Fairlight VFX Pipeline Management)
**Video ID:** `DBjXAbVomtU` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node1: Color Correction, Node2: Fusion for Visual Effects
- **Parameters:** Param1: LUT (Look-Up Table) for color grading, Param2: FX settings for visual effects
- **Steps:**
  1. Step 1: Import and organize footage in Fairlight
  2. Step 2: Apply LUTs and FX in Color Correction node, then send to Fusion for VFX
- **Tags:** Color Grading, VFX, Fairlight, Post-Production

---

## FVPM Pipeline Architecture

### Core Philosophy
**Fairlight as Project Hub** - Use Fairlight's superior audio sync, timeline management, and marker system as the central project organizer. Picture editorial follows audio lock.

### Page Responsibilities

| Page | Role in FVPM | Key Tasks |
|------|--------------|-----------|
| **FAIRLIGHT** | Central Hub | Media import, sync, timeline structure, markers, audio conform, final mix |
| **EDIT** | Assembly | Rough cut, pacing, story structure, select reels |
| **COLOR** | Picture Grade | Primary/secondary grade, LUT management, VFX plate prep, final grade |
| **FUSION** | VFX/Compositing | Paint, roto, tracking, comp, CG integration, title design |
| **DELIVER** | Output | Mastering, deliverables, QC |

---

## FVPM Workflow Steps

### Phase 1: Fairlight - Project Foundation
```
1. CREATE PROJECT
   └── Fairlight → New Project → Set Sample Rate (48kHz), Bit Depth (32-bit float)

2. IMPORT & ORGANIZE
   └── Media Pool → Bins: PRODUCTION_AUDIO, SFX, MUSIC, DIALOGUE, GUIDE_TRACKS
   └── Metadata: Scene, Take, Camera, Sound Roll (Fairlight reads BWF metadata)

3. SYNC PRODUCTION AUDIO
   └── Auto Sync: Timecode → Waveform → Manual (clapper)
   └── Create Compound Clips: [Video + Synced Audio] per take
   └── Verify Sync: Playhead scrub, check clapper alignment

4. BUILD TIMELINE STRUCTURE
   └── Markers: Scene, Shot, VFX, ADR, Foley, Music cues
   └── Marker Colors: Red=VFX, Blue=ADR, Green=Foley, Yellow=Music, Cyan=Notes
   └── Timeline Tracks:
       A1-A4: Dialogue (Boom, Lav1, Lav2, ADR)
       A5-A8: SFX (Hard, Foley, Amb, Design)
       A9-A12: Music (Main, Alt, Stems, Score)
       A13-A14: Printmaster L/R

5. ROUGH ASSEMBLY (Picture)
   └── Edit Page: Assemble from synced compounds
   └── Focus: Story, pacing, performance selects
   └── Lock Picture: "Picture Lock v1" marker
```

### Phase 2: Color - Grade & VFX Plates
```
1. PRIMARY GRADE (All Shots)
   └── CST: Camera → DaVinci WG Intermediate
   └── Balance: Exposure, WB, Contrast
   └── Creative LUT (Show LUT) on separate node
   └── Version: "Primary_Grade_v1"

2. VFX PLATE PREPARATION
   └── Duplicate Grade Version → "VFX_Plates"
   └── Disable Creative LUT node
   └── Keep: CST + Primary Balance only
   └── Handle: +8 to +16 frames head/tail
   └── Render: EXR 16-bit half, DWG, Full Range
   └── Naming: [PROJECT]_[SCENE]_[SHOT]_PLATE_v001.####.exr

3. GRADE NOTES FOR VFX
   └── Markers on timeline: "VFX_PLATE_RENDERED", "MATCH_GRADE_REF"
   └── Export CDL/Grade Reference: .ccc or .davinci grade
```

### Phase 3: Fusion - VFX Execution
```
1. RECEIVE PLATES
   └── Loader: EXR sequences (DWG colorspace)
   └── Set: Input Colorspace = DaVinci WG, Linearize = No (already linear)

2. VFX WORK
   ├── Paint/Cleanup → Paint Node (Clone, Reveal)
   ├── Roto/Rotopaint → Polygon/BSpline + Paint
   ├── Tracking → Planar Tracker / Camera Tracker
   ├── Comp → Merge, ChannelBoolean, ColorCorrector
   ├── CG Integration → Render3D, Lighting, Shadows
   └── Titles/GFX → Text+, 3D Text, Particles

3. COLOR SPACE MANAGEMENT
   └── Work in: DaVinci WG (Linear) or ACEScct
   └── View: sRGB/Rec.709 LUT for monitoring
   └── Output: EXR 16-bit half, DWG, no LUT baked

4. DELIVER TO COLOR
   └── Render: [PROJECT]_[SCENE]_[SHOT]_COMP_v001.####.exr
   └── Include: Alpha channel, Depth pass (if 3D), Cryptomatte
```

### Phase 4: Color - Final Grade & Conform
```
1. CONFORM VFX SHOTS
   └── Replace plate clips with comp renders
   └── Verify: Frame range, handle frames, sync
   └── Apply: Match Grade from reference

2. SECONDARY GRADE
   └── Power Windows: Face, Sky, Product
   └── Qualifiers: Skin tone, Sky replacement
   └── Tracking: Window trackers on movement

3. UNIFIED LOOK
   └── Show LUT refinement
   └── Scene-to-scene consistency
   └── HDR/SDR trim passes (if dual deliverable)

4. QC & VERSIONING
   └── Version: "Final_Grade_v1" → "Final_Grade_v2" (notes)
   └── Gallery Stills: Hero frames per scene
   └── Render: ProRes 4444 XQ / DNxHR HQX for master
```

### Phase 5: Fairlight - Final Mix
```
1. CONFORM AUDIO TO PICTURE LOCK
   └── Import: Final picture (ProRes) → Video Track
   └── Reconform: Dialogue, SFX, Music to new edit
   └── Check: Sync drift, missing handles

2. DIALOGUE EDIT
   └── Smooth: Room tone, crossfades
   └── Noise Reduce: iZotope RX / Fairlight NR (gentle)
   └── EQ/Comp: Consistency across scenes
   └── ADR: Record → Sync → Match

3. SOUND DESIGN
   ├── Hard FX: On-screen actions
   ├── Foley: Feet, cloth, props (perform to picture)
   ├── Ambience: Room tone, exteriors, perspectives
   └── Design: Sweeps, impacts, UI, magical

4. MUSIC
   ├── Score: Stem mixing (Str, Brs, Perc, Syn)
   ├── Licensed: Edit to picture, clearance
   └── Ducking: Sidechain under dialogue

5. RE-RECORDING MIX
   ├── Pre-dubs: DX, MX, FX stems
   ├── Final Mix: Balance, automation, panning
   ├── Loudness: -24 LKFS (Broadcast) / -14 LKFS (Streaming)
   └── Printmaster: L/R + Stems (DX, MX, FX, DIA)

6. QC & DELIVER
   └── Loudness Verification (ITU-R BS.1770)
   └── True Peak Check (< -2 dBTP)
   └── Phase Correlation Check
   └── Export: WAV 48k/24-bit stems + Printmaster
```

---

## Project Organization (FVPM Standard)

### Bin Structure
```
FAIRLIGHT PROJECT
├── 01_PRODUCTION_AUDIO
│   ├── PROD_DIALOGUE
│   ├── PROD_SFX
│   └── PROD_AMBIENCE
├── 02_POST_AUDIO
│   ├── ADR
│   ├── FOLEY
│   ├── SFX_DESIGN
│   └── MUSIC
├── 03_TIMELINES
│   ├── SELECTS
│   ├── ASSEMBLY
│   ├── ROUGH_CUT_v###
│   ├── FINE_CUT_v###
│   ├── PICTURE_LOCK_v###
│   └── CONFORM_v###
├── 04_VFX
│   ├── PLATES_OUT (to Fusion)
│   ├── COMPS_IN (from Fusion)
│   ├── TURNOVER_SHEETS
│   └── REFERENCE_GRADES
├── 05_COLOR
│   ├── GRADE_VERSIONS
│   ├── LUTS (Show, Creative, Technical)
│   ├── STILLS (Gallery)
│   └── MASTERS
├── 06_DELIVERABLES
│   ├── MASTERS (ProRes/DNx)
│   ├── STREAMING (H.264/HEVC)
│   ├── BROADCAST (XDCAM/IMX)
│   └── STEMS (Audio)
└── 07_PROJECT_FILES
    ├── AAF/XML/EDL
    ├── NOTES
    └── REPORTS
```

### Naming Convention
```
[PROJECT]_[DEPT]_[SCENE]_[SHOT]_[TASK]_v###[_####].ext

Examples:
MYFILM_VFX_SC01_SH005_COMP_v003.1001.exr
MYFILM_COL_SC01_SH005_GRADE_v002.dpx
MYFILM_AUD_SC01_SH005_ADR_v001.wav
MYFILM_EDL_SC01_v005.xml
```

---

## Roundtrip Protocols

### Color → Fusion → Color
```
COLOR (Grade)          FUSION (VFX)           COLOR (Conform)
─────────────────     ──────────────         ─────────────────
1. Primary Grade       1. Load Plate          1. Replace Plate
2. Create Plate Ver    2. VFX Work            2. Match Grade
   (No Creative LUT)      (DWG Linear)           (Ref Still)
3. Render EXR          3. Render Comp         3. Secondary Grade
   (DWG, 16-bit)          (DWG, 16-bit)          + Creative LUT
4. Turnover Sheet  ←→  4. Turnover Sheet  ←→  4. QC / Version
```

### Edit → Color → Edit (Conform)
```
EDIT                  COLOR                   EDIT
─────                 ─────                   ─────
1. Picture Lock       1. Grade                1. Import Grade
2. Export XML/AAF  →  2. Import XML           2. Compare/Conform
3. (Reference QT)       3. Render Master      3. Update Timeline
                           4. Export XML       4. Lock
```

---

## Communication Tools

### Turnover Sheet (Color → Fusion)
| Shot | Plate In | Plate Out | Handles | Grade Ref | Notes |
|------|----------|-----------|---------|-----------|-------|
| SC01_SH005 | 1001 | 1120 | 8/8 | v003 | Wire removal, sky replace |

### VFX Shot List (Fusion → Color)
| Shot | Comp Version | Frames | Alpha | Passes | Status |
|------|--------------|--------|-------|--------|--------|
| SC01_SH005 | v003 | 1001-1120 | Yes | Beauty, Depth, Crypto | Approved |

### Color Notes (Color → Fairlight)
| Timecode | Shot | Note | Priority |
|----------|------|------|----------|
| 01:03:12:15 | SC01_SH005 | Skin tone warm, match SC01_SH003 | High |

---

## Automation & Scripting

### Python API (DaVinci Resolve Scripting)
```python
# Example: Auto-create VFX plate version
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

# Duplicate current grade version as "VFX_Plates"
color = timeline.GetColorPage()
grade = color.GetCurrentGrade()
grade.Duplicate("VFX_Plates")
# Disable creative LUT node (index varies)
```

### Keyboard Shortcuts (Custom for FVPM)
| Action | Shortcut | Context |
|--------|----------|---------|
| Send to Fusion | F8 | Color/Edit |
| Open in Color | F7 | Edit/Fairlight |
| Render VFX Plate | Shift+F8 | Color |
| Conform VFX | Shift+F7 | Color |
| Sync Audio | Ctrl+Shift+S | Fairlight |
| Create Marker | M | All Pages |
| Next Marker | Shift+M | All Pages |

---

## Skill Trigger Examples

- "FVPM workflow DaVinci Resolve"
- "Fairlight VFX pipeline management"
- "Color to Fusion roundtrip"
- "VFX plate preparation DaVinci"
- "Post production pipeline Fairlight hub"
- "Conform VFX shots after grade"
- "Turnover sheet template VFX"
- "Project organization DaVinci Resolve"
- "Audio sync Fairlight workflow"
- "Mastering deliverables DaVinci"