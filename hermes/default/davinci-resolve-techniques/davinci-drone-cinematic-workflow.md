---
name: davinci-drone-cinematic-workflow
description: DaVinci Resolve cinematic drone workflow — color grading aerial footage, motion tracking for stabilization, camera movement analysis, and drone-specific grading techniques from 3 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [drone, cinematic, aerial, color-grading, motion-tracking, davinci-resolve, drone-footage, stabilization]
trigger: Use when user wants to grade, stabilize, or enhance drone/aerial footage in DaVinci Resolve
parameters:
  - name: drone_type
    description: Drone/camera type for log conversion
    type: string
    enum: [dji-mavic, dji-inspire, dji-air, autel, fpv, generic-log]
    default: generic-log
  - name: grading_style
    description: Desired look
    type: string
    enum: [cinematic, natural, film-emulation, high-contrast, golden-hour]
    default: cinematic
  - name: stabilize
    description: Apply motion tracking stabilization
    type: boolean
    default: true
steps:
  - step: Convert log footage to Rec.709
    description: CST or technical LUT for drone log profile (D-Log, D-Cinelike)
  - step: Primary correction for aerial haze
    description: Dehaze, contrast, saturation for atmospheric perspective
  - step: Motion tracking stabilization
    description: Fusion Camera Tracker or Stabilizer for micro-jitter
  - step: Creative grade with sky enhancement
    description: Qualifier for sky, power windows for ground separation
  - step: Export with appropriate codec
    description: ProRes/DNx for post, H.265 for delivery
---

# DaVinci Resolve Cinematic Drone Workflow

**Cluster:** 3 techniques tagged "drone", "cinematic drone", "aerial"

## Techniques Covered

| Reel | Technique | Key Focus |
|------|-----------|-----------|
| C33n2bxpcTm | Best Drone — cinematic drone moves | Movement types, shot design |
| C5TByCRv0ZZ | Cinematic Drone Moves | Color correction + motion tracking |
| C4FqbyWSgxs | Drone Photography | Color correction for aerial |

## Drone Log Profiles & Conversion

| Drone | Log Profile | Input Color Space | Input Gamma |
|-------|-------------|-------------------|-------------|
| DJI Mavic 3 | D-Log / D-Log M | DJI D-Gamut | D-Log |
| DJI Air 2S/3 | D-Log M | DJI D-Gamut | D-Log M |
| DJI Mini 3/4 Pro | D-Cinelike | Rec.709 | D-Cinelike |
| DJI Inspire 2/3 | D-Log | DJI D-Gamut | D-Log |
| Autel EVO II | A-Log | Autel Log | A-Log |
| FPV (GoPro) | Flat/ProTune | Rec.709 / GoPro | Flat |

### CST Setup (Node 1 - Technical)
```
Color Space Transform OFX:
  Input Color Space: [Match drone — DJI D-Gamut, etc.]
  Input Gamma: [Match drone — D-Log, D-Cinelike, etc.]
  Output Color Space: Rec.709
  Output Gamma: Gamma 2.4 (or 2.2 for web)
```

**Alternative**: Technical LUT (DJI provides .cube for D-Log → Rec.709)

## Node Structure for Drone Grading

```
Node 1: CST / Technical LUT        (Log → Rec.709)
Node 2: Primary - Dehaze/Contrast  (Aerial haze removal)
Node 3: Sky Isolation (Qualifier)  (Separate sky grade)
Node 4: Ground Isolation (Window)  (Separate ground grade)
Node 5: Creative Grade             (Look/LUT)
Node 6: Output Transform           (Final CST if needed)
```

### Node 2: Aerial Haze Removal (Primary)
- **Contrast**: +15 to +25 (compress atmospheric haze)
- **Pivot**: 0.35-0.4 (protect midtones)
- **Saturation**: +10 to +20 (haze desaturates)
- **Dehaze** (if using Color Boost OFX): +10 to +30
- **Shadows**: Lift slightly (-5 to -10) for depth

### Node 3: Sky Grade (Qualifier → HSL)
```
Qualifier:
  • Select blue/cyan sky range (Hue ~200-240°)
  • Softness: High (40-60)
  • Clean up with erode/dilate

Adjustments:
  • Saturation: +20 to +40 (pop sky)
  • Luminance: -10 to -20 (deepen blue)
  • Hue shift: Slight teal (+5-10) for cinematic
```

