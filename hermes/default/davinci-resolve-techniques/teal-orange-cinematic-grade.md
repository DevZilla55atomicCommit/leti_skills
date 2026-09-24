---
name: teal-orange-cinematic-grade
description: Classic teal & orange cinematic look in DaVinci Resolve — split-toning via Color Wheels (Lift=Teal, Gain=Orange), Curves for density, Power Windows for subject isolation, and optional HSL Curves for hue-specific saturation control.
trigger: User wants the blockbuster "teal & orange" look for cinematic, automotive, travel, or narrative work
category: davinci-resolve-color-grading
tags:
  - color-grading
  - cinematic
  - tealandorange
  - split-toning
  - automotive
  - urban
  - blockbuster
  - lut
parameters:
  - name: lift_teal_amount
    description: Blue/cyan push in shadows
    default: "Blue +0.03 to +0.06, Green -0.01 to -0.02"
    type: string
  - name: gain_orange_amount
    description: Warm/orange push in highlights
    default: "Red +0.03 to +0.06, Green +0.01 to +0.03"
    type: string
  - name: saturation_global
    description: Overall saturation for muted vs pop look
    default: "85-95% (muted) or 100-110% (pop)"
    type: string
  - name: subject_window_boost
    description: Power Window on subject for separation
    default: "Exposure +0.05 to +0.15, Sat +5-15%, Feather 40-60"
    type: string
  - name: vignette_strength
    description: Subtle vignette to center focus
    default: "Circle window, -0.1 to -0.2 Exp, Feather 80+"
    type: string
steps:
  - step: "Node 1 - Primary: Balance exposure, set contrast 1.0-1.1, saturation 90-100%, white balance neutral"
  - step: "Node 2 - Split Tone (Color Wheels): Lift → Teal/Blue; Gamma → Neutral; Gain → Warm/Orange; Offset → slight global warmth"
  - step: "Node 3 - Density/Contrast (Curves): S-curve for contrast, or Luma curve for midtone density; RGB curves for cross-process feel"
  - step: "Node 4 - Subject Isolation (Power Window): Track subject (person/car), local Exposure +0.1, Sat +10%, Contrast +5"
  - step: "Node 5 - HSL Curves (Optional): Hue vs Sat — desaturate greens/yellows; Hue vs Hue — shift cyans to teal, yellows to orange"
  - step: "Node 6 - Vignette (Power Window): Circle center, Exposure -0.15, Feather 85+, Opacity 50-70%"
  - step: "Optional Node 7 - Film Emulation: Cineon Log → Film Print LUT (Kodak 2383, Fuji 3510) at 30-50% opacity"
difficulty: intermediate
resolve_page: Color
node_graph_type: serial
key_nodes:
  - Color Wheels (Split Toning: Lift/Gain)
  - Curves (Density/Contrast)
  - Power Window (Subject Isolation + Vignette)
  - HSL Curves (Hue vs Sat, Hue vs Hue)
  - LUT / Film Emulation (Optional)
source_techniques:
  - video_id: C_lLHxVgEyc
    technique_name: Cinematic Teal and Orange Color Grading
    tags: [color-grading, cinematic, golden-hour, automotive]
  - video_id: DGgVaDWSTMg
    technique_name: Muted Teal & Orange Cinematic Color Grade
    tags: [color-grading, cinematic, tealandorange, urban]
  - video_id: C9pc6r6u9pJ
    technique_name: Instagram Reel C9pc6r6u9pJ - DaVinci Resolve Technique (LUT Mapping)
    tags: [Instagram Reel, DaVinci Resolve, Color Grading, LUT Mapping]
  - video_id: DKz0aPLuo31
    technique_name: Instagram Reel DKz0aPLuo31 - DaVinci Resolve Technique (Color Correction + LUT)
    tags: [Color Correction, LUT, DaVinci Resolve, Instagram Reel]
  - video_id: DNNWY5RzE3R
    technique_name: Instagram Reel DNNWY5RzE3R - DaVinci Resolve Technique (Color Correction + LUT)
    tags: [Color Correction, LUT Application, Instagram Reel Editing]
---

# Teal & Orange Cinematic Grade

The iconic blockbuster look — cool teal shadows, warm orange highlights, subject separation, and cinematic density. Works on automotive, urban, travel, narrative, and commercial work.

## When to Use
- Cinematic narrative / short films
- Automotive / car commercials
- Urban / cityscape / architecture
- Travel / lifestyle content
- Music videos
- Any "blockbuster" aesthetic request

## The Theory
**Teal (shadows) + Orange (highlights) = Maximum color contrast** on the color wheel (complementary). Skin tones live in orange → pop against teal backgrounds. The most "cinematic" color relationship.

