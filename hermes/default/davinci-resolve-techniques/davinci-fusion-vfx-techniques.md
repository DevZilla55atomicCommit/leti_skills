---
name: davinci-fusion-vfx-techniques
description: Fusion page VFX, compositing, motion graphics, and node-based workflows - Grid Warp, Paint/Clone, Text+, Magic Mask, Depth masking
category: davinci-resolve
tags: [fusion, vfx, compositing, warp, paint, text, masking, motion-graphics, node-graph]
trigger: Use when user asks about Fusion page, VFX compositing, Grid Warp, Paint/Clone tool, Text+, Magic Mask, depth masking, or node-based workflows
---

# DaVinci Resolve Fusion VFX & Compositing Techniques

Fusion page node-based compositing for VFX, motion graphics, and advanced effects.

## Techniques Included

### 1. Luffy Stretch / Warp Distortion (Grid Warp)
**Video ID:** `C-nf4xytQUu` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Serial
- **Key Nodes:** MediaIn, Grid Warp, Transform, MediaOut
- **Parameters:** Grid Warp Type: Bilinear, Mesh Density: High, Smoothness: Medium
- **Steps:**
  1. Add the clip to the Fusion page
  2. Add a Grid Warp node after the MediaIn
  3. Increase the mesh density to allow for finer control over the subject limbs
  4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
  5. Apply a Transform node to adjust the final framing after the distortion
  6. Add a Blur node if necessary to soften the edges of the distortion
- **Tags:** fusion, warp, vfx, onepiece, specialeffects

### 2. Text Behind Subject (Depth Masking - Fusion Method)
**Video ID:** `C_x0IZRODYf` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Serial
- **Key Nodes:** Text+, Alpha Output, Magic Mask
- **Parameters:** Font Style: Bold Serif, Tracking: Wide, Mask Softness: Low-to-Medium
- **Steps:**
  1. Import the clip to the Fusion page
  2. Add a Text+ node and type the desired text (GLOW TEXT EFFECT)
  3. Use the Magic Mask tool or a manual Polygon mask to select the subject (the person)
  4. Connect the mask to the Alpha channel of the Text+ node
  5. Adjust the text position so the subject overlaps with the letters
  6. Merge the masked text over the original background footage
- **Tags:** vfx, text-effect, masking, fusion, davinci-resolve

### 3. Object Removal using Patch Replacement / Clone (Paint Node)
**Video ID:** `C_yv2diSvey` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Layer Mixer
- **Key Nodes:** MediaIn, Paint Node, Merge, MediaOut
- **Parameters:** Paint Tool: Clone, Stroke Type: Smart, Opacity: 1.0
- **Steps:**
  1. Import the clip into the Fusion page
  2. Add a Paint node and connect it after MediaIn
  3. Select the Paint tool and choose Clone mode
  4. Hold Alt and click on a clean source area near the fishing wire
  5. Paint over the fishing wire to cover it with the clean pixels
  6. Adjust stroke smoothness to blend the patch seamlessly
- **Tags:** davinciresolve, vfx, objectremoval, fusion

---

## Fusion Node Graph Fundamentals

### Basic Node Flow
```
MediaIn → [Processing Nodes] → MediaOut
              ↓
        [Mask/Alpha Nodes]
              ↓
          Merge (combine)
              ↓
         MediaOut
```

### Essential Node Types

| Category | Nodes | Purpose |
|----------|-------|---------|
| **Input/Output** | MediaIn, MediaOut, Loader, Saver | Footage I/O |
| **Transform** | Transform, CornerPositioner, GridWarp | Position, scale, distort |
| **Color** | ColorCorrector, BrightnessContrast, Gamma, LUT | Color adjustments |
| **Masking** | RectangleMask, EllipseMask, PolygonMask, B-Spline | Shapes & rotoscoping |
| **Keying** | DeltaKeyer, UltraKeyer, ChromaKeyer | Green/blue screen |
| **Merge** | Merge, LayerMerge, ChannelBoolean | Compositing ops |
| **Text** | TextPlus, Text3D | Typography |
| **Paint** | Paint (Clone, Reveal, Blur, Sharpen) | Cleanup, retouch |
| **Tracking** | Tracker, PlanarTracker | Motion tracking |
| **Particles** | pEmitter, pRender, pTurbulence | Particle effects |
| **3D** | Camera3D, Renderer3D, Shape3D | 3D compositing |

