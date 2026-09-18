---
name: motion-graphics-fundamentals-fusion
description: Core motion graphics concepts in DaVinci Resolve Fusion page
category: photography
tags: [fusion, motion-graphics, keyframing, text, tracking, particles]
difficulty: intermediate
---

# Motion Graphics Fundamentals in Fusion

Core motion graphics workflows using DaVinci Resolve Fusion page.

## Fusion Interface Basics

### Node Types for Motion Graphics
| Category | Key Nodes |
|----------|-----------|
| **Generators** | Background, FastNoise, Gradient, Shape3D |
| **Text** | Text+, Text3D, CharacterLevelStyling |
| **Transform** | Transform, Transform3D, Camera3D, Renderer3D |
| **Masking** | Rectangle, Ellipse, Polygon, B-Spline, Paint |
| **Color** | BrightnessContrast, ColorCorrector, GamutMap |
| **Blur/Sharpen** | Blur, DirectionalBlur, VectorBlur, Sharpen |
| **Particles** | pEmitter, pRender, pTurbulence, pGravity |
| **Time** | TimeSpeed, TimeStretcher, FrameHold |

### Flow View Navigation
- **Pan**: Middle mouse / Space + drag
- **Zoom**: Scroll wheel / Ctrl + scroll
- **Fit**: F key
- **Search**: Tab → type node name

## Text Animation

### Text+ Essentials
1. **Text+** → StyledText for rich formatting
2. **CharacterLevelStyling** → Per-character animation
3. **Modifiers** → Add via right-click parameter → Add Modifier

### Write-On Effect
```
Text+ → WriteOn (in Modifiers tab)
- WriteOn: 0 to 1 over duration
- Add "Follower" for cursor effect
```

### Text on Path
1. **Text+** → Layout → Path → **B-Spline** or **Circle**
2. Animate **Path Position** for crawl/scroll

## Keyframing Workflow

### Spline Editor (Do This)
1. Set keyframes in Inspector (diamond icon)
2. Open **Spline Editor** (bottom panel)
3. Select keys → **S** for smooth / **L** for linear
4. **Overshoot**: Pull handles past target
5. **Easy Ease**: Right-click → Ease In/Out

### Expression Basics
Right-click parameter → **Expression**:
```lua
-- Loop
math.sin(time * 2 * math.pi / duration) * amplitude

-- Random shake
math.random(-1, 1) * intensity

-- Link to other node
comp.FindTool("Transform1").Center.X
```

## Tracking & Match Move

### Planar Tracker (Best for Screens/Surfaces)
1. **Tracker** node → Operation: **Track**
2. Draw spline on planar surface
3. **Track Forward**
4. **Export** → Corner Pin / Transform / Stabilize

### Point Tracker (For Single Points)
1. **Tracker** → Tracker 1-4
2. Pattern box on high-contrast detail
3. Search box larger for motion
4. **Apply** → To Transform / Stabilize

### Camera Tracker (3D)
1. **CameraTracker** node
2. **Track** → Solve Camera
3. **Create** → 3D Scene with Camera3D + PointCloud
3D text/objects now match move!

## Particle Systems

### Basic Emitter Setup
```
Background → pEmitter → pRender → Merge → MediaOut
              │
              ├─ pTurbulence (organic motion)
              ├─ pGravity (fall)
              ├─ pDirectionalForce (wind)
              └─ pColor (age-based color)
```

### Common Parameters
| Parameter | Effect |
|-----------|--------|
| **Number** | Particles per frame |
| **Lifespan** | Frames alive |
| **Velocity** | Initial speed |
| **Spread** | Emission cone angle |
| **Style** | Point / Blob / Sprite / Line |

### Text Dissolve to Particles
1. Text+ → **Text to Mask** (right-click)
2. pEmitter → **Shape** = Bitmap (connect mask)
3. Animate **Number** 1000 → 0
4. Add **pTurbulence** for organic scatter

## 3D Motion Graphics

### Basic 3D Scene
```
Shape3D (Text3D/Box/Sphere) → Renderer3D → MediaOut
         ▲              ▲
         │              │
    Camera3D ────────── Lights (Point/Spot/Directional)
```

### Camera Animation
- **Camera3D** → Transform → Keyframe Position/Rotation
- **Focal Length** → Dolly zoom (zoom + dolly counter-move)
- **Depth of Field** → Aperture + Focus Distance keyframes

## Templates & Macros

### Create Macro
1. Select nodes → Right-click → **Create Macro**
2. Name, icon, publish parameters
3. Saves as `.setting` in Macros folder

### Publish Parameters
- Right-click any slider → **Publish**
- Appears in Macro Inspector for easy tweaking

## Performance Tips

| Tip | Why |
|-----|-----|
| **Proxy mode** (Timeline → Proxy) | Half-res playback |
| **Cache nodes** (Right-click → Cache) | Pre-render heavy branches |
| **Merge instead of Over** | Faster composite mode |
| **Disable HiQ** during playback | Faster scrub |
| **Reduce viewer resolution** | 50% or 25% in viewer |

## Common Motion Graphics Recipes

### Lower Third
```
Background (Shape) → Text+ (Name) → Text+ (Title) → Merge x2 → Transform (slide in)
```
Animate Transform Position X: -1920 → 0 with overshoot

### Logo Reveal
```
MediaIn (Logo) → Mask (animate reveal) → Glow → Merge over BG
```

### Kinetic Typography
```
Text+ → CharacterLevelStyling → 
  Modifier: Position.Y = sin(time*freq)*amp
  Modifier: Rotation = noise(time)*deg
  Modifier: Scale = 1 + noise(time)*0.2
```

### HUD/UI Elements
- **Shape3D** → Rectangle/Ring for brackets
- **Text+** → Monospace font for data
- **Transform3D** → 3D space placement
- **Camera3D** → Subtle parallax on camera move

## Tags
`fusion` `motion-graphics` `keyframing` `text` `tracking` `particles` `3d` `templates` `expressions`