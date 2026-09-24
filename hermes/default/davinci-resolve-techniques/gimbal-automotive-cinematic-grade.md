---
name: gimbal-automotive-cinematic-grade
description: Cinematic automotive grading with gimbal stabilization workflow — primary correction, power windows for car body highlights, curves for metallic paint, and LUT finishing in DaVinci Resolve Color page.
trigger: User grading car footage, automotive content, gimbal-stabilized shots, or metallic paint enhancement
category: davinci-resolve-color-grading
tags:
  - automotive
  - gimbal
  - cinematic
  - color-grading
  - stabilization
  - metallic-paint
  - power-windows
parameters:
  - name: stabilization_mode
    description: Stabilizer mode for gimbal footage cleanup
    default: "Perspective / Similarity"
    type: string
  - name: primary_contrast
    description: Contrast boost for carbon fiber/texture
    default: "High (1.15-1.25)"
    type: string
  - name: power_window_shape
    description: Mask shape for car body highlights
    default: "Custom Bezier / Power Window"
    type: string
  - name: lut_style
    description: Final LUT for cinematic automotive look
    default: "Kodak 2383 / Fuji 3513 / Custom cinematic"
    type: string
steps:
  - step: "Stabilize: Inspector → Stabilizer → Perspective/Similarity mode, Smooth 0.5-1.0, Zoom 1.05-1.15 if needed"
  - step: "Node 1 - Primary: Balance blacks/whites on carbon fiber texture, set contrast high, slight saturation boost"
  - step: "Node 2 - Power Window: Custom shape masking car body, increase exposure +0.1-0.2, boost saturation +10-15% on metallic paint"
  - step: "Node 3 - Curves: RGB curves for metallic tone separation — lift reds in highlights, crush blues in shadows"
  - step: "Node 4 - LUT/Grade: Apply cinematic LUT (Kodak 2383, Fujifilm 3513) at 40-60% intensity, adjust temperature for golden hour warmth"
  - step: "Optional Node 5 - Glow/Halation: Subtle glow on specular highlights (sun reflections on paint)"
difficulty: intermediate
resolve_page: Color
node_graph_type: serial
key_nodes:
  - Stabilizer (Inspector)
  - Primary Wheels
  - Power Window (Custom)
  - RGB Curves
  - LUT / Film Emulation
source_techniques:
  - video_id: DHLSAxAIQ9O
    technique_name: Gimbal Stabilization and Dynamic Color Grading
    tags: [gimbal, cinematic, color-grading, automotive, stabilization]
  - video_id: DG5M8Mhocoz
    technique_name: Dynamic Gimbal Stabilization and Color Grading
    tags: [automotive, gimbal, cinematic, colorgrading]
  - video_id: DADa0Tturp7
    technique_name: Gimbal Movement for Car Photography
    tags: [Car Photography, Gimbal Movement]
---

# Gimbal & Automotive Cinematic Grade

Complete workflow for grading gimbal-stabilized automotive footage — from stabilization cleanup to metallic paint enhancement and cinematic LUT finishing.

## When to Use
- Car commercials / automotive content
- Gimbal/glidecam footage needing micro-jitter cleanup
- Metallic/pearlescent paint enhancement
- Golden hour / magic hour car shoots
- Social media automotive reels (Instagram/TikTok/Reels)

## Node Graph (Serial) + Inspector Stabilizer

```
Inspector: Stabilizer (Perspective/Similarity)
    ↓
Node 1: Primary Correction (Balance, Contrast, Sat)
    ↓
Node 2: Power Window → Car Body (Exposure + Sat boost)
    ↓
Node 3: RGB Curves (Metallic tone separation)
    ↓
Node 4: Cinematic LUT (Kodak 2383 / Fuji 3513 @ 40-60%)
    ↓
Node 5: Optional Glow on Specular Highlights
```

## Stabilizer Settings (Inspector → Stabilizer)
| Parameter | Value | Notes |
|-----------|-------|-------|
| Mode | Perspective / Similarity | Perspective for 3D gimbal moves |
| Smooth | 0.5 - 1.0 | Lower = more natural, higher = locked |
| Zoom | 1.05 - 1.15 | Compensates for stabilization crop |
| Camera Lock | OFF | Use for tripod; ON only for locked-off simulation |

