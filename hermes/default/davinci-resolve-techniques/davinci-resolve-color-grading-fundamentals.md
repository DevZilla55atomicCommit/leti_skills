---
name: davinci-resolve-color-grading-fundamentals
description: Core color grading fundamentals using Color Wheels, Color Correction nodes, Grading nodes, and LUTs. Use when learning or applying primary color correction, contrast/saturation adjustments, and creative grading workflows.
trigger: User wants to learn or apply color grading fundamentals in DaVinci Resolve (Color Wheels, Color Correction nodes, Grading nodes, LUTs).
category: davinci-resolve
tags:
  - color correction
  - color grading
  - color wheels
  - lut
  - grading
  - davinci resolve
  - color page
steps:
  - name: primary-correction-color-wheels
    description: Primary correction using Color Wheels (Lift/Gamma/Gain) for exposure, contrast, and white balance
    parameters:
      - name: lift
        type: string
        description: Shadow adjustment (e.g., "0.2" or "low")
      - name: gamma
        type: string
        description: Midtone adjustment (e.g., "0.8" or "medium")
      - name: gain
        type: string
        description: Highlight adjustment (e.g., "1.0" or "high")
      - name: offset
        type: string
        description: Overall brightness offset
      - name: saturation
        type: string
        description: Global saturation (e.g., "0.5" for low, "1.0" for normal)
    difficulty: beginner
  - name: secondary-correction-color-correction-node
    description: Targeted corrections using Color Correction node (HSL qualifiers, power windows)
    parameters:
      - name: qualifier_hue
        type: string
        description: Hue range for selection
      - name: qualifier_sat
        type: string
        description: Saturation range for selection
      - name: qualifier_lum
        type: string
        description: Luminance range for selection
      - name: power_window
        type: string
        description: Shape type (circle, square, custom)
    difficulty: intermediate
  - name: creative-grading-grading-node
    description: Creative look development using Grading node with LUTs and custom curves
    parameters:
      - name: lut_path
        type: string
        description: Path to .cube LUT file (e.g., "custom_lut.cube")
      - name: lut_intensity
        type: string
        description: LUT blend amount (0.0-1.0)
      - name: contrast_curve
        type: string
        description: Custom curve preset (e.g., "s-curve", "film-emulation")
      - name: color_temp
        type: string
        description: Color temperature shift (e.g., "2500K" for warm)
    difficulty: intermediate
  - name: lut-workflow
    description: Apply and manage LUTs for consistent looks
    parameters:
      - name: lut_type
        type: string
        description: "technical" (Rec709, Log->Rec709) or "creative" (film looks)
      - name: lut_position
        type: string
        description: Node position: "input" (before grade), "creative" (middle), "output" (final)
      - name: interpolation
        type: string
        description: "tetrahedral" for smooth gradients, "trilinear" for speed
    difficulty: intermediate
parameters:
  - name: resolve_page
    type: string
    default: "Color"
    description: DaVinci Resolve page (always "Color" for grading)
  - name: node_graph_type
    type: string
    default: "serial"
    description: Node graph structure (serial for most grading workflows)
---

# DaVinci Resolve Color Grading Fundamentals

Core color grading techniques using DaVinci Resolve's Color page: primary correction with Color Wheels, secondary corrections with Color Correction nodes, creative grading with Grading nodes, and LUT workflows.

## Techniques Covered

| Technique | Video IDs | Key Nodes | Difficulty |
|-----------|-----------|-----------|------------|
| Primary Color Correction (Color Wheels) | C4bgrkyJ572, CeTi2YXljSw, DOZJKKlE3Dv, DGeumrjxgyW | Color Wheels | Beginner |
| Color Correction Node (HSL/Power Windows) | C3mZDyZvjcZ, C2dRJq3pccX, C9a-uTQv2GX, DNN18eNxjM8, DFmJ8wGxa3j | Color Correction Node | Intermediate |
| Creative Grading Node with LUTs | C3mZDyZvjcZ, C9a-uTQv2GX, C8Y4iXdq9CW, C8AANlhv82q, C3dokA0OETD | Grading Node, LUT Node | Intermediate |
| LUT Application Workflow | C4bgrkyJ572, C3KQIN7PpHV, CeTi2YXljSw, DOZJKKlE3Dv, DGeumrjxgyW | LUTs | Intermediate |

## Core Workflows

### 1. Primary Correction with Color Wheels
**Video Reference**: C4bgrkyJ572 (Instagram Reel Color Grading)

```
Node 1: Color Wheels
├── Lift: Adjust shadows (e.g., "high" for lifted blacks)
├── Gamma: Adjust midtones (e.g., "medium" for balanced)
├── Gain: Adjust highlights (e.g., "high" for bright look)
├── Offset: Overall brightness
└── Saturation: Global saturation (e.g., "low" for desaturated look)
```

