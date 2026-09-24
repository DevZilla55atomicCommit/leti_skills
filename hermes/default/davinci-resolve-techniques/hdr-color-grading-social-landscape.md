---
name: hdr-color-grading-social-landscape
description: HDR color grading workflows for social media and landscape content. Covers HDR Color Wheels, HDR Palette, highlight/shadow recovery, and high-bitrate export for Instagram.
trigger: User wants to grade HDR content, recover highlights/shadows in landscape footage, or create vibrant social media looks with HDR tools.
category: davinci-resolve/color-grading
tags: [hdr, color-grading, instagram, landscape, davinci-resolve, hdr-color-wheels, hdr-palette, curves, color-tone, highlight-recovery, shadow-detail]
steps:
  - name: HDR Color Grading for Social Media (DEploZ8IT9M)
    description: HDR workflow with highlight boost for sunsets, shadow lift for detail, and mobile-optimized vibrance
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [HDR Color Wheels, HDR Palette, Curves, Color Tone]
    parameters:
      HDR_Global_Contrast: "Increased"
      HDR_Highlights: "Boosted for sunset pop"
      HDR_Shadows: "Lifted for detail in snow"
      Saturation: "Increased for mobile vibrance"
    steps:
      - Set project color management to Rec.709 or DaVinci Wide Gam for HDR workflow
      - Add an HDR Color Wheels node to isolate high-dynamic range areas
      - Adjust the HDR Highlights slider to bring life to the sunset clouds without clipping whites
      - Use the HDR Shadows slider to reveal detail in the snowy mountain shadows
      - Apply a slight glow or bloom effect to the light sources
      - Export using H.264/H.265 with high bitrate for Instagram compression
    difficulty: intermediate
    video_id: DEploZ8IT9M
    tags: [HDR, ColorGrading, Instagram, Landscape, DaVinciResolve]

  - name: Atmospheric Haze & Cinematic Grading (C_s_3BrqhAl)
    description: Aerial/landscape haze look with lowered contrast, localized saturation, glow/blur for atmosphere
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Power Window, Color Mixer]
    parameters:
      Contrast: "Lowered"
      Saturation: "Reduced"
      Midtone_Detail: "Increased"
      Tint: "Teal/Blue shift"
    steps:
      - Add a primary node to balance exposure and lower the overall contrast
      - Apply a Power Window to the landmass to slightly increase saturation locally
      - Use the Glow effect or a slight Blur node to create a misty/atmospheric look
      - Shift shadows toward blue/teal and highlights toward a warm or neutral tone using Color Wheels
      - Adjust the Midtone Detail to bring back texture to the water and trees
    difficulty: intermediate
    video_id: C_s_3BrqhAl
    tags: [cinematic, aerial, colorgrading, haze]

  - name: Natural Light Glow & Soft Diffusion Effect (C95GBSmxyzX)
    description: Dreamy bloom around light sources using Glow node with qualifier isolation
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Exposure, Color Correction, Soft Glow/Glow, Qualifier Mask]
    parameters:
      Glow_Threshold: "0.4"
      Glow_Radius: "0.50"
      Opacity: "0.3"
      Highlights_Gain: "+1.2"
    steps:
      - Import footage and go to the Color page
      - Add a serial node to balance exposure and white balance
      - Add a second serial node for effects and apply the Glow effect or use the Glow node
      - Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger the effect
      - Increase the Radius and Opacity to create a dreamy bloom around light sources
      - Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows or midtones
    difficulty: intermediate
    video_id: C95GBSmxyzX
    tags: [cinematic, natural light, glow, color grading]
parameters:
  - name: HDR_Global_Contrast
    description: Overall HDR contrast adjustment
  - name: HDR_Highlights
    description: Highlight recovery and shaping
  - name: HDR_Shadows
    description: Shadow detail recovery
  - name: Saturation
    description: Overall saturation for mobile display
  - name: Glow_Threshold
    description: Luminance threshold for glow effect (0-1)
  - name: Glow_Radius
    description: Bloom radius spread
  - name: Opacity
    description: Glow effect opacity
  - name: Midtone_Detail
    description: Texture enhancement in midtones
