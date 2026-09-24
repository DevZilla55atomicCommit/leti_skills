---
name: davinci-resolve-advanced-black-white-rgb-mixer
description: "Advanced Black & White technique in DaVinci Resolve using RGB Mixer in Monochrome mode with Luma blend composite for precise tonal control."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Black & White, RGB Mixer, Monochrome, Luma Blend]
    source_url: "https://www.instagram.com/p/DW8pSzwjESq/"
    source_creator: "@marcoherbst.work"
    source_date: "2025-04-10"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Black & White, RGB Mixer, Monochrome, Luma Composite, Cinematic B&W, Marco Herbst]
---

# DaVinci Resolve: Advanced Black & White — RGB Mixer Monochrome Technique

**Source:** [@marcoherbst.work Instagram Post](https://www.instagram.com/p/DW8pSzwjESq/) — "Advanced Black & White in DaVinci Resolve – volle Kontrolle mit dem RGB Mixer"

## Technique Overview

**Problem:** Standard desaturation (Saturation = 0) loses all tonal control — colors convert to gray with fixed luminance ratios.

**Solution:** **RGB Mixer + Monochrome mode + Luma Composite** — precise control over how each color channel maps to grayscale, exactly like B&W film filters.

> "Die meisten machen Schwarzweiß einfach über Desaturation… und verlieren dabei komplett die Kontrolle über ihr Bild. Mit dieser Technik bestimmst du exakt, wie Farben in Graustufen übersetzt werden – für einen deutlich cinematischeren Black & White Look."

---

## Node Structure

```
Node 01: Base Grade (Corrected)
Node 02: **LUMA NODE** (Serial)
  → Balance exposure, contrast, curves
Node 03: **BW NODE** (Serial)
  → RGB Mixer → **Monochrome: ON**
  → Adjust R/G/B channel weights
Node 04: **COMPOSITE** (Luma Blend)
  → BW Node → Composite Mode: **Luminance**
  → Auto Normalize: ON
```

---

## Step-by-Step Procedure

### 1. Create Luma Node (Node 02)
- Add Serial Node after base grade
- Label: **"LUMA"**
- Adjust: Exposure, Contrast, Pivot, Curves
- **Purpose:** Clean luminance foundation before B&W conversion

### 2. Create BW Node (Node 03)
- Add Serial Node after Luma
- Label: **"BW"**
- Open **RGB Mixer** panel
- **Enable: Monochrome** (checkbox)
- Adjust channel weights:
  | Channel | Typical Range | Effect |
  |---------|---------------|--------|
  | **Red** | 0.2–0.5 | Skin tones, lips, warmth |
  | **Green** | 0.3–0.6 | Foliage, midtones, luminance |
  | **Blue** | 0.1–0.3 | Sky, shadows, cool tones |
  | **Sum** | ≈ 1.0 | Maintain overall brightness |

> **Pro Tip:** Work actively with color channels in RGB Mixer for separation/depth.

### 3. Luma Composite (Node 04)
- Add Serial Node after BW
- **Composite Mode: Luminance**
- **Auto Normalize: ON**
- This blends BW luminance with Luma node's color (if any) or preserves clean tonal structure

---

## Channel Weight Guidelines

| Look | Red | Green | Blue | Effect |
|------|-----|-------|------|--------|
| **Standard B&W** | 0.30 | 0.59 | 0.11 | Rec.709 luminance |
| **Portrait/Skin** | 0.40 | 0.45 | 0.15 | Lift skin, smooth tones |
| **Landscape/Drama** | 0.25 | 0.50 | 0.25 | Sky separation, clouds |
| **High Contrast** | 0.35 | 0.40 | 0.25 | Deep shadows, punchy |
| **Infrared Look** | 0.10 | 0.80 | 0.10 | Foliage bright, sky dark |
| **Red Filter (B&W Film)** | 0.50 | 0.30 | 0.20 | Dark sky, light skin |
| **Green Filter** | 0.20 | 0.60 | 0.20 | Foliage separation |
| **Blue Filter** | 0.15 | 0.25 | 0.60 | Moody, dark skin |

---

## Why This Beats Desaturation

| Desaturation (Sat=0) | RGB Mixer Monochrome |
|----------------------|---------------------|
| Fixed Rec.709 weights | **Fully adjustable per channel** |
| No creative control | **Artistic filter simulation** |
| Flat, muddy grays | **Separation & depth** |
| Skin often too dark | **Skin tone control** |
| Sky blows out | **Sky/Cloud separation** |

---

## Pro Tips from Comments

**@siimkristjanpariis.ee:** *"Whats different about it compared to just reducing saturation to 0 and adjusting the contrast with primary wheels?"*
→ **Answer:** Desaturation uses fixed luminance coefficients. RGB Mixer lets you simulate color filters (red, green, blue, yellow) for creative tonal mapping.

**Auto Normalize** keeps overall brightness stable while you adjust channel mix.

---

## Verification Checklist

- [ ] Luma node: clean exposure/contrast base
- [ ] BW node: Monochrome ON in RGB Mixer
- [ ] Channel weights sum ≈ 1.0
- [ ] Composite Mode: Luminance
- [ ] Auto Normalize: ON
- [ ] Skin tones render as intended
- [ ] Sky/clouds have separation
- [ ] No clipped highlights/crushed blacks
- [ ] A/B: looks "cinematic B&W" not "desaturated video"

---

## Related Techniques

- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer for WB
- `davinci-resolve-split-tone-studio-free` — Split tone for toned B&W
- `davinci-resolve-cinematic-look-post-production-philosophy` — Full pipeline

---

## Tags

`#davinciresolve` `#blackandwhite` `#rgb-mixer` `#monochrome` `#luma-composite` `#cinematic-bw` `#marcoherbst` `#colorgrading`