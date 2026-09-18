---
name: davinci-instagram-bitrate-optimization-and-downscaling-export
description: DaVinci Resolve technique: Instagram Bitrate Optimization and Downscaling Export from Instagram Reel DAPleMmu4GD
category: creative/davinci-resolve-techniques
tags: ["instagram", "social media", "bitrate", "downscaling", "export settings", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DAPleMmu4GD"
collection: "Export_Videos"
resolve_page: "Deliver"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Instagram Bitrate Optimization and Downscaling Export

**Source:** Instagram Reel `DAPleMmu4GD` (Export_Videos)  
**Page:** Deliver | **Graph:** serial | **Difficulty:** beginner

![Instagram Bitrate Optimization and Downscaling Export](DAPleMmu4GD.gif)

## Node Graph Structure

- Source Clip
- Export Settings

## Parameters

- **Resolution**: 1920x1080
- **Frame Rate**: 30 or 60 fps
- **Bitrate**: Restrict to 10,000 Kbps or lower
- **Encoder**: H.264 or HEVC

## Steps to Reproduce in DaVinci Resolve

1. Create a timeline set to 1920x1080 (1080p)
2. Import 4K footage into the timeline
3. Go to the Deliver page
4. Select the H.264 preset
5. Set Resolution to Custom 1920x1080
6. Under Quality, change from Automatic to Restrict to Bitrate
7. Set the bitrate between 8000 and 12000 Kbps to prevent Instagram compression
8. Check Use when encoding if using HEVC
9. Add to Render Queue and Render All

## Tags
`instagram`, `social media`, `bitrate`, `downscaling`, `export settings`
