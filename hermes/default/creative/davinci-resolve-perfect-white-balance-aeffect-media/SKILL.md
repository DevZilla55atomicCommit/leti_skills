---
name: davinci-resolve-perfect-white-balance-aeffect-media
category: creative
description: "DaVinci Resolve: Perfect White Balance in Seconds — Quick WB workflow using Gain, Gray Card, Parade/Vectorscope"
tags:
  - davinci-resolve
  - white-balance
  - color-correction
  - gain-vs-offset
  - gray-card
  - parade
  - vectorscope
  - aeffect-media
version: 1.0.0
author: "aeffect.media (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DFzIiiKy5Cw/"
---

# DaVinci Resolve: Perfect White Balance in Seconds

## Overview
Quick white balance workflow emphasizing **checking WB on every clip** before creative grading. Uses **RGB Gain** (not Offset) with Parade and Vectorscope for consistent, accurate results.

## Core Philosophy

> "If the LUTs, colour grades or presets you use are not working, the chances are your white balance is not set correctly. It's a wise idea before you start the colour grading process to correct your white balance, even if the camera sets it automatically. Build the habit of checking each clip."

## Why Gain, Not Offset?

**Offset** (Lift): Shifts entire signal — affects shadows disproportionately
**Gain**: Scales signal proportionally — preserves relative channel relationships

For WB: **Gain = Photometric scaling** (like changing exposure per channel)
- Matches how light actually works
- Cleaner, more natural results
- Parade RGB stays balanced through tonal range

## Quick WB Workflow (Seconds per Clip)

### 1. Scopes Setup
- **Parade RGB** (primary): Watch R/G/B alignment
- **Vectorscope** (verify): Neutral = center dot

### 2. Find Neutral Reference
- **Gray card** / White card / Neutral surface in frame
- **No reference?** Use **Qualifier** on likely neutral (white shirt, wall, cloud)

### 3. Adjust RGB Gain (Color Wheels → Gain)
1. **Green = Reference** (usually leave at 1.0)
2. **Red Gain**: Adjust until Red trace aligns with Green on Parade
3. **Blue Gain**: Adjust until Blue trace aligns with Green on Parade
4. **Verify**: Vectorscope trace centers on crosshair

### 4. Confirm
- Toggle node on/off — should look neutral, no cast
- Check skin tones on Vectorscope (skin tone line ~103°)

## Node Structure

```
Node 01: Input
Node 02: CST (Camera → Working)
Node 03: **WB Gain Balance** (This node — label "WB Fix")
Node 04: Primary Grade
Node 05: Creative LUT / Look
Node 06: Output CST
```

## Pro Tips

- **Per-clip habit**: WB check takes 10 seconds, saves minutes of fighting LUTs
- **Auto WB ≠ Accurate WB**: Camera AWB drifts, shifts with scene content
- **Gain first, then Offset if needed**: Only use Offset for creative tint after Gain is neutral
- **Parade > Vectorscope for WB**: Parade shows channel balance directly
- **Match clips**: Copy WB node (CMD+Option+C / CTRL+Alt+C) → Paste Attributes (CMD+Option+V) to matching shots

## Common Questions (from comments)

> **"Why Gain and not Offset?"** — @michael.mivid
> Gain scales channels proportionally (photometric). Offset shifts entire signal, crushing/raising shadows unevenly. Gain = correct WB; Offset = creative tint.

> **"Do you need Studio version?"** — @kierenmurphyy
> No — Color Wheels (Gain/Offset) and Scopes are in Free version.

> **"See color parade is important too"** — @thoriqkurobing
> Yes — Parade RGB is the primary WB tool; Vectorscope confirms.

> **"I use a gray card and it works perfectly every time"** — @dantheironpan
> Gray card = fastest, most accurate reference. Always shoot one per setup/lighting change.

## Related Skills
- `davinci-resolve-white-balance-luma-mix` — Luma Mix=0, RGB Gain
- `davinci-resolve-rgb-mixer-white-balance` — Ivar Brauer 3-axis control
- `davinci-resolve-white-balance-linear-mode-gablasc` — Linear mode, Luma Mix=0
- `davinci-resolve-white-balance-3-methods` — Ivar Brauer: Temp/Tint, Linear, Gray Card

## Source
Instagram: @aeffect.media — "How to achieve perfect white balance in a matter of seconds"
URL: https://www.instagram.com/reel/DFzIiiKy5Cw/
Date: 2025-07-12