---
name: davinci-resolve-match-color-grade-davinciresolved
description: Match color grade in DaVinci Resolve — using Color Match tool, waveform/vectorscope reference, and manual curve matching for shot-to-shot consistency
category: creative
tags: [davinci-resolve, color-match, shot-matching, color-grading, waveform, vectorscope, curves, davinciresolved]
source_url: https://www.instagram.com/reel/DKkAFDhx-2F/
author: davinciresolved
---

# DaVinci Resolve: Match Color Grade

> **"Match color grade in DaVinci Resolve"** — davinciresolved

## Core Techniques for Shot Matching

### Method 1: Color Match Tool (Resolve 18+)

**Location:** Color Page → Color Match panel (or `Color Match` button in toolbar)

1. **Select reference clip** (the look you want to match)
2. **Select target clip** (the clip to grade)
3. **Click Color Match** → Resolve analyzes and applies initial match
4. **Refine manually** — Color Match is a starting point, not final grade

### Method 2: Waveform + Vectorscope Reference (Manual, Pro Way)

| Scope | What to Match | How |
|-------|--------------|-----|
| **Waveform (Luma)** | Overall exposure, black/white points | Adjust Lift/Gamma/Gain to match reference IRE levels |
| **Parade (RGB)** | Color balance per channel | Match R/G/B parade shapes between clips |
| **Vectorscope** | Hue/saturation of skin tones, memory colors | Align skin tone line, match saturation distance |

### Method 3: Curve Matching (Most Precise)

1. **Open Curves** on both clips (reference + target)
2. **Overlay reference** (still/grab) in viewer
3. **Match RGB curves point-by-point**:
   - Shadows (0–20 IRE)
   - Midtones (20–80 IRE)
   - Highlights (80–100 IRE)
4. **Fine-tune Hue vs Hue / Hue vs Sat** for color shifts

## Pro Workflow: Shot Matching System

```
REFERENCE CLIP (Hero shot, best exposure)
    │
    ├── Grab Still → Gallery
    │
    └── TARGET CLIPS (to match)
        ├── Clip A: Similar lighting → Minor tweaks
        ├── Clip B: Different exposure → Lift/Gamma/Gain + Curves
        └── Clip C: Different WB → Temp/Tint + Parade RGB
```

### Step-by-Step Per Clip

1. **Sync Scopes:** Pin Waveform + Vectorscope + Parade
2. **Set Reference:** Grab still of hero → Pin to viewer (wipe mode)
3. **Match Luma First:** Lift/Gamma/Gain to align Waveform
4. **Match Chroma:** Parade RGB → Adjust Temp/Tint/Lift/Gain per channel
5. **Match Skin Tones:** Vectorscope skin line → Qualifier if needed
6. **Creative Polish:** Curves / Color Wheels / LUT (shared across matched clips)

## Comment Insights

> **@mmjf___:** *"Isn't it easier to just apply grade or it won't be accurate?"*
> 
> → **Answer:** "Apply Grade" (copy/paste node tree) works **only if lighting/camera are identical**. Color Match / manual matching handles **different exposures, WB, lighting**.

> **@ivinnayayoesel:** *"Are these on the pro version or the free one?"*
> 
> → **Color Match tool:** Studio only. **Manual scope matching:** Free + Studio.

## Advanced: Color Match with Reference Stills

1. Build **Reference Library** in Gallery:
   - Skin tones (various ethnicities)
   - Sky/foliage (memory colors)
   - Black/white points
   - Key props/wardrobe colors

2. **Match to Reference Still** (not just adjacent clip):
   - More consistent across scene
   - Survives re-edits / clip reordering

## Related Skills

- `davinci-resolve-grading-systems-cdvc-day19` — Group Pre/Post-Clip for scene-wide matching
- `davinci-resolve-primary-color-correction-workflow-linear` — Printer lights method for matching
- `davinci-resolve-cinematic-grading-3-mistakes` — CST→DWG pipeline for consistent color management
- `davinci-resolve-node-tree-river-analogy` — Mental model: matching flows downstream

## Quick Reference Card

```
SHOT MATCHING CHECKLIST:
☐ Scopes pinned: Waveform, Parade RGB, Vectorscope
☐ Reference still grabbed & pinned (wipe mode)
☐ Luma matched (Lift/Gamma/Gain → Waveform align)
☐ Chroma matched (Temp/Tint + RGB Parade align)
☐ Skin tones on line (Vectorscope + Qualifier check)
☐ Creative grade applied AFTER match (shared nodes)
☐ Version saved (Timeline Grade / PowerGrade)
```

## Hashtags

#davinciresolve #colorgrading #colormatch #shotmatching #videoediting