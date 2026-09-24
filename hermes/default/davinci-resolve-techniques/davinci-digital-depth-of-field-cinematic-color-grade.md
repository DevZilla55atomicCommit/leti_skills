---
name: davinci-digital-depth-of-field-cinematic-color-grade
description: DaVinci Resolve technique: Digital Depth of Field & Cinematic Color Grade from Instagram Reel C_fOMoCIICp
category: creative/davinci-resolve-techniques
tags: ["cinematic", "depth of field", "fusion", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_fOMoCIICp"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Digital Depth of Field & Cinematic Color Grade

**Source:** Instagram Reel `C_fOMoCIICp` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Digital Depth of Field & Cinematic Color Grade](C_fOMoCIICp.gif)

## Node Graph Structure

- MediaIn
- Background
- Blur
- Merge

## Parameters

- **Blur Radius**: 0.65
- **Softness**: 0.5
- **Contrast**: 1.1

## Steps to Reproduce in DaVinci Resolve

1. Import clip and go to the Fusion page
2. Add a Background node and a Blur node
3. Use a Magic Mask or Rotoscine to isolate the subject from the background
4. Apply a Gaussian Blur to the background layer to create shallow depth
5. Merge the isolated subject back over the blurred background
6. Go to the Color page to adjust skin tones, saturation, and contrast

## Tags
`cinematic`, `depth of field`, `fusion`, `masking`
