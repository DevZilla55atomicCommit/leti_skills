---
name: davinci-resolve-texture-pop
category: creative
description: "Texture Pop technique in DaVinci Resolve — native micro-contrast enhancement for detail and texture using Custom Curves + Blur Overlay"
tags:
  - davinci-resolve
  - color-grading
  - texture-pop
  - detail-enhancement
  - micro-contrast
  - native-tools
  - sharpening-alternative
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKMzNsQRTXY/"
creator: "@davinciresolved"
vault_file: "Creative Grading & Looks/45-Texture-Pop_davinciresolved_Native-Tools.md"
---

# Texture Pop in DaVinci Resolve

## Overview
Native micro-contrast enhancement technique using Custom Curves + Blur Overlay to boost texture detail without artificial sharpening halos. Works in Free and Studio versions.

## When to Use
- Landscape/detail shots (rocks, foliage, architecture)
- Product/commercial (fabric, materials, surfaces)
- Documentary footage needing "crunch"
- Adding perceived sharpness without edge halos
- **Avoid**: Clean beauty/skin, already noisy footage

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic node structure knowledge
- Footage with sufficient resolution for detail

## Node Structure

```
Node 01: Primary Grade (Balance, Exposure, Contrast)
Node 02: Texture Pop Effect
  ├─ Custom Curve (S-curve in midtones)
  └─ Blur OFX → Overlay/Soft Light composite
Node 03: Creative Grade / Film Emulation / Grain
```

## Step-by-Step Procedure

### 1. Primary Grade First
Complete base balance before texture enhancement:
- Exposure, White Balance, Contrast
- Color Managed pipeline recommended

### 2. Build Texture Pop (Node 02)

**Option A: Custom Curve + Blur (Free & Studio)**

1. **Add Custom Curve OFX** (or use Curves panel)
2. **Create Micro-Contrast S-Curve:**
   - Anchor: (0.0, 0.0) and (1.0, 1.0)
   - Midtone lift: 0.50 → 0.53 to 0.55
   - Quarter-tone push: 0.25 → 0.22, 0.75 → 0.78
   - Creates localized contrast in texture frequency range

3. **Add Blur OFX:**
   - Radius: **2-5px** (4K: 3-5, HD: 2-3)
   - Composite Mode: **Overlay** (or Soft Light)
   - Opacity: **20-40%**
   - Acts as unsharp mask via local contrast

**Option B: Spatial NR Sharpen (Studio Only)**

1. Open **Motion Effects** panel → **Spatial Noise Reduction**
2. Mode: **Sharpen** (not NR)
3. Radius: **0.5-1.5**
4. Threshold: **5-15**
5. Blend: **30-50%**

### 3. Blend & Refine
- Texture Pop node blend: **30-50% opacity** (parallel) or adjust curve/blur intensity
- Check at 100% zoom for halos/noise

## Parameter Presets

| Style | Curve Mid Lift | Blur Radius | Blur Opacity | Blend |
|-------|----------------|-------------|--------------|-------|
| **Subtle** | +0.03 | 2px | 15% | 25% |
| **Medium** | +0.05 | 3px | 30% | 40% |
| **Strong** | +0.08 | 5px | 45% | 50% |

## Selective Application

### Power Window (Subject Isolation)
- Circular/oval window on subject
- **Invert** → Apply to background only
- Track if camera/subject moves

### Qualifier (Skin Protection)
- HSL Qualifier on skin tones
- **Invert** → Reduce effect on skin
- Softness: High (50-80)

### Luma Key (Shadow/Highlight Control)
- Limit to midtones (0.2-0.8)
- Prevents noise in shadows, halos in highlights

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Halos on edges | Blur radius too large | Reduce to 2-3px |
| Noise amplification | Footage noisy, effect too strong | Denoise first, lower blend |
| Plastic skin look | Applied to face | Power Window invert or Qualifier exclude |
| Color shifts | Overlay on saturated areas | Use Soft Light, check Vectorscope |
| Overdone "crunch" | All settings maxed | Dial back to subtle preset |

## S-Log3 / Log Footage Considerations
- Apply **AFTER** CST to Rec.709
- Log noise in shadows → Denoise before Texture Pop
- Highlight latitude → Check for highlight halos at 100% zoom

## Related Skills
- `davinci-resolve-sharpening-marco-herbst` — Marco Herbst's 3 sharpening hacks
- `davinci-resolve-edge-detect-soften` — Edge Detect alternative to Texture Pop
- `davinci-resolve-sharpening-3-hacks` — Kasia Jarco / Color Grading Insights 3 methods
- `davinci-resolve-promist-slog3-dreamy` — Opposite effect (softening/diffusion)

## References
- Source: @davinciresolved Instagram Reel (May 28, 2025)
- Hashtags: #davinciresolve #videoediting #colorgrading #davinci
- Community feedback: "You're like The Hoof GP of davinci tutorials 🐄"