---
name: davinci-resolve-depth-map-relight-davinciresolved
description: Depth Map Relight in DaVinci Resolve 20 — Studio feature for 3D relighting using depth maps, FG/MG/BG layer isolation, atmospheric perspective
category: creative
tags: [davinci-resolve, depth-map, relight, studio, 3d, lighting, fg-mg-bg, davinciresolved, resolve20]
source_url: https://www.instagram.com/reel/DL7j-M-xiDL/
author: davinciresolved
---

# DaVinci Resolve 20: Depth Map Relight

> **"Depth Map Relight in DaVinci Resolve 20"** — davinciresolved

## Core Feature: 3D Relighting via Depth Maps (Studio Only)

DaVinci Resolve 20 Studio introduces **Depth Map Relight** — a native tool for adding virtual lights to 2D footage using AI-generated depth maps.

> **⚠️ Studio Only** — Not available in Free version (confirmed by @kushal_roy69: "Not in free version though")

## What It Does

| Capability | Description |
|------------|-------------|
| **Virtual Light Placement** | Add point, spot, directional lights in 3D space |
| **FG/MG/BG Isolation** | Depth-based layer separation (Foreground, Midground, Background) |
| **Atmospheric Perspective** | Fog/haze that respects depth (distance-based) |
| **Shadow Casting** | Virtual lights cast shadows based on depth geometry |
| **Material Response** | Specular, diffuse, ambient response per depth layer |

## Workflow

### 1. Generate Depth Map
```
Color Page → Depth Map Effect (OFX)
    ├── Auto-generate from footage (Neural Engine)
    ├── Refine: Edge detection, temporal stability
    └── Output: Depth map as alpha/matte
```

### 2. Apply Relight Effect
```
Node Graph:
Node 01: Source Footage
    │
    ▼
Node 02: Depth Map (from Node 01 or separate)
    │
    ▼
Node 03: Relight OFX (Studio)
    ├── Light 1: Key (position, intensity, color, falloff)
    ├── Light 2: Fill (softer, opposite side)
    ├── Light 3: Rim/Backlight (catch edges via depth)
    ├── Atmosphere: Fog density, color, height falloff
    └── Shadows: Enable, softness, opacity
```

### 3. Layer Isolation (FG/MG/BG)
```
Relight Node → Output Options:
├── Combined (all lights + atmosphere)
├── Foreground Only (depth < 30%)
├── Midground Only (depth 30–70%)
├── Background Only (depth > 70%)
└── Depth Pass (grayscale for composting)
```

## Key Parameters

| Parameter | Range | Typical Use |
|-----------|-------|-------------|
| **Light Type** | Point / Spot / Directional | Point=omni, Spot=directed, Dir=sun |
| **Position (XYZ)** | 3D coordinates | Place in scene space |
| **Intensity** | 0–10+ | Match exposure |
| **Color Temp** | 1000K–10000K | Warm key, cool fill |
| **Falloff** | Linear / Quadratic / Custom | Realistic light decay |
| **Fog Density** | 0–1 | Atmospheric depth cue |
| **Fog Height** | 0–1 | Ground fog vs. uniform |
| **Shadow Softness** | 0–1 | Hard sun vs. soft sky |

## Pro Tips

| Tip | Why |
|-----|-----|
| **Track lights to camera** | If camera moves, parent lights to tracked null |
| **Use multiple Relight nodes** | Separate key/fill/rim for independent control |
| **Depth map quality matters** | Clean edges = clean light falloff; use temporal NR |
| **Combine with Depth Map Grading** | See `davinci-resolve-depth-map-grading` for color-by-depth |

## Comment Insights

> **@allpointsonepoint:** *"Any one know about any free way to do a depth map out of a video?"*
>
> → **Free options:** DaVinci Resolve Free has basic Depth Map effect but **no Relight**. For depth maps: Blender (free), MiDaS (AI, Python), RunwayML (web).

> **@roryphoto_:** *"my computer is on fire"*
>
> → **Performance:** Depth Map + Relight is GPU-intensive. Use proxy/optimized media.

## Related Skills

- `davinci-resolve-depth-map-grading` — Depth Map for FG/MG/BG color grading (gabelomotey)
- `davinci-resolve-depth-map-tutorial-gabelomotey` — Depth Map tutorial FG/MG/BG layer isolation
- `davinci-resolve-magicgrade-workflow-blueprint` — Keyboard-driven grading template

## Hashtags

#davinciresolve #colorgrading #videoediting #depthmap #relight #studio #resolve20 #3d #lighting