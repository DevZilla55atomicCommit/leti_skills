---
name: 'local-contrast-texture-enhancement'
description: 'Midtone Detail, Clarity, Texture, Sharpening, and Blur tools for local contrast enhancement and creative texture control.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'midtone-detail', 'clarity', 'texture', 'sharpening', 'blur', 'color-fx']
---

# Local Contrast Texture Enhancement

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, midtone-detail, clarity, texture, sharpening, blur, color-fx

---

## Overview

Midtone Detail, Clarity, Texture, Sharpening, and Blur tools for local contrast enhancement and creative texture control.

This skill covers 7 related techniques extracted from 7 Instagram Reel analyses.

### Techniques Covered
- Primary Color Correction and Tone Curve Grading
- Tone Curve and Detail Grade Grading
- Local Contrast and Global Enhancement via Post-Processing
- Local Adjustments and Tone Curve Grading
- Selective Color Masking and Texture Enhancement
- Selective Saturation boosting using Custom Curves
- Local Contrast via Custom Curves

---

## Key Nodes & Tools
- **Midtone Detail (MDT)**
- **Color FX Tab → Texture/Clarity**
- **Blur Tab → Sharpening**
- **Blur Tab → Blur/Mist**
- **Custom Curves**

---

## Parameters & Settings

### Midtone Detail
- Positive = texture boost, Negative = smoothing

### Clarity
- Midtone contrast (micro-contrast)

### Texture
- High-frequency detail enhancement

### Sharpening
- **radius**: Edge width
- **detail**: Threshold
- **masking**: Edge-only application

### Blur
- **radius**: Softness
- **type**: ['Gaussian', 'Mist', 'Bloom']

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
