---
name: davinci-resolve-glow-halation-cinematic
category: creative
description: "Cinematic Glow/Halation in DaVinci Resolve — proper highlight bloom with warm color and optional red halation fringe (film emulation)"
tags:
  - davinci-resolve
  - color-grading
  - glow
  - halation
  - bloom
  - cinematic
  - highlights
  - film-emulation
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DH69ylBy1SL/"
creator: "@caleboshi"
vault_file: "Creative Grading & Looks/47-Glow-Halation-Cinematic_caleboshi_Add-Glow-Right-Way.md"
---

# Add GLOW the Right Way — Cinematic Halation/Bloom

## Overview
Proper technique for adding cinematic glow/halation in DaVinci Resolve — isolate highlights, apply colored blur with Add/Screen blend, optional red halation fringe for film emulation.

## When to Use
- Adding filmic quality to digital footage
- Music videos, narrative, fashion, commercial
- Enhancing practical lights (neon, lamps, sun)
- Creating dreamy/nostalgic atmosphere
- **Avoid**: Corporate, documentary, news (unless stylized)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic Qualifier/Power Window knowledge
- Understanding of blend modes (Add, Screen)

## Node Structure

```
Node 01: Base Grade (CST, Balance, Contrast)
Node 02: Highlight Isolation (Qualifier / Power Window / Luma Key)
Node 03: Glow Build (Blur OFX → Add/Screen → Color Wheels for warmth)
Node 04: Halation Fringe [Optional] (Smaller blur → Strong Red → Add)
Node 05: Global Polish (LUT, Grain, Final Contrast)
```

## Step-by-Step Procedure

### 1. Base Grade First (Node 01)
Complete primary grade before glow:
- CST / Input Transform
- Exposure, White Balance, Contrast
- Clean, balanced image

### 2. Isolate Highlights (Node 02) — CRITICAL
**Option A: Luma Key (Fastest)**
- Qualifier → **Luma** mode
- Low: 0.85, High: 1.0
- Softness: 0.15-0.25

**Option B: HSL Qualifier (More Control)**
- Qualifier → **HSL** mode
- Sample brightest highlights
- Expand range to capture all specular

**Option C: Power Window (Precise per Light)**
- Circular/Gradient window on each light source
- Track if camera/light moves
- Best for practicals, neon, sun

**Refine Matte:**
- Softness: 50-80 (feathered edge)
- Clean Black/White: Tighten matte
- Blur matte slightly for natural falloff

### 3. Build Glow (Node 03)
**Add Blur OFX:**
- Effect: **Blur** (Box or Radial)
- Radius: **30-100px** (4K: 50-80, HD: 25-40)
- Composite Mode: **Add** (brighter) or **Screen** (softer)

**Color the Glow (Color Wheels on same node):**
- **Gain**: Warm Orange/Amber (Hue 20-40°, Saturation 50-100%)
- **Gamma**: Slight warmth
- **Lift**: Neutral (0) — don't glow shadows

**Opacity/Blend:**
- Node output gain/opacity: **15-40%**
- Or Layer Mixer blend if using parallel

### 4. Halation Fringe — Film Emulation (Node 04, Optional)
- Duplicate Node 03 structure
- **Blur Radius**: 10-20px (tighter)
- **Composite**: **Add**
- **Gain**: **Deep Red** (Hue 10-20°, Saturation 100%)
- **Opacity**: 5-15%
- Creates red/orange fringe at highlight edges (Kodak film halation)

### 5. Global Polish (Node 05, Serial)
- Film LUT / Emulation
- Film Grain (breaks up glow naturally)
- Final contrast/saturation

## Parameter Presets

| Style | Blur Radius | Blend Mode | Glow Color (Gain) | Opacity | Halation Fringe |
|-------|-------------|------------|-------------------|---------|-----------------|
| **Subtle Lens Glow** | 20-30px | Screen | Warm 20°, Sat 30% | 10-15% | None |
| **Cinematic Bloom** | 50-80px | Add | Amber 30°, Sat 70% | 25-35% | Light (5%, Red 15px) |
| **Dreamy/Nostalgic** | 80-120px | Add | Gold 40°, Sat 80% | 35-50% | Medium (10%, Red 15px) |
| **Film Halation** | 60px + 15px | Add x2 | Amber 30° + Red 15° | 30% + 8% | Strong (15%, Red 10px) |
| **Anamorphic Streak** | Dir. Blur 100px | Add | Warm 25°, Sat 60% | 20% | Red streak |

## Advanced Techniques

### Per-Light Glow (Most Realistic)
1. Power Window track each practical light
2. Individual Node 03 per light (size matches source)
3. Different glow colors per light type (neon=color, tungsten=warm)

### Chromatic Aberration Glow
- Separate Blur OFX per RGB channel
- Red Blur > Green Blur > Blue Blur
- Mimics lens dispersion

### HDR Glow (Studio Only)
- HDR Wheels → **High** range (>100 nits)
- Glow only affects specular highlights
- SDR fallback: Luma Key > 0.92

### Glare/Starburst (Anamorphic)
- Resolve FX → **Glare** OFX
- Streaks: 4-8, Angle: 0°/90°
- Threshold: High (only brightest)
- Blend: Add

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Whole image glowy | No highlight isolation | Luma Key/Qualifier > 0.85 |
| Glow looks digital/fake | White/neutral glow color | Warm Gain to 20-40° (amber) |
| Blown highlights | Glow adds to clipped values | Check waveform, lower opacity |
| Glow in shadows | Matte not clean | Raise Luma Low, increase Softness |
| No film character | Missing halation fringe | Add Node 04 (Red fringe) |
| Inconsistent across shots | Fixed values | Adjust per shot, use stills |

## Pro Tips

- **Glow BEFORE film LUT**: LUT responds to glow naturally (recommended)
- **Glow AFTER film LUT**: Stylized, LUT doesn't affect glow color
- **Combine with grain**: Film grain breaks up glow → more organic
- **Track windows**: Moving lights need tracked power windows
- **Offer free footage**: @caleboshi provides S-Log3 practice clips ("Comment Log")

## Related Skills
- `davinci-resolve-promist-slog3-dreamy` — Pro Mist diffusion + glow
- `davinci-resolve-cinematic-haze-effect` — Native haze/glow
- `davinci-resolve-diffusion-soft-light` — Blur + Soft Light diffusion
- `davinci-resolve-color60-film-grain-highlights` — Film grain in highlights

## References
- Source: @caleboshi Instagram Reel (Apr 1, 2025)
- Hashtags: #davinciresolve #colorgrading #cinematic #glow #halation
- Community: "Comment Log for free SLOG3 Ungraded Footage Pack"