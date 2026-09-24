---
name: fusion-3d-camera-tracking
description: 3D camera tracking and object integration in DaVinci Resolve Fusion — CameraTracker, 3D camera solve, 3D model import (OBJ/FBX), Merge3D, Renderer3D, and compositing 3D elements into tracked footage for VFX, automotive, and motion graphics.
trigger: User needs to integrate 3D objects (cars, text, graphics) into live-action footage with camera movement
category: davinci-resolve-fusion
tags:
  - VFX
  - 3D
  - Camera Tracking
  - Fusion
  - compositing
  - 3D integration
  - automotive
  - motion graphics
parameters:
  - name: tracking_mode
    description: CameraTracker analysis mode
    default: "Auto (default) or Manual Plan for complex shots"
    type: string
  - name: solve_method
    description: Camera solve type
    default: "Perspective (standard) or Tripod Pan/Tilt/Zoom for static camera"
    type: string
  - name: model_format
    description: 3D model file format
    default: "OBJ, FBX, or glTF (FBX recommended for animation)"
    type: string
  - name: projection_type
    description: Camera projection
    default: "Perspective (default)"
    type: string
  - name: lighting_setup
    description: 3D scene lighting
    default: "HDRI Environment + Key/Fill Point Lights"
    type: string
steps:
  - step: "Fusion Page: Add CameraTracker node → Connect to MediaIn (footage)"
  - step: "CameraTracker: Click 'Track' → Analyze features (default Auto) → Review track points, delete bad ones"
  - step: "CameraTracker: Click 'Solve' → Choose Perspective (moving camera) or Tripod (static) → Check solve error (< 1.0 px ideal)"
  - step: "Right-click CameraTracker → 'Create 3D Camera' → Adds Camera3D + Tracker points to 3D space"
  - step: "Add Loader/Import3D node → Load 3D model (OBJ/FBX) → Connect to Merge3D"
  - step: "Add Merge3D node → Connect Camera3D (from solve) + 3D Model → Merge3D"
  - step: "Add Renderer3D → Connect Merge3D output → Set Renderer3D Camera input to Camera3D"
  - step: "Add ImagePlane (background footage) → Connect to Merge3D (or Merge 2D over Renderer3D)"
  - step: "Align 3D model: Use Transform3D on model to position/scale/rotate to match floor/perspective"
  - step: "Lighting: Add Light3D (Point/Directional) + EnvironmentMap (HDRI) → Connect to Merge3D"
  - step: "Renderer3D settings: Enable Motion Blur, AA (Anti-Aliasing) 2-4x, Depth of Field if needed"
  - step: "Color page: Grade 3D render to match footage (CST, LUT, Color Wheels)"
difficulty: advanced
resolve_page: Fusion
node_graph_type: serial (3D node graph)
key_nodes:
  - CameraTracker
  - Camera3D
  - Import3D / Loader (3D)
  - Merge3D
  - Renderer3D
  - Transform3D
  - Light3D / EnvironmentMap
  - ImagePlane
source_techniques:
  - video_id: C9wagvWK8vy
    technique_name: 3D Camera Tracking and Object Integration
    tags: [VFX, 3D, Camera Tracking, Fusion]
  - video_id: C_QClmggW_f
    technique_name: 3D Car Rendering with Animation Gizmo
    tags: [3D, rendering, animation, car, Fusion]
---

# Fusion 3D Camera Tracking & Object Integration

Professional 3D camera tracking in Fusion page — solve camera motion, import 3D models (cars, products, text), composite into live footage with correct perspective, lighting, and motion blur.

## When to Use
- Product/automotive placement in real environments
- Motion graphics with 3D text/logos in tracked shots
- VFX: set extension, object replacement, screen replacement
- Virtual production previs
- Any shot needing 3D elements locked to camera move

---

## Prerequisites
- **Footage**: Good parallax, texture, minimal motion blur, 1080p+ preferred
- **Models**: OBJ/FBX with UVs, reasonable poly count (<100k tris for realtime)
- **HDRI**: For realistic lighting (Poly Haven, HDRI Haven free)
- **Resolve Studio**: Required for CameraTracker (Free version limited)