---

## Node Graph (Serial)

```
Node 1: Primary Balance (Exposure, WB, Contrast, Sat)
    ↓
Node 2: Split Tone — Color Wheels (Lift=Teal, Gain=Orange)
    ↓
Node 3: Density & Contrast — Curves (S-curve / Luma / RGB)
    ↓
Node 4: Subject Isolation — Power Window (Tracked)
    ↓
Node 5: Hue/Sat Control — HSL Curves (Optional)
    ↓
Node 6: Vignette — Power Window (Circle)
    ↓
Node 7: Film Emulation LUT — 30-50% (Optional)
```

---

## Node-by-Node Breakdown

### Node 1: Primary Balance — Foundation
**Goal**: Clean, neutral base. No look yet — just correct.

| Parameter | Setting | Why |
|-----------|---------|-----|
| **Exposure** | ±0.0 (balanced) | Protect highlights/shadows |
| **Contrast** | 1.00 - 1.10 | Slight pop |
| **Pivot** | 0.50 | Center contrast on mid-gray |
| **Saturation** | 90-100% | Slight desat for filmic base |
| **Temp / Tint** | Neutral (skin on line) | White balance correct |

> **Scope**: Parade RGB balanced, Vectorscope skin on line, Waveform 15-95 IRE

---

### Node 2: Split Tone — Color Wheels (The Heart)
**Goal**: Push shadows teal, highlights orange.

| Wheel | Adjustment | Typical Values |
|-------|------------|----------------|
| **Lift (Shadows)** | Teal/Cyan push | Blue: **+0.04 to +0.07**<br>Green: **-0.01 to -0.02**<br>Red: **-0.01 to -0.02** |
| **Gamma (Midtones)** | Neutral / Subtle | Red: +0.01, Green: 0, Blue: -0.01 |
| **Gain (Highlights)** | Warm/Orange push | Red: **+0.04 to +0.07**<br>Green: **+0.01 to +0.03**<br>Blue: **-0.01 to -0.02** |
| **Offset (Global)** | Overall warmth | Temp: **+50 to +150**, Tint: **+5 to +10** |

**Visual Check**: Vectorscope — teal cluster (shadows), orange cluster (highlights), skin on line.

> **Pro Tip**: Start with **Offset warmth** (+100 Temp), then push Lift/Gain. Less Gain push = more natural.

---

### Node 3: Density & Contrast — Curves
**Goal**: Cinematic density (rich midtones), not just contrast.

**Option A: Luma Curve (Density)**
```
Input:  0.0 ───┐
         0.25 ──┤
         0.50 ──┼──▲  (lift midtones +0.03 to +0.05)
         0.75 ──┤
         1.0 ───┘
```
- Creates "thick" filmic midtones
- Shadows stay lifted, highlights roll off

**Option B: S-Curve (Contrast)**
- Anchor 0.0 and 1.0
- Pull 0.25 down slightly, push 0.75 up slightly
- Contrast +10 to +20 equivalent

**Option C: RGB Cross-Process (Stylized)**
| Channel | Curve |
|---------|-------|
| **Red** | Slight S |
| **Green** | Inverse S (lift shadows, drop highlights) |
| **Blue** | Lift shadows, drop highlights |

> **From C_lLHxVgEyc**: "High contrast, desaturated midtones" — use Luma curve for density, desaturate mids in Node 5.

---

### Node 4: Subject Isolation — Power Window
**Goal**: Pop the hero (car, person, product) from background.

**Window Setup**:
- **Shape**: Custom (trace subject) OR Circle (person) OR Linear (car side)
- **Tracker**: **Enable** → Track forward/backward
- **Feather**: 40-60 (soft edge)
- **Invert**: OFF (affecting subject)

**Adjustments (on Subject)**:
| Parameter | Value | Effect |
|-----------|-------|--------|
| **Exposure** | +0.05 to +0.15 | Brighter = closer |
| **Saturation** | +5% to +15% | More color = hero |
| **Contrast** | +5 to +10 | More definition |
| **Midtone Detail** | +5 to +10 | Texture pop |

**From C_lLHxVgEyc**: "Power Window on car → slightly increase exposure and saturation"

---

### Node 5: HSL Curves — Hue-Specific Control (Optional)
**Goal**: Surgical color cleanup — kill ugly greens, push teal/orange purity.

