---
name: davinci-color-correction-lut-workflow
description: Professional color correction and LUT workflow in DaVinci Resolve. Covers primary correction, creative LUT application, node structures, CST workflows, and matching grades across clips.
trigger: color correction, LUT, color grading, CST, color space transform, node structure, primary correction, creative grade, davinci resolve color
steps:
  - "Import footage, set project color space (DaVinci YRGB / ACES)"
  - "Set clip input color space (Camera Raw settings or CST Input)"
  - "Node 1: Primary Correction - Balance, Exposure, Contrast, Saturation"
  - "Node 2: Creative LUT (Film Look, Kodak 2383, Fuji, Custom)"
  - "Node 3: Secondary Adjustments - Skin tones, Sky, Foliage (Qualifiers)"
  - "Node 4: Global Adjustments - Vignette, Grain, Halation, Glow"
  - "Node 5: Output Transform (CST to Rec.709/sRGB/P3)"
  - "Save as PowerGrade (.drx) for reuse across projects"
parameters:
  - name: color_science
    type: string
    description: Color management mode
    enum: ["DaVinci YRGB", "DaVinci YRGB Color Managed", "ACEScc", "ACESct"]
    default: "DaVinci YRGB Color Managed"
  - name: input_color_space
    type: string
    description: Camera/source color space
    enum: ["S-Log3/S-Gamut3.Cine", "V-Log/V-Gamut", "C-Log3/Cinema Gamut", "BRAW", "RAW (BMD Film)", "Rec.709", "Rec.2020"]
    default: "S-Log3/S-Gamut3.Cine"
  - name: output_color_space
    type: string
    description: Delivery color space
    enum: ["Rec.709 Gamma 2.4", "Rec.709 Gamma 2.2", "sRGB", "P3-D65", "HDR ST.2084 (PQ)", "HDR HLG"]
    default: "Rec.709 Gamma 2.4"
  - name: lut_type
    type: string
    description: LUT category
    enum: ["Technical (CST)", "Creative Film Print (Kodak 2383)", "Creative Film Stock (Fuji, Kodak)", "Creative Look (Teal/Orange, Bleach Bypass)", "Custom .cube/.3dl"]
    default: "Creative Film Print (Kodak 2383)"
  - name: lut_intensity
    type: number
    description: LUT blend strength (0-1, use Key Output Gain)
    default: 1.0
    minimum: 0
    maximum: 1
  - name: node_structure
    type: string
    description: Node graph topology
    enum: ["Serial (Linear)", "Parallel (Layer Mixer)", "Layer Mixer + Parallel", "Compound Node"]
    default: "Serial (Linear)"
tags:
  - color-correction
  - lut
  - color-grading
  - davinci-resolve
  - cst
  - color-space-transform
  - primary-correction
  - creative-grade
  - powergrade
  - node-structure
  - aces
  - color-management
category: davinci-resolve-color
---

# DaVinci Resolve Color Correction & LUT Workflow

Professional color correction pipeline using DaVinci Resolve's Color page. Covers color-managed workflows, node structures, LUT application strategies, and grade matching.

## Color Management Setup (Project Settings)

### Option A: DaVinci YRGB Color Managed (Recommended)
```
Project Settings → Color Management:
- Color Science: DaVinci YRGB Color Managed
- Color Processing Mode: "Use Project Settings"
- Timeline Color Space: DaVinci Wide Gamut Intermediate (DWG)
- Output Color Space: Rec.709 Gamma 2.4 (or target delivery)
- Color Science Version: Latest (v2024+)

Clip Level (Right-click clip → Input Color Space):
- Auto-detect from metadata (BRAW, ARRI, Sony, Canon, etc.)
- Manual override if needed
```

