---
name: 'tilt-shift-edge-blur-masking'
description: 'Tilt-Shift Blur effect for miniature look or selective focus — gradient blur mask with adjustable angle, position, and falloff.'
category: 'davinci-resolve-techniques'
tags: ['color-page', 'tilt-shift', 'blur', 'selective-focus', 'miniature-effect', 'gradient-mask']
---

# Tilt Shift Edge Blur Masking

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-page, tilt-shift, blur, selective-focus, miniature-effect, gradient-mask

---

## Overview

Tilt-Shift Blur effect for miniature look or selective focus — gradient blur mask with adjustable angle, position, and falloff.

This skill covers 1 related techniques extracted from 1 Instagram Reel analyses.

### Techniques Covered
- Tilt Shift Edge Blur Masking

---

## Key Nodes & Tools
- **Node 1 (Map/Mask)**
- **Node 2 (Tilt-Shift Blur)**
- **Window (Gradient)**

---

## Parameters & Settings

### Blur Node
- Blur Type: Tilt-Shift
- Center
- Angle
- Width
- Falloff
- Strength

### Map Node
- Gradient window defining sharp zone

### Creative
- Miniature/fake tilt-shift
- Selective focus simulation
- Dreamy portrait look

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
