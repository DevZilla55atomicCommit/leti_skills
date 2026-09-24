---
name: davinci-camera-tracking-matchmove
description: Camera tracking and match-moving in DaVinci Resolve Fusion page. Covers 3D camera solver, planar tracking, object tracking, and integrating 3D elements/CGI into live footage.
trigger: camera tracking, matchmove, 3d camera solver, planar tracking, object tracking, fusion tracking, vfx integration, davinci resolve fusion
steps:
  - "Edit Page: Rough cut, identify shots needing tracking"
  - "Fusion Page: Add Tracker tool, select tracking points (high contrast, corners)"
  - "Tracker: Track forward/backward, refine with keyframes"
  - "Camera Tracker: Switch to 3D mode, solve camera (focal length, sensor size)"
  - "Verify: Add 3D primitive (Cube/Sphere), lock to ground plane"
  - "Import 3D: Loader (FBX/OBJ/Alembic) → Connect to Camera3D"
  - "Lighting: Match HDRI/Environment to plate lighting"
  - "Render: Multi-pass (Beauty, Shadow, AO, Cryptomatte) → Composite in Fusion"
parameters:
  - name: tracker_type
    type: string
    description: Type of tracking needed
    enum: ["Planar Tracker (Mocha-style)", "Point Tracker (2D)", "Camera Tracker (3D Solve)", "Object Tracker (3D Object)", "Surface Tracker (Deformable)"]
    default: "Camera Tracker (3D Solve)"
  - name: solve_method
    type: string
    description: Camera solve algorithm
    enum: ["Tripod (No Parallax)", "Free Camera (General)", "Nodal Pan (Rotation Only)", "Survey (Known Points)"]
    default: "Free Camera (General)"
  - name: focal_length_known
    type: boolean
    description: Whether focal length is known from metadata
    default: false
  - name: sensor_size
    type: string
    description: Camera sensor size for solve
    enum: ["Full Frame (36x24mm)", "Super 35 (24.9x18.7mm)", "APS-C (23.6x15.7mm)", "Micro 4/3 (17.3x13mm)", "1-inch (13.2x8.8mm)", "Custom"]
    default: "Super 35 (24.9x18.7mm)"
  - name: track_point_count
    type: number
    description: Minimum tracking points for stable solve
    default: 8
    minimum: 6
    maximum: 50
  - name: export_format
    type: string
    description: Export format for 3D app
    enum: ["FBX (Maya/Blender/C4D)", "Alembic (.abc)", "USD (.usd)", "Maya ASCII (.ma)", "Nuke (.chan)"]
    default: "FBX (Maya/Blender/C4D)"
tags:
  - camera-tracking
  - matchmove
  - 3d-camera-solver
  - planar-tracking
  - object-tracking
  - fusion
  - vfx
  - davinci-resolve
  - 3d-integration
  - cgi
  - compositing
category: davinci-resolve-fusion-tracking
---

# DaVinci Resolve Camera Tracking & Match-Moving (Fusion)

Complete workflow for 2D/3D camera tracking, planar tracking, and object tracking in DaVinci Resolve Fusion page. Integrate CGI, text, graphics, and set extensions into live footage.

## Tracking Types Overview

| Tracker Type | Dimensions | Use Case | Fusion Tool |
|--------------|------------|----------|-------------|
| **Point Tracker** | 2D (X,Y) | Corner pin, stabilization, simple follow | Tracker |
| **Planar Tracker** | 2.5D (Plane) | Screen replacement, sign replacement, rotoscoping | PlanarTracker |
| **Camera Tracker** | 3D (Camera + Points) | CGI integration, set extension, matte painting | CameraTracker |
| **Object Tracker** | 3D (Object + Camera) | Moving object replacement, character tracking | CameraTracker (Object mode) |
| **Surface Tracker** | 3D (Deforming Mesh) | Face tracking, cloth, organic deformation | SurfaceTracker |

---

## 1. Point Tracking (2D) - Foundation

### Basic Workflow
```
Fusion Composition:
MediaIn → Tracker → Transform/Tracker → MediaOut

Tracker Tool Settings:
- Operation: "Track"
- Pattern Box: 16-32px (high contrast area)
- Search Box: 2-4x pattern size
- Motion Model: Translation / Rotation / Scale / Perspective
- Channels: Luma (fastest) / RGB (color changes)
```

