---
name: color-grading-theory-fundamentals
description: Core color grading principles applicable to any grading system
category: photography
tags: [color-theory, grading-fundamentals, scopes, lut, workflow]
difficulty: beginner
---

# Color Grading Theory Fundamentals

Universal principles for cinematic color grading across all platforms.

## Color Science Basics

### Color Spaces
| Space | Gamut | Use Case |
|-------|-------|----------|
| **Rec.709** | Standard HD | Broadcast, web delivery |
| **DCI-P3** | Wide gamut | Cinema projection |
| **Rec.2020** | Ultra-wide | HDR, future-proof |
| **ACES** | Scene-referred | VFX, multi-cam pipeline |

### Gamma Curves
- **Linear** (1.0) — Sensor data, compositing
- **Log** (Cineon, Arri LogC, Sony S-Log) — Maximum DR capture
- **Gamma 2.2/2.4** — Display referred (sRGB/Rec.709)
- **HLG / PQ** — HDR display curves

## Scopes Reading

### Waveform (Luma)
- **0-100 IRE** (Rec.709) or **0-1023** (10-bit)
- **Black**: 0-10 IRE (crush check)
- **Skin**: 55-70 IRE (caucasian), 40-55 IRE (darker)
- **White**: 90-100 IRE (clipping check)

### Vectorscope (Chroma)
- **Skin tone line**: ~11 o'clock (FLESH LINE)
- **Saturation**: Distance from center
- **Hue**: Angle around center
- **Legal limits**: 75% color bars box

### Parade (RGB)
- **White balance**: R=G=B at neutral
- **Color casts**: Channel separation in shadows/mids/highlights
- **Clipping**: Any channel hitting 1023 (10-bit)

### Histogram
- **Left pile**: Crushed blacks
- **Right pile**: Blown highlights
- **Gap at ends**: Headroom/footroom available

## Primary Grading Workflow

### 1. Balance (Technical)
```
Lift/Gamma/Gain → RGB Parade match
```
- Set black point (lift)
- Set white point (gain)
- Set middle gray (gamma ~40-50 IRE)

### 2. Contrast (Creative)
```
Contrast/Pivot OR Custom Curves
```
- **S-curve**: Lift shadows, lower highlights
- **Pivot**: Center of contrast expansion
- **Avoid**: Crushed blacks / blown highlights

### 3. Saturation
```
Saturation knob OR HSV curves
```
- **Global**: Subtle (±10-15%)
- **Selective**: Hue vs Sat curves for control

### 4. Color Temperature/Tint
```
Temp: Blue←→Orange (Kelvin)
Tint: Green←→Magenta
```
- **Skin tone reference**: Vectorscope flesh line
- **Gray reference**: RGB parade match

## Secondary / Selective Grading

### Qualifier (HSL Keys)
- **Hue**: Select color range
- **Sat**: Limit to saturated/desaturated
- **Lum**: Limit to shadows/mids/highlights
- **Refine**: Softness, shrink/grow, spill suppression

### Power Windows
- **Circle/Gradient**: Vignettes, spotlights
- **Custom/Poly**: Complex shapes
- **Track**: Planar tracker for moving objects

### Curves (Hue vs Hue, Hue vs Sat, Lum vs Sat)
- **Hue vs Hue**: Shift specific hues (skin→orange, foliage→teal)
- **Hue vs Sat**: Desaturate problem colors (neon signs)
- **Lum vs Sat**: "Film look" — desaturate shadows, saturate mids

## Creative Looks

### Teal & Orange (Blockbuster)
```
Shadows: Push teal (Lift → cyan/blue)
Midtones: Warm skin (Gamma → orange/red)
Highlights: Clean or slightly warm
```
**Guard**: Skin tone line on vectorscope

### Bleach Bypass
```
High contrast + Low saturation
Curves: Strong S-curve
Saturation: -20 to -40%
Optional: Add grain
```

### Cross Process
```
Split tone: Shadows cool, Highlights warm
Curves: Crossed RGB channels
High contrast, color shift
```

### Film Emulation
1. **Log → Rec.709** (CST / LUT)
2. **Film Print LUT** (Kodak 2383, Fuji 3510)
3. **Grain** (Fusion / OpenFX)
4. **Halation** (Glow OFX, highlight isolation)
5. **Gate weave** (Transform micro-jitter)

## LUT Workflow

### Technical LUTs
- **Input**: Log → Scene-referred (CST)
- **Output**: Scene-referred → Display (Rec.709, P3)
- **Creative**: Applied *after* primary, *before* secondary

### LUT Best Practices
- **Exposure first**: LUTs assume correct middle gray
- **White balance first**: LUTs baked for neutral
- **Intensity**: Blend 50-75% for subtlety
- **Stack**: Technical → Creative → Trim

## HDR Grading (PQ / HLG)

### Nits Reference
| Level | SDR (nits) | HDR (nits) |
|-------|-----------|------------|
| Black | 0 | 0 |
| Mid-gray | 100 | 200 |
| White | 100 | 203 (PQ) / 1000 (ref) |
| Specular | N/A | 1000-4000 |
| Peak | 100 | 4000-10000 |

### HDR Grading Rules
- **Don't grade by eye on SDR monitor**
- **Use Dolby Vision / HDR10 metadata**
- **Specular highlights**: 1000-4000 nits for sparkle
- **Average Picture Level (APL)**: Manage power/brightness

## Delivery Specs

| Platform | Color Space | Gamma | Bit Depth |
|----------|-------------|-------|-----------|
| YouTube/Instagram | Rec.709 | 2.4 | 8-bit |
| Netflix | DCI-P3 / Rec.2020 | PQ | 10-bit |
| Broadcast | Rec.709 | 2.4 | 10-bit |
| Cinema | DCI-P3 | 2.6 | 12-bit |

## Tags
`color-theory` `grading-fundamentals` `scopes` `lut` `workflow` `hdr` `aces` `film-emulation`