---
name: 'drone-cinematography'
description: 'Drone shooting techniques — cinematic moves, camera settings (log, D-Log), ND filters, height/angle planning, and regulatory basics.'
category: 'davinci-resolve-techniques'
tags: ['cinematography', 'drone', 'aerial', 'd-log', 'log', 'nd-filters', 'cinematic-moves']
---

# Drone Cinematography

**Category:** davinci-resolve-techniques  
**Resolve Page:** N/A (Production) / Color (Grading D-Log)  
**Node Graph:** Serial (CST for D-Log)  
**Tags:** cinematography, drone, aerial, d-log, log, nd-filters, cinematic-moves

---

## Overview

Drone shooting techniques — cinematic moves, camera settings (log, D-Log), ND filters, height/angle planning, and regulatory basics.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Drone (31 analyzed reels)
- DJI Gimbals Tips

---

## Key Nodes & Tools
- **Color Space Transform (D-Log → Rec.709)**
- **Primary Wheels**
- **HSL Curves (greens/blues)**

---

## Parameters & Settings

### Camera Settings
- D-Log / Log profile
- White balance (Kelvin)
- Shutter: 180° rule
- ISO: Native (100/200)

### Nd Filters
- Essential for 180° shutter in daylight

### Cinematic Moves
- Rise/Descend
- Orbit POI
- Dolly/Track
- Reveal (tilt up)
- Top-down
- Fly-through

### Post
- CST node → Creative grade → Sky replacement if needed

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
