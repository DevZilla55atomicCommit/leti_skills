---
name: davinci-resolve-camera-movement-techniques
description: Camera movement analysis and replication techniques in DaVinci Resolve. Use for learning gimbal moves, drone shots, dolly/slider moves, and applying digital camera movement in post (Transform, Dynamic Zoom, Speed Warp).
trigger: User wants to learn, analyze, or replicate camera movements (gimbal, drone, dolly, slider) in DaVinci Resolve.
category: davinci-resolve
tags:
  - camera movement
  - gimbal
  - drone
  - dolly
  - slider
  - dynamic zoom
  - transform
  - davinci resolve
  - video movements
steps:
  - name: analyze-camera-move
    description: Analyze camera movement type from reference footage
    parameters:
      - name: movement_type
        type: string
        enum: ["Gimbal Walkthrough", "Drone Orbit/Reveal", "Dolly In/Out", "Slider Lateral", "Push/Pull (Dolly)", "Handheld Shake", "Static/Tripod", "Whip Pan", "Tilt Up/Down", "Crane/Jib"]
        description: Identify the movement type
      - name: speed_profile
        type: string
        enum: ["Constant", "Ease In", "Ease Out", "Ease In-Out", "Speed Ramp"]
        default: "Ease In-Out"
      - name: axis
        type: string
        enum: ["X (Pan)", "Y (Tilt)", "Z (Dolly/Push)", "XY (Arc/Orbit)", "XYZ (Complex)"]
    difficulty: beginner
  - name: digital-camera-move-transform
    description: Create digital camera moves using Transform keyframes (Pan, Tilt, Zoom, Rotation)
    parameters:
      - name: anchor_point
        type: string
        default: "Center or Subject"
        description: Set anchor to subject for natural rotation/scale
      - name: keyframe_interpolation
        type: string
        enum: ["Linear", "Bezier", "Ease In", "Ease Out", "Ease In-Out"]
        default: "Ease In-Out"
      - name: motion_blur
        type: boolean
        default: true
        description: Enable Motion Blur in Inspector for realism
      - name: resolution_loss
        type: string
        default: "Acceptable up to 150% zoom on 4K→1080"
    difficulty: beginner
  - name: dynamic-zoom-keyframed-framing
    description: Use Dynamic Zoom (Edit page) for automatic Ken Burns style moves
    parameters:
      - name: dynamic_zoom_mode
        type: string
        enum: ["Linear", "Ease In", "Ease Out", "Ease In-Out", "Custom"]
        default: "Ease In-Out"
      - name: start_framing
        type: string
        default: "Wide establishing"
      - name: end_framing
        type: string
        default: "Tight on subject"
      - name: swap_direction
        type: boolean
        default: false
    difficulty: beginner
  - name: speed-ramp-gimbal-move
    description: Enhance gimbal moves with speed ramping (Retime Curve)
    parameters:
      - name: ramp_points
        type: string
        default: "100% → 50% (emphasize) → 150% (transition) → 100%"
      - name: optical_flow
        type: boolean
        default: true
      - name: motion_estimation
        type: string
        enum: ["Standard", "Enhanced (Studio)"]
        default: "Enhanced"
    difficulty: intermediate
parameters:
  - name: resolve_page
    type: string
    default: "Edit|Color"
    description: Edit for Transform/Dynamic Zoom, Color for Dynamic Zoom keyframes
  - name: source_resolution
    type: string
    default: "4K+ recommended for digital zoom"
    description: Higher resolution = more digital zoom headroom
---

# DaVinci Resolve Camera Movement Techniques

Analyze, replicate, and enhance camera movements in DaVinci Resolve: gimbal walks, drone orbits, dolly pushes, slider moves, and digital camera moves in post.

## Video References

| Technique | Video ID | Key Tools | Tags |
|-----------|----------|-----------|------|
| Video Movements Analysis | C4DeCQYAWMg | node1, node2 | video editing, color correction, instagram reel |
| Video Movements | C4L7p2vpxGR | node1, node2 | video movements |
| The Gimbal Move | C1CATqWiahJ | Color Correction, Motion Tracking | gimbal move, motion tracking |
| Camera Tips with Bell | C1Lcmsht6J9 | node1, node2 | camera tips, bell shot |
| The Rock Camera Movement | - | - | camera movement |
| Car Camera Movement | - | - | car photography |
| Motorcycle Camera Movement | - | - | motorcycle |

## Camera Movement Taxonomy

