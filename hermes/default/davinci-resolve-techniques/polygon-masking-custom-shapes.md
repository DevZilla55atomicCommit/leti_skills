---
name: 'polygon-masking-custom-shapes'
description: 'Polygon and B-Spline masking in Fusion for precise rotoscoping, custom shapes, and animated mattes with keyframeable vertices.'
category: 'davinci-resolve-techniques'
tags: ['fusion', 'polygon-mask', 'b-spline', 'rotoscoping', 'custom-shapes', 'keyframing', 'mattes']
---

# Polygon Masking Custom Shapes

**Category:** davinci-resolve-techniques  
**Resolve Page:** Fusion  
**Node Graph:** Serial  
**Tags:** fusion, polygon-mask, b-spline, rotoscoping, custom-shapes, keyframing, mattes

---

## Overview

Polygon and B-Spline masking in Fusion for precise rotoscoping, custom shapes, and animated mattes with keyframeable vertices.

This skill covers 1 related techniques extracted from 1 Instagram Reel analyses.

### Techniques Covered
- Polygon Masking

---

## Key Nodes & Tools
- **Polygon1**
- **BezierSpline**
- **EllipseMask**
- **RectangleMask**
- **Transform**

---

## Parameters & Settings

### Polygon
- Add/Remove vertices
- Vertex position (X/Y)
- Open/Closed
- Soft Edge
- Border Width

### B Spline
- Control points
- Tension
- Closed loop
- Animation via keyframes

### Animation
- Keyframe vertex positions per frame

### Output
- Connect to EffectMask input or use as matte in Merge

---

## Typical Workflow
1. **Open in Fusion** — Right-click clip → Open in Fusion Page
2. **Build Comp** — Add nodes (Tracker, Mask, Merge, Transform)
3. **Track/Keyframe** — Planar track, point track, or keyframe animation
4. **Composite** — Merge elements, adjust blend modes, color match
5. **Return to Edit** — Comp renders inline on timeline

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
