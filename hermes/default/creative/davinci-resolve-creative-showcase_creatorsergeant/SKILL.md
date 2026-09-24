---
name: davinci-resolve-creative-showcase_creatorsergeant
category: creative
description: "Creative grading showcase combining Hue vs Hue color shifting, anamorphic lens flares, and Power Window object tracking — late night experiment demonstrating multi-technique integration"
tags:
  - davinci-resolve
  - color-grading
  - creative-showcase
  - hue-vs-hue
  - color-shift
  - anamorphic-flare
  - car-tracking
  - mask-tracking
  - power-window
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DFQ5MG7uoXa/"
creator: "@creatorsergeant"
vault_file: "Creative Grading & Looks/58-Creative-Showcase_creatorsergeant_Hue-vs-Hue-Flares-Tracking.md"
---

# Late Night Creative Grading Showcase — Hue vs Hue + Flares + Tracking

## Overview
@creatorsergeant's creative experiment combining multiple advanced techniques: **Hue vs Hue color shifting**, **anamorphic lens flares**, and **Power Window object tracking** — demonstrates real-world integration of isolated techniques.

## When to Use
- Creative exploration / skill stacking
- Music videos, commercials, narrative moments
- Demonstrating technique combination
- **Not for**: Standard delivery grades (too experimental)

## Prerequisites
- DaVinci Resolve (Studio for Lens Flare OFX; Free: overlays)
- Power Window tracking proficiency
- Custom Curves (Hue vs Hue) knowledge
- Node graph organization

## Core Concept

> **Real grades combine techniques** — Isolation + Hue Shift + Optical FX = Integrated Look

---

## Node Structure (Reconstructed)

```
Node 01: CST / Input Transform
Node 02: Primary Balance
Node 03: [POWER WINDOW + TRACKER] — Car Isolation
    ├── Hue vs Hue Curve (Color Shift)
    └── Curves/Wheels (Exposure Match)
Node 04: [LENS FLARE OFX / OVERLAY] — Anamorphic Flares
    ├── Tracked to Practical Lights
    └── Composite: Screen/Add
Node 05: Global Creative Grade (Teal/Orange, etc.)
Node 06: Polish (Grain, Vignette, LUT)
```

---

## Technique 1: Hue vs Hue Color Shift (Node 03)

### Setup
1. Power Window on car → **Tracker** → Track Forward/Back
2. **Softness**: 20-40 (blend edge)
3. Custom Curves → **Hue vs Hue**
4. **Source Hue**: Car's original color (sample with picker)
5. **Target Hue**: Desired color (e.g., red ~0°)
6. **Anchor neighbors** to limit range

### Community Confirmation
- **@mithune91**: "Hue vs hue me color change Kiya na bhai" — Yes, Hue vs Hue for color change

---

## Technique 2: Anamorphic Lens Flares (Node 04)

### Studio: Lens Flare OFX
- Effects → Resolve FX Light → **Lens Flare**
- **Type**: Anamorphic / Streak
- **Streak Length**: 200-500
- **Position**: On specular highlights (headlights, reflections)
- **Color**: Grade-matched (cool/warm)
- **Track**: If camera moves, track flare to light source

### Free: Flare Overlay
- PNG/EXR anamorphic flare elements
- Composite: **Screen** or **Add**
- Position/scale/rotate to highlights
- Track if needed

### Community Question
- **@ben_daniel11**: "How you make the anamorphic light?"

---

## Technique 3: Power Window Object Tracking (Node 03)

### Procedure
1. **Window Palette** → Circle or Custom (car shape)
2. **Position/Size** over car
3. **Tracker** (bottom toolbar) → **Track Forward/Back**
4. **Analyze** — Resolve tracks position/scale/rotation
5. **Refine**: Adjust keyframes if drift
6. **Softness**: 20-40 for moving objects

### Community Question
- **@alex_mirzayan**: "How did you do the tracking of the car with the mask?"

---

## Integration: Making It "Realistic"

### Key Principles (from "Realistic switch to red" comment)
1. **Exposure Match** — Shifted object matches scene lighting
2. **Edge Blend** — Window softness hides isolation
3. **Flare Consistency** — Flares match new color temp
4. **Global Grade** — Creative look unifies everything

### Workflow Order Matters
```
Isolate (Window) → Shift (Hue vs Hue) → Match (Curves) → Flare (OFX) → Unify (Global)
```

---

## Parameter Reference

| Technique | Key Params | Typical Values |
|-----------|------------|----------------|
| **Power Window** | Shape, Softness | Custom/Circle, 20-40 |
| **Tracker** | Mode, Frames | Position+Scale+Rot, Full clip |
| **Hue vs Hue** | Source Hue, Target Hue | Sample → Target, ±30° anchors |
| **Lens Flare OFX** | Type, Streak, Color | Anamorphic, 300, Grade-matched |
| **Flare Overlay** | Mode, Opacity | Screen/Add, 30-70% |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Hard window edge | Visible mask line | **Softness 20-40** |
| Track drift | Window off object | **Manual keyframes** |
| Hue shift bleeds | Adjacent colors change | **Anchor neighboring hues** |
| Flare static | Doesn't follow light | **Track flare to source** |
| Color shift flat | Unrealistic | **Match exposure/contrast** |

---

## Pro Tips

- **@creatorsergeant**: Late night = creative freedom, experiment!
- **@ateam.alex**: "Tutorial coming soon??" — High demand for breakdown
- **Stack techniques** — Real work combines isolation, hue, optical FX
- **Order matters** — Isolate → Shift → Flare → Unify
- **Test on movement** — Tracking quality reveals on motion

---

## Related Skills
- `davinci-resolve-split-tone-studio-free` — Hue vs Hue shifting
- `davinci-resolve-anamorphic-look_jihadjk` — Anamorphic flares
- `davinci-resolve-power-windows_davinciresolved` — Window tracking
- `davinci-resolve-texture-pop_creatorsergeant` — Same creator, Studio effects

---

## References
- Source: @creatorsergeant Instagram Reel (Jan 25, 2025)
- Hashtags: #dabinciresolve #colorgrading
- Engagement: 3,195 likes, 42 comments
- Community: Technique questions (tracking, flares, hue shift), tutorial requests