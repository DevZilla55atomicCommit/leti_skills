---
name: instagram-reel-color-grading-workflow
description: Instagram Reel-specific color grading workflows optimized for social media delivery. Use when creating Reels content with vibrant, engaging looks that work on mobile screens.
trigger: User wants to grade Instagram Reels in DaVinci Resolve with social-media-optimized looks.
category: davinci-resolve
tags:
  - instagram reel
  - color grading
  - social media
  - davinci resolve
  - vertical video
steps:
  - name: instagram-reel-base-grade
    description: Base grade optimized for mobile viewing (higher contrast, punchier colors)
    parameters:
      - name: contrast_boost
        type: string
        default: "15-25%"
        description: Increase contrast for small screens
      - name: saturation_boost
        type: string
        default: "10-20%"
        description: Boost saturation for pop on mobile
      - name: shadow_lift
        type: string
        default: "slight"
        description: Lift shadows to prevent crushing on phone displays
    difficulty: beginner
  - name: instagram-reel-teal-orange-look
    description: Popular teal/orange complementary color scheme for Reels
    parameters:
      - name: teal_intensity
        type: string
        default: "medium"
        description: Teal push in shadows/midtones
      - name: orange_skin_protection
        type: boolean
        default: true
        description: Protect skin tones from teal contamination
      - name: split_toning
        type: boolean
        default: true
        description: Use split toning for shadows/highlights
    difficulty: intermediate
  - name: instagram-reel-vibrant-pop
    description: High-energy vibrant look for lifestyle/travel Reels
    parameters:
      - name: vibrance
        type: string
        default: "high"
        description: Vibrance over saturation for natural skin
      - name: clarity
        type: string
        default: "medium"
        description: Local contrast for texture pop
      - name: highlight_rolloff
        type: string
        default: "soft"
        description: Protect highlights from clipping
    difficulty: intermediate
parameters:
  - name: aspect_ratio
    type: string
    default: "9:16"
    description: Instagram Reel vertical format
  - name: delivery_colorspace
    type: string
    default: "Rec.709 / sRGB"
    description: Mobile display target
  - name: bit_depth
    type: string
    default: "10-bit recommended"
    description: Prevent banding in gradients
---

# Instagram Reel Color Grading Workflow

DaVinci Resolve color grading workflows specifically tailored for Instagram Reels (9:16 vertical, mobile-first delivery). Techniques optimized for small-screen viewing with punchy contrast, protected skin tones, and social-media-ready looks.

## Video References

| Technique | Video ID | Key Nodes | Tags |
|-----------|----------|-----------|------|
| Instagram Reel Color Grading | C4bgrkyJ572 | Color Wheels, LUTs | color grading, instagram reel |
| Instagram Reel C4T1GP7pvpW | C4T1GP7pvpW | Color, Edit | color grading, instagram reel |
| Instagram Reel C2BV1DJy2Cn | C2BV1DJy2Cn | node1, node2 | color correction, grading, instagram reel |
| Instagram Reel C2AxeJLuvPE | C2AxeJLuvPE | Color, Edit | color correction, grading, instagram reel |
| Instagram Reel C1mVyNYNvQ8 | C1mVyNYNvQ8 | node1, node2 | color correction, grading |
| Instagram Reel Color Correction & Grading | CeTi2YXljSw | Color Wheels, LUTs | color correction, grading |

## Core Workflow

### 1. Project Setup for Reels
```
Timeline Settings:
├── Resolution: 1080x1920 (9:16)
├── Frame Rate: 30fps or 60fps
├── Color Space: DaVinci YRGB Color Managed
├── Input Color Space: Camera log (S-Log3, LogC, etc.)
├── Timeline Color Space: Rec.709
└── Output Color Space: Rec.709 / sRGB
```

### 2. Base Grade for Mobile (All Reels)
**Reference**: C4bgrkyJ572, CeTi2YXljSw

```
Node 1: Input Transform (Camera Log → Rec.709)
Node 2: Primary Correction (Color Wheels)
├── Contrast: +15-25% (punchier for small screens)
├── Saturation: +10-20% (vibrant but not oversaturated)
├── Shadow Lift: Slight (prevent crushing on OLED)
├── Highlight Roll-off: Soft (protect specular highlights)
└── Skin Tone Check: Vectorscope → Skin Tone Line
Node 3: Creative Look (per technique below)
Node 4: Output Transform (Rec.709 → sRGB for delivery)
```

### 3. Teal/Orange Complementary Look
**Reference**: Popular Instagram aesthetic