---

## Grid Warp Deep Dive

### Grid Warp Node Controls
```
Grid Warp → Controls Tab:
├── Grid Size: [X: 10, Y: 10] (default) → Increase for more control points
├── Interpolation: Bilinear / Bicubic / BSpline
├── Show Grid: On/Off (viewport overlay)
├── Lock Aspect: Maintain proportions
└── Publish Controls: Expose specific points to modifier panel
```

### Warp Workflow for Character Distortion
1. **High Mesh Density:** Set X/Y to 20-40 for limb-level control
2. **Reference Frame:** Find neutral pose frame, key all points
3. **Keyframe Strategy:**
   - Key every 2-4 frames for smooth motion
   - Use "Smooth" interpolation (right-click keyframe → Smooth)
4. **Edge Handling:**
   - Add Blur node after Grid Warp (Radius 2-5)
   - Or use Soft Edge on grid boundary points

### Common Use Cases
- **Character stretch/squash** (cartoon style)
- **Lens distortion correction/creative**
- **Morphing between shapes**
- **Flag/wave simulations**

---

## Paint Node (Clone/Heal) Workflow

### Paint Node Modes
| Mode | Use Case | Shortcut |
|------|----------|----------|
| **Clone** | Copy pixels from source | Alt+Click to set source |
| **Reveal** | Reveal underlying layer | Brush over top layer |
| **Blur** | Soften edges | Brush size/strength |
| **Sharpen** | Enhance detail | Brush size/strength |
| **Smear** | Push pixels | Drag to smear |
| **Warp** | Local distortion | Drag to warp |

### Clone Tool Best Practices
1. **Source Sampling:** Alt+Click on clean area **per stroke** (not once)
2. **Brush Settings:**
   - Size: Match feature size
   - Softness: 50-80% for blending
   - Flow: 20-50% for buildup
   - Spacing: 10-20% for smooth strokes
3. **Stroke Type:** "Smart" for adaptive, "Single" for precise
4. **Layer Management:** Multiple Paint nodes for different objects

### Non-Destructive Paint Workflow
```
MediaIn → Paint (Clone wire removal)
    → Paint (Skin cleanup)
    → Paint (Object removal)
    → Merge (with clean plate if needed)
    → MediaOut
```

---

## Text+ (Fusion Titles) Advanced

### Text+ vs Text3D
| Feature | Text+ | Text3D |
|---------|-------|--------|
| 2D/3D | 2.5D (extrude) | True 3D |
| Shaders | Limited | Full material |
| Animation | Modifier-based | Keyframe + Modifiers |
| Performance | Fast | Heavy |
| Use Case | UI, lower thirds, simple 3D | Hero titles, 3D logos |

### Text+ Styling Pipeline
```
Text+ → Layout (Position, Tracking, Line Spacing)
     → Style (Font, Size, Color, Stroke, Shadow)
     → Transform (3D Position, Rotation, Scale)
     → Shading (Material, Lighting - if extruded)
     → Output (Alpha, RGB)
```

### Glow Text Effect (Common Social Media)
```
Text+ (White text, Bold)
    → Glow (Size: 20, Color: Brand, Blend: Screen)
    → Merge (Over footage, Blend: Add/Screen)
```

### Text Behind Subject (Fusion Method) - Node Graph
```
MediaIn (Background)
    │
    ├──→ Magic Mask → Polygon Mask (Subject) → Alpha
    │
    └──→ Text+ (Styled Text)
             │
             └──→ Merge (FG: Text, BG: MediaIn, EffectMask: Magic Mask Alpha)
                       │
                       → MediaOut
```