| Curve | Adjustment |
|-------|------------|
| **Hue vs Sat** | **Green (120°)**: -15% to -30% (kill spill)<br>**Yellow (60°)**: -10% to -20% (mute)<br>**Cyan (180°)**: +5% (enhance teal)<br>**Orange (30°)**: +5% (enhance warm) |
| **Hue vs Hue** | **Cyan → Teal**: 180° → 190° (+10°)<br>**Yellow → Orange**: 60° → 40° (-20°)<br>**Magenta → Red**: 300° → 350° |
| **Sat vs Sat** | Compress low sat (noise), expand mid sat (skin) |

**From DGgVaDWSTMg**: "Hue/Sat curve to target and desaturate greens and yellows" — classic teal/orange cleanup.

---

### Node 6: Vignette — Power Window
**Goal**: Subtle center focus, cinematic frame.

**Window**: Circle, Centered
- **Feather**: 85-95 (max softness)
- **Roundness**: 1.0 (perfect circle)
- **Exposure**: -0.10 to -0.20
- **Opacity** (Key Output): 50-70% (dial back)

> **Alternative**: Use **Midtone Detail** -5 in vignette area to soften edges.

---

### Node 7: Film Emulation LUT (Optional)
**Goal**: Organic film response curve + halation/grain feel.

| LUT | Opacity | Notes |
|-----|---------|-------|
| **Kodak 2383** (Print Film) | 30-50% | Classic cinema print look |
| **Fuji 3510** | 30-40% | Cooler, greener shadows |
| **ARRI LogC → Rec709** | 50-70% | Clean Alexa emulation |
| **Custom DCTL** | 100% | If using DCTL film emulation |

**Placement**: After all color — LUT sees graded image.

**From C9pc6r6u9pJ / DKz0aPLuo31 / DNNWY5RzE3R**: Multiple techniques use "Color Correction + LUT Mapping" workflow.

---

## Variations

### **Muted Teal & Orange** (DGgVaDWSTMg style)
- Saturation: 85-90% (Node 1)
- Lift Teal: +0.03 Blue, -0.01 Green
- Gain Orange: +0.03 Red, +0.02 Green
- Hue vs Sat: Greens -25%, Yellows -20%
- **Result**: Moody, urban, desaturated — "Blade Runner 2049" vibe

### **Pop Teal & Orange** (Commercial/Automotive)
- Saturation: 105-110% (Node 1)
- Lift Teal: +0.06 Blue
- Gain Orange: +0.06 Red, +0.03 Green
- Subject Window: +0.15 Exp, +15% Sat
- **Result**: High-energy, car commercial, travel vlog

### **Golden Hour Teal & Orange** (C_lLHxVgEyc)
- Node 1 Temp: +200 to +300 (warm base)
- Lift: Teal (balance warm shadows)
- Gain: Heavy Orange (match sun)
- Vignette: Stronger (-0.25)
- **Result**: Sunset/sunrise cinematic

---

## Scope Targets

| Scope | Target |
|-------|--------|
| **Vectorscope** | Two distinct clusters: Teal (shadows, ~180°), Orange (highlights/skin, ~30°) |
| **Parade RGB** | Blue lifted in shadows, Red lifted in highlights |
| **Waveform** | Blacks ~15 IRE (lifted), Whites ~90 IRE (soft roll-off) |
| **Histogram** | No hard clipping, smooth distribution |

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Skin turns green | Lift teal too strong | Reduce Lift Blue, add Qualifier for skin protection |
| Orange blowout | Gain too hot | Pull Gain Red/Green, check Waveform highlights |
| Muddy midtones | No density curve | Add Node 3 Luma curve midtone lift |
| Subject lost in BG | No isolation | Power Window (Node 4) — track it! |
| Looks like Instagram filter | Over-saturated, no density | Desat Node 1 to 90%, add Curve density |
| Vignette obvious | Feather too low | Feather 85+, Opacity 50% |

---

## Source Techniques Summary

| Technique | Key Insight |
|-----------|-------------|
| **C_lLHxVgEyc** | Power Window on subject + Vignette = classic teal/orange |
| **DGgVaDWSTMg** | Muted sat (35%), Hue vs Sat to kill greens/yellows |
| **C9pc6r6u9pJ** | Color Correction → LUT Mapping workflow |
| **DKz0aPLuo31** | Color Balance → LUT for specific look |
| **DNNWY5RzE3R** | Color Correction Node → Grading Node → LUT |

---

## Related Skills
- `skin-tone-portrait-grade` — protect skin in teal/orange
- `golden-hour-atmospheric-grade` — teal/orange for landscapes
- `gimbal-automotive-cinematic-grade` — car teal/orange
- `hdr-social-media-grade` — HDR teal/orange
- `social-media-sharpening-export` — delivery
- `beginner-color-correction-basics` — Node 1 foundation