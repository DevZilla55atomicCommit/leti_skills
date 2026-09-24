---
name: davinci-time-lapse-hyperlapse
description: Time-lapse and hyperlapse photography workflows in DaVinci Resolve - from image sequence import to flicker-free rendering, motion blur simulation, and creative speed ramping.
trigger: time-lapse, hyperlapse, timelapse, image sequence, interval photography, DaVinci Resolve timelapse
steps:
  - "Shoot: Intervalometer settings (interval, exposure, focus lock)"
  - "Import: Media Pool → Import image sequence (auto-detect frames)"
  - "Timeline: Create timeline matching sequence frame rate (24/30 fps)"
  - "Edit: Speed change for duration control (Retime Controls)"
  - "Color: Deflicker (Smooth OFX or manual keyframe exposure)"
  - "Color: Add motion blur (Directional Blur OFX or ReelSmart Motion Blur)"
  - "Fusion: Optional camera move (Transform keyframes on zoom/pan)"
  - "Deliver: Render high-bitrate ProRes/DNxHR for archive, H.264 for web"
parameters:
  - name: interval_seconds
    type: number
    description: Seconds between shots
    default: 3
  - name: sequence_frame_rate
    type: number
    description: Timeline frame rate for sequence interpretation
    default: 24
  - name: output_frame_rate
    type: number
    description: Final export frame rate
    default: 30
  - name: deflicker_method
    type: string
    description: Deflickering approach
    enum: ["Smooth OFX", "Manual Keyframes", "LUT Normalization", "External (LRTimelapse)"]
    default: "Smooth OFX"
  - name: motion_blur
    type: boolean
    description: Add synthetic motion blur
    default: true
  - name: camera_move
    type: string
    description: Simulated camera movement type
    enum: ["None", "Slow Pan", "Slow Zoom", "Pan + Zoom", "Parallax (Fusion 3D)"]
    default: "None"
tags:
  - time-lapse
  - hyperlapse
  - timelapse
  - image-sequence
  - interval-photography
  - deflicker
  - motion-blur
  - davinci-resolve
  - fusion
  - retime
category: davinci-resolve-timelapse
---

# DaVinci Resolve Time-Lapse & Hyperlapse Workflow

Complete workflow for creating professional time-lapse and hyperlapse videos in DaVinci Resolve, from image sequence import through deflickering, motion blur, and creative camera moves.

## Shooting Guidelines (Pre-Production)

### Interval Settings by Subject
| Subject | Interval | Duration (for 10s @ 30fps) |
|---------|----------|---------------------------|
| Clouds (fast) | 1-2 sec | 5-10 min |
| Clouds (slow) | 3-5 sec | 15-25 min |
| Sunrise/Sunset | 5-10 sec | 30-60 min |
| Stars/Milky Way | 15-30 sec | 2-4 hours |
| Traffic (day) | 1-2 sec | 5-10 min |
| Traffic (night trails) | 2-4 sec | 10-20 min |
| Construction | 10-30 sec | Hours/Days |
| People/Crowds | 0.5-1 sec | 2-5 min |
| Plant Growth | 5-10 min | Days/Weeks |

### Camera Settings (Critical)
```
Mode: Manual (M) - NO auto exposure
Focus: Manual focus, lock after focusing
White Balance: Fixed Kelvin (e.g., 5600K) - NO auto WB
Aperture: f/8-f/11 (sharpness, depth of field)
Shutter: 1/2 interval (e.g., 2s interval → 1s shutter) for motion blur
ISO: Base ISO (100/200) - NO auto ISO
Format: RAW + JPEG (RAW for grading, JPEG for quick preview)
Battery: Grip / USB-C power / intervalometer with power pass-through
```

## Import & Timeline Setup

### Method 1: Image Sequence Import (Recommended)
```
1. Media Pool → Right-click → "Import Media"
2. Select FIRST image of sequence (e.g., IMG_0001.jpg)
3. Resolve auto-detects sequence → Imports as single clip
4. Clip properties show: "Image Sequence: 1250 frames"
```

