---
name: davinci-resolve-kodak-2383-breakdown-gabelomotey
description: "Kodak 2383 Film Look breakdown in DaVinci Resolve — S-Log3 pipeline, CST to Cineon, LUT application, film emulation workflow by @gabelomoteycreative."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Kodak 2383, Film Emulation, S-Log3, CST]
    source_url: "https://www.instagram.com/reel/DS0_E-ykfAT/"
    source_creator: "@gabelomoteycreative"
    source_date: "2025-01-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Kodak 2383, Film Look, S-Log3, CST, Cineon, Film Emulation, Gabelomotey]
---

# DaVinci Resolve: Kodak 2383 Film Look Breakdown — @gabelomoteycreative

**Source:** [@gabelomoteycreative Instagram Reel](https://www.instagram.com/reel/DS0_E-ykfAT/) — "My Kodak 2383 Film Look breakdown in DaVinci Resolve"

## Technique Overview

Kodak 2383 Film Look breakdown using **S-Log3 pipeline** with proper CST to Cineon Log before LUT application. Educational tutorial for film emulation workflow.

> *"My Kodak 2383 Film Look breakdown in DaVinci Resolve 🎨✨"*

---

## Pipeline: S-Log3 → Kodak 2383

### Correct Order (as per COLOR60 Day 10)

```
Node 01: S-Log3/S-Gamut3.Cine → Rec.709 Gamma 2.4 (CST)
Node 02: Primary Balance (Rec.709)
Node 03: CST → Rec.709 Cineon Film Log (☑️ Apply Inverse OOTF)
Node 04: Kodak 2383 LUT (D55/D65)
Node 05: Compound Node → Key Output Gain (50-80%)
Node 06: Output CST → Rec.709 Gamma 2.4 + Gamut Map
```

---

## Key Settings

| Node | Tool | Settings |
|------|------|----------|
| **01** | CST | Input: S-Gamut3.Cine / S-Log3 → Output: Rec.709 / Gamma 2.4 |
| **02** | Primaries | Balance, exposure, contrast in Rec.709 |
| **03** | CST | Input: Rec.709 / 2.4 → Output: Rec.709 / **Cineon Film Log** ☑️ Inverse OOTF |
| **04** | 3D LUT | **Kodak 2383 D55** (daylight) or **D65** |
| **05** | Compound | Key Output Gain: **50-80%** per shot |
| **06** | CST + Map | Input: Cineon → Output: Rec.709 / 2.4, Gamut Map: Sat, Max 0.92, Knee 0.85 |

---

## Comment Questions & Answers

| Question | Answer |
|----------|--------|
| @garrison.ricee: *"Why Cineon Film Log?"* | 2383 LUT **expects Cineon Log input**, not Rec.709 |
| @ashwinbalajii: *"How to learn step by step?"* | Follow COLOR60 series, practice pipeline |
| @mirole._: *"Why CST out not to 2.2/2.4?"* | LUT needs Cineon; final output CST goes to 2.4 |

---

## Why This Pipeline Works

1. **Grade in controllable space** (Rec.709) — scopes, wheels work
2. **Transform TO LUT space** (Cineon) — CST with Inverse OOTF
3. **Apply LUT** — receives correct input
4. **Control intensity** — Compound Node gain
5. **Transform FROM LUT space** — Output CST + Gamut Map

---

## Related Techniques

- `davinci-resolve-color60-kodak-2383-correct` — @officialjonathankim COLOR60 Day 10
- `davinci-resolve-kodak-2383-film-emulation` — @kasia.jarco Rec.709 intermediate
- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Free LUT pack + PowerGrade

---

## Tags

`#davinciresolve` `#colorgrading` `#kodak2383` `#film-look` `#slog3` `#cst` `#cineon` `#film-emulation` `#gabelomoteycreative`