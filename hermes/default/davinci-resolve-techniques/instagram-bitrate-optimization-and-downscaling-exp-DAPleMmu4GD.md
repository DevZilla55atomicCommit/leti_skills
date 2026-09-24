---
name: instagram-bitrate-optimization-and-downscaling-exp-DAPleMmu4GD
description: Instagram Bitrate Optimization and Downscaling Export - DaVinci Resolve
  technique from Instagram Reel DAPleMmu4GD
category: davinci-resolve
tags:
- instagram
- social media
- bitrate
- downscaling
- export settings
resolve_page: Deliver
node_graph_type: serial
difficulty: beginner
key_nodes:
- Source Clip
- Export Settings
parameters:
  Resolution: 1920x1080
  Frame Rate: 30 or 60 fps
  Bitrate: Restrict to 10,000 Kbps or lower
  Encoder: H.264 or HEVC
steps_to_reproduce:
- Create a timeline set to 1920x1080 (1080p)
- Import 4K footage into the timeline
- Go to the Deliver page
- Select the H.264 preset
- Set Resolution to Custom 1920x1080
- Under Quality, change from Automatic to Restrict to Bitrate
- Set the bitrate between 8000 and 12000 Kbps to prevent Instagram compression
- Check Use when encoding if using HEVC
- Add to Render Queue and Render All
source_reel_id: DAPleMmu4GD
---
# Instagram Bitrate Optimization and Downscaling Export

**Source Reel:** DAPleMmu4GD
**Resolve Page:** Deliver
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel DAPleMmu4GD.

## Key Nodes
- Source Clip
- Export Settings

## Parameters
Resolution: 1920x1080
Frame Rate: 30 or 60 fps
Bitrate: Restrict to 10,000 Kbps or lower
Encoder: H.264 or HEVC


## Steps to Reproduce
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
instagram, social media, bitrate, downscaling, export settings
