---
name: davinci-resolve-transitions-effects
description: Transition effects and creative video effects in DaVinci Resolve (Edit page transitions, Fusion composites, OFX plugins). Use for smooth cuts, creative transitions, motion effects, and visual storytelling.
trigger: User wants to add transitions, creative effects, or composite elements in DaVinci Resolve.
category: davinci-resolve
tags:
  - transitions
  - video editing
  - effects
  - fusion
  - davinci resolve
  - edit page
  - creative
steps:
  - name: edit-page-transitions
    description: Apply and customize built-in transitions on Edit page
    parameters:
      - name: transition_type
        type: string
        enum: ["Cross Dissolve", "Dip to Color", "Push", "Slide", "Wipe", "Iris", "Shape"]
        default: "Cross Dissolve"
      - name: duration
        type: string
        default: "15-30 frames"
        description: Transition length in frames
      - name: alignment
        type: string
        enum: ["Center at Cut", "Start at Cut", "End at Cut"]
        default: "Center at Cut"
      - name: easing
        type: string
        enum: ["Linear", "Ease In", "Ease Out", "Ease In Out"]
        default: "Ease In Out"
    difficulty: beginner
  - name: fusion-custom-transitions
    description: Build custom transitions in Fusion page (dissolve, push, morph, displacement)
    parameters:
      - name: transition_style
        type: string
        enum: ["Dissolve", "Push/Wipe", "Morph", "Displacement", "Glitch", "Light Leak"]
        default: "Dissolve"
      - name: duration_frames
        type: integer
        default: 30
      - name: use_masks
        type: boolean
        default: true
        description: Use animated masks for shaped transitions
    difficulty: intermediate
  - name: speed-ramp-transitions
    description: Speed ramp transitions (time remapping) for dynamic pacing
    parameters:
      - name: retime_curve
        type: string
        default: "Retime Curve editor (Ctrl+R)"
      - name: optical_flow
        type: boolean
        default: true
      - name: transition_type
        type: string
        enum: ["Slow→Fast", "Fast→Slow", "Freeze→Motion", "Reverse"]
        default: "Slow→Fast"
    difficulty: intermediate
  - name: creative-video-effects
    description: OFX and built-in creative effects (Glow, Film Grain, Halation, Lens Flare, Edge Detect)
    parameters:
      - name: effect_type
        type: string
        enum: ["Glow", "Film Grain", "Halation", "Lens Flare", "Edge Detect", "Chromatic Aberration", "Vignette"]
        default: "Glow"
      - name: blend_mode
        type: string
        enum: ["Add", "Screen", "Overlay", "Soft Light"]
        default: "Screen"
      - name: intensity
        type: string
        default: "Low-Medium"
    difficulty: intermediate
parameters:
  - name: resolve_page
    type: string
    default: "Edit|Fusion|Color"
    description: Edit for built-in transitions, Fusion for custom, Color for grading transitions
  - name: node_graph_type
    type: string
    default: "serial"
---

# DaVinci Resolve Transitions & Creative Effects

Complete guide to transitions and creative video effects in DaVinci Resolve: built-in Edit page transitions, custom Fusion transitions, speed-ramp transitions, and OFX creative effects.

## Video References

| Technique | Video ID | Key Nodes/Tools | Tags |
|-----------|----------|-----------------|------|
| Instagram Reel Transition Effect | Cz02iyXrjan | node1, node2 | transitions, color correction, grading |
| Speed Hump Tutorial | C6rpIhKLk5V | node1, node2 | tutorial, speed hump, video editing |
| Instagram Reel Ct3ex_fLyZA | Ct3ex_fLyZA | node1, node2 | video editing, instagram reel |

## Core Workflows

### 1. Edit Page Built-in Transitions (Fastest)
**Reference**: Cz02iyXrjan (Transition Effect)

