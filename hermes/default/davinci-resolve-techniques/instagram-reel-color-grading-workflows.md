---
name: instagram-reel-color-grading-workflows
description: Instagram Reel specific color grading and color correction workflows. Covers Color Wheels, LUTs, parallel nodes, text overlays, and social-media optimized grading for Reels content.
trigger: User wants to color grade Instagram Reels, apply LUTs, add text overlays, or learn Reel-specific grading workflows.
category: davinci-resolve/color-grading
tags: [instagram, reels, color-grading, color-correction, luts, color-wheels, parallel-nodes, text-overlay, social-media]
steps:
  - name: Dynamic Dust Enhancement & Golden Hour Grading (C_ZTbU5uVcK)
    description: Action sports golden hour - primary correction + qualifier for gold tones + power window for dust + sharpening
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Qualifier/Mask, Power Window]
    parameters:
      Contrast: "Increased"
      Saturation: "Boosted in highlights"
      Gamma: "Warm (Orange/Yellow)"
      Midtone: "Lift for dust detail"
    steps:
      - Apply primary color correction to balance the exposure against the sun flare
      - Use a Power Window (circular or custom) to isolate the dust cloud
      - Increase Gain and Saturation specifically on the masked area to make the dust pop
      - Use a Qualifier to select the golden/orange tones and boost their vibrance
      - Add a slight sharpening effect to the dust area to enhance texture and sand particles
    difficulty: intermediate
    video_id: C_ZTbU5uVcK
    tags: [color grading, action sports, golden hour, masking]

  - name: Instagram Reel with Parallel Nodes (DJrVhCyp9n3)
    description: Parallel node structure for independent grading paths
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: parallel
    key_nodes: [Keyframe 1, Keyframe 2]
    parameters:
      Parameter 1: "Value 1"
      Parameter 2: "Value 2"
    steps:
      - Import the Instagram Reel video into DaVinci Resolve
      - Create a new parallel node group
    difficulty: Intermediate
    video_id: DJrVhCyp9n3
    tags: [DaVinci Resolve, Instagram Reel, DJrVhCyp9n3]

  - name: Blackmagic App Promotion - Color + Text Overlay (DHdPK-lOAxM)
    description: Color correction node + text overlay node for promotional Reels
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [color correction node, text overlay node]
    parameters:
      color_correction_node:
        input_clip: "original footage"
        output_clip: "corrected footage"
      text_overlay_node:
        input_clip: "corrected footage"
        output_clip: "final reel with text"
    steps:
      - Import original footage into DaVinci Resolve
      - Apply color correction to the footage using the Color page
    difficulty: intermediate
    video_id: DHdPK-lOAxM
    tags: [color grading, text overlay, Instagram Reel promotion]

  - name: Instagram Reel Color Correction & LUT Mapping (C9pc6r6u9pJ)
    description: Two-node workflow: Color Correction → LUT Mapping
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Node1: Color Correction, Node2: LUT Mapping]
    parameters:
      param1: "LUT File Path"
      param2: "Color Temperature Adjustment"
    steps:
      - Step 1: Import and Organize Footage
      - Step 2: Apply Color Correction and LUT Mapping
    difficulty: Intermediate
    video_id: C9pc6r6u9pJ
    tags: [Instagram Reel, DaVinci Resolve, Color Grading, LUT Mapping]

  - name: Instagram Reel Color Correction + Text Overlay (C9M-Q9nAJPx)
    description: Color correction for contrast/saturation + text overlay for engagement
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Node1: Color Correction, Node2: Text Overlay]
    parameters:
      param1: "Contrast and Saturation Adjustments"
    steps:
      - Step 1: Importing the footage
      - Step 2: Applying color correction using DaVinci Resolve's Color page
    difficulty: Intermediate
    video_id: C9M-Q9nAJPx
    tags: [Color Correction, Text Overlay, Instagram Reel]

  - name: Instagram Reel Color Grading (C-7evtCqc5L)
    description: Standard Reel color grading workflow
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [node1, node2]
    parameters:
      param1: "value1"
    steps:
      - step1
      - step2
    difficulty: intermediate
    video_id: C-7evtCqc5L
    tags: [color grading, instagram reel, video editing]

  - name: Color Correction and Grading in DaVinci Resolve (C-rvS38CGHI)
    description: Color Wheels for white balance + LUTs for creative look
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Color Wheels, LUTs]
    parameters:
      param1: "White Balance Shift"
      param2: "Contrast Adjustment"
    steps:
      - Adjusting White Balance
      - Applying LUTs for a specific look
    difficulty: intermediate
    video_id: C-rvS38CGHI
    tags: [Color Grading, DaVinci Resolve Tutorial]

  - name: Instagram Reel Color Correction (C-Sh_9IuE-O)
    description: Basic color correction for Reels
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [node1, node2]
    parameters:
      param1: "value1"
    steps:
      - step1
      - step2
    difficulty: intermediate
    video_id: C-Sh_9IuE-O
    tags: [color correction, instagram reel, video editing]

  - name: Eye Tracking Effect for Reels (C-0FjexOViB)
    description: Specialized eye tracking node for engagement-focused Reels
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [eye_tracking_node]
    parameters:
      eye_tracking_node: "on"
    steps:
      - import_image
      - apply_eye_tracking_effect
    difficulty: intermediate
    video_id: C-0FjexOViB
    tags: [Instagram Reel, Color Correction, Eye Tracking]

  - name: Instagram Reel Color Correction & LUT (DKz0aPLuo31)
    description: Color balance for lighting + LUT for style
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Node for Color Correction, Node for LUT (Look-Up Table)]
    parameters:
      param1: "Adjusting the color balance to match the scene's lighting conditions"
      param2: "Applying a LUT to give the footage a specific look or style"
    steps:
      - Step 1: Import and organize the footage in DaVinci Resolve
      - Step 2: Apply color correction and LUT to match the scene's lighting conditions and achieve the desired aesthetic
    difficulty: Intermediate
    video_id: DKz0aPLuo31
    tags: [Color Correction, LUT, DaVinci Resolve, Instagram Reel]

  - name: Instagram Reel Color Correction & Grading Nodes (C5_Q7OZNK3q)
    description: Color Correction Node (saturation/contrast) + Grading Node (lift/gamma/gain)
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Color Correction Node, Grading Node]
    parameters:
      Color_Correction_Node:
        saturation: "1.0"
        contrast: "0.5"
      Grading_Node:
        lift: "0.2"
        gamma: "0.8"
        gain: "0.4"
    steps:
      - Import the footage into DaVinci Resolve
      - Apply a Color Correction node to adjust the color balance and saturation
    difficulty: intermediate
    video_id: C5_Q7OZNK3q
    tags: [Color Grading, Instagram Reel, DaVinci Resolve]

  - name: Instagram Reel Color Correction and Grading (DE5fztcMNcP)
    description: Color Correction (saturation/contrast) + Grading (lift/gamma/gain)
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Color Correction Node, Grading Node]
    parameters:
      Color_Correction_Node:
        saturation: "0.5"
        contrast: "1.2"
      Grading_Node:
        lift: "0.3"
        gamma: "0.7"
        gain: "0.8"
    steps:
      - Import the Instagram Reel into DaVinci Resolve
      - Apply a Color Correction node to adjust the color balance and saturation
      - Add a Grading node to fine-tune the contrast and overall look
    difficulty: intermediate
    video_id: DE5fztcMNcP
    tags: [Color Correction, Grading, Instagram Reel]
