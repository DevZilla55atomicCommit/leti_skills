---
name: davinci-resolve-cinematic-grading-3-mistakes
description: "DaVinci Resolve: 3 mistakes killing cinematic look — node structure, exposure, and color management fixes from @ey_cinema."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Cinematic, Node Structure, Exposure, Color Management]
---

# DaVinci Resolve — 3 Mistakes Killing Your Cinematic Look

Learn the **3 critical mistakes** that secretly kill cinematic footage from @ey_cinema — based on 5 years of color grading experience. Covers node structure, exposure management, and color pipeline fixes in DaVinci Resolve.

## When to Use
- Your grades look "video-ish" not cinematic
- Struggling with clean, filmic node trees
- Exposure/contrast feels off despite correct scopes
- Color management pipeline issues (CST placement, gamut mapping)
- Want a repeatable "slightly better" method that compounds

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic node graph familiarity
- Understanding of CST (Color Space Transform) basics

## How to Run
Review the 3 mistakes and their fixes. Apply to your node tree in order: Structure → Exposure → Color Management.

## Quick Reference
| Mistake | Symptom | Fix | Node/Tool |
|---------|---------|-----|-----------|
| 1. Wrong Node Structure | Messy tree, hard to match shots | Serial: Balance → Exposure → Color → Creative | Serial Nodes, Labels |
| 2. Exposure/Contrast Order | Flat or crushed look | Balance first, then contrast via Gain/Pivot | Primary Wheels, Pivot 0.335 |
| 3. Color Management Gaps | Gamut clipping, hue shifts | CST early → Grade in wide gamut → CST late | CST Nodes, DWG/ACEScg |

## Procedure

### Mistake 1 — Wrong Node Structure (The Foundation)
**Problem:** Random node order, parallel nodes too early, no logical flow.
**Cinematic Principle:** "Slightly better adjustments compound quickly."

**Correct Serial Flow:**
```
INPUT
  │
  ├─ NODE 01: PRIMARY BALANCE (Linear, Luma Mix=0, RGB Gain)
  ├─ NODE 02: EXPOSURE / CONTRAST (Gain + Pivot, or Log Wheels)
  ├─ NODE 03: COLOR / SATURATION (HSV, Color Wheels, Color Slice)
  ├─ NODE 04: CREATIVE LOOK / LUT (Film emulation, halation, grain)
  └─ NODE 05: OUTPUT CST (Rec.709 / P3 / HDR)
```

**Key Rules:**
- **Correction before Creative** — always
- **Serial for correction, Layer/Parallel for isolation** (skin, sky, etc.)
- **Label every node** (WB, EXP, SAT, LOOK, OUT)
- **PowerGrade the template** for reuse

### Mistake 2 — Exposure/Contrast in Wrong Order
**Problem:** Adding contrast (Lift/Gamma/Gain) before white balance → color contamination.
**Cinematic Principle:** Clean balance = clean contrast.

**Correct Order:**
1. **NODE 01:** White Balance (RGB Gain, Luma Mix=0) — neutralize first
2. **NODE 02:** Exposure/Contrast — **Gain + Pivot (0.335)** or **Log Wheels**
   - Gain = global brightness (printer lights)
   - Pivot = 18% gray anchor (0.335)
   - Avoid Lift/Gamma for primary contrast
3. **Verify on Waveform:** Skin 50-70 IRE, legal range 64-940

> **Why Gain+Pivot?** Lift/Gamma couples shadows/midtones. Gain+Pivot = clean offset, matches film printer lights.

### Mistake 3 — Color Management Gaps (CST Placement)
**Problem:** Grading in Rec.709 → clipping, hue shifts, no highlight rolloff.
**Cinematic Principle:** Grade in wide gamut, output transform last.

**Correct Pipeline:**
```
CAMERA LOG (S-Log3, LogC, BRAW, etc.)
  │
  ├─ CST 1: Camera Log → **DWG Intermediate / ACEScg / Linear** (wide gamut)
  │       └─ Grade HERE (all correction + creative)
  │
  └─ CST 2: DWG/ACEScg → **Rec.709 / P3-D65 / ST2084** (display transform)
```

**Critical Settings:**
- CST 1: **Tone Mapping = None** (preserve all data)
- Grade in **Linear/DWG** — massive headroom, no clipping
- CST 2: **Tone Mapping = DaVinci** (or ACES for HDR)
- **Never** put creative LUT before final CST

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Grades don't match across shots | No template / random node order | Build PowerGrade template; copy Node 01-03 |
| Highlights clip, skin looks wrong | Grading in Rec.709 | Move CST to end; grade in DWG/ACEScg |
| Hue shifts on saturated colors | Wrong gamut mapping | CST early; verify with CIE scope |
| Contrast looks "digital" | Lift/Gamma primary | Use Gain+Pivot (0.335) or Log Wheels |
| LUT looks different per clip | LUT before CST / wrong input | LUT after CST 2; or CST→LUT→CST chain |

## Verification
1. **Node Tree:** Clean serial 01-05, labeled, PowerGrade saved
2. **Scopes:** Waveform legal, Parade balanced, Vectorscope skin on line
3. **Toggle Test:** Each correction node improves image cleanly
4. **Shot Match:** Copy template → tweak Node 01-02 per clip → consistent

## References
- Source: Instagram @ey_cinema — "why your color grading never looks CINEMATIC (and how to fix it in DaVinci Resolve)" / "after 5 years of color grading I see 3 MISTAKES that secretly KILLS your footage"
- Carousel post (8 slides), node graph with 3 red-circled mistakes
- Caption: "Comment 'movie' for a full breakdown on this workflow"
- Hashtags: #videography #colorgrading #cinematic #fyp
- Date: ~1 week ago at capture (June 27, 2026 post date)

## Related Skills
- `davinci-resolve-white-balance-luma-mix` (Mistake 2 fix)
- `davinci-resolve-masking-power-masking` (Layer node isolation)
- `color-correction-fundamentals` (Scopes, linear workflow)