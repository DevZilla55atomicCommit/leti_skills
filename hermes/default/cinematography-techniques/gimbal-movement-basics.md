---
name: gimbal-movement-basics
description: Core gimbal movement patterns for cinematic camera work
category: cinematography
tags: [gimbal, camera-movement, cinematography, stabilization]
difficulty: beginner
---

# Gimbal Movement Basics

Fundamental gimbal movement patterns used in professional cinematography.

## Core Movement Types

### 1. Drift / Pan Follow
- **Description**: Walk in one direction while panning opposite to keep subject centered
- **Creates**: Parallax depth, professional tracking feel
- **Use case**: Revealing environments, following walking subjects

### 2. Side-to-Side / Pan Follow
- **Description**: Lateral movement while maintaining subject framing
- **Creates**: Smooth lateral tracking, architectural reveals
- **Use case**: Real estate, automotive, establishing shots

### 3. Push In / Pull Out
- **Description**: Move toward/away from subject while adjusting frame
- **Creates**: Emotional emphasis, dramatic reveals
- **Use case**: Character moments, detail reveals

### 4. Orbit / Circular Track
- **Description**: Circle around subject at consistent distance
- **Creates**: 3D spatial awareness, heroic framing
- **Use case**: Hero shots, product reveals, dance/movement

### 5. Low Mode / Ground Level
- **Description**: Inverted gimbal near ground for low-angle tracking
- **Creates**: Unique perspective, scale emphasis
- **Use case**: Sports, automotive, creative transitions

### 6. Crane / Vertical Lift
- **Description**: Smooth vertical movement (requires extension arm or operator movement)
- **Creates**: Scale revelation, transition between levels
- **Use case**: Architecture, landscape, scene transitions

## Stabilization Best Practices

| Setting | Value | Purpose |
|---------|-------|---------|
| Smoothing | 30-50% | Remove micro-jitter |
| Deadband | 1-2° | Ignore tiny corrections |
| Follow Speed | 30-50 | Natural operator feel |
| Motor Power | High | Heavy payload stability |

## Post-Production Stabilization (DaVinci Resolve)

If physical gimbal work needs refinement:

1. **Color Page → Stabilizer**
2. **Mode**: Camera Plane / Perspective
3. **Smoothing**: 40-60
4. **Zoom**: Auto-crop edges

## Common Mistakes to Avoid

- ❌ Walking too fast (creates robotic motion)
- ❌ Over-smoothing (removes natural human feel)
- ❌ Ignoring horizon level (tilted horizons in post)
- ❌ No weight distribution (operator fatigue = shake)

## Tags
`gimbal` `camera-movement` `cinematography` `stabilization` `tracking-shot`