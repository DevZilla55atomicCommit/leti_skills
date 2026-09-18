---
name: davinci-drone-cinematography
description: Drone footage workflows — cinematic drone grading, LUT mapping, depth of field simulation, aerial color correction, drone moves
trigger: Use when grading drone/aerial footage, applying cinematic LUTs, simulating depth of field, or creating drone move tutorials
steps:
  - name: Cinematic Drone Shot with DaVinci Resolve
    description: Color grade drone footage with cinematic LUT mapping
    resolve_page: Color|Edit|Fusion|Fairlight
    difficulty: intermediate
    key_nodes: [Color Correction Node, LUT Mapping Node]
    parameters:
      Color Correction Node:
        saturation: "100%"
        contrast: "50%"
      LUT Mapping Node:
        input_lut: "Cinematic Drone LUT"
        output_lut: "Final Output LUT"
    steps:
      - Import footage into DaVinci Resolve
      - Apply color correction using the Color Correction Node with desired saturation and contrast values
      - Apply cinematic drone LUT via LUT Mapping Node
      - Fine-tune exposure and white balance after LUT
      - Protect highlights with curves if needed
    tags: [drone cinematography, color grading, da vinci resolve techniques, lut, aerial]

  - name: Cinematic Drone Moves Tutorial
    description: Apply cinematic LUT and motion tracking to drone footage
    resolve_page: Color|Edit|Fusion|Fairlight
    difficulty: intermediate
    key_nodes: [Node for Color Correction, Node for Motion Tracking]
    parameters:
      param1: "LUT for Cinematic Look"
      param2: "Motion Tracking Settings"
    steps:
      - Import Drone Footage
      - Apply LUT for Cinematic Look
      - Perform Motion Tracking for stabilization or object tracking
      - Add speed ramps for dynamic moves
    tags: [drone filming, cinematic techniques, lut, motion tracking]

  - name: Best Drone Footage Color Correction
    description: Color correction workflow specifically for drone camera profiles
    resolve_page: Color|Edit|Fusion|Fairlight
    difficulty: intermediate
    key_nodes: [Color Correction, LUT (Look-Up Table)]
    parameters:
      param1: "Adjusting the color balance to enhance the natural colors of the drone footage"
    steps:
      - Import the raw footage into DaVinci Resolve
      - Apply a LUT to match the color profile of the drone camera (D-Log, D-Cinelike, etc.)
      - Adjust white balance for sky/ground separation
      - Use curves to recover highlight detail in sky
      - Add subtle vignette to draw focus to center
    tags: [drone footage, color correction, lut, d-log, d-cinelike]

  - name: Drone Photography Color & Exposure
    description: Adjust color and exposure for drone photography stills/video
    resolve_page: Color|Edit|Fusion|Fairlight
    difficulty: intermediate
    key_nodes: [node1, node2]
    parameters:
      param1: "value1"
    steps:
      - Import footage into DaVinci Resolve
      - Adjust color and exposure settings
      - Apply lens correction if needed
      - Enhance sky and ground separately with qualifiers
    tags: [drone photography, instagram reel, davinci resolve, color, exposure]

  - name: Artificial Depth of Field / Focus Blur (Drone)
    description: Simulate shallow depth of field on drone footage using Magic Mask + Gaussian Blur
    resolve_page: Color
    difficulty: intermediate
    key_nodes: [Gaussian Blur, Magic Mask]
    parameters:
      Blur Radius: "25.0"
      Strength: "1.0"
    steps:
      - Import footage and go to the Color Page
      - Use the Magic Mask to isolate the subject (the drone/foreground object)
      - Create a new node for the background
      - Add a Gaussian Blur or Lens Blur effect to the background node
      - Adjust the blur radius to create a cinematic shallow depth of field
      - Animate mask if subject moves
    tags: [cinematic, drone, depth-of-field, tutorial, magic mask, gaussian blur]

  - name: Teal & Orange Aerial Grade
    description: Classic teal-orange cinematic look for aerial/drone footage
    resolve_page: Color
    difficulty: beginner
    key_nodes: [Primary Wheels, Curves, Hue/Saturation/Luma]
    parameters:
      Saturation: "+15"
      Contrast: "Increased"
      Midtones: "Warm/Orange"
      Shadows: "Teal/Blue"
    steps:
      - Add a primary node to adjust contrast and white balance
      - Use the Color Wheels to push shadows toward teal/blue
      - Use the Offset or Wheels to push midtones/highlights toward a warm orange/yellow
      - Use the Hue/Saturation curve to de-saturate greens if they appear distracting
      - Apply a slight vignette to draw focus to the central island formation
    tags: [color grading, cinematic, aerial, teal-and-orange, drone]

