---
name: leica-l-log-workflow
description: "Grade Leica L-Log footage with CST/ACES in DaVinci Resolve."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color, Leica, L-Log, CST, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Leica L-Log Color Space Workflow

## When to Use

Use when grading Leica SL2, SL2-S, SL3 L-Log footage in DaVinci Resolve 21.1+. Native Leica L-Log support added in v21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 7:14-7:36
- **Resolve Page:** Color

## Camera Models
- Leica SL2 (L-Log)
- Leica SL2-S (L-Log)
- Leica SL3 (L-Log)
- Leica Q2/Q3 (L-Log via firmware)

## Workflow Options
### Option A: CST Node
1. Add Color Space Transform node
2. Input Color Space: Leica L-Log
3. Input Gamma: Leica L-Log
4. Output Color Space: Rec.709 / Rec.2020 / DCI-P3
5. Output Gamma: Rec.709 / ST.2084 / HLG

### Option B: RCM
1. Project Settings → Color Management → RCM
2. Input Color Space: Leica L-Log (per clip/timeline)
3. Timeline Color Space: DaVinci Wide Gamut / Rec.2020
4. Output Color Space: Target display

### Option C: ACES
1. Project Settings → Color Management → ACES 2.0
2. IDT: Leica L-Log
3. ODT: Target display

## Node Graph Template
```
Node 1: CST (Leica L-Log → DWG/Rec.2020)
Node 2: Primary Balance
Node 3: Creative Grade
Node 4: CST (DWG → Output)
```

## Key Characteristics
- Log curve: Leica logarithmic encoding
- Gamut: Leica Wide Gamut (near Rec.2020)
- Highlight latitude: ~13 stops
- Color science: Leica natural skin tones

## Tips
- Leica L-Log preserves highlight detail well
- Skin tones render naturally with minimal correction
- Match well with ARRI LogC workflows
- Use Leica LUTs for creative starting points

## Cross-References
- **Related Skills:** `cst-node-workflow`, `aces-workflow`, `leica-lut-integration`
- **Tags:** `leica`, `l-log`, `cst`, `color-management`, `v21.1`
- **Collection:** `camera-workflows`