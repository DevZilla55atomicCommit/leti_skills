---
name: davinci-color-correction-lut
description: Master color correction and LUT application workflows in DaVinci Resolve. Covers serial node graphs, LUT application, color wheels, and grading techniques from Instagram Reel analysis.
trigger: color correction, LUT application, color grading, DaVinci Resolve color page, serial node graph
steps:
  - "Import footage into DaVinci Resolve Media Pool"
  - "Navigate to Color page and create a new serial node graph"
  - "Add first node: Color Correction (adjust lift, gamma, gain, saturation, contrast)"
  - "Add second node: LUT Application (select and apply .cube LUT file)"
  - "Fine-tune LUT intensity using key output gain or layer mixer opacity"
  - "Use Color Wheels (Primary/Log/HDR) for primary corrections"
  - "Apply Hue vs Sat / Hue vs Hue curves for selective color adjustments"
  - "Save grade as PowerGrade or export LUT for reuse"
parameters:
  - name: lut_file_path
    type: string
    description: Path to .cube LUT file
    required: true
  - name: saturation
    type: number
    description: Saturation adjustment (0-200%)
    default: 100
  - name: contrast
    type: number
    description: Contrast adjustment
    default: 50
  - name: temperature
    type: number
    description: Color temperature in Kelvin
    default: 5600
  - name: lift
    type: number
    description: Lift/shadow adjustment
    default: 0
  - name: gamma
    type: number
    description: Gamma/midtone adjustment
    default: 1.0
  - name: gain
    type: number
    description: Gain/highlight adjustment
    default: 1.0
tags:
  - color-correction
  - lut
  - color-grading
  - davinci-resolve
  - serial-node-graph
  - instagram-reel
  - color-wheels
  - powergrade
category: davinci-resolve-color
---

# DaVinci Resolve Color Correction & LUT Application

Master professional color correction and LUT workflows in DaVinci Resolve Color page using serial node graphs. Based on analysis of 15+ Instagram Reel techniques covering color correction, LUT application, and grading workflows.

## Overview

This skill consolidates color correction techniques from multiple Instagram Reels demonstrating DaVinci Resolve workflows. The core pattern uses a **serial node graph** with 2-3 nodes: Color Correction → LUT Application → Optional Creative Grade.

## Core Node Graph Structure

```
Node 1 (Serial) → Node 2 (Serial) → Node 3 (Serial, optional)
   │                 │                  │
Color            LUT              Creative
Correction      Application      Grade/Refinement
```

### Node 1: Primary Color Correction
- **Tool**: Color Wheels (Primary / Log / HDR)
- **Key Parameters**: Lift, Gamma, Gain, Offset, Saturation, Contrast
- **Purpose**: Balance exposure, white balance, contrast base

### Node 2: LUT Application
- **Tool**: LUT Node (3D LUT)
- **Key Parameters**: LUT File Path, Key Output Gain (intensity)
- **Purpose**: Apply creative look / film emulation / camera-to-display transform

### Node 3: Creative Refinement (Optional)
- **Tools**: Curves (Hue vs Sat, Hue vs Hue, Hue vs Lum), Qualifier, Power Windows
- **Purpose**: Secondary adjustments, skin tone protection, selective grading

## Key Techniques from Batch Analysis

### Technique 1: Basic Color Correction + LUT (C93Ef02BTJV, C913vb9PoeI, C9BB0vtxdWK)
```text
Steps:
1. Import footage → Color page
2. Node 1: Color Wheels → Adjust Lift/Gamma/Gain for exposure balance
3. Node 2: Add LUT node → Select .cube file → Set Key Output Gain to 0.5-1.0
4. Node 3 (optional): Hue vs Sat curve → Protect skin tones
```

### Technique 2: Vintage Look via Saturation/Contrast (C8E_bWsuEOx)
```text
Node 1: Color Wheels
  - Saturation: 80-90 (desaturate slightly)
  - Contrast: 55-60 (increase for film look)
  - Temperature: 5000-5500K (warm vintage tone)

Node 2: LUT (Kodak 2383 or Fuji 3510 emulation)
  - Key Output Gain: 0.7
```

### Technique 3: LUT Matching for Instagram Reel Recreation (C7xcsf6Iw0m, C5K366TPHoj)
```text
1. Import reference Reel + your footage
2. Node 1: Match color wheels to reference (use scopes: Parade RGB, Vectorscope)
3. Node 2: Apply same LUT as reference (if known) or create custom LUT via Color Match
4. Node 3: Fine-tune with Curves to match exact look
```

### Technique 4: Red Light Effect (C8e4UkvoT7E)
```text
Node 1: Color Wheels → Push shadows toward red (Lift: R+15, G-5, B-10)
Node 2: Custom Curve (Red channel) → Lift shadows, compress highlights
Node 3: Glow OFX (optional) → Add bloom to red highlights
```

## Parameter Reference

| Parameter | Range | Typical Value | Node |
|-----------|-------|---------------|------|
| Saturation | 0-200% | 80-120% | Color Wheels |
| Contrast | 0-100 | 40-60 | Color Wheels |
| Temperature | 2000-10000K | 5600K (daylight) | Color Wheels / Temp/Tint |
| Tint | -100 to +100 | 0 | Color Wheels |
| Lift | -1.0 to +1.0 | -0.1 to +0.1 | Color Wheels |
| Gamma | 0.5-2.0 | 0.9-1.1 | Color Wheels |
| Gain | 0.5-2.0 | 0.9-1.1 | Color Wheels |
| LUT Key Output Gain | 0-1.0 | 0.5-1.0 | LUT Node |

## Scopes to Monitor

1. **Parade RGB** - RGB channel balance, exposure
2. **Vectorscope** - Hue/saturation, skin tone line
3. **Waveform (Luma)** - Overall luminance distribution
4. **Histogram** - Tonal distribution

## PowerGrade Export Workflow

1. Right-click grade in Gallery → "Export PowerGrade"
2. Save as `.dragr` file for reuse
3. Import via Gallery → "Import PowerGrade"
4. Apply to any clip via right-click → "Apply Grade"

## LUT Management

- **Location**: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/`
- **Format**: `.cube` (3D LUT), `.3dl` (3D LUT)
- **Refresh**: Color page → LUT Browser → Refresh button

## Common Pitfalls

- ❌ Applying LUT before primary correction (breaks log-to-rec709 transform)
- ❌ Using LUT at 100% intensity without Key Output Gain adjustment
- ❌ Ignoring color space mismatches (clip vs timeline vs output)
- ✅ Always color correct FIRST, then apply LUT
- ✅ Use Key Output Gain (0.3-0.8) for creative LUTs
- ✅ Match clip color space to timeline (Project Settings → Color Management)

## Related Skills

- `davinci-color-grading-fundamentals` - Core grading principles
- `davinci-cinematic-looks` - Film emulation, teal-orange, bleach bypass
- `davinci-lut-management` - LUT organization, creation, ACES workflows