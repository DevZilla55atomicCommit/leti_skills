---
name: atmospheric-haze-cinematic-glow
description: Atmospheric haze, cinematic glow, halation, and diffusion effects using Glow OFX, Blur+Soft Light, Color Mixer, and natural light techniques. For aerial, landscape, golden hour, and dreamy aesthetics.
trigger: User wants to add atmospheric haze, cinematic glow, halation, bloom, or dreamy diffusion effects to footage.
category: davinci-resolve/color-grading
tags: [atmospheric, haze, cinematic, glow, halation, diffusion, blur, soft-light, color-mixer, natural-light, aerial, golden-hour, dreamy]
steps:
  - name: Atmospheric Haze & Cinematic Grading (C_s_3BrqhAl)
    description: Lower contrast + Power Window on land + Glow/Blur for mist + Color Wheels for teal shadows/warm highlights + Midtone Detail
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Power Window, Color Mixer]
    parameters:
      Contrast: "Lowered"
      Saturation: "Reduced"
      Midtone_Detail: "Increased"
      Tint: "Teal/Blue shift"
    steps:
      - Add a primary node to balance exposure and lower the overall contrast
      - Apply a Power Window to the landmass to slightly increase saturation locally
      - Use the Glow effect or a slight Blur node to create a misty/atmospheric look
      - Shift shadows toward blue/teal and highlights toward a warm or neutral tone using Color Wheels
      - Adjust the Midtone Detail to bring back texture to the water and trees
    difficulty: intermediate
    video_id: C_s_3BrqhAl
    tags: [cinematic, aerial, colorgrading, haze]

  - name: Natural Light Glow & Soft Diffusion Effect (C95GBSmxyzX)
    description: Glow OFX on highlights + Qualifier mask to protect shadows/midtones + exposure balance
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Exposure, Color Correction, Soft Glow/Glow, Qualifier Mask]
    parameters:
      Glow_Threshold: "0.4"
      Glow_Radius: "0.50"
      Opacity: "0.3"
      Highlights_Gain: "+1.2"
    steps:
      - Import footage and go to the Color page
      - Add a serial node to balance exposure and white balance
      - Add a second serial node for effects and apply the Glow effect or use the Glow node
      - Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger the effect
      - Increase the Radius and Opacity to create a dreamy bloom around light sources
      - Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows or midtones
    difficulty: intermediate
    video_id: C95GBSmxyzX
    tags: [cinematic, natural light, glow, color grading]

  - name: Pro Mist / Black Pro Mist Filter Look for S-Log3 (C7-dN8GB)
    description: Pro Mist diffusion filter emulation using Glow + Blur + Soft Light composite
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Pro Mist Look, S-Log3 Workflow]
    parameters:
      param1: "Pro Mist filter emulation for S-Log3 footage"
    steps:
      - Apply S-Log3 to Rec.709 CST
      - Add serial node with Glow OFX
      - Add Blur node in Soft Light composite mode
      - Adjust for halation/bloom on highlights
    difficulty: intermediate
    video_id: C7-dN8GB
    tags: [Pro Mist, Black Pro Mist, S-Log3, diffusion, halation]

  - name: Free Halation Effect (C9i31Ifx9uB)
    description: Native halation emulation without plugins - Glow on highlights + color shift
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Halation Effect]
    parameters:
      param1: "Halation emulation using native tools"
    steps:
      - Isolate highlights with Qualifier or Luma Key
      - Apply Glow with red/orange tint
      - Blur and composite in Add/Screen mode
      - Mask to protect midtones
    difficulty: intermediate
    video_id: C9i31Ifx9uB
    tags: [Halation, Free, Native, DaVinci Resolve]

  - name: Cinematic Glow/Halation Proper Way (C7eXh5oI, C7Rx1nGJ)
    description: Native Glow OFX + Soft Light composite for proper highlight rolloff
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Glow OFX, Soft Light]
    parameters:
      param1: "Proper glow/halation using native Glow OFX and Soft Light"
    steps:
      - Add Glow OFX node at end of chain
      - Set threshold for highlights only
      - Add Blur node, set composite mode to Soft Light
      - Blend for natural highlight bloom
    difficulty: intermediate
    video_id: C7eXh5oI
    tags: [Glow, Halation, Cinematic, Native OFX]

  - name: Day to Night Transition (DMHHqfYSS97)
    description: Gradient mask + exposure drop + color temp shift for day-to-night
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Day to Night Transition]
    parameters:
      param1: "Day to night grading transition"
    steps:
      - Apply primary grade for day look
      - Add serial node with gradient Power Window (top to bottom)
      - Lower exposure significantly on masked area
      - Shift temperature to blue (moonlight)
      - Add subtle glow on practical lights
    difficulty: intermediate
    video_id: DMHHqfYSS97
    tags: [Day to Night, Transition, Grading]

  - name: Low Contrast Dreamy Look (C13opd8S)
    description: Low contrast + lifted blacks + subtle glow for dreamy aesthetic
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Low Contrast Dreamy Look]
    parameters:
      param1: "Low contrast dreamy look shortcut"
    steps:
      - Lift blacks (lift wheel up)
      - Lower contrast/pivot
      - Reduce saturation slightly
      - Add subtle Glow on highlights
      - Cool shadows, warm highlights
    difficulty: beginner
    video_id: C13opd8S
    tags: [Low Contrast, Dreamy, Shortcut, @caleboshi]
parameters:
  - name: Contrast
    description: Overall contrast level - lowered for atmospheric look
  - name: Saturation
    description: Reduced for muted/film-like aesthetic
  - name: Midtone_Detail
    description: Increased to restore texture after contrast reduction
  - name: Tint
    description: Teal/blue shift in shadows, warm in highlights
  - name: Glow_Threshold
    description: Luminance threshold for glow activation (0.3-0.5)
  - name: Glow_Radius
    description: Spread/bloom radius of glow effect
  - name: Opacity
    description: Glow intensity/blend opacity
  - name: Highlights_Gain
    description: Boost to highlights before glow for stronger bloom