---

## Node Graph (Fusion 3D Workspace)

```
MediaIn (Footage)
    │
    ▼
CameraTracker ──▶ [Track] ──▶ [Solve] ──▶ [Create 3D Camera]
    │                                      │
    │                                      ▼
    │                              Camera3D (solved)
    │                                      │
    ▼                                      ▼
Import3D (Model) ──────▶ Transform3D ◀──── Merge3D ◀──── Light3D / EnvironmentMap
                                                │
                                                ▼
                                         Renderer3D
                                                │
                                                ▼
                                         Merge (over MediaIn)
                                                │
                                                ▼
                                         MediaOut
```

---

## Step-by-Step Workflow

### 1. Camera Tracking (CameraTracker Node)

**Add CameraTracker**:
- Fusion page → Right-click → Add Tool → Tracking → CameraTracker
- Connect **MediaIn** (footage) to CameraTracker **Input**

**Track Features**:
| Setting | Value | Notes |
|---------|-------|-------|
| **Track Mode** | Auto | Good default; Manual Plan for complex |
| **Min Features** | 100-200 | More = better solve |
| **Search Area** | 32-64 | Larger for fast motion |
| **Keyframe Interval** | 1 | Track every frame |

- Click **Track** → Wait for analysis
- **Review tracks**: Delete short/jittery tracks (red in viewer)
- **Tip**: Track 200+ features, keep 100+ good ones

**Solve Camera**:
- Click **Solve** → Choose:
  - **Perspective**: Moving camera (handheld, gimbal, drone, dolly)
  - **Tripod Pan/Tilt/Zoom**: Static position, rotating/zooming
  - **Tripod Pan/Tilt**: Static, rotating only
- **Solve Error**: Target < 1.0 pixels (0.5 = excellent)
- If error high: Delete bad tracks, re-solve, adjust focal length guess

**Create 3D Camera**:
- Right-click CameraTracker → **Create 3D Camera**
- Adds: **Camera3D** (animated) + **PointCloud3D** (track points)

---

### 2. Import & Position 3D Model (Import3D + Transform3D)

**Import Model**:
- Add Tool → 3D → Import3D (or Loader for OBJ/FBX)
- Browse to model file
- **Import Options**:
  - Units: Match scene (meters/centimeters)
  - Normals: Compute if missing
  - Animation: Enable if FBX has animation

**Position Model (Transform3D)**:
- Connect Import3D → Transform3D → Merge3D
- **Transform3D Controls**:
  - **Translate X/Y/Z**: Position on ground plane (Y=0 usually)
  - **Rotate X/Y/Z**: Match orientation to scene
  - **Scale**: Match real-world size (measure reference in footage)

**Alignment Workflow**:
1. Enable **Renderer3D** preview (wireframe/shaded)
2. Match **horizon line** → Camera3D Y rotation
3. Match **ground plane** → Model Y = 0, Camera3D Y = sensor height
4. Match **scale** → Known object size (car wheel = ~60cm)
5. Use **PointCloud3D** (track points) as reference — they sit on real geometry

---

### 3. Build 3D Scene (Merge3D)

**Merge3D Inputs**:
| Input | Connect | Purpose |
|-------|---------|---------|
| **Camera** | Camera3D (solved) | Viewpoint |
| **Scene** | Transform3D (model) | 3D objects |
| **Lights** | Light3D(s) + EnvironmentMap | Lighting |
| **Point Cloud** | PointCloud3D (optional) | Reference |

**Multiple Models**: Chain Merge3D nodes (Merge3D → Merge3D → Renderer3D)

---

### 4. Lighting (Critical for Realism)

**Environment Lighting (HDRI)**:
- Add Tool → 3D → EnvironmentMap
- Load HDRI (.hdr/.exr) → Connect to Merge3D **Environment** input
- **Rotation**: Match sun direction to footage shadows

**Key/Fill Lights**:
- Light3D (Point) → Key: Intensity 2-5, Position: 45° side, above
- Light3D (Point) → Fill: Intensity 0.5-1, Opposite side
- Light3D (Directional) → Sun: If HDRI not used

