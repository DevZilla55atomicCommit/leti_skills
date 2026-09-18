---
name: davinci-resolve-saturation-color-density_hudson-twarren
category: creative
description: "Color Density via Hue vs Sat / Lum vs Sat / Sat vs Sat curves — cinematic richness without clipping or skin tone damage"
tags:
  - davinci-resolve
  - color-grading
  - saturation
  - color-density
  - hue-vs-sat
  - lum-vs-sat
  - sat-vs-sat
  - curves
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKIGX5GtJjk/"
creator: "@hudson_twarren"
vault_file: "Creative Grading & Looks/48-Saturation-Color-Density_hudson-twarren_Hue-vs-Sat-Curves.md"
---

# How to Add Saturation and Color Density — Curve-Based Approach

## Overview
Technique for adding **color density** (perceived richness) rather than blind global saturation — using three curve tools (Hue vs Sat, Lum vs Sat, Sat vs Sat) for precise, perceptual control that protects skin tones and preserves highlight detail.

## When to Use
- Any grade wanting "rich" look without clown colors
- Narrative, commercial, music video, fashion
- When global saturation slider breaks skin/highlights
- Film emulation base (before LUT)
- **Avoid**: Quick social content (use global sat +10)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic Custom Curves panel knowledge
- Vectorscope / Parade monitoring

## Node Structure

```
Node 01: Base Grade (CST, Balance, Contrast) — NO SAT YET
Node 02: Hue vs Sat Curve     — Hue-selective density
Node 03: Lum vs Sat Curve     — Luminance-selective density
Node 04: Sat vs Sat Curve     — Saturation dynamic range
Node 05: Global Sat (Subtle)  — Final unified push (+5 to +15)
Node 06: Creative Look / LUT / Grain
```

## Step-by-Step Procedure

### 1. Base Grade First (Node 01) — Critical
Complete primary grade BEFORE density curves:
- CST / Color Managed pipeline
- Exposure, White Balance, Contrast/Pivot
- Clean, neutral image
- **Zero creative saturation at this stage**

### 2. Hue vs Sat Curve (Node 02) — "Which Hues Get Dense"

**Purpose**: Boost nature tones, protect skin/magenta

**Curve Anchors (Hue → Output Saturation Multiplier):**

| Hue Region | Degrees | Target Output | Why |
|------------|---------|---------------|-----|
| **Skin** | 30-40° | **0.5-0.7** (lock) | Never oversaturate people |
| **Warm/Gold** | 40-60° | 0.9-1.1 | Golden hour feel |
| **Foliage/Green** | 100-140° | **1.2-1.5** | Rich vegetation |
| **Cyan/Teal** | 160-200° | 1.1-1.3 | Cinematic shadows |
| **Blue/Sky** | 200-240° | **1.1-1.3** | Deep skies/water |
| **Magenta** | 300-340° | 0.8-1.0 | Skin-adjacent, moderate |

**Technique**: Add control points at each region, create smooth curve. **Lock skin point** — don't let it move.

### 3. Lum vs Sat Curve (Node 03) — "Where in Brightness"

**Purpose**: Dense midtones, clean highlights, controlled shadows

**Curve Anchors (Luminance → Output Saturation Multiplier):**

| Luma Region | Range | Target Output | Why |
|-------------|-------|---------------|-----|
| **Blacks** | 0.0-0.1 | 0.5-0.7 | Dense but not noisy |
| **Shadows** | 0.1-0.3 | 0.7-0.9 | Rich dark tones |
| **Low-Mids** | 0.3-0.5 | **1.1-1.3** | **Peak density here** |
| **Mid-Highs** | 0.5-0.7 | 1.0-1.1 | Natural |
| **Highlights** | 0.7-0.9 | 0.5-0.7 | **Film desaturates highlights** |
| **Specular** | 0.9-1.0 | 0.3-0.5 | Clean, no color fringing |

**Key Insight**: Midtones (0.3-0.6) carry perceived "colorfulness" — boost here. Highlights desaturate = filmic.

