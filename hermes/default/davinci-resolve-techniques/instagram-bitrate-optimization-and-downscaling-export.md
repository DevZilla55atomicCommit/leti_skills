---
name: Instagram Bitrate Optimization and Downscaling Export
description: DaVinci Resolve technique from Instagram Reel DAPleMmu4GD
trigger: "instagram bitrate optimization and downscaling export"
page: Deliver
difficulty: beginner
tags: ['instagram', 'social media', 'bitrate', 'downscaling', 'export settings']
video_id: DAPleMmu4GD
source: instagram-reel
updated: 2026-07-28T16:41:35.652938
---

# Instagram Bitrate Optimization and Downscaling Export

**Source:** Instagram Reel `DAPleMmu4GD`  
**Resolve Page:** Deliver  
**Difficulty:** beginner  
**Node Graph Type:** serial

## Key Nodes
- Source Clip
- Export Settings

## Parameters
- **Resolution:** 1920x1080
- **Frame Rate:** 30 or 60 fps
- **Bitrate:** Restrict to 10,000 Kbps or lower
- **Encoder:** H.264 or HEVC

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
- #instagram
- #social media
- #bitrate
- #downscaling
- #export settings
