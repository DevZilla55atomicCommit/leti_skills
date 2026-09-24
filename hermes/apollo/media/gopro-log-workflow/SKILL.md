---
name: gopro-log-workflow
description: "Grade GoPro Log footage with CST/ACES in DaVinci Resolve."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color, GoPro, Log, CST, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# GoPro Log Color Space Workflow

## When to Use

Use when grading GoPro Hero 10/11/12/13 Log footage in DaVinci Resolve 21.1+. Native GoPro Log support added in v21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 7:14-7:36
- **Resolve Page:** Color

## Camera Models
- GoPro Hero 10 Black (GP-Log)
- GoPro Hero 11 Black (GP-Log)
- GoPro Hero 12 Black (GP-Log)
- GoPro Hero 13 Black (GP-Log)

## Workflow Options
### Option A: CST Node (Recommended)
1. Add Color Space Transform node
2. Input Color Space: GoPro Log
3. Input Gamma: GoPro Log
4. Output Color Space: Rec.709 / Rec.2020 / DCI-P3
5. Output Gamma: Rec.709 / ST.2084 (PQ) / HLG

### Option B: RCM (Resolve Color Management)
1. Project Settings → Color Management → RCM
2. Input Color Space: GoPro Log (per clip or timeline)
3. Timeline Color Space: DaVinci Wide Gamut / Rec.2020
4. Output Color Space: Rec.709 / P3 / Rec.2020

### Option C: ACES
1. Project Settings → Color Management → ACES 2.0
2. IDT: GoPro Log (auto-detect or manual)
3. ODT: Target display (sRGB, Rec.709, P3, Rec.2020)

## Node Graph Template (Serial)
```
Node 1: CST (GoPro Log → DWG/Rec.2020)
Node 2: Primary Balance (Exposure, Contrast, WB)
Node 3: Creative Grade
Node 4: CST (DWG → Output Display)
```

## Key Characteristics
- Log curve: Custom GoPro logarithmic encoding
- Gamut: GoPro Wide Gamut (near Rec.2020)
- Highlight rolloff: Gradual, protect highlights
- Noise floor: Higher in shadows (small sensor)

## Tips
- Expose to the right (ETTR) for cleaner shadows
- Use Noise Reduction (spatial/temporal) on Node 1
- Highlight reconstruction helps blown skies
- Match with other cams using Color Match

## Cross-References
- **Related Skills:** `cst-node-workflow`, `aces-workflow`, `rcm-setup`
- **Tags:** `gopro`, `gopro-log`, `cst`, `color-management`, `v21.1`
- **Collection:** `camera-workflows`