## Node Details

### Node 1: Primary Correction
- **Lift**: Crush blacks slightly on carbon fiber/tire detail (Lift -0.02 to -0.05)
- **Gamma**: 1.05-1.1 for midtone contrast
- **Gain**: Protect highlights on chrome/glass (Gain 0.98-1.0)
- **Contrast**: 1.15-1.25 (punchy for automotive)
- **Saturation**: 105-110% (metallic paint pops)
- **Temp/Tint**: Warm 5600-6000K for golden hour; neutral 5000K for showroom

### Node 2: Power Window — Car Body Highlights
- **Shape**: Custom Bezier tracing car silhouette
- **Feather**: 15-25 (soft edge on body panels)
- **Adjustments**:
  - Exposure: +0.1 to +0.2 (brings out metallic flake)
  - Saturation: +10% to +15% (paint vibrancy)
  - Contrast: +5-10 (panel definition)
- **Invert**: OFF (affecting car only)

### Node 3: RGB Curves — Metallic Tone Separation
| Channel | Curve Shape | Purpose |
|---------|-------------|---------|
| **Red** | Highlight lift (+5-10) | Warm metallic highlights |
| **Green** | Slight midtone dip (-3) | Reduce green cast on silver/gray |
| **Blue** | Shadow crush (-5 to -10) | Deep shadows, cool undertones |
| **Master** | Gentle S-curve | Overall contrast |

### Node 4: Cinematic LUT
| LUT | Intensity | Best For |
|-----|-----------|----------|
| Kodak 2383 | 40-60% | Classic film, warm highlights |
| Fujifilm 3513 | 30-50% | Cooler, cleaner, modern |
| Arri LogC → Rec709 | 100% | If footage is Log, use as base |
| Custom "Automotive" | 50-70% | Tailored to brand colors |

### Node 5 (Optional): Glow on Speculars
- **Tool**: Glow OFX or Blur + Screen blend
- **Threshold**: 0.85-0.95 (only brightest reflections)
- **Radius**: 15-30 pixels
- **Opacity**: 0.15-0.25
- **Mask**: Qualifier on highlights (Lum > 90%) → feed to Glow mask input

## Pro Tips from Source Techniques

### From DHLSAxAIQ9O (Gimbal Stabilization)
> "Mount camera on gimbal for smooth low-angle tracking shots → Stabilizer in Inspector for micro-jitters → Primary grade on carbon fiber texture → LUT for cinematic automotive look"

### From DG5M8Mhocoz (Dynamic Gimbal)
> "Power Windows to isolate highlights on car body → Cinematic LUT for final look → Capture with motorized gimbal for smooth tracking"

### From DADa0Tturp7 (Gimbal Movement)
> "45° camera angle, slow steady movement → Turntable for 360° product shots → Stabilize in post for micro-corrections"

## Scope Targets
- **Waveform**: Car body 40-70 IRE, speculars 90-100 IRE (don't clip!)
- **Vectorscope**: Metallic paints near center (desaturated), accents on skin tone line
- **Parade**: Balanced RGB on neutral grays; separation on colored paints

## Common Pitfalls
- ❌ Over-stabilizing → "Jello" warp on background; keep Smooth ≤ 1.0
- ❌ Clipping chrome/glass highlights → pull Gain down, use Qualifier to protect
- ❌ Power window too sharp → feather 15+ or use gradient mask
- ❌ LUT at 100% → looks "LUTty"; blend 40-60% with graded base
- ❌ Saturation too high → metallic paint looks plastic; 105-110% max

## Delivery for Social Media (Instagram Reels)
See `social-media-sharpening-export` skill for:
- 1080×1920 vertical crop with safe zones
- 20-30 Mbps H.264/HEVC
- Sharpening for compression resilience

## Related Skills
- `teal-orange-cinematic-grade` — for stylized automotive looks
- `social-media-sharpening-export` — final delivery
- `hdr-social-media-grade` — HDR automotive workflow
- `stabilization-workflow` — deeper stabilization techniques