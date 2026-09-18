---
name: 'stabilization-optical-flow'
description: 'Clip stabilization using Edit page Stabilizer (Perspective/Similarity/Translation) and Optical Flow for micro-jitter removal — plus Smooth Cut for jump cuts.'
category: 'davinci-resolve-techniques'
tags: ['edit-page', 'color-page', 'stabilization', 'optical-flow', 'smooth-cut', 'micro-jitter', 'retime']
---

# Stabilization Optical Flow

**Category:** davinci-resolve-techniques  
**Resolve Page:** Edit / Color / Fusion  
**Node Graph:** Serial (Inspector)  
**Tags:** edit-page, color-page, stabilization, optical-flow, smooth-cut, micro-jitter, retime

---

## Overview

Clip stabilization using Edit page Stabilizer (Perspective/Similarity/Translation) and Optical Flow for micro-jitter removal — plus Smooth Cut for jump cuts.

This skill covers 3 related techniques extracted from 3 Instagram Reel analyses.

### Techniques Covered
- Micro-Jitter Stabilization (Optical Flow / Retime)
- Stabilization
- Plan Tracker Stabilization

---

## Key Nodes & Tools
- **Inspector → Stabilization**
- **Retime Controls → Optical Flow**
- **Smooth Cut Transition**
- **Planar Tracker (Fusion)**

---

## Parameters & Settings

### Edit Stabilizer
- **modes**: ['Perspective', 'Similarity', 'Translation']
- **smoothness**: 0.5-0.7 typical
- **zoom**: Auto/Manual

### Optical Flow
- Retime → Optical Flow (for slow-mo or stabilization)

### Smooth Cut
- Transition → Smooth Cut (morphs jump cuts)

### Planar Tracker
- Fusion page → PlanarTracker node (corner pin)

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
