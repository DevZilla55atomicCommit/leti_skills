---
name: davinci-resolve-promist-slog3-dreamy
category: creative
description: "Pro Mist / Black Pro Mist filter look for S-Log3 footage — halation, bloom, dreamy atmosphere in DaVinci Resolve"
tags:
  - davinci-resolve
  - color-grading
  - promist
  - slog3
  - halation
  - bloom
  - dreamy-look
  - diffusion
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DFyvSukM8Py/"
creator: "@caleboshi"
vault_file: "Creative Grading & Looks/44-Pro-Mist-SLog3-Dreamy_caleboshi_Halation-Bloom.md"
---

# Pro Mist Filter Look for S-Log3 — Dreamy Atmosphere

## Overview
Creates the Pro Mist / Black Pro Mist optical filter look in post for S-Log3 footage using Parallel Mixer with Blur + Soft Light and Glow OFX for halation/bloom.

## When to Use
- Dreamy, cinematic atmosphere
- Music videos, narrative, fashion
- Softening digital sharpness
- Mimicking vintage lens character
- When you didn't shoot with physical diffusion filters

## Prerequisites
- DaVinci Resolve (Free or Studio)
- S-Log3/S-Gamut3.Cine footage (or any log footage)
- Basic node structure knowledge

## Node Structure

```
Node 01: CST — S-Log3/S-Gamut3.Cine → Rec.709/Gamma 2.4
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: [PARALLEL MIXER] Pro Mist Effect
  ├─ Node 03a: Blur OFX (Box/Radial) → Soft Light composite
  ├─ Node 03b: Glow OFX (Resolve FX) → Add/Screen composite
  └─ Node 03c: Contrast/Pivot adjustment (shadow lift)
Node 04: Creative Grade / Film Emulation / Grain
```

## Step-by-Step Procedure

### 1. Base Conversion
- CST: **S-Log3/S-Gamut3.Cine → Rec.709/Gamma 2.4**
- Or manual: Cineon Log → Linear → Rec.709

### 2. Build Pro Mist in Parallel Mixer
**Create Layer Mixer → Set to Parallel mode**

**Node 03a — Soft Glow Base:**
- Effect: **Blur OFX** (Box or Radial)
- Radius: **15-30px** (4K: 25-30, HD: 10-15)
- Composite Mode: **Soft Light**
- Opacity: **15-25%**

**Node 03b — Highlight Halation:**
- Effect: **Glow OFX** (Resolve FX Glow)
- Threshold: **0.85-0.95** (only brightest highlights)
- Radius: **50-100px**
- Intensity: **0.1-0.3**
- Composite: **Add** or **Screen**

**Node 03c — Contrast Compensation:**
- Contrast: **-5 to -10**
- Pivot: **0.5**
- Lifts shadows slightly (mimics filter shadow lift)

### 3. Blend Pro Mist Layer
- Parallel Mixer blend: **20-40% opacity**
- Or Layer Mixer with **Soft Light** composite at 30-50%

### 4. Optional: Selective Application
- **Power Window** on subject → Invert → Apply only to background
- **Qualifier** on skin tones → Reduce effect on face
- Track window if subject moves

## Parameter Presets

| Style | Blur Radius | Blur Opacity | Glow Threshold | Glow Radius | Glow Intensity | Blend % |
|-------|-------------|--------------|----------------|-------------|----------------|---------|
| **Subtle (1/8)** | 10-15px | 10% | 0.95 | 30px | 0.05 | 15% |
| **Medium (1/4)** | 20-25px | 20% | 0.90 | 60px | 0.15 | 30% |
| **Strong (1/2)** | 30-40px | 30% | 0.85 | 100px | 0.30 | 50% |

## S-Log3 Specific Considerations

1. **Highlight Latitude**: S-Log3 holds massive highlight detail → raise Glow Threshold (0.9+)
2. **Shadow Noise**: Pro Mist lifts shadows → may reveal noise
   - Fix: Denoise *before* Pro Mist node, or limit blend in shadows
3. **Color Shifts**: S-Gamut3.Cine → Rec.709 can shift highlight hues
   - Check Vectorscope after Glow addition

## Variations

### Black Pro Mist (Stronger Contrast Reduction)
- Add **Lift +0.02 to +0.05** on Pro Mist node
- Contrast: **-15**
- Better for high-contrast scenes

### Warm Pro Mist (Golden Hour)
- Temperature: **+50 to +100** on Pro Mist node
- Tint: **+5 to +10** (Magenta)
- Blend: **15-20%**

### Anamorphic-Style Streaks
- Replace Box Blur with **Directional Blur OFX**
- Angle: Match light source direction
- Composite: **Add** mode for highlight streaks

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Image too soft | Blur radius too high / blend too strong | Reduce radius, lower blend % |
| Highlights blown out | Glow threshold too low | Raise threshold to 0.95+ |
| Skin looks plastic | Effect applied to face | Power Window invert or Qualifier exclude |
| Noise in shadows | Shadow lift reveals sensor noise | Denoise earlier, or limit blend with Luma key |
| Color fringing | Glow on saturated highlights | Lower Glow Intensity, check Vectorscope |

## Related Skills
- `davinci-resolve-diffusion-soft-light` — Blur + Soft Light diffusion (@yancolorist)
- `davinci-resolve-cinematic-haze-effect` — Native haze/glow (@3rdvisionfilm)
- `davinci-resolve-color60-film-grain-highlights` — Film grain in highlights (Color60 Day 11)
- `davinci-resolve-cinematic-haze-20-2` — Resolve 20.2 Cinematic Haze (@creatorsergeant)

## References
- Source: @caleboshi Instagram Reel (Feb 7, 2025)
- Hashtags: #davinciresolve #davinciresolvestudio #davinciresolvetutorial #editing #slog3 #promistfilter #promist
- Community: "Comment MIST for free SLOG3 Ungraded Footage Pack"