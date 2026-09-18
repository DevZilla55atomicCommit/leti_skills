---
name: davinci-lut-application-workflow
description: DaVinci Resolve LUT application workflow — importing LUTs, applying via nodes, LUT management, creative LUT vs technical LUT, and LUT stacking techniques from 7 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [lut, look-up-table, color-grading, davinci-resolve, lut-management, creative-lut, technical-lut]
trigger: Use when user wants to apply, manage, or create LUT workflows in DaVinci Resolve
parameters:
  - name: lut_type
    description: Type of LUT to apply
    type: string
    enum: [technical, creative, film-emulation, camera-specific, custom]
    default: creative
  - name: application_method
    description: How to apply LUT
    type: string
    enum: [node, clip-lut, timeline-lut, output-lut, group-pre-lut]
    default: node
  - name: intensity
    description: LUT intensity (0-1, applied via Key Output Gain)
    type: number
    default: 1.0
steps:
  - step: Install LUT in Resolve LUT folder
    description: Project Settings → Color → Lookup Tables → Open LUT Folder → copy .cube files
  - step: Refresh LUTs
    description: Project Settings → Color → Refresh LUT Lists
  - step: Apply LUT via Node
    description: Color page → Right-click node → 3D LUT → Select LUT
  - step: Adjust intensity
    description: Key Output Gain on node with LUT (0.5 = 50% intensity)
  - step: Stack LUTs if needed
    description: Multiple serial nodes each with different LUT
---

# DaVinci Resolve LUT Application Workflow

**Cluster:** 7 techniques tagged "LUT", "LUT Application", "Look-Up Table"

## Techniques Covered

| Reel | Technique | LUT Usage |
|------|-----------|-----------|
| DAGr5n-If-O | Color Correction + LUT Application | LUT on Node 2 |
| C93Ef02BTJV | Color Correction + Grading and LUT | LUT on Node 1 |
| C913vb9PoeI | Color Correction + LUT | LUT for color grade |
| C7xcsf6Iw0m | Apply LUT to match color grade | LUT matching |
| C9BB0vtxdWK | Color Correction + LUT | LUT for desired look |
| C6HzBePg764 | Color Correction + LUT | LUT to match standard/style |
| C4jZ4etJES2 | Color Correction + LUT | Custom LUT input/output |

## LUT Types & When to Use

| Type | Purpose | Examples | Node Position |
|------|---------|----------|---------------|
| **Technical** | Log → Rec.709, Camera → Output | DJI D-Log → Rec.709, Sony S-Log3 → Rec.709 | Node 1 (First) |
| **Creative** | Artistic look, film emulation | Kodak 2383, Fuji 3510, Teal-Orange | Node 2-3 (After primary) |
| **Camera-Specific** | Manufacturer "look" | ARRI Alexa Classic, RED IPP2, Canon C-Log | Node 1 or 2 |
| **Output** | Delivery transform | Rec.709 → P3, HDR PQ, HLG | Last Node (Output) |
| **Utility** | Exposure assist, false color | Exposure check, skin tone line | Temporary/Parallel |

## Installing LUTs in DaVinci Resolve

### Method 1: Project-Specific (Recommended for Teams)
```
Project Settings (Cmd+,) → Color → Lookup Tables
  → "Open LUT Folder" (per project)
  → Create subfolders: /Technical, /Creative, /Film, /Camera
  → Copy .cube/.3dl files
  → Click "Update Lists" or restart Resolve
```

### Method 2: System-Wide (All Projects)
```
macOS: ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/
Windows: %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\LUT\
Linux: ~/.local/share/DaVinciResolve/LUT/
```

### Method 3: Project-Level via Media Pool
```
Media Pool → Right-click → "Import LUT" (Resolve 18.5+)
  → Select .cube files
  → Auto-places in project LUT folder
```

## Applying LUTs: 4 Methods

### Method A: Node LUT (Most Common, Flexible)
```
Color Page → Node Graph
  1. Add Serial Node (Opt+S / Alt+S)
  2. Right-click node → 3D LUT → Select LUT
  3. Adjust: Key Output Gain (Inspector) for intensity
```
**Pros**: Per-clip control, stackable, keyframeable, blend modes
**Cons**: Must apply per clip

### Method B: Clip LUT (Media Pool)
```
Media Pool → Right-click clip → "Clip LUT" → Select LUT
```
**Pros**: Applies to all instances of clip
**Cons**: Not keyframeable, hidden from node graph

### Method C: Timeline LUT (Project Settings)
```
Project Settings → Color → Timeline LUT
  → Set Input/Output LUT for entire timeline
```
**Pros**: Global, good for dailies/uniform footage
**Cons**: Affects everything, less control

