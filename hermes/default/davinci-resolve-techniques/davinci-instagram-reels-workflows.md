---
name: davinci-instagram-reels-workflows
description: Instagram Reels creation workflows - vertical formatting, text overlays, thumbnails, color grading for social, cross-page pipeline
category: davinci-resolve
tags: [instagram, reels, social-media, vertical-video, text-overlay, thumbnail, color-grading, export]
trigger: Use when user asks about creating Instagram Reels, vertical video formatting, social media export, text overlays for Reels, or Reels color grading
---

# DaVinci Resolve Instagram Reels Workflows

Complete workflows for creating Instagram Reels including vertical formatting, text overlays, thumbnails, color grading for social, and export settings.

## Techniques Included

### 1. Instagram Reel Creation with DaVinci Resolve (Multi-Page Workflow)
**Video ID:** `C_LV_aAsXH_` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node for Color Correction, Node for Speed Effect
- **Steps:**
  1. Step 1: Import and Organize Footage
  2. Step 2: Apply Color Correction and Speed Effect
- **Tags:** Instagram Reel Creation, DaVinci Resolve Technique

### 2. Instagram Reel Creation with DaVinci Resolve (Color + Effects)
**Video ID:** `C_tccu0Pfjf` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, Effects Node
- **Parameters:** Color Correction: Saturation 100%, Contrast 50%; Effects: Opacity 25%, Blur: Gaussian Blur (Soft)
- **Steps:**
  1. Import the Instagram Reel footage into DaVinci Resolve
  2. Apply color correction to enhance the visual appeal
- **Tags:** Instagram Reels, Color Correction, Effects, DaVinci Resolve

### 3. Instagram Reel Creation with DaVinci Resolve (Color + Grading)
**Video ID:** `C_Wi25Vvkqi` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, Grading Node
- **Parameters:** Color Correction: Saturation 100%, Contrast 50%; Grading: Lift 25%, Gamma 100%
- **Steps:**
  1. Import Instagram Reel footage into DaVinci Resolve
  2. Apply Color Correction to the footage
  3. Add Grading effects to enhance the visual appeal
- **Tags:** Instagram Reels, Color Correction, Grading, DaVinci Resolve

### 4. Instagram Reel C_VmwLspFQC - Save (LUT Application)
**Video ID:** `C_VmwLspFQC` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Steps:**
  1. Step 1: Import the Instagram Reel C_VmwLspFQC into DaVinci Resolve
  2. Step 2: Apply a LUT (Look-Up Table) to the footage to enhance colors and contrast
- **Tags:** color grading, Instagram Reel, DaVinci Resolve

### 5. Instagram Reel Editing Techniques (Color + Audio Sync)
**Video ID:** `DTdILe3DdXS` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node for Color Correction, Node for Audio Sync
- **Parameters:** Param1: Adjusting color balance to match outdoor lighting conditions, Param2: Synchronizing audio with video for lip sync and proper timing
- **Steps:**
  1. Import the footage into DaVinci Resolve
  2. Apply color correction to match outdoor lighting conditions
- **Tags:** Instagram Reel Editing, Color Correction, Audio Sync

### 6. Instagram Reel with DaVinci Resolve (Color Correction + Grading)
**Video ID:** `DOQVFcdjasb` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, Grading Node
- **Parameters:** Color Correction: Saturation 0.5, Contrast 1.2; Grading: Lift 0.3, Gamma 0.8
- **Steps:**
  1. Import footage into DaVinci Resolve
  2. Apply color correction to the footage
  3. Adjust grading to enhance contrast and saturation
- **Tags:** Instagram Reel, DaVinci Resolve, Color Correction, Grading

### 7. Cinematic Drone Moves Tutorial Thumbnail
**Video ID:** `C11pkkePnC4` | **Difficulty:** Beginner | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Text+, Color Correction
- **Parameters:** Text+: Font: Impact, Size: 100, Color: Yellow, Outline Color: Black, Outline Width: 2; Color Correction: Contrast 1.2, Saturation 1.1, Gamma 0.9
- **Steps:**
  1. Import the drone footage into DaVinci Resolve
  2. Add a Text+ node to the timeline
  3. Type "3 CINEMATIC DRONE MOVES PART 6" into the Text+ node
  4. Adjust the font, size, color, and outline of the text to match the example
  5. Apply color correction to the footage to enhance the colors and contrast
  6. Position the text and drone footage to create a compelling thumbnail
- **Tags:** thumbnail, text overlay, drone footage, tutorial, cinematic

### 8. Instagram Reel Promotional Landscape
**Video ID:** `C1CXJysIoyU` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Corrector, Contrast Adjustment
- **Parameters:** Color Corrector: Saturation: 50, Lift: 20, Gain: -10, Hue Shift: 0
- **Steps:**
  1. Import footage
  2. Apply color grading using Color Corrector node
  3. Adjust contrast with Contrast Adjustment node
