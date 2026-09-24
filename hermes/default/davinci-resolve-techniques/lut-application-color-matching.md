---
name: 'lut-application-color-matching'
description: 'Apply, manage, and blend LUTs for creative looks, technical transforms (log→Rec.709), and reference-based color matching.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'lut', 'color-space-transform', 'creative-lut', 'technical-lut']
---

# Lut Application Color Matching

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, lut, color-space-transform, creative-lut, technical-lut

---

## Overview

Apply, manage, and blend LUTs for creative looks, technical transforms (log→Rec.709), and reference-based color matching.

This skill covers 4 related techniques extracted from 4 Instagram Reel analyses.

### Techniques Covered
- Color Matching via LUT Application
- White Balance Correction via Eyedropper Tool
- Color Space Transform RAW Photo Grading
- CST Workflow for Multi-Cam Matching

---

## Key Nodes & Tools
- **LUT Node**
- **Color Space Transform (CST)**
- **Primary Wheels**
- **Custom Curves**

---

## Parameters & Settings

### Lut Types
- Technical (Log→Rec709)
- Creative (Film Emulation)
- Camera-specific
- Output/Display

### Intensity
- 0-100% blend with original grade

### Placement
- Input (before grade), Middle (creative), Output (final delivery)

### Cst Settings
- **input**: Camera log/gamut
- **output**: Working/Delivery space
- **tone_mapping**: Auto/Manual

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
