---
name: photography
description: Use for lens theory, color grading, lighting, compositing.
category: creative
tags: [photography, lenses, color-theory, lighting, compositing, split-screen, architecture]
---

# Photography Techniques

Class-level umbrella for photography skills covering lens theory, color grading fundamentals, architectural/interior lighting, compositing/masking workflows, and split-screen comparative layouts applicable to both still and motion work.

## Sub-Domains

| Domain | Description | Key References |
|--------|-------------|----------------|
| **Lens Theory** | Focal length effects, sensor crop, aperture for cinematic depth | `references/lens-selection-cinematic-look.md` |
| **Color Grading** | Scopes, primary/secondary, creative looks, LUT workflow, HDR | `references/color-grading-theory-fundamentals.md` |
| **Lighting** | Natural/artificial, golden/blue hour, HDR, architectural | `references/architectural-photography-lighting.md` |
| **Compositing** | Masking, tracking, object insertion, Fusion workflows | `references/motion-graphics-fundamentals-fusion.md` |
| **Layout** | Split-screen, before/after, comparison grids | `references/split-screen-comparison-technique.md` |

## Photography → Video Workflow

### Still-to-Motion
1. **Pre-visualize** — Lens choice, lighting design, color palette from stills
2. **Bracket** — HDR brackets for dynamic range (3-5 exposures, 2EV spacing)
3. **Grade** — Apply stills color theory to video timeline (Color page)
4. **Composite** — Fusion masking/tracking for object insertion/removal

### DaVinci Resolve Integration

#### Color Page (Grading)
- **Scopes**: Waveform (luma), Parade (RGB), Vectorscope (skin tone line)
- **Primary**: Lift/Gamma/Gain → Contrast/Pivot → Custom Curves
- **Secondary**: Qualifier (HSL) → Power Windows → Tracker
- **Creative**: Hue vs Hue/Sat/Lum curves, Film LUTs, Grain/Halation

#### Fusion Page (Compositing)
- **Tracking**: Planar Tracker for screens/surfaces, Point Tracker for details
- **Masking**: Polygon/B-Spline/Paint → Keyframe path → Soft Edge
- **3D**: CameraTracker → 3D scene → Text/Shape3D integration
- **Particles**: pEmitter + Forces for atmospheric/text dissolves

#### Edit Page (Layout)
- **Split-screen**: Crop/Transform on stacked tracks, animated wipe
- **Speed**: Retime Curve + Optical Flow + Motion Blur
- **Text**: Text+ with CharacterLevelStyling for kinetic typography

## Key References

- `references/lens-selection-cinematic-look.md` — Focal length effects, sensor crop, aperture choices, lens character
- `references/color-grading-theory-fundamentals.md` — Scopes, primary/secondary workflow, creative looks, LUTs, HDR
- `references/architectural-photography-lighting.md` — Natural/artificial, golden/blue hour, HDR, composition
- `references/split-screen-comparison-technique.md` — Edit/Fusion methods, layouts, sync/alignment, export presets
- `references/motion-graphics-fundamentals-fusion.md` — Text animation, keyframing, tracking, particles, 3D, templates

## Common Mistakes to Avoid

1. **Over-sharpening** — Halos on edges, use Micro Contrast/Texture instead
2. **Saturation abuse** — Hue vs Sat curves for selective control
3. **Ignoring gamut** — CST input/output for every camera profile
4. **Flat lighting** — Always create depth with shadow/highlight separation
5. **No reference** — ColorChecker/X-Rite on every shoot for match

## Related Skills

- `cinematography` — Camera movement, gimbal, stabilization, transitions
- `camera-hardware` — Sensor formats, codecs, log profiles, media management
- `davinci-resolve` — Color grading, Fusion masking, stabilization tools

## Session Context (2026-07-29)

Created from Instagram→DaVinci pipeline where non-Resolve content (architectural photography, lens tutorials, color grading demos) needed structured categorization. NVIDIA API is the only reliable vision path; local Ollama crashes on M4 16GB under concurrent load.