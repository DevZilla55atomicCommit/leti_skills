---
name: davinci-gimbal-stabilization-camera-movement
description: DaVinci Resolve gimbal stabilization and camera movement techniques — in-camera gimbal setup, post-production stabilization, camera tracking, and movement analysis from 5 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [gimbal, stabilization, camera-movement, camera-tracking, davinci-resolve, video-stabilization, smooth-footage]
trigger: Use when user wants to stabilize footage, set up gimbal, or analyze camera movement in DaVinci Resolve
parameters:
  - name: technique
    description: Specific technique to apply
    type: string
    enum: [gimbal-setup, in-camera-stabilization, post-stabilization, camera-tracking, movement-analysis]
    default: post-stabilization
  - name: footage_type
    description: Type of footage
    type: string
    enum: [gimbal, handheld, drone, tripod]
    default: gimbal
  - name: stabilization_strength
    description: Stabilization intensity
    type: string
    enum: [light, medium, strong]
    default: medium
steps:
  - step: In-camera gimbal setup
    description: Balance gimbal, configure follow modes, calibrate IMU
  - step: Import and organize footage
    description: Media Pool → create bins for gimbal shots
  - step: Apply DaVinci Resolve stabilization
    description: Inspector → Stabilization → choose mode (Perspective/Similarity/Translation)
  - step: Camera tracking for VFX/motion graphics
    description: Fusion → Camera Tracker → solve 3D camera
  - step: Analyze and refine movement
    description: Use keyframes to smooth residual motion
---

# DaVinci Resolve Gimbal Stabilization & Camera Movement

**Cluster:** 5 techniques — 3 tagged "gimbal", 3 tagged "stabilization", 2 tagged "camera movement/tracking"

## Techniques Covered

| Reel | Technique | Type | Key Nodes/Tools |
|------|-----------|------|-----------------|
| C91G59fPx0Q | Gimbal Tip — smooth steady shot | In-camera | Gimbal settings |
| C9L5b-7Ppnb | 6 Tips for Gimbal Beginners | In-camera + Post | Color correction + Stabilizer node |
| C5FYbsZvZfH | Gimbal Stabilization Technique | Post | Stabilizer Node |
| C8zcAmnvxT9 | Gimbal Shooting + Color Correction | Hybrid | Import/Organize + Color Correction |
| C8WE9KionAk | Camera Movement Tracking | Post/VFX | Camera Tracker node |

## Gimbal Setup (In-Camera) — From C91G59fPx0Q, C9L5b-7Ppnb

### Physical Balance
1. **Mount camera** — Slide plate until balanced front/back
2. **Balance roll** — Adjust roll arm until camera stays level
3. **Balance tilt** — Tilt up/down, adjust until stable
4. **Balance pan** — Pan left/right, fine-tune

### Gimbal Modes (per C9L5b-7Ppnb)
| Mode | Use Case |
|------|----------|
| **PF (Pan Follow)** | Walking shots — pan follows, tilt locked |
| **PTF (Pan Tilt Follow)** | Run/gun — both follow |
| **FPV (First Person)** | All axes follow — immersive |
| **Lock** | All axes locked — fixed direction |
| **POV** | Tilt follows, pan locked — POV shots |

### Settings to Adjust
- **Motor strength**: Higher for heavier cameras
- **Follow speed**: 5-15 for smooth, 20+ for fast action
- **Deadband**: 0.5-2° — ignore micro-movements
- **SmoothTrack**: Enable for organic feel

## Post-Production Stabilization — From C5FYbsZvZfH, C9L5b-7Ppnb, C4nzM9hgcbb

### DaVinci Resolve Stabilizer (Edit/Color Page)
```
Inspector → Stabilization → Mode:
  • Perspective (default) — full 3D, handles rotation
  • Similarity — rotation + scale, no perspective
  • Translation — position only, fastest
```

### Settings by Strength
| Strength | Smoothness | Zoom | Cropping |
|----------|------------|------|----------|
| Light | 0.15-0.25 | 1-2% | Minimal |
| Medium | 0.3-0.5 | 3-5% | Moderate |
| Strong | 0.6-1.0 | 5-10% | Heavy |

