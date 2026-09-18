---
name: davinci-resolve-tone-curve-basics
description: "Learn the basics of the Tone Curve — quick guide on tone curve fundamentals for photography and color grading. Tone curve vs masks differences."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Tone Curve, Photography, Basics]
    source_url: "https://www.instagram.com/p/DS3CZ6CCJqr/"
    source_creator: "@huggyyx"
    source_date: "2025-01-15"
    vault_category: "Educational Resources"
    skill_level: "Beginner"
    tags: [Tone Curve, Basics, Photography, Color Grading, Tutorial, Huggyyx]
---

# DaVinci Resolve: Tone Curve Basics — @huggyyx

**Source:** [@huggyyx Instagram Post](https://www.instagram.com/p/DS3CZ6CCJqr/) — "Learn the basics of the Tone Curve"

## Technique Overview

Educational post explaining **Tone Curve basics** — quick and easy guide for photography and color grading. Covers what tone curves do vs masks.

> *"Learn the basics of the Tone Curve. Just a quick and easy guide on the basics of the Tone Curve. Hope this helps! Save this for later & Share with a friend!"*

---

## Tone Curve Fundamentals

### What It Controls
| Axis | Controls |
|------|----------|
| **X-axis (Input)** | Original pixel values (shadows → highlights) |
| **Y-axis (Output)** | New pixel values after adjustment |
| **Diagonal line** | No change (input = output) |

### Basic Curve Shapes

| Shape | Effect | Use Case |
|-------|--------|----------|
| **S-Curve** | Contrast ↑ (shadows down, highlights up) | Standard contrast boost |
| **Inverted S** | Contrast ↓ (shadows up, highlights down) | Flatten, HDR recovery |
| **Lift shadows** | Raise left side | Shadow detail recovery |
| **Crush shadows** | Lower left side | Moody, cinematic blacks |
| **Roll off highlights** | Flatten right side | Highlight protection |

---

## Tone Curve vs Masks (Common Question)

**Comment:** *"What's the difference between the tone curve and adding masks, don't they all practically do the same thing?"*

| Tone Curve | Masks / Local Adjustments |
|------------|---------------------------|
| **Global** — affects entire image by tonal range | **Local** — affects specific areas |
| **Tonal selection** — by brightness | **Spatial selection** — by position |
| **Smooth transitions** — no hard edges | **Can have hard edges** (needs feathering) |
| **Single tool** | **Multiple tools** (brush, gradient, radial) |
| **Faster for overall look** | **Precise for specific areas** |

**Answer:** They complement each other. Tone curve = global tonal shaping. Masks = local creative control.

---

## When to Use Tone Curve

| Scenario | Approach |
|----------|----------|
| **Overall contrast** | S-curve on RGB or Luma |
| **Shadow detail** | Lift lower-left anchor |
| **Highlight rolloff** | Flatten upper-right |
| **Color contrast** | Separate R/G/B curves |
| **Film emulation** | Custom curve per channel |
| **Match shots** | Curve matching via scopes |

---

## Pro Tips

1. **Start with Luma curve** — affects contrast without color shift
2. **Use RGB curves for color grading** — split toning, cross process
3. **Anchor points** — set at 25%, 50%, 75% for control
4. **Scopes always** — Waveform for luma, Parade for RGB
5. **Subtle = pro** — extreme curves look "digital"

---

## Related Techniques

- `davinci-resolve-primary-color-correction-linear-printer-lights` — Printer lights vs curves
- `davinci-resolve-cinematic-grading-3-mistakes` — Gain+Pivot vs Curves for exposure
- `davinci-resolve-color60-cinematic-saturation-hsv` — HSV saturation with curves

---

## Tags

`#davinciresolve` `#colorgrading` `#tone-curve` `#photography` `#basics` `#tutorial` `#huggyyx`