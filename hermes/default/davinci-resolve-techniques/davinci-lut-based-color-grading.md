---
name: davinci-lut-based-color-grading
description: DaVinci Resolve LUT workflows — applying, blending, and managing Look-Up Tables for creative grading, camera log conversion, and film emulation from 7 analyzed Instagram Reel techniques.
category: davinci-resolve
tags: [lut, color-grading, davinci-resolve, look-up-table, film-emulation, log-conversion, creative-lut]
trigger: Use when user wants to apply, create, or manage LUTs in DaVinci Resolve
parameters:
  - name: lut_type
    description: Type of LUT workflow
    type: string
    enum: [creative, technical, film-emulation, log-conversion, hybrid]
    default: creative
  - name: lut_intensity
    description: LUT blend strength (0-100%)
    type: integer
    default: 75
  - name: node_position
    description: Where to place LUT in node graph
    type: string
    enum: [output-node, creative-node, dedicated-lut-node]
    default: output-node
steps:
  - step: Prepare footage with primary correction first
    description: Balance exposure and white balance before LUT
  - step: Add dedicated LUT node at end of chain
    description: Right-click node graph → Add Node → Serial → Label "LUT"
  - step: Apply LUT via LUT browser or CST OFX
    description: Drag .cube/.3dl file to node or use Color Space Transform
  - step: Blend LUT intensity
    description: Use Key Output Gain or Layer Mixer to blend 50-100%
  - step: Fine-tune post-LUT
    description: Add node after LUT for secondary adjustments
---

# DaVinci Resolve LUT-Based Color Grading

**Cluster:** 7 techniques tagged "lut" / "LUT" / "LUT Application"

## Techniques Covered

| Reel | Technique | LUT Type | Key Parameters |
|------|-----------|----------|----------------|
| C93Ef02BTJV | LUT on footage for color grade | Creative | LUT File Path |
| C7xcsf6Iw0m | Match color grade of original via LUT | Creative/Match | LUT intensity |
| C9BB0vtxdWK | Apply LUT for desired look | Creative | Lift Shadows/Highlights |
| C6HzBePg764 | LUT to match colors to standard/style | Technical/Creative | Color balance + saturation pre-LUT |
| C5zHQrqp3Rx | LUT + Grade node for overall tone | Hybrid | LUT + Grade parameters |
| C4q_btGp1yN | LUT application workflow | Creative | Standard LUT workflow |
| C4jZ4etJES2 | Custom LUT input/output | Technical | Custom .cube input/output |

## LUT Workflow Types

### 1. Creative LUT (Output Node)
```
Primary → Creative → LUT (Output)
```
- Apply .cube LUT on final node for "look"
- Blend 50-100% via Key Output Gain
- Best for: Film emulation, stylized looks

### 2. Technical LUT (Camera Log → Rec.709)
```
Primary → CST/LUT → Creative
```
- Convert log footage to display space FIRST
- Then grade in normalized space
- Best for: S-Log3, V-Log, LogC, BRAW

### 3. Hybrid (LUT + Grade)
```
Primary → LUT (50%) → Grade → Output
```
- Partial LUT as base, refine with grading
- Best for: Film print emulation (Kodak 2383, Fuji 3510)

## Step-by-Step: Creative LUT Application

1. **Primary correction first** — Never apply LUT to uncorrected log footage
2. **Add serial node** at end of chain, label "LUT"
3. **Open LUT Browser** (Color page → LUTs panel)
4. **Drag .cube file** onto LUT node
5. **Adjust intensity**: Key Output Gain → 0.75 (75%) for subtle blend
6. **Post-LUT node**: Add node AFTER LUT for highlight rolloff, skin protection

## Step-by-Step: Technical Log Conversion

1. **Node 1**: Primary correction (exposure, WB only — no creative)
2. **Node 2**: Color Space Transform OFX
   - Input Color Space: Camera (S-Log3/S-Gamut3, V-Log/V-Gamut, etc.)
   - Output Color Space: Rec.709 Gamma 2.4
3. **Node 3+**: Creative grading in display-referred space

## LUT Management Tips

| Task | Method |
|------|--------|
| Organize LUTs | Create folders in LUT Browser: /Creative, /Technical, /Film |
| Preview LUT | Hover in LUT Browser — shows thumbnail on selected clip |
| Batch apply | Gallery → Grab Still → Right-click → Apply LUT to selected clips |
| Export grade as LUT | Right-click node → Generate 3D LUT (.cube) |
| Protect skin tones | Qualifier on post-LUT node → isolate skin → reduce saturation |

## Parameters from Reels

- **C93Ef02BTJV**: `"LUT File Path": "path/to/lut.cube"` — Apply LUT to footage
- **C6HzBePg764**: `"Adjusting color balance and saturation... BEFORE applying LUT"` — Pre-LUT prep critical
- **C5zHQrqp3Rx**: `"LUT for color grading", "Grade to adjust overall tone"` — Hybrid approach
- **C4jZ4etJES2**: `"input_lut": "custom_lut.cube", "output_lut": "custom_lut.cube"` — Round-trip LUT

## Common LUT Packs Referenced

- Kodak 2383 / Fujifilm 3510 (film print emulation)
- ARRI LogC → Rec.709 (technical)
- Sony S-Log3 → Rec.709 (technical)
- Creative: "Teal Orange", "Cinematic", "Bleach Bypass", "Vintage"

## Related Skills

- `davinci-color-correction-grading-fundamentals` — Primary/creative node structure
- `davinci-color-management-cst` — Color Space Transform deep dive
- `davinci-film-emulation-workflows` — Film print emulation with LUTs + grain