### Physical Movements (In-Camera)
| Type | Description | Typical Use |
|------|-------------|-------------|
| **Gimbal Walkthrough** | Smooth 3-axis stabilized walk | Real estate, venue tours, follow subject |
| **Drone Orbit/Reveal** | Circular/ascending around subject | Establishing shots, epic reveals |
| **Dolly Push/Pull** | Linear track in/out on subject | Emphasis, intimacy, reveal |
| **Slider Lateral** | Side-to-side on track | Parallax depth, product showcase |
| **Crane/Jib** | Vertical sweep up/down | Scale, grandeur, transition |
| **Handheld** | Organic shake | Energy, urgency, documentary |
| **Whip Pan** | Fast blur transition | Scene change, energy |
| **Tilt Up/Down** | Vertical rotation | Reveal height, connect sky/ground |

### Digital Movements (In-Post)
| Type | Tool | Best For |
|------|------|----------|
| **Digital Pan/Tilt** | Transform (Position) | Reframing, subtle reposition |
| **Digital Dolly (Zoom)** | Transform (Zoom) | Push in/out from static shot |
| **Digital Rotation** | Transform (Rotation) | Dutch angle, level horizon |
| **Ken Burns (Dynamic Zoom)** | Dynamic Zoom | Photo animation, slow drift |
| **Speed Ramp** | Retime Curve | Emphasize moment, transition |
| **3D Camera Track** | Fusion Camera Tracker | Add 3D elements, stabilize |

## Workflow 1: Analyze Reference Movement

**Steps** (from C1Lcmsht6J9, C4DeCQYAWMg):
1. Import reference clip to timeline
2. Play at 0.25x speed, observe:
   - **Primary Axis**: X (pan), Y (tilt), Z (dolly), or combination
   - **Speed Profile**: Constant / Ease In / Ease Out / Ease In-Out / Ramped
   - **Parallax**: Foreground vs background speed difference (indicates 3D move)
   - **Rotation**: Any roll/yaw/pitch?
   - **Stabilization**: Smooth (gimbal) vs organic (handheld) vs locked (tripod)
3. Note keyframes: Start frame, end frame, any inflection points

## Workflow 2: Digital Camera Move (Transform Keyframes)

**Edit Page → Inspector → Transform**

```
Transform Settings:
├── Zoom (X/Y linked): 1.0 → 1.3 (Digital dolly push)
├── Position X: 0.0 → -0.15 (Pan right)
├── Position Y: 0.0 → 0.1 (Tilt down)
├── Rotation: 0.0 → 1.5° (Subtle Dutch/level)
├── Anchor Point: X=0.5, Y=0.5 (Center) OR Subject position
└── Keyframes: Set at In/Out points + any mid-move changes
```

**Anchor Point Critical Rule**:
- **Center (0.5, 0.5)**: Rotation/scale from frame center (standard)
- **Subject (e.g., 0.5, 0.3)**: Rotation/scale around subject (natural for dolly/tilt)
- **To set**: Click anchor crosshair → Click subject in viewer

**Keyframe Interpolation**:
| Interpolation | Feel | Use Case |
|---------------|------|----------|
| Linear | Mechanical, constant | Technical moves |
| Ease In | Starts slow, accelerates | Pull out, reveal |
| Ease Out | Decelerates to stop | Push in, settle |
| Ease In-Out | Smooth start & stop | Natural camera move |
| Bezier | Custom curve | Complex multi-phase |

**Motion Blur** (Essential for realism):
```
Inspector → Transform → Motion Blur: ON
├── Shutter Angle: 180° (standard)
├── Samples: 8-16 (quality vs render time)
└── Apply to: Transform only (not Crop)
```

**Resolution Headroom**:
| Source → Timeline | Max Clean Zoom | Notes |
|-------------------|----------------|-------|
| 8K → 4K | 200% | Full flexibility |
| 6K → 4K | 150% | Good |
| 4K → 1080p | 200% | Excellent |
| 4K → 4K | 110-120% | Minimal, use Super Scale (Studio) |

## Workflow 3: Dynamic Zoom (Ken Burns for Video)

**Edit Page → Inspector → Dynamic Zoom**

```
Dynamic Zoom Settings:
├── Mode: Ease In-Out (most natural)
├── Start: Green box (initial framing)
├── End: Red box (final framing)
├── Swap: Reverses direction
└── Works on: Video clips, stills, adjustment clips
```

