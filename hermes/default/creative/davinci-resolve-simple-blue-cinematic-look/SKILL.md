---
name: davinci-resolve-simple-blue-cinematic-look
description: "Simple blue/cinematic look in DaVinci Resolve — node combo for teal/orange cinematic grade using curves and color wheels."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Cinematic Look, Blue/Teal, Color Wheels, Curves]
    source_url: "https://www.instagram.com/reel/DWACYNFESlj/"
    source_creator: "@ryanherrickk"
    source_date: "2025-04-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner to Intermediate"
    tags: [Cinematic Look, Blue/Teal, Color Wheels, Curves, Node Combo, Ryan Herrick]
---

# DaVinci Resolve: Simple Blue/Cinematic Look — @ryanherrickk

**Source:** [@ryanherrickk Instagram Reel](https://www.instagram.com/reel/DWACYNFESlj/) — "How to get that simple blue/cinematic look inside of DaVinci Resolve!"

## Technique Overview

A simple, repeatable node structure for achieving a clean blue/cinematic (teal/orange) look using native DaVinci Resolve tools. Works in Free and Studio versions.

> "I've been using this node combo for quite some time now!" — @ryanherrickk

---

## Node Structure

```
Node 01: CST (Camera Log → DWG Intermediate Linear)
Node 02: PRIMARY BALANCE (Linear Gain, Luma Mix=0, Pivot=0.335)
Node 03: CREATIVE GRADE — "CINEMATIC BLUE"
  ├── Color Wheels: Gain (Warm), Lift (Cool/Teal), Gamma (Neutral)
  ├── Curves: Hue vs Hue (shift greens→teal, reds→orange)
  └── Curves: Hue vs Sat (protect skin, boost key colors)
Node 04: OUTPUT CST (DWG → Rec.709 + Gamut Mapping)
```

---

## Step-by-Step

### 1. CST Pipeline (Nodes 01 & 04)
| Node | Input | Output |
|------|-------|--------|
| 01 | Camera Log (S-Log3/BRAW/LogC) | DWG Intermediate Linear |
| 04 | DWG Intermediate Linear | Rec.709 Gamma 2.4 + Gamut Map |

### 2. Primary Balance (Node 02)
- **Color Wheels: Linear** mode
- **Key Panel → Luma Mix = 0**
- **Gain Pivot = 0.335**
- Parade RGB → R=G=B on neutrals
- Vectorscope → Neutral centered

### 3. Cinematic Blue Look (Node 03)

**Color Wheels:**
| Wheel | Hue | Saturation | Purpose |
|-------|-----|------------|---------|
| **Gain (Highlights)** | ~35° (Warm/Orange) | 15-25 | Skin warmth, golden hour |
| **Lift (Shadows)** | ~205° (Cool/Teal) | 15-25 | Cinematic cool shadows |
| **Gamma (Midtones)** | Neutral (Center) | 0 | Preserve midtone balance |
| **Offset** | Slight warm | 2-5 | Overall warmth |

**Custom Curves — Hue vs Hue:**
| Source Hue | Target Hue | Purpose |
|------------|------------|---------|
| Greens (100°-140°) | → 180°-200° (Teal) | Foliage to cinematic teal |
| Reds (0°-30°, 330°-360°) | → 20°-40° (Orange) | Skin/warmth to orange |
| Cyans (180°-220°) | → 200°-210° (Deeper teal) | Sky/water depth |

**Custom Curves — Hue vs Sat:**
| Hue Range | Saturation | Purpose |
|-----------|------------|---------|
| Skin (25°-45°) | -5 to -10% | Protect skin from oversat |
| Teal (180°-220°) | +10 to +20% | Boost cinematic teal |
| Orange (30°-50°) | +5 to +15% | Enhance warmth |

---

## Key Principles

| Principle | Application |
|-----------|-------------|
| **CST First** | All grading in DWG Intermediate |
| **Linear Balance** | Luma Mix=0, Pivot=0.335 |
| **Split Tone** | Warm highlights + Cool shadows |
| **Hue Shifting** | Greens→Teal, Reds→Orange |
| **Skin Protection** | Desaturate skin hues slightly |
| **Gamut Safety** | Output CST + Saturation Mapping |

---

## Pro Tips

1. **Shot Match:** Copy Node 02 (Primary) across scene
2. **Intensity Control:** Key Output Gain on Node 03 (50-100%)
3. **Per-Shot Tweak:** Adjust Node 03 curves per shot
4. **LUT Alternative:** This node tree replaces "cinematic LUTs"
5. **Free Version Compatible:** All tools available in Free

---

## Comment Insights

**@rma_wild, @samy_aitchikh, @dee_graph1cs, @ziko_no_p01, @felipe_prefetti, @mr_shaf_obrien, @tf_kaleem, @milan2797, @allfuckerrr, @jeshua.vire, @_junior.cakacaka_** — All commented "text" or "Text" — likely requesting the text animation pack mentioned in caption.

---

## Related Techniques

- `davinci-resolve-complementary-color-grading` — Teal/Orange deep dive
- `davinci-resolve-cinematic-look-post-production-philosophy` — Full 9-node template
- `davinci-resolve-split-tone-studio-free` — Built-in split tone
- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer for WB

---

## Tags

`#davinciresolve` `#colorgrading` `#cinematic-look` `#blue-teal` `#split-tone` `#ryanherrickk` `#color-wheels` `#curves`