---
name: davinci-timelapse-photography-workflow
description: DaVinci Resolve time-lapse photography workflow — importing image sequences, applying time-lapse effects, color correction, exposure compensation, and white balance from 2 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [timelapse, time-lapse, photography, davinci-resolve, image-sequence, exposure-compensation, white-balance]
trigger: Use when user wants to create time-lapse videos from photos in DaVinci Resolve
parameters:
  - name: input_type
    description: Source material type
    type: string
    enum: [raw-photos, jpeg-sequence, video-speed-up, hybrid]
    default: raw-photos
  - name: frame_rate
    description: Output frame rate
    type: integer
    default: 24
  - name: exposure_compensation
    description: Exposure adjustment for sequence
    type: string
    default: -0.5
  - name: white_balance
    description: White balance mode
    type: string
    enum: [auto, daylight, cloudy, tungsten, custom-kelvin]
    default: auto
steps:
  - step: Import image sequence
    description: Media Pool → Import → select first image → check "Image Sequence"
  - step: Set timeline frame rate
    description: Project Settings → Timeline Frame Rate → 24/30/60 fps
  - step: Apply time-lapse effect
    description: Retime Controls (Cmd+R) → Speed → 100-1000% or use Optical Flow
  - step: Color correct sequence
    description: Color page → primary correction → match exposure across frames
  - step: Export time-lapse
    description: Deliver page → Render settings → QuickTime/MP4
---

# DaVinci Resolve Time-Lapse Photography Workflow

**Cluster:** 2 techniques tagged "time-lapse" / "Time-Lapse Photography"

## Techniques Covered

| Reel | Technique | Key Nodes | Parameters |
|------|-----------|-----------|------------|
| C5nY7z9Pn_O | Time-lapse Photography with DaVinci Resolve | Time-lapse Effect + Color Correction | Exposure Compensation: -0.5, White Balance: Auto |
| C5iZf_6P648 | Time-Lapse Photography | Import/Organize + Color Correction/Adjustments | Exposure Compensation, White Balance |

## Complete Time-Lapse Workflow

### 1. Shoot: Capture Image Sequence
```
Camera Settings (from reels):
  • Interval: 2-10 seconds (clouds: 5-10s, people: 2-3s, stars: 20-30s)
  • Duration: 30 min - 3 hours
  • Format: RAW preferred, JPEG acceptable
  • Manual mode: Fixed aperture, shutter, ISO
  • White Balance: Fixed (not Auto) for consistency
  • Focus: Manual, locked
```

### 2. Import: Image Sequence to Media Pool
```
Media Pool → Right-click → Import Media
  • Navigate to folder
  • Select FIRST image only
  • Check "Import as Image Sequence"
  • DaVinci auto-detects numbering (IMG_0001, IMG_0002...)
  • Creates single clip representing entire sequence
```

**Pro Tip (C5iZf_6P648)**: "Import and organize images from camera" — Create bins by date/location

### 3. Timeline: Set Frame Rate
```
Project Settings (Cmd+,) → Master Settings:
  • Timeline Frame Rate: 24 (cinematic), 30 (web), 60 (smooth)
  • Playback Frame Rate: Match timeline
  • Image Sequence Frame Rate: Set to desired output fps
```

**Math**: 300 photos @ 24fps = 12.5 seconds of video

### 4. Retime: Create Time-Lapse Speed
```
Method A: Retime Controls (Edit page)
  • Select clip → Cmd+R (Retime Controls)
  • Speed Change → 500-2000% (adjust for desired duration)
  • Ripple Sequence: ON (shifts downstream clips)

Method B: Optical Flow (for smooth motion)
  • Retime Controls → Optical Flow → Speed Warp
  • Better for: cloud movement, water, traffic

Method C: Frame Blending (fast preview)
  • Retime Controls → Frame Blend
  • Good for: draft/preview, not final
```

### 5. Color: Exposure & White Balance (from reels)
```
Node 1: Primary Correction
  • Exposure Compensation: -0.5 EV (C5nY7z9Pn_O)
    - Time-lapses often overexpose highlights over time
    - Pull highlights down, lift shadows slightly
  • White Balance: Fixed Kelvin (C5iZf_6P648)
    - Don't use Auto — causes flicker
    - Set to daylight (5600K) or measured Kelvin
    - Keyframe WB if lighting changes (sunset)

Node 2: Deflicker (CRITICAL for time-lapse)
  • OFX: Deflicker (Resolve Studio) or third-party
  • Analyze luminance variation frame-to-frame
  • Smooth exposure jumps

Node 3: Creative Grade
  • Saturation boost for landscapes
  • Contrast for sky definition
  • LUT if desired (Kodak 2383 for film look)
```

### 6. Advanced: Holy Grail Time-Lapse (Day to Night)
```
Keyframe exposure/WB across transition:
  • Node 1 keyframes: Exposure, Temp, Tint
  • Set keyframes every 50-100 frames
  • Smooth curves in Keyframe Editor
  • Use Deflicker OFX after keyframing
```

### 7. Export: Deliver Settings
```
Deliver Page → Render Settings:
  • Format: QuickTime (ProRes 422 HQ) or MP4 (H.264/H.265)
  • Resolution: 4K/5K/6K from photos → downscale to 4K/1080p
  • Frame Rate: Match timeline (24/30/60)
  • Quality: High bitrate (100-200 Mbps for ProRes, 50-80 for H.264)
  • Render: Individual clips or single file
```

## Parameters from Reels

| Parameter | C5nY7z9Pn_O | C5iZf_6P648 |
|-----------|-------------|-------------|
| Exposure Compensation | -0.5 | Keyframed |
| White Balance | Auto (not recommended) | Manual/Custom |
| Key Nodes | Time-lapse Effect, Color Correction | Import/Organize, Color Correction |

**Correction**: Reels say "Auto" WB but **pro workflow uses fixed Kelvin** to prevent flicker.

## Interval Calculator

| Subject | Interval | Duration for 10s @ 24fps |
|---------|----------|--------------------------|
| Fast clouds | 2-3s | 8-12 min |
| Slow clouds | 5-10s | 20-40 min |
| Sunrise/sunset | 5-10s | 30-60 min |
| Stars/Milky Way | 20-30s | 2-3 hours |
| City traffic | 1-2s | 4-8 min |
| Construction | 30-60s | 2-4 hours |
| Plant growth | 5-15 min | Days/weeks |

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Flicker | Auto exposure/WB | Manual mode, fixed WB, Deflicker OFX |
| Jitter | Camera movement | Sturdy tripod, weighted bag, remote trigger |
| Sensor dust spots | Visible at small apertures | Clean sensor, or spot-remove in Fusion |
| Battery death | Long shoots | External power (USB-C PD, V-mount) |
| Storage full | RAW sequences huge | Shoot JPEG for very long, or bring SSDs |

## Pro Tips from Reels

- **C5nY7z9Pn_O**: "Apply time-lapse effect using built-in tools or plugins" — Retime Controls is built-in
- **C5iZf_6P648**: "Import and organize images from camera" — Bin structure saves hours later
- **Both**: Exposure compensation negative (-0.5) protects highlights in changing light

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Grade time-lapse sequences
- `davinci-fusion-deflicker` — Advanced deflickering in Fusion
- `davinci-speed-ramping-retiming` — Retime controls deep dive
- `davinci-drone-cinematic-workflow` — Aerial time-lapses