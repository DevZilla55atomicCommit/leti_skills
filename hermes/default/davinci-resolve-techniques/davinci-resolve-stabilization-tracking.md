---
name: davinci-resolve-stabilization-tracking
description: Stabilization (Perspective/Similarity/Translation modes) and Motion Tracking workflows in DaVinci Resolve. Use for smoothing handheld/gimbal footage, locking onto subjects, and stabilizing real estate/walkthrough videos.
trigger: User needs to stabilize shaky footage or track motion for effects/compositing in DaVinci Resolve (Edit page Inspector or Color page Tracker).
category: davinci-resolve
tags:
  - stabilization
  - gimbal
  - smartphone
  - real estate
  - videography
  - motion tracking
  - tracker
  - davinci resolve
  - edit page
steps:
  - name: inspector-stabilization
    description: Stabilize footage using Edit page Inspector (Perspective/Similarity/Translation modes)
    parameters:
      - name: mode
        type: string
        enum: ["Perspective", "Similarity", "Translation"]
        default: "Perspective"
        description: Perspective for 3D camera moves, Similarity for rotation/scale, Translation for position only
      - name: smoothness
        type: string
        default: "Medium"
        enum: ["Low", "Medium", "High"]
        description: Smoothing strength (higher = more crop)
      - name: crop_amount
        type: string
        default: "Automatic"
        description: "Automatic" or manual percentage to hide black borders
      - name: zoom
        type: string
        default: "Auto"
        description: Auto-zoom to fill frame after stabilization
    difficulty: beginner
  - name: color-page-tracker
    description: Advanced tracking on Color page for power windows, qualifiers, and effects
    parameters:
      - name: tracker_mode
        type: string
        enum: ["Point", "Planar", "Surface"]
        default: "Point"
        description: Point for simple tracks, Planar for surfaces, Surface for corner-pin
      - name: reference_frame
        type: string
        description: Frame number to start tracking from
      - name: track_forward
        type: boolean
        default: true
      - name: track_backward
        type: boolean
        default: false
    difficulty: intermediate
  - name: power-window-tracking
    description: Track Power Windows to follow moving subjects for isolated grading
    parameters:
      - name: window_shape
        type: string
        enum: ["Circle", "Square", "Custom", "Curve"]
        default: "Circle"
      - name: softness
        type: string
        default: "Medium"
      - name: tracking_mode
        type: string
        enum: ["Point", "Planar"]
        default: "Planar"
    difficulty: intermediate
parameters:
  - name: resolve_page
    type: string
    default: "Edit|Color"
    description: Edit page for clip stabilization, Color page for tracked grades
  - name: node_graph_type
    type: string
    default: "serial"
---

# DaVinci Resolve Stabilization & Motion Tracking

Stabilization and motion tracking workflows in DaVinci Resolve for smoothing handheld footage, gimbal moves, and tracking subjects for isolated grading or effects.

## Video References

| Technique | Video ID | Key Nodes/Tools | Tags |
|-----------|----------|-----------------|------|
| Smartphone Gimbal Stabilization for Real Estate | C0B6gaTt6nm | Clip, Transform, Stabilizer | stabilization, gimbal, smartphone, real estate, videography, tutorial |
| Instagram Reel C1CATqWiahJ - The Gimbal Move | C1CATqWiahJ | Color Correction Node, Motion Tracking Node | gimbal move, color correction, motion tracking |

## Core Workflows

### 1. Edit Page Inspector Stabilization (Quick, Clip-Level)
**Reference**: C0B6gaTt6nm (Smartphone Gimbal Stabilization for Real Estate)

**Best for**: Quick stabilization of handheld/smartphone/gimbal footage before editing.

```
Inspector → Video → Stabilization
├── Mode: Perspective (default, handles 3D camera movement)
│   ├── Similarity: Rotation + Scale + Position (no perspective)
│   └── Translation: Position only (fastest, least crop)
├── Smoothness: Low / Medium / High
│   ├── Low: Subtle, minimal crop
│   ├── Medium: Balanced (recommended start)
│   └── High: Maximum smoothing, significant crop
├── Camera Lock: Off / On
│   └── On: Locks camera position entirely (tripod simulation)
├── Zoom: Auto / Off
│   └── Auto: Scales clip to hide black borders
└── Cropping Ratio: Displays crop percentage after analysis
```

**Steps** (from C0B6gaTt6nm):
1. Import smartphone footage into DaVinci Resolve
2. Place clip on timeline in Edit page
3. Select clip → Open Inspector panel
4. Go to Transform section → Enable Stabilizer
5. Choose **Mode: Perspective** (for gimbal/walkthrough moves)
6. Set **Smoothness: Medium**
7. Click **Analyze** - Resolve analyzes frame-by-frame
8. Review stabilized footage
9. Adjust **Crop Amount** if black borders appear (Automatic recommended)

**Mode Selection Guide**:
| Footage Type | Recommended Mode | Reason |
|--------------|------------------|--------|
| Gimbal/walkthrough | Perspective | Handles 3D parallax |
| Handheld walking | Perspective | Complex motion |
| Tripod with vibration | Translation | Minor position jitter |
| Drone footage | Similarity | Rotation/scale dominant |
| Locked-off with shake | Translation | Position only |

