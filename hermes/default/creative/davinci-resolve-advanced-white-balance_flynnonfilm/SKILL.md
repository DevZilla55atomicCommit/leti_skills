---
name: davinci-resolve-advanced-white-balance_flynnonfilm
category: creative
description: "Advanced White Balance beyond Temp & Tint — RGB Mixer with Luma Mix = 0, Custom Curves per-luminance, Vectorscope/Parade verification for surgical precision"
tags:
  - davinci-resolve
  - color-grading
  - white-balance
  - temp-tint
  - rgb-mixer
  - luma-mix
  - vectorscope
  - parade
  - precision-wb
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DIyuyeHsd6m/"
creator: "@flynn.on.film"
vault_file: "Color Correction Fundamentals/59-Advanced-WB_flynnonfilm_RGB-Mixer-Luma-Mix.md"
---

# Advanced White Balance — Beyond Temp & Tint

## Overview
Professional white balance using **RGB Mixer (Luma Mix = 0)**, **Custom Curves (per-luminance)**, and **scope verification** — replaces crude Temp/Tint with surgical 3-4 axis chrominance control.

## When to Use
- **Every grade** — WB is the foundation; wrong WB breaks downstream
- Precision required (product, beauty, narrative consistency)
- Mixed lighting (shadows ≠ highlights WB)
- Skin tone critical (WB affects skin hue directly)
- **Not for**: Quick social cuts (Temp/Tint fine)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Scope literacy: Parade RGB, Vectorscope, Waveform
- Understanding of luma/chroma separation
- Basic RGB color theory

## Core Principle

> **Temp & Tint = 2-axis display-referred. Pro WB = 3-4 axis scene-referred with Luma Mix = 0.**

### The Luma Mix = 0 Insight
| Luma Mix | Behavior |
|----------|----------|
| **100 (Default)** | RGB changes affect BOTH color AND brightness |
| **0** | RGB changes affect ONLY color (chroma), luminance locked |

**@hands.solo**: "You should also set the luma mix to 0" — This is the professional standard.

---

## Method 1: RGB Mixer (Luma Mix = 0) — Most Precise

### Setup
1. **Color Wheels Panel** → **RGB Mixer** tab (or RGB Mixer OFX)
2. **Luma Mix = 0** (Critical!)
3. **Output Channel Sliders** → Adjust for neutral

### Procedure
1. **Find neutral reference** (gray card, white shirt, known neutral)
2. **Parade RGB** → Observe R/G/B misalignment at neutral
3. **Adjust Output Channels**:
   - Output Red → Red slider (reduce if red cast)
   - Output Green → Green slider
   - Output Blue → Blue slider
4. **Target**: R=G=B at neutral on Parade
5. **Verify**: Vectorscope center dot, Waveform stable

### Channel Logic
| Cast | Adjustment |
|------|------------|
| **Red/Orange** | Reduce Output Red, Increase Output Blue |
| **Blue/Cool** | Reduce Output Blue, Increase Output Red |
| **Green** | Reduce Output Green, Balance R/B |
| **Magenta** | Reduce Output Red & Blue, Increase Green |

---

## Method 2: Custom Curves (RGB, Per-Luminance) — Zone WB

### Setup
1. **Custom Curves OFX** → **RGB** mode (Break Chain)
2. **Independent R/G/B curves**

### Procedure
1. **Identify zones** on Parade:
   - **Shadows** (0-30%): Often cool (blue cast)
   - **Midtones** (30-70%): Primary WB (gray cards, skin)
   - **Highlights** (70-100%): Often warm (specular)
2. **Add anchors** at zone boundaries
3. **Adjust per channel per zone**:
   - Shadows: Blue down / Red up (warm shadows)
   - Midtones: Balance R=G=B
   - Highlights: Red down / Blue up (cool highlights)

### Advantage
Real-world lighting has **different WB per luminance zone** — curves handle this; Temp/Tint cannot.

---

## Method 3: Offset/Color Wheels (Fast, Good Enough)

### Setup
1. **Color Wheels** → **Offset** (master) or **Lift/Gamma/Gain**
2. **Parade + Vectorscope** visible

### Procedure
1. **Offset** → Nudge toward neutral on Parade
2. **Vectorscope** → Gray patch to center
3. **Check**: Skin tone line (103°)

### Limitation
- Coupled adjustments
- Display-referred
- No Luma Mix control

---

## Method 4: White Balance OFX (Auto + Refine)

### Setup
1. **Effects** → **Resolve FX Color** → **White Balance**
2. **Auto** (Picker on gray card)
3. **Manual refine** (Temp/Tint + Luma Mix)

### Advantage
- Auto from reference
- Luma Mix control available
- Good starting point

---

## Verification Workflow (Mandatory)

### 1. Parade RGB (Primary)
```
Neutral Reference:
R ████████
G ████████  ← Align perfectly
B ████████
```

### 2. Vectorscope (Secondary)
```
Gray Patch → Center dot (zero hue)
Skin Tone → On 103° line
```

### 3. Waveform (Luminance Integrity)
```
Gray Patch → Flat line at expected IRE
NO SHIFT after WB (confirms Luma Mix = 0)
```

---

## Scenario-Based Method Selection

| Scenario | Best Method | Why |
|----------|-------------|-----|
| **Gray card in shot** | RGB Mixer + Picker | Precise, measurable |
| **No card, known neutral** | Custom Curves (Midtones) | Per-luminance control |
| **Mixed lighting** | Custom Curves (Zones) | Shadows≠Highlights WB |
| **Skin tone priority** | RGB Mixer + Vectorscope | Skin on line = correct |
| **Fast turnaround** | Offset Wheel + Scopes | Good enough, fast |
| **BRAW/RAW metadata** | Camera WB + Refine | Start from sensor data |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Luma Mix = 100 | Exposure shifts during WB | **Luma Mix = 0** |
| No scope verification | Guessing | **Parade + Vectorscope always** |
| Single zone WB | Shadows/Highlights wrong | **Custom Curves zones** |
| Ignore skin line | Magenta/Green skin | **Vectorscope 103° target** |
| Temp/Tint only | Coarse, coupled | **RGB Mixer or Curves** |
| Grade before WB | LUTs/looks fail | **WB FIRST, always** |

---

## Pro Tips

- **@hands.solo**: "Luma mix to 0" — The defining pro technique
- **@fueledbyhart**: "Thanks for the help" — Practical, works
- **@floris_vroegh**: "BRAW lets you change in post" — RAW = WB flexibility
- **@flynn.on.film**: Director sees emotion; Colorist sees technique — Bridge both
- **Save as PowerGrade** — Reusable WB node for camera types

---

## Related Skills
- `davinci-resolve-white-balance-linear-mode` — RGB Gain + Luma Mix 0
- `davinci-resolve-white-balance-luma-mix` — Luma Mix technique
- `davinci-resolve-skin-tones-right_mansourmelouli` — WB for skin
- `davinci-resolve-three-color-fundamentals_chrisseinn` — YRGB foundations
- `davinci-resolve-color-management-timeline_caleboshi` — WB in CM pipeline

---

## References
- Source: @flynn.on.film Instagram Reel (Apr 23, 2025)
- Hashtags: #director #cinematographer #colorist #colorgrading #colorgradinglife #colorgradingtutorial #davinciresolve #davinciresolve18 #davinciresolvetutorial #howto #tutorial #viral #explore #bts
- Engagement: 22K likes, 115 comments
- Key insight: Community-driven "Luma Mix = 0" in comments