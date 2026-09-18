---
name: davinci-resolve-ivarbrauer-white-balance-fixes
description: "3 Easy White Balance Fixes for Natural Neutral Colors — Temperature/Tint, Linear Gain (Luma Mix=0), and Gray Card/Reference methods in DaVinci Resolve."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, White Balance, Color Correction, Linear Gain]
    source_url: "https://www.instagram.com/reel/DY7uvhhxw_o/"
    source_creator: "@ivarbrauer"
    source_date: "2025-05-24"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Beginner to Intermediate"
    tags: [White Balance, Temperature, Tint, Linear Gain, Luma Mix, Gray Card, Parade RGB, Vectorscope, Ivar Brauer]
---

# DaVinci Resolve: 3 Easy White Balance Fixes for Natural Neutral Colors

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DY7uvhhxw_o/) — "3 Easy White Balance Fixes for Natural Neutral Colors"

## Overview

Three practical white balance methods in DaVinci Resolve, ranging from basic to professional. Key insight: **Linear Gain with Luma Mix = 0** is the most photorealistic method but requires disabling Lum Mix.

---

## Method 1: Temperature / Tint Sliders (Basic)
**Tool:** Color Wheels → Temp / Tint
- **Fastest** for rough correction
- **Limitation:** Operates in display-referred space, not scene-linear
- **Use case:** Quick fixes, client previews, non-critical work

---

## Method 2: Linear Gain with Luma Mix = 0 (Pro / Photorealistic)
**Tool:** Key Panel → Gain (RGB) + Luma Mix = 0

### Why This Works
- **Gain in Linear space** = pure photon multiplier (printer lights)
- **Luma Mix = 0** decouples Gain from Lift/Gamma
- **Luma Mix ≠ 0** introduces artificial cross-contamination (per @_daniel.pk comment)

### Setup
1. **Node 01:** CST — Camera Log → **Linear** (same gamut)
2. **Key Panel:**
   - **Luma Mix:** **0** (critical!)
   - **Gain Pivot:** 0.335 (18% gray anchor)
3. **RGB Gain:** Adjust R/G/B independently until neutrals align on Parade
4. **Vectorscope:** Verify center crosshair on neutral reference

> **Comment by @_daniel.pk:** *"When using Linear Gain, you need to set Lum Mix to 0 for it to look truly photorealistic. Lum Mix is an artificial behavior that we don't want, as it doesn't work well with Linear Gain. It can technically destroy the image, even if you might not perceive it with the naked eye."*

---

## Method 3: Gray Card / Color Checker Reference (Most Accurate)
**Tool:** Qualifier + Vectorscope + Parade

### Workflow
1. Shoot **gray card** or **ColorChecker** in scene lighting
2. **Qualifier** → Pick gray patch (L=50%, S≈0)
3. **Vectorscope:** Display Qualifier Focus ON
4. **Parade RGB:** Adjust Gain until R=G=B on gray patch
5. **Copy** Node 01 settings to all shots in same lighting

### ColorChecker Bonus
- **White patch:** Set highlight exposure (90-95 IRE)
- **Gray patch:** White balance (R=G=B)
- **Black patch:** Black level (5-10 IRE)
- **Skin patches:** Verify skin tone line alignment

---

## Pro Workflow: Combined Approach

```
Node 01: CST — Camera Log → Linear (same gamut)
Node 02: PRIMARY WB — Linear Gain, Luma Mix 0, Pivot 0.335
  → Parade RGB: Match R/G/B on gray reference
  → Vectorscope: Neutrals centered
Node 03: CREATIVE — (After WB is locked)
Node 04: OUTPUT CST — Linear → Rec.709 + Gamut Mapping
```

---

## Key Settings Summary

| Setting | Value | Why |
|---------|-------|-----|
| **Color Space** | Linear (via CST) | Photometric accuracy |
| **Luma Mix** | **0** | Pure Gain = printer lights |
| **Gain Pivot** | 0.335 | Locks 18% gray |
| **Scopes** | Parade RGB + Vectorscope | Objective verification |
| **Qualifier** | Display Qualifier Focus | Precision picking |

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Temp/Tint only | Color shifts with exposure | Use Linear Gain |
| Luma Mix ≠ 0 | Cross-contamination, weird colors | Set Luma Mix = 0 |
| WB in Log space | Non-linear response | Convert to Linear first |
| No reference | Guessing | Shoot gray card / ColorChecker |
| WB after creative | Creative grade shifts WB | WB **first**, creative **after** |

---

## Related Techniques

- `davinci-resolve-white-balance-luma-mix` — @rolling.shuttermedia Luma Mix=0 deep dive
- `davinci-resolve-primary-color-correction-linear` — Waqas Qazi linear workflow
- `davinci-resolve-cinematic-grading-3-mistakes` — @ey_cinema node structure (CST first)

---

## Tags

`#davinciresolve` `#whitebalance` `#colorcorrection` `#lineargain` `#lumamix` `#printerlights` `#paradergb` `#vectorscope` `#ivarbrauer` `#photorealistic`