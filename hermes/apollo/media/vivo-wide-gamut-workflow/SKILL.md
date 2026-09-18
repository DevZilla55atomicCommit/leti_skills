---
name: vivo-wide-gamut-workflow
description: "Grade Vivo Wide Gamut / Log footage with CST/ACES."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color, Vivo, Wide Gamut, Log, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Vivo Wide Gamut / Log Color Space Workflow

## When to Use

Use when grading Vivo X100 Pro, X100 Ultra footage in DaVinci Resolve 21.1+. Native Vivo Wide Gamut and Log support added in v21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 7:14-7:36
- **Resolve Page:** Color

## Camera Models
- Vivo X100 Pro (Vivo Wide Gamut / Log)
- Vivo X100 Ultra (Vivo Wide Gamut / Log)
- Vivo X90 Pro+ (similar pipeline)

## Workflow Options
### Option A: CST Node
1. Add Color Space Transform node
2. Input Color Space: Vivo Wide Gamut
3. Input Gamma: Vivo Log
4. Output Color Space: Rec.709 / Rec.2020 / DCI-P3
5. Output Gamma: Rec.709 / ST.2084 / HLG

### Option B: RCM
1. Project Settings → Color Management → RCM
2. Input Color Space: Vivo Wide Gamut / Vivo Log
3. Timeline Color Space: DaVinci Wide Gamut / Rec.2020
4. Output Color Space: Target display

### Option C: ACES
1. Project Settings → Color Management → ACES 2.0
2. IDT: Vivo Wide Gamut / Vivo Log
3. ODT: Target display

## Key Characteristics
- Wide Gamut: Exceeds Rec.2020 coverage
- Log curve: Optimized for mobile sensor DR
- Computational photography integration
- 1-inch sensor (X100 Ultra) → better DR

## Tips
- Vivo Log preserves highlights aggressively
- Wide Gamut needs careful gamut compression
- Multi-frame processing may affect noise structure
- Test with Zeiss T* coating color rendering

## Cross-References
- **Related Skills:** `cst-node-workflow`, `aces-workflow`, `mobile-cinema-workflow`
- **Tags:** `vivo`, `wide-gamut`, `vivo-log`, `cst`, `color-management`, `v21.1`
- **Collection:** `camera-workflows`