### Option B: ACES 2.0 (High-End/VFX Pipeline)
```
Project Settings → Color Management:
- Color Science: ACEScc or ACESct
- ACES Version: 2.0
- Input Device Transform (IDT): Per camera (auto or manual)
- Output Device Transform (ODT): Rec.709, P3-D65, HDR ST.2084
- Working Space: ACES2065-1 / ACEScct

Benefits: Industry standard, VFX interchange, future-proof
Cost: Steeper learning curve, LUTs must be ACES-compatible
```

### Option C: DaVinci YRGB (Legacy/Simple)
```
Project Settings → Color Management:
- Color Science: DaVinci YRGB
- No color management - manual CST nodes required
Use for: Quick turnaround, non-log footage, legacy projects
```

## Node Graph Structures

### Structure 1: Serial (Linear) - Standard
```
Node 1: Primary Correction (Balance/Exposure)
Node 2: Creative LUT / Look
Node 3: Secondary (Skin, Sky, Qualifiers)
Node 4: Global FX (Vignette, Grain, Halation)
Node 5: Output CST (if not color managed)

Flow: 1 → 2 → 3 → 4 → 5
Best for: Single-look grades, speed, simplicity
```

### Structure 2: Parallel (Layer Mixer) - Independent Adjustments
```
Layer Mixer (Normal/Composite):
├── Node 1a: Shadows/Lift Grade
├── Node 1b: Midtones/Gamma Grade
├── Node 1c: Highlights/Gain Grade
└── Node 2: Creative LUT (on mixed result)

Node 3: Secondary (after mixer)
Node 4: Global FX
Node 5: Output CST

Best for: Split-toning, independent shadow/mid/highlight control
```

### Structure 3: Compound Node (Reusable Grade Package)
```
Compound Node "MyFilmLook":
├── Internal Node 1: Primary
├── Internal Node 2: LUT (Kodak 2383 @ 50%)
├── Internal Node 3: Skin Qualifier
├── Internal Node 4: Grain
└── Published Inputs: LUT Strength, Grain Amount, Vignette

Main Graph:
Node 1: CST Input → Rec.709
Node 2: Compound Node "MyFilmLook"
Node 3: CST Output → Delivery

Best for: Template grades, team sharing, versioning
```

## Primary Correction (Node 1) - Step by Step

### 1. Balance (White Balance)
```
Tools: Temperature, Tint, OR RGB Lift/Gamma/Gain wheels
Method A (Wheels):
- Lift (Shadows): Push toward blue for cool, orange for warm
- Gamma (Midtones): Main WB adjustment
- Gain (Highlights): Fine-tune highlight tint

Method B (Temp/Tint):
- Temperature: 2800K (tungsten) → 10000K (shade)
- Tint: -50 (green) → +50 (magenta)

Tip: Use Parade RGB scope - align R/G/B peaks in shadows
```

### 2. Exposure (Contrast/Pivot or Custom Curves)
```
Contrast/Pivot Method:
- Contrast: 0.1-0.3 (subtle)
- Pivot: 0.4-0.5 (protect midtones)

Custom Curves (More Control):
- Master Curve: Gentle S-curve
  Shadows: Lift: +0.05, Gamma: 0.95, Gain: 1.02
- RGB Individual: Red channel slightly lifted in shadows for warmth
```

### 3. Saturation
```
Global Saturation: 50-65 (log footage starts ~10-20)
Or: HSV Curves → Sat vs Sat (protect skin tones)
  - Low sat: Boost slightly
  - High sat: Compress slightly
```

### 4. Color Boost (Optional)
```
Color Wheels → Offset (Master): Tiny push toward look direction
- Teal/Orange: Offset toward cyan in shadows, orange in highlights
- Filmic: Slight green in shadows, red in highlights
```

## Creative LUT Application (Node 2)

### LUT Placement Strategies

#### Strategy A: LUT as "Look" (After Primary)
```
Node 1: Primary Correction (normalize log → linear-ish)
Node 2: Creative LUT (Kodak 2383, Fuji 3510, custom)
Node 3: Post-LUT tweaks (skin, saturation, contrast)

Key: LUT expects "correct" input → Primary must normalize first
```