tags: [atmospheric, haze, cinematic, glow, halation, diffusion, blur, soft-light, color-mixer, natural-light, aerial, golden-hour, dreamy, pro-mist, halation, day-to-night]
---

# Atmospheric Haze, Cinematic Glow & Diffusion Effects

**Atmospheric effects** for aerial, landscape, golden hour, and dreamy aesthetics. Native DaVinci Resolve tools: Glow OFX, Blur+Soft Light, Color Mixer, Power Windows.

## Techniques Included

### 1. Atmospheric Haze & Cinematic Grading (C_s_3BrqhAl)
**Aerial/landscape haze with localized saturation**

- **Node 1**: Primary - lower contrast, balance exposure
- **Node 2**: Power Window on landmass - boost saturation locally
- **Node 3**: Glow/Blur - misty atmospheric veil
- **Node 4**: Color Wheels - teal shadows, warm/neutral highlights
- **Node 5**: Midtone Detail - restore water/tree texture

**Key Settings**: Contrast ↓, Saturation ↓, Midtone Detail ↑, Teal Shadows

### 2. Natural Light Glow & Soft Diffusion (C95GBSmxyzX)
**Sunbeam bloom with shadow protection**

- **Node 1**: Exposure/WB balance
- **Node 2**: Glow OFX - Threshold 0.4, Radius 0.5, Opacity 0.3
- **Node 3**: Highlights Gain +1.2 (pre-glow boost)
- **Node 4**: Qualifier Mask - protect shadows/midtones from glow

**Key Settings**: Threshold 0.4, Radius 0.5, Opacity 0.3, Highlights +1.2

### 3. Pro Mist / Black Pro Mist Filter Look (C7-dN8GB)
**Diffusion filter emulation for S-Log3**

```
S-Log3 CST → Node 1: Glow OFX → Node 2: Blur (Soft Light composite) → Grade
```

- **Glow**: Threshold ~0.5, small radius
- **Blur**: Radius 5-10, Composite: Soft Light, Opacity 15-25%
- **Result**: Halation on highlights, softened contrast, bloom

### 4. Free Halation Effect (C9i31Ifx9uB)
**Native halation without plugins**

1. **Isolate Highlights**: Qualifier (Luma > 0.85) or Luma Key
2. **Colorize**: Tint toward red/orange (halation color)
3. **Blur**: Radius 10-20, Composite: Add/Screen
4. **Protect**: Mask midtones, blend 20-30%

### 5. Cinematic Glow/Halation Proper Way (C7eXh5oI, C7Rx1nGJ)
**Glow OFX + Soft Light composite (Caleboshi method)**

```
Grade Chain → Glow OFX (threshold 0.7, radius 0.3) 
         → Blur (Soft Light, 20% opacity)
```

### 6. Day to Night Transition (DMHHqfYSS97)
**Gradient mask + exposure + temp shift**

- **Node 1**: Day grade
- **Node 2**: Gradient Power Window (top→bottom)
- **Node 3**: Exposure -2 to -3 on mask
- **Node 4**: Temp → Blue (4000K), Tint → Magenta
- **Node 5**: Glow on practical lights (windows, lamps)

### 7. Low Contrast Dreamy Look (C13opd8S)
**@caleboshi shortcut**

- **Lift**: Raise blacks (Lift wheel up)
- **Contrast**: Lower pivot/contrast
- **Saturation**: -10 to -20%
- **Glow**: Subtle on highlights
- **Split Tone**: Cool shadows, warm highlights

## Glow OFX Settings Reference

| Look | Threshold | Radius | Opacity | Composite |
|------|-----------|--------|---------|-----------|
| **Subtle Bloom** | 0.7 | 0.3 | 0.2 | Normal |
| **Strong Halation** | 0.6 | 0.5 | 0.4 | Normal |
| **Dreamy Haze** | 0.5 | 0.8 | 0.3 | Screen |
| **Pro Mist** | 0.5 | 0.4 | 0.25 | Soft Light* |

*Use Blur node in Soft Light instead of Glow composite

## Blur + Soft Light Recipe (Pro Mist)

```
Node N:   Grade complete
Node N+1: Blur (Radius 8-15) → Inspector → Composite Mode: Soft Light → Opacity 15-25%
Node N+2: Optional Glow for extra highlight bloom
```

## Atmospheric Grading Cheat Sheet

| Element | Shadows | Midtones | Highlights |
|---------|---------|----------|------------|
| **Haze** | Lift ↑, Teal | Desaturate | Warm/Neutral |
| **Golden Hour** | Warm | Warm | Hot/Orange |
| **Blue Hour** | Deep Blue | Cool | Neutral |
| **Fog/Mist** | Lift ↑↑ | Desat ↑ | Glow/Bloom |
| **Dreamy** | Lift ↑, Cool | Soft Contrast | Glow, Warm |

## Power Window for Atmospheric Depth

1. **Foreground**: Window on near elements → Contrast ↑, Detail ↑
2. **Midground**: Window on subject → Normal grade
3. **Background**: Inverse window → Contrast ↓, Sat ↓, Cool ↑, Blur ↑

Creates **atmospheric perspective** (depth cueing)

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Glow looks digital | Lower threshold, increase radius, use Soft Light blur |
| Halation too strong | Reduce opacity, mask off non-light areas |
| Haze flattens image | Midtone Detail +10 to +20, local contrast on subject |
| Color contamination | Qualifier restrict glow to luminance only |
| Banding in glow | Add 0.5% noise before glow, or dither |