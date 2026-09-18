---
name: davinci-resolve-kodak-2383-film-emulation
description: "Kodak 2383 film emulation in DaVinci Resolve — LUT application, intermediate Rec.709 workflow, CST pipeline, cinematic language, emotional grounding."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Kodak 2383, Film Emulation, LUT, Cinematic]
    source_url: "https://www.instagram.com/reel/DUlwVzIAAyL/"
    source_creator: "@kasia.jarco / @colorgradinginsights"
    source_date: "2025-02-10"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Kodak 2383, Film Emulation, LUT, Cinematic, Rec.709 Intermediate, Kasia Jarco, Color Grading Insights]
---

# DaVinci Resolve: Kodak 2383 Film Emulation — @kasia.jarco / @colorgradinginsights

**Source:** [@kasia.jarco Instagram Reel](https://www.instagram.com/reel/DUlwVzIAAyL/) — "There's something timeless about Kodak 2383..."

## Technique Overview

Kodak 2383 film emulation workflow — originally designed for print film, this emulation isn't about flashy color but **restraint, density, and character**. How to apply the LUT in DaVinci Resolve for cinematic, emotionally grounded results.

> *"When used thoughtfully, 2383 doesn't just 'grade' your image; it anchors it in a cinematic language that feels intentional and emotionally grounded."* — @kasia.jarco

> **Note:** Post says "2328" but context clearly indicates **Kodak 2383** (common typo)

---

## Recommended Pipeline (from comments + best practice)

### Correct Kodak 2383 Pipeline
```
Node 01: Base Grade (Rec.709, Balanced)
Node 02: CST (Rec.709 → Cineon Log)
Node 03: Kodak 2383 LUT (D55 or D65)
Node 04: Compound Node → Key Output Gain (50-80%)
Node 05: Output CST (Rec.709 + Gamut Map)
```

### Why Rec.709 Intermediate?
- **LUTs expect Cineon Log input** — not Rec.709 direct
- **Grade in Rec.709** → CST to Cineon → LUT → Compound for control
- **Wrong way:** Direct LUT on Rec.709 = crushed/oversaturated

---

## Key Settings

| Step | Tool | Settings |
|------|------|----------|
| **1. Base Grade** | Primary | Rec.709, balanced, scopes-verified |
| **2. CST to Cineon** | Color Space Transform | Input: Rec.709/Gamma 2.4 → Output: Cineon/Log |
| **3. Kodak 2383 LUT** | 3D LUT | Kodak 2383 D55 (daylight) or D65 |
| **4. Control** | Compound Node | Key Output Gain: 50-80% (per shot) |
| **5. Output** | CST + Gamut Map | Cineon → Rec.709/2.4, Gamut Map Sat |

---

## Pro Tips from Comments

| Comment | Insight |
|---------|---------|
| @jay_not_son | *"Why do you do intermediate in rec 709?"* → **LUTs need Cineon input; Rec.709 grade is controllable** |
| @ceoanwar | *"How about if shoot in vlog? Panasonic. Did the setting same?"* → **Yes, CST chain adapts: V-Log→Rec.709→Cineon→LUT** |
| @kolawoleblvck | *"❤️❤️"* |
| @hotelkiloproject | *"Interesting topic!! Is that CST also applied to sony a7iv camera? Thank you"* → **Yes, S-Log3→Rec.709→Cineon→LUT works** |
| @eueliaslimaofc | *"👏👏👏👏👏👏"* |
| @nestorvisions | *"If you get tired of grading VO work will definitely be a backup"* |
| @andiinsta1966 | *"As always very pro and on the point... and I love your voice"* |

---

## When to Use

| Scenario | Recommended |
|----------|-------------|
| **Narrative/Drama** | ✅ Perfect — emotional grounding |
| **Commercial/Brand** | ⚠️ May be too restrained |
| **Wedding/Romantic** | ✅ Timeless, density |
| **Documentary** | ✅ Natural, cinematic |
| **Music Video** | ✅ Character, texture |

---

## Related Techniques

- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Film LUT pack + PowerGrade (Free + Paid)
- `davinci-resolve-kodak-2383-darren-mostyn` — Correct application (CST to Cineon)
- `davinci-resolve-kodak-2383-gabe-lomotey` — DWG Intermediate + DCTLs + Dehancer

---

## Tags

`#davinciresolve` `#colorgrading` `#kodak2383` `#film-emulation` `#lut` `#cinematic` `#kasia-jarco` `#colorgradinginsights` `#cineon` `#print-film`