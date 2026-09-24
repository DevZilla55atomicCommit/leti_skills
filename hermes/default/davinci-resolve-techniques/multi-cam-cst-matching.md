---
name: 'multi-cam-cst-matching'
description: 'Multi-camera color matching workflow using Color Space Transform (CST) nodes per camera — normalize log formats, match sensors, unify look.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'multi-cam', 'cst', 'color-space-transform', 'camera-matching', 'log-normalization']
---

# Multi Cam Cst Matching

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial (per clip)  
**Tags:** color-grading, color-page, multi-cam, cst, color-space-transform, camera-matching, log-normalization

---

## Overview

Multi-camera color matching workflow using Color Space Transform (CST) nodes per camera — normalize log formats, match sensors, unify look.

This skill covers 1 related techniques extracted from 1 Instagram Reel analyses.

### Techniques Covered
- CST Workflow for Multi-Cam Matching

---

## Key Nodes & Tools
- **Color Space Transform (CST)**
- **Balance Node**
- **Serial Nodes**

---

## Parameters & Settings

### Per Camera
- Add CST node to each camera angle's clip

### Input Spaces
- Sony S-Log3/S-Gamut3.Cine
- Canon C-Log 2/3
- Panasonic V-Log
- RED Log3G10
- ARRI LogC
- Blackmagic Film

### Output Space
- DaVinci Wide Gamut / Rec.709 / P3

### Balance Node
- After CST → Primary Wheels for matching

### Group Grade
- Apply unified creative grade via Group Post-Clip or Timeline Grade

---

## Typical Workflow
1. **Import & Organize** — Add clips to timeline, create Color page version
2. **Base Correction** — Serial Node 1: White Balance, Exposure, Contrast (Primary Wheels)
3. **Technical Transform** — CST/LUT node for log→Rec.709 if needed
4. **Creative Grade** — Additional serial nodes for look development
5. **Local Adjustments** — Power Windows, Qualifiers, Magic Mask for isolation
6. **Texture & Finish** — Film grain, halation, sharpening, noise reduction
7. **Review & Deliver** — Toggle grades, compare versions, render

---

## Related Skills
- `davinci-resolve-techniques/serial-node-grading-workflow`
- `davinci-resolve-techniques/custom-curves-contrast-adjustment`
- `davinci-resolve-techniques/hsl-curves-qualifier-techniques`
- `davinci-resolve-techniques/power-windows-zone-grading`
- `davinci-resolve-techniques/magic-mask-ai-tracking`
- `davinci-resolve-techniques/noise-reduction-spatial-temporal`
- `davinci-resolve-techniques/render-cache-proxy-workflow`

---

## Source
Generated from 453 completed vision analyses of Instagram Reels (DaVinci Resolve techniques) — `VISION_PROGRESS.json`
