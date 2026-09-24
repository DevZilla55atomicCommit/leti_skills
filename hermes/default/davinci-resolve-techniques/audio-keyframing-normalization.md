---
name: 'audio-keyframing-normalization'
description: 'Rapid audio keyframing with Option/Alt-click, volume automation, and loudness normalization (EBU R128 / ATSC A/85).'
category: 'davinci-resolve-techniques'
tags: ['edit-page', 'fairlight', 'audio', 'keyframing', 'normalization', 'loudness', 'volume-automation']
---

# Audio Keyframing Normalization

**Category:** davinci-resolve-techniques  
**Resolve Page:** Edit / Fairlight  
**Node Graph:** N/A  
**Tags:** edit-page, fairlight, audio, keyframing, normalization, loudness, volume-automation

---

## Overview

Rapid audio keyframing with Option/Alt-click, volume automation, and loudness normalization (EBU R128 / ATSC A/85).

This skill covers 3 related techniques extracted from 3 Instagram Reel analyses.

### Techniques Covered
- Rapid Audio Keyframing with Option/Alt Click
- Rapid Audio Keyframing Placement
- Normalize Audio Levels

---

## Key Nodes & Tools
- **Timeline Volume Line**
- **Keyframe Markers**
- **Normalize Audio Dialog**
- **Fairlight Page**

---

## Parameters & Settings

### Keyframing
- Opt/Alt + click on volume line to add keyframe

### Normalization Modes
- Sample Peak
- True Peak
- Loudness (EBU R128)
- Loudness (ATSC A/85)

### Target Levels
- **ebu_r128**: -23 LUFS
- **atsc_a85**: -24 LKFS
- **streaming**: -14 to -16 LUFS

---

## Typical Workflow
1. **Setup** — Configure project settings, timeline resolution
2. **Edit** — Assemble rough cut using shortcuts (Blade, Trim, Swap)
3. **Refine** — Add transitions, effects, adjustment clips
4. **Audio** — Keyframe levels, normalize, add music beats
5. **Color** — Switch to Color page for grading
6. **Deliver** — Render cache, render in place, export

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
