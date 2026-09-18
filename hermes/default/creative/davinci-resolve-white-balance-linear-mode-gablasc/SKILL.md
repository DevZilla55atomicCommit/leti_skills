---
name: davinci-resolve-white-balance-linear-mode-gablasc
category: creative
description: "DaVinci Resolve White Balance in Linear Mode with Luma Mix = 0 for precise channel control"
tags:
  - davinci-resolve
  - white-balance
  - linear-mode
  - luma-mix
  - rgb-mixer
  - vectorscope
  - gablasc
version: 1.0.0
author: "gablasc (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DKBME3_g_jD/"
---

# DaVinci Resolve: White Balance in Linear Mode with Luma Mix = 0

## Overview
Technique for precise white balance using **RGB Mixer in Linear Mode** with **Luma Mix = 0**. This approach performs WB adjustments in linear gamma space for photometrically accurate channel balancing, avoiding the hue shifts that can occur in log/gamma-encoded space.

## Core Concept

### Why Linear Mode for WB?
- **Photometric accuracy**: Linear light = how light actually behaves physically
- **No gamma distortion**: Channel ratios preserved without gamma curve interference
- **Cleaner separation**: Red/Green/Blue gain adjustments don't shift hue unexpectedly
- **Vectorscope precision**: Neutral axis alignment more accurate in linear

### The Luma Mix = 0 Key
- **Default Luma Mix = 1**: RGB Mixer blends with luminance (preserves brightness)
- **Luma Mix = 0**: Pure RGB channel mixing — no luminance compensation
- **Result**: True channel gain control, essential for linear WB accuracy

## Node Structure

```
Node 01: Input (Log/Raw)
Node 02: CST (Camera → Linear Working Space, e.g., DWG Linear / ACEScct Linear)
Node 03: Primary Balance (Exposure, rough WB)
Node 04: **RGB Mixer — Linear Mode, Luma Mix = 0** (Precise WB)
Node 05: CST (Linear → Working Gamma, e.g., DWG / ACEScct)
Node 06: Creative Grade
Node 07: Output CST (Working → Display)
```

## Step-by-Step Workflow

### 1. Set Up Linear Working Space
**Project Settings → Color Management:**
- **Color Science**: DaVinci YRGB Color Managed
- **Processing Mode**: DaVinci Wide Gamut (or ACEScct)
- **OR**: Use CST node: Input = Camera Log, Output = **DWG Linear** / **ACEScct Linear**

### 2. Add RGB Mixer Node
1. Add **Serial Node** → Label "WB Linear"
2. Open **RGB Mixer** (not Color Wheels)
3. **Critical Settings**:
   - **Mode**: **Linear** (dropdown: Video/Linear/Log → select Linear)
   - **Luma Mix**: **0** (slider all the way down)

### 3. White Balance Procedure
1. **Open Vectorscope** — enable **Skin Tone Indicator** (optional) or just use center crosshair
2. **Find Neutral Reference**: White/gray card, white shirt, neutral wall
3. **Qualify Neutral Area**: Use Qualifier (HSL) or Power Window to isolate neutral patch
4. **Adjust RGB Gain** (not Offset!):
   - **Red Gain**: Adjust until neutral trace centers on vectorscope
   - **Green Gain**: Fine-tune (usually leave at 1.0 as reference)
   - **Blue Gain**: Adjust to center trace
5. **Verify**: Toggle node — image should look neutral, no color cast

### 4. Return to Gamma Space (if using CST approach)
- Add CST after RGB Mixer: Linear → DWG / ACEScct (gamma)
- Continue grading in gamma-encoded space

## RGB Mixer Settings Reference

| Parameter | Setting | Why |
|-----------|---------|-----|
| **Mode** | **Linear** | Photometric channel mixing |
| **Luma Mix** | **0** | Pure RGB, no luminance compensation |
| **Red Gain** | ~0.8–1.3 | Channel balance for WB |
| **Green Gain** | 1.0 (ref) | Reference channel |
| **Blue Gain** | ~0.8–1.3 | Channel balance for WB |
| **Red/Green/Blue Lift** | 0 | Don't use for WB (use Gain) |

## Pro Tips

- **Qualifier First**: Always isolate a true neutral (gray card, white reference) before adjusting
- **Vectorscope Center**: Perfect neutral = single pixel at center — but slight spread is normal
- **Green as Reference**: Keep Green Gain = 1.0, adjust Red/Blue relative to it
- **Linear vs Log Wheels**: Log Wheels = perceptual; Linear RGB Mixer = photometric
- **Combine with CST**: Camera Log → Linear (CST) → RGB Mixer → Gamma (CST) → Grade
- **Exposure First**: Set exposure (middle gray ~18-40 IRE) before WB for accurate vectorscope

## Common Questions from Comments

> **"What does linear mean?"**
> Linear = gamma 1.0, no curve. Light values proportional to photon count.

> **"Luma Mix to 0 before using gain"**
> Correct — Luma Mix 1.0 compensates brightness changes, which fights your WB adjustments.

> **"Better to use HDR wheels / X-Y balance"**
> HDR wheels are perceptual (log-encoded). Linear RGB Mixer is technically more accurate for WB.

> **"Why linear node?"**
> Isolates WB operation in linear light — prevents gamma/hue interaction artifacts.

## Related Skills
- `davinci-resolve-white-balance-luma-mix` — Luma Mix = 0 + RGB Gain (Rolling Shutter Media)
- `davinci-resolve-rgb-mixer-white-balance` — Ivar Brauer 3-axis channel control
- `davinci-resolve-white-balance-helper-window-technique` — WB via Power Window + Highlight Mode
- `davinci-resolve-white-balance-linear-mode` — Marco Herbst WB Helper: Source Window + Linear Gamma

## Source
Instagram: @gablasc — "Hope this helped!!!"
URL: https://www.instagram.com/reel/DKBME3_g_jD/
Date: 2025-07-11