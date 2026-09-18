---
name: Subtle Skin Tone Enhancement and Background Separation
description: DaVinci Resolve technique from Instagram Reel C18_hSSPmOY
trigger: "subtle skin tone enhancement and background separation"
page: Color
difficulty: intermediate
tags: ['color grading', 'skin tones', 'background separation', 'subtle adjustments']
video_id: C18_hSSPmOY
source: instagram-reel
updated: 2026-07-28T12:39:28.948243
---

# Subtle Skin Tone Enhancement and Background Separation

**Source:** Instagram Reel `C18_hSSPmOY`  
**Resolve Page:** Color  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- ColorWheel
- Curves
- Qualifier

## Parameters
- **ColorWheel_Lift_Gamma_Gain:** {'lift': [1.0, 1.0, 1.0], 'gamma': [1.0, 1.0, 1.0], 'gain': [1.0, 1.0, 1.0]}
- **Curves_Midtones:** {'gamma': 1.0}
- **Qualifier_Hue:** [0.0, 1.0]
- **Qualifier_Saturation:** [0.0, 1.0]
- **Qualifier_Luminance:** [0.0, 1.0]

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
- #color grading
- #skin tones
- #background separation
- #subtle adjustments