#### Strategy B: LUT as "Base" (Before Primary) - Rare
```
Node 1: Creative LUT (on log footage)
Node 2: Primary Correction (adjust LUT result)
Key: Only for LUTs designed for log input (technical LUTs)
```

#### Strategy C: LUT in Parallel (Blend Control)
```
Layer Mixer:
├── Node A: Primary Grade (100% opacity)
├── Node B: LUT Only (50% opacity, or Key Output Gain)
└── Composite: Normal/Add/Overlay

Control: Key Output Gain on LUT node = LUT intensity slider
```

### Essential LUT Pack Recommendations

| LUT Pack | Type | Best For | Intensity |
|----------|------|----------|-----------|
| Kodak 2383 (Free) | Film Print | Universal, skin tones | 50-70% |
| Fuji 3510/3513 | Film Print | Greens, nature, portraits | 50-80% |
| ARRI K1S1/K2S2 | Technical | Alexa LogC → Rec.709 | 100% (technical) |
| Cineon Log → Rec.709 | Technical | Scanned film | 100% |
| DJI D-Log → Rec.709 | Technical | Drone footage | 100% |
| Custom .cube | Creative | Signature look | 30-100% |

### LUT Technical Details
```
Format: .cube (3D LUT) or .3dl
Size: 17^3, 33^3, 65^3 (larger = smoother, slower)
Bit Depth: 10-bit or 12-bit preferred
Color Space: Must match input (Log → Rec.709, or Log → Log)

Resolve LUT Folder:
macOS: ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/
Windows: %APPDATA%\Blackmagic Design\DaVinci Resolve\LUT\
Linux: ~/.local/share/DaVinciResolve/LUT/

Refresh: Project Settings → Color Management → "Update Lists"
```

## Secondary Corrections (Node 3+)

### Skin Tone Protection (Qualifier)
```
1. Add Node → Qualifier (HSL)
2. Select: Hue ~25-45 (skin range), Sat ~20-60, Lum ~20-80
3. Refine: Clean Black/White, Blur Radius 2-5
4. Enable "Highlight" mode to see selection
5. Adjust: Hue vs Hue (stabilize), Sat vs Sat (natural), Lum vs Sat (protect)
6. Key Output Gain: 0.5-1.0 for subtle correction
```

### Sky Replacement/Enhancement
```
1. Qualifier: Hue 190-240 (blue), Sat 30-100, Lum 30-90
2. Power Window: Gradient (top of frame) + Qualifier (intersect)
3. Adjust: Darken, saturate, push teal
4. Track window if camera moves
```

### Foliage/Grass
```
1. Qualifier: Hue 80-140 (green), Sat 20-80, Lum 20-70
2. Hue vs Hue: Shift yellow-green → pure green
3. Sat vs Sat: Reduce oversaturated yellows
```

## Global Effects (Final Nodes)

### Film Grain (Resolve FX Film Grain)
```
Type: Kodak 5219 / Fuji F64 / Custom
Size: 0.5-1.0 (relative to resolution)
Strength: 0.15-0.35 (subtle)
Softness: 0.2-0.5
Color: ON (chromatic grain)
```

### Halation (Resolve FX Glow - "Halation" mode)
```
Threshold: 0.85-0.95 (only brightest highlights)
Size: 10-30 pixels
Strength: 0.1-0.3
Color: Warm (orange/red tint)
Mix: Screen/Add
```

### Vignette (Power Window + Curves)
```
1. Circular Power Window (soft edge 0.8-1.0)
2. Invert window
3. Custom Curves → Master: Pull down shadows slightly
4. Or: Color Wheels → Gain → Lower slightly
```

### Glow/Bloom (Resolve FX Glow)
```
Mode: Standard or Soft Light
Threshold: 0.7-0.9
Size: 20-100
Intensity: 0.1-0.3
Use sparingly - modern sensors don't bloom naturally
```

