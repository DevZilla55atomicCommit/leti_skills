---
name: 'timeline-vs-clip-grading'
description: 'Understanding Timeline Grade (affects all clips) vs Clip Grade vs Group Pre/Post Clip grades — when to use each level.'
category: 'davinci-resolve-techniques'
tags: ['color-grading', 'color-page', 'timeline-grade', 'clip-grade', 'group-grade', 'color-groups', 'workflow']
---

# Timeline Vs Clip Grading

**Category:** davinci-resolve-techniques  
**Resolve Page:** Color  
**Node Graph:** Multiple (Timeline, Clip, Group Pre/Post)  
**Tags:** color-grading, color-page, timeline-grade, clip-grade, group-grade, color-groups, workflow

---

## Overview

Understanding Timeline Grade (affects all clips) vs Clip Grade vs Group Pre/Post Clip grades — when to use each level.

This skill covers 1 related techniques extracted from 1 Instagram Reel analyses.

### Techniques Covered
- Timeline Grading

---

## Key Nodes & Tools
- **Timeline Node**
- **Clip Nodes**
- **Group Pre-Clip**
- **Group Post-Clip**

---

## Parameters & Settings

### Hierarchy
- Timeline → Group Pre → Clip → Group Post → Output

### Use Cases
- **timeline**: Global look, film emulation LUT, output transform
- **group_pre**: Camera matching, base correction per camera
- **clip**: Creative grade per shot
- **group_post**: Final unified adjustments

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
