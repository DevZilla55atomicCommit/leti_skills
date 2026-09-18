---
name: davinci-resolve-skin-tones-right_mansourmelouli
category: creative
description: "Skin tone correction workflow using Vectorscope Skin Tone Indicator, Power Windows, and HDR Wheels — the emotional anchor of every grade"
tags:
  - davinci-resolve
  - color-grading
  - skin-tones
  - vectorscope
  - skin-tone-indicator
  - power-windows
  - hdr-wheels
  - color-correction-fundamentals
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJ8srvVo1ZJ/"
creator: "@mansourmelouli"
vault_file: "Color Correction Fundamentals/17-Skin-Tones-Right_mansourmelouli_Vectorscope-HDR-Wheels.md"
---

# How to Get Your Skin Tones Right

## Overview
Step-by-step skin tone correction using Vectorscope Skin Tone Indicator, Power Window isolation, and HDR Wheels for precise gamma correction — skin tones are the emotional anchor of every grade.

## When to Use
- **Every narrative/commercial project** with people
- When skin looks "off" (green, magenta, yellow, red cast)
- Establishing baseline before creative grade
- Troubleshooting skin tone issues
- **Not for**: Faceless content (products, landscapes only)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic Vectorscope, Power Window, HDR Wheels knowledge
- Footage with visible skin (face, hands, arms)

## The Core Principle

> **All human skin falls on the Vectorscope Skin Tone Line (~103°). Only saturation varies by ethnicity.**

- **Hue is constant** — never rotate hue off-line for ethnicity
- **Saturation = radius** — Light skin near center, dark skin near edge
- **Line is your truth** — Monitor calibration varies, scope doesn't

## Node Structure

```
Node 01: CST / Input Transform (Color Managed or manual)
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: Skin Isolation (Power Window + Qualifier)
Node 04: Skin Correction (HDR Wheels — Gamma primary)
Node 05: Background/Non-Skin (Inverted Window)
Node 06: Global Polish / Creative Look
Node 07: Skin Protection (Post-LUT safety net)
```

## Step-by-Step Procedure

### 1. Enable Skin Tone Indicator (Once Per Session)
**Vectorscope** → **Settings (Gear/Three Dots)** → **Show Skin Tone Indicator** → **ON**
- Line appears at ~103° (between Red and Yellow)
- This is your reference for ALL skin work

### 2. Primary Balance First (Node 02)
Before touching skin:
- CST / Color Managed pipeline correct
- Exposure, White Balance, Contrast/Pivot set
- Neutral, balanced image
- **Skin correction on bad balance = fighting yourself**

### 3. Isolate Skin (Node 03)
**Power Window:**
- Shape: **Circle/Oval** on face (primary), add hands/arms if visible
- **Softness: 80-100** (max feather — invisible vignette)
- **Tracker**: Track Forward/Back if subject moves

**Qualifier (Inside Window — Optional but Recommended):**
- HSL Qualifier → Sample skin in window
- Refine: Hue ±15°, Sat 15-80%, Lum 20-80%
- **Invert OFF** (we want skin selected)
- Blur/Softness: High for clean matte

### 4. Read Vectorscope (Windowed)
- With Node 03 selected, **Vectorscope shows ONLY windowed pixels**
- Skin trace position relative to Skin Tone Line:
  - **On line** → Perfect (check saturation next)
  - **Toward Green (150°)** → Sickly → Needs Red/Magenta
  - **Toward Magenta (320°)** → Sunburned → Needs Green/Cyan
  - **Toward Cyan (190°)** → Cold → Needs Red/Yellow
  - **Toward Red (10°)** → Overheated → Needs Cyan/Blue
  - **Near center** → Desaturated → Needs Saturation (outward on line)
  - **Beyond line** → Oversaturated → Needs Desat (inward on line)

### 5. Correct with HDR Wheels (Node 04)
**Why HDR Wheels?** — Separate Lift/Gamma/Gain for shadow/mid/high skin tones.

| Wheel | Skin Region | When to Use |
|-------|-------------|-------------|
| **Shadows (Lift)** | Deep shadow skin (jaw, neck) | Rarely |
| **Midtones (Gamma)** | **Main skin tones (cheeks, forehead)** | **90% of corrections** |
| **Highlights (Gain)** | Specular highlights (forehead, nose) | Subtle warmth/cool |

