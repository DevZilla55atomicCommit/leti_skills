---
name: davinci-resolve-white-balance-linear-mode
category: creative
description: "White Balance in Linear Mode with Luma Mix = 0 using Vectorscope for precise neutral balance — @gablasc technique"
tags:
  - davinci-resolve
  - color-grading
  - white-balance
  - linear-mode
  - luma-mix
  - vectorscope
  - rgb-gain
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKBME3_g_jD/"
creator: "@gablasc"
vault_file: "Color Correction Fundamentals/15-White-Balance-Linear-Mode_Luma-Mix-Zero_gablasc_Vectorscope-WB.md"
---

# White Balance in Linear Mode with Luma Mix = 0

## Overview
Technique for precise technical white balance correction using DaVinci Resolve's Linear node mode with Luma Mix set to 0, monitoring on Vectorscope to center the trace for perfect neutral balance.

## When to Use
- Technical white balance correction (neutralize color casts)
- Shot matching where precise neutral is critical
- Log/RAW footage before creative grading
- When Temperature/Tint controls aren't precise enough

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Footage in a scene-referred color space (or after CST to linear)
- Basic understanding of Vectorscope and Parade RGB

## Step-by-Step Procedure

### 1. Setup Node Structure
```
Node 01: CST / Input Transform (if needed)
Node 02: [NEW] Serial Node — Set to Linear Mode
```

### 2. Configure Linear Node
1. Right-click Node 02 → **Color Space** → **Linear**
2. Open **Key** panel (or Node Key Output)
3. Set **Luma Mix = 0** (critical — decouples luma from chroma)

### 3. Monitor on Vectorscope
- Open **Vectorscope** (Window → Vectorscope)
- Disable **Skin Tone Indicator** (not needed for WB)
- Neutral white/gray should sit at **exact center** (zero saturation)
- Any offset from center = color cast direction

### 4. Adjust RGB Gain Wheels
| Wheel | Vectorscope Shift |
|-------|-------------------|
| **Red Gain** | Toward Cyan (opposite) / Red |
| **Green Gain** | Toward Magenta / Green |
| **Blue Gain** | Toward Yellow / Blue |

Adjust each gain until trace centers perfectly.

### 5. Verify on Parade RGB
- Open **Parade RGB** scope
- Neutrals should show **perfectly aligned R/G/B channels**
- Any separation = residual color cast

## Key Principles

### Why Linear Mode?
- Scene-referred linear light = physically accurate color math
- No gamma curve distorting color relationships
- Gain adjustments behave linearly (perceptually uniform)

### Why Luma Mix = 0?
- Default Luma Mix = 1.0 (luma contributes to output)
- Luma Mix = 0 → **chroma-only output** from this node
- Prevents brightness shifts while adjusting color balance
- Pure chrominance correction

### Why Vectorscope?
- Visual center-target for neutral
- More precise than Temp/Tint sliders
- Shows exact hue/saturation of cast

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Forgot Luma Mix = 0 | Brightness shifts when adjusting Gain — always verify Luma Mix = 0 |
| Node not in Linear | Right-click node → Color Space → Linear (not "Linear RGB" if different) |
| Adjusting Offset instead of Gain | Offset shifts entire signal — use Gain for WB |
| Parade shows separation after centering | Double-check node order (WB before creative grades) |

## Variations

### With Qualifier (for specific region)
1. Add Qualifier on Node 02
2. Sample neutral gray/white reference in frame
3. Adjust Gain while watching *only that region* on Vectorscope

### Combined with CST Workflow
```
Node 01: Camera → DaVinci YRGB (CST)
Node 02: Linear + Luma Mix 0 → WB Correction (this technique)
Node 03+: Creative Grade
```

## Related Skills
- `davinci-resolve-white-balance-luma-mix` — Luma Mix with RGB Gain (non-linear)
- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer surgical WB (@ivarbrauer)
- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier as measurement tool
- `davinci-resolve-auto-balance-ivarbrauer` — Auto Balance comparison

## References
- Source: @gablasc Instagram Reel (May 23, 2025)
- Community discussion: Linear mode WB best practices
- DaVinci Resolve Manual: Node Color Spaces, Key Panel Luma Mix