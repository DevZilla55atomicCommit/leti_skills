---
name: davinci-resolve-parallel-density-layer-mixer
description: "Parallel Density technique using Layer Mixer in DaVinci Resolve — blend graded and ungraded signals for controllable film-like density without affecting color balance."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Parallel Density, Layer Mixer, Density, Film Look]
    source_url: "https://www.instagram.com/reel/DXxCYbyIi-8/"
    source_creator: "@harmony_the_artistic_colorist / @davinciresolved"
    source_date: "2025-04-30"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Parallel Density, Layer Mixer, Density, Film Look, Color Grading, Color60, Harmony, davinciresolved]
---

# DaVinci Resolve: Parallel Density — Layer Mixer Technique

**Source:** [@harmony_the_artistic_colorist Instagram Reel](https://www.instagram.com/reel/DXxCYbyIi-8/) — "Day 17/60: COLOR60 — Parallel density in DaVinci Resolve"

**Original Credit:** @davinciresolved (original video/visuals/content)

## Technique Overview

**Problem:** Standard saturation/contrast adjustments affect both color and luminance — hard to get pure "density" (filmic richness) without color shifts.

**Solution:** **Parallel Density** — Use **Layer Mixer** to blend a density-adjusted version (via curves/Hue vs Lum) with the original at reduced opacity. Separates density from color balance.

> **Series:** COLOR60 — Day 17 of 60 color grading challenge
> **Original Creator:** @davinciresolved

---

## Key Concept: Density vs Saturation

| Property | Saturation | Density (Parallel) |
|----------|------------|-------------------|
| **What changes** | Chroma (distance from gray) | Luminance of saturated colors |
| **Color balance** | Often shifts | **Preserved** |
| **Luminance** | Increases | **Decreases** (richer) |
| **Feel** | "Digital pop" | "Filmic depth" |

---

## Node Structure

```
Node 01: Base Grade (Corrected, Balanced)
Node 02: **DENSITY NODE** (Serial)
  → Custom Curves: Hue vs Lum (pull saturated hues down)
  → OR: Color Warper → Hue vs Lum
Node 03: **LAYER MIXER** (Parallel)
  ├── Input 1: Base Grade (Node 01)
  └── Input 2: Density Node (Node 02)
      → Composite Mode: **Normal** (or Soft Light)
      → **Opacity: 20-50%** (density intensity)
Node 04: Output CST + Gamut Mapping
```

---

## Step-by-Step Procedure

### 1. Create Density Node (Node 02)
| Tool | Settings |
|------|----------|
| **Custom Curves → Hue vs Lum** | Pull down luminance on saturated hues |
| **Target Hues** | Skin (20°-40°): -0.02; Foliage (100°-140°): -0.10; Sky (180°-220°): -0.15 |
| **Protect Skin** | Anchor points at 30°/40° = 0.0 change |

### 2. Layer Mixer Setup (Node 03)
| Setting | Value |
|---------|-------|
| **Composite Mode** | Normal (or Soft Light for glow) |
| **Opacity** | 25-40% (start 30%) |
| **Layer Order** | Input 1 = Base (bottom), Input 2 = Density (top) |

### 3. Fine-Tune Density
| Control | Range | Effect |
|---------|-------|--------|
| **Layer Mixer Opacity** | 10-50% | Overall density strength |
| **Hue vs Lum Curve Depth** | -0.05 to -0.20 | Per-hue density |
| **Blend Mode** | Normal / Soft Light / Overlay | Character |

---

## Pro Tips from Comments

**@ulterior_visuals:** *"Love that! What about the density slider in the colour slice page?"*
→ **Color Slice** has Density slider (Resolve 18.5+) — alternative to Hue vs Lum curves.

**@aik_kai_:** *"Check your CST bro"*
→ **Always verify CST pipeline** — density works best in proper color space (DWG Intermediate).

**@axelk:** *"Do you need to disable any of the channels?"*
→ **No** — Layer Mixer blends full RGB. Channels disabled only if using specific channel isolation.

**@johnhafner:** *"How is this different than increasing luminance gain?"*
→ **Luminance Gain** = lifts entire image. **Parallel Density** = only affects saturated colors, preserves neutrals/skin.

**@cashvizionz:** *"🔥"*
→ Community loves this technique!

---

## When to Use Parallel Density

| Scenario | Use Parallel Density? |
|----------|----------------------|
| **Filmic look** | ✅ Yes — core technique |
| **Skin tone protection** | ✅ Yes — anchor skin in Hue vs Lum |
| **Landscape/foliage depth** | ✅ Yes — deepen greens naturally |
| **High-key / bright scenes** | ✅ Yes — add richness without mud |
| **Color grading log footage** | ✅ Yes — after CST to DWG Intermediate |
| **Quick social media grade** | Maybe — use Color Slice Density slider instead |

---

## Alternative: Color Slice Density (Resolve 18.5+)

```
Node 02: Color Slice OFX
  → For each hue slice (Red, Yellow, Green, Cyan, Blue, Magenta):
      → Density: -10 to -30
      → Saturation: 0 (or slight +)
      → Luminance: 0
  → Global Density: -10 to -20
```

---

## Related Techniques

- `davinci-resolve-hue-vs-luminance-density-saturation` — @ulterior_visuals subtractive saturation
- `davinci-resolve-soft-light-glow-cinematic-emotion` — @mastermotion Soft Light glow
- `davinci-resolve-cinematic-look-post-production-philosophy` — @mastermotion full pipeline

---

## Tags

`#davinciresolve` `#colorgrading` `#parallel-density` `#layer-mixer` `#density` `#film-look` `#color60` `#harmony` `#davinciresolved`