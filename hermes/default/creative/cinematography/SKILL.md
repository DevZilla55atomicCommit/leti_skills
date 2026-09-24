---
name: cinematography
description: Use for camera movement, gimbal, stabilization, transitions.
category: creative
tags: [cinematography, camera-movement, gimbal, stabilization, transitions, production]
---

# Cinematography Techniques

Class-level umbrella for cinematography skills covering camera movement vocabulary, gimbal operation, stabilization (physical + digital), transition design, and on-set production workflows applicable to both production and DaVinci Resolve post-production.

## Sub-Domains

| Domain | Description | Key References |
|--------|-------------|----------------|
| **Camera Movement** | 7 core movements, composite moves, execution parameters | `references/gimbal-movement-basics.md` |
| **Gimbal Operation** | Modes, balancing, walking technique, common mistakes | `references/gimbal-camera-movements.md` |
| **Stabilization** | Physical gimbal + Resolve post-stabilization | `references/gimbal-camera-movements.md`, `references/gimbal-movement-basics.md` |
| **Transitions** | Whip pan, match cut, invisible cut, drone transitions | `references/camera-movement-transitions.md` |
| **Production** | Shot listing, movement vocabulary, on-set workflow | `references/gimbal-movement-basics.md` |

## Movement Vocabulary (Standardized)

| Movement | Description | Emotional Effect | Resolve Post |
|----------|-------------|------------------|--------------|
| **Push In** | Move toward subject | Intimacy, focus, revelation | Stabilize if handheld |
| **Pull Out** | Move away from subject | Context, isolation, scale | Stabilize if handheld |
| **Truck L/R** | Lateral move, subject centered | Following, parallax, journey | Stabilize horizontal |
| **Orbit/Arc** | Circular path around subject | Hero moment, 3D depth, importance | Planar track if needed |
| **Tilt Up/Down** | Vertical rotation from fixed pos | Reveal, scale, verticality | Rarely needed |
| **Pan L/R** | Horizontal rotation from fixed pos | Scanning, connecting spaces | Rarely needed |
| **Dutch/Roll** | Horizon rotation | Disorientation, tension, dream | Avoid in post |

## Composite Movements

| Combo | Name | Use Case |
|-------|------|----------|
| Push + Pan | **Drift Pan-Follow** | Architectural walkthrough |
| Orbit + Tilt | **Helix** | Hero product/architecture |
| Truck + Tilt | **Vertical Parallax** | Forest, columns, facades |
| Push + Tilt Down | **Top-Down Reveal** | Floor patterns, tables |

## Stabilization Workflow

### Physical (On-Set)
1. **Balance perfectly** — No motor strain, silent operation
2. **Walk heel-to-toe** — Bent knees, "ninja walk" for micro-jitter
3. **Use modes correctly** — PF for tracking, Lock for push/pull, FF for run-and-gun
4. **Horizon calibration** — Before every take, auto-level in app

### Digital (DaVinci Resolve Color Page)
```
Inspector → Stabilizer
Mode: Camera Plane (preserves intent) / Perspective (locks frame)
Smoothing: 25-50 subtle, 50-75 locked-off feel
Zoom: Auto-crop edges (check "Zoom")
```

### When to Use Which
| Situation | Physical | Digital |
|-----------|----------|---------|
| Planned movement | ✅ Primary | Minor cleanup |
| Run-and-gun | ✅ Best effort | ✅ Essential |
| Locked-off needed | ❌ Impossible | ✅ Camera Lock mode |
| Extreme shake | ❌ Overload | ⚠️ Limited (crop loss) |

## Transition Design

### Whip Pan / Swish Pan
- **Shoot**: End A with fast pan (90°+ in <0.5s), Start B with matching pan
- **Edit**: Cut at peak blur, add Motion Blur OFX (Shutter Angle 180-360°)

### Match Cut
- **Shape/Color/Movement** continuity across cut
- **Resolve**: Dynamic Zoom for subtle reframe alignment

### Invisible Cut (Object Wipe)
- **Shoot**: Foreground object crosses full frame width
- **Fusion**: Track object edge → Animate Polygon mask → Reveal Shot B

### Drone Transitions
- **Top-Down Reveal**: Nadir → Pull back + Tilt up
- **Orbit Transition**: Match orbit direction/speed between locations
- **Speed Ramp**: Retime Curve + Optical Flow between locations

## DaVinci Resolve Integration

### Edit Page
- **Dynamic Zoom** for push/pull without quality loss
- **Retime Curve** for speed ramps (Bezier easing)
- **Crop/Transform** keyframes for simulated movement

### Color Page
- **Stabilizer** as primary cleanup tool
- **Tracker** for Power Window following movement

### Fusion Page
- **Planar Tracker** for screen replacements, signage
- **CameraTracker** for 3D text integration into move
- **Polygon Mask** animation for architectural wipe transitions

## Key References

- `references/gimbal-movement-basics.md` — 7 core movements, stabilization best practices, Resolve post workflow
- `references/camera-movement-transitions.md` — Whip pan, match cut, invisible cut, drone transitions, speed ramp
- `references/gimbal-camera-movements.md` — 7 core movements, composite moves, execution parameters, common mistakes

## Common Mistakes to Avoid

1. **Over-smoothing** — Removes human feel, looks robotic (Smoothing >75)
2. **Ignoring horizon** — Tilted horizon = amateur; calibrate every setup
3. **Wrong mode** — PF for orbit (causes drift), Lock for tracking (fights operator)
4. **No weight distro** — Counterbalance for front-heavy lenses
5. **Cutting movement** — Cut ON movement, not static frames

## Related Skills

- `photography` — Lens theory, lighting, color grading, compositing
- `camera-hardware` — Sensor formats, codecs, log profiles, media management
- `davinci-resolve` — Color grading, Fusion masking, stabilization tools

## Session Context (2026-07-29)

Created from Instagram→DaVinci pipeline where gimbal tutorials, stabilization demos, and transition breakdowns needed structured categorization. NVIDIA API is the only reliable vision path; local Ollama crashes on M4 16GB under concurrent load.