### Node 4: Ground Grade (Power Window)
```
Circular/Gradient Window:
  • Cover ground/landscape
  • Softness: 0.3-0.5
  • Invert: ON (affect ground only)

Adjustments:
  • Exposure: +0.2 to +0.5 (ground often underexposed)
  • Warmth: +100 to +300K (golden hour feel)
  • Contrast: +10
```

## Motion Tracking Stabilization (from C5TByCRv0ZZ)

### Fusion Camera Tracker (for VFX integration)
1. Fusion page → MediaIn
2. CameraTracker → Track Features → Solve
3. Export 3D camera for compositing

### Stabilizer (for micro-jitter removal)
```
Edit/Color Page → Inspector → Stabilization:
  Mode: Perspective (handles rotation)
  Smoothness: 0.2-0.4 (light — drone already stable)
  Zoom: Auto (crop edges)
```

**Pro Tip**: Drones are already stabilized by gimbal. Only stabilize if:
- Wind gust caused frame shift
- FPV footage (no gimbal)
- Telephoto drone shots (amplified shake)

## Cinematic Drone Moves (from C33n2bxpcTm, C4FqbyWSgxs)

| Move | Description | Grading Note |
|------|-------------|--------------|
| **Reveal** | Rise up to reveal landscape | Keyframe exposure up as sky enters |
| **Orbit** | Circle subject at radius | Track subject with power window |
| **Dolly** | Forward/backward linear | Retime for speed ramp |
| **Top-down** | Nadir (straight down) | Symmetry — center frame, minimal grade |
| **Low skim** | Near ground, fast | Motion blur — Optical Flow retime |
| **Pull-away** | Back + up simultaneously | Reveal scale — grade for depth |
| **Crane** | Vertical up/down | Match exposure to changing sky |

## Speed Ramping Drone Footage
```
Retime Controls (Cmd+R):
  • Speed points at move start/end
  • 100% → 50% → 100% for emphasis
  • Optical Flow (Speed Warp) for smooth slow-mo
  • Ease curves: Bezier for natural acceleration
```

## Color Grading Styles for Drone

### Cinematic (Default)
- Teal shadows, warm highlights (orange-teal)
- Sky: deep blue/cyan, Ground: warm gold
- Film emulation LUT (Kodak 2383, Fuji 3510)

### Natural/Documentary
- Accurate colors, minimal saturation boost
- CST only + slight contrast
- White balance: measured Kelvin

### Golden Hour
- Warmth: +500-1000K temp
- Magenta tint: +5 to +10
- Sky gradient: orange→blue via power window

### High Contrast / Moody
- Crush shadows (Lift -20)
- Blow highlights slightly (Gain +10)
- Desaturate -20, then selective re-saturate

## Export Settings for Drone

| Delivery | Codec | Bitrate | Notes |
|----------|-------|---------|-------|
| YouTube 4K | H.265 | 50-80 Mbps | Tag HDR if graded in PQ |
| Instagram Reel | H.264 | 15-20 Mbps | 1080x1920 vertical crop |
| Client Review | ProRes 422 HQ | ~500 Mbps | 10-bit if source 10-bit |
| Archive | ProRes 4444 | ~1.5 Gbps | Alpha if VFX |

## Common Drone Issues & Fixes

| Issue | Fix |
|-------|-----|
| Propeller shadows | Crop/zoom slightly, or paint out in Fusion |
| Lens flare (sun in frame) | Power window to reduce highlights, add glow |
| Color shift across pan | Keyframe WB/temp in Node 1 |
| Jello/rolling shutter | Optical Flow retime, or Fusion Vector Motion Blur |
| Noise in shadows (high ISO) | Noise Reduction (Studio) — Spatial 5, Temporal 3 |
| Horizon not level | Transform → Rotation keyframe |

## Pro Tips from Reels

- **C5TByCRv0ZZ**: "Track motion in Edit page, refine tracking results, apply stabilization" — Two-stage: track then stabilize
- **C5TByCRv0ZZ**: "Color correction using Color page — adjust saturation, contrast, exposure for visual appeal" — Aerial needs more contrast
- **C4FqbyWSgxs**: "Adjust color balance, contrast, saturation for professional look" — Standard drone workflow
- **C33n2bxpcTm**: "Best drone moves" — Plan shots, don't just fly randomly

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Core grading nodes
- `davinci-fusion-camera-tracking` — Advanced 3D tracking
- `davinci-speed-ramping-retiming` — Speed ramps for drone moves
- `davinci-color-management-cst` — Log conversion deep dive