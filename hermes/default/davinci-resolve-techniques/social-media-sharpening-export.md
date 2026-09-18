---
name: social-media-sharpening-export
description: High-quality export settings for Instagram Reels, TikTok, YouTube Shorts — vertical 1080x1920, high bitrate (20-30 Mbps), sharpening for compression resilience, and deliver page optimization in DaVinci Resolve.
trigger: User exporting vertical video for social media (Reels, TikTok, Shorts) and wants maximum quality after platform compression
category: davinci-resolve-deliver
tags:
  - export
  - deliver
  - instagram
  - tiktok
  - reels
  - shorts
  - vertical
  - sharpening
  - bitrate
  - h264
  - h265
parameters:
  - name: resolution
    description: Vertical video resolution
    default: "1080x1920 (9:16)"
    type: string
  - name: codec
    description: Video codec for best compatibility/quality
    default: "H.264 (Main/High Profile) or H.265/HEVC"
    type: string
  - name: bitrate_mode
    description: Bitrate control mode
    default: "Restrict to (CBR-like)"
    type: string
  - name: bitrate_value
    description: Target bitrate for quality headroom
    default: "20,000-30,000 kbps (20-30 Mbps)"
    type: string
  - name: frame_rate
    description: Match timeline frame rate
    default: "24, 30, or 60 fps (match source)"
    type: string
  - name: sharpen_amount
    description: Pre-export sharpening for compression
    default: "Amount 20-40, Radius 0.5-0.7, Threshold 0-5"
    type: string
  - name: color_space
    description: Output color space
    default: "Rec.709 / sRGB (for social media)"
    type: string
steps:
  - step: "Timeline: Set to 1080x1920 (9:16) — Project Settings → Master Settings → Timeline Resolution"
  - step: "Color Page: Add final serial node → Sharpen tool (Amount 20-40, Radius 0.5-0.7) for compression resilience"
  - step: "Color Page: Optional — Midtone Detail +5 to +15 for texture pop"
  - step: "Deliver Page: Select 'Custom Export' or 'H.264/H.265' preset"
  - step: "Format: QuickTime (.mov) or MP4 — MP4 preferred for Instagram"
  - step: "Codec: H.264 (High Profile, Level 5.0/5.1) or H.265/HEVC (Main 10)"
  - step: "Resolution: 1080x1920 — ensure 'Stretch frame to fit' OFF, use 'Crop' for letterbox"
  - step: "Quality: 'Restrict to' → 25,000-30,000 kbps (Instagram recompresses to ~3-5 Mbps)"
  - step: "Advanced: Keyframe Interval = Frame Rate (e.g., 30 for 30fps), GOP Closed"
  - step: "Audio: AAC, 48kHz, 320 kbps stereo"
  - step: "Render: 'Add to Render Queue' → 'Render All' — verify output in media player"
difficulty: beginner
resolve_page: Deliver
node_graph_type: serial
key_nodes:
  - Deliver Page
  - Render Settings
  - Sharpen (Color Page final node)
  - Midtone Detail (Color Page)
source_techniques:
  - video_id: DaUiQZsi4Nv
    technique_name: Optimized Export Settings for Video
    tags: [davinci resolve, export, tutorial, video editing]
  - video_id: DLo8aPeJZRp
    technique_name: High-Quality Social Media Export Settings
    tags: [export, davinci-resolve, social-media, quality]
  - video_id: DFskyYxTwN7
    technique_name: High-Bitrate Crisp Export for Instagram Reels
    tags: [davinci resolve, instagram reels, social media, video editing, export settings]
  - video_id: DCHcJ2DOzlb
    technique_name: Social Media Sharpening & Detail Recovery
    tags: [social-media, sharpening, color-grading, optimization]
---

# Social Media Export & Sharpening (Reels/TikTok/Shorts)

Complete Deliver page workflow for vertical social media — maximum quality survives platform recompression. Includes pre-export sharpening strategy for Instagram/TikTok/YouTube Shorts.

