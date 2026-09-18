---
name: davinci-color-grading-techniques
description: Core color grading techniques - Offset balancing, Teal/Orange, Selective masking, Primary wheels, Curves, HSL, LUT workflows
category: davinci-resolve
tags: [color-grading, color-correction, teal-orange, offset, curves, hsl, lut, primary-wheels, masking, color-wheels]
trigger: Use when user asks about color grading, color correction, color wheels, curves, LUTs, teal/orange look, offset balancing, HSL qualifier, or primary/secondary grading
---

# DaVinci Resolve Color Grading Techniques

Core color grading workflows and techniques for the Color page - from primary balance to creative looks.

## Techniques Included

### 1. Global Offset Color Balancing
**Video ID:** `C9m9A2SpR-_` | **Difficulty:** Beginner | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Offset Node
- **Parameters:** Offset: 25.00, Lift: 25.00, Gamma: 25.00, Gain: 1.00
- **Steps:**
  1. Import the video clip into the timeline
  2. Navigate to the Color page
  3. Select the Offset tool in the color wheels panel
  4. Adjust the circular color wheel to balance the global color tint and exposure
  5. Monitor the Waveform scopes to ensure highlights are not clipping
- **Tags:** color grading, mobile, offset, video editing

### 2. Teal and Orange Cinematic Grade
**Video ID:** `Cve9BKQocVN` | **Difficulty:** Beginner | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Primary Wheels, Curves, Hue/Saturation/Luma
- **Parameters:** Saturation: +15, Contrast: Increased, Midtones: Warm/Orange, Shadows: Teal/Blue
- **Steps:**
  1. Add a primary node to adjust contrast and white balance
  2. Use the Color Wheels to push shadows toward teal/blue
  3. Use the Offset or Wheels to push midtones/highlights toward a warm orange/yellow
  4. Use the Hue/Saturation curve to de-saturate greens if they appear distracting
  5. Apply a slight vignette to draw focus to the central island formation
- **Tags:** color grading, cinematic, aerial, teal-and-orange

### 3. Selective Subject Polygon Masking
**Video ID:** `C-ZGotYNz4b` | **Difficulty:** Intermediate | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Qualifier/Window, Primary Grade
- **Parameters:** Window Type: Polygon, Tracking: Active, Offset: 25.00
- **Steps:**
  1. Go to the Color page
  2. Select the Polygon Window tool from the Window tab
  3. Draw a custom path around the desired subject
  4. Go to the Tracker tab and click play to track the mask to the subject movement
  5. Apply color adjustments using the Primary Wheels or Curves to affect the masked area
- **Tags:** masking, color-grading, polygon, isolation

### 4. Artificial Depth of Field / Focus Blur
**Video ID:** `Cv2MWyANfG7` | **Difficulty:** Intermediate | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Gaussian Blur, Magic Mask
- **Parameters:** Blur Radius: 25.0, Strength: 1.0
- **Steps:**
  1. Import footage and go to the Color Page
  2. Use the Magic Mask to isolate the subject (the drone)
  3. Create a new node for the background
  4. Add a Gaussian Blur or Lens Blur effect to the background node
  5. Adjust the blur radius to create a cinematic shallow depth of field
- **Tags:** cinematic, drone, depth-of-field, tutorial

### 5. Instagram Reel C_VmwLspFQC - Save (LUT Application)
**Video ID:** `C_VmwLspFQC` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Steps:**
  1. Step 1: Import the Instagram Reel C_VmwLspFQC into DaVinci Resolve
  2. Step 2: Apply a LUT (Look-Up Table) to the footage to enhance colors and contrast
- **Tags:** color grading, Instagram Reel, DaVinci Resolve

---

## Color Grading Fundamentals

### Node Graph Architecture

#### Serial (Sequential) - Default
```
Node 01 → Node 02 → Node 03 → Output
```
Each node receives output of previous. Standard for primary → secondary → creative.

#### Parallel (Side-by-Side)
```
       → Node A →
Input →          → Merge → Output
       → Node B →
```
Multiple grades from same source, blended. Good for: skin tone + background separate.

#### Layer Mixer (Composite)
```
Node 01 (Base)
    ↓
Layer Mixer ← Node 02 (Overlay: Add/Screen/Overlay)
    ↓
Output
```
Compositing modes between nodes. Good for: glow, texture overlays.

#### Compound (Nested)
```
Compound Node
  └── Internal Graph (Serial/Parallel)
```
Encapsulate complex graphs. Reusable as "PowerGrade".

