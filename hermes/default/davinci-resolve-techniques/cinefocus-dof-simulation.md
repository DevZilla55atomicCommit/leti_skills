---
name: 'cinefocus-dof-simulation'
description: 'DaVinci Resolve 21+ AI CineFocus for synthetic depth of field — depth map generation, focus distance, aperture shape, and bokeh simulation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'cinefocus', 'depth-of-field', 'ai', 'resolve-21', 'studio', 'bokeh']
---

# Cinefocus Dof Simulation

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, cinefocus, depth-of-field, ai, resolve-21, studio, bokeh

---

## Overview

DaVinci Resolve 21+ AI CineFocus for synthetic depth of field — depth map generation, focus distance, aperture shape, and bokeh simulation.

This skill covers 1 related techniques extracted from 1 Instagram Reel analyses.

### Techniques Covered
- CineFocus Depth of Field Simulation (Resolve 21)

---

## Key Nodes & Tools
- **AI CineFocus Node**
- **Depth Tab**
- **Focus Tab**
- **Depth Map Tab**

---

## Parameters & Settings

### Depth Tab
- Auto-generate or import depth map

### Focus Tab
- Focus Distance
- Aperture (f-stop)
- Focus Falloff

### Depth Map Tab
- Refine map
- Edge cleanup
- Subject isolation

### Bokeh
- Shape (circle, polygon, anamorphic)
- Rotation
- Anamorphic squeeze
- Highlight gain

### Requirements
- DaVinci Resolve Studio 21+

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
