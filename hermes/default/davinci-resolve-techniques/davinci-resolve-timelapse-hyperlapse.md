---
name: davinci-resolve-timelapse-hyperlapse
description: Time-lapse and hyperlapse creation workflows in DaVinci Resolve. Use for cityscapes, clouds, construction, day-to-night transitions, and creative speed-ramped sequences.
trigger: User wants to create time-lapse, hyperlapse, or speed-ramped videos in DaVinci Resolve.
category: davinci-resolve
tags:
  - time-lapse
  - hyperlapse
  - photography
  - speed ramp
  - davinci resolve
  - cityscape
  - montage
steps:
  - name: basic-timelapse-assembly
    description: Assemble photo sequence into time-lapse on Edit page
    parameters:
      - name: frame_rate
        type: string
        default: "24fps or 30fps"
        description: Timeline frame rate
      - name: photo_duration
        type: string
        default: "1 frame per photo"
        description: Each photo = 1 frame
      - name: deflicker
        type: boolean
        default: true
        description: Enable deflicker in Media Pool or Color page
    difficulty: beginner
  - name: hyperlapse-stabilization
    description: Stabilize hyperlapse (moving camera time-lapse) using Optical Flow or Stabilizer
    parameters:
      - name: method
        type: string
        enum: ["Optical Flow (Speed Warp)", "Stabilizer (Perspective)", "Fusion Tracker"]
        default: "Optical Flow (Speed Warp)"
      - name: speed_warp_mode
        type: string
        enum: ["Speed Warp", "Frame Blend", "Nearest"]
        default: "Speed Warp"
    difficulty: intermediate
  - name: day-to-night-holy-grail
    description: Holy Grail time-lapse (exposure ramping day to night) with keyframed exposure/WB
    parameters:
      - name: exposure_ramping
        type: string
        default: "Keyframed ISO/Shutter in Camera RAW settings"
        description: Animate RAW params or use Color page keyframes
      - name: white_balance_ramping
        type: boolean
        default: true
        description: Keyframe Temp/Tint for consistent color
      - name: deflicker_strength
        type: string
        default: "Medium"
    difficulty: advanced
  - name: speed-ramp-montage
    description: Dynamic speed ramping for action/cinematic montages
    parameters:
      - name: retime_curve
        type: string
        default: "Retime Curve (Ctrl+R)"
        description: Use Retime Curve editor for smooth ramps
      - name: optical_flow
        type: boolean
        default: true
        description: Enable Optical Flow for smooth slow-mo
      - name: speed_points
        type: string
        default: "100% → 50% → 200% → 100%"
        description: Example speed keyframe progression
    difficulty: intermediate
parameters:
  - name: resolve_page
    type: string
    default: "Edit|Color|Fusion"
    description: Edit for assembly, Color for deflicker/grade, Fusion for advanced stabilization
  - name: node_graph_type
    type: string
    default: "serial"
---

# DaVinci Resolve Time-Lapse & Hyperlapse Workflows

Complete workflows for creating time-lapses, hyperlapses, day-to-night "Holy Grail" sequences, and dynamic speed-ramped montages in DaVinci Resolve.

## Video References

| Technique | Video ID | Key Nodes/Tools | Tags |
|-----------|----------|-----------------|------|
| Time-Lapse Photography | C3qf4DGg631 | node1, node2 | time-lapse, photography |
| Time-Lapse Montage | CznfJkjrMon | node1, node2 | time-lapse, montage |
| Cityscape Time-Lapse | - | - | cityscape, time-lapse |
| Dramatic Time-Lapse | - | - | time-lapse |
| Cityscape Time-Lapse with DaVinci Resolve | - | - | cityscape, time-lapse |
| Time-Lapse Photography with DaVinci Resolve | - | - | time-lapse, photography |

## Core Workflows

### 1. Basic Time-Lapse Assembly (Photo Sequence → Video)
**Reference**: C3qf4DGg631, CznfJkjrMon

**Method A: Media Pool Import (Recommended)**
```
1. Media Page → Navigate to photo folder
2. Select first image → Check "Import as Image Sequence" (or drag folder)
3. Set Start Frame / End Frame if numbered
4. Import → Creates single clip in Media Pool
5. Drag to timeline → Each photo = 1 frame
```

