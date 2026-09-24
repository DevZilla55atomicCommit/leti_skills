---
name: krokodove-s-primitive
description: "Create basic 3D primitive shapes with Krokodove S Primitive."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Primitives, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove S Primitive Create Tool

## When to Use

Use when you need to create basic 3D primitive shapes (cross, polygon, rectangle, star) for motion graphics and 3D design. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:33-8:42
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → S Primitive Create

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Shape Type | Enum | Cross | Cross/Polygon/Rectangle/Star |
| Size | Float | 1.0 | Overall shape size |
| Sides | Integer | 5 | Polygon sides (for Polygon/Star) |
| Inner Radius | Float | 0.5 | Star inner radius ratio |
| Thickness | Float | 0.1 | Shape thickness/extrusion |
| Roundness | Float | 0.0 | Corner rounding |

## Node Graph Setup
```
SPrimitiveCreate → Material3D → Merge3D → Renderer3D
```

## Workflow
1. Add S Primitive Create tool
2. Select Shape Type
3. Adjust Size and shape-specific parameters
4. Set Thickness for 3D extrusion
5. Apply Material3D for shading
6. Render via Renderer3D

## Shape Details
| Shape | Key Parameters |
|-------|----------------|
| Cross | Size, Thickness |
| Polygon | Size, Sides (3+), Roundness |
| Rectangle | Size (X/Y), Roundness |
| Star | Size, Sides, Inner Radius |

## Use Cases
- Motion graphics elements
- UI/UX 3D icons
- Data visualization markers
- Technical diagram symbols
- Particle system sprites
- Logo mark creation

## Tips
- Animate Sides for polygon morphing
- Star Inner Radius 0.0 = solid, 0.5+ = hollow
- Combine with Tube Create for complex shapes
- Low Thickness = flat 2D-like, High = 3D blocks
- Publish parameters for expression animation

## Cross-References
- **Related Skills:** `krokodove-tube-create`, `krokodove-height-field-image-plane`, `krokodove-edge-manipulation`
- **Tags:** `krokodove`, `fusion-3d`, `primitives`, `shapes`, `v21.1`
- **Collection:** `krokodove-tools`