---
name: davinci-resolve-automotive-cinematic-grade
description: "DaVinci Resolve automotive cinematic grading: CST end-node, power window tracking, free LUT/PowerGrade from @bwd_motorsports."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Automotive, Cinematic, Color Grading, Power Window Tracking, CST, LUT, PowerGrade]
---

# DaVinci Resolve — Automotive Cinematic Grading (BWD Motorsports)

Learn the **automotive cinematic grading workflow** from @bwd_motorsports (Ben @ BWD Motorsports) — featuring CST at end node, circular power window tracking for vehicles, and a free Cinematic LUT + PowerGrade.

## When to Use
- Automotive/motorsports footage color grading
- Vehicle tracking with power windows (circular masks)
- Cinematic look for car commercials, racing, automotive content
- CST-based color management pipeline (CST at end node)
- Free LUT/PowerGrade application for consistent looks

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Automotive footage (log or RAW preferred: S-Log3, BRAW, LogC, etc.)
- Basic power window tracking familiarity

## How to Run
Build the node tree in DaVinci Resolve Color page as described in **Procedure**. Apply free LUT/PowerGrade from creator.

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 | Primary Balance | WB + Exposure (Luma Mix=0) |
| 2 | Node 02 | Power Window | Circular mask on vehicle, track |
| 3 | Node 03 | Vehicle Grade | Isolated vehicle enhancement |
| 4 | Node 04 | Background | Sky/environment grade |
| 5 | CST (End) | Color Space Transform | Log → Rec.709 (end node) |
| 6 | Output | LUT/PowerGrade | Free Cinematic LUT + PG |

## Procedure

### 1. Node 01 — Primary Balance (Base Correction)
- Serial Node, label: `BASE`
- Luma Mix = 0, RGB Gain for white balance
- Parade RGB aligned, Vectorscope centered
- Sets clean foundation before isolation

### 2. Node 02 — Power Window Tracking (Vehicle Isolation)
- Serial Node, label: `VEHICLE_MASK`
- **Power Window → Circle/Ellipse** on vehicle
- **Tracker**: Track forward/backward (vehicle moves)
- Softness: 0.2-0.4 for natural edge
- **Key Output ON** — verify clean vehicle isolation
- *Comment insight: "circular mask you applied track the car"*

### 3. Node 03 — Vehicle Grade (Isolated Enhancement)
- Serial Node (or Layer from Node 02), label: `VEHICLE_GRADE`
- Key Input ← Node 02 Alpha
- Enhance vehicle: saturation, contrast, color pop
- Paint/bodywork: Hue vs Hue for brand colors
- Reflections: Manage with curves/highlights

### 4. Node 04 — Background/Environment Grade
- Serial Node, label: `BG_GRADE`
- Key Input ← Node 02 Alpha, **Invert ON**
- Grade sky, track, environment separately
- Sky: Teal push, gradient for drama
- Track/asphalt: Cool, desaturated

### 5. CST Node (End Node) — Color Space Transform
- **Position: LAST NODE** (after all grading)
- Input: [Camera Log] (S-Log3, BRAW, LogC, etc.)
- Output: Rec.709 Gamma 2.4 (or P3/ST2084 for HDR)
- Tone Mapping: DaVinci (or None if graded in wide gamut)
- *Comment insight: "CCT - end node!!!!!"*

### 6. Free Cinematic LUT + PowerGrade
- Creator provides: **Free Cinematic LUT** + **PowerGrade**
- Apply LUT before CST or within PowerGrade
- PowerGrade includes: Node template, tracking setup, CST config
- *Caption: "Free Cinematic LUT and Powergrade. Built from the ground up"*

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Vehicle mask drifts | Tracker loses lock | Manual keyframes; increase search area; use planar tracker (Studio) |
| CST clips highlights | Tone Mapping=None in wide gamut | Use DaVinci Tone Mapping; or grade in DWG→CST |
| LUT looks wrong | Applied after CST / wrong input space | LUT before CST; match LUT input space |
| Free version lacks tracker | Planar/3D tracker Studio only | Use point tracker + manual keyframes (Free) |
| Sky/vehicle spill | Softness too high/low | Adjust Power Window softness; refine with curves |

## Verification
1. Scrub timeline: Vehicle mask tracks perfectly
2. Toggle Node 02 Key Output: Clean vehicle isolation
3. CST last: Scopes legal (Waveform 64-940)
4. LUT/PowerGrade applied: Consistent look across clips
5. Export: Vehicle pops, sky dramatic, cinematic feel

## References
- Source: Instagram @bwd_motorsports (Ben @ BWD Motorsports)
- Post: Automotive cinematic grading with circular mask tracking
- Comments: "CCT - end node!!!!!", "circular mask you applied track the car", "Free Cinematic LUT and Powergrade"
- Hashtags: Automotive, cinematography, color grading, LUT, PowerGrade
- Free assets: Cinematic LUT + PowerGrade download (link in bio/profile)

## Related Skills
- `davinci-resolve-masking-power-masking` (Power Window tracking)
- `davinci-resolve-cinematic-grading-3-mistakes` (CST pipeline)
- `davinci-resolve-white-balance-luma-mix` (Base balance)