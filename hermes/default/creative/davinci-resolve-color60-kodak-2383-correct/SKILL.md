---
name: davinci-resolve-color60-kodak-2383-correct
description: "COLOR60 Day 10/60: Kodak 2383 LUT correct application — expects Rec.709 color space + Cineon Film Log gamma, NOT Rec.709 gamma 2.4. Common mistake: applying LUT directly on Rec.709."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Kodak 2383, LUT, Cineon, COLOR60]
    source_url: "https://www.instagram.com/reel/DTVZJYlkQAc/"
    source_creator: "@officialjonathankim"
    source_date: "2025-01-16"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Kodak 2383, LUT, Cineon, Film Log, COLOR60, Jonathan Kim]
---

# DaVinci Resolve: COLOR60 Day 10 — Kodak 2383 LUT Correct Application — @officialjonathankim

**Source:** [@officialjonathankim Instagram Reel](https://www.instagram.com/reel/DTVZJYlkQAc/) — "DAY 10/60: COLOR60"

## Technique Overview

**Correct Kodak 2383 LUT application** — the LUT expects **Rec.709 color space + Cineon Film Log gamma**, NOT Rec.709 gamma 2.4. Most people apply it wrong directly on Rec.709 footage.

> *"I've seen so many people use the Kodak 2383 LUT wrong in DaVinci Resolve, and even worse, I've seen it taught incorrectly. Anytime you use a LUT, you need to know what color space it expects. A lot of people assume 2383 is Rec.709 gamma 2.4, but it's not. It expects Rec.709 for color space and Cineon Film Log for gamma."*

> **Series:** COLOR60 — Day 10 of 60

---

## The Mistake (What Most People Do)

```
WRONG PIPELINE:
Node 01: Grade in Rec.709 Gamma 2.4
Node 02: Kodak 2383 LUT (direct on Rec.709)
Node 03: Output

RESULT: Crushed shadows, oversaturated, wrong contrast, "digital" look
```

---

## Correct Pipeline

```
CORRECT PIPELINE:
Node 01: Grade in Rec.709 Gamma 2.4 (Balanced)
Node 02: CST (Rec.709 Gamma 2.4 → Rec.709 Cineon Log)
Node 03: Kodak 2383 LUT (D55 or D65)
Node 04: Compound Node → Key Output Gain (50-80% control)
Node 05: Output CST (Cineon → Rec.709 Gamma 2.4 + Gamut Map)
```

### Why This Works
- **LUT expects Cineon Log input** — not Rec.709
- **Grade in Rec.709** (controllable, scopes work)
- **CST to Cineon** — transforms to LUT's expected input
- **Compound Node** — gain control for per-shot intensity
- **Output CST** — back to delivery space

---

## Step-by-Step Settings

| Step | Node | Tool | Settings |
|------|------|------|----------|
| **1. Base Grade** | 01 | Primary | Rec.709 Gamma 2.4, balanced, scopes-verified |
| **2. CST to Cineon** | 02 | Color Space Transform | **Input:** Rec.709 / Gamma 2.4 → **Output:** Rec.709 / **Cineon Film Log** |
| **3. Kodak 2383 LUT** | 03 | 3D LUT | **Kodak 2383 D55** (daylight) or **D65** |
| **4. Gain Control** | 04 | Compound Node | **Key Output Gain:** 50-80% (per shot) |
| **5. Output CST** | 05 | CST + Gamut Map | **Input:** Cineon → **Output:** Rec.709 Gamma 2.4, Gamut Map: Sat, Max 0.92, Knee 0.85 |

---

## Comment Insights

| Comment | Insight |
|---------|---------|
| @s.schoutenmedia | *"Don't you put the LUT at the end of the node tree?"* → **Yes, but AFTER CST to Cineon** |
| @jonathankim | *"Instagram TOOK DOWN the original audio... REPOST on my page"* | |
| @zurawskipiotrek | *"2383 is not meant for shooting on it bro"* → Print film emulation, not camera LUT |
| @morten_jensen_privat | *"Good video - just showed the correct way"* | |
| @brandon_scott2727 | *"What would I change if shooting on bmpcc4k?"* → Same pipeline: BRAW→Rec.709→Cineon→LUT |

---

## Key Takeaway

| Principle | Application |
|-----------|-------------|
| **Know your LUT's expected input** | 2383 = Rec.709 + Cineon Log |
| **Grade in controllable space** | Rec.709 (scopes, wheels work) |
| **Transform TO LUT space** | CST before LUT |
| **Control intensity** | Compound Node gain |
| **Transform FROM LUT space** | Output CST after LUT |

---

## Related Techniques

- `davinci-resolve-kodak-2383-film-emulation` — @kasia.jarco Rec.709 intermediate workflow
- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Free LUT pack + PowerGrade
- `davinci-resolve-kodak-2383-darren-mostyn` — BBC/Netflix pro correct application

---

## Tags

`#davinciresolve` `#colorgrading` `#kodak2383` `#lut` `#cineon` `#film-log` `#color60` `#officialjonathankim`