parameters:
  - name: Color_Wheels
    description: Primary color balance - Lift/Gamma/Gain
  - name: LUT_Application
    description: Creative LUT selection and intensity
  - name: Parallel_Nodes
    description: Independent grading paths for different image areas
  - name: Text_Overlay
    description: Title/text overlay for engagement
  - name: Qualifier_Mask
    description: Selective color adjustment (golden hour tones, skin, etc.)
  - name: Power_Window
    description: Geographic isolation (dust clouds, subjects, etc.)
  - name: Eye_Tracking
    description: Specialized effect for viewer retention
tags: [instagram, reels, color-grading, color-correction, luts, color-wheels, parallel-nodes, text-overlay, social-media, golden-hour, masking]
---

# Instagram Reel Color Grading Workflows

**Reel-specific color grading** workflows covering Color Wheels, LUTs, parallel nodes, text overlays, golden hour enhancement, and social-media optimized looks.

## Techniques Included

### 1. Dynamic Dust & Golden Hour (C_ZTbU5uVcK)
**Action sports golden hour with dust enhancement**

- **Node 1**: Primary Correction - balance sun flare exposure
- **Node 2**: Power Window - isolate dust cloud, boost gain/saturation
- **Node 3**: Qualifier - select golden/orange tones, boost vibrance
- **Node 4**: Sharpen - enhance dust/sand texture