### Method 2: Individual Import (For Mixed Sequences)
```
1. Import folder of images
2. Select all → Right-click → "Create Timeline from Clips"
3. Set "One clip per frame" OFF, "Frame Rate" = 24/30 fps
```

### Timeline Configuration
```
Project Settings:
- Timeline Frame Rate: 24 fps (cinematic) or 30 fps (web)
- Playback Frame Rate: Match timeline
- Timeline Resolution: 3840x2160 (4K) or 1920x1080 (HD)
  → Allows 2x-4x zoom/pan in post without quality loss
```

## Deflickering (Essential for Quality)

### Method 1: Smooth OFX (Color Page) - Fastest
```
Node Graph:
Node 1: Primary Grade
Node 2: Smooth OFX (Resolve FX → Smooth)
  - Temporal Radius: 3-5 frames
  - Spatial Radius: 0 (temporal only)
  - Luma Only: ON (preserves color)
  - Strength: 0.5-0.8

⚠️ Render cache needed for real-time playback
```

### Method 2: Manual Keyframe Exposure (Precise)
```
1. Color page → Scopes: Waveform (Luma)
2. Node 1: Add keyframes on Gain/Offset every 10-30 frames
3. Match median luma across sequence
4. Use "Smooth" keyframe interpolation (right-click keyframe)
Best for: Severe flicker, mixed lighting
```

### Method 3: LRTimelapse + DaVinci (Professional)
```
1. Export sequence → LRTimelapse (deflicker + keyframe ramping)
2. LRTimelapse writes XMP sidecars
3. Import back to Resolve → Read XMP metadata
4. Grade with keyframes already smoothed
Best for: Holy Grail (day-to-night), professional work
```

### Method 4: Color Space Transform Normalization
```
Node 1: CST (Input: Camera Log, Output: Linear)
Node 2: Exposure normalization (Math: Divide by mean luma per frame)
Node 3: CST (Input: Linear, Output: Rec.709)
Advanced: Requires scripting/ACES workflow
```

## Motion Blur (Critical for Natural Look)

### Option A: ReelSmart Motion Blur (RSMB) - Best Quality
```
OFX: RE:Vision Effects → RSMB Pro
- Motion Sensitivity: 0.5-1.0
- Blur Amount: 0.5-1.0 (shutter angle equivalent)
- Requires license ($149)
```

### Option B: Directional Blur OFX (Built-in, Free)
```
Node: Directional Blur (Resolve FX Blur)
- Angle: Match motion direction (analyze first frame → last frame)
- Distance: 5-20 pixels (simulates shutter angle)
- Animate Distance: 0 at start → max at middle → 0 at end
Limitation: Uniform blur, not per-pixel
```

### Option C: Fusion Vector Motion Blur (Advanced)
```
Fusion Page:
1. Loader (image sequence)
2. OpticalFlow → Vector motion vectors
3. VectorMotionBlur → Per-pixel accurate blur
4. Saver
Best quality, slower, requires Fusion knowledge
```

### Option D: Retime + Frame Blending (Quick)
```
Edit Page:
1. Select clip → Retime Controls (Cmd+R)
2. Speed: 50% (or desired)
3. Retime Process: "Optical Flow" or "Frame Blend"
4. Adds natural motion blur during speed changes
```

## Creative Camera Moves (Post-Production)

### Simple Pan/Zoom (Color Page - Transform)
```
Node 1: Grade
Node 2: Transform (Inspector → Transform)
  - Keyframe Zoom X/Y: 1.0 → 1.3 (slow zoom in)
  - Keyframe Pan: -0.1 → 0.1 (slow pan right)
  - Keyframe Tilt: 0.0 → -0.05 (slow tilt down)
  - Ease In/Out on all keyframes (right-click → Ease)
  
Tip: Work in 4K timeline, export 1080p → 2x zoom headroom
```

