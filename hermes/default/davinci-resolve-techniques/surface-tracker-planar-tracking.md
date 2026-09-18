---
name: 'surface-tracker-planar-tracking'
description: 'Planar surface tracking (corner pin) in Color and Fusion pages — screen replacement, sign tracking, and perspective-locked composites.'
category: 'davinci-resolve-techniques'
tags: ['fusion', 'color-page', 'planar-tracking', 'surface-tracker', 'corner-pin', 'screen-replacement', 'compositing']
---

# Surface Tracker Planar Tracking

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color / Fusion  
**Node Graph:** Serial  
**Tags:** fusion, color-page, planar-tracking, surface-tracker, corner-pin, screen-replacement, compositing

---

## Overview

Planar surface tracking (corner pin) in Color and Fusion pages — screen replacement, sign tracking, and perspective-locked composites.

This skill covers 3 related techniques extracted from 3 Instagram Reel analyses.

### Techniques Covered
- Surface Tracker (Planar Tracking)
- Surface Tracking
- Planar Tracking with Temporary Contrast

---

## Key Nodes & Tools
- **Surface Tracker**
- **Corner Pin**
- **Media In**
- **Media Out**
- **Tracker Panel**

---

## Parameters & Settings

### Tracker Modes
- Planar Tracker (perspective)
- Point Tracker (position/rotation/scale)

### Surface Tracker
- 4-corner pin
- Grid warp
- Mesh warp

### Refine
- Adjust track points
- Add keyframes
- Smooth

### Apply To
- Power Window
- Corner Pin
- Transform
- Mesh Warp

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
