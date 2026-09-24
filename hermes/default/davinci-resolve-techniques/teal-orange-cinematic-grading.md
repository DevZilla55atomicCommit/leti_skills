---
name: teal-orange-cinematic-grading
description: Teal & Orange cinematic color grading techniques for automotive, urban, and landscape footage using Color Wheels, Curves, and Power Windows.
trigger: User wants to create cinematic teal-orange look, grade automotive/urban footage, or learn professional color grading workflows.
category: davinci-resolve/color-grading
tags: [cinematic, teal-orange, color-grading, color-wheels, curves, power-windows, automotive, urban, landscape]
steps:
  - name: Cinematic Teal & Orange Color Grading (C_lLHxVgEyc)
    description: Classic teal-orange look with Power Windows for subject isolation and vignette for focus
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Color Wheels, Power Windows, Vignette]
    parameters:
      Temperature: "Warm Highlights"
      Contrast: "High"
      Saturation: "Desaturated Midtones"
      Shadow_Tint: "Teal/Cyan"
    steps:
      - Add a primary correction node to balance exposure and contrast
      - Use Color Wheels to push shadows toward a teal/blue tint
      - Use Color Wheels to push highlights toward a warm/orange tone
      - Apply a Power Window to the subject (car) to slightly increase exposure and saturation
      - Add a subtle vignette to draw focus to the center
    difficulty: intermediate
    video_id: C_lLHxVgEyc
    tags: [color-grading, cinematic, golden-hour, automotive]

  - name: Muted Teal & Orange Cinematic Color Grade (DGgVaDWSTMg)
    description: Muted teal-orange look with HDR tools, hue/saturation curves for green/yellow desaturation
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Correction, Color Wheels, Curves, HDR]
    parameters:
      Saturation: "35"
      Contrast: "1.20"
      Shadows_Tint: "Teal"
      Highlights_Tint: "Warm/Orange"
    steps:
      - Adjust exposure and contrast using Primary Wheels for a balanced base
      - Use the Lift wheel to push shadows toward a teal/blue hue
      - Use the Gain wheel to push highlights toward a warm orange/yellow hue
      - Lower overall saturation to achieve a muted look
      - Apply a Hue/Saturation curve to target and desaturate greens and yellows
      - Add a slight vignette to draw focus to the subject
    difficulty: beginner
    video_id: DGgVaDWSTMg
    tags: [color-grading, cinematic, tealandorange, urban]

  - name: Cinematic Bottom Masking & Exposure Grading (DFHQC0cuy9-)
    description: Gradient mask on lower frame for moody cinematic look with warm highlight tint
    resolve_page: Color
    node_graph_type: serial
    key_nodes: [Primary Grade, Power Window Mask, Color Balance]
    parameters:
      Exposure: "Low (on mask)"
      Contrast: "High"
      Softness: "High feathering"
      Saturation: "Desaturated in highlights"
    steps:
      - Add a new serial node for the specific grade
      - Open the Power Window tool and select the Linear or Gradient mask
      - Draw the mask covering the bottom half of the frame (the road/foreground)
      - Increase the Softness (feathering) of the mask edge to create a seamless transition
      - Lower the Exposure and Gamma specifically on this masked area to deepen the shadows
      - Apply a warm yellow/orange tint to the highlights globally to match the text color
    difficulty: beginner
    video_id: DFHQC0cuy9-
    tags: [cinematic, masking, color grading, moody]
parameters:
  - name: Temperature
    description: Color temperature for warm/cool balance
  - name: Contrast
    description: Contrast level for cinematic depth
  - name: Saturation
    description: Overall saturation (muted for cinematic look)
  - name: Shadow_Tint
    description: Teal/blue push in shadows
  - name: Highlights_Tint
    description: Warm/orange push in highlights
  - name: Power_Window_Softness
    description: Feathering for seamless mask transitions
tags: [cinematic, teal-orange, color-grading, color-wheels, curves, power-windows, automotive, urban, landscape]
---

# Teal & Orange Cinematic Color Grading

Professional cinematic color grading techniques for creating the signature **teal-orange** look used in automotive, urban, and landscape content. These workflows use DaVinci Resolve's Color Wheels, Curves, Power Windows, and HDR tools.

## Techniques Included

### 1. Cinematic Teal & Orange Color Grading (C_lLHxVgEyc)
Classic teal-orange workflow with subject isolation via Power Windows and vignette for focus.

**Nodes**: Primary Correction → Color Wheels → Power Windows → Vignette  
**Key Parameters**: High Contrast, Desaturated Midtones, Teal Shadows, Warm Highlights

### 2. Muted Teal & Orange Cinematic Color Grade (DGgVaDWSTMg)
Muted variant using HDR Color Wheels and Hue/Saturation curves for selective desaturation.

**Nodes**: Primary Correction → Color Wheels → Curves → HDR  
**Key Parameters**: Saturation 35, Contrast 1.20, Teal Shadows, Orange Highlights

### 3. Cinematic Bottom Masking & Exposure Grading (DFHQC0cuy9-)
Gradient mask on lower frame for moody look with warm highlight tint.

**Nodes**: Primary Grade → Power Window Mask → Color Balance  
**Key Parameters**: Low Exposure on Mask, High Contrast, High Feathering, Desaturated Highlights

## Common Workflow

1. **Balance First**: Primary correction for exposure/contrast baseline
2. **Split Tone**: Lift → Teal, Gain → Orange (Color Wheels)
3. **Refine**: Curves for midtone control, HDR for highlight/shadow detail
4. **Isolate**: Power Windows for subject emphasis
5. **Focus**: Vignette or gradient mask for compositional guidance

## Pro Tips

- **Desaturate mids** for that cinematic "film" density
- **Feather heavily** on Power Windows (0.5-1.0) for invisible transitions
- **Use HDR tools** for highlight rolloff without clipping
- **Match highlight tint** to practical lights in scene (street lamps, sunset)