---

## Magic Mask (AI Rotoscoping) in Fusion

### Availability
- **Resolve Studio 18.5+** required
- **Fusion Page:** Tools → Magic Mask (or right-click viewer → Magic Mask)

### Workflow
1. Select clip in timeline → Fusion page
2. Add MediaIn → Magic Mask tool
3. Draw rough stroke on subject (foreground)
4. Draw rough stroke on background (optional)
5. Click "Track Forward" / "Track Backward"
6. Refine: Add strokes on problem frames
7. Output: Connect Mask to Merge.EffectMask or Paint.EffectMask

### Magic Mask Tips
- **Stroke Quality > Quantity:** Fewer, cleaner strokes track better
- **Keyframe Refinement:** Fix every 5-10 frames manually
- **Edge Softness:** 2-5 pixels for natural composites
- **GPU Memory:** Requires 8GB+ VRAM for 4K

---

## Depth-Based Compositing (Depth Map)

### Depth Map Sources
1. **DaVinci Depth Map** (Color page → Depth Map effect)
2. **Fusion Depth Map** (Camera3D → Renderer3D → Z-Depth)
3. **External:** Z-depth pass from 3D app (EXR)

### Depth Mask Node Graph
```
MediaIn (Beauty)
    │
    ├──→ Depth Map (Grayscale: White=Near, Black=Far)
    │
    └──→ Grade (Color Correct)
             │
             └──→ ChannelBoolean (Operation: Depth Map → Alpha)
                       │
                       └──→ Merge (FG: Graded, BG: Original, EffectMask: Depth Alpha)
```

### Creative Uses
- **Atmospheric Fog:** Grade distant objects (blue, low contrast)
- **Depth of Field:** Blur based on depth (Lens Blur + Depth Map)
- **Selective Grading:** Sky replacement, foreground pop
- **Parallax:** 2.5D camera moves from stills

---

## Performance Optimization

### Proxy Workflow
```
Project Settings → Master Settings → Proxy Resolution: Half/Quarter
                    → Proxy Format: ProRes Proxy / DNxHR LB
Media Pool → Right-click clips → Generate Proxy Media
```

### Fusion Memory Management
| Setting | Location | Recommendation |
|---------|----------|----------------|
| GPU Memory | Preferences → Memory | 80% of VRAM |
| Cache Size | Fusion → Preferences → Global | 4-8 GB RAM |
| Tile Size | Fusion → Preferences → OpenCL | 256×256 (safe), 512×512 (fast) |
| Multi-Frame | Render Settings | Enable for batch |

### Node Graph Hygiene
- **Disable unused nodes** (D key) instead of deleting
- **Group nodes** (Ctrl+G) for organization
- **Publish only needed controls** to modifier panel
- **Use Macro/Template** for repeated setups

---

## Common Fusion Templates (Save as .setting)

### 1. Basic Composite
```
MediaIn → Transform → Merge → MediaOut
             ↑
        MediaIn2 (FG)
```

### 2. Screen Replacement
```
MediaIn (Screen) → PlanarTracker → CornerPin → Merge → MediaOut
                                    ↑
                             MediaIn2 (Replacement)
```

### 3. Beauty Cleanup
```
MediaIn → Paint (Clone) → Paint (Heal) → ColorCorrector → MediaOut
```

### 4. Lower Third Template
```
MediaIn → Text+ (Name) → Text+ (Title) → Merge → Merge → MediaOut
                    ↑              ↑
               Published       Published
```

---

## Skill Trigger Examples

- "How do I use Grid Warp in Fusion?"
- "Remove object with Paint node in DaVinci"
- "Text behind person effect Fusion"
- "Magic Mask tracking not working"
- "Depth map compositing DaVinci Resolve"
- "Fusion node graph best practices"
- "Clone stamp tool Fusion page"
- "Create lower third in Fusion"