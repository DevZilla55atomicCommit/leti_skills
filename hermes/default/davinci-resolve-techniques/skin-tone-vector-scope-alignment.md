---
name: 'skin-tone-vector-scope-alignment'
description: 'Professional skin tone correction using Vector Scope skin tone line as reference with Qualifier/Pen Window isolation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'skin-tones', 'vector-scope', 'qualifier', 'pen-window']
---

# Skin Tone Vector Scope Alignment

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, skin-tones, vector-scope, qualifier, pen-window

---

## Overview

Professional skin tone correction using Vector Scope skin tone line as reference with Qualifier/Pen Window isolation.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Skin Tone Alignment using Vector Scope Mask
- Color Cast Correction via Tint Adjustment

---

## Key Nodes & Tools
- **Vector Scope**
- **Qualifier (Pen Tool Window)**
- **Primary Wheels**
- **Hue vs Sat Curves**

---

## Parameters & Settings

### Skin Tone Line
- 11-degree line between Red and Yellow

### Workflow
- Mask skin → adjust hue/sat → align vector trace to line

### Tools
- Pen Window
- Qualifier HSL
- Color Wheels
- Curves

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
