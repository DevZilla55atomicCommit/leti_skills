---
name: krokodove-3d-region
description: "Define 3D regions for effects with Krokodove 3D Region."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, 3D, Region, Masking, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove 3D Region Toolset

## When to Use

Use when you need to define spatial regions in 3D space to isolate effects, constrain tools, or create volumetric masks. Works with Objectify 3D and other Krokodove tools. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:20-8:29
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → 3D Region Toolset

## Region Types
| Region Type | Parameters | Use Case |
|-------------|------------|----------|
| Box | Center, Size (XYZ) | Cuboid volumes, room bounds |
| Sphere | Center, Radius | Spherical influence, planet atmospheres |
| Cylinder | Center, Radius, Height | Columnar zones, tunnels |
| Custom | Mesh input | Complex shapes from geometry |

## Parameters (Common)
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Region Type | Enum | Box | Shape of 3D region |
| Center | 3D Point | (0,0,0) | Region center position |
| Size/Radius | Float/Vector | 1.0 | Region dimensions |
| Falloff | Float | 0.0 | Soft edge transition |
| Invert | Boolean | False | Invert region (outside affected) |
| Transform | Matrix | Identity | Full 3D transform |

## Node Graph Setup
```
3DRegionToolset → Objectify3D (or other tools)
         ↓
    EffectTool (masked by region)
```

## Workflow
1. Add 3D Region Toolset
2. Select Region Type (Box/Sphere/Cylinder/Custom)
3. Position and scale in 3D space
4. Adjust Falloff for soft edges
5. Connect to Objectify 3D or other tools that accept region input
6. Tools inside region apply effect; outside = no effect

## Use Cases
- Localized fog/atmosphere in 3D scenes
- Selective particle emission zones
- Volumetric lighting bounds
- Effect constraints for performance
- 3D vignetting
- Spatial audio visualization zones
- Transition wipes in 3D space

## Tips
- Multiple regions can be combined (union/intersect/subtract)
- Animate region transforms for moving effect zones
- Use with Height Field tools to constrain displacement
- Falloff > 0 creates feathered boundaries
- Custom region type accepts any 3D mesh
- Publish region parameters for expression control

## Cross-References
- **Related Skills:** `krokodove-objectify-3d`, `krokodove-height-field`, `krokodove-connect-3d`
- **Tags:** `krokodove`, `fusion-3d`, `region`, `masking`, `volumetric`, `v21.1`
- **Collection:** `krokodove-tools`