- **Tags:** landscape, motivation, promotion

---

## Reels Project Setup

### Timeline Settings for Reels (9:16 Vertical)
```
Project Settings → Master Settings:
├── Timeline Resolution: 1080x1920 (or 2160x3840 for 4K)
├── Pixel Aspect Ratio: Square
├── Timeline Frame Rate: 30 fps (Reels standard) or 24 fps (cinematic)
├── Video Monitoring: 1080x1920
└── Color Science: DaVinci YRGB Color Managed
```

### Vertical Timeline Templates
```
Method 1: New Timeline → Custom Settings → 1080x1920
Method 2: Right-click Media Pool → Timelines → Create New Timeline → Vertical
Method 3: File → New Timeline → "Use Custom Settings" → 1080x1920
```

---

## Cross-Page Reels Workflow

### Complete Pipeline
```
EDIT PAGE (Assembly & Timing)
    │
    ├── Import vertical clips (or rotate horizontal)
    ├── Rough cut to ~15-90 seconds
    ├── Add music/sync points (markers on beat)
    ├── Text/Titles placement (Edit page titles or Fusion)
    └── Pancake: Selects (top) → Assembly (bottom)
    │
    ▼
CUT PAGE (Fast Trim - Optional)
    │
    ├── Source Tape → Quick selects
    ├── Sync Bin → Multi-cam if applicable
    └── Trim to beat
    │
    ▼
FUSION PAGE (Advanced GFX)
    │
    ├── Text+ animations (lower thirds, captions)
    ├── Motion graphics (subscribe, follow)
    ├── Transitions (custom wipes, zooms)
    └── Tracking (text follows subject)
    │
    ▼
COLOR PAGE (Grade & Format)
    │
    ├── CST: Camera → Rec.709 (sRGB for IG)
    ├── Primary: Exposure, WB, Contrast
    ├── Creative: LUT / Look (teal/orange, moody, bright)
    ├── Vignette: Subtle (-0.1 to -0.3)
    ├── Letterbox/Pillarbox: Handle non-9:16 sources
    └── Safe Zones: View → Safe Margins (Title: 90%, Action: 95%)
    │
    ▼
FAIRLIGHT (Audio Polish)
    │
    ├── Loudness: -14 LUFS (IG target)
    ├── True Peak: -1 dBTP
    ├── Voice: Clarity, De-ess, Compress
    ├── Music: Duck under voice (sidechain)
    └── SFX: Transitions, whooshes
    │
    ▼
DELIVER PAGE (Export)
    │
    ├── Format: MP4 (H.264 High Profile)
    ├── Resolution: 1080x1920
    ├── Frame Rate: 30 fps
    ├── Bitrate: 10-20 Mbps (CBT/VBR)
    ├── Audio: AAC 256 kbps
    └── Filename: PROJECT_IG_REEL_v01.mp4
```

---

## Text & Caption Workflows

### Auto-Captions (DaVinci 18.5+)
```
Timeline → Right-click audio track → "Create Subtitles from Audio"
Settings:
├── Language: English (or source language)
├── Max Characters/Line: 32-42 (vertical)
├── Max Lines: 2
├── Min Duration: 1.5 sec
└── Style: Preset or Custom
```

### Manual Text+ for Reels (Animated)
```
Fusion Page:
Text+ → Layout:
├── Font: Montserrat Bold / Inter Bold / Impact
├── Size: 120-180 (for 1080p)
├── Alignment: Center
├── Line Spacing: 1.2
├── Tracking: 10-20
└── Style:
    ├── Fill: White / Brand Color
    ├── Stroke: Black, 3-5px
    ├── Shadow: Offset (3,3), Blur 8, Opacity 0.5
    └── Background: Rounded Rect, Padding 20, Color Brand/Black 80%

Animation (Modifiers):
├── Position Y: Expression (sine wave for bounce)
├── Scale: Keyframe 0→100% over 15 frames (pop-in)
├── Opacity: Fade in/out
└── Tracking: Animate 0→20 over word duration
```

### Caption Safe Zones (9:16)
```
┌─────────────────────────────────┐ 1080px
│  ░░░░░ TITLE SAFE (90%) ░░░░░  │ 54px margin top/bottom
│  ░                              ░ │
│  ░   ░░ ACTION SAFE (95%) ░░   ░ │ 27px margin
│  ░   ░                      ░   ░ │
│  ░   ░   CONTENT AREA      ░   ░ │
│  ░   ░                      ░   ░ │
│  ░   ░░░░░░░░░░░░░░░░░░░░░   ░ │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└─────────────────────────────────┘ 1920px
```

---

## Color Grading for Instagram

