---
name: davinci-gimbal-stabilization-techniques
description: DaVinci Resolve gimbal and stabilization techniques — in-camera gimbal setup, post-production stabilization, camera movement analysis, and smooth footage workflows from 5 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [gimbal, stabilization, camera-movement, davinci-resolve, video-stabilization, smooth-footage, gimbal-techniques]
trigger: Use when user wants to stabilize footage, set up gimbal, or analyze camera movement in DaVinci Resolve
parameters:
  - name: technique
    description: Specific technique to apply
    type: string
    enum: [gimbal-setup, in-camera-stabilization, post-stabilization, camera-tracking, movement-analysis]
    default: post-stabilization
  - name: footage_type
    description: Type of footage being stabilized
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

# DaVinci Resolve Gimbal & Stabilization Techniques

**Cluster:** 5 techniques — 3 tagged "gimbal", 3 tagged "stabilization", 2 tagged "camera movement/tracking"

## Techniques Covered

| Reel | Technique | Type | Key Tools |
|------|-----------|------|-----------|
| C91G59fPx0Q | Gimbal Tip — smooth steady shot | In-camera | Gimbal settings |
| C9L5b-7Ppnb | 6 Tips for Gimbal Beginners | In-camera + Post | Color correction + Stabilizer node |
| C5FYbsZvZfH | Gimbal Stabilization Technique | Post | Stabilizer Node |
| C8zcAmnvxT9 | Gimbal Shooting + Color Correction | Hybrid | Import/Organize + Color Correction |
| C8WE9KionAk | Camera Movement Tracking | Post/VFX | Camera Tracker node |

---

## Gimbal Setup (In-Camera) — From C91G59fPx0Q, C9L5b-7Ppnb

### Physical Balance (Critical First Step)
```
1. Mount camera → Slide plate until balanced front/back
2. Balance ROLL → Adjust roll arm until camera stays level
3. Balance TILT → Tilt up/down, adjust until stable at any angle
4. Balance PAN → Pan left/right, fine-tune for no drift
```
**Test**: Power on → Hold gimbal still → No motor noise = balanced

### Gimbal Follow Modes (C9L5b-7Ppnb)
| Mode | Axes Active | Best For |
|------|-------------|----------|
| **PF (Pan Follow)** | Pan only | Walking shots, horizon lock |
| **PTF (Pan Tilt Follow)** | Pan + Tilt | Run-and-gun, following subject |
| **FPV (First Person View)** | All 3 axes | Immersive, dynamic movement |
| **Lock** | None (all locked) | Fixed direction, vehicle mount |
| **POV** | Tilt follows, Pan locked | POV shots, simulate head movement |

### Key Settings to Tune
| Setting | Range | Recommendation |
|---------|-------|----------------|
| **Motor Strength** | Low/Med/High/Max | Match camera weight — heavier = higher |
| **Follow Speed** | 1-100 | 5-15 smooth, 20+ fast action |
| **Deadband** | 0.1-5° | 0.5-1.5° ignores micro-shake |
| **SmoothTrack** | On/Off | On for organic, off for precise |
| **Control Stick Sensitivity** | 1-100 | 20-40 for slow cinematic pans |

---

## Post-Production Stabilization — From C5FYbsZvZfH, C9L5b-7Ppnb

### DaVinci Resolve Stabilizer (Edit/Color Page Inspector)
```
Select clip → Inspector → Stabilization
  Mode: Perspective (default, handles rotation)
        Similarity (rotation + scale, no perspective)
        Translation (position only, fastest)
  Camera Lock: On = tripod simulation
  Zoom: Auto (crops to hide edges)
  Smooth: 0.0-1.0 (start 0.25, adjust)
  Strength: 0.0-1.0 (start 0.5, adjust)
```

### Settings by Strength Level
| Strength | Smooth | Zoom | Cropping | Use Case |
|----------|--------|------|----------|----------|
| **Light** | 0.15 | 1-2% | Minimal | Gimbal footage, minor micro-jitter |
| **Medium** | 0.35 | 3-5% | Moderate | Handheld, walking shots |
| **Strong** | 0.7+ | 5-10% | Heavy | Run-and-gun, action cam |

### Workflow (C5FYbsZvZfH)
```
1. Import gimbal footage to Media Pool
2. Cut to timeline → Select clip
3. Inspector → Stabilization → Analyze
4. Choose Mode → Perspective for gimbal
5. Adjust Smoothness → Preview in viewer
6. Check edges → Increase Zoom if black borders
7. Render cache for smooth playback
```

### Advanced: Stabilizer Node (Color Page)
```
Color Page → Node Graph
  Right-click → Add Node → Stabilizer
  More control: per-axis, keyframeable, before/after grade
```
**Use when**: Stabilization needs vary across clip (e.g., static then handheld)

---

## Camera Tracking — From C8WE9KionAk

### Fusion Camera Tracker (for VFX/Motion Graphics)
```
Fusion Page:
  1. MediaIn (source clip)
  2. CameraTracker tool
  3. Track Features → Auto Track
  4. Solve Camera → Get 3D camera + point cloud
  5. Export: 3D Camera for compositing
```

