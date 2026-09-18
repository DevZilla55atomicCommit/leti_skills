---
name: davinci-resolve-color-management-timeline_caleboshi
category: creative
description: "DaVinci Resolve Color Management at Timeline Level — DaVinci YRGB Color Managed, DWG grading, automatic clip transforms, HDR/SDR setup, camera input settings"
tags:
  - davinci-resolve
  - color-grading
  - color-management
  - timeline-level
  - davinci-yrgb
  - cst
  - aces
  - color-space
  - pipeline
  - hdr
  - sdr
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DGUZWubsGp0/"
creator: "@caleboshi"
vault_file: "Color Management & Pipeline/56-Color-Management-Timeline_caleboshi_DWG-Setup.md"
---

# DaVinci Resolve Color Management — Timeline Level (DaVinci YRGB Color Managed)

## Overview
Modern color pipeline using project-wide Timeline Color Management — replaces per-clip CST nodes with centralized DaVinci Wide Gamut (DWG) grading, automatic input transforms, and single output transform.

## When to Use
- **Every new project** — Foundation for consistent color
- Multi-camera shoots — Auto-normalizes different log spaces
- HDR + SDR deliverables — Same grade, different output transforms
- Team collaboration — Shared settings = consistent results
- **Not for**: Legacy projects with baked CST grades (conversion risky)

## Prerequisites
- DaVinci Resolve 18+ (Free or Studio)
- Basic color management concepts
- Understanding of scene-referred vs display-referred
- HDR monitor for HDR work (or SDR sim)

## Core Concept

> **Grade once in DWG (Scene-Referred), deliver anywhere** — Input transforms auto, output transform global.

---

## Setup Procedure

### 1. Project Settings → Color Management
```
Color Management: DaVinci YRGB Color Managed
Timeline Color Space: DaVinci Wide Gamut Intermediate (DWG)
Output Color Space: Rec.709 (SDR) / Rec.2020 ST.2084 (HDR)
```

### 2. Clip Attributes (Input Transform)
- **Auto**: Resolve reads metadata (camera, codec)
- **Manual Override**: Right-click clip → Clip Attributes → Color Space
- **Common Inputs**:
  - Sony S-Log3: S-Gamut3.Cine + S-Log3
  - ARRI LogC: AlexaWideGamut + LogC3/4
  - RED: REDWideGamutRGB + Log3G10
  - BRAW: Blackmagic Design Film + BMD Film
  - Canon C-Log: Cinema Gamut + C-Log2/3
  - Panasonic V-Log: V-Gamut + V-Log
  - DJI D-Log: D-Gamut + D-Log
  - iPhone ProRes Log: Apple Log + Apple Log

### 3. Node Graph — Clean & Simple
```
OLD (Per-Clip CST):
Node 01: CST (Log → Rec.709)
Node 02: Grade
Node 03: Creative

NEW (Timeline Managed):
Node 01: Grade (in DWG — Scene Referred!)
Node 02: Creative
(Auto Output: DWG → Rec.709/P3/Rec.2020)
```

**No CST nodes needed!** Grade directly in DWG.

---

## Grading in DWG (Scene-Referred) — Key Differences

### Exposure Reference
- **Middle Gray**: ~0.18 in DWG (not 0.4-0.5 in Rec.709)
- **Highlights**: Can exceed 1.0 (speculars 10-100+)
- **Waveform**: Reads 0-100+ (nit-equivalent)

### Tools Behavior
- **Primary Wheels**: Operate in DWG (scene-linear-ish)
- **Log Wheels**: Match camera log encoding
- **HDR Wheels**: Nits-based (HDR timelines only)
- **Curves**: Scene-referred response

### LUTs in Managed Pipeline
| LUT Type | Input Space | Placement |
|----------|-------------|-----------|
| **Creative Look** | DWG (modern) / Log (legacy) | Node in DWG |
| **Film Emulation** | Usually Log or DWG | Node in DWG |
| **Technical (Input)** | Camera → DWG | **Use CM instead** |
| **Technical (Output)** | DWG → Display | **Use CM Output Transform** |

### Noise Reduction Order
1. **Temporal NR** → On raw/clip (pre-CM)
2. **Spatial NR** → In DWG (post-transform)

---

## HDR Setup (ST.2084 / Dolby Vision)

### Project Settings
```
Color Management: DaVinci YRGB Color Managed
Timeline Color Space: DaVinci Wide Gamut Intermediate
Output Color Space: Rec.2020 ST.2084 (1000/2000/4000 nits)
```

### Monitoring
- **HDR Reference Monitor** required for grading
- **SDR Sim**: Viewer → HDR → SDR Sim (client review)

### HDR Grading Tools
- **HDR Wheels**: Specular / Highlights / Midtones / Shadows (nits)
- **Specular Control**: Critical — don't blow 1000+ nits
- **Legal Range**: 10-bit = 64-940 → maps to 0-1023 HDR

---

## Per-Timeline Override
- Right-click Timeline → Timelines → Color Management
- Override project settings per timeline
- Use case: SDR timeline + HDR timeline in same project

---

## Camera Input Quick Reference

| Camera | Color Space | Gamma |
|--------|-------------|-------|
| Sony S-Log3 | S-Gamut3.Cine | S-Log3 |
| ARRI LogC | AlexaWideGamut | LogC3/4 |
| RED | REDWideGamutRGB | Log3G10 |
| BRAW | BMD Film Gen 5 | BMD Film |
| Canon C-Log | Cinema Gamut | C-Log2/3 |
| Panasonic V-Log | V-Gamut | V-Log |
| DJI D-Log | D-Gamut | D-Log |
| iPhone ProRes Log | Apple Log | Apple Log |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Grade in Rec.709 with CM on | Dark, contrasty, wrong | **Grade in DWG** |
| Double transform (CST + CM) | Weird colors, clipped | **Remove CST nodes** |
| Wrong clip input | Color shift, clipping | **Check Clip Attributes** |
| LUT in wrong space | Color shift | **LUT space = Timeline space** |
| No HDR monitor | Can't grade HDR | **Get monitor or SDR sim** |
| Mix CM projects | Incompatible grades | **Match settings exactly** |

---

## Pro Tips

- **@caleboshi**: "Color Management is crucial to getting great color grades" — Foundation skill
- **@intensity_film**: "Another way to do it" — Multiple valid approaches exist
- **Community demand**: 567 comments for community access — High-value knowledge
- **Save as Project Default** — Gear icon in Color Management panel
- **Test with Chart** — X-Rite / DSC charts verify pipeline

---

## Related Skills
- `davinci-resolve-cst-basics` — Clip-level CST (legacy)
- `davinci-resolve-aces-workflow` — ACES pipeline
- `davinci-resolve-hdr-grading-basics` — HDR specifics
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Grading in managed space

---

## References
- Source: @caleboshi Instagram Reel (Feb 20, 2025)
- Hashtags: #davinciresolve #colormanagement #colorgrading #timeline #workflow
- Engagement: 3,771 likes, 567 comments
- Community: High demand for color grading education