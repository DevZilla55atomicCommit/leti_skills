---
name: social-media-export-instagram-reels
description: High-quality export settings for Instagram Reels, TikTok, and vertical social media. Covers Deliver page settings, bitrate optimization, H.264/H.265 codecs, and vertical 1080x1920 workflows.
trigger: User wants to export for Instagram Reels, TikTok, YouTube Shorts, or needs high-bitrate vertical video settings.
category: davinci-resolve/deliver-export
tags: [deliver, export, instagram, reels, tiktok, shorts, vertical, h264, h265, bitrate, render-queue, 1080x1920]
steps:
  - name: Optimized Export Settings for Video (DaUiQZsi4Nv)
    description: Standard high-quality H.264 export for general social media
    resolve_page: Deliver
    node_graph_type: serial
    key_nodes: [Deliver Page, Render Queue]
    parameters:
      Format: "QuickTime"
      Codec: "H.264"
      Resolution: "1920x1080"
      Frame_rate: "24 fps"
      Encoding_Profile: "Auto"
    steps:
      - Navigate to the Deliver page (rocket icon) in DaVinci Resolve
      - Select your project name and define file location
      - Set Format to QuickTime
      - Set Video Codec to H.264
      - Ensure Resolution matches your timeline settings
      - Set Encoding Profile to Auto or High
      - Click Add to Render Queue
      - Click Render All from the Render Queue
    difficulty: beginner
    video_id: DaUiQZsi4Nv
    tags: [davinci resolve, export, tutorial, video editing]

  - name: High-Quality Social Media Export Settings (DLo8aPeJZRp)
    description: Custom export with restricted bitrate for vertical 1080x1920 content
    resolve_page: Edit
    node_graph_type: serial
    key_nodes: [Deliver Page, Render Settings]
    parameters:
      Format: "H.264"
      Codec: "MP4"
      Resolution: "1080x1920"
      Frame_Rate: "Match Timeline"
      Bitrate_Limit: "Restrict to"
      BitrateValue: "20000-30000 kbps"
    steps:
      - Go to the Deliver page
      - Select Custom Export
      - Set Format to H.264 and Container to MP4
      - Ensure Resolution is set to 1080x1920 for vertical video
      - Under Encoding, find Quality settings
      - Restrict Bitrate to 20000-30000 kbps for high detail without massive files
      - Add to Render Queue and Render
    difficulty: beginner
    video_id: DLo8aPeJZRp
    tags: [export, davinci-resolve, social-media, quality]

  - name: High-Bitrate Crisp Export for Instagram Reels (DFskyYxTwN7)
    description: Maximum quality vertical export with 20-30Mbps bitrate for Instagram compression survival
    resolve_page: Deliver
    node_graph_type: serial
    key_nodes: [Color Page, Deliver Page, Export Settings]
    parameters:
      format: "MP4/QuickTime"
      codec: "H.264"
      resolution: "1080x1920"
      framerate: "30"
      bitrate: "Restrict to"
      bitrate_value: "20000-30000 kbps"
      encoding: "Native"
    steps:
      - Ensure timeline is 1080x1920 (Vertical Resolution)
      - Go to the Deliver Page
      - Set Format to MP4
      - Set Video Codec to H.264
      - Under Quality, select Restrict to
      - Set the bitrate to 20000 kbps or higher to prevent compression artifacts
      - Enable Use maximum quality when rendering if available
      - Add to Render Queue and Render All
    difficulty: beginner
    video_id: DFskyYxTwN7
    tags: [davinci resolve, instagram reels, social media, video editing, export settings]
parameters:
  - name: Format
    description: Container format - MP4 (recommended) or QuickTime
  - name: Codec
    description: Video codec - H.264 (compatible) or H.265/HEVC (efficient)
  - name: Resolution
    description: Vertical 1080x1920 for Reels/Shorts/TikTok
  - name: Frame_Rate
    description: Match timeline (24/30/60 fps)
  - name: Bitrate_Limit
    description: Restrict to specific bitrate for quality control
  - name: BitrateValue
    description: 20000-30000 kbps for Instagram Reels quality
  - name: Encoding_Profile
    description: Auto, High, or Maximum Quality
tags: [deliver, export, instagram, reels, tiktok, shorts, vertical, h264, h265, bitrate, render-queue, 1080x1920, social-media]
---

