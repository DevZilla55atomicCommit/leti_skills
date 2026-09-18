---
name: skin-tone-portrait-grade
description: Subtle skin tone enhancement, background separation, and natural portrait grading in DaVinci Resolve — serial node workflow with Color Wheels, Curves, Qualifier, and Power Window for professional skin tones without orange/plastic look.
trigger: User grading portraits, interviews, talking heads, fashion, beauty, wedding, or any footage with prominent skin tones
category: davinci-resolve-color-grading
tags:
  - color grading
  - skin tones
  - background separation
  - subtle adjustments
  - portrait
  - interview
  - beauty
  - wedding
parameters:
  - name: exposure_balance
    description: Balanced exposure via Lift/Gamma/Gain
    default: "Lift 1.0, Gamma 1.0, Gain 1.0 (adjust ±0.05-0.1)"
    type: string
  - name: midtone_curve
    description: Gentle midtone lift for skin glow
    default: "Gamma 0.95-1.05 (slight lift)"
    type: string
  - name: skin_qualifier_hue
    description: Skin tone hue selection range
    default: "25°-45° (wider for diverse skin tones)"
    type: string
  - name: skin_qualifier_sat
    description: Skin tone saturation selection
    default: "0.2-0.6 (exclude over-sat/under-sat)"
    type: string
  - name: skin_qualifier_lum
    description: Skin tone luminance selection
    default: "0.3-0.7 (mid-tones primarily)"
    type: string
  - name: vignette_strength
    description: Subtle background darkening
    default: "Circle/Power Window, -0.1 to -0.2 exposure, high feather"
    type: string
steps:
  - step: "Node 1 - Primary Balance: Color Wheels to balance exposure/contrast globally. Small Lift/Gamma/Gain adjustments (±0.05-0.1). Keep natural."
  - step: "Node 2 - Midtone Curve: Curves tool, gentle S-curve or midtone lift (Gamma 0.95-1.05) for skin luminosity without crushing shadows."
  - step: "Node 3 - Skin Qualifier: Qualifier (HSL) → Hue 25-45°, Sat 0.2-0.6, Lum 0.3-0.7. Refine with Clean Black/White, Blur radius 2-3."
  - step: "Node 3 Adjustments: On qualified skin: slight Sat -5% (de-sat), Hue ±2° (correct cast), Lum +2% (glow). NO heavy smoothing."
  - step: "Node 4 - Background Separation: Power Window (Circle/Custom) on background → Exposure -0.1 to -0.2, Sat -5%, Feather 60-80."
  - step: "Node 5 (Optional) - Eye/Lip Pop: Small Power Window on eyes/lips → slight Contrast +5, Sat +5, Sharpness +5."
  - step: "Node 6 (Optional) - Global Vignette: Circle window center, -0.15 exposure, Feather 80+, Roundness high."
difficulty: intermediate
resolve_page: Color
node_graph_type: serial
key_nodes:
  - Color Wheels (Primary Balance)
  - Curves (Midtone Lift)
  - Qualifier / HSL (Skin Isolation)
  - Power Window (Background / Eyes / Vignette)
source_techniques:
  - video_id: C18_hSSPmOY
    technique_name: Subtle Skin Tone Enhancement and Background Separation
    tags: [color grading, skin tones, background separation, subtle adjustments]
---

# Skin Tone & Portrait Grade

Professional, natural skin tone grading for portraits, interviews, talking heads, fashion, beauty, and wedding work. **Goal: enhance, not mask** — avoid the "orange plastic" look.

## When to Use
- Interview / talking head footage
- Portrait / fashion / beauty photography
- Wedding / event videography
- Corporate / documentary subjects
- Any footage where skin is the hero

## The Golden Rule
> **Subtlety > Strength**. Skin should look like *better skin*, not *graded skin*. If you can see the grade, it's too much.

## Node Graph (Serial)

