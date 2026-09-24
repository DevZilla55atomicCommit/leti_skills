---
name: 'custom-curves-contrast-adjustment'
description: 'Create custom contrast curves including S-curves, lifted blacks (faded film look), and channel-specific RGB curve manipulation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'curves', 'contrast', 's-curve', 'rgb-curves', 'lifting-blacks']
---

# Custom Curves Contrast Adjustment

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, curves, contrast, s-curve, rgb-curves, lifting-blacks

---

## Overview

Create custom contrast curves including S-curves, lifted blacks (faded film look), and channel-specific RGB curve manipulation.

This skill covers 7 related techniques extracted from 7 Instagram Reel analyses.

### Techniques Covered
- Hue/Saturation/Curves Adjustment
- Custom Curves Contrast Adjustment
- Vintage Film Look via Lift and Curves
- Lifting Blacks (Faded Look)
- Tone Curve and Detail Grade Grading
- Local Adjustments and Tone Curve Grading
- Soft Cinematic Glow Overlay

---

## Key Nodes & Tools
- **Curves Tool**
- **Custom Curves**
- **RGB Curves**
- **Hue Curves**
- **Lum vs Sat Curves**

---

## Parameters & Settings

### Curve Types
- Master (Luma)
- Red
- Green
- Blue
- Hue vs Hue
- Hue vs Sat
- Hue vs Lum
- Lum vs Sat
- Sat vs Sat

### Common Shapes
- S-curve (contrast)
- Inverted S (flat)
- Lifted blacks (film)
- Channel separation (color grading)

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
