---
name: 'halation-glow-effects'
description: 'Create cinematic halation (highlight bloom) and soft diffusion glow effects using blur, blend modes, and highlight isolation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'edit-page', 'halation', 'glow', 'bloom', 'diffusion', 'cinematic']
---

# Halation Glow Effects

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color / Edit  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, edit-page, halation, glow, bloom, diffusion, cinematic

---

## Overview

Create cinematic halation (highlight bloom) and soft diffusion glow effects using blur, blend modes, and highlight isolation.

This skill covers 4 related techniques extracted from 4 Instagram Reel analyses.

### Techniques Covered
- Halation Effect
- Filmic Glow / Soft Diffusion Effect
- Selective Luminance Masking & Glow Grading
- Soft Cinematic Glow Overlay

---

## Key Nodes & Tools
- **Gaussian Blur**
- **Lumetri Color**
- **Adjustment Layer**
- **Qualifier (Highlights)**
- **Blend Modes (Screen/Lighten/Add)**

---

## Parameters & Settings

### Blur Radius
- High (50-200px for halation)

### Blend Mode
- Screen, Lighten, or Add

### Opacity
- Low-Medium (10-40%)

### Highlight Isolation
- Qualifier or Luma Key for bright areas only

### Color Tint
- Optional warm/red tint for film halation

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