```
Node 1: Primary Balance (Color Wheels)
    ↓
Node 2: Midtone Curve (Curves)
    ↓
Node 3: Skin Isolation (Qualifier/HSL)
    ↓
Node 4: Background Separation (Power Window)
    ↓
Node 5: Eye/Lip Accent (Power Window) — Optional
    ↓
Node 6: Global Vignette (Power Window) — Optional
```

---

## Node-by-Node Breakdown

### Node 1: Primary Balance — Color Wheels
**Purpose**: Global exposure, contrast, white balance foundation.

| Wheel | Adjustment | Typical Range |
|-------|------------|---------------|
| **Lift** | Shadow balance | ±0.03-0.05 per channel |
| **Gamma** | Midtone contrast | ±0.02-0.05 per channel |
| **Gain** | Highlight balance | ±0.03-0.05 per channel |
| **Offset** | Global WB tweak | Temp ±50-100, Tint ±5-10 |

**Tips**:
- Start with **White Balance** (Temp/Tint) before wheels
- Use **Parade RGB** scope — align R/G/B in skin tones (cheek highlight)
- Keep Contrast/Pivot at default (1.0 / 0.5) — adjust in Node 2
- **Skin tone line** on Vectorscope = your north star

---

### Node 2: Midtone Lift — Curves
**Purpose**: Gentle skin luminosity boost without crushing shadows.

**Curve Shape**:
```
Input:  0.0 ───┐
         0.25 ──┤
         0.50 ──┼──▲  (lift midpoint +0.02 to +0.05)
         0.75 ──┤
         1.0 ───┘
```

**Settings**:
- **Master Curve**: Slight S (Contrast +5 to +10) OR
- **RGB Curves**: Lift Green midtone slightly (+0.02) for health
- **Luma Curve**: Midpoint (0.5) → 0.52-0.55 (subtle glow)

**Scope Check**: Waveform — skin highlights 65-75 IRE, shadows 20-30 IRE

---

### Node 3: Skin Isolation — Qualifier (HSL)
**Purpose**: Targeted skin refinement — desaturate orange push, fix color cast, add glow.

**Qualifier Settings**:
| Parameter | Range | Notes |
|-----------|-------|-------|
| **Hue** | 25° - 45° | Wider for diverse skin tones (20°-50°) |
| **Saturation** | 0.20 - 0.60 | Excludes over-sat (makeup) & under-sat (shadows) |
| **Luminance** | 0.30 - 0.70 | Mid-tones; exclude deep shadows & specular highlights |

**Refinement**:
- **Clean Black**: 0.02-0.05 (remove noise in shadows)
- **Clean White**: 0.95-0.98 (remove specular highlights)
- **Blur Radius**: 2-3 (soften selection edge)
- **Invert**: OFF (selecting skin, not background)

**Adjustments on Qualified Skin**:
| Parameter | Adjustment | Why |
|-----------|------------|-----|
| **Saturation** | -3% to -8% | Removes "orange tan" look |
| **Hue** | ±2° (toward neutral) | Fixes magenta/green color cast |
| **Luminance** | +1% to +3% | Subtle "healthy glow" |
| **Contrast** | 0 to +5 | Only if skin looks flat |

> ⚠️ **NO Blur/Smooth in Qualifier node** — that's plastic territory. Use Face Refinement (Studio) on separate node if needed.

---

### Node 4: Background Separation — Power Window
**Purpose**: Subtle subject/background depth — "pop" without vignette obviousness.

**Window Setup**:
- **Shape**: Circle (centered on subject) OR Custom (trace subject)
- **Operation**: **Invert** (affecting background)
- **Feather**: 60-80 (very soft)
- **Roundness**: High (organic)

**Adjustments (on Background)**:
| Parameter | Value | Effect |
|-----------|-------|--------|
| **Exposure** | -0.10 to -0.20 | Darkens BG, lifts subject |
| **Saturation** | -5% to -10% | Desaturates BG, saturates subject relatively |
| **Contrast** | -5 to 0 | Softens BG detail |
| **Blur** | 0-5 (optional) | Subtle depth-of-field feel |

