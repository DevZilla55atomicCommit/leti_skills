---
name: davinci-instagram-reel-workflow
description: Complete Instagram Reel creation workflow in DaVinci Resolve - from import through color, edit, effects, and export optimized for Instagram vertical format (9:16).
trigger: Instagram Reel, vertical video, 9:16, social media export, DaVinci Resolve Reels
steps:
  - "Set project to 1080x1920 (9:16) timeline resolution"
  - "Import Reel footage to Media Pool"
  - "Create timeline matching project settings (1080x1920, 30fps or 60fps)"
  - "Edit page: Cut clips to beat/music, add transitions"
  - "Color page: Apply color correction + LUT for consistent look"
  - "Fusion page: Add text overlays, lower thirds, animated elements"
  - "Fairlight page: Mix audio, add music, voiceover, sound effects"
  - "Deliver page: Export using Instagram preset (H.264, 1080x1920, <100MB)"
parameters:
  - name: timeline_resolution
    type: string
    description: Timeline resolution (width x height)
    default: "1080x1920"
    required: true
  - name: frame_rate
    type: number
    description: Frame rate for Instagram (30 or 60 fps)
    default: 30
  - name: lut_file
    type: string
    description: Path to creative LUT for consistent look
  - name: music_track
    type: string
    description: Path to background music file
  - name: export_bitrate
    type: number
    description: Target bitrate in Mbps (Instagram max ~10-12 Mbps)
    default: 10
tags:
  - instagram-reel
  - vertical-video
  - 9:16
  - social-media
  - davinci-resolve
  - edit-page
  - color-page
  - fusion-page
  - fairlight-page
  - deliver-page
category: davinci-resolve-social-media
---

# DaVinci Resolve Instagram Reel Workflow

End-to-end workflow for creating professional Instagram Reels in DaVinci Resolve, covering all pages (Edit, Color, Fusion, Fairlight, Deliver) optimized for 9:16 vertical format.

## Project Setup

### Timeline Settings
```
Resolution: 1080 × 1920 (9:16 vertical)
Frame Rate: 30 fps (or 60 fps for smooth motion)
Color Space: Rec.709 Gamma 2.4 (or DaVinci YRGB Color Managed)
```

### Project Settings (File → Project Settings)
- **Master Settings** → Timeline Resolution: 1080x1920
- **Color Management** → Color Science: DaVinci YRGB Color Managed
- **Color Management** → Output Color Space: Rec.709 Gamma 2.4

## Page-by-Page Workflow

### 1. Media Page / Cut Page - Import & Organize
```
1. Drag footage to Media Pool
2. Create bins: "Footage", "Music", "Graphics", "Exports"
3. Right-click clips → "Clip Attributes" → Verify frame rate matches timeline
4. Use "Smart Bins" for auto-organization by metadata
```

### 2. Edit Page - Assembly & Timing
```
Timeline Structure (Video Tracks):
V1: Main footage (A-roll)
V2: B-roll / overlays
V3: Text / Graphics (from Fusion)
V4: Transitions / Effects

Key Techniques from Batch:
- Cut to beat: Use waveform view, add edits at transients (B key)
- Jump cuts: Remove silence/pauses (Blade tool + Delete + Ripple Delete)
- Speed ramping: Retime controls (Cmd+R) → Speed points for ramping
- Transitions: Smooth Cut, Cross Dissolve, Push (vertical direction)
```

**Instagram-Specific Editing Tips:**
- First 3 seconds = hook (front-load best content)
- Vertical-safe framing: Keep subjects in center 70% of frame
- Text safe zone: Center 80% (avoid top/bottom UI overlap)

### 3. Color Page - Consistent Look
```
Node Graph (Serial):
Node 1: Primary Correction (Color Wheels - match all clips)
Node 2: Creative LUT (Key Output Gain: 0.5-0.7)
Node 3: Skin Tone Protection (Hue vs Sat curve)
Node 4: Vignette / Edge Darken (Power Window)

Batch Matching:
1. Grade hero clip fully
2. Select all clips → Right-click → "Apply Grade from Clip" (or Middle-click drag)
3. Fine-tune each clip's Node 1 for exposure/WB differences
```

