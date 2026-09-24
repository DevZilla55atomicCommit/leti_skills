---
name: davinci-resolve-anamorphic-look_jihadjk
category: creative
description: "Create anamorphic scope look in DaVinci Resolve — 2.39:1 letterbox, oval bokeh, horizontal flares, lens distortion, vignette for cinematic fake anamorphic aesthetic"
tags:
  - davinci-resolve
  - color-grading
  - anamorphic
  - aspect-ratio
  - letterbox
  - lens-flare
  - oval-bokeh
  - cinematic
  - mask
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DF5brPQvf3-/"
creator: "@jihadk__"
vault_file: "Creative Grading & Looks/54-Anamorphic-Look_jihadjk_Fake-Scope.md"
---

# Anamorphic Look in DaVinci Resolve — Fake Scope Aesthetic

## Overview
Post-production anamorphic simulation using letterbox masking, oval bokeh (Defocus OFX or Blur+Mask), horizontal lens flares, and subtle barrel distortion — achieves 2.39:1 cinematic scope without anamorphic lenses.

## When to Use
- Any project wanting "scope" look (2.39:1)
- No anamorphic lens budget/access
- Music videos, narrative, commercial
- **Not for**: Projects requiring true anamorphic optical characteristics (breathing, squeeze)

## Prerequisites
- DaVinci Resolve (Free: letterbox, blur, overlay; Studio: Defocus, Lens Flare, Lens Distortion OFX)
- Basic node graph, Power Window, compositing modes
- Flare overlays (PNG/EXR) for Free version

## Core Concept

> **Four pillars: Aspect + Bokeh + Flare + Distortion** — each independently controllable in post.

---

## Node Structure

```
Node 01: CST / Input Transform
Node 02: Primary Grade
Node 03: [LETTERBOX] — 2.39:1 Mask (Output Sizing / Cropping)
Node 04: [OVAL BOKEH] — Defocus OFX (Studio) or Blur + Mask (Free)
Node 05: [FLARE] — Overlay / Lens Flare OFX
Node 06: [DISTORTION] — Lens Distortion OFX (subtle)
Node 07: Global Polish / Grain / LUT
```

---

## Step-by-Step Procedure

### 1. Aspect Ratio Mask (2.39:1)
**Timeline Settings (Recommended):**
- Timeline Resolution: **1920x804** (2.39:1) or **3840x1608**
- Image Scaling: **Scale full frame with crop**

**Alternative: Output Blanking**
- Project Settings → **Output Blanking** → **2.39:1**

**Alternative: Node Cropping (Node 03)**
- Color Page → **Sizing** → **Cropping**
- 1080p: Top 132px, Bottom 132px
- 4K: Top 264px, Bottom 264px

### 2. Oval Bokeh (Vertical Stretch)

**Studio: Defocus OFX (Best)**
- Effects → Resolve FX Blur → **Defocus**
- **Shape**: Anamorphic
- **Aspect Ratio**: **2.0-2.5** (vertical stretch = anamorphic bokeh)
- **Radius**: 5-15 (background only)
- **Mask**: Power Window (Circle, Inverted, Softness 100) → Background only
- **Track** window to camera/subject movement

**Free: Gaussian Blur + Mask**
- Node 04: **Gaussian Blur** (Radius 10-20)
- **Power Window** → Circle → **Inverted** → **Softness 100**
- **Stretch window vertically** → Oval shape
- Track background

### 3. Horizontal Lens Flares

**Best: Flare Overlay (Free + Studio)**
- Source: Anamorphic flare elements (PNG/EXR, horizontal streaks)
- Node 05: **Composite Mode: Screen/Add**
- Position/scale to **practical lights, sun, reflections**
- Color grade flare to match (cool/warm tint)

**Studio: Lens Flare OFX**
- Effects → Resolve FX Light → **Lens Flare**
- **Type**: Anamorphic / Streak
- **Streak Length**: 200-500
- **Position** on highlights
- **Tint** to grade palette