# Social Media Export: Instagram Reels, TikTok & Shorts

**Deliver page workflows** for **vertical 1080x1920** content optimized for **Instagram Reels, TikTok, YouTube Shorts**. High-bitrate settings that survive platform recompression.

## Techniques Included

### 1. Optimized Export Settings (DaUiQZsi4Nv)
**Standard high-quality H.264 for general social**

- **Format**: QuickTime / MP4
- **Codec**: H.264
- **Resolution**: 1920x1080 (horizontal) or 1080x1920 (vertical)
- **Frame Rate**: 24/30 fps (match timeline)
- **Profile**: Auto or High
- **Use Case**: General purpose, horizontal content

### 2. High-Quality Social Media Export (DLo8aPeJZRp)
**Custom vertical export with bitrate restriction**

- **Format**: H.264 / MP4
- **Resolution**: **1080x1920** (vertical)
- **Bitrate**: **20,000-30,000 kbps** (restricted)
- **Frame Rate**: Match Timeline
- **Use Case**: Instagram Reels, TikTok, Shorts

### 3. High-Bitrate Crisp Export for Reels (DFskyYxTwN7)
**Maximum quality for Instagram's aggressive compression**

- **Format**: MP4/QuickTime
- **Codec**: H.264
- **Resolution**: 1080x1920
- **Frame Rate**: 30 fps
- **Bitrate**: **20,000-30,000 kbps** (Restrict to)
- **Quality**: "Use maximum quality when rendering" ON
- **Use Case**: Critical quality Reels, portfolio pieces

## Recommended Settings by Platform

| Platform | Resolution | Codec | Bitrate | FPS | Container |
|----------|------------|-------|---------|-----|-----------|
| **Instagram Reels** | 1080x1920 | H.264 | 20-30 Mbps | 30 | MP4 |
| **TikTok** | 1080x1920 | H.264 | 15-25 Mbps | 30 | MP4 |
| **YouTube Shorts** | 1080x1920 | H.264/H.265 | 20-40 Mbps | 30/60 | MP4 |
| **Facebook Reels** | 1080x1920 | H.264 | 15-20 Mbps | 30 | MP4 |

## Deliver Page Workflow

```
1. Timeline: Set to 1080x1920 (File → Project Settings → Master Settings)
2. Deliver Page: Select "Custom Export"
3. Format: H.264 (most compatible) or H.265 (smaller files)
4. Resolution: 1080x1920 (verify!)
5. Quality: "Restrict to" → 25000 kbps
6. Advanced: Enable "Use Maximum Render Quality"
7. Audio: AAC, 48kHz, 320 kbps
8. Add to Render Queue → Render All
```

## Bitrate Guidelines

| Content Type | Bitrate | Notes |
|--------------|---------|-------|
| **Talking head** | 15-20 Mbps | Low motion, efficient |
| **Fast action** | 25-35 Mbps | High motion needs bits |
| **Text/graphics heavy** | 20-30 Mbps | Preserves edges |
| **Cinematic/portfolio** | 30-40 Mbps | Maximum quality |

## Pro Tips

1. **Test upload first** - Private post to check compression
2. **H.265/HEVC** - Smaller files, but check platform support
3. **Color Space** - Rec.709 for SDR, P3 for HDR (Instagram HDR limited)
4. **Audio** - AAC 320kbps, loudness normalized to -14 LUFS
5. **Keyframes** - 1 keyframe per second (GOP 30@30fps)
6. **No B-frames** - Better compatibility, slightly larger

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Blurry upload | Low bitrate | Increase to 25+ Mbps |
| Color shift | Wrong color space | Set timeline to Rec.709 |
| Stuttering | Variable frame rate | Force constant 30fps |
| Audio drift | Sample rate mismatch | 48kHz throughout |
| Black bars | Wrong timeline res | 1080x1920 timeline |

## Quick Export Preset (Save as Preset)

```
Name: "Instagram Reels 1080x1920 High Quality"
Format: MP4
Codec: H.264
Resolution: 1080x1920
Quality: Restrict to 25000 kbps
FPS: 30
Audio: AAC 48kHz 320kbps
Keyframes: Every 30 frames
Max Quality: ON
```