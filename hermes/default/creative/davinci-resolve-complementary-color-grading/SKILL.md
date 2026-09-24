---
name: davinci-resolve-complementary-color-grading
description: "DaVinci Resolve complementary color grading: Teal & Orange split-toning via node graph, color wheels, and curves from @magimirrai."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Complementary Colors, Teal Orange, Split Toning, Color Theory]
---

# DaVinci Resolve — Complementary Color Grading (Teal & Orange)

Learn the **Complementary Color Grading** technique from @magimirrai — using color theory (opposite hues on color wheel) to create the classic "teal & orange" cinematic look via DaVinci Resolve node graph, color wheels, and curves.

## When to Use
- Creating cinematic "blockbuster" teal & orange look
- Making subjects pop against backgrounds via color separation
- Photo/video editing with complementary color theory
- Quick stylized grades for social media, portraits, commercial work
- Understanding color wheel relationships in grading

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic node graph and color wheels familiarity
- Footage with distinct subject/background separation (skin tones + sky/water/background)

## How to Run
Build the node tree in DaVinci Resolve Color page as described in **Procedure**.

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 | Primary Balance | Neutral WB (Luma Mix=0, RGB Gain) |
| 2 | Node 02 | Color Wheels — Gain | Push **Gain toward Orange** (warm highlights) |
| 3 | Node 03 | Color Wheels — Lift | Push **Lift toward Teal** (cool shadows) |
| 4 | Node 04 | Curves / Hue vs Hue | Refine hue separation, protect skin |
| 5 | Node 05 | Saturation / Contrast | Global sat boost, contrast via Gain+Pivot |

## Procedure

### 1. Node 01 — Neutral Base (Prerequisite)
- Serial Node, label: `BASE`
- Luma Mix = 0, RGB Gain for clean WB (Parade aligned)
- Sets clean canvas — no color cast before creative grade

### 2. Node 02 — Warm Highlights (Orange/Teal Split: Highlights)
- Serial Node, label: `TEAL_ORANGE_HIGHLIGHTS`
- **Gain Wheel**: Push toward **Orange** (warm, ~30-45° on hue)
- Affects: Skin highlights, bright areas, specular reflections
- **Why:** Orange complements teal; warms subject naturally

### 3. Node 03 — Cool Shadows (Orange/Teal Split: Shadows)
- Serial Node, label: `TEAL_ORANGE_SHADOWS`
- **Lift Wheel**: Push toward **Teal** (cool, ~180-210° on hue)
- Affects: Shadows, water, sky, dark backgrounds
- **Why:** Teal in shadows creates depth, separates from warm subject

### 4. Node 04 — Hue Refinement (Protect Skin)
- Serial Node, label: `HUE_REFINE`
- **Hue vs Hue Curve**: 
  - Anchor skin tones (orange-red) — prevent overshift
  - Push cyans/blues toward teal
  - Push yellows toward orange
- **Optional:** Qualifier on skin → Layer Mixer to protect

### 5. Node 05 — Global Polish
- Serial Node, label: `POLISH`
- **Saturation**: +10 to +20 (global)
- **Contrast**: Gain + Pivot (0.335) for filmic pop
- **Optional:** Soft clip highlights, add grain/halation

> **Color Theory:** Teal (180°) and Orange (30°) are **complementary** — maximum contrast, visual pop. Used in Hollywood blockbusters for subject/background separation.

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Skin turns green/orange mess | No skin protection | Hue vs Hue anchor skin; Qualifier + Layer Node |
| Image looks "filtered" not graded | Over-saturation, no contrast base | Balance first; Gain+Pivot contrast; moderate sat |
| Shadows too noisy | Lift pushed too far | Reduce Lift teal; use Log Wheels for shadow control |
| Highlights clip | Gain too warm/bright | Lower Gain; check Waveform <940 |
| Look doesn't suit footage | Wrong color palette for scene | Assess: teal/orange works best with sky/water/urban |

## Verification
1. **Vectorscope**: Two distinct clusters — skin near orange line, bg near teal
2. **Parade**: R > G > B in highlights (orange), B > G > R in shadows (teal)
3. **Skin check**: Natural, not oversaturated, on 11° line
4. **Toggle test**: Each node adds intentional shift, not accident

## References
- Source: Instagram @magimirrai — "How to Color Grade Using Complementary Colors (Magimir Guide)" (9 weeks ago at capture)
- Caption: #magimir #photoediting #colorgrading #retouch #phototips #photography
- Engagement: 15.3K likes, 172 comments requesting "Magimir guide"
- Technique: Teal & Orange split-toning via Gain/Lift color wheels + Curves

## Related Skills
- `davinci-resolve-white-balance-luma-mix` (Node 01 base)
- `davinci-resolve-cinematic-grading-3-mistakes` (Gain+Pivot contrast)
- `skin-tone-workflow` (Protection via Layer Node)