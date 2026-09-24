---
name: davinci-selective-focus-bokeh-warm-cinematic-grade
description: DaVinci Resolve technique: Selective Focus Bokeh & Warm Cinematic Grade from Instagram Reel C69CkokPVBr
category: creative/davinci-resolve-techniques
tags: ["bokeh", "depth of field", "cinematic", "selective-focus", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C69CkokPVBr"
collection: "Footage_Collection"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Focus Bokeh & Warm Cinematic Grade

**Source:** Instagram Reel `C69CkokPVBr` (Footage_Collection)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Selective Focus Bokeh & Warm Cinematic Grade](C69CkokPVBr.gif)

## Node Graph Structure

- MediaIn
- Blur
- Mask
- ColorCorrect

## Parameters

- **Blur Radius**: High
- **Mask Edge Softness**: High
- **Temperature**: Warm (Yellow/Orange)
- **Saturation**: Increased Midtones

## Steps to Reproduce in DaVinci Resolve

1. Import clip into the Fusion page
2. Add a Gaussian Blur node and increase the radius to blur the background
3. Create an Ellipse Mask and draw it carefully around the flower
4. Invert the mask so the blur is applied everywhere except the flower
5. Adjust the mask feathering to create a natural transition between the sharp and blurred areas
6. Add a Color Correct node to enhance the warm oranges and saturation

## Tags
`bokeh`, `depth of field`, `cinematic`, `selective-focus`
