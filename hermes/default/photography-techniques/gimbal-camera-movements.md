---
name: gimbal-camera-movements
description: Core gimbal movements for cinematic footage
category: photography
tags: [gimbal, camera-movement, cinematography, stabilization, movement-vocabulary]
difficulty: beginner
---

# Gimbal Camera Movements

Standardized vocabulary and execution for motorized gimbal shots.

## The 7 Core Movements

| Movement | Description | Emotional Effect |
|----------|-------------|------------------|
| **Push In** | Move forward toward subject | Intimacy, focus, revelation |
| **Pull Out** | Move backward from subject | Context, isolation, scale |
| **Truck Left/Right** | Lateral movement, subject centered | Following, parallax, journey |
| **Orbit / Arc** | Circular path around subject | Hero moment, 3D depth, importance |
| **Tilt Up/Down** | Vertical rotation from fixed position | Reveal, scale, verticality |
| **Pan Left/Right** | Horizontal rotation from fixed position | Scanning, connecting spaces |
| **Dutch / Roll** | Rotate horizon line | Disorientation, tension, dream |

## Composite Movements

| Combo | Name | Use Case |
|-------|------|----------|
| Push + Pan | **Drift Pan-Follow** | Architectural walkthrough |
| Orbit + Tilt | **Helix** | Hero product/architecture |
| Truck + Tilt | **Vertical Parallax** | Forest, columns, facades |
| Push + Tilt Down | **Top-Down Reveal** | Floor patterns, tables |

## Execution Parameters

### Speed
| Speed | Feel | When to Use |
|-------|------|-------------|
| **Slow (1-2 ft/s)** | Dreamy, commercial, luxury | Real estate, high-end product |
| **Medium (3-5 ft/s)** | Natural, documentary | Narrative, vlog, B-roll |
| **Fast (6+ ft/s)** | Energy, action, transition | Sports, music video, whip |

### Gimbal Modes
| Mode | Behavior | Best For |
|------|----------|----------|
| **Pan Follow (PF)** | Pan follows, tilt locked | Walking shots, tracking |
| **Lock** | All axes locked | Push/pull, static orbits |
| **Full Follow (FF)** | All axes follow | Handheld feel, run-and-gun |
| **POV / FPV** | All axes + roll follow | Immersive, FPV drone feel |

## DaVinci Resolve Post-Stabilization

**Edit Page → Inspector → Stabilization**:
- **Mode**: Camera Plane (movement preserved) / Perspective (locked)
- **Smoothing**: 25-50 for subtle, 50-75 for locked-off feel
- **Zoom**: Auto-crop edges (check "Zoom" box)

**Fusion → Stabilizer**:
- Planar tracker for complex motion
- Interactive refinement

## Common Mistakes

1. **Micro-jitter**: Walk heel-to-toe, bend knees, "ninja walk"
2. **Horizon drift**: Calibrate before shoot, use horizon lock
3. **Motor noise**: Balance perfectly, don't overload payload
4. **Dead weight**: Counterbalance for front-heavy lenses

## Shot List Template

```
Scene: [Name]
Movement: [Push In / Orbit / etc]
Mode: [PF / Lock / FF]
Speed: [Slow / Med / Fast]
Duration: [Seconds]
Subject: [What's in frame]
Notes: [Gimbal mode, focus method, ND]
```

## Tags
`gimbal` `camera-movement` `cinematography` `stabilization` `movement-vocabulary` `daVinci-resolve` `post-stabilization`