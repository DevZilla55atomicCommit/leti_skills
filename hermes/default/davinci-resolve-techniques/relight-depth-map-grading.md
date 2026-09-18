---
name: 'relight-depth-map-grading'
description: 'DaVinci Resolve 18.5+ Relight effect using Depth Maps for 3D lighting adjustments — virtual lights, position, intensity, and color in post.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'relight', 'depth-map', '3d-lighting', 'resolve-18-5', 'studio']
---

# Relight Depth Map Grading

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, relight, depth-map, 3d-lighting, resolve-18-5, studio

---

## Overview

DaVinci Resolve 18.5+ Relight effect using Depth Maps for 3D lighting adjustments — virtual lights, position, intensity, and color in post.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Relight Effect (DaVinci Resolve 18.5+)
- Relight tool

---

## Key Nodes & Tools
- **Relight Effect**
- **Depth Map**

---

## Parameters & Settings

### Light Types
- Point
- Spot
- Directional
- Environment

### Controls
- Position (X/Y/Z)
- Intensity
- Color
- Falloff
- Shadow Casting

### Depth Map
- Auto-generated or imported

### Requirements
- DaVinci Resolve Studio 18.5+

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
