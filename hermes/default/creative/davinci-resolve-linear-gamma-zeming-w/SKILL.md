---
name: davinci-resolve-linear-gamma-zeming-w
category: creative
description: "DaVinci Resolve Linear Gamma Setting — Accurate, realistic color grading workflow using linear gamma for natural results"
tags:
  - davinci-resolve
  - linear-gamma
  - color-grading
  - color-management
  - cst
  - zeming-w
version: 1.0.0
author: "zeming_w (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DFJoUj3s3Qx/"
---

# DaVinci Resolve: Linear Gamma Setting — Realistic Color Grading

## Overview
Technique using **Linear Gamma** setting in DaVinci Resolve for accurate, lighting-accurate, realistic, and natural color grading. Transforms footage into any color profile with photometric precision.

## Core Concept

### Why Linear Gamma?
- **Standard gamma (2.2/2.4)**: Perceptual encoding — not linear light
- **Linear Gamma (1.0)**: Scene-referred linear light — matches physical light behavior
- **Benefits**: Exposure adjustments are photometric, no hue shifts, CST works correctly

## Node Structure

```
Node 01: Input (Log/Raw)
Node 02: **CST: Camera Log → Linear Gamma (1.0)** — Critical!
Node 03: Primary Grade (Exposure, WB in Linear)
Node 04: Creative Grade
Node 05: **CST: Linear → Display Gamma (2.4 / PQ / HLG)**
Node 06: Output
```

## Step-by-Step Workflow

### 1. Input CST to Linear Gamma (Node 02)
- **Input Color Space**: Camera native (S-Log3/S-Gamut3, V-Log/V-Gamut, etc.)
- **Input Gamma**: Camera log curve
- **Output Color Space**: Same gamut (or DWG/ACEScg)
- **Output Gamma**: **Linear (1.0)** — **This is the key setting**

### 2. Grade in Linear Space (Node 03-04)
- **Exposure**: Use **Gain** (not Offset) — true photometric scaling
- **White Balance**: RGB Gain channels — no hue shift
- **Contrast**: Custom Curves or Log Wheels — linear response
- **Creative**: All operations behave physically correctly

### 3. Output CST from Linear (Node 05)
- **Input**: Linear gamma, working gamut
- **Output**: Display gamma (Rec.709 2.4, P3 2.6, PQ, HLG)
- **Tone Mapping**: For HDR outputs

## Critical Settings

| Node | Input Gamma | Output Gamma | Purpose |
|------|-------------|--------------|---------|
| **02** | Camera Log | **Linear (1.0)** | Decode to scene-linear |
| **05** | Linear (1.0) | Display (2.4/PQ) | Encode for display |

## Pro Tips

- **"Don't believe me, then please give it a try!"** — @zeming_w
- **CST Sandwich**: Linear in middle = all grading in physically correct space
- **Single CST at end only**: Works but less accurate — log math on creative ops
- **Color Managed alternative**: Set Timeline = Linear, Output = Display — same result

## Common Questions (from comments)

> **"CST at first and last vs only at end — which is right?"** — @metaphor_foto
> **Both work**. CST sandwich (first+last) = grade in linear/working space (accurate). Single CST at end = grade in log space (faster, but exposure/contrast behave perceptually, not photometrically). **For precision: sandwich**.

> **"If you don't shoot log, do you still do CST nodes?"** — @hamzuh
> Yes — any non-linear source (Rec.709, HLG) needs CST to linear for photometric grading. If already linear (rare), skip.

> **"Nice edit / Great tip / Thanks!"** — Multiple users
> Community validates the technique.

## Linear Gamma vs Log Grading Comparison

| Aspect | Log Space Grading | Linear Gamma Grading |
|--------|-------------------|---------------------|
| **Exposure** | Perceptual (Lift/Gamma/Gain) | **Photometric (Gain = true scaling)** |
| **WB** | Hue shifts at extremes | **No hue shift** |
| **Contrast** | S-curve on log | **True linear contrast** |
| **CST Accuracy** | Approximate | **Exact** |
| **Speed** | Faster (1 CST) | Slower (2 CST) |

## Related Skills
- `davinci-resolve-color60-apply-inverse-ootf` — Inverse OOTF for Rec.709→Log
- `davinci-resolve-manual-color-profile-conversion` — CST bypass, Log→Rec.709
- `davinci-resolve-white-balance-linear-mode-gablasc` — Linear mode WB
- `davinci-resolve-simple-4-step-workflow` — CST, WB, Contrast, Stop

## Source
Instagram: @zeming_w — "This is the Linear Gamma setting in DaVinci Resolve..."
URL: https://www.instagram.com/reel/DFJoUj3s3Qx/
Date: 2025-07-12