parameters:
  - name: drone_log_profile
    type: string
    description: Drone camera log profile
    default: "D-Log (DJI) / D-Cinelike"
  - name: lut_type
    type: string
    description: LUT for drone footage
    default: "Cinematic Drone / Rec.709"
  - name: blur_radius
    type: number
    description: Gaussian blur radius for fake DOF
    default: 25

tags: [drone, cinematography, aerial, d-log, lut, color grading, depth of field, teal orange, davinci resolve, magic mask]
category: davinci-resolve-drone
---

# DaVinci Resolve Drone Cinematography & Grading

Specialized workflows for drone/aerial footage: log profile handling, cinematic LUTs, fake depth of field, teal-orange aerial looks, and tutorial thumbnail creation.

## Skills Included

1. **Cinematic Drone Shot with DaVinci Resolve** — Color correction + LUT mapping
2. **Cinematic Drone Moves Tutorial** — LUT + motion tracking + speed ramps
3. **Best Drone Footage Color Correction** — Drone log profile (D-Log) handling
4. **Drone Photography Color & Exposure** — Exposure/color for aerial stills/video
5. **Artificial Depth of Field / Focus Blur** — Magic Mask + Gaussian Blur for shallow DOF
6. **Teal & Orange Aerial Grade** — Classic cinematic look for aerial footage

## Quick Reference

| Task | Page | Key Nodes | Difficulty |
|------|------|-----------|------------|
| Drone grade + LUT | Color | Color Correct, LUT Mapping | Intermediate |
| Drone moves tutorial | All | Color Correct, Motion Track | Intermediate |
| D-Log correction | Color | Color Correct, LUT | Intermediate |
| Drone photo edit | Color | Color, Exposure | Intermediate |
| Fake DOF | Color | Magic Mask, Gaussian Blur | Intermediate |
| Teal/Orange aerial | Color | Wheels, Curves, Hue/Sat | Beginner |

## Drone Camera Profiles & LUTs

| Drone | Log Profile | Recommended LUT/Input |
|-------|-------------|----------------------|
| DJI Mavic 3 / Mini 3 Pro / Air 2S | D-Log / D-Log M | DJI D-Log to Rec.709 |
| DJI Mini 2 / Air 2 | D-Cinelike | DJI D-Cinelike to Rec.709 |
| Autel EVO II | A-Log | Autel A-Log to Rec.709 |
| Skydio 2/2+ | Skydio Log | Custom / Rec.709 |
| FPV (GoPro) | GoPro Protune Flat | GoPro CineD to Rec.709 |

## Tips

- **Always shoot in log** (D-Log, D-Cinelike) for maximum dynamic range
- **CST Node workflow**: Camera Log → CST (to Rec.709) → Creative Grade → LUT (optional)
- **Fake DOF on drone**: Magic Mask the foreground subject → invert → blur background
- **Sky recovery**: Use Qualifier (HSL) to select sky → pull highlight detail with curves
- **Green desaturation**: Drone footage often has oversaturated greens; use Hue vs Sat curve
- **Vignette**: Subtle vignette (Power Window → Gradient → Invert) draws eye to center
- **Stabilization**: Use Edit page Stabilize or Fusion Tracker for micro-jitter removal

## Color Page Node Tree for Drone

```
Node 01: CST (D-Log → Rec.709)
Node 02: Primary Balance (WB, Exposure)
Node 03: Sky Recovery (Qualifier + Curves)
Node 04: Creative Look (Teal/Orange or LUT)
Node 05: Fake DOF (Magic Mask + Blur) — if needed
Node 06: Vignette (Power Window)
Node 07: Final Trim (Gain/Offset)
```

## Related Skills

- `davinci-resolve-techniques/davinci-color-grading-fundamentals` — Core color grading
- `davinci-resolve-techniques/davinci-masking-compositing` — Magic Mask, Power Windows
- `davinci-resolve-techniques/davinci-fusion-fairlight-vfx` — Fusion stabilization, comp