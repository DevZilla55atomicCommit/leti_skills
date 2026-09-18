---
name: davinci-resolve-perfect-color-mightymad
category: creative
description: "DaVinci Resolve: Perfect Color Every Time — 9-node pipeline with LUTs, CST, HSL curves, Color Shift, Shadow/Highlight toning"
tags:
  - davinci-resolve
  - color-grading
  - lut-workflow
  - cst
  - hsl-curves
  - color-shift
  - shadow-highlight
  - mightymad
version: 1.0.0
author: "mightymad (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DJuz-eDB4iS/"
---

# DaVinci Resolve: Perfect Color Every Time — 9-Node Pipeline

## Overview
Complete color grading node tree (9 nodes) for consistent, repeatable results. Uses **CST at start and end**, **LUT integration**, **HSL curves**, **Color Shift**, and **Shadow/Highlight toning** for a professional pipeline.

## Node Structure (9 Nodes)

```
Node 01: CST (Camera → Working Space, e.g., DWG / ACEScct)
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: Creative LUT (Look LUT — applied in working space)
Node 04: HSL Curves (Hue vs Hue, Hue vs Sat, Lum vs Sat)
Node 05: Color Shift (Resolve FX Color → Color Shift)
Node 06: Shadow/Highlight Toning (Log Wheels or Custom Curves)
Node 07: Secondary Adjustments (Skin, Sky, etc.)
Node 08: Global Polish (Grain, Glow, Vignette)
Node 09: CST (Working → Display, e.g., Rec.709 / P3)
```

## Step-by-Step Workflow

### 1. Input CST (Node 01)
- **Input Color Space**: Camera native (S-Log3/S-Gamut3, V-Log/V-Gamut, BRAW, etc.)
- **Output Color Space**: Working space (DaVinci Wide Gamut / ACEScct)
- **Why first**: All subsequent ops in known, uniform space

### 2. Primary Balance (Node 02)
- Exposure (middle gray ~18-40 IRE)
- White Balance (Temp/Tint or RGB Gain)
- Contrast/Pivot or Custom Curves S-shape
- **Goal**: Neutral, balanced base

### 3. Creative LUT (Node 03)
- **LUT Type**: Creative look LUT (Kodak 2383, Fujifilm, custom)
- **Placement**: In working space (DWG/ACEScct) — NOT in log
- **Intensity**: Key Output Gain 0.5–1.0 for blend control
- **Why here**: LUT bakes look into linear/gamma space cleanly

### 4. HSL Curves (Node 04)
- **Hue vs Hue**: Skin tone protection, sky correction, foliage shift
- **Hue vs Sat**: Desaturate distracting hues, pop key colors
- **Lum vs Sat**: Reduce saturation in shadows (film-like), protect highlights
- **Sat vs Sat**: Compress over-saturated areas

### 5. Color Shift (Node 05)
- **Effect**: Resolve FX Color → Color Shift
- **Use**: Global hue rotation for mood (cool→warm, green→teal)
- **Subtle**: 5–15° shifts; keyframe for scene transitions

### 6. Shadow/Highlight Toning (Node 06)
- **Option A**: Log Wheels (Shadows/Midtones/Highlights color)
- **Option B**: Custom Curves (R/G/B independent)
- **Teal shadows / Orange highlights** classic split tone
- **Preserve skin**: Qualifier mask if needed

### 7. Secondary Adjustments (Node 07)
- **Skin**: Qualifier + Power Window → Hue vs Sat, Lum vs Sat
- **Sky**: Gradient + Qualifier → Blue enhancement
- **Foliage**: Hue vs Hue (green→teal/orange)

### 8. Global Polish (Node 08)
- **Film Grain**: Resolve FX Texture → Film Grain
- **Glow/Halation**: Glow OFX (Soft Light, threshold 0.8+)
- **Vignette**: Power Window (circle, inverted, soft)

### 9. Output CST (Node 09)
- **Input**: Working space (DWG / ACEScct)
- **Output**: Delivery space (Rec.709 Gamma 2.4, PQ, HLG)
- **Tone Mapping**: Auto / Manual (for HDR→SDR)

## Pro Tips from Comments

> **"Or a node tree that we can download and utilize"** — @marshallchikorowondo
> → Save as **PowerGrade** (.dpx grade) for reuse

> **"Do you have LUTs you have already created"** — @marshallchikorowondo
> → Build LUT library: Kodak 2383, Fuji 3510, custom creative LUTs

> **"Show each step in more depth: HSL curves, Color Shift, Shadow Highlight toning"** — @alex__brando
> → Each node deserves its own deep-dive

> **"I would use CST in the beginning and CST in the end for larger color space"** — @andyhendrata
> → **Correct** — CST sandwich is standard Color Managed workflow

> **"Why do you use CST at the back? So the result is different if you use CST at the forward?"** — @ferdipodiman
> → **Forward (Node 01)**: Camera→Working (normalizes)
> → **Backward (Node 09)**: Working→Display (delivers)
> → Different direction = different transform

> **"YouTube channel sir..?"** — @bishal.sendha
> → Educational content demand

> **"I mean 9 nodes just for colour?"** — @jay_not_son
> → **Pro pipeline**: Each node = single responsibility = adjustable, debuggable, reusable

## Common Questions

| Question | Answer |
|----------|--------|
| Why 9 nodes? | Separation of concerns; each adjustable independently |
| LUT before or after HSL? | After primary, before HSL — LUT sets look, HSL refines |
| CST at start AND end? | Yes — Camera→Working (in), Working→Display (out) |
| Can I skip LUT? | Yes — Node 03 becomes "Creative Grade" (curves/wheels) |
| Shadow/Highlight on Log or Primary? | Log Wheels (scene-referred) for toning; Primary for contrast |

## Related Skills
- `davinci-resolve-simple-4-step-workflow` — CST, WB/Exposure, Contrast, Stop
- `davinci-resolve-cst-gamut-mapping-color-spill` — CST gamut mapping
- `davinci-resolve-color-shift` — Color Shift OFX technique
- `davinci-resolve-kodak-2383-film-emulation` — LUT application
- `davinci-resolve-manual-color-profile-conversion` — CST bypass, Log→Rec.709

## Source
Instagram: @mightymad — "Perfect color every time in DaVinci Resolve"
URL: https://www.instagram.com/reel/DJuz-eDB4iS/
Date: 2025-07-11