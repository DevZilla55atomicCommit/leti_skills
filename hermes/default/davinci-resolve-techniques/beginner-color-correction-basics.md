---
name: beginner-color-correction-basics
description: Foundational color correction workflow in DaVinci Resolve — primary balance, white balance, exposure, contrast, and saturation using Color Wheels, Curves, and Parade/Vectorscope/Waveform scopes. Essential first step before any creative grading.
trigger: User starting color correction, needs primary balance, fixing exposure/WB, or learning scope-based correction
category: davinci-resolve-color-grading
tags:
  - color correction
  - beginner
  - primary balance
  - white balance
  - exposure
  - scopes
  - parade
  - vectorscope
  - waveform
  - color wheels
parameters:
  - name: exposure_target
    description: Waveform IRE targets for balanced image
    default: "Shadows 15-25, Midtones 40-55, Highlights 70-90"
    type: string
  - name: white_balance_method
    description: WB technique using scopes
    default: "Parade RGB alignment + Vectorscope skin tone line"
    type: string
  - name: contrast_pivot
    description: Contrast pivot point for natural look
    default: "0.45-0.55 (mid-gray)"
    type: string
  - name: saturation_base
    description: Base saturation after correction
    default: "90-100% (slight desat for log)"
    type: string
steps:
  - step: "Scopes Setup: Open Parade (RGB), Waveform (Luma), Vectorscope (YUV) — dock all three"
  - step: "Node 1 - Primary Balance (Color Wheels): Lift/Gamma/Gain to set black/white points using Waveform"
  - step: "Node 1 - White Balance: Offset wheel or Temp/Tint to align Parade RGB channels in neutrals"
  - step: "Node 1 - Saturation: Global Sat 90-100% (log footage often 100-110%)"
  - step: "Node 2 - Contrast/Density (Curves): Gentle S-curve or Luma curve midtone lift for density"
  - step: "Node 3 - Saturation Refinement (Curves): Hue vs Sat — protect skin, desat problem colors"
  - step: "Verify: Parade balanced, Waveform 15-90 IRE, Vectorscope skin on line, no clipping"
difficulty: beginner
resolve_page: Color
node_graph_type: serial
key_nodes:
  - Color Wheels (Primary: Lift, Gamma, Gain, Offset)
  - Curves (Luma Contrast, Hue vs Sat)
  - Parade RGB Scope
  - Waveform Luma Scope
  - Vectorscope YUV
source_techniques:
  - video_id: DBsxmNLS1Lz
    technique_name: Instagram Reel Color Grading with DaVinci Resolve
    tags: [Color Grading, Instagram Reel, DaVinci Resolve]
  - video_id: C-rvS38CGHI
    technique_name: Color Correction and Grading in DaVinci Resolve
    tags: [Color Grading, DaVinci Resolve Tutorial]
  - video_id: DGBm_L7SqNS
    technique_name: Casual Color Grading
    tags: [color grading, Instagram Reel, Casual Photography]
  - video_id: DKz0aPLuo31
    technique_name: Instagram Reel DKz0aPLuo31 - DaVinci Resolve Technique (Color Correction + LUT)
    tags: [Color Correction, LUT, DaVinci Resolve, Instagram Reel]
  - video_id: DNNWY5RzE3R
    technique_name: Instagram Reel DNNWY5RzE3R - DaVinci Resolve Technique (Color Correction + LUT)
    tags: [Color Correction, LUT Application, Instagram Reel Editing]
---

# Beginner Color Correction Basics

The essential primary correction workflow — fix exposure, white balance, contrast, saturation **before** any creative grade. Scope-driven, node-based, repeatable.

## When to Use
- First node on every clip
- Log footage normalization (S-Log, V-Log, C-Log, BRAW)
- Mixed lighting correction
- Matching cameras
- Foundation for all creative grades

---

## The Golden Rule
> **Correct first, create second.** A bad primary makes every creative node fight you.

---

## Scope Setup (Do This First)

**Open & Dock Three Scopes**:
| Scope | What It Shows | Primary Use |
|-------|---------------|-------------|
| **Parade RGB** | R/G/B channels side-by-side | White balance, channel clipping |
| **Waveform (Luma)** | Brightness 0-1023 (or 0-100 IRE) | Exposure, black/white points |
| **Vectorscope YUV** | Hue/Saturation wheel | Skin tone line, color cast, saturation |

**Layout**: Parade left, Waveform center, Vectorscope right — always visible.

---

## Node 1: Primary Correction (Color Wheels)

### Step 1: Set Black Point (Lift)
**Scope**: Waveform (Luma)
- **Target**: Shadows at **15-25 IRE** (not 0 — crushed loses detail)
- **Action**: Lower **Lift** until darkest shadows hit 15-20 IRE
- **Check**: Parade — all three channels should hit same low point

### Step 2: Set White Point (Gain)
**Scope**: Waveform (Luma)
- **Target**: Highlights at **70-90 IRE** (90 = bright, 70 = moody)
- **Action**: Raise **Gain** until brightest important detail hits target
- **Check**: Parade — no channel clipping at 1023/100 IRE

### Step 3: Set Midtone Contrast (Gamma)
**Scope**: Waveform (Luma)
- **Target**: Midtones (skin, gray cards) at **40-55 IRE**
- **Action**: Adjust **Gamma** — lift for brighter, lower for moodier
- **Pivot**: Keep at **0.50** (center) unless intentional

### Step 4: White Balance (Offset / Temp-Tint)
**Scope**: **Parade RGB** (most accurate) + **Vectorscope**

**Method A: Parade Alignment (Technical)**
- Find neutral reference (gray card, white wall, shadow)
- Adjust **Offset** (or Temp/Tint) until **R=G=B** on Parade at that region
- **Offset** = global shift; **Temp/Tint** = perceptual

