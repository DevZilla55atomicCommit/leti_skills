---
name: davinci-gimbal-stabilization
description: Gimbal shooting techniques and in-camera/post stabilization workflows in DaVinci Resolve. Covers gimbal settings, stabilization nodes, and smoothing techniques from Instagram Reel analysis.
trigger: gimbal, stabilization, camera movement, smooth footage, DaVinci Resolve stabilizer
steps:
  - "Configure gimbal: balance, motor strength, follow modes (PF, PTF, FPV, Lock)"
  - "Shoot with proper technique: ninja walk, two-handed grip, controlled movements"
  - "Import footage to DaVinci Resolve"
  - "Edit page: Inspector → Stabilization → Select mode (Perspective/Similarity/Translation)"
  - "Color page: Add Stabilizer node (OFX) for additional smoothing"
  - "Fine-tune: Smooth, Strength, Zoom, Cropping Ratio parameters"
  - "For gimbal footage: Use 'Similarity' mode with low Strength (0.1-0.3)"
  - "For handheld: Use 'Perspective' mode with higher Strength (0.4-0.7)"
parameters:
  - name: stabilization_mode
    type: string
    description: Stabilization analysis mode
    enum: ["Perspective", "Similarity", "Translation"]
    default: "Similarity"
  - name: smooth
    type: number
    description: Smoothness amount (0-1)
    default: 0.5
  - name: strength
    type: number
    description: Stabilization strength (0-1)
    default: 0.3
  - name: zoom
    type: string
    description: Auto-zoom to fill frame after stabilization
    enum: ["Auto", "Off", "Custom"]
    default: "Auto"
  - name: cropping_ratio
    type: number
    description: How much to crop (0-1)
    default: 0.1
  - name: camera_type
    type: string
    description: Camera/gimbal type for preset
    enum: ["DJI RS2/RS3", "DJI Ronin", "Zhiyun Weebill", "Moza", "Handheld", "Drone"]
tags:
  - gimbal
  - stabilization
  - camera-movement
  - davinci-resolve
  - inspector-stabilization
  - ofx-stabilizer
  - smooth-footage
  - ninja-walk
category: davinci-resolve-stabilization
---

# DaVinci Resolve Gimbal & Stabilization Techniques

Complete guide to gimbal shooting techniques and post-production stabilization in DaVinci Resolve, based on Instagram Reel analysis covering DJI, Zhiyun, Moza gimbals and handheld/drone stabilization.

## Gimbal Setup & Shooting Techniques

### Pre-Shoot Balancing (Critical)
```
1. Mount camera → Balance Tilt axis (camera stays level when released)
2. Balance Roll axis (camera doesn't roll left/right)
3. Balance Pan axis (gimbal doesn't drift when powered off)
4. Power on → Auto-tune motors (if supported)
5. Test: Ninja walk - smooth heel-to-toe steps, bent knees
```

### Gimbal Follow Modes Explained

| Mode | Pan | Tilt | Roll | Best For |
|------|-----|------|------|----------|
| **PF** (Pan Follow) | Follow | Locked | Locked | Walking shots, tracking subject |
| **PTF** (Pan/Tilt Follow) | Follow | Follow | Locked | General run-and-gun, vlogging |
| **FPV** (First Person View) | Follow | Follow | Follow | Creative, dynamic, drone-like |
| **Lock** (All Locked) | Locked | Locked | Locked | Tripod replacement, timelapse |
| **Flashlight** | Follow | Follow | Follow (inverted) | Inverted/low angle creative |

### Camera Settings for Gimbal
```
- Shutter Speed: 180° rule (1/60 for 30fps, 1/120 for 60fps)
- Aperture: f/2.8-f/4 (depth for subject separation)
- ISO: Native ISO (base ISO for cleanest image)
- Focus: Continuous AF (AF-C) with small focus area
- IBIS: OFF (gimbal handles stabilization)
- Profile: Log (S-Log3, V-Log, C-Log) for max DR
```

## DaVinci Resolve Stabilization Workflow

### Method 1: Inspector Stabilization (Edit/Cut Page)
```
1. Select clip in timeline
2. Open Inspector (top right)
3. Scroll to "Stabilization" section
4. Click "Analyze" (spins up analysis)
5. Choose Mode:
   - Perspective: Handles rotation + perspective (handheld, drone)
   - Similarity: Rotation + scale + translation (gimbal, smoothest)
   - Translation: X/Y only (minimal crop, subtle shake)
6. Adjust parameters (see Parameter Guide below)
7. Click "Stabilize" to apply
```

