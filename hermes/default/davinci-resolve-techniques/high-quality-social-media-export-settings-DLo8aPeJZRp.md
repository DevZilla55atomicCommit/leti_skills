---
name: high-quality-social-media-export-settings
description: 'DaVinci Resolve technique: High-Quality Social Media Export Settings
  from Instagram Reel DLo8aPeJZRp'
category: davinci-resolve
tags:
- export
- davinci-resolve
- social-media
- quality
- edit
- beginner
version: 1.0.0
source_reel_id: DLo8aPeJZRp
resolve_page: Edit
node_graph_type: serial
key_nodes:
- Deliver Page
- Render Settings
parameters:
  Format: H.264
  Codec: MP4
  Resolution: 1080x1920
  Frame Rate: Match Timeline
  Bitrate Limit: Restrict to
  BitrateValue: 20000-30000 kbps
steps_to_reproduce:
- Go to the Deliver page
- Select Custom Export
- Set Format to H.264 and Container to MP4
- Ensure Resolution is set to 1080x1920 for vertical video
- Under Encoding, find Quality settings
- Restrict Bitrate to 20000-30000 kbps for high detail without massive files
- Add to Render Queue and Render
difficulty: beginner
---
# High-Quality Social Media Export Settings

**Source Reel:** DLo8aPeJZRp
**Resolve Page:** Edit
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel DLo8aPeJZRp.

## Key Nodes
- Deliver Page
- Render Settings

## Parameters
Format: H.264
Codec: MP4
Resolution: 1080x1920
Frame Rate: Match Timeline
Bitrate Limit: Restrict to
BitrateValue: 20000-30000 kbps


## Steps to Reproduce
1. Go to the Deliver page
2. Select Custom Export
3. Set Format to H.264 and Container to MP4
4. Ensure Resolution is set to 1080x1920 for vertical video
5. Under Encoding, find Quality settings
6. Restrict Bitrate to 20000-30000 kbps for high detail without massive files
7. Add to Render Queue and Render

## Tags
export, davinci-resolve, social-media, quality