**Recommended LUTs for Reels:**
- Kodak 2383 / Fuji 3510 (film look)
- Teal-Orange (cinematic)
- Custom brand LUT

### 4. Fusion Page - Motion Graphics
```
Common Reel Elements:
- Lower Thirds: Text (name/handle)
- Animated Hashtags
- Progress Bar (30s/60s/90s timer)
- Swipe Transitions (custom Fusion macros)
- Call-to-Action Buttons (Follow, Link in Bio)

Text+ Template Workflow:
1. Create Text+ template with animations
2. Publish parameters (Text, Color, Position)
3. Save as Macro (.setting) → Reuse across projects
4. Use "Instagram Safe Zone" guides (View → Overlay → Safe Areas)
```

### 5. Fairlight Page - Audio Mix
```
Track Layout:
A1: Dialogue/Voiceover (mono)
A2: Music (stereo)
A3: Sound Effects (stereo)
A4: Ambience/Room tone

Processing Chain (per track):
Dialogue: Noise Reduction → EQ (high-pass 100Hz) → Compressor (3:1, -3dB) → Limiter
Music: EQ (duck under dialogue) → Sidechain Compressor (keyed to dialogue)
Master: Loudness Meter (Target: -14 LUFS integrated for Instagram)
```

**Instagram Audio Specs:**
- AAC-LC, 44.1kHz or 48kHz
- Stereo
- Max 128 kbps (Instagram re-encodes)

### 6. Deliver Page - Export Settings
```
Instagram Reel Preset:
Format: MP4 (H.264)
Codec: H.264 High Profile
Resolution: 1080 × 1920
Frame Rate: 30 fps
Bitrate: 8-12 Mbps (CBR or VBR 1-pass)
Audio: AAC, 48kHz, 128 kbps
Max Duration: 90 seconds
File Size: < 100 MB (ideally < 50 MB)

Render Settings:
- "Use Optimized Media" OFF
- "Use Render Cached Images" ON
- "Force Sizing to Timeline Resolution" ON
```

## Batch Export for Series

```python
# Python script concept (use in Resolve Scripting)
timelines = project.GetTimelineCount()
for i in range(timelines):
    tl = project.GetTimelineByIndex(i+1)
    project.SetCurrentTimeline(tl)
    project.AddRenderJob({
        "TargetDir": "/path/to/exports",
        "CustomName": tl.GetName(),
        "Format": "mp4",
        "Codec": "H264",
        "Width": 1080,
        "Height": 1920,
        "FrameRate": 30,
        "BitRate": 10000  # kbps
    })
project.StartRendering()
```

## Time-Saving Templates

### Project Template (.drp)
1. Set up project with all settings above
2. Create empty timeline with track structure
3. Add Fusion text templates to Media Pool
4. Save as Project Template: File → Export → Project Template

### Render Preset
1. Deliver page → Configure settings above
2. Click "Save Preset" → Name: "Instagram Reel 1080x1920"
3. Available in Render Settings dropdown

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Horizontal footage in vertical timeline | Edit → Transform → Rotation: 90° + Zoom to fill |
| Black bars top/bottom | Inspector → Cropping → Crop Top/Bottom OR use Transform Zoom |
| Text cut off on phone | Keep text in center 80% (Title Safe overlay) |
| Audio too quiet | Fairlight → Master Bus → Gain +6dB, check Loudness Meter |
| Color shifts on upload | Export Rec.709 Gamma 2.4, no HDR, tag as SDR |

## Related Skills

- `davinci-color-correction-lut` - Color grading details
- `davinci-fusion-motion-graphics` - Text templates, animations
- `davinci-fairlight-audio-mix` - Audio processing chains
- `davinci-deliver-optimization` - Export settings for platforms