### Method 2: OFX Stabilizer Node (Color Page) - More Control
```
Node Graph:
Node 1: Primary Grade
Node 2: Stabilizer OFX (before grade for clean analysis)
Node 3: Creative LUT/Grade

Stabilizer OFX Settings:
- Analysis Mode: Same as Inspector modes
- Smooth: 0.0-1.0 (temporal smoothing)
- Strength: 0.0-1.0 (correction amount)
- Zoom: Auto/Off/Custom (fills black edges)
- Cropping Ratio: 0.0-1.0 (edge crop tolerance)
- Camera Lock: Lock X/Y/Rotation independently
```

## Parameter Tuning Guide

### For Gimbal Footage (Already Smooth)
```
Mode: Similarity
Smooth: 0.2-0.4
Strength: 0.1-0.3
Zoom: Auto
Cropping Ratio: 0.05-0.1
Result: Subtle micro-jitter removal, maintains natural motion
```

### For Handheld Footage
```
Mode: Perspective
Smooth: 0.5-0.7
Strength: 0.4-0.7
Zoom: Auto
Cropping Ratio: 0.1-0.2
Result: Significant shake reduction, some crop expected
```

### For Drone Footage
```
Mode: Perspective or Similarity
Smooth: 0.3-0.5
Strength: 0.2-0.4
Zoom: Auto
Cropping Ratio: 0.05-0.1
Note: Drones have vibration - may need Gyroflow pre-processing
```

### For Walking/Talking Head (Ninja Walk)
```
Mode: Similarity
Smooth: 0.4-0.6
Strength: 0.2-0.4
Zoom: Auto
Cropping Ratio: 0.1
Tip: Analyze on wide shot, apply to close-ups (copy stabilization data)
```

## Advanced Techniques

### Copy Stabilization Across Clips
```
1. Stabilize master/wide shot fully
2. Right-click clip → "Copy" (or Cmd+C)
3. Select target clips → Right-click → "Paste Attributes"
4. Check only "Stabilization" → Paste
5. All clips share same stabilization data (consistent movement)
```

### Stabilization + Speed Ramp
```
Issue: Stabilization analyzes at timeline speed
Fix:
1. Stabilize at 100% speed first
2. Compound Clip (right-click → New Compound Clip)
3. Apply Retime/Speed Ramp to compound clip
4. Stabilization "baked in" before speed change
```

### Gyroflow Pre-Processing (For Severe Shake)
```
1. Export clips from Resolve
2. Process in Gyroflow (free, uses gyro data)
3. Re-import stabilized clips
4. Minimal Resolve stabilization needed
Best for: Action cams, drones, severe handheld
```

### Selective Stabilization (Power Window)
```
Color Page:
1. Add Stabilizer OFX node
2. Add Power Window (Circle/Gradient) on Stabilizer node
3. Track subject (Tracker)
4. Invert window → Stabilize ONLY background
5. Result: Subject stays sharp, background smoothed
```

## Gimbal-Specific Tips by Brand

### DJI RS2 / RS3 / RSC2
- **Auto-Tune**: Hold trigger + power on
- **SuperSmooth**: Enable for telephoto (100mm+)
- **Sport Mode**: Faster response for running
- **Bluetooth**: Control via Ronin app (focus, settings)

### Zhiyun Weebill 3 / Crane 4
- **ViaTouch 2.0**: Touchscreen control
- **Smart Follow**: AI subject tracking
- **Axis Locks**: Quick release for transport

### Moza AirCross 3 / gimbals
- **Inception Mode**: 360° roll (creative)
- **Mimic Motion**: Remote control via phone

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Warping/distortion | Over-stabilization (Strength too high) | Reduce Strength, increase Cropping Ratio |
| Black edges | Zoom: Off or insufficient | Set Zoom: Auto, increase Cropping Ratio |
| Jello/wobble | Rolling shutter + stabilization | Enable "Rolling Shutter Reduction" in OFX |
| Drift over time | Long clip, accumulated error | Split clip, re-analyze each section |
| Subject distortion | Perspective mode on gimbal footage | Use Similarity mode for gimbal |

## Parameter Reference Quick Card

```
INSPECTOR / OFX STABILIZER PARAMETERS:

Mode:           Perspective | Similarity | Translation
Smooth:         0.0 ────────────────── 1.0  (temporal smoothing)
Strength:       0.0 ────────────────── 1.0  (correction force)
Zoom:           Auto / Off / Custom
Cropping Ratio: 0.0 ────────────────── 1.0  (edge tolerance)
Camera Lock:    ☐ Pan  ☐ Tilt  ☐ Roll   (lock axes independently)
```

## Related Skills

- `davinci-camera-movement-tracking` - Camera tracker for match-moving
- `davinci-dynamic-zoom-keyframe` - Keyframed zoom/pan movements
- `davinci-time-lapse-hyperlapse` - Stabilized timelapse workflows