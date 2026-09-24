---
name: 'power-windows-zone-grading'
description: 'Zone-based grading using Power Windows (radial, linear, custom) with tracking for localized exposure, color, and contrast control.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'power-windows', 'masks', 'tracking', 'zone-grading', 'vignette']
---

# Power Windows Zone Grading

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, power-windows, masks, tracking, zone-grading, vignette

---

## Overview

Zone-based grading using Power Windows (radial, linear, custom) with tracking for localized exposure, color, and contrast control.

This skill covers 4 related techniques extracted from 4 Instagram Reel analyses.

### Techniques Covered
- Zone-based Color Grading with Power Windows
- Split Screen Window Masking
- Graduated Window Masking Grading
- Masking and Color Isolation

---

## Key Nodes & Tools
- **Power Windows**
- **Radial Gradient**
- **Linear Gradient**
- **Custom Curve Window**
- **Tracker**

---

## Parameters & Settings

### Window Types
- Circle
- Square
- Polygon
- Linear Gradient
- Radial Gradient
- Custom Curve

### Tracking Modes
- Pan
- Tilt
- Zoom
- Rotate
- 3D
- Perspective

### Softness
- Feathering for seamless blends

### Invert
- Invert mask for outside correction

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
