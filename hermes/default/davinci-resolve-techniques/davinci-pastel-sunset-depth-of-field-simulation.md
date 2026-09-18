---
name: davinci-pastel-sunset-depth-of-field-simulation
description: DaVinci Resolve technique: Pastel Sunset & Depth of Field Simulation from Instagram Reel C3NxPWZx5I8
category: creative/davinci-resolve-techniques
tags: ["cinematic", "sunset", "color-grading", "depth-of-field", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3NxPWZx5I8"
collection: "Cinematic"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Pastel Sunset & Depth of Field Simulation

**Source:** Instagram Reel `C3NxPWZx5I8` (Cinematic)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Pastel Sunset & Depth of Field Simulation](C3NxPWZx5I8.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Blur

## Parameters

- **lift_tint**: Magenta/Blue
- **midtone_tint**: Orange/Pink
- **saturation**: +15
- **lens_blur_radius**: Variable based on f-stop simulation

## Steps to Reproduce in DaVinci Resolve

1. Apply a Teal and Orange-inspired grade using Color Wheels to enhance the sunset pinks.
2. Use Curves to lift the Midtones toward pink and the Shadows toward a slight blue/purple.
3. Increase saturation to make the sunset colors pop.
4. To simulate the different f-stops, use a Power Window/Mask to isolate the background and apply Gaussian Blur (for the F/2.8 look).
5. Ensure the subject remains sharp by masking them out of the effect.

## Tags
`cinematic`, `sunset`, `color-grading`, `depth-of-field`