**Correction Action:**
1. Select **Gamma (Midtones) Wheel**
2. Drag toward Skin Tone Line
   - Green cast → Drag toward **Red/Magenta** (opposite)
   - Magenta cast → Drag toward **Green/Cyan**
   - Cyan cast → Drag toward **Red/Yellow**
   - Red cast → Drag toward **Cyan/Blue**
3. **Watch Vectorscope** — trace moves in real-time
4. **Stop when centered on line**
5. Check **Parade RGB** — channels should align at skin values

### 6. Background Separation (Node 05)
- **Invert Power Window** (same window, invert button)
- Or new serial node with inverted window
- **Background treatment:**
  - Cool it (push toward teal/cyan)
  - Desaturate (-10 to -30%)
  - Reduce contrast
- Creates **pop**: Warm subject, cool background

### 7. Creative Grade (Node 06)
- Film LUT, contrast, saturation, look
- **Re-check skin on Vectorscope** — LUTs often shift skin!

### 8. Skin Protection Safety Net (Node 07)
After creative grade:
- Qualifier: Skin tones
- **Hue vs Hue**: Pull any hue drift back to 103°
- **Hue vs Sat**: Normalize saturation to ethnicity-appropriate
- **Gain**: Fine-tune skin brightness

## Skin Tone by Ethnicity (Reference)

| Skin Type | Vectorscope Position | Saturation Radius |
|-----------|---------------------|-------------------|
| Very Light / Pale | On line, near center | 10-20% |
| Light / Caucasian | On line, inner third | 20-35% |
| Medium / Olive | On line, middle | 35-50% |
| Tan / Latin / Asian | On line, outer middle | 45-60% |
| Dark / Black | On line, far out | 55-75% |
| Very Dark | On line, near edge | 70-85% |

**MEMORIZE**: Hue ~103° constant. Only saturation changes.

## Common Problems & Fixes

| Problem | Vectorscope | HDR Wheel Fix (Gamma) |
|---------|-------------|----------------------|
| Green/Cyan cast | 150-190° | Drag → Red/Magenta |
| Magenta/Pink cast | 300-340° | Drag → Green/Cyan |
| Yellow/Orange cast | 60-90° | Drag → Blue/Cyan |
| Red/Sunburn cast | 0-20° | Drag → Cyan/Blue |
| Desaturated (gray) | Near center | Drag outward on line |
| Oversaturated | Beyond line | Drag inward on line |

## Pro Tips

- **Qualify in Wide Gamut**: If Color Managed, qualify in DWG before output transform — cleaner matte
- **Tracker is Mandatory**: Moving subject = tracked window, or manual keyframes
- **Softness = 100**: Hard window edges = visible "spotlight" = amateur
- **HDR Gamma = Main Tool**: Lift/Gain for skin are secondary
- **Post-LUT Check**: Every creative LUT shifts skin — always verify Node 07
- **Separate Hands/Face**: Different exposure = different correction sometimes

## Advanced: Parallel Skin Branch (Alternative)

```
Layer Mixer (Parallel)
├── Branch 1: Full Creative Grade
└── Branch 2: Skin Normalization
    ├── Power Window: Face (tracked)
    ├── HDR Wheels: Gamma to skin line
    └── Blend: 50-70% opacity
```

## Why This Order Works

```
1. CST/Transform     → Correct color math foundation
2. Primary Balance   → Neutral luminance/chrominance
3. Skin Isolation    → Measure ONLY skin (windowed scope)
4. HDR Gamma Fix     → Precise 3-way correction to line
5. Background        → Visual hierarchy, separation
6. Creative Look     → Artistic intent
7. Skin Protect      → Safety net after look shifts
```

## Related Skills
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Foundations (CM, Contrast, Skin Line, Oval Window)
- `davinci-resolve-white-balance-linear-mode` — Precision WB on scope
- `davinci-resolve-rgb-mixer-white-balance` — Surgical channel WB
- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier as measurement

## References
- Source: @mansourmelouli Instagram Reel (May 22, 2025)
- Hashtags: #davinciresolve #davinciresolve20 #colorgrading #skintones #gradingtips #videoediting #postproduction #filmmaking #videographer #photographer #videography
- Community: 5K+ likes, 70 comments, high engagement
- Free training link shared in comments: blackmagicdesign.com/products/davinciresolve/training