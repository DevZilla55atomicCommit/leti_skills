---
name: 'noise-reduction-spatial-temporal'
description: 'Spatial and Temporal Noise Reduction workflows in the Motion Effects panel — settings, radius, threshold, and temporal frames for clean footage.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'noise-reduction', 'spatial-nr', 'temporal-nr', 'motion-effects', 'denoise']
---

# Noise Reduction Spatial Temporal

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, noise-reduction, spatial-nr, temporal-nr, motion-effects, denoise

---

## Overview

Spatial and Temporal Noise Reduction workflows in the Motion Effects panel — settings, radius, threshold, and temporal frames for clean footage.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Spatial Noise Reduction
- Temporal Noise Reduction

---

## Key Nodes & Tools
- **Motion Effects Panel → Spatial NR**
- **Motion Effects Panel → Temporal NR**

---

## Parameters & Settings

### Spatial Nr
- **mode**: ['Faster', 'Better']
- **radius**: 1-8
- **luma/chroma**: Separate controls
- **threshold**: Detail preservation

### Temporal Nr
- **frames**: 1-5 (odd numbers)
- **motion_estimation**: ['Faster', 'Better']
- **luma/chroma**: Separate
- **threshold**: Ghosting prevention

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