### Multi-Point Tracking (Corner Pin)
```
1. Add 4 Tracker tools (or 1 Tracker with 4 patterns)
2. Track each corner of screen/sign/window
3. Connect to CornerPositioner tool:
   - Input1: MediaIn
   - TopLeft: Tracker1
   - TopRight: Tracker2
   - BottomLeft: Tracker3
   - BottomRight: Tracker4
4. Connect replacement media to CornerPositioner Background
```

### Tracking Difficult Shots
```
Motion Blur:
- Increase Search Box
- Use "Adaptive" search
- Track on sharp frames, interpolate

Occlusion:
- Track before/after occlusion
- Keyframe "Track" checkbox OFF during occlusion
- Use "Append" to continue track

Lighting Change:
- Track on Luma channel
- Reference Frame: Track on first frame, search subsequent
- Use "Match Move" instead of "Track" for relative movement
```

---

## 2. Planar Tracking (Mocha-Style) - PlanarTracker

### When to Use
- Screen replacements (phone, TV, monitor)
- Sign/billboard replacement
- Large flat surface tracking
- Rotoscoping assistance

### Workflow
```
1. PlanarTracker Tool
2. Draw spline around planar surface (Roto-like)
3. "Track Forward" / "Track Backward"
4. Adjust: Min % Pixels Tracked (default 50% - lower for partial occlusion)
5. Output: "Corner Pin" or "Stabilize" or "Match Move"

Corner Pin Output:
- Connect replacement media to PlanarTracker "Background" input
- PlanarTracker automatically cornerspins

Stabilize Output:
- Inverts track → locks plane in place
- Great for cleaning up plate before paint/roto
```

### PlanarTracker Advanced
```
Grid Warp (Deformable):
- Enable "Grid Warp" in PlanarTracker
- Tracks non-rigid surfaces (clothing, skin, flags)
- Output: UV map for STMap-style warping

Export to Mocha Pro:
- Right-click PlanarTracker → "Export to Mocha"
- Advanced roto, lens distortion, stereo
- Import back: "Import from Mocha" (.mocha file)
```

---

## 3. Camera Tracking (3D Solve) - CameraTracker

### The Most Powerful Tool for VFX Integration

### Prerequisites for Good Solve
```
Footage Requirements:
- Parallax (camera MUST move - no tripod pans only)
- Sufficient detail/texture (not solid walls, green screens)
- 100+ frames ideal (minimum ~30)
- Known sensor size + focal length (helps immensely)
- Low motion blur, low rolling shutter
- No extreme lens distortion (or calibrate first)

Metadata to Collect:
- Camera model
- Lens model + focal length (EXIF or lens metadata)
- Sensor size (Full Frame / S35 / M43 / etc.)
- Frame rate
- Resolution
```

### CameraTracker Workflow
```
1. New Fusion Comp (on timeline clip or standalone)
2. Add CameraTracker tool
3. Settings Tab:
   - Solve Method: "Free Camera" (default)
   - Focal Length: "Unknown" (or enter known mm)
   - Sensor Size: Select preset or Custom (mm)
   - Principal Point: Center (default)
   - Distortion Model: Brown3 (standard)

4. Trackers Tab:
   - "Auto Track" → Adds ~50-200 trackers automatically
   - OR manual: Click "Add Tracker" → Place on high-contrast features
   - Minimum 8-12 GOOD tracks for solve
   - Track all frames: "Track Forward" + "Track Backward"

5. Solve Tab:
   - Click "Solve"
   - Check "Solve Error" (aim < 1.0 pixel, < 0.5 ideal)
   - Check "Focal Length" result (reasonable?)
   - View 3D: "Show 3D View" → Verify point cloud looks correct

6. Refine:
   - Delete bad tracks (high error, jumping)
   - Re-solve
   - Add "Survey Points" if known 3D positions exist
   - Lock good tracks: "Lock" checkbox
```

