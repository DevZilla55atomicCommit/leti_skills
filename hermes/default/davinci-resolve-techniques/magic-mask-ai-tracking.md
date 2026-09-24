---
name: 'magic-mask-ai-tracking'
description: 'DaVinci Resolve Magic Mask (AI) for automatic object/person isolation with forward/backward tracking and mask refinement.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'magic-mask', 'ai', 'object-tracking', 'person-mask', 'rotoscoping']
---

# Magic Mask Ai Tracking

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, magic-mask, ai, object-tracking, person-mask, rotoscoping

---

## Overview

DaVinci Resolve Magic Mask (AI) for automatic object/person isolation with forward/backward tracking and mask refinement.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Magic Mask AI Object Tracking
- Magic Mask Tool Stacking

---

## Key Nodes & Tools
- **Magic Mask**
- **Tracker**
- **Curves**
- **Qualifier**

---

## Parameters & Settings

### Mask Modes
- Person
- Object

### Tracking
- Forward
- Backward
- Bidirectional

### Refinement
- **softness**: Edge feather
- **expand_contract**: Mask dilation/erosion
- **profile**: AI model selection (Modern 01-03)

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
