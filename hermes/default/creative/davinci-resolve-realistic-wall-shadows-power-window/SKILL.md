---
name: davinci-resolve-realistic-wall-shadows-power-window
description: "Create realistic wall shadows using Power Windows + tracking in DaVinci Resolve — shape light falloff on walls for cinematic depth and environmental integration."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Power Windows, Shadows, Lighting, Cinematic]
    source_url: "https://www.instagram.com/reel/DX98iHhIq-S/"
    source_creator: "@harmony_the_artistic_colorist"
    source_date: "2025-05-05"
    vault_category: "Masking & Power Windows"
    skill_level: "Intermediate"
    tags: [Power Window, Shadow, Wall, Tracking, Cinematic Lighting, Color60, Realistic Shadows]
---

# DaVinci Resolve: Realistic Wall Shadows with Power Windows

**Source:** [@harmony_the_artistic_colorist Instagram Reel](https://www.instagram.com/reel/DX98iHhIq-S/) — "Day 22/60: COLOR60 — Realistic Wall Shadows in DaVinci"

## Technique Overview

Create **realistic shadows cast on walls** using **Power Windows + Tracking** — simulates practical lighting interaction with environment. Adds cinematic depth, grounds subjects in space.

> **Original Credit:** @davinciresolved (original video/visuals/content)
> **Series:** COLOR60 — Day 22 of 60

---

## Node Structure

```
Node 01: Base Grade (Corrected, Balanced)
Node 02: **WALL SHADOW NODE** (Serial after base)
  └── Power Window (Custom Shape)
  └── Exposure / Lift / Gamma adjustment
  └── Tracker (if camera/subject moves)
Node 03: Optional — Skin Protection (Layer Mixer)
Node 04: Output CST + Gamut Mapping
```

---

## Step-by-Step Procedure

### 1. Create Shadow Node (Node 02)
- Add Serial Node after base grade
- Label: **"WALL SHADOW"**

### 2. Draw Power Window Shape
| Setting | Value | Notes |
|---------|-------|-------|
| **Shape** | Custom (Bézier) | Trace wall contour where shadow falls |
| **Type** | **Custom Curve** | Click points along shadow edge |
| **Softness** | **0.3-0.5** (Inner) / **0.6-0.8** (Outer) | Feather for natural falloff |
| **Position** | Match wall plane | Perspective-correct if possible |

> **Pro Tip from @khaleeq96:** *"Instead of duplicating the clip just for using the Magic Mask, you can add a Layer node after the power window and apply the Magic Mask there and it will give you the same result."*

### 3. Shadow Grading (Inside Power Window)
| Parameter | Value | Why |
|-----------|-------|-----|
| **Exposure / Offset** | -0.3 to -0.8 | Darken wall where shadow falls |
| **Lift (Shadows)** | -0.1 to -0.2 | Deepen shadow base |
| **Gamma (Midtones)** | -0.05 to -0.15 | Shape falloff |
| **Contrast** | +5 to +15 | Define shadow edge |
| **Saturation** | -10 to -20% | Shadows less saturated |
| **Color Temp** | Slightly cool (-50 to -100K) | Natural shadow color |

### 4. Track the Shadow (If Camera/Subject Moves)
1. Select Power Window
2. **Tracker** panel → **Track Forward** (or backward)
3. **Tracking Mode:** Perspective (for wall planes) or Planar
4. **Keyframe** shape if shadow geometry changes

### 5. Refine with Qualifier (Optional)
- Qualifier → **Luma Range:** Shadows only (0-0.3)
- Ensures adjustment only affects dark areas

---

## Parameter Presets by Lighting Scenario

| Scenario | Exposure | Softness | Temp Shift | Falloff |
|----------|----------|----------|------------|---------|
| **Hard Sun (Direct)** | -0.6 to -0.8 | 0.2-0.3 (sharp) | -100K | Sharp edge |
| **Window Light (Soft)** | -0.3 to -0.5 | 0.5-0.7 (feathered) | -50K | Gradual |
| **Practical Lamp** | -0.2 to -0.4 | 0.6-0.8 (very soft) | +50K (warm) | Circular |
| **Overcast/Diffuse** | -0.15 to -0.3 | 0.7-0.9 (very soft) | 0K | Barely visible |

---

## Advanced: Layer Node Magic Mask Alternative

Per comment by @khaleeq96:
```
Layer Mixer
├── Input 1: Main Grade
└── Input 2: Shadow Layer
    ├── Power Window (Wall shape)
    ├── Magic Mask (AI subject isolation) — *on Layer Node, not clip*
    ├── Exposure -0.5
    └── Composite: Multiply (or Normal with Alpha)
```
→ Isolates subject from wall automatically, cleaner than manual window

---

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Shadow floats/detaches | Bad track | Re-track with Perspective mode |
| Shadow too hard/soft | Wrong softness | Match light source quality |
| Shadow wrong color | No temp shift | Shadows = cooler (blue shift) |
| Affects subject | Window too big | Tighten window, add qualifier |
| Jittery edge | Track slip | Manual keyframe cleanup |

---

## Verification Checklist

- [ ] Shadow shape matches subject silhouette
- [ ] Perspective correct on wall plane
- [ ] Falloff matches light source quality
- [ ] Shadow color cooler than lit wall
- [ ] Tracks solidly through shot
- [ ] Subject unaffected (qualifier/window)
- [ ] A/B: Adds depth, feels "in camera"

---

## Related Techniques

- `davinci-resolve-masking-power-masking` — Loris Marie Power Masking (Radial + Magic Mask)
- `davinci-resolve-depth-map-grading` — Mastermotion Depth Map (FG/MG/BG layers)
- `davinci-resolve-cinematic-haze-effect` — Atmospheric depth via haze
- `davinci-resolve-soft-light-glow-cinematic-emotion` — Glow for light sources

---

## Tags

`#davinciresolve` `#powerwindow` `#shadow` `#tracking` `#cinematic` `#lighting` `#color60` `#harmony` `#masking` `#environment`