## When to Use
- Instagram Reels (1080×1920, 30fps max)
- TikTok (1080×1920, 30/60fps)
- YouTube Shorts (1080×1920, 60fps)
- Any vertical social video delivery

---

## The Core Problem
| Platform | Upload Spec | Recompresses To | Your Strategy |
|----------|-------------|-----------------|---------------|
| **Instagram Reels** | 1080×1920, 30fps, H.264 | ~3-5 Mbps, heavy quant | **Overshoot bitrate 5-10x** |
| **TikTok** | 1080×1920, 30/60fps | ~4-6 Mbps | High bitrate + sharpen |
| **YouTube Shorts** | 1080×1920, 60fps | ~8-12 Mbps | Highest bitrate viable |

**Rule**: Upload at **20-30 Mbps** → Platform compresses to 3-8 Mbps → Your detail survives.

---

## Timeline Setup (Before Color/Deliver)

**Project Settings → Master Settings**:
| Setting | Value |
|---------|-------|
| **Timeline Resolution** | 1080 × 1920 (Custom) |
| **Timeline Frame Rate** | 30 fps (Reels/TikTok) or 60 fps (Shorts) |
| **Pixel Aspect Ratio** | Square (1.0) |
| **Color Science** | DaVinci YRGB Color Managed |
| **Color Space** | Rec.709 (sRGB) for social; DaVinci Wide Gamut for HDR |

**Safe Zones** (for UI overlay clearance):
- **Top 15%**: TikTok caption/username
- **Bottom 25%**: Reels caption, likes, comments, share
- **Center 60%**: Critical content safe area

---

## Pre-Export Sharpening (Color Page — Final Node)

**Add Serial Node at END of grade** (after all color, before output):

### Sharpen Tool Settings
| Parameter | Value | Why |
|-----------|-------|-----|
| **Amount** | 20-40 | Boost edge contrast |
| **Radius** | 0.5-0.7 | Fine detail, not halos |
| **Threshold** | 0-5 | Ignore noise, sharpen edges |
| **Mode** | Luminance Only | Avoid color fringing |

### Midtone Detail (Alternative/Additional)
| Parameter | Value |
|-----------|-------|
| **Midtone Detail** | +5 to +15 |
| **Radius** | 15-25 |
| **Threshold** | 0.02-0.05 |

> **From DCHcJ2DOzlb**: "Sharpen Amount 20-40, Radius 0.67, Midtone Detail +1.5, Contrast +0.05 — compensates for Instagram compression flattening"

### Qualifier Mask (Protect Skin/Noise)
- Qualifier → Select skin tones / noisy shadows
- **Invert** → Apply sharpen ONLY to non-skin/detail areas
- Prevents "crunchy" skin, noise amplification

---

## Deliver Page Settings (Custom Export)

### Format & Codec
| Setting | Recommended | Notes |
|---------|-------------|-------|
| **Format** | MP4 | Best compatibility |
| **Codec** | H.264 (High Profile) | Universal; H.265 for TikTok/Shorts if supported |
| **Profile** | High / Level 5.0/5.1 | Level 5.1 = 4K@60, fine for 1080p |
| **Container** | MP4 (not MOV) | Instagram prefers MP4 |

### Video Settings
| Setting | Value |
|---------|-------|
| **Resolution** | 1080 × 1920 |
| **Frame Rate** | Match timeline (30 or 60) |
| **Field Order** | Progressive |
| **Color Space** | Rec.709 / sRGB |
| **Gamma** | sRGB (BT.1886) |

### Bitrate — THE CRITICAL SETTING
| Mode | Setting |
|------|---------|
| **Rate Control** | **Restrict to** (CBR-like) |
| **Bitrate** | **25,000 - 30,000 kbps** (25-30 Mbps) |
| **Min/Max** | Same (if available) |
| **Keyframe Interval** | **Frame Rate value** (30 for 30fps, 60 for 60fps) |
| **GOP** | Closed GOP |

