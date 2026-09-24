---
name: skin-tones-portrait-color-grading
description: Professional skin tone grading workflows for portrait, beauty, and people-focused content. Covers Color Wheels, Qualifier, Curves, Power Windows for skin isolation, background separation, and natural enhancement.
trigger: User wants to grade skin tones, enhance portraits, separate subjects from backgrounds, or create flattering people-focused looks.
category: davinci-resolve/color-grading
tags: [skin-tones, portrait, beauty, color-wheels, qualifier, curves, power-windows, background-separation, vignette, natural-look]
steps:
  - name: Subtle Skin Tone Enhancement & Background Separation (C18_hSSPmOY)
    description: 4-node workflow: balance → curves → skin qualifier → background vignette
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [ColorWheel, Curves, Qualifier]
    parameters:
      ColorWheel_Lift_Gamma_Gain:
        lift: [1.0, 1.0, 1.0]
        gamma: [1.0, 1.0, 1.0]
        gain: [1.0, 1.0, 1.0]
      Curves_Midtones:
        gamma: 1.0
      Qualifier_Hue: [0.0, 1.0]
      Qualifier_Saturation: [0.0, 1.0]
      Qualifier_Luminance: [0.0, 1.0]
    steps:
      - Add a new node
      - Use the Color Wheels to make subtle adjustments to Lift, Gamma, and Gain to balance the overall exposure and contrast
      - Add another node
      - Use the Curves tool to fine-tune the midtones for a more pleasing look
      - Add a third node
      - Use the Qualifier to select the skin tones
      - Make subtle adjustments to Hue, Saturation, and Luminance within the Qualifier to enhance the skin tones without making them look unnatural
      - Add a fourth node
      - Use a power window to create a subtle vignette or to further separate the subject from the background by slightly darkening or adjusting the background colors
    difficulty: intermediate
    video_id: C18_hSSPmOY
    tags: [color grading, skin tones, background separation, subtle adjustments]

  - name: Casual Color Grading (DGBm_L7SqNS)
    description: Simple one-node color correction for casual/natural portrait look
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Node for color correction]
    parameters:
      color_correction_node:
        saturation: "100%"
        contrast: "50%"
        temperature: "6000K"
    steps:
      - Import the footage into DaVinci Resolve
      - Apply a basic color correction node to the clip
    difficulty: beginner
    video_id: DGBm_L7SqNS
    tags: [color grading, Instagram Reel, Casual Photography]

  - name: Instagram Reel Color Correction (DFD15P6xMfi)
    description: Color wheel-based skin tone enhancement for social media portraits
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Node for color correction, Node for adjusting exposure]
    parameters:
      param1: "Adjusting saturation to enhance the subject's skin tone"
      param2: "Balancing the contrast and brightness to create a more dynamic image"
    steps:
      - Import the Instagram Reel into DaVinci Resolve
      - Apply color correction using the color wheel tool
    difficulty: Intermediate
    video_id: DFD15P6xMfi
    tags: [Color grading, Instagram reels editing, DaVinci Resolve tutorial]

  - name: Instagram Reel Color Grading (DBsxmNLS1Lz)
    description: Color Wheels + LUT workflow for social media portrait grading
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Color Wheels, LUTs]
    parameters:
      param1: "Adjusting the LUT for a specific look"
    steps:
      - Importing the footage into DaVinci Resolve
      - Applying color correction using Color Wheels and LUTs
    difficulty: intermediate
    video_id: DBsxmNLS1Lz
    tags: [Color Grading, Instagram Reel, DaVinci Resolve]

  - name: S-Log3 Skin Tone Exposure Workflow (DYR3FBWtxn3)
    description: Sony S-Log3 specific workflow for proper skin tone exposure
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [Raw vs Log workflow]
    parameters:
      workflow: "S-Log3 skin tone exposure"
    steps:
      - Expose S-Log3 for skin tones (typically +1.5 to +2 stops over middle gray)
      - Use CST to convert to Rec.709
      - Fine-tune with Color Wheels
    difficulty: intermediate
    video_id: DYR3FBWtxn3
    tags: [raw vs log, S-Log3, skin tones, exposure]

  - name: S-Log3 Workflow from @sprin (DYE7JNyAR07)
    description: Professional S-Log3 grading workflow for natural skin tones
    resolve_page: Color|Edit|Fusion|Fairlight
    node_graph_type: serial
    key_nodes: [S-Log3 Workflow]
    parameters:
      workflow: "S-Log3 from @sprin"
    steps:
      - Apply S-Log3/S-Gamut3.Cine CST
      - Normalize exposure
      - Grade skin tones with Qualifier
    difficulty: intermediate
    video_id: DYE7JNyAR07
    tags: [S-Log3, Workflow, @sprin]
parameters:
  - name: ColorWheel_Lift_Gamma_Gain
    description: Lift/Gamma/Gain RGB values for primary balance
  - name: Curves_Midtones
    description: Midtone gamma adjustment via Curves
  - name: Qualifier_Hue
    description: Hue range for skin tone selection (typically 20-50° for caucasian, broader for diverse tones)
  - name: Qualifier_Saturation
    description: Saturation range for skin selection
  - name: Qualifier_Luminance
    description: Luminance range for skin selection
  - name: Power_Window_Softness
    description: Feathering for background separation vignette
