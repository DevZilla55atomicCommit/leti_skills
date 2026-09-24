---
name: davinci-resolve-wedding-film-look
description: "Wedding film look in DaVinci Resolve — cinematic wedding grade using LUTs, curves, and color wheels for romantic, timeless aesthetic."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Wedding, Film Look, LUT, Cinematic]
    source_url: "https://www.instagram.com/reel/DV7NPGKkcGq/"
    source_creator: "@gabelomoteycreative"
    source_date: "2025-03-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner to Intermediate"
    tags: [Wedding, Film Look, LUT, Cinematic, Wedding Film, Color Grading, Gabelomotey]
---

# DaVinci Resolve: Wedding Film Look — @gabelomoteycreative

**Source:** [@gabelomoteycreative Instagram Reel](https://www.instagram.com/reel/DV7NPGKkcGq/) — "How to create a Wedding Film Look in DaVinci Resolve 🎨✨"

## Technique Overview

A beginner-friendly wedding film look using LUTs, curves, and color wheels for a romantic, timeless cinematic aesthetic. Designed for wedding videographers wanting consistent, beautiful grades.

> "Might do a few more of these, this one I might just consider it for beginners primarily" — @gabelomoteycreative

---

## Node Structure

```
Node 01: CST (Camera Log → DWG Intermediate Linear)
Node 02: PRIMARY (Linear, Luma Mix=0, Pivot=0.335)
Node 03: WEDDING LOOK
  ├── LUT: Wedding Film LUT (Key Output Gain: 50-70%)
  ├── Curves: Slight S-curve (toe lift, shoulder roll)
  ├── Color Wheels: Warm highlights, cool shadows (split tone)
  └── Hue vs Sat: Protect skin, boost warm tones
Node 04: OUTPUT CST (DWG → Rec.709 + Gamut Map)
```

---

## Step-by-Step

### 1. CST Pipeline (Nodes 01 & 04)
| Node | Input | Output |
|------|-------|--------|
| 01 | Camera Log | DWG Intermediate Linear |
| 04 | DWG Intermediate Linear | Rec.709 Gamma 2.4 + Gamut Map |

### 2. Primary Balance (Node 02)
- **Linear** mode, **Luma Mix = 0**, **Pivot = 0.335**
- Parade RGB: R=G=B on neutrals
- Vectorscope: Neutrals centered

### 3. Wedding Look (Node 03)

**LUT Application:**
- Apply Wedding Film LUT at **Key Output Gain: 50-70%**
- Never 100% — adjust per shot

**Curves (Custom):**
- **Toe:** Lift shadows slightly (0→5%)
- **Shoulder:** Roll highlights (90→96%)
- **RGB Split:** Red up slightly in highlights, Blue up in shadows

**Color Wheels (Split Tone):**
| Wheel | Hue | Sat | Purpose |
|-------|-----|-----|---------|
| **Gain** | ~35° (Warm) | 15-20 | Golden hour warmth |
| **Lift** | ~210° (Cool) | 10-15 | Clean, romantic shadows |
| **Gamma** | Neutral | 0 | Preserve midtones |

**Hue vs Sat (Skin Protection):**
- Skin range (25°-45°): -10%
- Warm tones (30°-50°): +10%
- Greens (100°-140°): -5% (natural foliage)

---

## Pro Tips from Comments

| Comment | Insight |
|---------|---------|
| @priyadarshi__pratyush | *"If you add lut at the end, don't you have to adjust contrast,expo..again?"* → **Answer:** LUT at 50-70% gain, fine-tune after |
| @gabelomoteycreative | *"Might do a few more of these, this one I might just consider it for beginners primarily"* |
| @bernardifilms | *"This look is great for weddings 🙌"* |
| @shotsbyvc | *"Straight to the point 🔥👏"* |
| @ikakofilms | *"Super easy and quick ❤️🙌"* |

---

## When to Use

| Scenario | Recommended |
|----------|-------------|
| Wedding highlight reels | ✅ Perfect |
| Ceremony footage | ✅ Consistent |
| Reception (mixed light) | ✅ Per-shot LUT gain adjust |
| Portrait/Detail shots | ✅ Skin protection built-in |
| Documentary style | ⚠️ May be too stylized |

---

## Related Techniques

- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Film LUT + PowerGrade
- `davinci-resolve-split-tone-studio-free` — Built-in split tone
- `davinci-resolve-cinematic-look-post-production-philosophy` — Full pipeline

---

## Tags

`#davinciresolve` `#colorgrading` `#wedding` `#film-look` `#lut` `#cinematic` `#wedding-film` `#gabelomoteycreative` `#beginner`