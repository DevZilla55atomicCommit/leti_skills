---
name: davinci-reel-CzHlwdRo
description: |
  DaVinci Resolve technique extracted from Instagram Reel CzHlwdRoYwn
  Collection: Photography/Videography
  Source: https://www.instagram.com/reel/CzHlwdRoYwn/
  Educational focus: 
version: 1.0.0
category: creative
tags:
  - davinci-resolve
  - color-grading
  - cinematography
  - natural-light
  - composition
  - bokeh
  - shallow-depth-of-field
references:
  - "instagram_reel_id": "CzHlwdRoYwn"
  - "source_url": "https://www.instagram.com/reel/CzHlwdRoYwn/"
  - "collection": "Photography/Videography"
  - "analyzed_at": "2026-07-24T11:23:02.970795"
---

# davinci-reel-CzHlwdRo

## Overview
This skill captures the cinematography and color grading techniques demonstrated in Instagram Reel `CzHlwdRoYwn` from the **Photography/Videography** collection.

## Key Techniques Demonstrated

### Composition & Framing


### Camera & Lens


### Lighting


## DaVinci Resolve Application

### Color Grade Recipe (Golden Hour Cinematic)
```node
Node 1: Primary - Lift/Gamma/Gain for golden hour warmth
  - Lift: +0.05 R, -0.02 B (warm shadows)
  - Gamma: +0.03 R, -0.01 B (midtone warmth)
  - Gain: +0.02 R (highlight warmth)
  - Contrast: +10, Pivot: 0.5
  - Saturation: +15 (greens/golds)

Node 2: Teal-Orange Split Toning (Parallel)
  - Shadows: Hue 200-210 (teal), Saturation 25
  - Highlights: Hue 30-40 (orange/gold), Saturation 35
  - Mix: 40% (Soft Light blend)

Node 3: Soft Contrast + Lifted Shadows (Serial)
  - Custom Curve: S-curve with lifted blacks
  - Black Level: +8 (lifted shadows)
  - Contrast: +5
  - Pivot: 0.45

Node 4: Vignette + Focus Pull (Serial)
  - Circular Power Window on subject
  - Outside: -0.15 exposure, slight blur
  - Inside: +0.05 exposure, sharp
  - Feather: 0.8
```

### PowerGrade Structure
```
├── Node 1: Primary Correction (CST if log)
├── Node 2: Creative Grade (Teal-Orange Split)
├── Node 3: Contrast/Texture (S-Curve + Film Grain)
├── Node 4: Vignette/Focus (Power Window)
└── Node 5: Output Transform (CST to Rec.709)
```

## Lighting Reference
- **Key**: Natural sun (backlight/rim) at 15-30° elevation
- **Fill**: Ambient sky reflection (cool, soft)
- **Ratio**: ~3:1 (high contrast, lifted shadows in grade)
- **Color Temp**: 3500-4500K (warm golden)

## Camera Settings Reference
- **Aperture**: f/1.8-f/2.8 (shallow DOF)
- **Focal Length**: 35-85mm equivalent (portrait to short telephoto)
- **Shutter**: 180° (1/48s at 24fps)
- **Movement**: Static to slow dolly; handheld organic

## Practice Exercises

### Exercise 1: Golden Hour Grade
1. Import any golden hour footage
2. Build the 5-node structure above
3. Match the warm/cool split tone
4. Add film grain overlay

### Exercise 2: Framing Within Frame
1. Find footage with architectural/natural frames
2. Power Window to isolate frame
3. Blur/darken outside, sharpen inside
4. Animate window if frame moves

### Exercise 3: Foreground Depth
1. In Fusion, add leaf/branch elements
2. Track to camera movement
3. Blend with Soft Light, animate subtle parallax

## Related Skills
- `davinci-resolve-golden-hour-grade`
- `davinci-resolve-teal-orange-split-tone`
- `davinci-resolve-power-window-tracking`
- `davinci-resolve-film-grain-workflow`

## Files Generated
- `vision_report.json` - Full frame-by-frame analysis
- `frames/` - Keyframes at 0s, 9.5s, 19s
- `gifs/` - 5s preview GIF
- `transcript/` - Whisper transcription (if speech detected)

## Metadata
- **Reel ID**: CzHlwdRoYwn
- **Collection**: Photography/Videography
- **Source**: https://www.instagram.com/reel/CzHlwdRoYwn/
- **Analyzed**: 2026-07-24T11:23:02.970795
- **Frames Analyzed**: 3
- **Educational Value**: 
