---
name: davinci-subtle-skin-tone-enhancement-and-background-separation
description: DaVinci Resolve technique: Subtle Skin Tone Enhancement and Background Separation from Instagram Reel C18_hSSPmOY
category: creative/davinci-resolve-techniques
tags: ["color grading", "skin tones", "background separation", "subtle adjustments", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C18_hSSPmOY"
collection: "Export_Photos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Subtle Skin Tone Enhancement and Background Separation

**Source:** Instagram Reel `C18_hSSPmOY` (Export_Photos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Subtle Skin Tone Enhancement and Background Separation](C18_hSSPmOY.gif)

## Node Graph Structure

- ColorWheel
- Curves
- Qualifier

## Parameters

- **ColorWheel_Lift_Gamma_Gain**: {'lift': [1.0, 1.0, 1.0], 'gamma': [1.0, 1.0, 1.0], 'gain': [1.0, 1.0, 1.0]}
- **Curves_Midtones**: {'gamma': 1.0}
- **Qualifier_Hue**: [0.0, 1.0]
- **Qualifier_Saturation**: [0.0, 1.0]
- **Qualifier_Luminance**: [0.0, 1.0]

## Steps to Reproduce in DaVinci Resolve

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
`color grading`, `skin tones`, `background separation`, `subtle adjustments`