```
Node 3: Teal/Orange Grade
├── Color Warper / Hue vs Hue
│   ├── Push shadows → Teal (180-200°)
│   ├── Push highlights → Orange/Gold (30-45°)
│   └── Protect skin tones (25-35°) with qualifier
├── Split Toning (Alternative)
│   ├── Shadows: Teal tint (Hue ~190, Sat ~15-25)
│   ├── Highlights: Warm gold (Hue ~40, Sat ~10-20)
│   └── Balance: Slightly toward highlights
└── Skin Tone Protection
    ├── Qualifier: Select skin tones (Hue 25-35, wide Sat/Lum)
    └── Invert mask → Apply teal only to non-skin areas
```

### 4. Vibrant Pop Look (Travel/Lifestyle)
**Reference**: C4T1GP7pvpW, C2BV1DJy2Cn

```
Node 3: Vibrant Pop
├── Color Wheels
│   ├── Gain: Push warmth slightly (+0.05 offset)
│   └── Saturation: +15-20%
├── Curves (Custom)
│   ├── RGB: Gentle S-curve for contrast
│   ├── Red: Slight lift in shadows (warmth)
│   └── Blue: Slight lift in highlights (sky pop)
├── Color Boost / Vibrance
│   ├── Vibrance: +25-35% (protects skin)
│   └── Saturation: +5-10% (global)
└── Clarity / Local Contrast
    ├── Radius: 20-30px
    └── Amount: +10-15%
```

### 5. Moody/Cinematic Look (Narrative Reels)
**Reference**: C8AANlhv82q (moody grade), C3dokA0OETD (Gibral Rock)

```
Node 3: Moody Cinematic
├── LUT: Film emulation (Kodak 2383, Fuji 3510) at 40-60%
├── Color Wheels
│   ├── Lift: Teal/blue push (+0.1 blue in shadows)
│   ├── Gamma: Slight green-magenta shift for mood
│   └── Gain: Warm highlight retention
├── Curves
│   ├── RGB: Crushed blacks, rolled highlights
│   └── Hue vs Sat: Desaturate greens, saturate reds/oranges
└── Grain: Film grain overlay (subtle, 10-15% opacity)
```

### 6. Clean Commercial Look (Product/Beauty)
**Reference**: C2AxeJLuvPE, C1mVyNYNvQ8

```
Node 3: Clean Commercial
├── Color Wheels: Neutral, accurate white balance
├── Color Correction Node: Skin tone refinement
│   ├── Qualifier: Skin tones
│   ├── Hue: Shift toward healthy (slight orange)
│   ├── Sat: Reduce slightly (-5-10%) for clean look
│   └── Lum: Slight lift for glow
├── Power Windows: Product highlight (circular, tracked)
└── Output: Precise Rec.709, no creative LUT
```

## Delivery Settings for Instagram Reels

| Setting | Value | Reason |
|---------|-------|--------|
| Format | MP4 (H.264/H.265) | Instagram requirement |
| Resolution | 1080x1920 | Native Reel resolution |
| Frame Rate | 30fps | Standard (60fps for smooth motion) |
| Bitrate | 8-12 Mbps (H.264), 5-8 Mbps (H.265) | Quality vs file size |
| Color Space | Rec.709 / sRGB | Mobile display target |
| Audio | AAC 128kbps+ | Instagram standard |
| Max Duration | 90 seconds | Reel limit |

## Quick Presets (Save as Grade Versions)

| Preset Name | Use Case | Key Settings |
|-------------|----------|--------------|
| Reel_Base | Starting point | +20% contrast, +15% sat, shadow lift |
| Reel_TealOrange | Lifestyle, travel | Teal shadows, orange highlights, skin protect |
| Reel_VibrantPop | Travel, food, energy | High vibrance, clarity, S-curve |
| Reel_MoodyCinematic | Narrative, fashion | Film LUT 50%, crushed blacks, grain |
| Reel_CleanCommercial | Product, beauty | Neutral WB, skin refine, product pop |

## Common Pitfalls & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Banding in skies | 8-bit export, heavy gradients | Use 10-bit export, add subtle noise/grain |
| Skin looks green | Teal shadow contamination | Qualifier mask on skin, invert teal push |
| Crushed blacks on phone | Over-aggressive contrast | Lift shadows +5-10, soft roll-off |
| Oversaturated on Android | Wide gamut displays | Target sRGB, reduce saturation 5-10% |
| Flicker in transitions | Frame rate mismatch | Ensure timeline = export = source fps |

## Related Skills
- `davinci-resolve-color-grading-fundamentals` - Core grading techniques
- `davinci-resolve-vertical-video-workflow` - 9:16 editing/transform
- `instagram-reel-editing-techniques` - Cutting, pacing, transitions