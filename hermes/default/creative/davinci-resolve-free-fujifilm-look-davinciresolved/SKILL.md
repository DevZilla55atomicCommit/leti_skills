---
name: davinci-resolve-free-fujifilm-look-davinciresolved
description: Free Fujifilm film look in DaVinci Resolve — using built-in Resolve Film LUTs with proper color space conversion (Rec.709 → Cineon Log → Fujifilm LUT)
category: creative
tags: [davinci-resolve, fujifilm, film-look, lut, film-emulation, color-space, rec709, cineon, davinciresolved]
source_url: https://www.instagram.com/reel/DKhdbNqRgXx/
author: davinciresolved
---

# DaVinci Resolve: Free Fujifilm Film Look

> **"Free Fujifilm look in DaVinci Resolve"** — davinciresolved

## Core Technique: Built-in Fujifilm LUTs with Correct Pipeline

DaVinci Resolve includes **free Fujifilm Film Look LUTs** — but they require the correct color space pipeline to work properly.

### ❌ Wrong Way (What Most People Do)
```
Footage (Rec.709) → Fujifilm LUT
```
Result: Crushed blacks, oversaturated, wrong colors

### ✅ Correct Pipeline
```
Footage (Log/Raw) 
    → CST: Camera Log → Rec.709 (or DWG Intermediate)
    → CST: Rec.709 → Cineon Log (Film Log)
    → Fujifilm LUT (Resolve built-in)
    → Compound Node: Key Output Gain control
    → Output CST: Cineon → Rec.709/Gamma 2.4
```

## Step-by-Step

| Node | Operation | Settings |
|------|-----------|----------|
| 01 | **CST (Input)** | Camera Space (S-Log3, F-Log, etc.) → Rec.709 / Gamma 2.4 |
| 02 | **CST (Film Prep)** | Rec.709 / Gamma 2.4 → Cineon Log / Cineon Gamut |
| 03 | **Fujifilm LUT** | Resolve Built-in: `Film Looks > Fujifilm` (e.g., Fujifilm 3510, 3513, etc.) |
| 04 | **Compound Node** | Key Output → Gain for intensity control (0.5–1.0 typical) |
| 05 | **CST (Output)** | Cineon Log → Rec.709 / Gamma 2.4 (or target delivery) |

## Critical Insight from Comments

> **@hiro_briquet:** *"Missing converting to Rec709 since the Resolve film lut expect rec709"*
> 
> **Correction:** The built-in Film Look LUTs expect **Cineon Log** input, not Rec.709. The pipeline is: Grade in Rec.709 → CST to Cineon → LUT → CST to Output.

> **@wayward.mov:** *"Does the Davinci software come with these LUTs?"* → **Yes**, built-in under `Film Looks` folder in LUT browser.

## Camera-Specific Notes

| Camera | Log Profile | Input CST |
|--------|-------------|-----------|
| Fujifilm X-T3/X-T4 | F-Log | F-Log / F-Gamut → Rec.709 |
| Fujifilm X-T30 (non-F-Log) | Standard/ETR | Rec.709 → Cineon (skip first CST) |
| Sony | S-Log3 | S-Log3 / S-Gamut3 → Rec.709 |
| Canon | C-Log | C-Log / Cinema Gamut → Rec.709 |

## Built-in Fujifilm LUTs (Resolve 18/19/20/21)

- `Fujifilm 3510` — Classic Chrome look
- `Fujifilm 3513` — Velvia-style saturation
- `Fujifilm 3514` — Pro Neg. Std
- `Fujifilm 3515` — Pro Neg. Hi
- `Fujifilm 3516` — Eterna (cinematic, low contrast)
- `Fujifilm 3517` — Acros (B&W)

## Pro Tips

1. **Intensity Control:** Wrap LUT in Compound Node → Key Output Gain = 0.5–0.7 for subtle look
2. **Skin Protection:** Add Qualifier + Layer Mixer before LUT to protect skin tones
3. **Halation/Grain:** Add after LUT for film texture (see `davinci-resolve-ivarbrauer-film-look-lut-powergrade`)
4. **BRAW/Raw:** Grade in DWG Intermediate → CST to Cineon → LUT for maximum latitude

## Related Skills

- `davinci-resolve-kodak-2383-film-emulation` — Kodak 2383 pipeline (similar CST→Cineon→LUT)
- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Free LUT pack + PowerGrade with halation/grain
- `davinci-resolve-kodak-2383-breakdown-gabelomotey` — S-Log3 → CST Rec.709 → CST Cineon → Kodak 2383

## Hashtags

#davinciresolve #colorgrading #videoediting #fujifilm #filmlook #lut