### 4. Sat vs Sat Curve (Node 04) — "Saturation Dynamic Range"

**Purpose**: Expand muted tones, compress saturated (filmic rolloff)

**Curve Anchors (Input Sat → Output Sat):**

| Input Sat | Output Sat | Purpose |
|-----------|------------|---------|
| 0.0 | 0.05 | Lift near-zero (wake up dead tones) |
| 0.2 | 0.4 | Expand low saturation |
| 0.4 | 0.6 | Natural mid-sat |
| 0.6 | 0.75 | Gentle transition |
| 0.8 | 0.85 | Compress high |
| 1.0 | 0.85-0.9 | **Rolloff prevents clipping** |

### 5. Global Saturation (Node 05) — Final Touch Only
- **Saturation**: +5 to +15 MAX
- **Purpose**: Unified coherence, curves did heavy lifting
- **Verify**: Vectorscope — no hue hitting boundary circle

## Parameter Presets

| Look | Hue vs Sat | Lum vs Sat | Sat vs Sat | Global |
|------|------------|------------|------------|--------|
| **Natural/Doc** | Foliage/sky +10% | Mild midtone +10% | Gentle compress | +5 |
| **Cinematic Rich** | Green/blue +30%, skin locked | Midtones +30%, HL -30% | Expand low, compress high | +10 |
| **Vibrant/Pop** | All non-skin +20% | Midtones +40% | Moderate compress | +15 |
| **Moody/Desat** | Reduce most, keep keys | Shadows dense, HL low | Heavy compress | -5 to 0 |
| **Film Emu Base** | Match film hue response | Film characteristic curve | Film rolloff | Via LUT |

## Skin Protection Strategies

### Primary: Hue vs Sat Anchors (Node 02)
- Place control points at skin hue (30-40°)
- Set output to 0.5-0.7
- Curve **must pass through** these points
- Automatic for all skin in frame

### Backup: Qualifier Parallel Branch
```
Layer Mixer (Parallel)
├── Main: All 3 density curves
└── Skin Protect:
    ├── Qualifier: Skin tones (HSL)
    ├── Hue vs Sat: Flat at 0.6
    └── Blend: 50-100% opacity
```

### Cleanup: Serial After Curves
- Node after Node 04
- Qualifier: Skin
- Hue vs Sat: Pull back overshoot
- Sat vs Sat: Compress skin range

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Global Sat +50 | Clown colors, clipped scopes | Curves only, global +10 max |
| No skin anchor on Hue vs Sat | Orange faces | Lock skin hue at 0.6 output |
| Highlights saturated | Digital/video look | Lum vs Sat: HL 0.4-0.6 |
| Shadows saturated | Noise, mud | Lum vs Sat: Shadows 0.6-0.8 |
| No Sat vs Sat curve | No color DR | Add curve, expand low/compress high |
| Curves before base grade | Unpredictable | Base grade FIRST (Node 01) |

## Color Science Why It Works

1. **Hue vs Sat** = Perceptual uniformity (Munsell, CIECAM) — vision more sensitive to green/blue saturation
2. **Lum vs Sat** = Hunt Effect + Bezold-Brücke + film highlight desaturation
3. **Sat vs Sat** = Gamut mapping / filmic saturation rolloff (shoulder)
4. **Combined** = Perceptually natural "density" not "saturation"

## Related Skills
- `davinci-resolve-increase-color-density-creatorsergeant` — Hue vs Lum density
- `davinci-resolve-density-saturation-hue-vs-luminance` — Density via Hue vs Lum
- `davinci-resolve-color60-cinematic-saturation-hsv` — HSV Gain/Lift density
- `davinci-resolve-three-color-fundamentals_chrisseinn` — Foundation before density

## References
- Source: @hudson_twarren Instagram Reel (May 26, 2025)
- Hashtags: #videography #cinematography #indiefilm #tipsandtricks #colourgrading
- Community: "Made HUGE difference to how I grade" — creator testimonial