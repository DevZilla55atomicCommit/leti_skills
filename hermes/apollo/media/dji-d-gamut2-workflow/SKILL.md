---
name: dji-d-gamut2-workflow
description: "Grade DJI D-Gamut 2 / D-Log2 footage with CST/ACES."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color, DJI, D-Gamut, D-Log2, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# DJI D-Gamut 2 / D-Log2 Color Space Workflow

## When to Use

Use when grading DJI Ronin 4D, Inspire 3, Mavic 3 Pro footage in DaVinci Resolve 21.1+. Native DJI D-Gamut 2 and D-Log2 support added in v21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 7:14-7:36
- **Resolve Page:** Color

## Camera Models
- DJI Ronin 4D (D-Gamut 2 / D-Log2)
- DJI Inspire 3 (D-Gamut 2 / D-Log2)
- DJI Mavic 3 Pro (D-Log M → similar)
- DJI Air 2S/3 (D-Log)

## Workflow Options
### Option A: CST Node
1. Add Color Space Transform node
2. Input Color Space: DJI D-Gamut 2
3. Input Gamma: DJI D-Log2
4. Output Color Space: Rec.709 / Rec.2020 / DCI-P3
5. Output Gamma: Rec.709 / ST.2084 / HLG

### Option B: RCM
1. Project Settings → Color Management → RCM
2. Input Color Space: DJI D-Gamut 2 / D-Log2
3. Timeline Color Space: DaVinci Wide Gamut / Rec.2020
4. Output Color Space: Target display

### Option C: ACES
1. Project Settings → Color Management → ACES 2.0
2. IDT: DJI D-Gamut 2 / D-Log2
3. ODT: Target display

## Key Characteristics
- D-Gamut 2: Wide gamut exceeding Rec.2020
- D-Log2: Improved log curve vs original D-Log
- Highlight latitude: ~14+ stops (Ronin 4D)
- Dual native ISO: 800/5000 (Ronin 4D)

## Tips
- D-Gamut 2 requires careful gamut mapping to Rec.2020
- Use Highlight Recovery for clipped specular highlights
- Ronin 4D raw → D-Gamut 2 pipeline preserves maximum data
- Match multiple DJI cams via Color Match

## Cross-References
- **Related Skills:** `cst-node-workflow`, `aces-workflow`, `dji-raw-workflow`
- **Tags:** `dji`, `d-gamut2`, `d-log2`, `cst`, `color-management`, `v21.1`
- **Collection:** `camera-workflows`