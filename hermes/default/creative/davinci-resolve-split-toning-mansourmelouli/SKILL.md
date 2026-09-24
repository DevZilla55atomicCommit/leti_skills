---
name: davinci-resolve-split-toning-mansourmelouli
category: creative
description: "Split toning via Custom Curves (RGB channels) — shadows to teal, highlights to orange, with skin tone protection via Qualifier + Curves lock"
tags:
  - davinci-resolve
  - color-grading
  - split-toning
  - custom-curves
  - rgb-curves
  - skin-tones
  - teal-orange
  - cinematic-mood
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJd0smRovvq/"
creator: "@mansourmelouli"
vault_file: "Creative Grading & Looks/51-Split-Toning_mansourmelouli_Custom-Curves-RGB.md"
---

# Split Toning with Custom Curves — Teal Shadows, Orange Highlights, Protected Skin

## Overview
Precise split toning using Custom Curves (independent RGB channels) with skin tone protection via Qualifier + Curves anchor locking. Creates cinematic teal/orange mood while keeping subjects natural.

## When to Use
- Narrative, commercial, music video — cinematic mood
- When you need **channel-level precision** (not possible with wheels)
- Skin tones MUST stay neutral
- **Not for**: Quick social content (use Color Wheels + Split Toning panel)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Custom Curves OFX knowledge
- Qualifier / HSL selection basics
- Vectorscope reading (skin tone line)

## Core Principle

> **Break the chain** → Independent R/G/B curves → Shadow/Highlight channel separation → Skin lock via Qualifier

## Node Structure

```
Node 01: CST / Input Transform
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: SKIN LOCK — Qualifier + Custom Curves (anchors)
Node 04: SPLIT TONE — Custom Curves (R/G/B broken chain)
Node 05: Global Polish / LUT / Grain
```

## Step-by-Step Procedure

### 1. Primary Grade First (Node 01-02)
- CST / Color Managed pipeline
- Exposure, White Balance, Contrast/Pivot
- Neutral, balanced base

### 2. Skin Tone Lock (Node 03)
**Qualifier:**
- HSL Qualifier → Sample skin (face, hands)
- Refine: Hue ±15°, Sat 20-80%, Lum 20-80%
- High softness, clean matte

**Custom Curves (on same node or serial):**
- Mode: **Custom** (not RGB/Y)
- **Break chain** (uncouple R/G/B) — NOT YET, just for skin lock
- Add **anchor points** at skin luminance on **each R/G/B channel**
- These anchors "pin" skin values — downstream curves won't move them
- **Verify**: Vectorscope skin trace on line at skin luminance

### 3. Split Tone Curves (Node 04)
**Add Custom Curves OFX → Break Chain (uncouple R/G/B)**

**Red Channel:**
- Shadows: **Pull DOWN** (remove red from shadows → cooler)
- Midtones: Anchor (skin locked from Node 03)
- Highlights: **Lift UP** (add red/warmth to highlights)

**Green Channel:**
- Shadows: **Slight Lift UP** (add green to shadows → teal)
- Midtones: Anchor
- Highlights: Neutral

**Blue Channel:**
- Shadows: **Lift UP** (add blue to shadows → teal)
- Midtones: Anchor
- Highlights: **Pull DOWN** (remove blue from highlights → warmer)

### 4. Verify & Refine
- **Vectorscope**: Skin trace on line (~103°)
- **Parade RGB**: Check channel separation in shadows/highlights
- **Waveform**: No clipping, legal range
- Adjust midtone anchors if skin drifted

## Curve Shape Reference

### Red Channel
```
Out
1.0 |           ● (Highlights up)
    |          /
    |         /
0.5 |--------● (Mid anchor)
    |       /
    |      /
0.0 |●____/    (Shadows down)
    +----------------> In
```

### Blue Channel
```
Out
1.0 |●____________ (Highlights down)
    |  \
    |   \
0.5 |    ●-------- (Mid anchor)
    |     \
    |      \
0.0 |       ●____ (Shadows up)
    +----------------> In
```

### Green Channel
```
Out
1.0 |_____________ (Highlights neutral)
    |
    |
0.5 |-------●------ (Mid anchor)
    |      \
    |       \
0.0 |        ●___ (Shadows slight up)
    +----------------> In
```

## Parameter Quick Table

| Step | Channel | Shadows | Midtones | Highlights |
|------|---------|---------|----------|------------|
| **Skin Lock** | All | Anchor at skin lum | **Anchor at skin lum** | Anchor at skin lum |
| **3** | **Red** | **Down** | Locked | Neutral/Slight up |
| **4** | **Blue** | **Up** | Locked | **Down** |
| **4** | **Green** | **Slight Up** | Locked | Neutral |
| **5** | **Red** | — | — | **Up** |
| **5** | **Blue** | — | — | **Down** |
| **6** | **All** | — | **Skin check** | — |

## Skin Protection Methods

### A: Serial Lock (Node 03) — Recommended
- Qualifier + Curves anchors BEFORE split tone node
- Downstream curves (Node 04) can't move anchored points
- Clean, single pipeline

### B: Parallel Branch
```
Layer Mixer (Parallel)
├── Branch 1: Full image → Split Tone Curves (Node 04)
└── Branch 2: Qualifier (Skin) → Flat Curves → Blend 70%
```

### C: Post-Correction (Node 05)
- After split tone: Qualifier skin → Hue vs Hue (to 103°) → Hue vs Sat (normalize)

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Chain not broken | Can't separate channels | Click chain icon → broken |
| No skin lock | Green/magenta faces | Qualifier + anchors Node 03 |
| Too aggressive | Posterized, clown look | Max 15-20% curve movement |
| Ignore midtones | Skin hue shifts | Anchor midtones, check vectorscope |
| Same values all shots | Inconsistent | Per-shot adjust, use gallery stills |
| No CST first | Wrong color math | Color Managed or CST before curves |

## Variations

| Look | Shadows | Highlights | Saturation |
|------|---------|------------|------------|
| **Classic Teal/Orange** | Teal (B+G up, R down) | Orange (R up, B down) | Medium |
| **Subtle Cool/Warm** | Cyan (subtle) | Gold (subtle) | Low (5-10%) |
| **Sci-Fi Magenta/Green** | Magenta (R+B up) | Green (G up, R+B down) | High |
| **Noir Blue/Gold** | Deep Blue | Warm Gold | Low-Med |
| **Vintage Sepia/Blue** | Blue | Sepia (R+G up) | Low |

## Pro Tips

- **Break chain FIRST** — easy to forget
- **Skin luminance varies** — place anchors at actual skin levels per shot
- **Vectorscope > Monitor** — monitor lies, scope doesn't
- **Gallery stills** — match split tone across scene
- **Qualifier in DWG** — if Color Managed, qualify in wide gamut for cleaner matte

## Related Skills
- `davinci-resolve-split-tone-studio-free` — No qualifier method
- `davinci-resolve-orange-teal-secret-kienobifilms` — Wheels method
- `davinci-resolve-orange-teal-parallel-nodes` — Parallel nodes method
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Foundations
- `davinci-resolve-skin-tones-right_mansourmelouli` — Skin workflow

## References
- Source: @mansourmelouli Instagram Reel (May 10, 2025)
- Hashtags: #davinciresolve #davinciresolve20 #colorgrading #splittoning #cinematiclook #filmmakingtips #postproduction #colorcontrast
- Engagement: 3,306 likes, 51 comments
- Community: International, high engagement, verified creator