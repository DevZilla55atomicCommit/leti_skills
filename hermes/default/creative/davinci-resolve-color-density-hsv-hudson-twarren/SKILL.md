---
name: davinci-resolve-color-density-hsv-hudson-twarren
category: creative
description: DaVinci Resolve color density/saturation technique using HSV curves for richer colors
tags:
  - davinci-resolve
  - color-density
  - hsv-curves
  - saturation
  - hudson-twarren
  - color-grading
version: 1.0.0
author: hudson_twarren (extracted by Hermes Agent)
source_url: https://www.instagram.com/reel/DKIGX5GtJjk/
---

# DaVinci Resolve: Color Density & Saturation via HSV Curves

## Overview
Technique for adding saturation and making shots more "color dense" using HSV (Hue-Saturation-Value) curves in DaVinci Resolve. This approach provides more control over saturation distribution across luminance ranges compared to global saturation.

## Core Concept

### Why HSV Curves for Density?
- **Luminance-aware saturation**: Control saturation independently in shadows, midtones, highlights
- **Hue-selective**: Target specific hue ranges for density
- **Natural rolloff**: Avoids the "crushed" look of global saturation boosts
- **Film-like response**: Mimics how film stock handles saturation at different exposures

## Node Structure

```
Node 01: Input (Log/Raw)
Node 02: CST (Log → Working Space, e.g., DaVinci Wide Gamut Intermediate)
Node 03: Primary Balance (Exposure, WB, Contrast)
Node 04: HSV Curves — Color Density (Parallel or Serial)
Node 05: Creative Look / Film Emulation
Node 06: Output CST (Working → Display)
```

## HSV Curve Technique

### Accessing HSV Curves
1. Open **Curves** panel
2. Click dropdown (default: "Custom") → Select **HSV**

### Key Curves for Color Density

| Curve | Purpose | Typical Shape |
|-------|---------|---------------|
| **Hue vs Sat** | Boost saturation for specific hues | Gentle S-curve on target hues |
| **Hue vs Lum** | Darken saturated hues for density | Pull down slightly on skin tones, foliage |
| **Sat vs Sat** | Compress/expand saturation range | S-curve: lift mids, roll off highlights |
| **Lum vs Sat** | **Primary density control** | **Inverse S: lower sat in shadows, peak in mids, roll off highlights** |

### Lum vs Sat Curve — The "Density" Secret
```
Shadows (0-20%):   Lower saturation → cleaner blacks, less noise
Midtones (20-70%): Peak saturation → maximum color density
Highlights (70%+): Roll off saturation → protect highlights, filmic rolloff
```

**Curve Points (approximate):**
- 0% → 0% (shadows desaturated)
- 15% → 10% (gentle lift)
- 40% → 60% (midtone density peak)
- 65% → 55% (start rolloff)
- 100% → 30% (highlight protection)

## Step-by-Step Workflow

1. **Base Grade First**: Complete primary correction (exposure, WB, contrast) before HSV curves
2. **Add Serial Node**: Label "HSV Density"
3. **Open Curves → HSV**: Select **Lum vs Sat**
4. **Shape Curve**: Create inverse-S as described above
5. **Refine with Hue vs Sat**: Target specific hues (skin, sky, foliage)
6. **Check Scopes**: Vectorscope for saturation, Parade for luminance integrity
7. **Global Blend**: Use node **Gain** (Key Output) to dial intensity (50-80% typical)

## Pro Tips

- **Combine with Qualifier**: Isolate skin tones → separate Hue vs Sat curve for protection
- **Parallel Node Alternative**: Put HSV curves in parallel mixer for blend control
- **Layer Mixer Method**: Base grade on Layer A, HSV density on Layer B, blend "Overlay" or "Soft Light"
- **CST Context**: Always work in wide gamut (DWG/ACEScct) for maximum headroom before display transform
- **Noise Awareness**: Lowering shadow saturation hides chroma noise — useful for high-ISO footage

## Comparison: Global Sat vs HSV Density

| Aspect | Global Saturation | HSV Lum vs Sat |
|--------|------------------|----------------|
| Shadows | Noisy, colored blacks | Clean, controlled |
| Skin tones | Oversaturated easily | Protected via curve shape |
| Highlights | Clipping risk | Natural rolloff |
| Creative control | Single slider | Per-luminance zone |
| Filmic feel | Digital "crank" | Organic density |

## Related Skills
- `davinci-resolve-saturation-color-density_hudson-twarren` — Hue vs Sat / Lum vs Sat curves
- `davinci-resolve-increase-color-density-creatorsergeant` — Density via multiple approaches
- `davinci-resolve-color-warper-saturation-balance` — Color Warper alternative

## Source
Instagram: @hudson_twarren — "How to add saturation and make your shots more colour dense"
URL: https://www.instagram.com/reel/DKIGX5GtJjk/
Date: 2025-07-11