---

### Essential Node Structure (Standard Workflow)

```
N01: CST / Input Transform     ← Camera Log → Working Space
N02: Primary Balance           ← Exposure, WB, Contrast, Saturation
N03: Exposure/Contrast Trim    ← Fine-tune after N02
N04: Creative LUT / Look       ← Show LUT, Film Emulation (Key Gain ~0.6)
N05: Skin Tone Protection      ← Qualifier: Skin → Hue vs Hue/Sat
N06: Sky/Background            ← Power Window + Grade
N07: Subject Isolation         ← Magic Mask / Qualifier + Grade
N08: Vignette / Focus          ← Circular Window
N09: Output Transform          ← Working → Display (Rec.709/P3)
```

---

## Primary Color Tools

### Color Wheels (Primary)
| Wheel | Controls | Typical Use |
|-------|----------|-------------|
| **Lift** | Shadows | Black level, shadow tint |
| **Gamma** | Midtones | Exposure, skin tones |
| **Gain** | Highlights | White level, highlight tint |
| **Offset** | Entire image | Global shift, creative tint |

**Log Wheels** (DaVinci YRGB Color Managed):
- Shadows/Midtones/Highlights mapped to log ranges
- Better for log footage

**HDR Wheels** (HDR Grading):
- Specular Highlights / Highlights / Midtones / Shadows
- For ST.2084 / HLG workflows

### Curves
| Curve | Controls | Best For |
|-------|----------|----------|
| **Custom (RGB)** | Master R/G/B channels | Precision contrast, cross-process |
| **Hue vs Hue** | Shift hue ranges | Skin tone fix, sky color |
| **Hue vs Sat** | Saturation per hue | Selective desaturation |
| **Hue vs Lum** | Luminance per hue | Brighten/darken specific colors |
| **Lum vs Sat** | Saturation per luminance | Shadow desat, highlight pop |
| **Sat vs Sat** | Saturation compression | Film-like roll-off |

### Color Warper (Resolve 18+)
- 3D grid: Hue (circular) × Saturation (radial) × Luminance (depth)
- Direct manipulation: drag points on grid
- Great for: skin tones, creative shifts, matching

---

## Secondary Grading Tools

### Qualifier (HSL Keyer)
```
Qualifier Panel:
├── Hue: [Center, Width, Softness]
├── Saturation: [Low, High, Softness]
├── Luminance: [Low, High, Softness]
├── 3D Viewer: Visualize key in 3D
├── Clean: Erode, Dilate, Blur, Shrink/Grow
└── Invert: Flip selection
```

**Pro Tip:** Use "Highlight" mode (eyeball icon) to see matte. Refine with Clean controls.

### Power Windows (Shapes)
| Shape | Use Case |
|-------|----------|
| **Circle/Oval** | Vignette, face/eye brightening |
| **Rectangle** | Horizon, sky, product |
| **Polygon** | Custom shapes (buildings, subjects) |
| **Gradient** | Sky gradients, radial falloff |
| **Curve** | Organic shapes |

**Tracking:** Tracker tab → Track Forward/Backward → Stabilize or Perspective

### Magic Mask (AI Rotoscoping)
- **Studio 18.5+** only
- Draw strokes: Green = Foreground, Red = Background
- Track → Refine → Output as Alpha
- Best for: People, animals, vehicles with clear separation

---

## Creative Looks

### Teal & Orange (Blockbuster)
```
N01: CST (Log → DWG)
N02: Primary (Balance, protect skin)
N03: Color Warper / Wheels:
     Shadows → Teal (Hue ~180, Sat +20)
     Midtones → Orange (Hue ~30, Sat +15)
N04: Hue vs Sat: Desaturate Greens (-20)
N05: Curves: Slight S-curve contrast
N06: Vignette (Subtle)
```

### Bleach Bypass (High Contrast, Desaturated)
```
N01: CST
N02: Primary
N03: RGB Mixer:
     Red: R=100, G=0, B=0
     Green: R=0, G=100, B=0
     Blue: R=0, G=0, B=100
     → Luma Mix = 0.5 (50% desat)
N04: Contrast +20, Pivot 0.5
N05: Lift slightly (milky blacks)
```

