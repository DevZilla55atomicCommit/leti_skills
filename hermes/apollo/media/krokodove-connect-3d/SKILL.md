---
name: krokodove-connect-3d
description: "Create 3D vertex connections with Krokodove Connect 3D tool."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Connect 3D Tool

## When to Use

Use when you need to create straight line connections between vertices/points in a 3D scene. New in DaVinci Resolve 21.1 under Fusion Effects → Krokodove category.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 7:58-8:04
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Connect 3D

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Start Vertex | 3D Point | (0,0,0) | Starting vertex coordinate |
| End Vertex | 3D Point | (1,1,1) | Ending vertex coordinate |
| Thickness | Float | 0.1 | Connection line thickness |
| Subdivisions | Integer | 10 | Number of segments for curved paths |
| Color | Color | White | Connection color |
| Opacity | Float | 1.0 | Connection opacity |

## Node Graph Setup
```
Connect3D → Merge3D → Renderer3D → Composite
```

## Workflow
1. Add Connect 3D tool from Krokodove category
2. Define start/end vertices (can link to other 3D tools' outputs)
3. Adjust thickness and subdivisions
4. Connect to Merge3D for scene integration
5. Render via Renderer3D

## Use Cases
- Wireframe visualizations
- Data connection diagrams
- 3D graph/network representations
- Technical illustrations
- Motion graphics connections

## Tips
- Animate vertices using Publish/Expressions for dynamic connections
- Combine with Height Field Create 3D for terrain wireframes
- Use with 3D Region Toolset to constrain connection areas
- Low subdivisions = straight lines, high = smooth curves

## Cross-References
- **Related Skills:** `krokodove-height-field`, `krokodove-3d-region`, `krokodove-objectify-3d`
- **Tags:** `krokodove`, `fusion-3d`, `connect-3d`, `v21.1`
- **Collection:** `krokodove-tools`