**Method B: Vectorscope Skin Tone (Perceptual)**
- Find skin in frame
- Adjust **Temp/Tint** until skin falls on **Skin Tone Line** (11 o'clock / ~Flesh tone)
- **Parade check**: R > G > B for healthy skin (by ~10-20%)

> **Pro Tip**: Use **Offset wheel** for WB — it's a pure RGB shift. Temp/Tint is perceptual and can skew.

### Step 5: Global Saturation
**Scope**: Vectorscope (distance from center)
- **Rec.709 footage**: **90-100%**
- **Log footage**: **100-110%** (log desaturates)
- **Creative intent**: 85% = muted/film, 110% = pop/social

---

## Node 2: Contrast & Density (Curves)

### Option A: Luma Curve (Contrast)
```
Input:  0.0 ───┐
         0.25 ──┤   ▲  (gentle S)
         0.50 ──┼───┤
         0.75 ──┤   ▼
         1.0 ───┘
```
- **Anchor**: 0.0 and 1.0 fixed
- **Shadows (0.25)**: Pull down slightly (-0.02 to -0.05)
- **Highlights (0.75)**: Push up slightly (+0.02 to +0.05)
- **Result**: Natural contrast boost, no crushing

### Option B: Luma Curve (Midtone Density — "Filmic")
```
Input:  0.0 ───┐
         0.50 ──┼───▲  (lift midtones +0.03 to +0.06)
         1.0 ───┘
```
- **Only move midpoint (0.5)** up
- **Shadows/Highlights fixed**
- **Result**: "Thick" midtones, film-like density

> **From DBsxmNLS1Lz / C-rvS38CGHI**: Basic correction uses Color Wheels + LUTs. Curves add "density."

---

## Node 3: Saturation Refinement (Hue vs Sat Curve)

**Purpose**: Fix oversaturated colors, protect skin, creative desat.

**Common Adjustments**:
| Hue Region | Adjustment | Why |
|------------|------------|-----|
| **Skin (25-45°)** | -°)** | **-5% to -10%** | Prevent orange oversat |
| **Greens (100-140°)** | **-10% to -20%** | Digital green often toxic |
| **Blues (200-240°)** | **-5% to -10%** | Sky/noise control |
| **Reds (0-20°, 340-360°)** | **0 to +5%** | Pop lips/accents |
| **Global Low Sat** | **Sat vs Sat: compress <0.2** | Clean noise floor |

**Tool**: Curves → **Hue vs Sat** (or **Hue vs Hue** for hue shifts)

---

## Verification Checklist (Before Creative Grade)

| Check | Scope | Pass Criteria |
|-------|-------|---------------|
| **Blacks not crushed** | Waveform | Lowest > 10 IRE |
| **Highlights not clipped** | Waveform/Parade | Highest < 95 IRE / 1000 code |
| **Neutrals neutral** | Parade | R≈G≈B on gray/white |
| **Skin on line** | Vectorscope | Skin cluster on 11 o'clock line |
| **No color cast** | Parade | Shadows R=G=B, Highlights R=G=B |
| **Legal levels** | Waveform | 16-235 (video) or 0-1023 (full) |

---

## Common Log Footage Baselines

| Camera / Log | Node 1 Start (Lift/Gamma/Gain) | Sat | Node 2 |
|--------------|--------------------------------|-----|--------|
| **Sony S-Log3** | Lift +0.15, Gamma +0.1, Gain -0.05 | 110% | CST: S-Log3/S-Gamut3 → Rec.709 |
| **Panasonic V-Log** | Lift +0.1, Gamma 0, Gain 0 | 105% | CST: V-Log/V-Gamut → Rec.709 |
| **Canon C-Log3** | Lift +0.08, Gamma +0.05, Gain 0 | 105% | CST: C-Log3/Cinema Gamut → Rec.709 |
| **Blackmagic BRAW** | Project Color Science handles | 100% | Usually none needed |
| **DJI D-Log** | Lift +0.12, Gamma +0.08, Gain -0.03 | 110% | CST or LUT |

> **Best Practice**: Use **Color Space Transform (CST)** or **Color Management** instead of manual log→Rec709. More accurate, consistent.

---

## Source Techniques Summary

| Technique | Workflow |
|-----------|----------|
| **DBsxmNLS1Lz** | Import → Color Wheels + LUTs |
| **C-rvS38CGHI** | White Balance Shift → Contrast Adjustment → LUTs |
| **DGBm_L7SqNS** | Basic Color Correction Node (Sat 100%, Contrast 50%, Temp 6000K) |
| **DKz0aPLuo31** | Color Correction Node → LUT Mapping Node |
| **DNNWY5RzE3R** | Color Correction Node → Grading Node → LUT Application |

---

## Keyboard Shortcuts (Color Page)
| Action | Shortcut |
|--------|----------|
| **Add Serial Node** | `Opt+S` / `Alt+S` |
| **Add Parallel Node** | `Opt+P` / `Alt+P` |
| **Add Layer Node** | `Opt+L` / `Alt+L` |
| **Disable Node** | `D` (toggle) |
| **Full Screen Viewer** | `F` |
| **Scopes Toggle** | `Shift+W` (Waveform), `Shift+P` (Parade), `Shift+V` (Vector) |

---

## Related Skills
- `teal-orange-cinematic-grade` — creative grade on corrected base
- `skin-tone-portrait-grade` — skin-specific refinement
- `golden-hour-atmospheric-grade` — landscape correction
- `social-media-sharpening-export` — final delivery
- `hdr-social-media-grade` — HDR correction workflow
- `fusion-compositing-basics` — if doing 2D fixes in Fusion