**Tracking**: Enable **Tracker** on window → Track subject movement

---

### Node 5: Eye / Lip Accent — Optional
**Purpose**: Draw attention to eyes/mouth — the "connection points."

**Windows**: Small circles on each eye, one on lips
- **Feather**: 10-15
- **Adjustments**:
  - Exposure: +0.05 to +0.10 (eyes only)
  - Contrast: +5 to +10
  - Saturation: +5 (lips) / 0 (eyes)
  - Sharpen: +5 to +10 (eyes)

**Track** each window independently.

---

### Node 6: Global Vignette — Optional
**Purpose**: Classic portrait framing.

**Window**: Circle, center frame
- **Feather**: 80-90 (max softness)
- **Roundness**: 1.0 (perfect circle)
- **Exposure**: -0.10 to -0.20
- **Opacity**: 50-70% (dial back in Key Output)

---

## Scope Targets for Skin

| Scope | Target |
|-------|--------|
| **Vectorscope** | Skin tones on **Skin Tone Line** (10:30 / 160°) |
| **Parade RGB** | R ≈ G ≈ B in cheek highlight (within 5-10 IRE) |
| **Waveform** | Skin highlight 65-75 IRE, shadow 20-30 IRE |
| **Histogram** | No clipping 0 or 1023; smooth roll-off |

---

## Diverse Skin Tones — Qualifier Adjustments

| Skin Tone | Hue Range | Sat Range | Lum Range | Notes |
|-----------|-----------|-----------|-----------|-------|
| **Light / Pale** | 25°-40° | 0.15-0.50 | 0.40-0.80 | Narrower sat, higher lum |
| **Medium / Olive** | 30°-45° | 0.20-0.60 | 0.30-0.70 | Standard |
| **Deep / Rich** | 20°-40° | 0.25-0.65 | 0.20-0.60 | Wider hue, lower lum |
| **Mixed Scene** | 20°-50° | 0.15-0.65 | 0.25-0.75 | Union of all; refine per shot |

> **Pro Tip**: Use **multiple Qualifier nodes** in parallel (Layer Mixer) for diverse casts — one per skin tone group.

---

## Face Refinement (Studio Only) — Alternative to Node 3 Smoothing

If skin *needs* smoothing (acne, heavy texture):
1. Add **Face Refinement OFX** on Node 3 (after Qualifier)
2. **Skin Smoothing**: 0.15-0.30 (subtle!)
3. **Eye/Lip Enhance**: 0.10-0.20
4. **Contour**: 0.05-0.10 (subtle shape)
5. **Track** face through clip

> Still prefer Qualifier + mild contrast over Face Refinement for natural look.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Orange skin (over-sat) | Node 3: Sat -5% to -10% on Qualifier |
| Green/magenta cast | Node 3: Hue ±2-3° toward skin tone line |
| Plastic/smooth skin | Remove blur/smooth; use Qualifier Lum +2% instead |
| Background competes | Node 4: Exp -0.15, Sat -10%, Feather 80 |
| Vignette obvious | Feather 80-90, Opacity 50%, or skip |
| Eyes dead | Node 5: Eye windows +0.1 Exp, +10 Contrast |

---

## Source Technique
Based on: **C18_hSSPmOY** — "Subtle Skin Tone Enhancement and Background Separation"
- 4-node serial: Color Wheels → Curves → Qualifier (skin) → Power Window (bg vignette)
- Tags: `color grading`, `skin tones`, `background separation`, `subtle adjustments`

---

## Related Skills
- `golden-hour-atmospheric-grade` — for outdoor portraits
- `teal-orange-cinematic-grade` — for stylized portrait looks
- `social-media-sharpening-export` — delivery for IG/TikTok
- `hdr-social-media-grade` — HDR portrait workflow
- `beginner-color-correction-basics` — foundation skills