**Method B: Timeline Import**
```
1. Edit Page → Right-click timeline → "Import Media"
2. Select image sequence folder
3. Resolve auto-detects sequence
```

**Project Settings**:
| Setting | Value |
|---------|-------|
| Timeline Resolution | 3840x2160 (4K) or 1920x1080 |
| Timeline Frame Rate | 24/30 fps (match delivery) |
| Image Scaling | "Scale Full Frame with Crop" |

**Deflicker (Critical for Time-Lapse)**:
```
Media Pool → Right-click clip → Clip Attributes → Deflicker: On
OR
Color Page → Timeline → Deflicker (OFX) on adjustment clip
```

### 2. Hyperlapse (Moving Camera Time-Lapse) Stabilization
**Reference**: C1CATqWiahJ (Gimbal Move tracking principles apply)

**Challenge**: Handheld/gimbal hyperlapse has frame-to-frame jitter.

**Solution A: Optical Flow Speed Warp (Best Quality)**
```
Edit Page:
├── Clip on timeline
├── Right-click → Retime Controls (Ctrl+R)
├── Set speed to desired rate (e.g., 300% = 30fps→10fps playback)
├── Retime Curve → Enable "Optical Flow: Speed Warp"
├── Analyze (may take time)
└── Render cache for playback

Color Page (Alternative):
├── Node 1: Optical Flow OFX (DaVinci Resolve Studio only)
├── Set vector detail: High
└── Smooth: 0.5-1.0
```

**Solution B: Edit Page Stabilizer**
```
Inspector → Stabilization
├── Mode: Perspective
├── Smoothness: High
├── Zoom: Auto
└── Analyze
```
*Then apply Retime for speed*

**Solution C: Fusion Stabilizer (Most Stabilizer + Retime)**
```
Fusion Page:
├── MediaIn → Stabilizer Tool (Planar/Tracker)
├── Track reference frames across sequence
├── Stabilize → Smooth: 0.8
├── MediaOut
└── Then Retime on Edit page
```

### 3. Day-to-Night "Holy Grail" Time-Lapse
**Advanced**: Requires shooting with exposure ramping (qDslrDashboard, LRTimelapse, or manual)

**Post-Workflow in Resolve**:
```
Color Page Node Structure:
├── Node 1: Input Transform (Log → Rec.709)
├── Node 2: Exposure Ramp (Keyframed)
│   ├── Gain/Offset: Animate to match exposure changes
│   ├── Keyframes: Every 50-100 frames at transition points
│   └── Use Offset for ISO-like lift, Gain for highlight protection
├── Node 3: White Balance Ramp (Keyframed)
│   ├── Temp: Cool → Warm (or vice versa)
│   ├── Tint: Compensate for green/magenta shift
│   └── Keyframe at same points as exposure
├── Node 4: Deflicker (OFX)
│   ├── Window: Large (full frame)
│   ├── Strength: Medium-High
│   └── Frame Range: Analyze full clip
├── Node 5: Color Grade (Creative)
└── Node 6: Output Transform
```

**Keyframe Strategy**:
- Set keyframes at **exposure change points** (not every frame)
- Typical: 5-10 keyframes for 10-second sequence
- Use **Offset** (lift) for shadow exposure, **Gain** for highlights
- Smooth keyframe interpolation: **Smooth (Bezier)**

**LRTimelapse Integration** (Best for Holy Grail):
```
1. Process in LRTimelapse (deflicker, keyframe exposure/WB)
2. Export graded JPEGs/DNGs
3. Import sequence to Resolve
4. Minimal grading needed (LRTimelapse did heavy lifting)
```

### 4. Speed Ramp Montage (Action/Cinematic)
**Reference**: C6rpIhKLk5V (Speed Hump Tutorial principles)

