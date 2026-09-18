---
name: fusion-3d-camera-tracking-vfx
description: Fusion page 3D camera tracking, 3D object integration, and VFX compositing workflows. Covers CameraTracker, 3D scene setup, Renderer3D, and advanced compositing for automotive and product visualization.
trigger: User wants to do 3D camera tracking, integrate 3D models into footage, or create VFX composites in Fusion.
category: davinci-resolve/fusion-vfx
tags: [fusion, 3d, camera-tracking, vfx, compositing, camera3d, merge3d, renderer3d, loader, transform]
steps:
  - name: 3D Camera Tracking & Object Integration (C9wagvWK8vy)
    description: Full 3D camera track → 3D camera creation → 3D model import → scene alignment → render
    resolve_page: Fusion
    node_graph_type: serial
    key_nodes: [CameraTracker, Camera3D, Merge3D, Renderer3D, ImagePlane]
    parameters:
      tracking_mode: "Auto/Manual Plan"
      projection: "Perspective"
      lighting: "HDRi or Point Lights"
    steps:
      - Import the background footage into the Fusion page
      - Add a CameraTracker node and analyze the footage movement
      - Right-click the tracker and select 'Create 3D Camera'
      - Import the 3D car model (OBJ or FBX) into the scene
      - Place the car model in a Merge3D node with the camera and background
      - Align the 3D model to match the floor perspective of the tracked footage
      - Add a Renderer3D node to output the 3D scene back to the 2D workspace
    difficulty: advanced
    video_id: C9wagvWK8vy
    tags: [VFX, 3D, Camera Tracking, Fusion]

  - name: 3D Car Rendering with Animation Gizmo (C_QClmggW_f)
    description: Import 3D car model → Transform positioning → Renderer3D → animation gizmo controls
    resolve_page: Fusion
    node_graph_type: serial
    key_nodes: [Loader, Transform, Renderer3D]
    parameters:
      car_model_path: "/path/to/car_model.fbx"
      animation_gizmo_enabled: true
      gizmo_type: "rotation_scale"
    steps:
      - Import the 3D car model into Fusion using a Loader node
      - Apply a Transform node to position and orient the car in the 3D scene
      - Add a Renderer3D node to render the 3D scene
      - Optionally, add animation controls or a gizmo to the car object for manipulation
    difficulty: intermediate
    video_id: C_QClmggW_f
    tags: [3D, rendering, animation, car, Fusion]
parameters:
  - name: tracking_mode
    description: CameraTracker analysis mode - Auto or Manual Plan
  - name: projection
    description: Camera projection type - Perspective or Orthographic
  - name: lighting
    description: Lighting setup for 3D scene - HDRi or Point Lights
  - name: car_model_path
    description: File path to 3D model (FBX, OBJ, GLB)
  - name: animation_gizmo_enabled
    description: Enable interactive gizmo for object manipulation
tags: [fusion, 3d, camera-tracking, vfx, compositing, camera3d, merge3d, renderer3d, loader, transform, 3d-modeling]
---

# Fusion 3D Camera Tracking & VFX Compositing

Advanced **Fusion page** workflows for **3D camera tracking**, **3D object integration**, and **VFX compositing**. Essential for automotive visualization, product shots, and environment integration.

## Techniques Included

### 1. 3D Camera Tracking & Object Integration (C9wagvWK8vy)
**Full pipeline: Track → Solve → Import 3D → Align → Render**

- **Tracker**: CameraTracker with Auto/Manual Plan
- **3D Scene**: Camera3D + Merge3D + Renderer3D + ImagePlane
- **Model Import**: OBJ/FBX via Loader → Merge3D
- **Alignment**: Match 3D model to tracked floor plane
- **Output**: Renderer3D back to 2D composite

**Nodes**: `CameraTracker → Camera3D → Merge3D → Renderer3D`

### 2. 3D Car Rendering with Animation Gizmo (C_QClmggW_f)
**Standalone 3D rendering in Fusion for turntable/product shots**

- **Import**: Loader node for FBX/OBJ/GLB
- **Position**: Transform node for placement/orientation
- **Render**: Renderer3D with lighting
- **Animation**: Gizmo controls for rotation/scale keyframing

**Nodes**: `Loader → Transform → Renderer3D`

## CameraTracker Workflow

```
Footage → CameraTracker (Analyze) → Create 3D Camera
                                    ↓
                            Camera3D (solved camera)
                                    ↓
                            Merge3D (camera + model + image plane)
                                    ↓
                            Renderer3D (final composite)
```

## 3D Model Integration Checklist

- [ ] **Scale**: Match real-world units (meters)
- [ ] **Origin**: Model pivot at ground contact point
- [ ] **Materials**: Assign proper PBR materials in Fusion
- [ ] **Lighting**: HDRi for reflections + key/fill for shape
- [ ] **Shadows**: Enable shadow catcher on ImagePlane
- [ ] **Motion Blur**: Match camera shutter angle

## Pro Tips

1. **Track planar surfaces** - Ground plane, walls give best solve
2. **Manual cleanup** - Delete bad trackers before solve
3. **Survey shot** - Film a 360° reference for HDRi lighting
4. **Proxy models** - Use low-poly for layout, swap hi-res for render
5. **Render passes** - Output beauty, shadow, AO, depth for comp flexibility

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Solve fails | More trackers, longer track length, planar constraints |
| Model floats | Align pivot to ground, check scale units |
| Jittery track | Increase smoothing, check for rolling shutter |
| Lighting mismatch | Capture on-set HDRi, match sun direction |