### Dynamic Hyperlapse Move (Fusion Page)
```
Fusion Composition:
1. Loader (image sequence)
2. Transform3D (or Camera3D)
   - Keyframe Position X/Y/Z over time
   - Keyframe Rotation for parallax
3. Renderer3D → MediaOut
   
Parallax Effect:
- Separate foreground/mid/background in Photoshop (layers)
- Import as separate Loaders
- Different Z positions in 3D space
- Camera move creates natural parallax
```

### Dolly Zoom (Vertigo Effect)
```
Color Page Transform:
- Keyframe Zoom: 1.0 → 2.0
- Keyframe Position: Compensate to keep subject same size
- Dolly in + Zoom out (or vice versa)
- Creates unsettling perspective shift
```

## Speed Ramping & Duration Control

### Constant Speed (Standard Timelapse)
```
Edit Page → Retime Controls (Cmd+R):
- Speed: Calculate for target duration
  Formula: (Total frames / Output fps) / Target seconds = Speed %
  Example: 900 frames / 30fps = 30s → Want 10s = 300% speed
```

### Variable Speed (Hyperlapse Style)
```
1. Add speed keyframes (Retime curve)
2. Start slow (100%) → Ramp to fast (500%) → End slow (100%)
3. Use "Smooth" interpolation on speed curve
4. Enable Optical Flow for smooth frames
```

### Frame Blending for Smooth Slow Sections
```
Retime Process options:
- Nearest Neighbor: Sharp, juddery (default)
- Frame Blend: Cross-dissolve frames (ghosting)
- Optical Flow: Motion vectors (best, slowest render)
```

## Export Settings

### Archive Quality (ProRes / DNxHR)
```
Deliver Page:
- Format: QuickTime
- Codec: Apple ProRes 422 HQ (or 4444 for alpha)
- Resolution: Timeline resolution (4K/3840x2160)
- Frame Rate: Timeline frame rate
- Quality: 100% / Restrict to: (leave blank)
Use for: Archival, further editing, VFX plates
```

### Web/Social (H.264/H.265)
```
Deliver Page:
- Format: MP4
- Codec: H.264 (High Profile) or H.265 (HEVC)
- Resolution: 1920x1080 (HD) or 3840x2160 (4K)
- Bitrate: VBR 1-pass, 20-50 Mbps (4K), 10-20 Mbps (HD)
- Audio: AAC 320kbps (if any)
- Keyframe Interval: 1 sec (30 frames @ 30fps)
Use for: YouTube, Instagram, Vimeo, web
```

### Instagram Reel Specific (Vertical Timelapse)
```
- Resolution: 1080x1920 (9:16)
- Crop/Pan: Use Transform to reframe horizontal → vertical
- Bitrate: 8-12 Mbps
- Max 90 seconds
```

## Batch Processing Multiple Sequences

### Resolve Script (Python)
```python
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
proj = pm.LoadProject("Timelapse_Batch")
mp = proj.GetMediaPool()

sequences = [
    ("/path/seq1/IMG_0001.dng", 24),
    ("/path/seq2/DSC_0001.CR3", 30),
]

for path, fps in sequences:
    clip = mp.ImportMedia([path])[0]
    tl = mp.CreateTimelineFromClips("TL_" + clip.GetName(), [clip])
    tl.SetSetting("timelineFrameRate", str(fps))
    # Add render job...
proj.GetRenderJobList()
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Flicker persists | Increase Smooth OFX radius, try LRTimelapse |
| Jittery motion | Enable Optical Flow retime, add motion blur |
| Black frames | Check for missing sequence numbers, re-import |
| Color shift | Fixed WB in camera, use CST for log normalization |
| Large file sizes | Render ProRes LT instead of HQ, or H.265 |
| Slow playback | Generate optimized media / render cache |

## Related Skills

- `davinci-hyperlapse-camera-move` - Advanced 3D camera moves in Fusion
- `davinci-deflicker-advanced` - LRTimelapse integration, holy grail
- `davinci-optical-flow-retime` - Frame interpolation deep dive