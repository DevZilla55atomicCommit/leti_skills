---
name: davinci-resolve-split-tone-studio-free
description: "Split Tone feature in DaVinci Resolve — works in both Studio and Free versions. Color Wheels → Split Tone for independent highlight/shadow tinting without curves."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Split Tone, Color Wheels, Free Version, Studio Version]
    source_url: "https://www.instagram.com/reel/DXpZfbzx_yZ/"
    source_creator: "@ivarbrauer"
    source_date: "2025-05-18"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner"
    tags: [Split Tone, Color Wheels, Free Version, Studio Version, DaVinci Resolve, Ivar Brauer]
---

# DaVinci Resolve: Split Tone — Works in Free & Studio

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DXpZfbzx_yZ/) — "Split Tone in Studio and Free Version"

## Technique Overview

**Hidden Gem:** DaVinci Resolve has a **built-in Split Tone** feature in Color Wheels — works in **both Free and Studio** versions. No curves, no qualifiers needed.

> "So much better than wheeling!" — @eclipsewindowfilmllc
> "There's a fucking split tone built into DaVinci??? I've been doing it with curves for YEARS" — @bloomfieldproductions

---

## Where to Find It

**Color Page → Color Wheels Panel → Split Tone button** (icon: two overlapping circles)

Or: **Right-click Color Wheels → Split Tone**

---

## Split Tone Controls

| Control | Function | Typical Range |
|---------|----------|---------------|
| **Highlights Hue** | Tint for bright areas | 30°-50° (warm) / 200°-220° (cool) |
| **Highlights Sat** | Intensity of highlight tint | 10-30 |
| **Shadows Hue** | Tint for dark areas | 200°-220° (cool) / 30°-50° (warm) |
| **Shadows Sat** | Intensity of shadow tint | 10-30 |
| **Balance** | Shift between H/S influence | 0.4-0.6 |

---

## Classic Split Tone Presets

| Look | Highlights (Hue/Sat) | Shadows (Hue/Sat) | Balance |
|------|---------------------|-------------------|---------|
| **Teal & Orange** | 35° / 25 | 205° / 20 | 0.50 |
| **Warm/Cool** | 40° / 30 | 210° / 25 | 0.55 |
| **Cinematic Cool** | 20° / 15 | 215° / 30 | 0.45 |
| **Golden Hour** | 45° / 35 | 25° / 15 | 0.60 |
| **Moonlight** | 210° / 20 | 230° / 25 | 0.40 |

---

## Step-by-Step

### 1. Enable Split Tone
- Color Wheels panel → Click **Split Tone** button
- Two new rings appear: **Highlights** (top) and **Shadows** (bottom)

### 2. Set Highlights (Warm)
- **Hue:** 30°-45° (orange/gold)
- **Saturation:** 15-30
- Adjust while watching Vectorscope

### 3. Set Shadows (Cool)
- **Hue:** 200°-220° (teal/blue)
- **Saturation:** 10-25

### 4. Fine-Tune Balance
- **Balance slider:** Shifts influence between H/S
- **0.50** = even split; **>0.5** = highlights dominate

### 5. Verify on Scopes
| Scope | Check |
|-------|-------|
| **Vectorscope** | Trace splits along highlight/shadow separation |
| **Parade RGB** | R/G/B separation in highlights vs shadows |
| **Waveform** | No clipping introduced |

---

## Pro Tips from Comments

**@jiri.fineart:** *"If you set project settings to DWG why change it in nodes? Can't you leave it on 'use timeline' settings?"*
→ **Answer:** Node-level override gives per-clip control; timeline setting is global default.

**@bloomfieldproductions:** *"I've been doing it with curves for YEARS"*
→ Split Tone is faster, non-destructive, and animatable.

**@eclipsewindowfilmllc:** *"So much better than wheeling!"*
→ No qualifier needed; instant global split.

---

## When to Use Split Tone vs Curves

| Scenario | Tool |
|----------|------|
| **Global film look** | Split Tone (fast, clean) |
| **Per-object tinting** | Curves + Qualifier |
| **Animating look change** | Split Tone (keyframeable) |
| **Complex hue shifts** | Custom Curves |
| **Skin-safe split** | Curves + Skin Qualifier |

---

## Related Techniques

- `davinci-resolve-complementary-color-grading` — Teal/Orange via Gain/Lift
- `davinci-resolve-hue-vs-luminance-density-saturation` — Density for color separation
- `davinci-resolve-soft-light-glow-cinematic-emotion` — Glow for atmosphere

---

## Tags

`#davinciresolve` `#split-tone` `#color-wheels` `#free-version` `#studio-version` `#ivarbrauer` `#colorgrading` `#cinematic-look`