### Workflow (C5FYbsZvZfH)
1. **Import gimbal footage** to Media Pool
2. **Cut to timeline** — select clip
3. **Inspector → Stabilization** → Analyze
4. **Choose mode** → Perspective for gimbal
5. **Adjust Smoothness** → Start 0.3, preview
6. **Check edges** — increase Zoom if black borders appear

### Advanced: Stabilizer Node (Color Page)
- Right-click node graph → Add Node → Stabilizer
- More control: per-axis, keyframeable
- Use when: stabilization varies across clip

## Camera Tracking — From C8WE9KionAk

### Fusion Camera Tracker
1. **Fusion page** → MediaIn (clip)
2. **Add CameraTracker** tool
3. **Track features** → Auto-track or manual
4. **Solve camera** → Get 3D camera + point cloud
5. **Export** → 3D camera for compositing/VFX

### Settings
- **Track threshold**: 0.01-0.05 (lower = more points)
- **Min track length**: 8-16 frames
- **Focal length**: Known or "Auto"
- **Sensor size**: Match camera (APS-C, Full Frame, MFT)

## Movement Analysis — From C6bSKc5AtaF, C5BIe_vArAP

### Analyzing Camera Movement
1. **Scrub timeline** — note pan/tilt/roll/dolly
2. **Mark keyframes** on Transform (Position/Rotation)
3. **Graph editor** — smooth curves (Bezier → ease in/out)
4. **Speed ramping** — retime for dramatic effect

### Movement Types (C5BIe_vArAP: "video movements")
| Type | Description | Stabilization Approach |
|------|-------------|------------------------|
| Pan | Horizontal rotation | Perspective mode |
| Tilt | Vertical rotation | Perspective mode |
| Dolly | Physical move forward/back | Similarity mode |
| Truck | Physical move left/right | Similarity mode |
| Crane | Vertical lift | Perspective + keyframe |
| Handheld shake | High-frequency micro-motion | Strong stabilization |
| Gimbal drift | Slow unwanted rotation | Keyframe correction |

## Combined Workflow: Gimbal Shoot → Post Stabilize → Grade

```
SHOOT (C91G59fPx0Q, C9L5b-7Ppnb)
  ├─ Balance gimbal perfectly
  ├─ Choose mode (PF/PTF/FPV)
  ├─ Shoot with smooth movements
  └─ Record at high frame rate (60fps+) for slow-mo option

EDIT (C5FYbsZvZfH, C4nzM9hgcbb)
  ├─ Import → bins by shot type
  ├─ Stabilize: Perspective, Smooth 0.3
  ├─ Check for warp artifacts at edges
  └─ Nest stabilized clip if needed

COLOR (C8zcAmnvxT9)
  ├─ Primary correction (exposure, WB)
  ├─ Creative grade (LUT or manual)
  └─ Match across gimbal shots

FUSION (C8WE9KionAk)
  ├─ Camera track for VFX integration
  ├─ Export 3D camera data
  └─ Composite graphics into tracked scene
```

## Pro Tips from Reels

- **C91G59fPx0Q**: "Freely adjust gimbal settings to meet your needs — no one setting fits all"
- **C9L5b-7Ppnb**: "Stabilization Strength: Medium works for most gimbal footage"
- **C5FYbsZvZfH**: "Import → Apply stabilization effect — simple 2-step"
- **C8WE9KionAk**: "Camera Tracker node solves 3D camera for VFX integration"
- **C6bSKc5AtaF**: "Analyze video movement first, then apply color correction"

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Warping/distortion | Over-stabilization | Reduce Smoothness, use Similarity mode |
| Black borders | Zoom insufficient | Increase Zoom, or crop in Edit |
| Rolling shutter skew | Fast pan + CMOS sensor | Perspective mode + reduce speed |
| Gimbal motor noise in audio | Mechanical vibration | External mic, or strip audio in Fairlight |
| Drift over time | IMU calibration off | Recalibrate gimbal before shoot |

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Grade stabilized footage
- `davinci-fusion-camera-tracking` — Deep dive on Fusion CameraTracker
- `davinci-speed-ramping-retiming` — Dramatic movement speed changes