**Shadows**:
- Renderer3D → **Shadows**: On (Raytraced)
- Light3D → **Cast Shadows**: On

---

### 5. Render (Renderer3D)

**Renderer3D Settings**:
| Setting | Value | Notes |
|---------|-------|-------|
| **Width/Height** | Match timeline | 1920x1080, 3840x2160, etc. |
| **Anti-Aliasing** | 2x - 4x | 4x for final |
| **Motion Blur** | On | Shutter Angle 180° |
| **Depth of Field** | Optional | Aperture 2.8-5.6, Focus Distance match |
| **Multi-Pass** | Optional | Beauty, Depth, Normal, ObjectID for comp |

**Output**: Connect Renderer3D → Merge (over MediaIn) → MediaOut

---

### 6. Composite & Grade (Color Page)

**Merge in Fusion** (quick comp) or **Color Page** (full grade):

**Fusion Merge**:
- Merge (2D) → Foreground: Renderer3D, Background: MediaIn
- Apply **ColorCorrector** on Renderer3D output to match footage

**Color Page Workflow** (Recommended):
1. Render 3D pass with **Alpha** (Renderer3D → Savers → EXR with Alpha)
2. Import EXR sequence to Media Pool
3. Color Page: Grade 3D render to match plate:
   - **CST**: Match color space (ACES/Rec709)
   - **Color Wheels**: Match blacks, whites, skin tones
   - **Noise/Grain**: Add film grain to 3D (matches plate)
   - **Lens Effects**: Chromatic aberration, vignette, bloom

---

## Pro Tips from Source Techniques

### From C9wagvWK8vy (3D Camera Tracking):
> "Right-click tracker → 'Create 3D Camera' → Import OBJ/FBX → Merge3D with Camera3D → Align model to floor perspective → Renderer3D output"

**Key Insight**: Use **PointCloud3D** (from solve) as visual reference — track points show where real geometry sits.

### From C_QClmggW_f (3D Car Rendering):
> "Loader for car model → Transform3D for position/orient → Renderer3D → Animation Gizmo for manipulation"

**Key Insight**: **Animation Gizmo** (Transform3D with published controls) lets you animate car doors, wheels, steering in Fusion.

---

## Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Solve error > 2px | Bad tracks, wrong focal guess | Delete outlier tracks, set focal length manually |
| Model floats/sinks | Y position wrong | Match model Y=0 to ground plane using PointCloud |
| Model slides | Track not locked | Re-track with more features; check solve error |
| Lighting wrong | HDRI rotation off | Rotate EnvironmentMap to match sun |
| No motion blur | Renderer3D setting off | Enable Motion Blur, set Shutter 180° |
| Jagged edges | AA too low | AA 4x minimum for final |
| Color mismatch | Color space diff | CST on 3D render to match timeline |

---

## Advanced: Animation Gizmo (From C_QClmggW_f)

**Create Controllable Car Rig**:
1. Import car as **separate parts** (body, wheels ×4, doors ×4, steering)
2. Each part → own Transform3D
3. **Publish** Transform3D controls (Right-click → Publish) for:
   - Wheel rotation (X axis)
   - Steering (Y axis on front wheels)
   - Door opening (Y/Z on doors)
   - Body suspension (Y on body)
4. Use **Expressions** or **Keyframes** on published controls
5. **Modifier** → **Animation Gizmo** → Custom UI for animator

---

## Delivery Specs

| Pass | Format | Use |
|------|--------|-----|
| **Beauty** | EXR 16-bit/32-bit | Main comp |
| **Depth** | EXR 32-bit | DoF, fog, depth comp |
| **Normal** | EXR 16-bit | Relighting, shading fixes |
| **ObjectID** | EXR 16-bit | Mattes per object |
| **Motion Vectors** | EXR 32-bit | RSMB, motion blur enhance |

---

## Related Skills
- `gimbal-automotive-cinematic-grade` — grading tracked car shots
- `teal-orange-cinematic-grade` — cinematic look for 3D integrates
- `fusion-compositing-basics` — 2D comp fundamentals
- `hdr-social-media-grade` — HDR 3D renders
- `social-media-sharpening-export` — final delivery