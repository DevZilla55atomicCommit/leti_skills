---
name: davinci-resolve-widescreen-look_caleboshi
category: creative
description: "Widescreen/Anamorphic look in DaVinci Resolve — Timeline Resolution method (proper) vs Letterbox masking, aspect ratio presets, export settings, anamorphic de-squeeze"
tags:
  - davinci-resolve
  - color-grading
  - anamorphic
  - widescreen
  - letterbox
  - aspect-ratio
  - timeline-resolution
  - 2.39:1
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DHryr1YMG_e/"
creator: "@caleboshi"
vault_file: "Creative Grading & Looks/59-Widescreen-Look_caleboshi_Aspect-Ratio.md"
---

# Widescreen / Anamorphic Look — Proper Timeline Resolution vs Letterbox

## Overview
Two approaches to 2.39:1 scope look: **Timeline Resolution change (proper)** vs **Letterbox masking (post crop)**. Community consensus: Timeline Resolution = correct workflow.

## When to Use
- **Timeline Resolution**: New projects, anamorphic footage, feature delivery
- **Letterbox**: Existing 16:9 projects, client needs 16:9 with bars, reframing flexibility

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Project setup knowledge
- Monitoring for scope aspect (external monitor or overlay)

## Core Principle

> **Timeline Resolution = Native Canvas** — Grade in target aspect, export true resolution. Letterbox = Compromise.

---

## Method 1: Timeline Resolution (Proper Way)

### Project Settings
```
Timeline Resolution: Custom
Width: 1920 (HD) / 3840 (4K) / 4096 (DCI 4K)
Height: Width ÷ 2.39
  - 1920 → 804
  - 3840 → 1607
  - 4096 → 1714
```

### Image Scaling
```
Input Scaling: Scale full frame with crop
(Or: Center crop — for anamorphic de-squeeze workflow)
```

### Monitoring
- **Viewer**: Native 2.39:1 (no UI bars)
- **External**: 2.39:1 monitor or Letterbox overlay

---

## Method 2: Letterbox Mask (Post Crop)

### Output Blanking (Project)
```
Project Settings → Color → Output Blanking: 2.39:1
```

### Node-Level (Per Shot)
```
Sizing → Cropping
1080p: Top 138px, Bottom 138px
4K: Top 276px, Bottom 276px
```

### Power Window (Creative Vignette)
- Circle → Invert → Softness 100
- Gain/Lift: -0.2 (edge darkening)

---

## Anamorphic De-Squeeze (If Shot Anamorphic)

| Squeeze | Pixel Aspect | Sizing Setting |
|---------|--------------|----------------|
| **2x** | 2.0 | Anamorphic: 2x |
| **1.33x** | 1.33 | Anamorphic: 1.33x |

---

## Export Settings

### True Scope (No Bars)
```
Delivery → Format: QuickTime/MP4
Resolution: Custom → 1920x804 (etc.)
Pixel Aspect: Square (1.0)
```

### With Bars (16:9 Delivery)
```
Resolution: 1920x1080
Output Blanking: Burned in
```

---

## Aspect Ratio Presets

| Name | Ratio | 1920 Wide | 3840 Wide | Use Case |
|------|-------|-----------|-----------|----------|
| **Scope / Cinema** | 2.39:1 | 1920x804 | 3840x1607 | Feature films |
| **Netflix Scope** | 2.00:1 | 1920x960 | 3840x1920 | Netflix Originals |
| **Ultrawide** | 2.35:1 | 1920x817 | 3840x1634 | Classic anamorphic |
| **IMAX Digital** | 1.90:1 | 1920x1011 | 3840x2022 | IMAX Digital |
| **Standard** | 16:9 | 1920x1080 | 3840x2160 | TV, Web |

---

## Community Insights

- **@dbk_drew_kamara**: Timeline resolution = proper way
- **@dedogonons**: "Different resolution than manual timeline adjustment?" → Timeline resolution IS the manual adjustment
- **@pierrx.pch**: "Create sequence with good dimension" → Same thing
- **@caleboshi**: Practice footage for grading community

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Letterbox on 16:9 export | Double bars | **Use Timeline Resolution** |
| Wrong height calc | Slightly off ratio | **Width ÷ 2.39 exactly** |
| No monitoring | Can't judge framing | **External scope monitor** |
| Mixed timelines | Inconsistent delivery | **One project = one timeline res** |
| Anamorphic not de-squeezed | Oval circles, tall actors | **Clip Attributes → Pixel Aspect** |

---

## Pro Tips

- **Decide EARLY** — Timeline resolution is project foundation
- **Test export** — Verify scope playback on target devices
- **Communicate** — Tell VFX, DIT, DP the timeline resolution
- **Save as Preset** — Project templates for 2.39:1, 2.00:1, etc.
- **Practice footage** — @caleboshi provides log footage for grading practice

---

## Related Skills
- `davinci-resolve-anamorphic-look_jihadjk` — Full fake anamorphic (flares, bokeh, distortion)
- `davinci-resolve-color-management-timeline_caleboshi` — CM with custom timelines
- `davinci-resolve-letterbox-cinematic-ratio` — Letterbox masking techniques

---

## References
- Source: @caleboshi Instagram Reel (Mar 26, 2025)
- Hashtags: #davinciresolve #widescreen #anamorphic #aspectratio #colorgrading
- Engagement: 1,676 likes, 50 comments
- Key comment: Timeline resolution method endorsed by community