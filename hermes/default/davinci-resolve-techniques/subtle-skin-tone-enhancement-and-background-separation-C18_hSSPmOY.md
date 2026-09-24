---
name: subtle-skin-tone-enhancement-and-background-separation
description: 'DaVinci Resolve technique: Subtle Skin Tone Enhancement and Background
  Separation from Instagram Reel C18_hSSPmOY'
category: davinci-resolve
tags:
- color grading
- skin tones
- background separation
- subtle adjustments
- color
- intermediate
version: 1.0.0
source_reel_id: C18_hSSPmOY
resolve_page: Color
node_graph_type: serial
key_nodes:
- ColorWheel
- Curves
- Qualifier
parameters:
  ColorWheel_Lift_Gamma_Gain:
    lift:
    - 1.0
    - 1.0
    - 1.0
    gamma:
    - 1.0
    - 1.0
    - 1.0
    gain:
    - 1.0
    - 1.0
    - 1.0
  Curves_Midtones:
    gamma: 1.0
  Qualifier_Hue:
  - 0.0
  - 1.0
  Qualifier_Saturation:
  - 0.0
  - 1.0
  Qualifier_Luminance:
  - 0.0
  - 1.0
steps_to_reproduce:
- Add a new node.
- Use the Color Wheels to make subtle adjustments to Lift, Gamma, and Gain to balance
  the overall exposure and contrast.
- Add another node.
- Use the Curves tool to fine-tune the midtones for a more pleasing look.
- Add a third node.
- Use the Qualifier to select the skin tones.
- Make subtle adjustments to Hue, Saturation, and Luminance within the Qualifier to
  enhance the skin tones without making them look unnatural.
- Add a fourth node.
- Use a power window to create a subtle vignette or to further separate the subject
  from the background by slightly darkening or adjusting the background colors.
difficulty: intermediate
---
# Subtle Skin Tone Enhancement and Background Separation

**Source Reel:** C18_hSSPmOY
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C18_hSSPmOY.

## Key Nodes
- ColorWheel
- Curves
- Qualifier

## Parameters
ColorWheel_Lift_Gamma_Gain:
  lift:
  - 1.0
  - 1.0
  - 1.0
  gamma:
  - 1.0
  - 1.0
  - 1.0
  gain:
  - 1.0
  - 1.0
  - 1.0
Curves_Midtones:
  gamma: 1.0
Qualifier_Hue:
- 0.0
- 1.0
Qualifier_Saturation:
- 0.0
- 1.0
Qualifier_Luminance:
- 0.0
- 1.0


## Steps to Reproduce
1. Add a new node.
2. Use the Color Wheels to make subtle adjustments to Lift, Gamma, and Gain to balance the overall exposure and contrast.
3. Add another node.
4. Use the Curves tool to fine-tune the midtones for a more pleasing look.
5. Add a third node.
6. Use the Qualifier to select the skin tones.
7. Make subtle adjustments to Hue, Saturation, and Luminance within the Qualifier to enhance the skin tones without making them look unnatural.
8. Add a fourth node.
9. Use a power window to create a subtle vignette or to further separate the subject from the background by slightly darkening or adjusting the background colors.

## Tags
color grading, skin tones, background separation, subtle adjustments