**Use**: Action sports, dirt bikes, rally, golden hour dust

### 2. Parallel Node Structure (DJrVhCyp9n3)
**Independent grading paths**

```
Input → Parallel Mixer
    ├── Path A: Keyframe 1 (shadows/midtones)
    └── Path B: Keyframe 2 (highlights/creative)
```

**Use**: Split-tone, separate subject/background grades

### 3. Promo Reel: Color + Text Overlay (DHdPK-lOAxM)
**Two-stage: Grade → Text**

- **Node 1**: Color Correction (Color page)
- **Node 2**: Text Overlay (Fusion/Edit page)
- **Workflow**: Grade first, text last (text shouldn't be graded)

### 4. Color Correction + LUT Mapping (C9pc6r6u9pJ, DKz0aPLuo31)
**Standard two-node Reel workflow**

| Node | Purpose | Tools |
|------|---------|-------|
| 1 | Color Correction | Color Wheels, Temp/Tint, Contrast |
| 2 | LUT Mapping | LUT Browser, Intensity, Key Output |

**Settings**: LUT Intensity 50-75%, Key Output Gain for skin protection

### 5. Color Correction + Text Overlay (C9M-Q9nAJPx)
**Engagement-focused: Grade + Caption**

- **Node 1**: Contrast + Saturation boost for mobile
- **Node 2**: Text Overlay (safe zones, animation)

### 6. Standard Reel Color Grading (C-7evtCqc5L)
**Basic serial grade**

- **Node 1**: Primary balance
- **Node 2**: Creative look

### 7. Color Wheels + LUTs Tutorial (C-rvS38CGHI)
**Educational: WB → LUT**

1. **White Balance**: Color Wheels → Temp/Tint for neutral
2. **Creative LUT**: Apply LUT, adjust intensity
3. **Refine**: Post-LUT tweaks on new node

### 8. Basic Reel Color Correction (C-Sh_9IuE-O)
**Quick fix workflow**

- Auto Color → Manual tweak → Done

### 9. Eye Tracking Effect (C-0FjexOViB)
**Retention hack: Eye focus**

- Fusion: Tracker on eyes → Highlight/Sharpen
- Subtle: Don't overdo (uncanny valley)

### 10. Dual Node: Correction + Grading (C5_Q7OZNK3q, DE5fztcMNcP)
**Separate technical vs creative**

| Node | Type | Parameters |
|------|------|------------|
| 1 | Correction | Saturation, Contrast, Balance |
| 2 | Grading | Lift, Gamma, Gain (creative) |

**Why separate**: Correction is objective, Grading is subjective. Easy to swap grades.

## Reel-Optimized Grading Principles

1. **Mobile-first**: View on phone - shadows crush, saturation pops
2. **First 3 seconds**: Highest contrast/saturation for hook
3. **Skin protection**: Qualifier parallel node before LUT
4. **Text safe**: Grade leaves room for captions (lower thirds)
5. **Loop-friendly**: First/last frame match for seamless loop

## Node Structure Templates

### Template A: Basic Reel (2 nodes)
```
Node 1: Color Correction (technical)
Node 2: Creative Grade/LUT (artistic)
```

### Template B: Protected Skin (3 nodes)
```
Node 1: Primary Balance
Node 2: Creative Grade
Node 3 (Parallel): Skin Qualifier → Protect from Node 2
```

### Template C: Split Tone (Parallel)
```
          ┌─ Node A: Shadows → Teal
Input ──┤
          └─ Node B: Highlights → Orange
         Parallel Mixer
```

### Template D: Golden Hour Action (4 nodes)
```
Node 1: Primary (exposure vs sun)
Node 2: Power Window (dust/subject pop)
Node 3: Qualifier (gold tones vibrance)
Node 4: Sharpen (texture)
```

## Text Overlay Best Practices

- **Safe Zone**: Keep text in center 80% (avoid notch/UI)
- **Contrast**: Stroke/shadow for readability on any bg
- **Timing**: 2-3 sec per line, sync to beat
- **Animation**: Subtle fade/slide, not distracting

## Export for Reels (Quick Ref)

- **Timeline**: 1080x1920, 30fps
- **Bitrate**: 25 Mbps (Restrict)
- **Codec**: H.264 MP4
- **Color**: Rec.709, Gamma 2.4