```
Edit Page:
├── Clip on timeline
├── Right-click → Retime Controls (Ctrl+R)
├── Retime Curve Editor (click curve icon)
│   ├── Add keyframes at beat points
│   ├── Speed graph: 100% → 50% (slow) → 200% (fast) → 100%
│   ├── Use Bezier handles for smooth transitions
│   └── Enable "Optical Flow: Speed Warp" for slow-mo sections
├── Music sync: Cut to beat, ramp on downbeats
└── Render cache for smooth playback
```

**Retime Curve Tips**:
| Action | Shortcut/Method |
|--------|-----------------|
| Add keyframe | Alt+Click on curve |
| Bezier handles | Drag keyframe handles |
| Smooth transition | Right-click keyframe → Smooth |
| Freeze frame | Horizontal curve segment (0% speed) |
| Reverse | Negative speed value |

**Optical Flow Settings** (for slow-mo sections):
```
Clip Attributes → Retime Process:
├── Speed Warp (Studio only) - Best quality
├── Frame Blend - Fast, good for mild slow-mo
└── Nearest Neighbor - Fastest, blocky
```

### 5. Cityscape/Cloud Time-Lapse with Motion
**Adding Cinematic Movement to Static Time-Lapse**

```
Fusion Page (or Edit Page Transform Keyframes):
├── MediaIn (4K+ source on 1080p timeline)
├── Transform Tool
│   ├── Center: Animate X/Y for pan
│   ├── Zoom: Animate for dolly/zoom
│   ├── Rotation: Subtle rotation for dynamic feel
│   └── Keyframes: Linear or Ease In/Out
└── MediaOut
```

**Edit Page Alternative**:
```
Clip on timeline (4K on 1080p timeline)
├── Inspector → Transform
├── Zoom: 150-200% (crop room for movement)
├── Position X/Y: Keyframe pan/tilt
├── Rotation: Keyframe subtle rotation
└── Dynamic Zoom: Auto-animate (linear/ease)
```

### 6. Time-Lapse Color Grading

```
Node Structure:
├── Node 1: Technical (Deflicker, Denoise)
├── Node 2: Primary (Exposure, Contrast, WB)
├── Node 3: Sky Enhancement
│   ├── Qualifier: Select sky (blue hues)
│   ├── Saturation: +20-30%
│   ├── Contrance: +10%
│   └── Gradient: Darken top of frame
├── Node 4: Ground/Foreground
│   ├── Power Window: Bottom 2/3
│   ├── Shadows: Lift slightly
│   └── Clarity: +10-15%
├── Node 5: Creative Look (LUT or Grade)
└── Node 6: Output (Rec.709, Legal Levels)
```

**Deflicker Settings** (Color Page OFX):
| Parameter | Value | Notes |
|-----------|-------|-------|
| Window Size | Large (full frame) | Time-lapse = global flicker |
| Strength | 0.5-0.8 | Higher = smoother, may blur detail |
| Frames | 5-15 | Analyze surrounding frames |
| Mode | Luminance | Or RGB for color flicker |

## Delivery Settings for Time-Lapse

| Platform | Resolution | Frame Rate | Codec | Bitrate |
|----------|------------|------------|-------|---------|
| Instagram Reel | 1080x1920 | 30fps | H.264 | 8-12 Mbps |
| YouTube | 3840x2160 | 24/30fps | H.264/H.265 | 35-45 Mbps |
| TikTok | 1080x1920 | 30fps | H.264 | 8-12 Mbps |
| Client Delivery | 4K/6K/8K | 24fps | ProRes/DNxHR | High |

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Flickering | Aperture/exposure variance | Deflicker OFX, LRTimelapse pre-process |
| Jittery hyperlapse | Handheld movement | Optical Flow Speed Warp, Planar Track |
| Banding in sky | 8-bit source, heavy grade | Add noise/grain, 10-bit export |
| Choppy playback | High-res, no cache | Render Cache (Smart/User), Proxy mode |
| Exposure jumps | Auto exposure in camera | Holy Grail keyframing, LRTimelapse |

## Related Skills
- `davinci-resolve-color-grading-fundamentals` - Grading time-lapses
- `davinci-resolve-stabilization-tracking` - Hyperlapse stabilization
- `davinci-resolve-optical-flow-retime` - Speed Warp deep dive
- `instagram-reel-editing-techniques` - Vertical time-lapse for Reels