```
Edit Page → Effects Library → Toolbox → Video Transitions
├── Dissolve
│   ├── Cross Dissolve (standard)
│   ├── Film Dissolve (color-aware)
│   └── Smooth Cut (morph, Studio only)
├── Iris / Shape
│   ├── Circle, Square, Star, Heart
│   └── Custom (svg mask)
├── Motion
│   ├── Push (directional)
│   ├── Slide (overlap)
│   └── Split (two-way)
├── Wipe
│   ├── Linear, Clock, Barn Door
│   └── Gradient (custom grayscale map)
└── Stylize
    ├── Glitch, Light Leaks, Film Damage (Studio)
```

**Applying Transitions**:
1. Open Effects Library → Video Transitions
2. Drag transition between two clips on timeline
3. Double-click transition → Inspector for settings
4. Adjust **Duration** (frames), **Alignment**, **Easing**

**Transition Settings (Inspector)**:
| Parameter | Options | Default | Notes |
|-----------|---------|---------|-------|
| Duration | Frames (1-120+) | 24 | Even numbers for smoothness |
| Alignment | Center/Start/End at Cut | Center | Center = symmetric |
| Easing | Linear/Ease In/Out/Ease In Out | Ease In Out | Ease In Out = natural |
| Border | Width/Color/Opacity | None | For wipe/push transitions |
| Reverse | On/Off | Off | Reverse direction |

**Pro Tips**:
- **Ripple Trim**: Hold Option (Alt) while dragging transition edge to ripple
- **Apply to Multiple**: Select multiple cuts → Right-click → Add Transition
- **Default Transition**: Right-click any transition → "Set as Default"

### 2. Custom Fusion Transitions (Advanced)
**For unique, branded, or complex transitions**

```
Fusion Page Composition:
├── MediaIn1 (Clip A - outgoing)
├── MediaIn2 (Clip B - incoming)
├── Dissolve/Merge Tool
│   ├── Blend: Dissolve / Add / Screen / Custom expression
│   └── Alpha: Animated mask (0→1)
├── Optional: Displace Tool
│   ├── X/Y Channel: Gradient or noise
│   └── Amount: Animated 0→50→0
├── Optional: Transform Tools
│   ├── MediaIn1: Scale/Position animate out
│   └── MediaIn2: Scale/Position animate in
└── MediaOut
```

**Common Fusion Transition Types**:

| Type | Key Tools | Description |
|------|-----------|-------------|
| Morph Dissolve | Dissolve + Optical Flow | Smooth morph between similar frames |
| Push/Wipe | Transform + Merge | Clip pushes next clip on/off screen |
| Displacement | Displace + Gradient | Organic liquid/distortion transition |
| Glitch | Noise + RGB Offset + Scanlines | Digital glitch aesthetic |
| Light Leak | Add Merge + Gradient + Blur | Film-style light leak burn |
| Shape Reveal | Polygon/BSpline Mask + Merge | Custom shape wipe |

**Saving as Template**:
1. Build in Fusion page
2. Right-click MediaOut → "Create Macro" or save as .setting
3. Use in Edit page: Right-click cut → "Fusion Transition" → Select macro

### 3. Speed Ramp Transitions (Time Remapping)
**Reference**: C6rpIhKLk5V (Speed Hump Tutorial)

```
Edit Page:
├── Two clips on timeline (or single clip with cut)
├── Blade cut at transition point
├── Select both clips (or sections)
├── Right-click → Retime Controls (Ctrl+R)
├── Retime Curve Editor (curve icon)
│   ├── Clip A end: 100% → 50% → 0% (freeze)
│   ├── Transition: 0% → 200% → 100% (speed burst)
│   └── Clip B start: 100% → 50% → 100%
├── Enable Optical Flow: Speed Warp (Studio)
└── Render Cache for playback
```

**Speed Ramp Patterns**:

| Pattern | Curve Shape | Use Case |
|---------|-------------|----------|
| Slow→Fast | Decelerate then accelerate | Action impact, reveal |
| Fast→Slow | Accelerate then decelerate | Crash, landing, emphasis |
| Freeze→Motion | 0% hold then ease out | Dramatic pause, photo-to-video |
| Reverse | Negative speed | Rewind, memory, surreal |

