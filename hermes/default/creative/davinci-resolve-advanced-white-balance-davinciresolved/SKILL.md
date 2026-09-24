---
name: davinci-resolve-advanced-white-balance-davinciresolved
description: Advanced white balance in DaVinci Resolve — Parade RGB alignment, chromatic adaptation, Raw tab vs Color page, vectorscope centering methods
category: creative
tags: [davinci-resolve, white-balance, parade-rgb, vectorscope, chromatic-adaptation, raw-tab, davinciresolved]
source_url: https://www.instagram.com/reel/DLpjSmBx24R/
author: davinciresolved
---

# DaVinci Resolve: Advanced White Balance

> **"Advanced white balance in DaVinci Resolve"** — davinciresolved

## Core Concept: Beyond Temp/Tint

Basic WB uses **Temp/Tint** sliders. Advanced WB uses **Parade RGB alignment**, **Vectorscope centering**, **Chromatic Adaptation**, and **Raw Tab** controls for scientific accuracy.

---

## Method Comparison

| Method | Tool | Precision | Best For |
|--------|------|-----------|----------|
| **Temp/Tint** | Color Wheels | Low | Quick fixes, creative warm/cool |
| **Parade RGB** | Waveform (Parade) | High | Technical neutrality, broadcast |
| **Vectorscope** | Vectorscope (center crosshair) | High | Skin tones, memory colors |
| **RGB Mixer** | RGB Mixer (Linear) | Very High | Printer lights, channel surgery |
| **Chromatic Adaptation** | CST / CAT | Scientific | Cross-illuminant matching |
| **Raw Tab** | Camera Raw Panel | Highest | Raw metadata, sensor-native |

---

## Method 1: Parade RGB Alignment (Technical Neutral)

### Principle
Neutral grays = **R = G = B** on Parade waveform.

### Steps
1. **Open Parade RGB** (Waveform → Parade)
2. **Find neutral reference** (gray card, white shirt, concrete, pavement)
3. **Adjust per channel:**
   - **Lift (Shadows):** Align R/G/B at black point
   - **Gamma (Midtones):** Align at 18% gray / 40–50 IRE
   - **Gain (Highlights):** Align at white point / 90 IRE

### Color Wheels Settings (Linear Mode)
```
Node: WB Balance
├── Color Space: Linear (or CST to Linear)
├── Luma Mix: 0
├── Gain Pivot: 0.335
├── Lift: Adjust R/G/B for shadow neutrality
├── Gamma: Adjust R/G/B for midtone neutrality  
└── Gain: Adjust R/G/B for highlight neutrality
```

---

## Method 2: Vectorscope Centering

### Principle
Neutral = **center of vectorscope** (zero saturation).

### Steps
1. **Open Vectorscope** — Enable **Center Crosshair**
2. **Select neutral target** (gray card, white object)
3. **Adjust Temp/Tint or RGB Gain** until target sits on center crosshair
4. **Verify on Parade** — R=G=B at target luminance

> **@thoriqkurobing:** *"Yes, perfect way to balance is centering as possible to center Vectorscope 🙌"*

---

## Method 3: Chromatic Adaptation (Scientific)

### What It Is
**CAT (Chromatic Adaptation Transform)** mathematically converts colors from one illuminant to another (e.g., D65 → D50, Tungsten → Daylight).

### In Resolve
```
CST Node:
├── Input: Camera Log + Illuminant (e.g., D65)
├── Output: Target + Illuminant (e.g., Rec.709 D65)
├── CAT Method: Bradford / Von Kries / CAT02 / CAT16
└── Result: Proper white point adaptation, not just RGB scaling
```

> **@d29.h45:** *"Why not use chromatic adaptation?"*
>
> → **Answer:** CAT is built into CST. Use CST with correct illuminant metadata for scientific WB.

---

## Method 4: Raw Tab (Sensor-Native)

### For BRAW / ProRes RAW / CinemaDNG
```
Raw Tab (Clip/Color Page):
├── Decode Quality: Full / Half / Quarter
├── Color Space: Camera Native (BMD Film, S-Gamut3, etc.)
├── Gamma: Camera Log (BRAW Film, S-Log3, etc.)
├── White Balance: 
│   ├── Temp/Tint (metadata-based)
│   ├── Kelvin Presets (3200K, 4500K, 5600K, 6500K)
│   └── Custom Kelvin + Tint
├── ISO: Native / Extended
└── Highlight Recovery: On/Off
```

> **@alain.vient:** *"Can't you do this in the raw tab?"*
>
> → **Yes!** Raw tab WB is **metadata-based, non-destructive**, uses sensor calibration. Best starting point.

### Raw Tab → Color Page Workflow
```
1. Raw Tab: Set WB to "As Shot" or measured Kelvin
2. Color Page: Fine-tune with Parade/Vectorscope
3. Benefit: Raw WB = optimal sensor data; Color WB = creative refinement
```

---

## Method 5: RGB Mixer (Printer Lights)

### In Linear Space
```
Node: RGB Mixer (Linear)
├── R Output: R×1.0 + G×0.0 + B×0.0 + Offset
├── G Output: R×0.0 + G×1.0 + B×0.0 + Offset
├── B Output: R×0.0 + G×0.0 + B×1.0 + Offset
└── Offsets = Printer Lights (RGB additive)
```

> **@erikwerlin:** *"It's a simple and amateur method but there are far better ways"*
>
> → **Context:** Temp/Tint is "amateur" vs. RGB Mixer in Linear = "pro" (printer lights).

---

## Pro Workflow: Layered WB

```
Node 01: Raw Tab WB (Metadata/As Shot)
    │
    ▼
Node 02: CST (Camera → Linear) + CAT if cross-illuminant
    │
    ▼
Node 03: Parade RGB WB (Lift/Gamma/Gain in Linear, Luma Mix 0)
    ├── Technical neutral base
    │
    ▼
Node 04: Creative WB Offset (Temp/Tint or RGB Gain)
    ├── Warm for golden hour
    ├── Cool for moonlight
    └── Artistic intent
    │
    ▼
Node 05: Output CST → Rec.709
```

---

## Comment Insights

> **@rahj_jordan:** *"This is bad!"* (referring to basic Temp/Tint)
>
> **@balde_photography:** *"These steps are after converting the footage to rec709?"*
>
> → **Answer:** WB in **Linear/Log** space (before Rec.709 CST) for cleanest results.

> **@hamzastudioo:** *Links to another reel* — Cross-reference for alternative method.

---

## Related Skills

- `davinci-resolve-white-balance-luma-mix-zero-rgb-gain` — Luma Mix=0, RGB Gain (Rolling Shutter Media)
- `davinci-resolve-white-balance-3-methods-ivar-brauer` — Temp/Tint, Linear Gain, Gray Card (Ivar Brauer)
- `davinci-resolve-wb-helper-power-window-highlight-mode` — Power Window + Highlight Mode WB (Marco Herbst)
- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer 3-axis surgical WB (Ivar Brauer)
- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier + Scopes for WB measurement

---

## Hashtags

#davinciresolve #videoediting #colorgrading #whitebalance #parade #vectorscope #chromaticadaptation #raw #printerlights