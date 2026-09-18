---
name: davinci-reel-AQN40Vz0
description: |
  DaVinci Resolve technique extracted from Instagram Reel AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U
  Collection: Photography/Videography
  Source: https://www.instagram.com/p/CUdBRuVDhPX/
  Educational focus: High - demonstrates natural light cinematography, composition techniques, and cinematic color palette achievable in DaVinci Resolve
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
  - "instagram_reel_id": "AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U"
  - "source_url": "https://www.instagram.com/p/CUdBRuVDhPX/"
  - "collection": "Photography/Videography"
  - "analyzed_at": "2025-07-22T17:25:00Z"
---

# davinci-reel-AQN40Vz0

## Overview
This skill captures the cinematography and color grading techniques demonstrated in Instagram Reel `AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U` from the **Photography/Videography** collection. The reel showcases natural light cinematography during golden hour with shallow depth of field, framing within frames, and a warm cinematic color palette.

## Key Techniques Demonstrated

### Composition & Framing
- **Framing within a frame**
- **Shallow depth of field**
- **Foreground masking**

### Camera & Lens
- **Shallow depth of field**
- **Macro photography style**
- **Bokeh effect**

### Lighting
- **Natural light utilization**
- **Golden hour lighting**

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

## Composition Techniques for Resolve

### Framing Within Frame
- Use Power Windows to emphasize architectural/natural frames
- Track window to subject if camera moves
- Blur outside frame slightly for depth

### Foreground Masking
- Add foreground elements in Fusion (leaves, branches)
- Animate subtle parallax for depth
- Blend with Soft Light at 30-40% opacity

### Golden Hour Workflow
1. **CST**: Input log → DaVinci WG/Intermediate
2. **Primary**: Warm lift, cool shadows (teal-orange split)
3. **Skin Tone**: Protect with qualifier if people present
4. **Grain**: Add 35mm film grain (Kodak 2383 LUT or built-in)
5. **Output**: CST to Rec.709

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
- **Reel ID**: AQN40Vz04BypuiVuC2ws5KvNxmzyDnSdQu-WKlVj1sA2ktGpkbl6sUbW6x9OPYhVOIXsh78Gsbb4WMm-J4oQvCcAqargq6Vb72eog5U
- **Collection**: Photography/Videography
- **Source**: https://www.instagram.com/p/CUdBRuVDhPX/
- **Analyzed**: 2025-07-22T17:25:00Z
- **Frames Analyzed**: 3
- **Educational Value**: High - demonstrates natural light cinematography, composition techniques, and cinematic color palette achievable in DaVinci Resolve