**Steps**:
1. Import footage to timeline
2. Open Color page, add first serial node
3. Select Color Wheels panel
4. Adjust Lift/Gamma/Gain for exposure balance
5. Set Offset for overall level
6. Adjust Saturation for creative intent

### 2. Secondary Correction with Color Correction Node
**Video References**: C3mZDyZvjcZ, C2dRJq3pccX, C9a-uTQv2GX

```
Node 1: Color Wheels (Primary)
Node 2: Color Correction Node (Secondary)
├── Qualifier: HSL selection (Hue/Sat/Lum ranges)
├── Power Window: Shape mask (Circle/Square/Custom)
├── Tracker: Track mask to subject
└── Adjustments: Targeted corrections within selection
```

**Steps**:
1. Add serial node after primary correction
2. Open Qualifier panel, use eyedropper to select color range
3. Refine with Hue/Sat/Lum sliders
4. Add Power Window for spatial isolation
5. Enable Tracker if subject moves
6. Apply targeted corrections (hue shift, saturation, luminance)

### 3. Creative Grading with Grading Node + LUTs
**Video References**: C8Y4iXdq9CW, C8AANlhv82q, C3dokA0OETD

```
Node 1: Color Wheels (Primary)
Node 2: Color Correction (Secondary - skin tones, sky, etc.)
Node 3: Grading Node (Creative)
├── LUT: Apply creative LUT (e.g., "custom_lut.cube")
├── Intensity: Blend LUT (0.3-0.7 typical)
├── Curves: Custom contrast curve (S-curve for film look)
├── Color Warper: Hue/Sat/Lum global shifts
└── Color Wheels: Final creative push
Node 4: Output LUT (Technical - Rec709, P3, etc.)
```

**Steps**:
1. Complete primary and secondary corrections first
2. Add Grading node for creative look
3. Load creative LUT via LUT browser or right-click node → LUT
4. Adjust LUT intensity with Key Output Gain
5. Add custom curves for contrast shaping
6. Use Color Warper for global hue shifts
7. Apply output transform LUT last

### 4. LUT Workflow Best Practices
**Video References**: C3KQIN7PpHV (Daytime Exterior), C4bgrkyJ572 (Instagram Reel)

**LUT Types & Positions**:
| Type | Purpose | Position | Example |
|------|---------|----------|---------|
| Technical Input | Log → Rec709 | Node 1 (first) | Sony S-Log3 → Rec709 |
| Creative | Film emulation, looks | Middle nodes | Kodak 2383, Fujifilm |
| Technical Output | Timeline → Display | Last node | Rec709 → P3, HDR |

**Settings**:
- Interpolation: **Tetrahedral** (smooth gradients, prevents banding)
- Color Space: Match project settings (DaVinci YRGB Color Managed recommended)
- Intensity: Use Key Output Gain (0.3-0.7) for subtle creative LUTs

## Node Graph Structure

```
Serial Node Graph (Standard Grading Pipeline)
├── Node 01: Primary Correction (Color Wheels)
├── Node 02: Secondary - Skin Tones (Color Correction + Qualifier)
├── Node 03: Secondary - Sky/Background (Color Correction + Power Window)
├── Node 04: Creative Grade (Grading Node + LUT + Curves)
├── Node 05: Global Adjustments (Color Warper, Color Wheels)
└── Node 06: Output Transform (Technical LUT)
```

## Parameters Reference

| Parameter | Typical Range | Notes |
|-----------|---------------|-------|
| Lift/Gamma/Gain | -1.0 to +1.0 | Relative to middle gray |
| Offset | -1.0 to +1.0 | Global lift |
| Saturation | 0.0 to 2.0 | 1.0 = neutral |
| LUT Intensity | 0.0 to 1.0 | Key Output Gain |
| Qualifier Hue | 0-360° | Center of selection |
| Qualifier Sat | 0-1.0 | Width of selection |
| Qualifier Lum | 0-1.0 | Luminance range |
| Power Window Softness | 0-100 | Edge feather |

## Tips & Best Practices

1. **Order Matters**: Primary → Secondary → Creative → Output
2. **Use Node Labels**: Label nodes (P: Primary, S: Skin, C: Creative) for readability
3. **Version Grades**: Use Grade Versions (Local/Remote) to experiment
4. **Color Management**: Enable DaVinci YRGB Color Managed for consistent pipeline
5. **Scopes**: Always reference Waveform (exposure), Vectorscope (skin tones), Parade (RGB balance)
6. **LUT Interpolation**: Always use Tetrahedral for creative LUTs to avoid banding

## Related Skills
- `davinci-resolve-lut-workflow` - Advanced LUT management
- `instagram-reel-color-grading-workflow` - Instagram-specific looks
- `davinci-resolve-color-management` - Color space/transform setup