---
name: davinci-resolve-white-balance-luma-mix
description: "DaVinci Resolve white balance technique: Luma Mix = 0 + RGB Gain for clean neutral balance."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Correction, White Balance, Luma Mix, Primary Correction]
---

# DaVinci Resolve White Balance — Luma Mix Zero Technique

Learn the **Luma Mix = 0** white balance technique from @rolling.shuttermedia — a fast, scope-driven method using **Primary Wheels → RGB Gain** with **Luma Mix set to 0** for clean, contamination-free white balancing in DaVinci Resolve.

## When to Use
- Quick white balance correction on any log/RAW footage
- Primary balance before creative grading
- Scope-driven neutral verification (Vectorscope + Parade)
- Replacing Temp/Tint with RGB Gain workflow (printer lights style)
- Shot matching across scenes

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Footage with a neutral reference (gray card, white shirt, clouds, etc.)
- Scopes open: **Vectorscope** (with Skin Tone Line), **Parade (RGB)**, **Waveform (Y)**

## How to Run
Execute the node setup in DaVinci Resolve Color page as described in **Procedure**. No external tools required.

## Quick Reference
| Step | Panel | Setting | Action |
|------|-------|---------|--------|
| 1 | Primary Wheels | **Luma Mix** | Set to **0** |
| 2 | Primary Wheels | **Gain** (RGB) | Adjust R/G/B to center Parade + Vectorscope |
| 3 | Vectorscope | Display Qualifier Focus | **ON** + Skin Tone Line **ON** |
| 4 | Parade | RGB | Verify R≈G≈B on neutrals |
| 5 | Waveform | Y | Check exposure (skin ~50-70 IRE) |

## Procedure

### 1. Node Setup — Primary Balance Node
1. Add a **Serial Node** at start of node tree (label: `WB_PRIMARY` or `01_BALANCE`).
2. Open **Primary Wheels** panel (bottom left).
3. **Critical:** Set **Luma Mix = 0** (slider all the way down).
   - This decouples Gain from Lift/Gamma — Gain becomes pure RGB multiplier (printer lights).
   - Prevents Lift/Gamma contamination when adjusting Gain.

### 2. Scope Configuration
| Scope | Settings |
|-------|----------|
| **Vectorscope** | Display Qualifier Focus: **ON** • Skin Tone Line: **ON** • 2x Zoom for precision |
| **Parade (RGB)** | Colorize: **ON** • Look for R≈G≈B alignment on neutral objects |
| **Waveform (Y)** | Colorize: **OFF** (clean luminance) • Video Levels: 64-940 (broadcast) |

### 3. White Balance via RGB Gain (Printer Lights Method)
1. **Identify neutral reference** in frame: gray card, white shirt, concrete, clouds, etc.
2. **Hover qualifier** (eyedropper) over neutral area → Vectorscope trace should center.
3. **Adjust RGB Gain wheels** (not Temp/Tint):
   - **Red Gain** → moves trace horizontally on Parade
   - **Green Gain** → moves trace vertically on Parade
   - **Blue Gain** → fine-tune
4. **Goal:** R, G, B channels **aligned on Parade** + trace **centered on Vectorscope**.
5. **Skin Tone Line check:** Skin should sit on or slightly clockwise of 11° line.

> **Why RGB Gain over Temp/Tint?** Temp/Tint are matrix transforms that can shift hue non-linearly. RGB Gain = pure channel scaling (printer lights) — cleaner, more predictable, matches film timing workflow.

### 4. Verify & Lock
- Toggle node **ON/OFF** (Cmd/Ctrl+D) — image should look neutral, no color cast.
- Check **Waveform**: blacks ~5-10 IRE, skin 50-70 IRE, whites <95 IRE.
- Copy this node to other clips in scene for **shot matching** (adjust per clip).

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Gain adjustments affect shadows/midtones | Luma Mix > 0 | **Set Luma Mix = 0** (critical) |
| Vectorscope trace won't center | Wrong reference point / mixed lighting | Pick cleaner neutral; use Qualifier to isolate |
| Parade channels won't align | Strong color cast / IR pollution | Add **Parallel Node** with Qualifier for problematic regions |
| Skin tones off after balance | Over-correction / no skin protection | Use **Layer Node** later to protect skin (see Skin Tones folder) |
| Clip-to-clip inconsistency | Different lighting per shot | Match Node 01 per clip; creative grade on later nodes |

## Verification
1. **Scopes:** Parade R≈G≈B on neutrals; Vectorscope trace centered; Waveform legal range.
2. **Visual:** Toggle node — no color cast, natural skin, clean whites.
3. **Shot match:** Apply to 3+ clips in same scene — consistent neutrality.

## References
- Source: Instagram @rolling.shuttermedia — "Here how to get the perfect white balance in Davinci Resolve. Also forgot to say turn Lum.Mix to 0" (6 days ago at capture)
- Hashtags: #davinciresolve #colorgrading #videography #tutorials #fyp
- Related: Waqas Qazi "Primary Color Correction Workflow" (Linear + Printer Lights), Joris Hermans "Cinematic Look via Correction"

## Related Skills
- `color-correction-fundamentals` (scopes, linear workflow)
- `skin-tone-workflow` (Layer Node protection after balance)