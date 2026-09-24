---
name: davinci-resolve-wheels-comparison_aparicio
category: creative
description: "Primary vs LOG vs HDR Wheels in DaVinci Resolve — when to use each wheel system for log normalization, creative grading, and HDR highlight control"
tags:
  - davinci-resolve
  - color-grading
  - primary-wheels
  - log-wheels
  - hdr-wheels
  - color-wheels
  - wheel-comparison
  - grading-tools
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJc15zpvqoe/"
creator: "@aparicio.co"
vault_file: "Color Correction Fundamentals/20-Wheels-Comparison_aparicio_Primary-LOG-HDR.md"
---

# Primary vs LOG vs HDR Wheels in DaVinci Resolve

## Overview
Complete guide to Resolve's three color wheel systems — Primary (Lift/Gamma/Gain), LOG (Shadows/Midtones/Highlights), and HDR (Specular/Highlights/Midtones/Shadows) — with decision matrix for workflow selection.

## When to Use
- **Every grade** — choosing the right wheel system is fundamental
- Log footage normalization → LOG wheels first
- Creative grading → Primary wheels
- HDR delivery → HDR wheels (Studio)
- Camera matching → LOG wheels per camera

## Prerequisites
- DaVinci Resolve (Free: Primary + LOG; Studio: all three)
- Basic color wheel operation
- Understanding of display-referred vs scene-referred
- HDR wheels require Studio + HDR timeline

## The Three Wheel Systems

### Primary Wheels (Lift / Gamma / Gain) — Display-Referred
**Range**: Fixed (Shadows 0-30%, Midtones 30-70%, Highlights 70-100% IRE)
**Space**: Output color space (Rec.709, P3, etc.)
**Best for**: Creative grading, SDR delivery, final polish

| Wheel | Controls | Typical Use |
|-------|----------|-------------|
| **Lift** | Shadows | Black level, shadow tint, crush |
| **Gamma** | Midtones | Exposure, contrast pivot, skin tones |
| **Gain** | Highlights | White level, highlight tint, rolloff |

**Characteristics**: Coupled ranges, display-linear response, universal compatibility

---

### LOG Wheels (Shadows / Midtones / Highlights) — Scene-Referred
**Range**: Logarithmic (matches camera log encoding)
**Space**: Camera log space (S-Log3, LogC, BRAW, etc.)
**Best for**: Log normalization, camera matching, exposure correction

| Wheel | Log Range | Typical Use |
|-------|-----------|-------------|
| **Shadows** | Log black → ~18% gray | Log black level, shadow noise, lift |
| **Midtones** | ~18% gray → ~90% reflect | Log exposure, middle gray, skin |
| **Highlights** | ~90% reflect → Log white | Highlight rolloff, specular control |

**Characteristics**: Decoupled log ranges, scene-linear response, pivot adjustable

---

### HDR Wheels (Specular / Highlights / Midtones / Shadows) — Perceptual-Referred
**Range**: Nits-based (absolute luminance)
**Space**: HDR timeline (ST.2084, HLG, DWG)
**Best for**: HDR grading, specular control, Dolby Vision/HDR10
**Studio Only**

| Wheel | Nits Range | Typical Use |
|-------|------------|-------------|
| **Specular** | >Diffuse white (100-10000+ nits) | Sun, reflections, practicals |
| **Highlights** | Diffuse white → Mid-gray | Bright surfaces, sky, lights |
| **Midtones** | Mid-gray → Near black | Subject exposure, skin |
| **Shadows** | Near black → 0 nits | Black level, shadow detail |

**Characteristics**: 4-wheel precision, perceptual response, EOTF-aware

---

## Decision Matrix: Which Wheel First?

| Footage Type | Delivery | First Wheel | Second Wheel | Workflow |
|--------------|----------|-------------|--------------|----------|
| **Log** | SDR | **LOG** | Primary | Normalize → Create |
| **Log** | HDR | **LOG** | HDR | Normalize → HDR Grade |
| **Rec.709** | SDR | **Primary** | — | Direct grade |
| **HDR** | HDR | **HDR** | Primary | Perceptual → Creative |
| **Multi-cam** | Any | **LOG (each)** | Primary | Match in log → Unify |
| **Quick look** | SDR | **Primary** | — | Fast iteration |

---

## Recommended Workflows

### SDR Log Workflow (Standard)
```
Node 01: LOG Wheels          → Log normalize (exposure, WB, contrast)
Node 02: CST (Log → DWG/709) → Transform
Node 03: Primary Wheels      → Creative grade
Node 04: Polish (LUT, Grain) → Finish
```

### HDR Workflow (Studio)
```
Node 01: LOG Wheels          → Log normalize
Node 02: CST (Log → DWG/ST2084) → HDR space
Node 03: HDR Wheels          → Primary HDR grade (SPECULAR CONTROL!)
Node 04: Primary Wheels      → Creative refinements
Node 05: HDR Wheels          → Final trim / SDR sim
```

### Camera Matching
```
Cam A: Node 01: LOG Wheels → Match reference
Cam B: Node 01: LOG Wheels → Match reference
Both:  Node 02: CST → Common space → Primary → Unified creative
```

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Primary on log footage | Crushed blacks, color shifts | LOG wheels first |
| LOG on Rec.709 | Over-complicated, wrong response | Primary only |
| HDR on SDR | Wasted precision, confusion | Primary only |
| Only Primary on log | Can't cleanly fix exposure | Add LOG node first |
| Random wheel mixing | Conflicting adjustments | Follow workflow order |
| Ignoring pivots | Ranges don't match footage | Adjust LOG/HDR pivots |

---

## Pro Tips

- **@neilchh**: "What does lift gamma gain affect?" → Lift=shadows, Gamma=midtones, Gain=highlights (display space)
- **@simon.kirketerp**: "Not changing color profile... inputs work most correct" → Use Color Managed project, not clip-level CST
- **@colorsense.io**: "Try HSV, much better results!" → HSV wheels alternative for hue-based grading
- **@z4ck.3d**: "Premiere has dedicated curve for this" → Concept transfers across NLEs
- **@interfilmproductions**: "Get a LUT and refine" → LUTs = starting point, wheels = refinement

---

## Related Skills
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Foundations including wheel basics
- `davinci-resolve-white-balance-linear-mode` — Precision WB with wheels
- `davinci-resolve-skin-tones-right_mansourmelouli` — HDR wheels for skin
- `davinci-resolve-white-balance-luma-mix` — RGB Gain alternative
- `davinci-resolve-color-compressor` — HDR highlight management

---

## References
- Source: @aparicio.co Instagram Reel (May 9, 2025)
- Hashtags: #davinciresolve #colorgrading #cinematography #filmmaking #editing #videography #tutorial #edit
- Engagement: 12K likes, 82 comments
- Community: Beginner-friendly, international, high educational value