> **From DLo8aPeJZRp / DFskyYxTwN7**: "Restrict to 20,000-30,000 kbps — prevents compression artifacts"

### Advanced Encoding (If Available)
| Setting | Value |
|---------|-------|
| **Entropy Coding** | CABAC |
| **B-Frames** | 2-3 |
| **Ref Frames** | 3-4 |
| **Adaptive Quant** | On |
| **Lookahead** | On (if hardware encoder) |

### Audio Settings
| Setting | Value |
|---------|-------|
| **Codec** | AAC |
| **Sample Rate** | 48 kHz |
| **Bitrate** | 320 kbps |
| **Channels** | Stereo |

---

## Render Queue & Verification

**Render Settings**:
- **Individual Clips**: OFF (single file)
- **File Naming**: Custom — `ProjectName_Reels_YYYYMMDD`
- **Destination**: Fast SSD (not external HDD)

**After Render — Verify**:
1. **Open in QuickTime/VLC** — check for artifacts, sync
2. **Scrub fast** — look for macroblocking on motion
3. **Check file size** — ~15-25 MB for 15s @ 25 Mbps
4. **Upload test** — private post → check quality after processing

---

## Platform-Specific Cheatsheets

### Instagram Reels
| Setting | Value |
|---------|-------|
| Resolution | 1080×1920 |
| Max Duration | 90 sec |
| Frame Rate | 30 fps |
| Bitrate Upload | 25-30 Mbps |
| Format | MP4, H.264 |
| Audio | AAC 48kHz 320kbps |

### TikTok
| Setting | Value |
|---------|-------|
| Resolution | 1080×1920 |
| Max Duration | 10 min (3 min typical) |
| Frame Rate | 30 or 60 fps |
| Bitrate Upload | 25-30 Mbps |
| Format | MP4, H.264 or H.265 |
| Audio | AAC 48kHz |

### YouTube Shorts
| Setting | Value |
|---------|-------|
| Resolution | 1080×1920 |
| Max Duration | 60 sec |
| Frame Rate | 60 fps preferred |
| Bitrate Upload | 30-40 Mbps |
| Format | MP4, H.264/H.265 |
| Audio | AAC 48kHz 320kbps |

---

## Common Pitfalls

| Mistake | Result | Fix |
|---------|--------|-----|
| Bitrate 5-10 Mbps | Muddy after recompress | **25-30 Mbps minimum** |
| MOV container | IG processing fail | **Use MP4** |
| 4K upload | Downscale artifacts | **Render 1080p native** |
| No sharpening | Soft after compress | **Sharpen node 20-40** |
| Sharpen on skin | Crunchy faces | **Qualifier mask skin** |
| 24fps timeline | Motion judder on 30/60 | **Match platform fps** |
| Rec.2020 color | Washed out on phone | **Rec.709/sRGB only** |

---

## Source Techniques Summary

| Technique | Key Insight |
|-----------|-------------|
| **DaUiQZsi4Nv** | Deliver Page → QuickTime/H.264 → 1920x1080 → 24fps → Auto Profile |
| **DLo8aPeJZRp** | H.264/MP4 → 1080x1920 → Restrict Bitrate 20-30 Mbps → Match Timeline FPS |
| **DFskyYxTwN7** | Vertical 1080x1920 → H.264 → Restrict 20,000+ kbps → Max Quality render |
| **DCHcJ2DOzlb** | Sharpen 20-40, Radius 0.67, Midtone Detail +1.5 → compensates IG compression |

---

## Related Skills
- `teal-orange-cinematic-grade` — grade before export
- `skin-tone-portrait-grade` — protect skin from sharpening
- `hdr-social-media-grade` — HDR→SDR conversion for social
- `gimbal-automotive-cinematic-grade` — car content export
- `beginner-color-correction-basics` — foundation before sharpening