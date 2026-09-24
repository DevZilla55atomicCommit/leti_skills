---
name: davinci-resolve-ivarbrauer-film-look-lut-powergrade
description: "Ivar Brauer's Film Look LUT Pack (Free) + PowerGrade template — cinematic film emulation looks for DaVinci Resolve with BRAW support."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, LUT, PowerGrade, Film Look, Film Emulation, BRAW, Creative Grading]
    source_url: "https://www.instagram.com/reel/DZDribWx46W/"
    source_creator: "@ivarbrauer"
    source_date: "2025-06-01"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner to Intermediate"
    tags: [LUT Pack, PowerGrade, Film Emulation, BRAW, Free LUT, Cinematic Look, Neo Noir, Ivar Brauer]
---

# DaVinci Resolve: Ivar Brauer Film Look LUT Pack & PowerGrade

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DZDribWx46W/) — "Film Look LUT Pack FREE + Powergrade Version"

## Overview

Ivar Brauer (@ivarbrauer) offers a **Film Look LUT Pack** with three tiers:
- **FREE:** LUT Pack (basic film looks)
- **8€ PowerGrade:** Full node tree with controls, BRAW optimized
- **16€ Project Version:** Complete project template with timelines, settings

Hashtags: #davinciresolve #powergrade #freelut #colorist #editingvideo

---

## What's Included (Based on Creator's Other Content)

### Free LUT Pack
- Multiple film emulation LUTs (Kodak 2383, Fujifilm, Cineon-based)
- Rec.709 and Log input variants
- Basic creative looks

### PowerGrade (8€) — Recommended for Serious Work
- **Full node tree** with labeled, adjustable nodes
- **BRAW optimization** — native Blackmagic RAW handling
- **CST pipeline** — proper color space transforms
- **Layer nodes** for skin protection, highlight rolloff
- **Custom curves** for film characteristics (toe, shoulder, halation)
- **Power Window templates** for vignette, subject isolation
- **Compound Node** — save as template, apply to any clip

### Project Version (16€)
- Complete Resolve project (.drp)
- Pre-built timelines with test footage
- Color management settings configured
- Delivery presets

---

## Typical PowerGrade Node Structure (Inferred)

```
Node 01: INPUT CST
  → Camera Log (BRAW/S-Log3/LogC) → DaVinci Wide Gamut / DWG Intermediate

Node 02: PRIMARY BALANCE
  → Linear Gain (Luma Mix 0, Pivot 0.335)
  → Exposure, White Balance

Node 03: FILM EMULATION CORE
  → Custom Curves (Toe lift, Shoulder roll, Cross-process hints)
  → Hue vs Hue/Sat for film color palette

Node 04: HALATION / BLOOM
  → Glow OFX (low threshold, large radius)
  → Add blend mode

Node 05: GRAIN / TEXTURE
  → Film Grain OFX (Kodak / Fuji presets)
  → Overlay/Soft Light blend

Node 06: CREATIVE LOOK (LUT Slot)
  → LUT input (swapable: Kodak 2383, Fuji 3510, etc.)
  → Key Output Gain for intensity

Node 07: SKIN PROTECTION (Layer Node)
  → Qualifier: Skin tones
  → Layer Mixer: Composite corrected skin OVER look

Node 08: VIGNETTE / POWER WINDOW
  → Circular window, feathered
  → Exposure -0.15 to -0.3

Node 09: OUTPUT CST
  → DWG Intermediate → Rec.709 Gamma 2.4
  → Gamut Mapping: Saturation, Max 0.92, Knee 0.85
```

---

## How to Use Free LUTs Properly

> ⚠️ **Critical:** Don't just drop LUT on log footage!

### Correct LUT Workflow:
```
1. Node 01: CST — Camera Log → Rec.709 (or DWG Intermediate)
2. Node 02: Balance/Exposure (scopes verified)
3. Node 03: **LUT** — Apply film LUT at 50-75% Key Output Gain
4. Node 04: Fine-tune (Contrast, Sat, WB) AFTER LUT
5. Node 05: Output CST → Rec.709 + Gamut Mapping
```

### Wrong Way (Common Mistake):
```
Log Footage → LUT (Rec.709) → Output
Result: Crushed blacks, clipped highlights, wrong colors
```

---

## BRAW-Specific Advantages (PowerGrade)

| Feature | Free LUT | PowerGrade |
|---------|----------|------------|
| BRAW Color Science | ❌ Fixed | ✅ Uses BRAW Panel (ISO, WB, Tint) |
| Highlight Recovery | Limited | Full BRAW highlight rolloff |
| Noise Management | None | Built-in NR nodes (Temporal/Spatial) |
| Flexibility | One look | Adjustable per node |
| Learning | Black box | Open node tree = education |

---

## Film Look Characteristics (Typical Brauer Style)

| Characteristic | Setting |
|----------------|---------|
| **Contrast** | Lowered midtones, lifted blacks (toe) |
| **Highlights** | Soft rolloff, slight bloom/halation |
| **Color Palette** | Teal shadows, warm mids, protected skin |
| **Saturation** | Moderate, film-like density (not digital pop) |
| **Grain** | Structural, not overlay — varies by ISO |
| **Gate/Weave** | Subtle (optional) |

---

## Installation

### Free LUTs:
1. Download from creator's link (comment "Free")
2. Copy `.cube` files to:
   - **Mac:** `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/`
   - **Win:** `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\LUT\`
3. Restart Resolve → LUTs appear in 3D LUT menu

### PowerGrade (.drx):
1. Purchase/download
2. In Color page → Gallery → Right-click → **Import PowerGrade**
3. Apply to clip: Drag from Gallery to node graph

---

## Related Techniques

- `davinci-resolve-kodak-2383-correct-application` — Proper film LUT pipeline
- `davinci-resolve-cst-gamut-mapping-color-spill` — Output gamut safety
- `davinci-resolve-diffusion-soft-light` — Halation/bloom for film feel
- `davinci-resolve-white-balance-luma-mix` — Clean base for LUTs

---

## Tags

`#davinciresolve` `#lut` `#powergrade` `#film-look` `#film-emulation` `#braw` `#cinematic` `#ivarbrauer` `#freelut` `#creative-grading`