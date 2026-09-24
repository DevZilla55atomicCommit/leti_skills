---
name: davinci-resolve-simple-4-step-workflow
description: "Simple 4-step color workflow in DaVinci Resolve — CST conversion, WB/exposure fix, contrast matching, minimal styling — 'Most footage doesn't need heavy styling, just balance.'"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Workflow, Simple, 4-Step, Color Balance]
    source_url: "https://www.instagram.com/p/DVCKFMXEoxQ/"
    source_creator: "@taylormadevisuals"
    source_date: "2025-02-21"
    vault_category: "Cinematic Grading Workflows"
    skill_level: "Beginner to Intermediate"
    tags: [Simple Workflow, 4-Step, CST, White Balance, Exposure, Contrast, Shot Matching, Minimal Grading, Taylor Made Visuals]
---

# DaVinci Resolve: Simple 4-Step Color Workflow — @taylormadevisuals

**Source:** [@taylormadevisuals Instagram Post](https://www.instagram.com/p/DVCKFMXEoxQ/) — "Day 5/30. This is how I actually color inside Resolve."

## Technique Overview

A simple, repeatable 4-step color workflow that prioritizes **proper balance over heavy styling**. Most footage doesn't need complex grading — it just needs to be balanced correctly.

> *"A lot of footage doesn't need heavy styling. It just needs to be balanced properly. If your footage still looks 'off,' you probably skipped the fixing part."* — @taylormadevisuals

---

## 4-Step Workflow

### Step 1: Convert Log → Rec.709 with CST
- **Node 01:** Color Space Transform
- **Input:** Camera Log (S-Log3, BRAW, LogC, V-Log, etc.)
- **Output:** Rec.709 Gamma 2.4
- **Gamut Mapping:** Enabled (Saturation method)

### Step 2: Fix White Balance + Exposure
- **Node 02:** Primary Balance
- **White Balance:** Temp/Tint or Linear Gain (Luma Mix=0)
- **Exposure:** Gain + Pivot (0.335) for photometric accuracy
- **Scopes:** Parade RGB + Vectorscope verification

### Step 3: Clean Up Contrast + Match Shots
- **Node 03:** Contrast + Shot Matching
- **Contrast:** Gain/Pivot or Custom Curves (S-curve)
- **Shot Match:** Copy Node 02-03 across scene, tweak per shot
- **Key:** Consistency across timeline

### Step 4: Stop There (Most of the Time)
- **No creative LUT**
- **No heavy stylization**
- **No split toning**
- **Deliver clean, balanced footage**

---

## When to Add Styling (Step 5+)

| Scenario | Addition |
|----------|----------|
| **Client requests look** | Add creative node(s) after balance |
| **Narrative/mood** | Split tone, film emulation, density |
| **Brand colors** | Hue shifts, color warper |
| **Artistic intent** | Full creative grade |

---

## Node Structure

```
Node 01: CST (Log → Rec.709)
Node 02: WB + Exposure (Primary)
Node 03: Contrast + Shot Match
Node 04: (Optional) Creative Look
```

---

## Core Philosophy

| Principle | Application |
|-----------|-------------|
| **Fix before style** | Balance → Contrast → Match → Style |
| **Less is more** | 80% of footage needs only Steps 1-3 |
| **Scopes don't lie** | Parade/Vectorscope over eye |
| **Consistency > Creativity** | Shot matching is the real skill |

---

## Pro Tips

1. **Save as PowerGrade:** "4-STEP_BALANCE" template
2. **Group Pre-Clip:** Apply CST to entire timeline
3. **Reference Stills:** Grab still of hero shot, match to it
4. **Client Review:** Show balanced version first, then styled

---

## Related Techniques

- `davinci-resolve-cinematic-grading-3-mistakes` — 3 mistakes: node structure, exposure, color management
- `davinci-resolve-white-balance-3-methods` — WB: Temp/Tint, Linear, Gray Card
- `davinci-resolve-cst-gamut-mapping-color-spill` — CST Gamut Mapping for spill control

---

## Tags

`#davinciresolve` `#colorgrading` `#workflow` `#simple` `#4-step` `#cst` `#white-balance` `#exposure` `#contrast` `#shot-matching` `#minimal-grading` `#taylormadevisuals`