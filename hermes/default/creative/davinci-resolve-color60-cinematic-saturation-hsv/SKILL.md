---
name: davinci-resolve-color60-cinematic-saturation-hsv
description: "COLOR60 Day 07/60: Cinematic saturation using HSV — Gain/Lift/Offset all affect saturation differently. Offset and Lift can be powerful for saturation control, not just Gain. Extra node pairing with HSV for film-like saturation."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, HSV, Saturation, Cinematic, COLOR60]
    source_url: "https://www.instagram.com/reel/DTPUK3kkaE8/"
    source_creator: "@officialjonathankim"
    source_date: "2025-01-18"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [HSV, Saturation, Cinematic, Gain, Lift, Offset, COLOR60, Jonathan Kim]
---

# DaVinci Resolve: COLOR60 Day 07 — Cinematic Saturation with HSV — @officialjonathankim

**Source:** [@officialjonathankim Instagram Reel](https://www.instagram.com/reel/DTPUK3kkaE8/) — "DAY 07/60: COLOR60"

## Technique Overview

**Cinematic saturation using HSV** — Most people only use Gain wheel for HSV saturation, but **Offset and Lift can be just as powerful**. They all affect saturation differently. Part 2 covers an extra node that pairs perfectly with HSV for film-like saturation.

> *"Separating this into two parts so it's easier to digest. Part one breaks down cinematic saturation using HSV. Most people are told to use the gain wheel for HSV saturation, but offset and lift can be just as powerful. They all affect saturation differently, and I explain how here. Part two dives into an extra node that pairs perfectly with HSV and really helps you achieve that cinematic, film-like saturation you see in your favorite movies today."*

> **Series:** COLOR60 — Day 7 of 60

---

## HSV Saturation: Gain vs Lift vs Offset

| Wheel | Effect on Saturation | Best For |
|-------|---------------------|----------|
| **Gain (Highlights)** | Increases saturation in highlights | Bright areas, specular highlights |
| **Lift (Shadows)** | Increases saturation in shadows | Shadow detail, crushed blacks recovery |
| **Offset (Global)** | Uniform saturation shift | Overall saturation balance |

### Why Not Just Gain?
- **Gain only** = highlights saturate, shadows stay flat
- **Lift + Gain** = full tonal range saturation control
- **Offset** = global "vibrance" without crushing

---

## Recommended HSV Workflow

### Part 1: HSV Node (Saturation Shaping)
```
Node 01: CST (Log → DWG)
Node 02: Primary Balance
Node 03: **HSV SATURATION NODE**
  ├── Gain: +10 to +20 (highlight sat)
  ├── Lift: +5 to +15 (shadow sat)
  ├── Offset: +5 to +10 (global sat)
  └── Hue/Sat curves: Fine-tune per hue
Node 04: Creative Look
Node 05: Output CST
```

### Part 2: The "Extra Node" (Pairs with HSV)
**Hint from caption:** *"Extra node that pairs perfectly with HSV and really helps achieve cinematic, film-like saturation"*

**Likely candidates:**
1. **Color Slice** — Per-hue saturation + luma control
2. **Hue vs Sat Curves** — Targeted saturation per hue
3. **Luma vs Sat Curve** — Saturation by luminance (film response)
4. **Contrast + Pivot** — Density-based saturation

---

## Gain/Lift/Offset Saturation Behavior

| Adjustment | Saturation Change | Visual Result |
|------------|-------------------|---------------|
| **Gain ↑** | Highlights saturate more | Brighter colors pop |
| **Lift ↑** | Shadows saturate more | Dark areas gain color |
| **Offset ↑** | All tones saturate evenly | Global "vibrance" |
| **Gain ↓ + Lift ↑** | Shift saturation to shadows | Moody, filmic |
| **Lift ↓ + Gain ↑** | Shift saturation to highlights | Bright, airy |

---

## Comment Insights

| Comment | Insight |
|---------|---------|
| @alexrqz | *"How can you even discover/learn this by yourself? I would never guessed that channel 1/3 are for H/V"* → HSV channels: 1=Hue, 2=Sat, 3=Value |
| @le.witchere | *"Literally everybody does that"* → Common knowledge but often misunderstood |
| @antoine.lavenant | *"Is it what's called vibrance on Adobe products?"* → Similar concept: smart saturation |
| @theaveragewarthunderplayer | *"Or you could also just turn up the density slider"* → Density = saturation + contrast combo |

---

## Pro Tips

1. **Use Qualifier + HSV** — Isolate skin tones, protect from oversaturation
2. **Layer Mixer** — Blend HSV saturation with clean grade
3. **Luma vs Sat Curve** — Film response: midtones most saturated, highlights/shadows roll off
4. **Color Slice** — Per-hue control (skin protect, sky enhance, foliage pop)

---

## Related Techniques

- `davinci-resolve-density-saturation-hue-vs-luminance` — Hue vs Lum for density
- `davinci-resolve-color-warper-saturation-balance` — Color Warper saturation control
- `davinci-resolve-hue-vs-luminance-density-subtractive-saturation` — Subtractive saturation

---

## Tags

`#davinciresolve` `#colorgrading` `#hsv` `#saturation` `#cinematic` `#gain` `#lift` `#offset` `#color60` `#officialjonathankim`