### CameraTracker Outputs
```
CameraTracker Outputs:
- Camera3D: Animated camera (position, rotation, FOV)
- PointCloud: 3D points (for reference)
- ImagePlane: Background plate projected in 3D

Connecting 3D Elements:
1. Add Camera3D (from CameraTracker output)
2. Add Renderer3D
3. Connect Camera3D → Renderer3D.Camera
4. Add 3D objects (Shape3D, Import3D, Text3D)
5. Connect objects → Renderer3D.SceneInput
6. Renderer3D → Composite over plate (Merge)
```

### Solving Tripod/Nodal Shots (No Parallax)
```
Solve Method: "Tripod Pan" or "Nodal Pan"
- Camera rotates but doesn't translate
- Solves rotation + focal length only
- Cannot place 3D objects in world space
- Use for: Sky replacement, matte painting projection
- Output: Camera3D with rotation only, no position animation
```

### Lens Distortion Workflow
```
1. Shoot distortion grid (checkerboard) with same lens/settings
2. CameraTracker → Lens Tab → "Calibrate"
3. Load grid image → Auto-detect corners
4. Solve distortion coefficients (k1, k2, k3)
5. Apply to track: "Undistort" plate before tracking
6. After solve: "Redistort" 3D renders to match plate
7. OR: Use STMap (UV map) for redistort in composite
```

---

## 4. Object Tracking (Moving Objects)

### CameraTracker Object Mode
```
1. CameraTracker → Trackers Tab
2. Select trackers on moving object (car, person, etc.)
3. Right-click selected → "Create Object Tracker"
4. New ObjectTracker tool created
5. ObjectTracker solves object's 3D transform relative to camera
6. Output: Object's Position/Rotation/Scale in 3D space

Use for:
- Replace moving object (car → CGI car)
- Attach effects to moving object
- Stabilize object (invert transform)
```

### PlanarTracker for Object Track
```
For flat-sided objects (boxes, buildings, phones):
1. PlanarTracker on object surface
2. Track → "Match Move" output
3. Connect 3D element to PlanarTracker's 3D output
4. PlanarTracker creates 3D corner pin in space
```

---

## 5. Integrating 3D Elements (CGI/VFX)

### Importing 3D Assets
```
Supported Formats:
- FBX (Animation, Cameras, Lights, Materials)
- Alembic (.abc) - Geometry caches, deforming meshes
- OBJ (Static geometry + MTL materials)
- USD (.usd/.usda/.usdc) - Universal Scene Description
- GLTF/GLB (Web/PBR materials)

Import3D Tool:
- File: Select asset
- Scale: Match scene units (meters vs cm)
- Animation: Import animated transforms
- Materials: "Convert to Fusion Materials" or "Keep Original"
```

### Lighting Matching (Critical for Realism)
```
HDRI Workflow:
1. Shoot HDRI on set (Chrome ball / 360° pano)
2. EnvironmentMap tool → Load HDRI (.hdr/.exr)
3. Connect to Renderer3D → Global Illumination
4. Or: LightProbe tool for Image-Based Lighting

Manual Light Matching:
1. Analyze plate: Key light direction, fill ratio, color temp
2. Add DirectionalLight (sun) + AreaLights (fill)
3. Match shadows: Direction, hardness, color
4. Add Contact Shadows (AO pass)

Render Passes (Multi-Pass):
Renderer3D → Output Tab → Add Passes:
- Beauty (RGB)
- Alpha (Object ID)
- Z-Depth (World Position)
- Normal (World Space)
- ObjectID / MaterialID (Cryptomatte)
- Shadow (Raw)
- AO (Ambient Occlusion)
- Motion Vectors (for RSMB)
```

### Compositing 3D Over Plate
```
Basic Composite:
Plate (MediaIn) → Merge (Background)
                    ↑
              Renderer3D (Foreground)

Advanced (with passes):
Beauty → Merge (Over)
Shadow → Multiply (on plate)
AO → Multiply (subtle)
Z-Depth → DepthBlur / Fog / Atmosphere
Normal → Relight (NormalRelight tool)
Cryptomatte → Isolate objects for grading
```

