---
name: davinci-resolve-chroma-warp-davinciresolved
description: Chroma Warp tool in DaVinci Resolve — advanced color warping for hue/saturation/luminance manipulation, color-to-color mapping, creative color transformation
category: creative
tags: [davinci-resolve, chroma-warp, color-warping, color-grading, hue-mapping, davinciresolved]
source_url: https://www.instagram.com/reel/DLC60kJx5vD/
author: davinciresolved
---

# DaVinci Resolve: Chroma Warp Tool

> **"Chroma Warp tool in DaVinci Resolve"** — davinciresolved

## What is Chroma Warp?

**Chroma Warp** is an advanced color manipulation tool in DaVinci Resolve that allows **direct hue-to-hue, saturation-to-saturation, and luminance-to-luminance mapping** — essentially a 3D color warp grid for precise color transformation.

Think of it as **Color Warper on steroids** — instead of just pushing/pulling colors, you define exact input→output mappings for any color region.

## Location

**Color Page → OpenFX → Resolve FX Color → Chroma Warp**

(Or search "Chroma Warp" in Effects library)

## Core Concept: 3D Warp Grid

```
INPUT COLOR SPACE          OUTPUT COLOR SPACE
┌─────────────────┐       ┌─────────────────┐
│  Hue (0–360°)   │  ──▶  │  Hue (0–360°)   │
│  Sat (0–100%)   │       │  Sat (0–100%)   │
│  Lum (0–100%)   │       │  Lum (0–100%)   │
└─────────────────┘       └─────────────────┘
        │                         │
        └──── Warp Grid ─────────┘
        (Control points define mapping)
```

## Key Controls

| Control | Function |
|---------|----------|
| **Warp Grid** | 3D grid of control points — drag to remap colors |
| **Hue Warp** | Shift hues: red→orange, green→teal, etc. |
| **Saturation Warp** | Compress/expand saturation per hue region |
| **Luminance Warp** | Brighten/darken specific colors |
| **Range Limiter** | Restrict effect to specific hue/sat/lum range |
| **Smoothness** | Interpolation between control points |
| **Mix** | Blend with original (0–100%) |

## Common Use Cases

### 1. Color-to-Color Replacement
```
Red car → Blue car:
1. Select red hue range in Range Limiter
2. Drag Hue Warp control points: 0° → 240°
3. Adjust Sat/Lum to match target
```

### 2. Skin Tone Protection During Creative Grades
```
1. Range Limiter: Skin tone hue (20–40°), mid saturation
2. Lock Hue/Sat/Lum for skin range (flat warp)
3. Warp everything else creatively
```

### 3. Stylized Look: Single-Color Pop
```
1. Range Limiter: Target color (e.g., yellow taxi)
2. Boost Saturation Warp for that hue only
3. Desaturate Warp for all other hues
```

### 4. Color Harmony Enforcement
```
1. Define target palette (e.g., Teal & Orange)
2. Warp all hues toward nearest palette color
3. Smooth transitions via grid density
```

## Pro Tips from Comments

> **@kampsseedfarmllc:** *"I'm struggling to change the color to black, is it even possible to do so?"*
>
> **Answer:** Yes — set **Luminance Warp** to 0 for target hue range. But pure black = no chroma info. Better: desaturate (Sat Warp → 0) + crush blacks in curves.

> **@imniha1:** *"Does this work in free version?"*
>
> **Answer:** Chroma Warp is **Studio only** (Resolve FX Color category).

> **@willsart:** *"Why not Hue vs Hue?"*
>
> **Answer:** Hue vs Hue = 1D curve (hue→hue only). Chroma Warp = 3D (hue+sat+lum → hue+sat+lum). More control, but more complex.

> **@michel_rsdm:** *"Magic Mask + Chroma Warp for car color change — better or waste?"*
>
> **Answer:** **Better.** Magic Mask isolates object → Chroma Warp transforms color precisely. Without mask, Warp affects ALL similar colors in frame.

## Workflow: Object Color Change (Car Example)

```
Node 01: Source
    │
    ▼
Node 02: Magic Mask / Power Window (isolate car)
    ├── Output: Alpha → Node 03 Key Input
    │
    ▼
Node 03: Chroma Warp (Key Input from Node 02)
    ├── Range Limiter: Car's hue range
    ├── Hue Warp: Original → Target hue
    ├── Sat Warp: Match target saturation
    ├── Lum Warp: Match target brightness
    └── Mix: 100% (or blend for subtle)
    │
    ▼
Node 04: Edge refinement (blur alpha, spill suppress)
    │
    ▼
Output
```

## Chroma Warp vs. Other Tools

| Tool | Dimensions | Best For | Version |
|------|------------|----------|---------|
| **Hue vs Hue** | 1D (H→H) | Simple hue shifts | Free + Studio |
| **Hue vs Sat** | 1D (H→S) | Saturation per hue | Free + Studio |
| **Hue vs Lum** | 1D (H→L) | Brightness per hue | Free + Studio |
| **Color Warper** | 2D (H/S grid) | Push/pull color regions | Studio |
| **Chroma Warp** | **3D (H/S/L→H/S/L)** | **Precise color-to-color mapping** | **Studio** |
| **3D LUT** | 3D (fixed) | Look application | Free + Studio |

## Related Skills

- `davinci-resolve-color-warper-saturation-balance` — Color Warper for saturation control
- `davinci-resolve-hue-vs-luminance-density-saturation` — Hue vs Lum for density
- `davinci-resolve-masking-power-masking` — Magic Mask for object isolation

## Hashtags

#davinciresolve #colorgrading #videoediting #chroma-warp #color-warping #studioversion