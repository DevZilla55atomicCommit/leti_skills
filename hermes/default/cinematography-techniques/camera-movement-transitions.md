---
name: camera-movement-transitions
description: In-camera and editorial transitions using camera movement
category: cinematography
tags: [transitions, camera-movement, editing, whip-pan, match-cut]
difficulty: intermediate
---

# Camera Movement Transitions

Transitions achieved through physical camera movement, often enhanced in post.

## Whip Pan / Swish Pan Transition

**Concept**: Fast horizontal pan creates motion blur; cut on the blur to next shot.

**Shooting**:
1. End Shot A with fast pan (90°+ in <0.5s)
2. Start Shot B with matching pan direction/speed
3. Overlap motion blur in edit

**Post (DaVinci Resolve)**:
1. Cut at peak blur
2. Add Motion Blur effect on cut (OpenFX → Motion Blur)
3. Adjust Shutter Angle to 180-360°

## Match Cut / Graphic Match

**Concept**: Match composition, movement, or shape between shots.

**Types**:
- **Shape Match**: Circle → Circle, Doorway → Window
- **Movement Match**: Same camera move direction/speed
- **Color Match**: Dominant color carries across cut

**Post**:
1. Align key frames in timeline
2. Use Dynamic Zoom for subtle reframing
3. Color grade for continuity

## Invisible Cut (Whip + Object Pass)

**Concept**: Foreground object wipes frame, hiding cut.

**Shooting**:
1. Move camera past vertical element (door frame, pillar, person)
2. Match movement in next shot
3. Object must fully cover frame edge

**Post**:
1. Track object edge (Fusion → Tracker)
2. Animate mask to reveal Shot B
3. Add motion blur to mask edge

## Drone Transitions

### Top-Down Reveal
- Start: Nadir (straight down) on detail
- Move: Pull back + rise + tilt up
- End: Wide establishing

### Orbit Transition
- Circle subject at constant radius
- Match orbit direction between locations
- Cut at matching azimuth

## Speed Ramp Transition

**Concept**: Ramp speed to blend shots.

**DaVinci Resolve**:
1. Right-click clip → Retime Curve
2. Add keyframes at transition point
3. Ramp 100% → 300% → 100%
4. Enable Optical Flow for smoothness
5. Add Motion Blur on retime

## Tags
`transitions` `camera-movement` `editing` `whip-pan` `match-cut` `speed-ramp` `drone`