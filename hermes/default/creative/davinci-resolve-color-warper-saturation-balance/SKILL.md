---
name: davinci-resolve-color-warper-saturation-balance
description: "Balance saturation using Color Warper in DaVinci Resolve — precise saturation control per hue range, alternative to saturation vs saturation curves."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Color Warper, Saturation, Color Separation]
    source_url: "https://www.instagram.com/reel/DXaAQXhiNbH/"
    source_creator: "@harmony_the_artistic_colorist / @davinciresolved"
    source_date: "2025-04-25"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Color Warper, Saturation, Color Balance, Color Separation, COLOR60, Harmony, davinciresolved]
---

# DaVinci Resolve: Balance Saturation with Color Warper — @harmony_the_artistic_colorist (COLOR60 Day 9)

**Source:** [@harmony_the_artistic_colorist Instagram Reel](https://www.instagram.com/reel/DXaAQXhiNbH/) — "Day 9/60: COLOR60 — Balance Saturation with Color Warper in DaVinci Resolve"

**Original Credit:** @davinciresolved (original video/visuals/content)

## Technique Overview

**Problem:** Global saturation affects all colors equally — no control over which hues get saturated/desaturated.

**Solution:** **Color Warper** → **Saturation tab** — precise per-hue saturation control for color separation and balance.

> **Series:** COLOR60 — Day 9 of 60 color grading challenge
> **Original Creator:** @davinciresolved

---

## Key Concept: Color Warper Saturation Grid

The Color Warper panel has a **Saturation** mode that displays a hue circle with saturation intensity as radius — drag points to increase/decrease saturation per hue range.

| Feature | Benefit |
|---------|---------|
| **Visual Grid** | See saturation distribution at a glance |
| **Per-Hue Control** | Target specific color ranges |
| **Smooth Transitions** | Auto-interpolation between points |
| **Real-time Scope Sync** | Vectorscope updates live |

---

## Step-by-Step Procedure

### 1. Open Color Warper
- Color Page → **Color Warper** panel (right side)
- Select **Saturation** mode (icon: hue circle with radial lines)

### 2. Analyze Current Saturation
- Observe grid: distance from center = saturation
- Identify oversaturated/undersaturated hues

### 3. Balance Saturation
| Target Hue | Action | Why |
|------------|--------|-----|
| **Skin (25°-45°)** | **Decrease** slightly (-5 to -15%) | Natural skin, prevent orange |
| **Foliage (100°-140°)** | **Decrease** or maintain | Avoid "video green" |
| **Sky/Water (180°-220°)** | **Increase** slightly (+10-20%) | Cinematic teal separation |
| **Warm Highlights (30°-50°)** | Maintain or slight boost | Golden hour warmth |
| **Shadows (200°-240°)** | Slight decrease | Clean, deep shadows |

### 4. Use Multiple Points for Smooth Curves
- Add 3-5 points per hue range
- Avoid sharp angles (causes banding)
- Test: Toggle node ON/OFF — skin should stay natural

---

## Alternative: Sat vs Sat Curve (Per Comments)

**@kaxtru:** *"Sat vs sat curve is way faster and more precise to do this adjustment"*
**@alexaveryphotography:** *"In Photolab I'd just drop some control points... slider to prevent over-saturation of colours that applies globally and should start with the most saturated areas"*

### Sat vs Sat Curve Method:
1. Custom Curves → **Sat vs Sat**
2. X-axis: Input Saturation | Y-axis: Output Saturation
3. **Low sat** → Boost slightly (separation)
3. **High sat** → Pull down (prevent oversat)
4. **Mid sat** → Maintain

---

## Pro Tips from Comments

1. **@alexaveryphotography:** Global "over-saturation prevention" slider should target most saturated areas first
2. **@russell_cane_cinema:** *"🔥🔥"*
3. **@molyfts:** *"Can we do it in sat vs sat curve does it provide a different result?"* → Yes, different math, similar result
3. **@tellsulli:** *"This amazing"*

---

## When to Use Color Warper vs Curves

| Scenario | Tool |
|----------|------|
| **Visual, intuitive** | Color Warper Saturation grid |
| **Precision, repeatable** | Sat vs Sat / Hue vs Sat curves |
| **Global saturation limit** | Sat vs Sat (high sat pull-down) |
| **Per-hue creative shifts** | Color Warper / Hue vs Sat |
| **Skin-safe saturation** | Both work — curves more precise |

---

## Related Techniques

- `davinci-resolve-hue-vs-luminance-density-saturation` — Density via Hue vs Lum
- `davinci-resolve-parallel-density-layer-mixer` — Parallel density blend
- `davinci-resolve-split-tone-studio-free` — Split tone for color separation

---

## Tags

`#davinciresolve` `#colorgrading` `#color-warper` `#saturation` `#color-balance` `#color-separation` `#color60` `#harmony` `#davinciresolved`