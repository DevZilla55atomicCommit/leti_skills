---
name: krokodove-tube-create
description: "Create 3D tubes along paths with Krokodove Tube Create."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Tube, Path, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Tube Create 3D Tool

## When to Use

Use when you need to create tubular/pipe 3D geometry that follows a custom path. Ideal for motion graphics, data flows, organic structures, and technical visualization. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:15-8:19
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Tube Create 3D

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Path | Curve/Spline | Required | Centerline path for tube |
| Radius | Float | 0.5 | Tube radius |
| Segments | Integer | 16 | Radial subdivision count |
| Path Resolution | Integer | 64 | Longitudinal subdivision count |
| Radius Profile | Curve | Constant | Radius variation along path |
| Cap Ends | Boolean | True | Close tube ends |
| Twist | Float | 0.0 | Rotation along path |

## Node Graph Setup
```
PathTool → TubeCreate3D → Material3D → Merge3D → Renderer3D
```

## Workflow
1. Create or import a path/spline (Path tool, SVG import, or animated curve)
2. Add Tube Create 3D tool
3. Connect path to tool
4. Set Radius and Segments
5. Adjust Path Resolution for smooth curves
6. Use Radius Profile for variable thickness
7. Enable/Disable Cap Ends as needed
8. Apply Material3D for shading

## Use Cases
- Data flow visualization (tubes connecting nodes)
- Organic structures (vines, vessels, neurons)
- Motion graphics transitions
- Technical/medical animation
- Pipeline/cable routing visualization
- Abstract art installations

## Tips
- Animate Radius Profile for pulsing/growing effects
- Combine with Connect 3D for network diagrams
- Use Path Resolution ≥ 128 for tight curves
- Animate Twist for DNA helix effects
- Low Segments (6-8) = angular/faceted look
- Publish Radius for expression-driven animation

## Cross-References
- **Related Skills:** `krokodove-connect-3d`, `krokodove-3d-region`, `krokodove-s-primitive`
- **Tags:** `krokodove`, `fusion-3d`, `tube`, `path`, `spline`, `v21.1`
- **Collection:** `krokodove-tools`