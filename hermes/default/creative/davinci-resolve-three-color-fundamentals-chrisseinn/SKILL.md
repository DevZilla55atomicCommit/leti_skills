---
name: davinci-resolve-three-color-fundamentals-chrisseinn
category: creative
description: "DaVinci Resolve 3 fundamental color grading principles: YRGB Color Managed, Vectorscope skin tones, Power Window subject isolation"
tags:
  - davinci-resolve
  - color-grading
  - fundamentals
  - yrgb-color-managed
  - vectorscope
  - power-windows
  - skin-tones
  - chrisseinn
version: 1.0.0
author: "chrisseinn (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DJ-gXrBsA5G/"
---

# DaVinci Resolve: 3 Fundamental Color Grading Principles

## Overview
Three core techniques that instantly improve color grades: DaVinci YRGB Color Managed setup, Vectorscope skin tone workflow, and Power Window subject isolation.

## Core Principles

### 1. DaVinci YRGB Color Managed + Contrast First
**Project Settings > Color Management > DaVinci YRGB Color Managed**

- Set **Input Color Space** to match camera (e.g., Sony S-Log3/S-Gamut3.Cine)
- Set **Output Color Space** to display target (Rec.709, P3, etc.)
- **Critical**: Dial in contrast **before** any color adjustments
- Use **Contrast/Pivot** or **Custom Curves** for base contrast
- Why: Color Managed pipeline needs proper luminance foundation for accurate hue/sat mapping

### 2. Vectorscope Skin Tones — Qualifier Workflow
**Goal**: Perfect skin tone line alignment

1. **Open Vectorscope**: Enable **Skin Tone Indicator** (line at ~113° / flesh tone axis)
2. **Add Serial Node**: Label "Skin Tones"
3. **Qualifier Tool**: 
   - Sample skin region (forehead/cheek)
   - Refine with **Clean Black/White** sliders
   - Enable **Highlight** mode to verify selection
4. **Hue vs Sat / Hue vs Hue Curves**:
   - Adjust **Hue** to center vectorscope trace on skin tone line
   - Adjust **Sat** for natural saturation (typically 30-50% on vectorscope)
5. **Verify**: Toggle node on/off — skin should look natural, not orange/magenta

### 3. Power Window Subject Isolation
**Goal**: Separate subject from background for dimensionality

1. **Add Serial Node**: Label "Subject Isolation"
2. **Power Window**: **Oval** shape
3. **Position**: Cover subject (face + upper body typically)
4. **Softness**: **100** (maximum feather) for seamless blend
5. **Adjustments Inside Window**:
   - Slight exposure lift (+0.1 to +0.3)
   - Mild contrast boost
   - Skin tone refinement (if needed)
6. **Invert Window** (optional): For background treatment (darken, desaturate, blur)

## Node Tree Structure

```
Node 01: CST Input (Camera > Working Space)
Node 02: Primary Balance (Exposure, WB, Contrast/Pivot)
Node 03: Color Managed Foundation Check
Node 04: Skin Tones (Qualifier + Hue vs Hue/Sat)
Node 05: Subject Isolation (Power Window Oval, Softness 100)
Node 06: Background (Inverted Window — optional)
Node 07: Creative Look / Film Emulation
Node 08: Output CST (Working > Display)
```

## Key Settings Reference

| Setting | Value | Purpose |
|---------|-------|---------|
| Color Management | DaVinci YRGB Color Managed | Scene-referred pipeline |
| Contrast Method | Contrast/Pivot or Custom Curves | Base luminance structure |
| Vectorscope Skin Line | Enabled (113°) | Reference for skin hue |
| Qualifier Clean Black | 10-20 | Remove noise from selection |
| Qualifier Clean White | 80-90 | Tighten selection |
| Power Window Shape | Oval | Natural face/body shape |
| Power Window Softness | 100 | Invisible edge blend |
| Window Exposure Lift | +0.1 to +0.3 | Subject separation |

## Pro Tips

- **Order Matters**: Contrast > Color Management > Skin Tones > Isolation > Look
- **Skin Tone Protection**: Always qualify skin before global saturation adjustments
- **Window Tracking**: Enable tracker for moving subjects (Planar/Frame)
- **Multiple Windows**: Separate windows for face, hands, clothing if needed
- **Background Depth**: Inverted window with slight blur (Radius 5-10) adds cinematic depth

## Common Mistakes to Avoid

1. **Skipping Color Management** > Unpredictable hue shifts
2. **Saturation before Contrast** > Muddy, washed colors
3. **No Skin Qualification** > Global saturation ruins skin
4. **Hard Window Edges** > Visible "halo" around subject
5. **Over-isolation** > Subject looks "cut out" / composited

## Related Skills
- `davinci-resolve-skin-tones-qualifier-noisy` — Clean skin isolation
- `davinci-resolve-power-masking` — Radial > Magic Mask > Inverted BG
- `davinci-resolve-white-balance-helper-window-technique` — WB via Power Window

## Source
Instagram: @chrisseinn — "3 things I learned that will instantly improve your colors"
URL: https://www.instagram.com/reel/DJ-gXrBsA5G/
Date: 2025-07-11