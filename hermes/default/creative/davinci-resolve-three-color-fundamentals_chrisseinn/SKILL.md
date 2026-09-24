---
name: davinci-resolve-three-color-fundamentals_chrisseinn
category: creative
description: "3 fundamental color grading principles: DaVinci YRGB Color Managed setup, Vectorscope skin tone line, Oval Power Window at 100 softness for subject isolation"
tags:
  - davinci-resolve
  - color-grading
  - color-management
  - yrgb-color-managed
  - vectorscope
  - skin-tones
  - power-windows
  - workflow-fundamentals
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJ-gXrBsA5G/"
creator: "@chrisseinn"
vault_file: "Color Correction Fundamentals/16-Three-Color-Fundamentals_chrisseinn_YRGB-SkinTone-PowerWindow.md"
---

# 3 Things to Instantly Improve Your Colors

## Overview
Three fundamental color grading principles from @chrisseinn: proper DaVinci YRGB Color Managed setup, vectorscope-guided skin tones, and oval power window subject isolation at 100 softness.

## When to Use
- **Every grade** — these are foundations, not creative choices
- Starting any new project/resolve session
- Troubleshooting "muddy" or "wrong" colors
- Establishing consistent pipeline across projects

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic color page navigation
- Footage with known camera log/color space

## The 3 Fundamentals (In Order)

### 1. DaVinci YRGB Color Managed — Pipeline First
**Project Settings → Color Management:**
```
Mode:              DaVinci YRGB Color Managed
Input Color Space: [Camera Specific - S-Log3/S-Gamut3.Cine, etc.]
Timeline Color:    DaVinci Wide Gamut
Output Color:      Rec.709 Gamma 2.4 (or target)
Tone Mapping:      DaVinci (or ACES)
```
**Why First**: All subsequent color math depends on correct color space transforms. Wrong CM = wrong colors permanently.

### 2. Contrast Before Color (Node 02)
**Before any color wheels:**
- Contrast: +15 to +30
- Pivot: 0.4-0.5 (protect midtones)
- Verify Waveform: Legal range, clean blacks/whites
**Principle**: Color rides on luminance. Wrong contrast = wrong color perception.

### 3. Vectorscope Skin Tone Line (Node 04)
**The Skin Tone Line = ~103° (between Red-Yellow)**
```
1. Qualifier → Sample skin tones
2. Refine: Hue ±10°, Sat 20-80%, Lum 20-80%
3. Hue vs Hue Curve → Pull skin hue TO the line
4. Hue vs Sat Curve → Set saturation (scope radius 40-60%)
5. Qualifier Blur/Softness: High for clean matte
```
**Don't guess** — monitor calibration varies, scope is absolute.

### 4. Oval Power Window — 100 Softness (Node 05/06)
```
Node 05 (Inside):  Oval on subject → Softness 100 → Subject pop (Lift/Gamma/Gain)
Node 06 (Inverted): Same window inverted → Background recede (darker, cooler, less contrast)
```
**Why 100 Softness**: Maximum feather = invisible vignette. Hard edges = amateur "spotlight."

## Complete Node Structure

```
Node 01: CST / Input Transform (if not Color Managed)
Node 02: Contrast & Pivot (FOUNDATION)
Node 03: White Balance / Global Balance
Node 04: Skin Tone Correction (Qualifier + Hue vs Hue/Sat + Vectorscope)
Node 05: Power Window Oval (Softness 100) → Subject Enhancement
Node 06: Power Window Inverted → Background Separation
Node 07: Global Polish (Sat, Contrast, Tint)
Node 08: Creative LUT / Film Emulation
Node 09: Grain / Halation / Texture
```

## Parameter Reference

| Fundamental | Tool | Key Parameter | Target |
|-------------|------|---------------|--------|
| **Color Mgmt** | Project Settings | DaVinci YRGB CM | Correct pipeline |
| **Contrast** | Node 02 | Contrast +20, Pivot 0.45 | Clean waveform |
| **Skin Hue** | Vectorscope + Qualifier | Hue vs Hue curve | On skin line (~103°) |
| **Skin Sat** | Hue vs Sat Curve | Radius on scope | 40-60% |
| **Subject Pop** | Power Window Oval | Softness = 100 | Invisible vignette |
| **BG Separation** | Inverted Window | Lift -0.02, Cool hue | Recedes naturally |

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Grade before Color Mgmt | Colors never look right, clipped | Setup CM first, every project |
| Contrast after color wheels | Hue shifts when contrast changes | Contrast FIRST (Node 02) |
| Eyeballing skin tones | Looks different on other screens | Vectorscope skin line = truth |
| Power Window softness < 100 | Visible ellipse on subject | Softness slider ALL THE WAY RIGHT |
| No background separation | Flat, 2D image | Invert window, push BG back |
| Saturation before hue fix | Hue shifts with saturation | Hue vs Hue first, then Hue vs Sat |

## Pro Workflow Order (Never Skip)

```
1. PROJECT SETUP: Color Management (once per project)
2. NODE 02: Contrast/Pivot (luminance foundation)
3. NODE 03: White Balance (neutral start)
4. NODE 04: Skin Tones (human anchor — Vectorscope)
5. NODE 05/06: Subject Isolation (visual hierarchy)
6. NODE 07+: Creative decisions (on solid base)
```

## Variations

### Minimal (Run & Gun)
- Skip Node 01 (use Color Managed auto)
- Node 02: Contrast only
- Node 04: Quick skin qualifier
- Node 05: Oval window, done

### Precision (Narrative/Commercial)
- Full CST chain in Node 01
- Custom curves for contrast
- Multiple qualifiers (face, hands, different skin tones)
- Tracked power windows per shot
- Shot matching via gallery stills

## Related Skills
- `davinci-resolve-white-balance-linear-mode` — Precision WB on Vectorscope
- `davinci-resolve-rgb-mixer-white-balance` — Surgical channel WB
- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier as measurement
- `davinci-resolve-color60-apply-inverse-ootf` — Color managed pipeline deep dive

## References
- Source: @chrisseinn Instagram Reel (May 22, 2025)
- Hashtags: #colorgrade #davinci #davinciresolve #cinematic #colorgrading
- Official Training: blackmagicdesign.com/products/davinciresolve/training
- Community Q: Cinematography courses, FCP compatibility