---
name: davinci-resolve-split-toning-danny-gan
description: Split toning without qualifiers or secondary tools — using curves and primaries for highlight/shadow color separation
category: creative
tags: [davinci-resolve, split-toning, curves, color-grading, danny-gan, visionary-colour, no-qualifiers]
source_url: https://www.instagram.com/reel/DLHpDHjJG1i/
author: dannygan_colorist
---

# DaVinci Resolve: Split Toning Without Qualifiers — Danny Gan

> **"I've been searching for a way to do split toning without any qualifiers or secondary tools... This is one of the breakthroughs I've experimented with the last few months and I'm revealing it to you."** — Danny Gan (@dannygan_colorist, @visionarycolouracademy)

## Core Concept: Split Toning via Curves + Primaries Only

Traditional split toning uses:
- **Qualifiers** to isolate highlights/shadows
- **Layer/Parallel Mixers** for blending
- **Secondary tools** (Color Warper, HSL)

**Danny's Method:** Pure **Curves + Primary Wheels** — no qualifiers, no secondaries.

---

## The Technique

### Understanding Split Toning
| Region | Traditional Approach | Danny's Approach |
|--------|---------------------|------------------|
| **Highlights** | Qualifier (Luma high) + Color Wheel | **Gain Wheel** (affects highlights most) |
| **Shadows** | Qualifier (Luma low) + Color Wheel | **Lift Wheel** (affects shadows most) |
| **Midtones** | Qualifier (Luma mid) + Color Wheel | **Gamma Wheel** (affects midtones most) |

### Step-by-Step

#### 1. Base Balance (Node 01)
```
Node 01: Primary Balance
    ├── CST to Linear (if log footage)
    ├── Luma Mix = 0
    ├── Gain Pivot = 0.335
    └── WB via Gain (RGB) on Vectorscope
```

#### 2. Split Tone via Color Wheels (Node 02)
```
Node 02: Split Tone (Serial after Node 01)
    ├── LIFT (Shadows) → Push toward COOL (teal/blue)
    │   ├── Hue: ~180–200°
    │   ├── Sat: 15–30 (subtle)
    │   └── Lum: Slight lift if needed
    │
    ├── GAMMA (Midtones) → NEUTRAL or slight WARM
    │   ├── Hue: ~30–50° (skin-friendly)
    │   ├── Sat: 5–15
    │   └── Lum: Preserve contrast
    │
    └── GAIN (Highlights) → Push toward WARM (gold/orange)
        ├── Hue: ~30–60°
        ├── Sat: 10–25
        └── Lum: Protect highlights (don't clip)
```

#### 3. Refine with Curves (Node 03)
```
Node 03: Custom Curves (Serial)
    ├── RGB Parade: Verify separation
    │   ├── Red channel: Highlights up, Shadows down (warm highlights, cool shadows)
    │   ├── Blue channel: Shadows up, Highlights down (cool shadows, warm highlights)
    │   └── Green channel: Minimal adjustment (skin protector)
    │
    ├── Hue vs Hue: Lock skin tones (~30°)
    ├── Hue vs Sat: Desaturate extreme highlights/shadows if needed
    └── Lum vs Sat: Film-like roll-off (highlights desaturate)
```

---

## Why This Works (Color Science)

### Primary Wheels = Natural Luma-Based Separation

| Wheel | Luminance Range Affected | Split Tone Role |
|-------|-------------------------|-----------------|
| **Lift** | Shadows (0–30% IRE) | Cool tint → Cyan/Teal/Blue |
| **Gamma** | Midtones (30–70% IRE) | Neutral / Skin-protect |
| **Gain** | Highlights (70–100% IRE) | Warm tint → Gold/Orange/Amber |

**No qualifier needed** because the wheels **inherently operate on different luminance bands**.

### Curves Provide Precision

- **RGB Parade** shows exact channel separation
- **Red up / Blue down in highlights** = Warm
- **Blue up / Red down in shadows** = Cool
- **Green stable** = Skin protection

---

## Pro Tips from Comments

> **@thoriqkurobing:** *"Basic but not everyone notices this 🔥"*
>
> → The power is in **simplicity** — wheels + curves = full split tone control.

> **@3wm_atelier:** *"I don't understand. You popped Blue, then popped sat and bring back sat down."*
>
> → **Translation:** He pushed Blue in shadows (cool), then adjusted saturation curves to control intensity — push/pull to taste.

> **@bfproductions_:** *"Literally was just looking for this answer for a music video I'm grading 😂 appreciate it! 💪🏾"*
>
> → Practical, production-ready technique.

---

## Complete Node Tree

```
INPUT (Log/Raw)
    │
    ▼
Node 01: CST → Linear + Luma Mix 0 + WB (Gain only)
    │
    ▼
Node 02: SPLIT TONE (Color Wheels)
    ├── Lift: Cool (Teal/Blue) @ 15-30 sat
    ├── Gamma: Neutral/Warm @ 5-15 sat
    └── Gain: Warm (Gold/Orange) @ 10-25 sat
    │
    ▼
Node 03: CURVES REFINEMENT
    ├── Red Channel: Highlights ↑, Shadows ↓
    ├── Blue Channel: Shadows ↑, Highlights ↓
    ├── Green Channel: Minimal (skin)
    ├── Hue vs Hue: Lock 30° (skin)
    ├── Hue vs Sat: Tame extremes
    └── Lum vs Sat: Highlight roll-off
    │
    ▼
Node 04: Creative Look / LUT (Optional)
    │
    ▼
Node 05: Output CST → Rec.709/Gamma 2.4
    │
    ▼
OUTPUT
```

---

## Variations

| Look | Lift (Shadows) | Gamma (Mid) | Gain (Highs) |
|------|----------------|-------------|--------------|
| **Teal & Orange** | Teal (180°) | Neutral | Orange (30°) |
| **Cool Moody** | Blue (220°) | Cool (200°) | Neutral |
| **Warm Nostalgic** | Warm (40°) | Warm (50°) | Gold (50°) |
| **Cinematic Bleach** | Cyan (190°) | Desat | Yellow (60°) |
| **Noir** | Blue (230°) | Neutral | Warm (30°) |

---

## Related Skills

- `davinci-resolve-split-tone-studio-free` — Built-in Split Tone feature (Ivar Brauer)
- `davinci-resolve-complementary-color-grading` — Teal & Orange via Gain/Lift + Curves
- `davinci-resolve-magicgrade-workflow-blueprint` — 4-step workflow includes split tone

---

## Hashtags

#malaysiancolorist #colorgrading #davinciresolve #postproduction #colorgrade #splittone #filmlook #cinematic #visionarycolour #dannygan