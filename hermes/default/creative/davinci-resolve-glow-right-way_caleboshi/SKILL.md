---
name: davinci-resolve-glow-right-way_caleboshi
category: creative
description: "Add glow/halation the right way in DaVinci Resolve — Glow OFX in Add composite mode on log/Scene-Referred footage before CST for optical accuracy"
tags:
  - davinci-resolve
  - color-grading
  - glow
  - halation
  - bloom
  - add-mode
  - cinematic
  - log-footage
  - scene-referred
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DJc15zpvqoe/"
creator: "@caleboshi"
vault_file: "Creative Grading & Looks/53-Glow-Right-Way_caleboshi_Add-Mode-Log-Space.md"
---

# Add Glow the Right Way in DaVinci Resolve

## Overview
Correct glow/halation workflow using Glow OFX in **Add composite mode** on **log/Scene-Referred footage** before CST/Output Transform — mimics optical lens bloom physics.

## When to Use
- Any cinematic grade wanting natural highlight bloom
- Practical lights (lamps, neon, sun, reflections)
- Film emulation base
- **Not for**: Quick social content (use Soft Light composite instead)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Log footage or Color Managed (DWG timeline)
- Glow OFX (Resolve FX Light)
- Basic node graph understanding

## Core Principle

> **Real light ADDS. Screen/Normal multiplies. Add mode = optical truth.**

## Node Structure

### Standard (Non-Color-Managed)
```
Node 01: Input (Log: S-Log3, LogC, BRAW, etc.)
Node 02: [GLOW OFX] — Composite: ADD, Log Space
Node 03: CST (Log → Rec.709 / DWG)
Node 04: Primary / Creative Grade
Node 05: Global Polish
```

### Color Managed (DWG Timeline)
```
Node 01: (Auto Input → DWG)
Node 02: [GLOW OFX] — In DWG (Scene-Referred)
Node 03: Creative Grade
Node 04: (Auto DWG → Output)
```

## Step-by-Step Procedure

### 1. Place Glow on Log Footage (Node 02)
- Effects → Resolve FX Light → Glow
- Serial node, BEFORE any CST/Output Transform

### 2. Critical Settings
| Parameter | Value | Reason |
|-----------|-------|--------|
| **Composite Type** | **Add** | Optical accuracy — light adds |
| **Shine Threshold** | 10-30% | Catch speculars, ignore midtones |
| **Spread** | 50-200 | Bloom radius (higher = halation) |
| **Intensity/Global Blend** | 0.1-0.5 | Subtle = cinematic |
| **Color** | Warm/White | Match light source |

### 3. Verify on Scopes
- **Waveform**: Highlights may exceed 1.0 (Add mode) — OK if CST after handles rolloff
- **Parade RGB**: Check glow color balance
- **If hard clipping**: Reduce Intensity or raise Threshold

### 4. CST After Glow (Node 03)
- Color Space Transform: Log → Rec.709 / DWG
- Glow now properly mapped to display space

## Parameter Presets

| Look | Threshold | Spread | Intensity | Color | Use Case |
|------|-----------|--------|-----------|-------|----------|
| **Subtle Lens Bloom** | 25% | 60 | 0.15 | Warm | Narrative, drama |
| **Cinematic Halation** | 15% | 150 | 0.3 | Warm | Film emulation |
| **Strong Practical** | 10% | 200 | 0.4 | Match source | Neon, lamps, sun |
| **Dreamy/Ethereal** | 20% | 300 | 0.25 | Cool/White | Music video, fantasy |
| **Anamorphic Style** | 20% | 100 (H) | 0.2 | Blue streak | Anamorphic sim |

## Advanced: Selective Glow (Power Window)
1. Power Window on practical (lamp, neon, sun)
2. Track window to light
3. Glow OFX inside window only
4. Multiple windows = multiple glows

## Advanced: Dual Glow (Bloom + Halation)
```
Node 02a: Glow — Spread 40, Intensity 0.15, Add (tight bloom)
Node 02b: Glow — Spread 180, Intensity 0.1, Add (wide halation)
```
- Tight bloom on speculars
- Wide halation on bright regions
- Combined = filmic depth

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Glow after LUT | Digital, baked look | Glow BEFORE CST/Output |
| Composite = Screen | Foggy, low contrast | **Composite = Add** |
| On Rec.709 footage | Blown highlights, wrong ratios | Use log or DWG space |
| Threshold too high | Only brightest specs glow | Lower to 10-30% |
| No glow color | White fringe | Tint to match source |
| Intensity too high | Nuclear bloom | Start 0.1, creep up |

## Pro Tips

- **Log space essential** — Scene-referred = optical accuracy
- **Add mode = physics** — Light adds, doesn't multiply
- **Track practicals** — Window + track = pro level
- **Subtlety wins** — If you notice the glow, it's too much
- **Pair with halation** — Glow + halation = full film bloom

## Related Skills
- `davinci-resolve-cinematic-glow_mansourmelouli` — Soft Light composite alternative
- `davinci-resolve-glow-halation-cinematic_caleboshi` — Multi-layer glow/halation
- `davinci-resolve-promist-slog3-dreamy` — Pro Mist diffusion + glow
- `davinci-resolve-cinematic-haze-effect` — Native haze alternative

## References
- Source: @caleboshi Instagram Reel (Apr 1, 2025)
- Hashtags: #davinciresolve #colorgrading #glow #halation #cinematic
- Engagement: 1,026 likes, 51 comments
- Community: "Comment Log to download footage" — practice pack