### IG-Optimized Look (Bright, Punchy, Mobile-Friendly)
```
Node 01: CST Input (Camera → DWG)
Node 02: Primary Balance
    ├── Lift: -5 to -10 (crush blacks slightly)
    ├── Gamma: +5 to +10 (lift mids for phone screens)
    ├── Gain: +5 (protect highlights)
    ├── Contrast: +10 to +15
    ├── Pivot: 0.45 (protect shadows)
    └── Saturation: +10 to +15
Node 03: Creative LUT (Optional)
    ├── "Instagram" / "Mobile" / "Social" LUTs
    ├── Key Output Gain: 0.7-0.9 (dial back)
Node 04: HSL Curves
    ├── Hue vs Sat: Skin tone protect (desat neighbors)
    ├── Hue vs Hue: Shift greens → teal, oranges → warm
    └── Lum vs Sat: Desaturate shadows (-10), saturate mids (+5)
Node 05: Vignette
    ├── Shape: Circle, Softness: 0.8
    ├── Size: 0.6, Strength: -0.15
Node 06: Output CST (DWG → Rec.709 sRGB)
    ├── Tone Mapping: Automatic
    └── Gamut Mapping: Perceptual
```

### Common Reels Looks

| Look | Vibe | Key Adjustments |
|------|------|-----------------|
| **Bright & Airy** | Lifestyle, travel | High key, low contrast, warm, +sat |
| **Moody Cinematic** | Story, drama | Teal/orange, crushed blacks, -sat |
| **Vintage Film** | Nostalgia | Film LUT, grain, halation, gate weave |
| **High Energy** | Fitness, dance | High contrast, saturated, punchy |
| **Clean Minimal** | Product, tech | Neutral WB, slight desat, crisp |

---

## Audio for Reels

### Loudness Standards
| Platform | Integrated | True Peak | LRA |
|----------|------------|-----------|-----|
| **Instagram Reels** | **-14 LUFS** | **-1 dBTP** | < 7 LU |
| TikTok | -14 LUFS | -1 dBTP | - |
| YouTube Shorts | -14 LUFS | -1 dBTP | - |

### Fairlight Quick Mix
```
Track 1: Voice/Dialogue
    ├── EQ: High-pass 100Hz, Presence +3dB @ 3-5kHz
    ├── De-Esser: 5-8kHz, Threshold -20dB
    ├── Compressor: 3:1, Attack 10ms, Release 100ms, -6dB GR
    └── Limiter: Ceiling -1dB

Track 2: Music
    ├── EQ: High-pass 80Hz, Dip 2-4kHz (voice clarity)
    ├── Sidechain Compressor: Key from Voice, 4:1, -6dB duck
    └── Level: -18 to -24 LUFS (under voice)

Track 3: SFX
    ├── Level: Match perceived loudness
    └── Pan: Creative (whoosh L→R)
```

---

## Export Settings (Deliver Page)

### Instagram Reels Optimized
```
Format: MP4
Codec: H.264 (Main/High Profile)
Resolution: 1080x1920
Frame Rate: 30 fps (constant)
Bitrate: 12-20 Mbps VBR (1-pass or 2-pass)
Keyframe Interval: 30 frames (1 sec)
Profile: High @ Level 4.1
Colorspace: Rec.709 / BT.709
Transfer: sRGB / BT.1886

Audio:
Codec: AAC-LC
Sample Rate: 48 kHz
Bitrate: 256 kbps
Channels: Stereo

Advanced:
├── Force Keyframes at Markers: On
├── Closed Captions: Burn-in or Sidecar (.srt)
├── Metadata: Title, Description, Tags
└── Upload Direct: Not recommended (use IG app)
```

### File Size Targets
| Duration | Target Size | Max Size (IG) |
|----------|-------------|---------------|
| 15 sec | 20-30 MB | 4 GB |
| 30 sec | 40-60 MB | 4 GB |
| 60 sec | 80-120 MB | 4 GB |
| 90 sec | 120-180 MB | 4 GB |

---

## Common Reels Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Black bars top/bottom** | Horizontal footage in vertical timeline | Crop/Zoom, or add blurred background |
| **Text cut off** | Outside title safe | Use Safe Margins, keep text in center 90% |
| **Video blurry on IG** | Over-compression | Export higher bitrate (20 Mbps), 2-pass |
| **Audio quiet** | Wrong loudness | Normalize to -14 LUFS in Fairlight |
| **Color washed out** | No Output CST | Add Output CST (DWG → Rec.709) |
| **Stutter playback** | Variable frame rate | Force 30 fps constant in Project Settings |
| **Caption sync off** | Frame rate mismatch | Generate captions AFTER final frame rate set |

---

## Skill Trigger Examples

- "How to make Instagram Reels in DaVinci Resolve"
- "Vertical video timeline setup DaVinci"
- "Auto captions DaVinci Resolve Reels"
- "Instagram Reels export settings"
- "Text animation for Reels Fusion"
- "Color grade for Instagram mobile"
- "Loudness -14 LUFS Fairlight"
- "Reels safe margins"
- "Horizontal to vertical conversion"
- "Reels thumbnail creation"