### Settings
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Track Threshold** | 0.01-0.05 | Lower = more points |
| **Min Track Length** | 8-16 frames | Longer = more stable |
| **Focal Length** | Known or "Auto" | Enter if known (EXIF) |
| **Sensor Size** | Match camera | APS-C, Full Frame, MFT, 1" |

### Output Uses
- **3D Text/Objects**: Place in tracked scene
- **Screen Replacement**: Corner pin to tracked plane
- **Stabilization Reference**: Use solved camera to reverse-engineer shake
- **Matchmove**: Composite CG elements

---

## Movement Analysis — From C6bSKc5AtaF, C5BIe_vArAP

### Analyzing Camera Movement
```
1. Scrub timeline → Identify move type:
   Pan / Tilt / Dolly / Truck / Pedestal / Roll / Combination
2. Mark keyframes on Transform (Edit page):
   Position X/Y, Rotation, Zoom
3. Graph Editor (Opt+F / Alt+F):
   Smooth curves → Bezier → Ease In/Out
4. Speed Ramp (Retime):
   Cmd+R → Add speed points → Curve for drama
```

### Movement Types & Stabilization Strategy
| Move Type | Description | Stabilize? | Approach |
|-----------|-------------|------------|----------|
| **Static/Locked** | No intentional movement | Yes (micro-shake) | Light Perspective |
| **Pan** | Horizontal rotation | Light | Preserve pan, smooth jitter |
| **Tilt** | Vertical rotation | Light | Preserve tilt |
| **Dolly/Truck** | Linear translation | Medium | Smooth velocity curve |
| **Crane/Pedestal** | Vertical translation | Medium | Smooth acceleration |
| **Orbit** | Circular around subject | Light | Track subject, stabilize radius |
| **FPV/Free** | All axes | Careful | May want raw energy |

### Speed Ramping for Cinematic Effect
```
Retime Controls (Cmd+R):
  • 100% → 50% at move start (emphasize)
  • 50% → 200% mid-move (energy)
  • 200% → 100% at end (settle)
  • Use Optical Flow (Speed Warp) for clean slow-mo
  • Curve: Bezier for natural acceleration
```

---

## Hybrid Workflow: Gimbal + Color (C8zcAmnvxT9)

### Step 1: Import & Organize
```
Media Pool:
  Master/
    ├── A_Cam/
    ├── B_Cam/
    ├── Gimbal/
    │   ├── Morning_Walk/
    │   ├── Evening_Orbit/
    │   └── Reveals/
    └── Drone/
```

### Step 2: Stabilize (if needed)
```
Gimbal bin → Select all → Right-click → "Stabilize Clips"
  Mode: Perspective
  Smooth: 0.2
  Process in background
```

### Step 3: Color Correction
```
Color Page → Per clip:
  Node 1: Primary (Exposure, WB, Contrast)
  Node 2: Creative (Saturation, Look)
  Node 3: Output (CST/LUT)
```
**Gimbal-specific grading**:
- Sky often overexposed → Power Window (Gradient) → Highlights -20
- Ground underexposed → Power Window (Inverse) → Shadows +15
- Consistent look across moves → Grab Still → Apply Grade

---

## Pro Tips from Reels

- **C91G59fPx0Q**: "Adjust gimbal settings to achieve smooth and steady shot" — In-camera > post
- **C9L5b-7Ppnb**: "Color correction + gimbal stabilization node" — Combine in Color page
- **C5FYbsZvZfH**: "Stabilizer Node" — Color page node for per-axis control
- **C8zcAmnvxT9**: "Import and organize footage, then apply color correction" — Organize first
- **C8WE9KionAk**: "Use Camera Tracker node to track camera movement" — Fusion for 3D

---

## Common Gimbal/Stabilization Issues & Fixes

| Issue | In-Camera Fix | Post Fix |
|-------|---------------|----------|
| **Horizon drift** | Recalibrate IMU, balance roll | Keyframe Rotation in Transform |
| **Micro-jitter (walking)** | Increase deadband, slower follow | Stabilizer: Perspective, Smooth 0.2 |
| **Z-axis bounce (up/down)** | Softer arm, walk heel-toe | Stabilizer: Translation only |
| **Motor noise in audio** | External mic, distance | N/A (prevention only) |
| **Rolling shutter skew** | Faster shutter, ND filters | Fusion: Vector Motion Blur / Rolling Shutter Repair |
| **Subject drift in frame** | Lock mode, or PF with subject tracking | Keyframe Position to re-center |

---

## Export Settings for Stabilized Footage

| Delivery | Resolution | Codec | Notes |
|----------|------------|-------|-------|
| **Social (Reels/TikTok)** | 1080x1920 | H.264 20Mbps | Vertical crop from 4K |
| **YouTube 4K** | 3840x2160 | H.265 50-80Mbps | Tag HDR if graded PQ |
| **Client Review** | 1920x1080 | ProRes 422 HQ | Fast decode, minimal loss |
| **Archive** | Native | ProRes 4444 | Preserve all data |

---

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Grading stabilized footage
- `davinci-fusion-camera-tracking` — Advanced 3D tracking
- `davinci-speed-ramping-retiming` — Speed ramps for movement
- `davinci-drone-cinematic-workflow` — Drone-specific stabilization