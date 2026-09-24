---
name: davinci-resolve-kodak-film-look-davinciresolved
description: "Kodak film look in DaVinci Resolve using built-in Film Looks (Kodak 2383, etc.) with correct CST pipeline: Grade in Rec.709 to CST to Cineon to Kodak LUT to Output CST"
category: creative
tags: [davinci-resolve, kodak, film-look, lut, film-emulation, cineon, cst, davinciresolved]
source_url: https://www.instagram.com/reel/DLsLVBOR0Eb/
author: davinciresolved
---

# DaVinci Resolve: Kodak Film Look

> **"Kodak film look in DaVinci Resolve"** -- davinciresolved

## Core Technique: Built-in Kodak LUTs + Correct Cineon Pipeline

DaVinci Resolve includes **free Kodak Film Look LUTs** (Kodak 2383, etc.) -- but they require the **Cineon Log pipeline** to work correctly.

---

## Wrong Way (What Most People Do)

```
Footage (Rec.709) to Kodak 2383 LUT
```
**Result:** Crushed blacks, blown highlights, oversaturated, wrong color response

---

## Correct Pipeline

```
Camera Log/Raw Footage
         |
         v
NODE 01: CST (Input)
Camera Log to Rec.709 / Gamma 2.4
e.g., S-Log3/S-Gamut3 to Rec.709

NODE 02: Primary Grade (Rec.709)
Balance, Exposure, Contrast, Skin
Grade creatively in Rec.709 space

NODE 03: CST (Film Prep)
Rec.709 / Gamma 2.4 to Cineon Log
Output: Cineon Log / Cineon Gamut

NODE 04: KODAK LUT (Built-in)
LUT Browser to Film Looks to Kodak
Options: Kodak 2383, Kodak 2393,
         Kodak Vision3 50D, 250D,
         500T, etc.

NODE 05: Compound Node (Optional)
Key Output to Gain: 0.5-0.8
Intensity control for subtle look

NODE 06: CST (Output)
Cineon Log to Rec.709 / Gamma 2.4
(or P3/DCI for cinema delivery)
```

---

## Built-in Kodak LUTs (Resolve 18/19/20/21)

| LUT Name | Character | Best For |
|----------|-----------|----------|
| **Kodak 2383** | Classic print film, warm highlights, teal shadows | Narrative, cinematic |
| **Kodak 2393** | Slightly higher contrast, cooler | Modern cinema |
| **Kodak Vision3 50D** | Daylight, fine grain, clean | Bright exteriors |
| **Kodak Vision3 250D** | Daylight, versatile | General daylight |
| **Kodak Vision3 500T** | Tungsten, low light, push look | Night, interiors |

---

## Why Cineon Log?

**Film LUTs are designed for Cineon Log input** -- the logarithmic encoding used in film scanning.

| Space | Gamma | Use |
|-------|-------|-----|
| **Rec.709** | 2.4 | Display, grading |
| **Cineon Log** | Log (10-bit) | Film LUT input |
| **Linear** | 1.0 | Compositing, CGI |

**Pipeline:** Grade in Rec.709 to **CST to Cineon** to Film LUT to **CST to Output**

---

## Pro Tips from Comments

> **@conteoregresivofilms:** *"Your output color space says timeline, which one did You have?"*
>
> Answer: Set Project Settings to Color Management to Output Color Space = **Rec.709 Gamma 2.4** (or P3/DCI). Timeline = Project setting.

> **@fahad_almacki:** *"I get hyper exposure when I add any LUT to my image"*
>
> Cause: Applying LUT **before** CST to Cineon, or on log footage directly.
> Fix: Follow pipeline above -- LUT *only* sees Cineon Log.

> **@sebastianbethcke:** *"What if my camera model is an iPhone?"*
>
> iPhone (Apple Log/ProRes): CST: Apple Log to Rec.709 to Cineon to Kodak LUT to Output CST
> iPhone (Standard): Skip first CST, grade in Rec.709 to Cineon to LUT

> **@claycadet_:** *"So all this time all the colors I have been seeing and buying LUTs all was there in Film looks in Davinci"*
>
> Yes! Resolve's built-in Film Looks (Kodak, Fuji, Agfa) are **free and professional-grade** when piped correctly.

> **@_aliasqarzadeh:** *"Do these settings apply to all cameras?"*
>
> Pipeline applies to ALL cameras -- only **Node 01 (Input CST)** changes per camera.

> **@dudusbigol:** *"I just did this and it's sweet! 🔥"*
>
> Works!

---

## Camera-Specific Input CST (Node 01)

| Camera | Log Profile | CST Input |
|--------|-------------|-----------|
| **Sony** | S-Log3 | S-Log3 / S-Gamut3 |
| **Canon** | C-Log3 | C-Log3 / Cinema Gamut |
| **Blackmagic** | BRAW Film Gen 5 | BM Film / BM Wide Gamut |
| **ARRI** | LogC3/4 | Alexa LogC / Alexa Wide Gamut |
| **RED** | Log3G10 | RED Log3G10 / RED Wide Gamut |
| **Fujifilm** | F-Log | F-Log / F-Gamut |
| **Panasonic** | V-Log | V-Log / V-Gamut |
| **iPhone** | Apple Log / ProRes | Apple Log / P3 / Rec.2020 |
| **DJI** | D-Log | D-Log / D-Gamut |

---

## Advanced: DWG Intermediate (Maximum Latitude)

For BRAW/Raw -- grade in **DaVinci Wide Gamut (DWG)**:

```
Node 01: CST: Camera to DWG (Intermediate)
Node 02: Grade in DWG (massive latitude)
Node 03: CST: DWG to Cineon Log
Node 04: Kodak LUT
Node 05: CST: Cineon to Output
```

---

## Related Skills

- `davinci-resolve-kodak-2383-film-emulation` -- Kasia Jarco: Kodak 2383 in Rec.709 intermediate
- `davinci-resolve-kodak-2383-breakdown-gabelomotey` -- Gabe Lomotey: S-Log3 to CST to CST to Kodak 2383
- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` -- Free LUT pack + PowerGrade (halation, grain)
- `davinci-resolve-free-fujifilm-look-davinciresolved` -- Same pipeline for Fujifilm LUTs

---

## Hashtags

#davinciresolve #colorgrading #videoediting #kodak #filmlook #lut #filmmulation #cineon #cst #davinciresolved