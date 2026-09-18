---
name: davinci-resolve-texture-pop_creatorsergeant
category: creative
description: "Texture Pop in DaVinci Resolve Studio — micro-contrast detail enhancement with Free version workaround using Blur + Soft Light + Unsharp Mask"
tags:
  - davinci-resolve
  - color-grading
  - texture-pop
  - studio-effect
  - clarity
  - detail-enhancement
  - free-version-workaround
  - sharpening
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJOfLJ0vVtF/"
creator: "@creatorsergeant"
vault_file: "Creative Grading & Looks/55-Texture-Pop_creatorsergeant_Studio-Effect.md"
---

# Texture Pop in DaVinci Resolve — Studio Effect + Free Workaround

## Overview
Micro-contrast texture enhancement using Resolve Studio's Texture Pop OFX, with a Free version replica using Blur + Soft Light composite + Unsharp Mask. Adds perceptual clarity without sharpening artifacts.

## When to Use
- Product, landscape, architecture — surface detail matters
- Soft lens correction (zoom lens ends)
- Documentary grit, realism
- **Not for**: Beauty, dreamy looks, noisy footage

## Prerequisites
- DaVinci Resolve Studio (for Texture Pop OFX)
- Free version: Native nodes only
- Basic node graph, composite modes
- Noise reduction knowledge (NR before texture!)

## Core Principle

> **Texture ≠ Sharpening** — Texture = mid-frequency micro-contrast; Sharpening = high-frequency edge contrast. Texture Pop targets the former.

## Node Structure

### Studio Version
```
Node 01: CST / Input Transform
Node 02: Primary Balance
Node 03: [TEXTURE POP OFX] — Resolve FX Texture
Node 04: [POWER WINDOW / QUALIFIER] — Selective (protect skin!)
Node 05: Global Polish / LUT / Grain
```

### Free Version Workaround
```
Node 01: CST / Input Transform
Node 02: Primary Balance
Node 03: [BLUR + SOFT LIGHT] — Micro-contrast (Texture Pop replica)
Node 04: [UNSHARP MASK] — Edge sharpening (separate)
Node 05: Global Polish
```

---

## Studio Version: Texture Pop OFX

### Add Effect
- Effects → Resolve FX Texture → **Texture Pop**
- Place on Node 03 (after primary)

### Parameters
| Parameter | Range | Typical | Effect |
|-----------|-------|---------|--------|
| **Amount** | 0-100 | 10-30 | Texture intensity |
| **Size** | 1-100 | 20-50 | Detail scale |
| **Softness** | 0-100 | 10-30 | Transition smoothness |
| **Boost Shadows** | 0-100 | 0-20 | Texture in darks |
| **Boost Highlights** | 0-100 | 0-20 | Texture in brights |

### Presets by Content

| Content | Amount | Size | Softness | Shadows | Highlights |
|---------|--------|------|----------|---------|------------|
| **Portraits/Skin** | 5-15 | 30-40 | 20-30 | 0 | 0 |
| **Landscapes** | 20-40 | 40-60 | 10-20 | 10-20 | 10-20 |
| **Product/Detail** | 30-50 | 20-40 | 5-15 | 10 | 10 |
| **Foliage/Nature** | 25-45 | 30-50 | 10-20 | 15 | 10 |
| **Subtle Global** | 5-10 | 50 | 30 | 0 | 0 |

### Critical: Protect Skin
- **Power Window** on face → Invert → Texture Pop on BG only
- **OR** Qualifier skin → Invert matte → Texture Pop on non-skin
- **NEVER** full-frame on portraits

### Blend Control
- Node Key Output Gain → Blend intensity
- Or: Layer Mixer parallel → Blend modes

---

## Free Version Workaround (Pinned Comment Method)

### Node 03: Micro-Contrast (Texture Pop Equivalent)
1. **Blur OFX** (Resolve FX Blur → Blur)
2. **Radius**: 10-20 (mid-frequency)
3. **Composite Mode**: **Soft Light**
4. **Opacity/Key Output Gain**: 10-20%

**Why it works**: Blur removes fine detail → Soft Light blends blurred midtones as contrast boost → Mimics Texture Pop's mid-frequency lift

### Node 04: Edge Sharpening (Separate)
1. **Unsharp Mask** (Resolve FX Sharpen → Unsharp Mask)
2. **Radius**: 2-4 (fine edges)
3. **Amount**: 0.3-0.7
4. **Threshold**: 2-5 (noise protection)

### Best Free Combo (Per Creator)
```
Node 03: Blur (Radius 15) → Composite: Soft Light → Opacity 15%
Node 04: Unsharp Mask (Radius 3, Amount 0.5)
```

---

## Advanced: Parallel Texture Branches

```
Layer Mixer (Parallel)
├── Branch A: Texture Pop (Background) — Amount 30
├── Branch B: Texture Pop (Skin) — Amount 5, Softness 40
└── Branch C: No Texture (Sky/Smooth) — Amount 0
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Full frame on faces | Pore horror, crunchy skin | **Window/Qualifier protect skin** |
| Amount > 50 | Artifacts, noise boost | **Subtle: 10-30** |
| No NR first | Sensor noise amplified | **NR BEFORE Texture Pop** |
| On compressed footage | Macro-blocking enhanced | Reduce amount, add NR |
| Ignore Size parameter | Wrong detail scale | Match Size to subject detail |

---

## Pro Tips

- **@creatorsergeant**: Free workaround in pinned comment — Blur + Soft Light + Unsharp Mask
- **@film.by.isku**: "All in the manual. No secret club" — Workaround IS documented
- **@samshroder06**: Fixes soft zoom lens ends — Practical use case
- **@rahj_jordan**: "Add shadows to duplicate" — Shadow texture matters
- **Order matters**: NR → Texture Pop → Sharpen (if needed)

---

## Related Skills
- `davinci-resolve-sharpening-3-hacks_davinciresolved` — 3 sharpening methods
- `davinci-resolve-sharpening-marco-herbst` — Proper sharpening workflow
- `davinci-resolve-orange-teal-parallel-nodes` — Parallel node structure
- `davinci-resolve-depth-map-grading_davinciresolved` — Depth-based texture

---

## References
- Source: @creatorsergeant Instagram Reel (Feb 12, 2025)
- Hashtags: #davinciresolve #davinciresolvestudio #texture #colorgrading #videoediting
- Engagement: 11K likes, 81 comments
- Free workaround: Pinned comment on original post