### 2. Color Page Tracker (Advanced, Grade-Level)
**Reference**: C1CATqWiahJ (Gimbal Move with Motion Tracking)

**Best for**: Tracking Power Windows, Qualifiers, or effects to moving subjects for isolated color grading.

```
Color Page → Tracker Panel (Window icon with crosshairs)
├── Tracker Type: Point / Planar / Surface
├── Reference Frame: Set playhead, click "Set Reference"
├── Track Forward: →
├── Track Backward: ←
├── Track All: ↔ (both directions)
├── Keyframes: Auto-generated on tracked parameters
└── Apply To: Power Window / Qualifier / Transform / OFX Plugin
```

**Steps** (from C1CATqWiahJ):
1. On Color page, select clip with gimbal move
2. Add serial node for color correction (saturation 100%, contrast 50%)
3. Add second node for Motion Tracking
4. Open Tracker panel (Window → Tracker or shortcut)
5. Choose **Tracker Type: Planar** (for surface tracking)
6. Draw tracking area over subject/feature
7. Set **Reference Frame** at clear view of subject
8. Click **Track Forward** (and Backward if needed)
9. Review track quality - adjust search area if drift occurs
10. Apply track to Power Window on color correction node
11. Grade isolated subject independently

### 3. Power Window Tracking for Isolated Grading
**Combines**: Color Correction Node + Power Window + Tracker

```
Node Structure:
├── Node 1: Primary Grade (Color Wheels)
├── Node 2: Subject Isolation
│   ├── Power Window: Circle/Square/Curve around subject
│   ├── Tracker: Planar track on window
│   ├── Softness: 20-40 (feather edge)
│   └── Grade: Subject-specific (skin tones, exposure)
└── Node 3: Background Grade
    └── Inverted Window (or separate node with inverted mask)
```

**Steps**:
1. Add serial node for subject isolation
2. Select Power Window tool (circle/square/curve)
3. Draw window around subject
4. Open Tracker panel, choose **Planar Tracker**
4. Track forward/backward
5. Increase **Softness** for natural blend
6. Apply grade inside window (skin tone fix, exposure)
7. Add another node with **Inverted Window** for background

### 4. Gimbal Move Enhancement (Stabilize + Track)
**Reference**: C1CATqWiahJ (The Gimbal Move)

**Workflow**: Stabilize the gimbal move, then track subject for grade separation.

```
Edit Page:
├── Clip on timeline
├── Inspector → Stabilization
│   ├── Mode: Perspective
│   ├── Smoothness: Low-Medium (preserve intentional gimbal move)
│   └── Analyze

Color Page:
├── Node 1: Primary (corrected stabilized footage)
├── Node 2: Subject Track
│   ├── Power Window + Planar Tracker on subject
│   ├── Grade: Pop subject (contrast, saturation)
└── Node 3: Background
    ├── Inverted window
    ├── Grade: Moody/atmospheric
```

## Parameters Reference

### Stabilization (Edit Page Inspector)
| Parameter | Options | Default | Notes |
|-----------|---------|---------|-------|
| Mode | Perspective / Similarity / Translation | Perspective | Perspective = most robust |
| Smoothness | Low / Medium / High | Medium | Higher = more crop |
| Camera Lock | On / Off | Off | Tripod simulation |
| Zoom | Auto / Off | Auto | Fills frame post-stabilize |
| Cropping Ratio | (Read-only) | - | Shows % crop applied |

### Tracker (Color Page)
| Parameter | Options | Default | Notes |
|-----------|---------|---------|-------|
| Tracker Type | Point / Planar / Surface | Point | Planar for surfaces |
| Reference Frame | Frame number | Current playhead | Clear feature frame |
| Search Area | Auto / Custom | Auto | Expand for fast motion |
| Track Direction | Forward / Backward / Both | Forward | Both = most accurate |
| Keyframe Interval | Every frame / Custom | Every frame | Smooth curves |

## Tips & Best Practices

1. **Stabilize First, Track Second**: Stabilize on Edit page, then track on Color page for cleanest results
2. **Don't Over-Smooth**: High smoothness crops heavily and creates "warp" artifacts
3. **Planar > Point**: Use Planar Tracker for any surface (walls, faces, products)
4. **Reference Frame Matters**: Pick frame with max contrast, minimal motion blur
5. **Check Track Quality**: Scrub timeline, watch for drift - re-track sections if needed
6. **Softness is Key**: 20-40 softness on Power Windows prevents hard edges
7. **Version Before Stabilizing**: Create timeline version (Timeline → Duplicate) before analyzing

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Warping/distortion | Perspective mode on pure rotation | Switch to Similarity mode |
| Excessive crop | High smoothness + wide lens | Lower smoothness, accept some shake |
| Tracker loses target | Motion blur, occlusion | Increase search area, manual keyframe |
| Jitter after stabilize | Rolling shutter | Enable "Rolling Shutter" in Project Settings |
| Black borders | Zoom off or insufficient | Enable Zoom: Auto |

## Related Skills
- `davinci-resolve-color-grading-fundamentals` - Power Window grading
- `instagram-reel-editing-techniques` - Stabilization for Reels
- `davinci-resolve-fusion-tracking` - Fusion planar/camera tracker