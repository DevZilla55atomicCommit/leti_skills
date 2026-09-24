---
name: davinci-resolve-color60-apply-inverse-ootf
description: "COLOR60 Day 03/60: Apply Inverse OOTF in CST — Opto-Optical Transfer Function, automatically applied when going from smaller to larger color space. Critical when converting Rec.709 to log profiles."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, CST, OOTF, Inverse OOTF, COLOR60]
    source_url: "https://www.instagram.com/reel/DTBErI_CQ0J/"
    source_creator: "@officialjonathankim"
    source_date: "2025-01-20"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [CST, OOTF, Inverse OOTF, Rec.709, Log, COLOR60, Jonathan Kim]
---

# DaVinci Resolve: COLOR60 Day 03 — Apply Inverse OOTF in CST — @officialjonathankim

**Source:** [@officialjonathankim Instagram Reel](https://www.instagram.com/reel/DTBErI_CQ0J/) — "DAY 03/60: COLOR60"

## Technique Overview

**Apply Inverse OOTF** in Color Space Transform — Opto-Optical Transfer Function, automatically applied when going from smaller to larger color space. Critical when converting Rec.709 to log profiles.

> *"Usually 'Apply Inverse OOTF' gets applied automatically when you go from a smaller color space to a larger one in your CST in. But you should always make sure to double check when going from Rec.709 to a log color profile that it is turned on."*

> **Series:** COLOR60 — Day 3 of 60

---

## What is OOTF?

| Term | Meaning |
|------|---------|
| **OOTF** | **Opto-Optical Transfer Function** |
| **Function** | Describes how scene light → display light (system gamma) |
| **Inverse OOTF** | Reverses the display-referred curve for scene-referred work |

> *"The name doesn't tell you anything about what it actually does. So just watch the video to see how I explain it."*

---

## When It Applies Automatically

| CST Direction | Inverse OOTF | Why |
|---------------|--------------|-----|
| **Rec.709 → DWG/Log** | ✅ **Auto-applied** | Smaller → larger gamut |
| **Rec.709 → Cineon Log** | ✅ **Auto-applied** | Smaller → larger gamut |
| **Log → Rec.709** | ❌ Not applied | Larger → smaller gamut |
| **DWG → Rec.709** | ❌ Not applied | Larger → smaller gamut |

---

## Critical Check: Rec.709 → Log

**Always verify** "Apply Inverse OOTF" is **ON** when:
- Converting **Rec.709 footage** to **Log color space** (Cineon, S-Log, etc.)
- Going from **smaller gamut** to **larger gamut**

```text
CST Settings for Rec.709 → Log:
├── Input Color Space: Rec.709
├── Input Gamma: Gamma 2.4 (or 2.2)
├── Output Color Space: Rec.709 (or wider)
├── Output Gamma: Cineon Film Log / S-Log3 / etc.
└── ☑️ Apply Inverse OOTF: **ON** (critical!)
```

---

## Why It Matters

| Without Inverse OOTF | With Inverse OOTF |
|---------------------|-------------------|
| Baked Rec.709 curve stays | Removes display curve |
| "Fake log" — crushed shadows | True scene-referred linear |
| Grading tools behave wrong | Wheels/curves work correctly |
| LUTs expect wrong input | LUTs receive correct data |

---

## Comment Debates

| Comment | Point |
|---------|-------|
| @nick_cartwright_creative | *"Can you go from Rec.709 to DaVinci WG with this process?"* → **Yes, same principle** |
| @artenmedia | *"You can take back Rec709 if original is rec709… It's not gonna be log"* → **Correct, no new DR created** |
| @journey47.8 | *"Purpose of log is more info. Transforming to log doesn't help"* → **True, can't recover lost DR** |
| @onurozkayaa | *"Completely useless. Same amount of information"* → **Agreed for grading, but needed for LUT pipeline** |
| @kdetenchlapecleti | *"Why not output to DaVinci Wide Gamut instead?"* → **Better: grade in DWG, but CST still needs OOTF** |
| @timotejtrnovec | *"DR of rec 709 baked in anyway. Just looks flatter"* → **Correct, it's a pipeline requirement** |

---

## Practical Workflow: Rec.709 Footage in Log Pipeline

```
Node 01: INPUT (Rec.709 Gamma 2.4)
Node 02: CST → Rec.709 Cineon Log
         ├── Input: Rec.709 / Gamma 2.4
         ├── Output: Rec.709 / Cineon Film Log
         └── ☑️ Apply Inverse OOTF: ON
Node 03: Grade in Log space (or DWG via another CST)
Node 04: Creative LUTs (expect Log input)
Node 05: Output CST → Rec.709 Gamma 2.4
```

---

## Key Takeaways

1. **Inverse OOTF** = removes display curve for scene-referred work
2. **Auto-applied** when gamut expands (Rec.709 → larger space)
3. **Always verify** when Rec.709 → Log (Cineon, S-Log, etc.)
4. **Doesn't create DR** — only prepares for correct LUT/grade pipeline
5. **Name is misleading** — "Opto-Optical" ≠ intuitive

---

## Related Techniques

- `davinci-resolve-cst-gamut-mapping-color-spill` — CST Gamut Mapping
- `davinci-resolve-apple-log2-workflow` — Dual-CST pipeline
- `davinci-resolve-color60-kodak-2383-correct` — LUT expects Cineon Log

---

## Tags

`#davinciresolve` `#colorgrading` `#cst` `#ootf` `#inverse-ootf` `#rec709` `#log` `#color60` `#officialjonathankim`