**Dynamic Zoom vs Transform Keyframes**:
| Feature | Dynamic Zoom | Transform Keyframes |
|---------|--------------|---------------------|
| Ease of Use | ★★★★★ | ★★★☆☆ |
| Custom Paths | No (straight line) | Yes (any curve) |
| Rotation | No | Yes |
| Anchor Control | Center only | Any point |
| Speed Graph | Preset only | Full control |
| Best For | Photos, simple drift | Complex moves, video |

## Workflow 4: Speed Ramping for Movement Emphasis

**Reference**: C1CATqWiahJ (Gimbal move enhancement)

```
Retime Curve (Ctrl+R / Right-click clip → Retime Controls):
├── Enable Retime Curve
├── Add Keyframes at:
│   ├── 0%: 100% speed (normal)
│   ├── 30%: 50% speed (slow - emphasize move)
│   ├── 60%: 150% speed (fast - transition feel)
│   └── 100%: 100% speed (return normal)
├── Interpolation: Optical Flow (Speed Warp)
└── Motion Estimation: Enhanced (Studio) / Standard
```

**Speed Ramp Patterns by Move Type**:

| Move Type | Ramp Pattern | Purpose |
|-----------|--------------|---------|
| Gimbal Walkthrough | 100% → 40% (at feature) → 120% | Highlight architectural detail |
| Drone Reveal | 100% → 30% (at subject) → 100% | Dramatic subject reveal |
| Dolly Push | 100% → 50% (approach) → 80% | Intimate approach |
| Whip Pan | 100% → 300% (blur) → 100% | Transition energy |
| Slider Parallax | 100% → 60% (depth moment) → 100% | Show depth layers |

## Workflow 5: Fusion 3D Camera Moves (Advanced)

**For**: Adding 3D elements, complex parallax, virtual camera

```
Fusion Page:
├── MediaIn
├── CameraTracker (Analyze → Solve)
│   ├── Track Features: 100+
│   ├── Solve: Camera Only / Camera + Scene
│   └── Focal Length: Known / Auto
├── Camera3D (From tracker or manual)
│   ├── Position/Animation: Keyframe or expression
│   └── Focal Length: Match source
├── Renderer3D
│   ├── Input: Camera3D
│   └── Scene: 3D elements (text, particles, imports)
└── MediaOut
```

**Manual 3D Camera (No Tracker)**:
```
Camera3D:
├── Position: Keyframe X/Y/Z for dolly/crane
├── Rotation: Keyframe for pan/tilt/roll
├── Focal Length: Animate for zoom (not Zoom parameter!)
├── Aperture: Match source sensor
└── Projection: Perspective
```

## Workflow 6: Stabilize + Digital Move Combo

**Best Practice**: Stabilize first, then add intentional digital move

```
Edit Page:
├── Clip on timeline
├── Inspector → Stabilization
│   ├── Mode: Perspective (gimbal) / Similarity / Translation
│   ├── Smoothness: Low-Medium (keep some organic feel)
│   └── Analyze
├── THEN: Transform keyframes for digital dolly/pan
└── Motion Blur: ON
```

## Instagram Reel Specific Moves (9:16 Vertical)

| Move | Transform Settings | Reel Use Case |
|------|-------------------|---------------|
| **Vertical Reveal** | Position Y: -0.3 → 0.3, Zoom: 1.0 → 1.2 | Tall subject (building, waterfall) |
| **Subject Push** | Zoom: 1.0 → 1.5, Anchor: Subject face | Portrait emphasis |
| **Environment Pan** | Position X: -0.2 → 0.2, Tilt: -5° → 5° | Show location context |
| **Rotation Reveal** | Rotation: -10° → 10°, Zoom: 1.1 | Dynamic transition |
| **Speed Ramp Drop** | Retime: 100% → 20% (beat) → 150% | Beat-sync transition |

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Jittery digital move | Too many keyframes, Linear interpolation | Reduce keyframes, use Ease In-Out |
| Warped perspective | Digital zoom + pan on wide lens | Keep zoom <120%, use anchor point |
| Motion blur missing | Motion Blur off | Enable in Transform Inspector |
| Quality loss | Over-zoom on low-res | Shoot 4K+, use Super Scale (Studio) |
| Unnatural speed | Linear retime curve | Use Bezier/Ease In-Out on Retime Curve |
| Anchor point drift | Forgot to set anchor | Set anchor to subject BEFORE keyframing |

## Related Skills
- `davinci-resolve-stabilization-tracking` - Stabilizer, Tracker
- `davinci-resolve-transitions-effects` - Speed ramp transitions
- `davinci-resolve-fusion-compositing` - 3D camera tracker
- `instagram-reel-editing-techniques` - Reel-specific pacing