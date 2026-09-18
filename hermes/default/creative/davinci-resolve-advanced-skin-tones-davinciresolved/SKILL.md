---
name: davinci-resolve-advanced-skin-tones-davinciresolved
description: "Advanced skin tones in DaVinci Resolve 20 - Face Refinement, Qualifier isolation, HSL curves, Color Warper, layer mixer protection"
category: creative
tags: [davinci-resolve, skin-tones, face-refinement, qualifier, color-warper, layer-mixer, resolve20, davinciresolved]
source_url: https://www.instagram.com/reel/DLz2kTIRf65/
author: davinciresolved
---

# DaVinci Resolve 20: Advanced Skin Tones

> **"Advanced skin tones in DaVinci Resolve 20"** -- davinciresolved

## Core Techniques for Professional Skin Grading

Resolve 20 enhances skin tone tools with improved **Face Refinement**, **Qualifier precision**, **Color Warper**, and **Layer Mixer** workflows.

---

## Tool Comparison

| Tool | Version | Best For | Precision |
|------|---------|----------|-----------|
| **Face Refinement** | 20+ (Studio) | Auto face detection, smoothing, relight | High (AI) |
| **Qualifier (HSL)** | All | Manual isolation, custom ranges | Very High |
| **Color Warper** | Studio | Creative skin pushing, hue mapping | High |
| **HSL Curves** | All | Targeted hue/sat/lum per range | High |
| **Layer Mixer** | All | Protect skin from creative grade | Essential |

---

## Workflow 1: Face Refinement (Studio, Fast)

```
Node 01: Balance
    |
    v
Node 02: Face Refinement (OFX)
    ├── Face Detection: Auto / Manual
    ├── Smoothing: 0.3-0.7 (subtle)
    ├── Skin Tone: Adjust hue/sat toward 30 deg line
    ├── Eye/Lip Enhance: Subtle (0.1-0.3)
    ├── Relight: Shape face with virtual lights
    └── Blend: 50-70% for natural
```

---

## Workflow 2: Qualifier + Layer Mixer (Pro, Free + Studio)

```
Node 01: Primary Balance (Linear, Luma Mix 0)
    |
    v
Node 02: Creative Grade (Teal/Orange, LUT, etc.)
    |
    v
Node 03: Qualifier (Skin Isolation)
    ├── Mode: HSL
    ├── Hue: 25-40 deg (skin range)
    ├── Sat: 0.1-0.5 (exclude over-sat)
    ├── Lum: 0.2-0.8 (exclude shadows/highlights)
    ├── Clean: Blur 0.5, Erode 1, Clean Black/White
    └── Output: Alpha
    |
    v
Node 04: Layer Mixer
    ├── A: Node 02 (Creative Grade)
    ├── B: Node 01 (Clean Skin / Original)
    └── Mask: Alpha from Node 03 (Composite B over A)
    |
    v
OUTPUT: Creative grade everywhere, protected skin
```

---

## Workflow 3: Color Warper for Skin Mapping (Studio)

```
Color Warper Panel:
├── Grid: 5x5 or 9x9
├── Select skin tone region (~30 deg hue)
├── Lock: Hue (prevent shift)
├── Adjust: Saturation (natural, 10-20)
├── Adjust: Luminance (healthy glow)
└── Smooth: High (natural falloff)
```

---

## Workflow 4: HSL Curves for Skin Precision

```
Hue vs Hue:   Lock 30 deg (skin) = flat line
Hue vs Sat:   Bell curve at 30 deg (control skin sat)
Hue vs Lum:   Gentle lift at 30 deg (healthy glow)
Lum vs Sat:   Film-like: desat highlights, sat midtones
Sat vs Sat:   Compress extreme saturation
```

---

## Skin Tone Reference Values

| Metric | Target | Scope |
|--------|--------|-------|
| **Hue** | ~30 deg (25-40) | Vectorscope skin line |
| **Saturation** | 10-30% (distance from center) | Vectorscope |
| **Luminance** | 40-70 IRE (midtones) | Waveform |
| **RGB Parade** | R > G > B (red dominant) | Parade |

---

## Pro Tips from Comments

> **@kenslyfresh:** *"These little tips turning me into a guru. It's like I'm a good colorist but these are turning me into a great colorist"*
>
> Layer Mixer protection = the secret separator between good/great.

> **@richiezmedia:** *"There is too much info on color grading on social media. I stopped listening to people and just spend a few hours a week exploring the color tab"*
>
> Experimentation > Tutorials. Build your own node trees.

> **@sophiarupprecht:** *"Oh hey that's me"*
>
> Real people, real results.

> **@ksameersingh:** *"That's Blood Line! Its irrespective of the skin colour"*
>
> Skin tone line (~30 deg) works across ethnicities — saturation/luminance vary, hue stays consistent.

---

## Complete Advanced Skin Node Tree

```
INPUT
  |
  v
N01: CST (Camera to Linear) + WB (Gain only, Luma Mix 0)
  |
  v
N02: Primary Balance (Contrast, Pivot, Exposure)
  |
  v
N03: Creative Look (Teal/Orange, LUT, Film Emulation)
  |
  v
N04: FACE REFINEMENT (Studio) --OR-- QUALIFIER (All)
  |     (If Qualifier: HSL 25-40H, 0.1-0.5S, 0.2-0.8L, Clean)
  |
  v
N05: LAYER MIXER (Skin Protection)
  |     A: N03 (Creative)
  |     B: N02 (Clean Skin)
  |     Mask: N04 Alpha
  |
  v
N06: HSL CURVES (Skin Polish)
  |     Hue vs Hue: Lock 30 deg
  |     Hue vs Sat: Control skin sat
  |     Lum vs Sat: Film rolloff
  |
  v
N07: COLOR WARPER (Studio, Optional)
  |     Skin region: Lock hue, subtle sat/lum
  |
  v
N08: Output CST (Linear to Rec.709/P3)
  |
  v
OUTPUT
```

---

## Related Skills

- `davinci-resolve-skin-tones-qualifier-noise` -- Ivar Brauer: Clean skin isolation, noisy Qualifier fix
- `davinci-resolve-soften-skin-free` -- Face Refinement + Circle Mask + Blur (free)
- `davinci-resolve-magicgrade-workflow-blueprint` -- F3 Split Tone includes skin handling
- `davinci-resolve-color-warper-saturation-balance` -- Color Warper for saturation control

---

## Hashtags

#davinciresolve #colorgrading #videoediting #skin-tones #face-refinement #qualifier #color-warper #layer-mixer #resolve20 #davinciresolved