tags: [skin-tones, portrait, beauty, color-wheels, qualifier, curves, power-windows, background-separation, vignette, natural-look, s-log3, instagram]
---

# Skin Tones & Portrait Color Grading

Professional **skin tone workflows** for portraits, beauty, interviews, and people-focused content. Covers isolation, enhancement, background separation, and natural-looking results across skin tones.

## Techniques Included

### 1. Subtle Skin Tone Enhancement & Background Separation (C18_hSSPmOY)
**4-Node Professional Workflow**

| Node | Tool | Purpose |
|------|------|---------|
| 1 | Color Wheels | Balance exposure/contrast globally |
| 2 | Curves | Fine-tune midtone density |
| 3 | Qualifier | Isolate & enhance skin tones |
| 4 | Power Window | Vignette for subject separation |

**Key Parameters**:
- **Qualifier**: Hue 20-50°, Sat 20-60%, Lum 20-80% (adjust per skin tone)
- **Enhancement**: +5-10% saturation, slight warmth, -5% luminance for density
- **Vignette**: Soft round window, 0.5-1.0 feather, -0.1 to -0.2 exposure

### 2. Casual Color Grading (DGBm_L7SqNS)
**One-Node Natural Look**

- **Saturation**: 100% (neutral)
- **Contrast**: 50% (slight punch)
- **Temperature**: 6000K (slightly warm)
- **Use**: Quick turnaround, natural aesthetic

### 3. Instagram Reel Color Correction (DFD15P6xMfi)
**Social Media Portrait Workflow**

- **Node 1**: Color Wheels for skin tone saturation
- **Node 2**: Exposure/contrast balance
- **Focus**: Dynamic but natural for mobile viewing

### 4. Color Wheels + LUT Workflow (DBsxmNLS1Lz)
**Creative LUT + Manual Refinement**

- **Base**: LUT for look (Kodak 2383, Fuji, custom)
- **Refine**: Color Wheels to correct LUT on skin
- **Protect**: Qualifier on skin before LUT (parallel node)

### 5. S-Log3 Skin Tone Exposure (DYR3FBWtxn3, DYE7JNyAR07)
**Sony Log Workflow for Skin**

1. **Expose**: +1.5 to +2 stops over middle gray for skin
2. **CST**: S-Log3/S-Gamut3.Cine → Rec.709/Gamma 2.4
3. **Normalize**: Lift shadows, roll off highlights
4. **Skin**: Qualifier isolation, subtle warmth + density
5. **Protect**: Power Window on face for consistency

## Skin Tone Qualifier Ranges (Starting Points)

| Skin Tone | Hue | Saturation | Luminance |
|-----------|-----|------------|-----------|
| **Light/Fair** | 25-35° | 15-40% | 40-80% |
| **Medium/Olive** | 30-45° | 20-50% | 30-70% |
| **Deep/Rich** | 20-40° | 25-60% | 20-60% |
| **Universal** | 20-50° | 15-60% | 20-80% |

*Always refine with eyedropper + softness/edge blur*

## Pro Skin Grading Workflow

```
Node 1: Primary Balance (Color Wheels)
    ↓
Node 2: Contrast/Density (Curves - gentle S)
    ↓
Node 3: Skin Isolation (Qualifier → Color Wheels)
    ↓
Node 4: Skin Texture (Midtone Detail / Blur)
    ↓
Node 5: Background Separation (Power Window Vignette)
    ↓
Node 6: Global Look (LUT or Creative Grade)
    ↓
Node 7: Skin Protection (Parallel: Qualifier invert → LUT)
```

## Key Principles

1. **Protect First** - Qualify skin *before* creative LUTs
2. **Subtle is Better** - 5% changes visible on faces
3. **Consistency** - Power Window tracks face across cuts
4. **Texture** - Midtone Detail +1 to +5 for pore structure
5. **Separation** - Vignette or background desat pushes subject forward

## Common Skin Issues & Fixes

| Issue | Fix |
|-------|-----|
| **Orange/Red** | Qualifier → Hue shift toward yellow, reduce sat |
| **Magenta** | Qualifier → Hue shift toward yellow/orange |
| **Green (fluorescent)** | Qualifier → Hue shift toward magenta/red |
| **Washed out** | Curves → lift midtones, add contrast |
| **Blotchy** | Qualifier → Blur radius 5-10, reduce noise |
| **Shiny/Oily** | Power Window → Highlights -0.1 to -0.2 |

## Background Separation Techniques

1. **Vignette**: Round Power Window, high feather, -0.15 exposure
2. **Desaturate BG**: Inverse window → Saturation -20 to -30%
3. **Cool BG**: Inverse window → Color Wheels → Lift toward teal
4. **Blur BG**: Inverse window → Blur radius 2-5 (simulate shallow DOF)
5. **Combine**: Subtle vignette + slight desat + cool shift = cinematic

## S-Log3 Specific Tips

- **Expose for skin**: Zebra at 70% (skin), not 90% (white)
- **CST first**: Always CST before grading
- **LUT last**: Creative LUT after skin protection
- **Noise**: NR on Node 1 (temporal 2, spatial 5) before skin work