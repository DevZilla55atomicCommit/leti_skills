---
name: davinci-fairlight-post-production
description: Fairlight audio post-production and cross-page pipeline management - FVPM workflow, audio sync, color→Fusion handoff
category: davinci-resolve
tags: [fairlight, audio-post, pipeline, color-grading, vfx, lut, audio-sync, multicam]
trigger: Use when user asks about Fairlight page, audio post-production, color-to-Fusion pipeline, audio sync, or cross-page workflow management
---

# DaVinci Resolve Fairlight & Cross-Page Post-Production Pipeline

Fairlight audio workflows and cross-page pipeline management (Color → Edit → Fusion → Fairlight) for professional post-production.

## Techniques Included

### 1. FVPM (Fairlight VFX Pipeline Management)
**Video ID:** `DBjXAbVomtU` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node1: Color Correction, Node2: Fusion for Visual Effects
- **Parameters:** Param1: LUT (Look-Up Table) for color grading, Param2: FX settings for visual effects
- **Steps:**
  1. Import and organize footage in Fairlight
  2. Apply LUTs and FX in Color Correction node, then send to Fusion for VFX
- **Tags:** Color Grading, VFX, Fairlight, Post-Production

### 2. Instagram Reel Editing Techniques (Color Correction + Audio Sync)
**Video ID:** `DTdILe3DdXS` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node for Color Correction, Node for Audio Sync
- **Parameters:** Param1: Adjusting the color balance to match the outdoor lighting conditions, Param2: Synchronizing the audio with the video to ensure lip sync and proper timing
- **Steps:**
  1. Import the footage into DaVinci Resolve
  2. Apply color correction to match the outdoor lighting conditions
- **Tags:** Instagram Reel Editing, Color Correction, Audio Sync

### 3. Instagram Reel with DaVinci Resolve (Color Correction + Grading)
**Video ID:** `DOQVFcdjasb` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, Grading Node
- **Parameters:** Color Correction Node: Saturation: 0.5, Contrast: 1.2; Grading Node: Lift: 0.3, Gamma: 0.8
- **Steps:**
  1. Import footage into DaVinci Resolve
  2. Apply color correction to the footage
  3. Adjust grading to enhance contrast and saturation
- **Tags:** Instagram Reel, DaVinci Resolve, Color Correction, Grading

---

## Cross-Page Pipeline Workflows

### Color → Fusion Roundtrip (Standard VFX Pipeline)
```
EDIT PAGE (Assembly)
    ↓
COLOR PAGE (Primary Grade + LUT)
    ↓ [Send to Fusion / Right-click → "Open in Fusion"]
FUSION PAGE (VFX / Compositing / Paint / Tracking)
    ↓ [Changes auto-update in Color]
COLOR PAGE (Secondary Grade / Match Grade)
    ↓
FAIRLIGHT (Audio Mix / Dialogue / SFX / Music)
    ↓
DELIVER PAGE (Render)
```

### FVPM - Fairlight VFX Pipeline Management
**Core Concept:** Use Fairlight as the central project organizer, then branch to Color/Fusion for picture.

**Workflow:**
1. **Fairlight - Organize & Sync**
   - Import all media (video + audio)
   - Sync external audio (timecode/waveform)
   - Create timeline structure
   - Mark sync points with markers

2. **Edit - Assembly**
   - Rough cut from Fairlight timeline
   - Picture lock

3. **Color - Primary Grade**
   - Base correction (CST → Balance → LUT)
   - Create "VFX Plate" version (no creative grade)

4. **Fusion - VFX Work**
   - Receive plates from Color
   - Comp, paint, track, roto
   - Render EXR sequences back to Media Pool

5. **Color - Final Grade**
   - Import VFX renders
   - Match grade to original plates
   - Creative look + secondary corrections

6. **Fairlight - Final Mix**
   - Conform audio to picture lock
   - Dialogue edit, SFX, music
   - Loudness compliance

7. **Deliver - Export**

---

## Audio Sync Techniques

### Waveform Sync (Auto)
```
Fairlight → Select video + audio clips → Right-click → "Auto Sync Audio"
Options: Based on Waveform / Timecode / Markers
```

### Manual Sync Points
1. Find clapper/slate or distinct transient (clap, spike)
2. Place marker on video clip (M key)
3. Place marker on audio clip at same event
4. Select both → Right-click → "Sync to Markers"

### Multicam Sync
```
Edit Page → Select all angles → Right-click → "Create Multicam Clip"
Sync by: Timecode / Audio Waveform / Markers / Clip Start
```

---

## Color Grading Node Structure for VFX Pipeline

```
Node 01: CST (Input Transform)          - Camera → Working Space
Node 02: Primary Balance                - Exposure, WB, Contrast
Node 03: Creative LUT / Look            - Show LUT / Creative Grade
Node 04: VFX Plate Output (Disable)     - Clean plate for Fusion
Node 05: Secondary Corrections          - Windows, Qualifiers
Node 06: Final Trim / Output Transform  - Working → Display
```

**VFX Plate Node (Node 04):**
- Disable by default (click node number)
- Enable only when sending to Fusion
- No creative LUT - only CST + Primary Balance
- Label: "VFX_PLATE" (right-click → Node Label)

---

## Fairlight Essentials

### Track Layout Template
```
Track 1-4:   Dialogue (Boom, Lav1, Lav2, ADR)
Track 5-8:   SFX (Hard FX, Foley, Ambience, Design)
Track 9-12:  Music (Main, Alt, Stems, Score)
Track 13-14: Printmaster / Stems Out
```

### Key Fairlight Shortcuts
| Action | Shortcut |
|--------|----------|
| Play/Stop | Space |
| Loop Selection | Shift+L |
| Add Marker | M |
| Next/Prev Marker | Shift+M / Opt+M |
| Nudge +1 Frame | . (period) |
| Nudge -1 Frame | , (comma) |
| Scrub Audio | Opt+Drag playhead |
| Automation Write | W (toggle) |
| Automation Touch | T (toggle) |

### Loudness Standards
| Platform | Target | True Peak |
|----------|--------|-----------|
| YouTube | -14 LUFS | -1 dBTP |
| Netflix | -27 LKFS | -2 dBTP |
| Broadcast (ATSC) | -24 LKFS | -2 dBTP |
| Podcast | -16 LUFS | -1 dBTP |

---

## Project Organization for Pipeline

### Bin Structure
```
MASTER
├── 01_FOOTAGE
│   ├── CAMERA_A
│   ├── CAMERA_B
│   └── DRONE
├── 02_AUDIO
│   ├── PRODUCTION
│   ├── SFX
│   └── MUSIC
├── 03_VFX
│   ├── PLATES_OUT
│   └── RENDERS_IN
├── 04_PROJECT_FILES
│   ├── TIMELINES
│   └── GRADES
└── 05_DELIVERABLES
```

### Naming Convention
```
[PROJECT]_[SCENE]_[SHOT]_[VERSION]_[DEPT].[ext]
EX: MYFILM_SC01_SH005_v003_COMP.exr
    MYFILM_SC01_SH005_v003_GRADE.dpx
    MYFILM_SC01_SH005_FINAL_MIX.wav
```

---

## Skill Trigger Examples

- "How do I set up a Color → Fusion → Color roundtrip?"
- "Fairlight audio sync workflow"
- "Organize DaVinci Resolve project for VFX pipeline"
- "Loudness standards for YouTube/Netflix"
- "Multicam sync in DaVinci Resolve"
- "VFX plate preparation for Fusion"