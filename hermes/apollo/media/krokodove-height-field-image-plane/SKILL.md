---
name: krokodove-height-field-image-plane
description: "Extrude 3D from images with Krokodove Height Field."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Extrusion, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Height Field Image Plane Tool

## When to Use

Use when you need to extrude a 2D image plane into 3D geometry using image maps for displacement. Creates actual 3D geometry from 2D images. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:11-8:14
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Height Field Image Plane

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Image Input | Image | Required | Source image for extrusion |
| Extrusion Depth | Float | 1.0 | Maximum extrusion distance |
| Base Thickness | Float | 0.1 | Minimum thickness at zero height |
| Resolution | Integer | 256 | Mesh resolution |
| UV Mapping | Boolean | True | Preserve UV coordinates for texturing |
| Channel | Enum | Luminance | Height data channel |

## Node Graph Setup
```
ImageLoader → HeightFieldImagePlane → Material3D → Merge3D → Renderer3D
```

## Workflow
1. Load source image for extrusion map
2. Add Height Field Image Plane tool
3. Connect image input
4. Set Extrusion Depth for 3D height
5. Adjust Base Thickness for minimum geometry
6. Enable UV Mapping for texture preservation
7. Apply Material3D for shading
8. Render via Renderer3D

## Use Cases
- 3D logo/text extrusion from alpha maps
- Product visualization from packaging art
- Architectural facade extrusion
- Motion graphics 3D elements
- Data-driven 3D infographics
- Photogrammetry-style surfaces

## Tips
- Alpha channel works well for clean edge extrusion
- High Resolution needed for sharp edges
- Combine with Height Field Create 3D for layered effects
- Use Material3D with environment maps for reflections
- Animate Extrusion Depth for build-up animations

## Cross-References
- **Related Skills:** `krokodove-height-field`, `krokodove-s-primitive`, `krokodove-tube-create`
- **Tags:** `krokodove`, `fusion-3d`, `extrusion`, `image-plane`, `v21.1`
- **Collection:** `krokodove-tools`