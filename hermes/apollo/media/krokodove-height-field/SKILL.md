---
name: krokodove-height-field
description: "Displace 3D plane from image using Krokodove Height Field."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Displacement, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Height Field Create 3D Tool

## When to Use

Use when you need to displace a 3D plane's geometry based on image luminance/color values. Creates terrain, surfaces, and organic shapes from 2D images. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:05-8:11
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Height Field Create 3D

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Image Input | Image | Required | Source image for displacement |
| Channel | Enum | Luminance | R/G/B/A/Luminance for height data |
| Scale | Float | 1.0 | Vertical displacement multiplier |
| Resolution | Integer | 256 | Plane subdivision resolution |
| Smoothing | Float | 0.0 | Mesh smoothing factor |
| Invert | Boolean | False | Invert height values |

## Node Graph Setup
```
ImageLoader → HeightFieldCreate3D → Displace3D (optional) → Merge3D → Renderer3D
```

## Workflow
1. Load source image (grayscale heightmap works best)
2. Add Height Field Create 3D tool
3. Connect image to tool's image input
4. Select channel (Luminance for grayscale, R/G/B for color channels)
5. Adjust Scale for displacement intensity
6. Increase Resolution for detail (performance cost)
7. Optionally add Displace3D for additional deformation

## Use Cases
- Terrain generation from heightmaps
- Abstract organic surfaces
- Data visualization (3D bar charts from images)
- Displacement mapping for textures
- Motion graphics backgrounds
- Audio visualization (waveform → 3D surface)

## Tips
- Use 16/32-bit EXR heightmaps for precision
- High Resolution + high Scale = heavy geometry (watch GPU memory)
- Combine with Height Field Image Plane for extrusion workflows
- Animate Scale for morphing terrain effects
- Use with 3D Region Toolset to mask displacement areas

## Cross-References
- **Related Skills:** `krokodove-height-field-image-plane`, `krokodove-3d-region`, `krokodove-connect-3d`
- **Tags:** `krokodove`, `fusion-3d`, `height-field`, `displacement`, `v21.1`
- **Collection:** `krokodove-tools`