**Retime Curve Tips**:
- **Bezier Handles**: Drag for smooth S-curves
- **Keyframe Sync**: Align speed keyframes to music beats
- **Optical Flow**: Essential for slow-mo (Speed Warp best quality)

### 4. Creative OFX Effects (Color/Edit Page)
**Studio-exclusive and built-in creative effects**

```
Effects Library → OpenFX → ResolveFX / Third-party
├── ResolveFX Texture
│   ├── Film Grain (Kodak/Fuji presets, custom)
│   ├── Halation (highlight bloom, film look)
│   ├── Bloom (soft glow)
│   └── Glare (anamorphic streaks)
├── ResolveFX Stylize
│   ├── Lens Flare (anamorphic, circular, custom)
│   ├── Chromatic Aberration (RGB split)
│   ├── Vignette (custom shape, feather)
│   └── Edge Detect (line art, stylize)
├── ResolveFX Light
│   ├── Light Rays (god rays, volumetric)
│   ├── Lens Flare (advanced)
│   └── Glow (soft, highlight-based)
└── ResolveFX Warp
    ├── Lens Distortion (barrel/pincushion)
    └── Perspective Warp
```

**Applying as Transition Effect**:
```
Adjustment Clip (above cut on timeline)
├── Duration: Spans cut (e.g., 15 frames each side)
├── Effect: Glow / Film Grain / Halation
├── Keyframes: Intensity 0 → 100 → 0 across cut
└── Blend Mode: Screen/Add (for glow/flare)
```

**Popular Transition Effect Combos**:
| Combo | Effects | Settings |
|-------|---------|----------|
| Film Burn | Halation + Film Grain + Vignette | Halation 0.5, Grain 15%, Vignette -0.3 |
| Digital Glitch | Chromatic Aberration + Noise + RGB Offset | Aberration 5px, Noise 10%, Offset 3px |
| Dreamy | Glow + Bloom + Soft Focus | Glow 0.3, Bloom 0.4, Blur 2px |
| Anamorphic | Lens Flare (anamorphic) + Chromatic Aberration | Flare 50%, Aberration 2px |

### 5. Instagram Reel Transition Style
**Reference**: Cz02iyXrjan, Ct3ex_fLyZA

**Vertical 9:16 Transition Tips**:
- Use **Push/Slide** transitions (vertical direction)
- Keep duration **short (8-15 frames)** for Reel pacing
- Match transition direction to camera movement
- Add **sound design** (whoosh, snap) synced to transition

```
Reel Transition Template:
├── Cut on beat
├── Push Transition (Up/Down matching content)
├── Duration: 10-12 frames @ 30fps
├── Easing: Ease Out (snappy)
├── Overlay: Light leak or flash frame (2-3 frames)
└── SFX: Synced whoosh/pop
```

## Fusion Transition Template (Copy-Paste)

```lua
-- Save as .setting file or Macro
-- Simple Dissolve with Ease
Tools = ordered() {
    MediaIn1 = MediaIn { },
    MediaIn2 = MediaIn { },
    Dissolve = Dissolve {
        Inputs = {
            Blend = Input { Value = 0.5, }, -- Animate 0→1
            ["Blend Mode"] = Input { Value = FuID { "Normal" }, },
        },
    },
    MediaOut = MediaOut {
        Inputs = {
            Input = Input { SourceOp = "Dissolve", Source = "Output", },
        },
    },
}
```

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Transition won't apply | Insufficient handles (media) | Extend clips, use "Trim to Fill" |
| Black flash at cut | Clips don't butt exactly | Zoom timeline, snap to cut |
| Choppy playback | No render cache | Playback → Render Cache → User/Smart |
| Fusion transition offline | Missing media in comp | Relink MediaIn nodes |
| Speed Warp artifacts | Complex motion, occlusion | Reduce speed change, add keyframes |

## Related Skills
- `davinci-resolve-fusion-compositing` - Advanced Fusion techniques
- `instagram-reel-editing-techniques` - Reel-specific transitions
- `davinci-resolve-optical-flow-retime` - Speed Warp deep dive
- `davinci-resolve-creative-effects` - Glow, halation, film grain