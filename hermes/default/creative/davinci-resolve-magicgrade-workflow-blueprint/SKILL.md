---
name: davinci-resolve-magicgrade-workflow-blueprint
description: "MagicGrade 4-Step Workflow Blueprint by Summy Dean — F1 Adjustments, F2 Color Palette, F3 Split Tone/Contrast, F4 Texture/Saturation/Density + Balance Golden Settings."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, MagicGrade, Workflow, Color Grading, Keyboard Shortcuts, Productivity]
    source_url: "https://www.instagram.com/p/DYsIl8-DZnK/"
    source_creator: "@summy_dean"
    source_date: "2025-05-23"
    vault_category: "Node Structures / Templates"
    skill_level: "Intermediate"
    tags: [MagicGrade, Workflow, 4-Step Grade, Keyboard Shortcuts, F-Keys, Summy Dean, Template, Blueprint]
---

# DaVinci Resolve: MagicGrade 4-Step Workflow Blueprint — @summy_dean

**Source:** [@summy_dean Instagram Post](https://www.instagram.com/p/DYsIl8-DZnK/) — "MagicGrade 7 day free trial... COMMAND FUNCTIONS and MAGICGRADE WORKFLOW BLUEPRINT"

## Overview

**MagicGrade** (by MrAlexTech) is a DaVinci Resolve workflow tool/plugin that maps a structured 4-step grading process to **F-keys (F1-F4)** for speed and consistency. This post shows the workflow blueprint.

> **Link:** https://magic-grade.com/summyd (7-day free trial)

---

## The 4-Step MagicGrade Workflow

| Key | Step | Name | Focus |
|-----|------|------|-------|
| **F1** | **01** | **ADJUSTMENTS** | Primary balance, exposure, contrast — "Tone Curve" |
| **F2** | **02** | **COLOR PALETTE** | Hue shifts, color harmony — "Color Palette HDS" |
| **F3** | **03** | **SPLIT TONE / CONTRAST** | Gain/Lift split, contrast shaping — "Split Tone Contrast" |
| **F4** | **04** | **TEXTURE / SATURATION / DENSITY** | Grain, halation, saturation, density — "Texture Saturation Density" |

### Golden Settings (Modifier)
| Key | Function |
|-----|----------|
| **+ALT** | **BALANCE** — Golden settings for overall balance |

---

## Detailed Step Breakdown

### F1 — ADJUSTMENTS (Tone Curve / Primary)
**Goal:** Technical balance — clean, neutral, proper exposure
- **Lift/Gamma/Gain** or **Linear Gain (Luma Mix 0)**
- **Contrast / Pivot** (0.335)
- **Tone Curve** — Master RGB for film-like toe/shoulder
- **White Balance** — Parade RGB aligned, Vectorscope centered
- **Scopes:** Waveform Y, Parade RGB, Vectorscope

### F2 — COLOR PALETTE (Hue Harmony)
**Goal:** Establish color identity — cohesive palette
- **Hue vs Hue** — Shift hues to harmonious scheme (Teal/Orange, Analogous, etc.)
- **Hue vs Sat** — Selective saturation per hue
- **Color Warper** — Visual palette manipulation
- **HDS** = Hue, Density, Saturation (MagicGrade terminology)

### F3 — SPLIT TONE / CONTRAST
**Goal:** Creative separation — depth via highlight/shadow divergence
- **Gain (Highlights):** Warm push (30-40°, +0.1-0.2)
- **Lift (Shadows):** Cool push (200-220°, +0.05-0.15)
- **Gamma:** Neutral or slight bias
- **Contrast + Pivot** — Refine separation

### F4 — TEXTURE / SATURATION / DENSITY
**Goal:** Filmic texture, organic feel, density over saturation
- **Film Grain OFX** — Structural grain (Kodak/Fuji)
- **Halation / Glow** — Glow OFX (threshold ~0.9) or Blur + Soft Light
- **Saturation** — Global + Hue vs Sat (density technique: Hue vs Lum down)
- **Density** — Hue vs Luminance curve (subtractive saturation @ulterior_visuals)
- **Vignette** — Subtle power window

---

## Keyboard Mapping (MagicGrade Default)

| Key | Action |
|-----|--------|
| **F1** | Jump to / Create "ADJUSTMENTS" node |
| **F2** | Jump to / Create "COLOR PALETTE" node |
| **F3** | Jump to / Create "SPLIT TONE" node |
| **F4** | Jump to / Create "TEXTURE" node |
| **ALT + (F+F1-F4** | Balance / Golden Settings for that step |
| **CTRL+C/V** | Copy/Paste node grades (standard) |

---

## Node Graph Structure (MagicGrade Template)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MAGICGRADE 4-STEP NODE TREE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Node 00: INPUT CST (Camera Log → DWG Intermediate Linear)                 │
│       │                                                                     │
│       ▼                                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │  NODE 01 │──▶│   NODE 02    │──▶│   NODE 03    │──▶│     NODE 04     │    │
│  │  F1:     │   │  F2: COLOR   │   │  F3: SPLIT   │   │  F4: TEXTURE/   │    │
│  │  ADJUST- │   │  PALETTE     │   │  TONE/       │   │  SATURATION/    │    │
│  │  MENTS   │   │  (Hue Shift) │   │  CONTRAST    │   │  DENSITY        │    │
│  └──────────┘   └──────────────┘   └──────────────┘   └─────────────────┘    │
│       │                                                                     │
│       ▼                                                                     │
│  Node 05: OUTPUT CST (DWG → Rec.709 + Gamut Mapping Saturation)            │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER NODE (Parallel) — SKIN PROTECTION                            │   │
│  │   └── Qualifier: Skin tones → Layer Mixer → Composite over Node 04 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## "Golden Settings" — ALT Modifier

The **+ALT** modifier applies "Golden Settings" — presumably balanced, tested presets for each step:
- **ALT+F1:** Balanced primary (exposure, WB, contrast baseline)
- **ALT+F2:** Harmonious palette (Teal/Orange or project-specific)
- **ALT+F3:** Standard split tone (warm highlights, cool shadows)
- **ALT+F4:** Film texture preset (grain + halation + density)

---

## Why This Workflow Works

| Principle | Application |
|-----------|-------------|
| **Separation of Concerns** | Technical (F1) → Creative Color (F2) → Creative Contrast (F3) → Texture (F4) |
| **Muscle Memory** | F-keys = instant node access, no hunting |
| **Repeatability** | Same 4 steps every project = consistent quality |
| **Client Revisions** | Change F2 palette without touching F1 balance |
| **Shot Matching** | Copy F1 across scene, customize F2-F4 per shot |

---

## Integration with Vault Techniques

| MagicGrade Step | Vault Technique | File |
|-----------------|-----------------|------|
| **F1: Adjustments** | Linear Balance, Luma Mix=0 | `Color Correction Fundamentals/02, 05, 07` |
| **F1: Tone Curve** | Film Curve (Toe/Shoulder) | `Creative Grading & Looks/08` (Mastermotion) |
| **F2: Color Palette** | Complementary (Teal/Orange) | `Creative Grading & Looks/01` (Magimirrai) |
| **F2: Hue vs Hue/Sat** | Hue vs Hue skin protection | `Color Correction Fundamentals/04` |
| **F3: Split Tone** | Gain/Lift split toning | `Creative Grading & Looks/01, 08` |
| **F4: Texture** | Film Grain OFX | `Creative Grading & Looks/08` (Mastermotion) |
| **F4: Halation** | Glow OFX / Blur+Soft Light | `Creative Grading & Looks/03, 09` |
| **F4: Density** | Hue vs Lum subtractive sat | `Creative Grading & Looks/06` (Ulterior Visuals) |
| **Output** | CST + Gamut Mapping | `Color Correction Fundamentals/06` |

---

## Installation / Access

1. Visit: **https://magic-grade.com/summyd**
2. 7-day free trial
3. Install via MagicGrade installer (adds F-key mappings, node templates)
4. Open DaVinci Resolve → MagicGrade panel / Keyboard shortcuts active

---

## Tags

`#davinciresolve` `#magicgrade` `#workflow` `#colorgrading` `#template` `#blueprint` `#fkeys` `#productivity` `#summy_dean` `#mralextech` `#node-structure` `#shot-matching`