## Output Transform (If Not Color Managed)

### CST Node (Color Space Transform)
```
Node: Color Space Transform (Resolve FX)
Input Color Space: [Camera Log, e.g., S-Log3/S-Gamut3.Cine]
Output Color Space: [Delivery, e.g., Rec.709 Gamma 2.4]
Tone Mapping: None (for SDR), or "ST.2084" for HDR
Gamut Mapping: "Perceptual" or "Saturation"
```

### Manual Alternative (Curves + Saturation)
```
If no CST: Custom Curves to approximate
- Lift shadows, roll off highlights
- Desaturate highlights (Sat vs Lum curve)
- Not recommended for professional delivery
```

## Grade Matching Across Clips

### Method 1: Still Reference (Gallery)
```
1. Grade hero clip perfectly
2. Color page → Gallery → "Grab Still" (or Ctrl+G)
3. Select target clips → Right-click still → "Apply Grade"
4. Fine-tune each clip (exposure/WB differ)
```

### Method 2: Copy/Paste Node Graph
```
1. Right-click graded clip → "Copy Grade" (or Ctrl+C)
2. Select target clips → Right-click → "Paste Grade" (Ctrl+V)
3. Or: Paste Attributes → Check "Color Grade" only
```

### Method 3: Color Group (Shared Grade)
```
1. Project Settings → Color Groups → Add Group "Main Look"
2. Select clips → Right-click → "Add to Color Group" → "Main Look"
3. Grade on Color Group pre-clip or post-clip node
4. All clips in group share that node
```

### Method 4: Remote Grades (Versioning)
```
1. Grade hero → Create Version "Master Grade"
2. Other clips → Right-click → "Attach Remote Grade" → Select "Master Grade"
3. Changes to Master propagate to all attached
```

## PowerGrade Export/Import (.drx)

### Export
```
1. Gallery → Right-click still → "Export" → .drx
2. Includes: Full node graph, LUTs (referenced), Power Windows, Keyframes
3. Save to: /LUT/PowerGrades/ or project folder
```

### Import
```
1. Gallery → Right-click → "Import" → Select .drx
2. LUTs must exist in Resolve LUT folder (or relink)
3. Apply like any Gallery still
```

## Scopes Reference

| Scope | Purpose | Target |
|-------|---------|--------|
| Parade RGB | Balance, exposure | Aligned R/G/B in shadows |
| Waveform (Luma) | Exposure, contrast | 0-100 IRE, skin ~55-65 IRE |
| Vectorscope | Saturation, hue | Skin tone line (10:30 position) |
| Histogram | Distribution | No clipping 0 or 1023 (10-bit) |
| CIE Chromaticity | Gamut, white point | Within target gamut |

## Quick Reference Card

```
NODE TEMPLATE (Save as PowerGrade):

N1  Primary: Temp/Tint | Contrast/Pivot | Saturation | Custom Curves
N2  LUT:      [Creative LUT] @ Key Output Gain 0.5-1.0 (published)
N3  Skin:     Qualifier (HSL) → Hue/Sat/Lum curves
N4  Sky:      Power Window + Qualifier → Curves
N5  Global:   Grain | Halation | Vignette | Glow (published params)
N6  Output:   CST (if not color managed)

Published Parameters (right-click node → Publish):
- LUT Strength (N2 Key Output Gain)
- Grain Amount (N5 Strength)
- Vignette Amount (N5 Curve Master)
- Halation Strength (N5 Glow Intensity)
```

## Related Skills

- `davinci-color-management-aces` - ACES workflow deep dive
- `davinci-skin-tone-workflow` - Advanced skin tone techniques
- `davinci-hdr-grading` - HDR PQ/HLG grading and delivery
- `davinci-lut-design` - Creating custom .cube LUTs
- `davinci-color-match` - Shot matching techniques