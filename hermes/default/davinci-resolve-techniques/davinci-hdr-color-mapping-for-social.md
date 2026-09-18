---
name: davinci-hdr-color-mapping-for-social
description: DaVinci Resolve technique: HDR Color Mapping for Social from Instagram Reel DEploZ8IT9M
category: creative/davinci-resolve-techniques
tags: ["HDR", "Color Grading", "Instagram", "Resolve", "Color Grading", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DEploZ8IT9M"
collection: "Export_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# HDR Color Mapping for Social

**Source:** Instagram Reel `DEploZ8IT9M` (Export_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![HDR Color Mapping for Social](DEploZ8IT9M.gif)

## Node Graph Structure

- HDR Color Palette
- HDR Wheels
- Color Compressor

## Parameters

- **HDR Tone Mapping**: Rec.709
- **HDR Gamut**: Rec.709
- **Highlights**: Adjust to prevent clipping
- **Shadows**: Adjust to maintain detail

## Steps to Reproduce in DaVinci Resolve

1. Set project color management to DaVinci Wide Gamut Intermediate to Rec.709
2. Add an HDR Color Palette node to the end of the chain
3. Use the HDR Highlights wheel to recover detail in the sunset
4. Use the HDR Shadows wheel to lift detail in the snowy mountain crevices
5. Apply a Color Compressor to prevent oversaturation and clipping after Instagram compression
6. Export using H.264 with a high bitrate optimized for mobile upload

## Tags
`HDR`, `Color Grading`, `Instagram`, `Resolve`, `Color Grading`
