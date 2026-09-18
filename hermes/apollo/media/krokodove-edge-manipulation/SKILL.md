---
name: krokodove-edge-manipulation
description: "Advanced edge ops for 3D shapes with Krokodove Edge Tools."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Edges, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Advanced Edge Manipulation Tools

## When to Use

Use when you need sophisticated edge operations on 3D shapes (bevel, chamfer, offset, subdivision) for motion graphics and design workflows. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:43-8:51
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Edge Manipulation (multiple tools)

## Edge Operations
| Operation | Parameters | Effect |
|-----------|------------|--------|
| Bevel | Width, Segments, Profile | Rounded edges |
| Chamfer | Width, Angle | Angled edge cuts |
| Offset | Distance, Direction | Parallel edge expansion |
| Subdivide | Levels, Smoothness | Mesh refinement |
| Extrude Edge | Distance, Direction | Edge-based extrusion |
| Loop Cut | Count, Position | Edge loop insertion |

## Node Graph Setup
```
ShapeTool → EdgeManipulation → Material3D → Merge3D → Renderer3D
```

## Workflow
1. Create base shape (S Primitive, imported mesh, etc.)
2. Add desired Edge Manipulation tool
3. Select edges (or use auto-selection)
4. Adjust operation parameters
5. Chain multiple edge ops for complex results
6. Apply Material3D

## Use Cases
- Hard-surface modeling
- Motion graphics bevels
- Architectural detail edges
- Product design chamfers
- Game asset optimization
- Technical illustration outlines

## Tips
- Bevel + Subdivide = smooth organic edges
- Chamfer low Segments = faceted tech look
- Offset negative = inset, positive = outset
- Combine with S Primitive for parametric designs
- Animate Bevel Width for build animations

## Cross-References
- **Related Skills:** `krokodove-s-primitive`, `krokodove-height-field`, `krokodove-tube-create`
- **Tags:** `krokodove`, `fusion-3d`, `edges`, `bevel`, `chamfer`, `v21.1`
- **Collection:** `krokodove-tools`