### Method D: Group Pre/Post LUT (Color Groups)
```
Color Page → Color Groups (top-right)
  → Create Group → Assign clips
  → Group Pre-LUT: Before node graph
  → Group Post-LUT: After node graph
```
**Pros**: Batch apply to scene/location
**Cons**: Requires Color Group setup

## LUT Stacking Techniques

### Stack 1: Technical + Creative
```
Node 1: Technical LUT (Log → Rec.709)
Node 2: Creative LUT (Film look)
Node 3: Key Output Gain 0.7 (reduce creative intensity)
Node 4: Primary correction (tweak after LUT)
```

### Stack 2: Camera LUT + Creative + Output
```
Node 1: Camera LUT (S-Log3 → Alexa LogC)
Node 2: Creative LUT (Kodak 2383)
Node 3: Output LUT (Rec.709 → P3 for cinema)
```

### Stack 3: Split Toning via LUTs
```
Node 1: Technical LUT
Node 2: Shadows LUT (teal lift) — Qualifier: shadows only
Node 3: Highlights LUT (warm push) — Qualifier: highlights only
Node 4: Blend via Layer Mixer (Composite Mode: Overlay/Soft Light)
```

## LUT Intensity Control

| Method | How | Use Case |
|--------|-----|----------|
| **Key Output Gain** | Inspector → Key Output Gain (0-1) | Quick blend |
| **Layer Mixer** | Layer Mixer node → Blend modes | Advanced blending |
| **Parallel Node** | Parallel mixer → LUT on one branch | Selective opacity |
| **Keyframe Gain** | Keyframe Key Output Gain over time | Dynamic intensity |

**Pro Tip (C7xcsf6Iw0m)**: "Apply LUT to match color grade of original" — Use Key Output Gain to dial in match percentage.

## LUT Management Best Practices

### Naming Convention
```
[Type]_[Camera/Source]_[Target]_[Look].cube
Examples:
  TECH_DJI_DLog_Rec709.cube
  CREATIVE_Kodak2383_Rec709_Film.cube
  CAMERA_Sony_SLog3_AlexaLogC.cube
  OUTPUT_Rec709_P3D65.cube
```

### Folder Structure
```
LUTs/
├── Technical/
│   ├── Camera/
│   │   ├── DJI/
│   │   ├── Sony/
│   │   └── Canon/
│   └── Output/
│       ├── Rec709_to_P3.cube
│       └── Rec709_to_HLG.cube
├── Creative/
│   ├── Film_Emulation/
│   ├── Teal_Orange/
│   ├── Vintage/
│   └── Mood/
└── Utility/
    ├── False_Color.cube
    └── Skin_Tone_Line.cube
```

### Version Control
- Keep `.cube` files in Git with project
- Document LUT source (URL, creator, date)
- Note intended input color space

## Common LUT Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Over-saturated/blown out** | LUT expects different input | Check input color space matches LUT design |
| **Green/magenta shift** | Wrong gamma in/out | Verify Input/Output Gamma in CST or LUT metadata |
| **Crushed shadows** | LUT designed for higher DR | Reduce Key Output Gain, lift shadows before LUT |
| **Band artifacts** | 8-bit LUT on 10-bit footage | Use 33-point or 65-point LUT, or CST instead |
| **LUT not showing** | Wrong folder / not refreshed | Project Settings → Color → Update Lists |

## LUT vs CST (Color Space Transform)

| Aspect | LUT | CST |
|--------|-----|-----|
| Precision | Fixed grid (17³-65³ points) | Math-per-pixel (infinite) |
| Flexibility | Fixed transform | Adjustable parameters |
| Performance | Fast (GPU texture) | Fast (GPU compute) |
| Gamut Mapping | Baked in | Selectable (clip/compress) |
| Best For | Creative looks, film emulation | Technical conversions, HDR |

**Rule**: Use CST for log→linear/Rec.709. Use LUT for creative looks.

## Pro Tips from Reels

- **C93Ef02BTJV**: "Apply LUT to footage for color correction" — LUT as grade starter
- **C913vb9PoeI**: "Apply LUT for desired color grade" — Creative intent
- **C7xcsf6Iw0m**: "Apply LUT to match color grade of original" — Matching workflow
- **C9BB0vtxdWK**: "Apply LUT to achieve desired look" — Look development
- **C6HzBePg764**: "LUT to match colors to specific standard/style" — Standardization
- **C4jZ4etJES2**: Custom input/output LUT paths — Pipeline integration

## Creating Custom LUTs in Resolve

```
1. Grade clip to desired look
2. Right-click clip → "Generate 3D LUT"
3. Choose: 33-point (standard) or 65-point (high precision)
4. Save to project LUT folder
5. Name: CUSTOM_[Project]_[Look]_[Date].cube
```

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Node structure for LUTs
- `davinci-color-management-cst` — Technical color transforms
- `davinci-film-emulation-luts` — Film look LUTs deep dive
- `davinci-hdr-grading-workflow` — Output LUTs for HDR