### Shadow Catching (CGI Shadows on Real Ground)
```
1. Create ground plane (Shape3D → Plane) matching plate ground
2. Material: "Matte" / "Shadow Catcher" (in Material tab)
   - Receive Shadows: ON
   - Visible to Camera: OFF
   - Visible to GI: ON
3. Ground plane follows tracked camera
4. Renderer3D outputs Shadow pass
5. Composite: Shadow pass → Multiply over plate
```

---

## 6. Set Extension / Matte Painting

### 2.5D Projection (Matte Painting)
```
1. CameraTracker solve → Camera3D
2. Projector3D tool:
   - Input: Matte painting (PSD layers separated)
   - Camera: Camera3D from solve
   - Geometry: Simple proxy geo (planes, boxes) matching architecture
3. Renderer3D → Projected matte painting
4. Merge over plate (with soft edge blending)

Layered Matte Painting:
- Foreground elements (trees, poles) → Separate planes, closer to camera
- Mid-ground (buildings) → Mid-distance planes
- Background (sky, mountains) → Far plane / EnvironmentMap
- Parallax automatically correct via 3D projection
```

### 3D Set Extension
```
For moving camera with significant parallax:
1. Model extension in 3D (Blender/Maya) → Export FBX/Alembic
2. Import3D → Match camera solve
3. Texture with projected plate + painted textures
4. Light to match
5. Render passes → Composite
```

---

## 7. Export/Import Pipeline (Round-trip)

### Export to 3D App (Maya/Blender/C4D/Houdini)
```
CameraTracker → Right-click → "Export Camera"
Formats:
- FBX: Cameras + Locators (points) + Animation
- Alembic: Cameras + Point Cloud + Animation
- Maya ASCII (.ma): Human-readable, editable
- Nuke (.chan): Channel file for Nuke

Export Settings:
- Frame Range: Match plate
- Units: Meters (standard)
- Up Axis: Y-Up (Maya/Blender) / Z-Up (Max/C4D)
- Bake Animation: Every frame (not just keys)
```

### Import from 3D App
```
After lighting/rendering in 3D app:
1. Render EXR multi-pass (Beauty, Shadow, AO, Z, Normal, Cryptomatte)
2. Import sequences in Fusion (Loader → "Sequence" checkbox)
3. Composite using passes
4. Color grade in Resolve Color page (ACES workflow ideal)
```

---

## 8. Troubleshooting Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Solve Error > 2px | Bad tracks, insufficient parallax | Delete outliers, add more tracks, check focal length |
| Focal length solves to nonsense | Zoom lens / wrong sensor size | Lock focal length if known, verify sensor size |
| Point cloud inverted/flipped | Coordinate system mismatch | Check "Flip Y" in CameraTracker, verify Up Axis |
| 3D objects slide on ground | Ground plane not tracked | Add trackers on ground, use "Ground Plane" constraint |
| Jittery solve | Rolling shutter, motion blur | Subspace Warp, gyro data, reduce track weight on blur frames |
| Tracks drift over time | Accumulated error | Keyframe "Reset" on cut points, re-track sections |
| Lens distortion visible | Wide lens, no calibration | Calibrate with grid, use Brown3 model |

---

## Quick Reference: Fusion Tracking Node Graph

```
BASIC 2D TRACK:
MediaIn → Tracker (Track) → Transform (Match Move) → MediaOut

PLANAR TRACK (Screen Replace):
MediaIn → PlanarTracker (Track → Corner Pin) → Merge (Screen Content) → MediaOut

CAMERA TRACK (3D):
MediaIn → CameraTracker (Auto Track → Solve) → Camera3D
                                              ↓
                                        Renderer3D ← Shape3D/Import3D
                                              ↓
                                        Merge (Over Plate) → MediaOut

OBJECT TRACK:
MediaIn → CameraTracker → ObjectTracker (on object tracks) → Transform3D (Object)
                                                                   ↓
                                                            Renderer3D → Merge
```

---

## Related Skills

- `davinci-fusion-compositing` - Core Fusion compositing workflows
- `davinci-planar-tracking-mocha` - Advanced PlanarTracker/Mocha integration
- `davinci-3d-compositing-passes` - Multi-pass EXR compositing
- `davinci-lens-distortion` - Calibration and correction
- `davinci-vfx-supervision` - On-set VFX data acquisition