**Free: Directional Blur Streak**
- Solid Color generator → **Directional Blur** (Angle 90°, Distance 200+)
- Mask to highlights → **Screen mode**

### 4. Subtle Lens Distortion (Studio)
- **Lens Distortion OFX**
- **Barrel**: **-0.02 to -0.05** (slight curve)
- **Center**: Image center
- **Anamorphic Squeeze**: 1.33x or 2x sim (optional)

### 5. Vignette / Edge Falloff
- **Power Window** → Circle → **Inverted** → **Softness 100**
- **Gain/Lift**: -0.1 to -0.2
- **Or**: Vignette OFX → Shape: Anamorphic

---

## Parameter Presets

| Look | Letterbox | Bokeh Aspect | Flare Type | Distortion | Vignette |
|------|-----------|--------------|------------|------------|----------|
| **Classic Scope** | 2.39:1 | 2.0x | Blue streak | -0.03 | Light |
| **Netflix Scope** | 2.00:1 | 1.8x | Warm streak | -0.02 | Medium |
| **Vintage 70s** | 2.39:1 | 2.5x | Rainbow streak | -0.05 | Heavy |
| **Modern Clean** | 2.39:1 | 1.5x | Subtle streak | 0 | Light |
| **Music Video** | 2.39:1 | 2.0x | Multi-color | -0.04 | Colored |

---

## Free vs Studio Features

| Feature | Free | Studio |
|---------|------|--------|
| Letterbox/Crop | ✅ | ✅ |
| Blur + Mask (Oval Bokeh) | ✅ | ✅ |
| Flare Overlay (PNG/EXR) | ✅ | ✅ |
| Directional Blur (Streak) | ✅ | ✅ |
| Defocus OFX (True Bokeh) | ❌ | ✅ |
| Lens Flare OFX | ❌ | ✅ |
| Lens Distortion OFX | ❌ | ✅ |
| Optical Quality Flares | ❌ | ✅ |

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Letterbox on 16:9 export | Baked black bars | **Export 2.39:1 timeline** |
| Bokeh on foreground | Subject blurry | **Mask/Track background ONLY** |
| Flare not tracked | Floats wrong | **Track to light source** |
| Too much distortion | Funhouse mirror | **Subtle: -0.02 to -0.05** |
| Same flare every shot | Fake, repetitive | **Vary color/position/intensity** |
| No grain | Digital clean = fake | **Add film grain** |

---

## Advanced: Real Anamorphic Footage Pipeline

### De-squeeze (2x or 1.33x squeeze)
```
Node 01: Input (squeezed) → Sizing: 2x Horizontal stretch
Node 02: Primary
Node 03: Native oval bokeh (already oval)
Node 04: Native flares (enhance, don't fake)
Node 05: Native distortion (correct or enhance)
```

### Hybrid (Real + Post Enhance)
- Shoot 1.33x anamorphic → De-squeeze
- Post: Stronger flares, bokeh boost, distortion enhance

---

## Pro Tips

- **@jihadk__**: "200mm lens helped blurry edges but effect works with any lens. Move mask to adjust range."
- **@evgeny.m7**: "Just use Gaussian blur for outside circle mask" — Simple oval blur trick
- **@nnanna_prince_**: Works on Free DaVinci — Letterbox + Blur + Overlay = Free
- **Track everything** — Masks, flares, windows must move with camera
- **Vary per shot** — Same settings = template look
- **Grain is mandatory** — Digital clean kills the illusion

---

## Related Skills
- `davinci-resolve-letterbox-cinematic-ratio` — Aspect ratio masking
- `davinci-resolve-lens-flare-overlay` — Flare compositing
- `davinci-resolve-promist-slog3-dreamy` — Diffusion alternative
- `davinci-resolve-glow-halation-cinematic_caleboshi` — Glow for highlights

---

## References
- Source: @jihadk__ Instagram Reel (May 4, 2025)
- Hashtags: #davinciresolve #anamorphic #cinematic #filmmaking #videoediting
- Engagement: 2,858 likes, 34 comments
- Community: Free vs Studio discussion, international, high educational value