---
name: hdr-color-mapping-for-social
description: 'DaVinci Resolve technique: HDR Color Mapping for Social from Instagram
  Reel DEploZ8IT9M'
category: davinci-resolve
tags:
- HDR
- Color Grading
- Instagram
- Resolve
- Color Grading
- color
- intermediate
version: 1.0.0
source_reel_id: DEploZ8IT9M
resolve_page: Color
node_graph_type: serial
key_nodes:
- HDR Color Palette
- HDR Wheels
- Color Compressor
parameters:
  HDR Tone Mapping: Rec.709
  HDR Gamut: Rec.709
  Highlights: Adjust to prevent clipping
  Shadows: Adjust to maintain detail
steps_to_reproduce:
- Set project color management to DaVinci Wide Gamut Intermediate to Rec.709
- Add an HDR Color Palette node to the end of the chain
- Use the HDR Highlights wheel to recover detail in the sunset
- Use the HDR Shadows wheel to lift detail in the snowy mountain crevices
- Apply a Color Compressor to prevent oversaturation and clipping after Instagram
  compression
- Export using H.264 with a high bitrate optimized for mobile upload
difficulty: intermediate
---
# HDR Color Mapping for Social

**Source Reel:** DEploZ8IT9M
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel DEploZ8IT9M.

## Key Nodes
- HDR Color Palette
- HDR Wheels
- Color Compressor

## Parameters
HDR Tone Mapping: Rec.709
HDR Gamut: Rec.709
Highlights: Adjust to prevent clipping
Shadows: Adjust to maintain detail


## Steps to Reproduce
1. Set project color management to DaVinci Wide Gamut Intermediate to Rec.709
2. Add an HDR Color Palette node to the end of the chain
3. Use the HDR Highlights wheel to recover detail in the sunset
4. Use the HDR Shadows wheel to lift detail in the snowy mountain crevices
5. Apply a Color Compressor to prevent oversaturation and clipping after Instagram compression
6. Export using H.264 with a high bitrate optimized for mobile upload

## Tags
HDR, Color Grading, Instagram, Resolve, Color Grading