tags: [hdr, color-grading, instagram, landscape, davinci-resolve, hdr-color-wheels, hdr-palette, curves, color-tone, highlight-recovery, shadow-detail, glow, atmospheric]
---

# HDR Color Grading for Social Media & Landscape

**HDR workflows** for vibrant social media content and **landscape photography** with highlight/shadow recovery, atmospheric effects, and mobile-optimized output.

## Techniques Included

### 1. HDR Color Grading for Social Media (DEploZ8IT9M)
**Full HDR pipeline: Wide Gamut → HDR Wheels → Glow → High-bitrate export**

- **Color Management**: DaVinci Wide Gamut / Rec.709
- **Tools**: HDR Color Wheels, HDR Palette, Curves, Color Tone
- **Highlights**: Boost sunset clouds without clipping
- **Shadows**: Lift detail in snow/foreground
- **Export**: H.264/H.265 high bitrate for Instagram

**Nodes**: `Primary → HDR Color Wheels → HDR Palette → Curves → Color Tone → Glow`

### 2. Atmospheric Haze & Cinematic Grading (C_s_3BrqhAl)
**Aerial/landscape haze look with localized adjustments**

- **Contrast**: Lowered for atmospheric depth
- **Saturation**: Reduced globally, boosted locally via Power Window
- **Atmosphere**: Glow/Blur node for mist effect
- **Color**: Teal shadows, warm/neutral highlights
- **Detail**: Midtone Detail for water/tree texture

**Nodes**: `Primary Correction → Power Window → Color Mixer → Glow/Blur`

### 3. Natural Light Glow & Soft Diffusion (C95GBSmxyzX)
**Dreamy bloom around practical lights/sun with shadow protection**

- **Glow Threshold**: 0.4 (only brightest highlights)
- **Glow Radius**: 0.50 for soft spread
- **Opacity**: 0.3 for subtle dreaminess
- **Highlights Gain**: +1.2 for sun beam pop
- **Isolation**: Qualifier/Mask protects shadows/midtones

**Nodes**: `Exposure/WB → Glow Node → Qualifier Mask`

## HDR Workflow for Social Media

```
Project Settings → Color Management → DaVinci Wide Gamut / Rec.2100
                                        ↓
Timeline → Color Page → HDR Color Wheels (Highlights/Shadows)
                                        ↓
HDR Palette → Curves (tone mapping) → Color Tone (creative)
                                        ↓
Glow/Bloom (optional) → Deliver → H.265 30Mbps → Instagram
```

## HDR Color Wheels vs Regular Wheels

| Feature | Regular Wheels | HDR Wheels |
|---------|---------------|------------|
| Range | 0-1 (SDR) | 0-100+ nits |
| Highlights | Clips at 1.0 | Recovers to 1000+ nits |
| Shadows | Crushes at 0 | Lifts detail from -10 |
| Best For | SDR delivery | HDR grading, highlight recovery |

## Pro Tips

1. **Set color management first** - Project Settings → Color Management → DaVinci Wide Gamut
2. **Monitor in HDR** - Use HDR reference monitor or Simulate HDR on SDR
3. **Highlight rolloff** - Use HDR Highlights wheel, not Gain (preserves midtones)
4. **Shadow lift** - HDR Shadows wheel recovers without noise amplification
5. **Mobile preview** - Check on phone: shadows crush, saturation pops differently

## Export for HDR Social

- **Codec**: H.265 (HEVC) preferred for HDR
- **Profile**: Main 10 / Main 10@L5.1
- **Bitrate**: 30-50 Mbps for HDR
- **Metadata**: Include HDR10/ HLG SEI messages
- **Test**: Upload private, check on mobile HDR display