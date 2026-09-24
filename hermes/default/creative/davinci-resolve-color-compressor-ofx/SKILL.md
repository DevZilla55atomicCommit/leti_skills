---
name: davinci-resolve-color-compressor-ofx
category: creative
description: DaVinci Resolve Color Compressor OFX (Studio 20+) for unified gamut mapping and color spill control
tags:
  - davinci-resolve
  - color-compressor
  - ofx
  - studio
  - gamut-mapping
  - color-spill
  - davinciresolved
version: 1.0.0
author: davinciresolved (extracted by Hermes Agent)
source_url: https://www.instagram.com/reel/DKAAH6VvR7H/
---

# DaVinci Resolve: Color Compressor OFX (Studio 20+)

## Overview
The **Color Compressor** is a Studio-only OFX plugin introduced in DaVinci Resolve 20 that provides unified gamut mapping and color spill/oversaturation control in a single tool. It replaces complex node trees for gamut compression.

## Core Concept

### What It Does
- **Gamut Mapping**: Compresses source gamut to target gamut in one operation
- **Color Spill Control**: Fixes oversaturated colors that bleed/contaminate adjacent hues
- **Unified Workflow**: Combines what previously required CST + Qualifier + Curves nodes
- **Perceptual Accuracy**: Uses advanced color science (CAM16/ICAM) for natural compression

### When to Use
- HDR → SDR gamut compression
- Wide gamut (DWG, Rec.2020) → Rec.709 delivery
- Fixing color spill from strong creative grades
- Camera gamut mapping (S-Gamut3, V-Gamut, etc. → Working Space)

## Node Placement

```
Node 01: Input (Log/Raw)
Node 02: CST (Camera → Working Space, e.g., DaVinci Wide Gamut)
Node 03: Primary Grade (Exposure, WB, Contrast)
Node 04: Creative Look / Film Emulation
Node 05: **Color Compressor OFX** (Working → Display Gamut)
Node 06: Output CST (if needed for specific deliverable)
```

**Critical**: Place **after** creative grade, **before** final output transform.

## Color Compressor Parameters

| Parameter | Function | Typical Setting |
|-----------|----------|-----------------|
| **Input Gamut** | Source color space | Auto (from clip) or Manual: DWG, Rec.2020, etc. |
| **Output Gamut** | Target color space | Rec.709, P3-D65, Rec.2020 |
| **Method** | Compression algorithm | **Perceptual** (default, filmic) / **Saturation** / **Clip** |
| **Strength** | Compression intensity | 0.5–1.0 (1.0 = full compression) |
| **Preserve Luminance** | Protect brightness | **On** (recommended) |
| **Color Spill Suppression** | Reduce hue contamination | 0.2–0.5 (subtle) |
| **Highlight Roll-off** | Smooth highlight compression | 0.3–0.7 |
| **Shadow Protection** | Prevent shadow crushing | 0.1–0.3 |

## Workflow Examples

### 1. HDR Grading → SDR Delivery
```
Input: ST.2084 / Rec.2020 (HDR)
Working: DaVinci Wide Gamut / HLG or PQ
Grade: Creative look in wide gamut
Color Compressor: 
  - Input: DaVinci Wide Gamut
  - Output: Rec.709
  - Method: Perceptual
  - Strength: 1.0
  - Highlight Roll-off: 0.5
Output: Rec.709 / Gamma 2.4
```

### 2. Fixing Color Spill from Aggressive Grade
```
Node N: Creative grade (heavy saturation, hue shifts)
Node N+1: Color Compressor
  - Input: Working Gamut
  - Output: Working Gamut (same)
  - Method: Saturation
  - Strength: 0.3–0.5
  - Color Spill Suppression: 0.4
  - Preserve Luminance: On
Result: Controlled saturation, fixed hue bleeding
```

### 3. Camera Gamut → Working Space (Alternative to CST)
```
Input: S-Log3 / S-Gamut3.Cine
Color Compressor:
  - Input: S-Gamut3.Cine
  - Output: DaVinci Wide Gamut
  - Method: Perceptual
  - Strength: 1.0
Advantage: Single node, perceptual mapping, no CST round-trip
```

## Method Comparison

| Method | Best For | Characteristics |
|--------|----------|-----------------|
| **Perceptual** | General gamut mapping, HDR→SDR | Filmic, preserves hue relationships, natural rolloff |
| **Saturation** | Color spill control, creative compression | Reduces saturation uniformly, good for spill |
| **Clip** | Hard limits, technical delivery | Hard clips out-of-gamut, use only for QC |

## Pro Tips

- **Always enable "Preserve Luminance"** — prevents brightness shifts during compression
- **Use Strength < 1.0 for creative spill control** — 1.0 is for full gamut mapping
- **Combine with CST**: CST for camera→working, Color Compressor for working→display
- **Check Scopes**: Parade RGB for clipping, Vectorscope for gamut boundary
- **Studio Only**: Requires DaVinci Resolve Studio 20+ (Free version lacks Color Compressor OFX)
- **Version Note**: Resolve 20.2+ has improved highlight handling

## Comparison: Color Compressor vs Traditional Workflow

| Aspect | CST + Qualifier + Curves | Color Compressor OFX |
|--------|-------------------------|---------------------|
| Nodes Required | 3–5 | 1 |
| Perceptual Accuracy | Manual tuning | Built-in CAM16/ICAM |
| Color Spill Fix | Separate qualifier nodes | Integrated parameter |
| Highlight Rolloff | Custom curves | Dedicated parameter |
| Workflow Speed | Slow | Fast |
| Flexibility | High (per-channel) | Unified (global) |

## Related Skills
- `davinci-resolve-cst-gamut-mapping-color-spill` — CST-based gamut mapping
- `davinci-resolve-gamut-io-fix-banding-luts` — Banding fixes with LUTs
- `davinci-resolve-tetrahedral-interpolation-luts` — LUT interpolation quality

## Source
Instagram: @davinciresolved — "Color compressor in DaVinci Resolve"
URL: https://www.instagram.com/reel/DKAAH6VvR7H/
Date: 2025-07-11