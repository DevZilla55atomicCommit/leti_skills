---
name: davinci-resolve-power-windows_davinciresolved
category: creative
description: "Power Windows in DaVinci Resolve — subject isolation, background separation, tracking, Outside Node technique for visual hierarchy and depth"
tags:
  - davinci-resolve
  - color-grading
  - power-windows
  - tracking
  - subject-isolation
  - background-separation
  - outside-node
  - visual-hierarchy
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKCmMw3xK1v/"
creator: "@davinciresolved"
vault_file: "Creative Grading & Looks/49-Power-Windows_davinciresolved_Subject-Background-Separation.md"
---

# Power Windows in DaVinci Resolve

## Overview
Fundamental technique for subject isolation and background separation using geometric masks (Power Windows) with tracking, softness control, and Outside Node workflow for dramatic yet subtle image depth.

## When to Use
- **Every narrative/commercial grade** with people or products
- Mixed lighting scenarios (window vs interior)
- Directing viewer attention
- Creating depth and dimension
- **Not for**: Flat, even lighting with no separation needed

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic node graph, color wheels knowledge
- Understanding of tracking (Tracker panel)

## Core Concept: Power Window = Spatial Selection

| Window Type | Best For |
|-------------|----------|
| **Circle/Oval** | Faces, heads, products (most natural) |
| **Square/Rectangle** | Screens, signs, architectural |
| **Linear Gradient** | Horizons, sky, vignettes |
| **Radial Gradient** | Vignettes, spotlights |
| **Custom (Bezier)** | Complex shapes, Magic Mask alternative |

## Node Structure

```
Node 01: Base Grade (CST, Balance, Contrast)
Node 02: Subject Enhancement (Power Window — Circle/Oval, Softness 100, Tracked)
Node 03: Background Treatment (Inverted Window OR Outside Node)
Node 04: Global Polish / Creative Look / LUT
```

## Step-by-Step Procedure

### 1. Create Subject Window (Node 02)
1. Select Node 02 → **Window Palette** → **Circle/Oval**
2. Position/size over **subject face/upper body**
3. **Softness: 80-100 (MAX)** — Critical for invisible blend
4. **Tracker** → Track Forward/Back (analyze motion)
5. Verify track — adjust keyframes if drift

### 2. Enhance Subject (Inside Window)
**Color Wheels (inside window only):**
| Wheel | Adjustment | Typical Range |
|-------|------------|---------------|
| **Lift** | Slight brighten | +0.01 to +0.03 |
| **Gamma** | Warmth + brightness | +0.02 to +0.05, Hue 30-50° |
| **Gain** | Specular pop | +0.01 to +0.03 |
| **Contrast** | Definition | +5 to +15 |
| **Saturation** | Color life | +5 to +15 |

### 3. Background Treatment (Node 03)

**Option A: Invert Same Window**
- Copy Node 02 window → Paste to Node 03 → **Click Invert**

**Option B: Outside Node (Recommended)**
- Right-click Node 02 → **Add Outside Node** → Creates Node 03 automatically
- Node 03 = Everything EXCEPT window (perfect inverse)

**Background Adjustments (Inside Window/Inverted):**
| Parameter | Adjustment | Why |
|-----------|------------|-----|
| **Temperature** | -50 to -150 (Cool) | Recedes, separates |
| **Tint** | Slight green | Complements warm subject |
| **Lift/Exposure** | -0.02 to -0.05 | Darker background = depth |
| **Contrast** | -10 to -20 | Flatter, less competition |
| **Saturation** | -15 to -30% | Muted, subject pops |

### 4. Global Polish (Node 04)
- Film LUT / Creative Look
- Global contrast/saturation
- Grain, halation, vignette
- **Re-check subject** — LUT may affect windowed area

## Parameter Reference

| Setting | Subject (Inside) | Background (Outside) |
|---------|------------------|---------------------|
| **Window Shape** | Circle/Oval | Same (inverted) |
| **Softness** | **100** | **100** (shared) |
| **Tracking** | Required if motion | Auto (inverted) |
| **Temp** | +50 to +150 | -50 to -150 |
| **Exposure** | +0.1 to +0.3 | -0.1 to -0.3 |
| **Contrast** | +10 to +20 | -10 to -20 |
| **Saturation** | +10 to +20 | -15 to -30 |

## Advanced: Outside Node Technique

```
Node 02: Power Window (Subject) → Enhancements
    │
    └─ Right-click → "Add Outside Node"
           │
           ▼
Node 03: Automatic Inverse Window → Background Treatment
```

**Benefits:**
- Perfect mathematical inverse (no edge artifacts)
- Single window to maintain
- Changes to Node 02 window auto-update Node 03

## Pro Tips from Community

- **@b.arvay**: "Add window → invert → reduce background exposure. Then Outside Node → bump exposure + contrast. More dramatic, yet subtle separation."
- **@kbem.mp4**: "Could you do this with a magic mask?" → **Yes!** Magic Mask (Studio) = AI subject isolation, faster for complex motion
- **Softness = 100** is non-negotiable for invisible windows
- **Track every shot** — even locked-off (micro-jitter)

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Softness < 80 | Hard ellipse visible | **Softness = 100** |
| No tracking | Window drifts | Track Forward + Back |
| Over-bright subject | "Spotlight" look | Reduce exposure, increase softness |
| Ignoring background | Flat, 2D image | Always treat inverted |
| Same values all shots | Inconsistent | Per-shot adjust, use gallery stills |
| Window too small | Cut off ears/hair | Cover full subject + margin |

## Variations

### Multiple Windows (Single Node)
- Window 1: Face (Softness 100)
- Window 2: Hands (Softness 80)
- Window 3: Product (Softness 60)
- Each with independent corrections

### Gradient Window (Sky/Horizon)
- Linear Gradient → Top of frame
- Cool/warm sky independently
- Softness: 50-80 (feathered horizon)

### Power Window + Qualifier (Precision)
```
Node 02: Power Window (Subject region)
    └── Qualifier (HSL) → Skin tones only
        └── Corrections affect ONLY skin in window
```

### Keyframed Manual Track
- Tracker fails → Manual keyframes
- Set keyframes every 5-10 frames
- Interpolate between

## Related Skills
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Oval window at 100 softness (fundamental)
- `davinci-resolve-skin-tones-right_mansourmelouli` — Power window for skin isolation
- `davinci-resolve-promist-slog3-dreamy` — Diffusion alternative to window separation
- `davinci-resolve-cinematic-contrast-trick_diginet` — Parallel density vs window separation

## References
- Source: @davinciresolved Instagram Reel (May 24, 2025)
- Hashtags: #davinci #videoediting #colorgrading
- Community: "You're like The Hoof GP of davinci tutorials 🐄" — @smashflick
- Pro Tip: @b.arvay Outside Node technique
- Magic Mask Q: @kbem.mp4