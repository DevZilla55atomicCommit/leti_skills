---
name: 'advanced-qualifier-layer-mixer'
description: 'Advanced masking workflows using Qualifier + Layer Mixer for parallel grade blending, edge refinement, and complex isolation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'qualifier', 'layer-mixer', 'parallel-nodes', 'masking', 'keying']
---

# Advanced Qualifier Layer Mixer

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Layer Mixer  
**Tags:** color-grading, color-page, qualifier, layer-mixer, parallel-nodes, masking, keying

---

## Overview

Advanced masking workflows using Qualifier + Layer Mixer for parallel grade blending, edge refinement, and complex isolation.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Advanced Qualifier with Layer Mixer
- Layer Mixer Masked Grading

---

## Key Nodes & Tools
- **Layer Mixer**
- **Qualifier**
- **Serial Nodes (Background/Foreground)**
- **Power Windows**

---

## Parameters & Settings

### Layer Mixer Inputs
- Background (base grade)
- Foreground (isolated grade)

### Blend Modes
- Normal
- Add
- Screen
- Overlay
- Multiply

### Qualifier Refinement
- Clean Black/White
- Softness
- In/Out Ratio
- Despill

### Edge Treatment
- Matte Finesse controls

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
