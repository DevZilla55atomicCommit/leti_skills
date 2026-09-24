---
name: HDR Color Mapping for Social
description: DaVinci Resolve technique from Instagram Reel DEploZ8IT9M
trigger: "hdr color mapping for social"
page: Color
difficulty: intermediate
tags: ['HDR', 'Color Grading', 'Instagram', 'Resolve', 'Color Grading']
video_id: DEploZ8IT9M
source: instagram-reel
updated: 2026-07-28T17:31:25.041035
---

# HDR Color Mapping for Social

**Source:** Instagram Reel `DEploZ8IT9M`  
**Resolve Page:** Color  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- HDR Color Palette
- HDR Wheels
- Color Compressor

## Parameters
- **HDR Tone Mapping:** Rec.709
- **HDR Gamut:** Rec.709
- **Highlights:** Adjust to prevent clipping
- **Shadows:** Adjust to maintain detail

## Steps to Reproduce
1. Set project color management to DaVinci Wide Gamut Intermediate to Rec.709
2. Add an HDR Color Palette node to the end of the chain
3. Use the HDR Highlights wheel to recover detail in the sunset
4. Use the HDR Shadows wheel to lift detail in the snowy mountain crevices
5. Apply a Color Compressor to prevent oversaturation and clipping after Instagram compression
6. Export using H.264 with a high bitrate optimized for mobile upload

## Tags
- #HDR
- #Color Grading
- #Instagram
- #Resolve
- #Color Grading
