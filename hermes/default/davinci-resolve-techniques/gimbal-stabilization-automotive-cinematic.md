---
name: gimbal-stabilization-automotive-cinematic
description: Gimbal stabilization workflows combined with cinematic color grading for automotive and action sports footage. Covers physical gimbal techniques, digital stabilization in Resolve, and automotive-focused grading.
trigger: User wants to stabilize gimbal footage, grade automotive content, or create cinematic car commercials.
category: davinci-resolve/stabilization-grading
tags: [gimbal, stabilization, automotive, cinematic, color-grading, camera-lock, transform, primary-correction, color-wheels, power-mask]
steps:
  - name: Gimbal Stabilization & Dynamic Color Grading (DHLSAxAIQ9O)
    description: Physical gimbal setup + Resolve Stabilizer tool + cinematic automotive grade
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Camera Clip, Primary Correction, Color Wheels, Stabilizer]
    parameters:
      stabilization: "Perspective/Similarity"
      contrast: "High"
      saturation: "Slight boost"
    steps:
      - Mount camera on a gimbal for smooth low-angle tracking shots
      - Import footage into DaVinci Resolve Color page
      - Use the Stabilizer tool in the Inspector tab to smooth out any remaining micro-jitters
      - Apply primary color correction to balance blacks and highlights on the car carbon fiber texture
      - Add a LUT or manual grade to achieve a cinematic automotive look
    difficulty: intermediate
    video_id: DHLSAxAIQ9O
    tags: [gimbal, cinematic, color-grading, automotive, stabilization]

  - name: Dynamic Gimbal Stabilization & Color Grading (DG5M8Mhocoz)
    description: Motorized gimbal capture + Camera Edge Mode stabilization + metallic paint enhancement
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Power Mask, Color Curves]
    parameters:
      Stabilization: "Camera Edge Mode"
      Contrast: "High Contrast"
      Saturation: "Enhanced for Metallic Tones"
    steps:
      - Capture footage using a motorized gimbal to ensure smooth tracking shots
      - Import footage into DaVinci Resolve
      - Use the Stabilization tab in the Inspector to fine-tune any remaining jitter
      - Apply a color grade to enhance the metallic paint of the vehicle
      - Use Power Windows to isolate highlights on the car body
      - Apply a cinematic LUT for the final look
    difficulty: intermediate
    video_id: DG5M8Mhocoz
    tags: [automotive, gimbal, cinematic, colorgrading]

  - name: Virtual Gimbal Movement & Stabilization (C9sE4njPHM4)
    description: Digital gimbal simulation using Camera Lock stabilization + Transform keyframes
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Stabilizer, Transform]
    parameters:
      Stabilization_Mode: "Camera Lock"
      Smoothing: "50"
      Zoom: "1.15"
    steps:
      - Import raw footage into the timeline
      - Open the Color page and create a new node
      - Apply the Stabilizer effect from the Inspector
      - Select 'Camera Lock' to stabilize handheld footage
      - Add a Transform node to create manual digital zooms or pans
      - Use keyframes to simulate a smooth gimbal-like tilt or movement
    difficulty: beginner
    video_id: C9sE4njPHM4
    tags: [cinematography, stabilization, davinci-resolve, gimbal]

  - name: Gimbal Movement for Car Photography (DADa0Tturp7)
    description: Physical gimbal technique for 45-degree car turntable shots
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Camera Gimbal, Car]
    parameters:
      Camera_Angle: "45 degrees"
      Movement_Speed: "Slow and steady"
    steps:
      - Set up the camera gimbal on a tripod
      - Mount the car on a turntable
    difficulty: Intermediate
    video_id: DADa0Tturp7
    tags: [Car Photography, Gimbal Movement]
parameters:
  - name: Stabilization_Mode
    description: Stabilizer mode - Perspective, Similarity, or Camera Lock
  - name: Smoothing
    description: Smoothing amount (0-100) for stabilization
  - name: Zoom
    description: Digital zoom factor for Camera Lock mode
  - name: Camera_Edge_Mode
    description: Edge handling for stabilization
tags: [gimbal, stabilization, automotive, cinematic, color-grading, camera-lock, transform, primary-correction, color-wheels, power-mask]
---

# Gimbal Stabilization & Automotive Cinematic Grading

Combined physical and digital gimbal workflows with cinematic color grading tailored for **automotive, action sports, and commercial content**. Covers both hardware gimbal techniques and Resolve's digital stabilization tools.

## Techniques Included

### 1. Gimbal Stabilization & Dynamic Color Grading (DHLSAxAIQ9O)
**Physical gimbal + Resolve Stabilizer + Automotive grade**

- **Stabilization**: Perspective/Similarity mode for micro-jitter removal
- **Grading**: High contrast, slight saturation boost, carbon fiber texture preservation
- **Nodes**: Camera Clip → Primary Correction → Color Wheels → Stabilizer

### 2. Dynamic Gimbal Stabilization & Color Grading (DG5M8Mhocoz)
**Motorized gimbal + Camera Edge Mode + Metallic paint enhancement**

- **Stabilization**: Camera Edge Mode for clean edges
- **Grading**: High contrast, metallic tone enhancement via Power Windows
- **Nodes**: Primary Correction → Power Mask → Color Curves

### 3. Virtual Gimbal Movement & Stabilization (C9sE4njPHM4)
**No gimbal needed - Digital simulation via Camera Lock + Transform keyframes**

- **Stabilization**: Camera Lock mode (locks camera position)
- **Movement**: Transform node with keyframed pans/tilts/zooms
- **Parameters**: Smoothing 50, Zoom 1.15
- **Nodes**: Stabilizer → Transform

### 4. Gimbal Movement for Car Photography (DADa0Tturp7)
**Physical technique: 45° gimbal on tripod + car turntable**

- **Setup**: Gimbal on tripod, car on motorized turntable
- **Angle**: 45 degrees, slow steady rotation
- **Use case**: 360° car showcase videos

## Stabilization Mode Guide

| Mode | Best For | Trade-off |
|------|----------|-----------|
| **Perspective** | General handheld | May warp straight lines |
| **Similarity** | Preserves aspect | Less correction power |
| **Camera Lock** | Digital gimbal simulation | Requires zoom (1.1-1.2x) |

## Automotive Grading Tips

1. **Protect carbon fiber** - Use Power Windows to isolate weave texture
2. **Enhance metallic flake** - Boost highlights on body panels via curved masks
3. **Teal shadows + warm highlights** - Classic automotive commercial look
4. **High contrast** - Deep blacks make paint pop

## Pro Workflow

```
Footage → Stabilize (Camera Lock) → Transform (keyframe movement) 
  → Primary Grade → Power Windows (car isolation) → Curves (metallic) → LUT
```