---
name: 'teal-orange-film-emulation'
description: 'Create cinematic teal & orange film looks using hue vs sat curves, qualifiers for skin protection, film grain, and lift/gamma/gain manipulation.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'teal-orange', 'film-emulation', 'skin-tones', 'film-look']
---

# Teal Orange Film Emulation

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Serial  
**Tags:** color-grading, color-page, teal-orange, film-emulation, skin-tones, film-look

---

## Overview

Create cinematic teal & orange film looks using hue vs sat curves, qualifiers for skin protection, film grain, and lift/gamma/gain manipulation.

This skill covers 4 related techniques extracted from 4 Instagram Reel analyses.

### Techniques Covered
- Cinematic Teal & Orange / Film Emulation
- Vintage Film Look via Lift and Curves
- Moody Color Grading with Saturation Reduction
- Selective Color (Color Splashing)

---

## Key Nodes & Tools
- **Primary Wheels**
- **Hue vs Saturation**
- **Qualifier (Skin Tone)**
- **Film Grain Effect**
- **Curves**
- **Lift/Gamma/Gain**

---

## Parameters & Settings

### Teal Shift
- Shift greens/cyans toward teal in shadows/midtones

### Orange Warmth
- Warm skin tones toward orange in midtones

### Skin Protection
- Qualifier mask to exclude skin from teal shift

### Film Grain
- Add organic texture (opacity 10-30%)

### Lifted Blacks
- Raise lift for faded film aesthetic

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
