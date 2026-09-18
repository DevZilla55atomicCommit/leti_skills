---
name: krokodove-objectify-3d
description: "Instance objects in 3D regions with Krokodove Objectify 3D."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Instancing, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Objectify 3D Tool

## When to Use

Use when you need to convert 3D regions into instanced objects with individual properties. Connects to 3D Region Toolset for procedural object placement. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:25-8:32
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Objectify 3D

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Region Input | 3D Region | Required | Source region from 3D Region Toolset |
| Object Type | Enum | Cube | Cube/Sphere/Cylinder/Custom Mesh |
| Instance Count | Integer | 10 | Number of instances |
| Distribution | Enum | Random | Random/Grid/Linear/Surface |
| Scale Variance | Float | 0.0 | Random scale variation (0-1) |
| Rotation Variance | Float | 0.0 | Random rotation variation |
| Material Variance | Float | 0.0 | Material variation per instance |
| Seed | Integer | 0 | Random seed for reproducibility |

## Node Graph Setup
```
3DRegionToolset → Objectify3D → Merge3D → Renderer3D
```

## Workflow
1. Create 3D Region Toolset defining the volume
2. Add Objectify 3D tool
3. Connect Region Input from 3D Region Toolset
4. Select Object Type (or Custom Mesh)
5. Set Instance Count
6. Choose Distribution mode
7. Adjust Variance parameters for natural variation
8. Connect to Merge3D for scene integration

## Distribution Modes
| Mode | Description |
|------|-------------|
| Random | Uniform random within region |
| Grid | Regular 3D grid pattern |
| Linear | Along a line/curve |
| Surface | On region boundary surface |

## Use Cases
- Procedural scattering (rocks, trees, debris)
- Particle-like object clouds
- Architectural element arrays
- Motion graphics replicators
- Data point visualization
- Crowd/flock base geometry

## Tips
- Use Custom Mesh for complex instanced objects
- Combine with Height Field for terrain-aware scattering
- Animate Instance Count for build-up effects
- Seed ensures reproducible layouts across renders
- Material Variance + Material3D = varied appearances
- Low Instance Count + high Scale Variance = hero objects

## Cross-References
- **Related Skills:** `krokodove-3d-region`, `krokodove-height-field`, `krokodove-tube-create`
- **Tags:** `krokodove`, `fusion-3d`, `instancing`, `objectify`, `procedural`, `v21.1`
- **Collection:** `krokodove-tools`