### Film Emulation (Kodak 2383 / Fuji 3510)
```
N01: CST (Camera → DWG)
N02: Primary
N03: Film LUT (Kodak 2383 / Fuji 3510)
     Key Output Gain: 0.4-0.6
N04: Halation (Glow OFX or Custom)
N05: Film Grain (Film Grain OFX)
N06: Gate Weave (Subtle)
N07: CST (DWG → Rec.709)
```

### Cross Process (Color Shift)
```
N01: CST
N02: Primary
N03: RGB Curves:
     Red: Lift shadows, lower highlights
     Green: S-curve
     Blue: Raise shadows, lower midtones
N04: Hue vs Hue: Shift cyans→blue, reds→magenta
```

---

## LUT Workflow

### LUT Types
| Type | Use | Bit Depth |
|------|-----|-----------|
| **1D LUT** | Gamma, simple curves | 10-bit |
| **3D LUT** | Complex color transforms | 17³, 33³, 65³ |
| **CDL** | Slope/Offset/Power/Personality | Metadata |

### LUT Application Methods

#### Method 1: Node LUT (Per Node)
```
Node → Right-click → 3D LUT → Select LUT
→ Key Output Gain: Adjust intensity
```

#### Method 2: Clip LUT (Input)
```
Media Pool → Right-click clip → LUT → Select
→ Applied before node graph
```

#### Method 3: Timeline LUT
```
Timeline → Right-click → LUT → Select
→ Applied after all node grades
```

#### Method 4: Project LUT (Monitor)
```
Project Settings → Color Management → 3D Output LUT
→ Monitor only, not baked
```

### LUT Best Practices
- **Know your LUT:** Input space (LogC, S-Log3, D-Log) → Output space (Rec.709, P3)
- **Don't stack LUTs** without understanding compound transform
- **Use Key Gain** to blend LUT (0.5 = 50% LUT)
- **CST > LUT** when possible (math vs lookup table)
- **Test on scopes:** Vectorscope skin tone line, Waveform legal range

---

## Color Management (DaVinci YRGB Color Managed)

### Setup (Project Settings → Color Management)
```
Color Science: DaVinci YRGB Color Managed
Color Processing: DaVinci Wide Gamut Intermediate
Output Color Space: Rec.709 (sRGB) / P3-D65 / Rec.2020
Tone Mapping: Automatic / Custom
```

### Input Color Space (Per Clip / Timeline)
| Camera | Setting |
|--------|---------|
| ARRI | ARRI LogC3 / LogC4 |
| Sony | S-Log3 / S-Gamut3.Cine |
| RED | Log3G10 / REDWideGamut |
| DJI | D-Log / D-Log M |
| Canon | C-Log3 / Cinema Gamut |
| Blackmagic | BM Film / Gen 5 |

### Benefits
- Consistent pipeline across cameras
- LUTs work predictably
- HDR/SDR from same grade
- Future-proof

---

## Scopes Reference

### Waveform (Luma)
- 0-1023 (10-bit) or 0-1.0 (float)
- Legal: 64-940 (Rec.709)
- Skin: ~55-65 IRE

### Vectorscope (Chroma)
- Skin tone line: ~11 o'clock (Flesh Tone)
- Saturation: Distance from center
- 75% color bars: Targets at boxes

### Parade (RGB)
- Three waveforms side by side
- White balance: Align R/G/B in neutrals
- Clipping: Any channel > 1023

### Histogram
- Distribution of luminance
- Shadows left, highlights right
- Gaps = missing data (banding risk)

---

## Common Problems & Fixes

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| **Banding in skies** | 8-bit, heavy compression | Add noise (Film Grain 0.5%), dither, 10-bit export |
| **Skin tones wrong** | WB off, color cast | Vectorscope → Align to skin tone line; Hue vs Hue |
| **Highlight clipping** | Waveform > 1023 | Highlight roll-off (Curves), HDR Wheels |
| **Muddy shadows** | Lift too high, no contrast | Lower Lift, increase Contrast/Pivot |
| **LUT looks wrong** | Wrong input space | Check CST input, use correct camera profile |
| **Color shift on export** | Color space mismatch | Verify Output CST, check Delivery settings |

---

## Skill Trigger Examples

- "How do I do teal and orange grade in DaVinci?"
- "Offset wheel vs Lift/Gamma/Gain"
- "Polygon window tracking not working"
- "Magic Mask for background blur"
- "LUT workflow DaVinci Resolve"
- "Color managed workflow setup"
- "Fix skin tones in color page"
- "Bleach bypass look DaVinci"
- "Film emulation LUT application"
- "Curves vs Wheels when to use"