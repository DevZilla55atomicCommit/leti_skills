---
name: davinci-artificial-depth-of-field-selective-focus-bokeh
description: DaVinci Resolve technique: Artificial Depth of Field / Selective Focus Bokeh from Instagram Reel C6wN1b7x-en
category: creative/davinci-resolve-techniques
tags: ["bokeh", "selective focus", "depth of field", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6wN1b7x-en"
collection: "Footage_Collection"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Artificial Depth of Field / Selective Focus Bokeh

**Source:** Instagram Reel `C6wN1b7x-en` (Footage_Collection)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Artificial Depth of Field / Selective Focus Bokeh](C6wN1b7x-en.gif)

## Node Graph Structure

- MediaIn
- Gaussian Blur
- Color Correct
- MediaOut

## Parameters

- **Blur Radius**: 50.0
- **Softness**: 0.5
- **Mask Feathering**: 2.0

## Steps to Reproduce in DaVinci Resolve

1. Bring the clip into the Fusion page.
2. Add a Gaussian Blur node connected to the MediaIn node.
3. Increase the Blur Radius to significantly blur the background and foreground elements.
4. Create a Polygon Mask and draw it carefully around the flower and the specific rail section.
5. Invert the mask so the blur is applied everywhere except the flower and the rail.
6. Adjust the mask feathering to create a natural-looking transition between the sharp and blurred areas.
7. Add a Color Correct node to enhance the warm oranges and saturation of the flower.

## Tags
`bokeh`, `selective focus`, `depth of field`, `masking`
