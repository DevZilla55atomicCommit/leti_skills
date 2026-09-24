---
name: 'hsl-curves-qualifier-techniques'
description: 'HSL Curves and Qualifier-based selective color grading — hue shifting, saturation targeting, luminance masking, and HSL qualifier workflows.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'hsl-curves', 'qualifier', 'selective-color', 'hue-vs-sat']
---

# Hsl Curves Qualifier Techniques

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, hsl-curves, qualifier, selective-color, hue-vs-sat

---

## Overview

HSL Curves and Qualifier-based selective color grading — hue shifting, saturation targeting, luminance masking, and HSL qualifier workflows.

This skill covers 9 related techniques extracted from 9 Instagram Reel analyses.

### Techniques Covered
- Hue, Saturation, Luminance (HSL) Curves
- HSL Curves Adjustment
- HSL Midtone Color Balancing
- HSL Color Correction
- Selective Color Desaturation via Hue Curves
- Selective Color Isolation (HSL Qualifier)
- HSL Qualifier Grading
- Color Mixer Adjustment
- Selective Luminance Masking & Glow Grading

---

## Key Nodes & Tools
- **HSL Curves**
- **Qualifier Node**
- **Color Mixer**
- **Hue Curves**
- **Saturation Curves**
- **Luminance Curves**

---

## Parameters & Settings

### Hsl Curves
- Hue vs Hue
- Hue vs Sat
- Hue vs Lum
- Lum vs Sat
- Sat vs Sat

### Qualifier
- **modes**: ['HSL', '3D', 'Luma']
- **tools**: ['eyedropper', 'add/subtract', 'clean black/white', 'softness']

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
