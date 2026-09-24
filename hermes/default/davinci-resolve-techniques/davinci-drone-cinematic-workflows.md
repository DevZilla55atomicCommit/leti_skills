---
name: davinci-drone-cinematic-workflows
description: Drone cinematography workflows - color grading, LUT mapping, cinematic moves, depth of field, aerial grading techniques
category: davinci-resolve
tags: [drone, cinematic, aerial, color-grading, lut, depth-of-field, cinematic-moves, drone-footage]
trigger: Use when user asks about drone footage grading, cinematic drone looks, aerial color correction, LUTs for drone, or depth of field for drone shots
---

# DaVinci Resolve Drone Cinematic Workflows

Specialized workflows for drone/aerial footage including color grading, LUT mapping, cinematic movement enhancement, and atmospheric effects.

## Techniques Included

### 1. Cinematic Drone Shot with DaVinci Resolve
**Video ID:** `C3xXriXIbv8` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, LUT Mapping Node
- **Parameters:** Color Correction: Saturation 100%, Contrast 50%; LUT Mapping: Input LUT "Cinematic Drone LUT", Output LUT "Final Output LUT"
- **Steps:**
  1. Import footage into DaVinci Resolve
  2. Apply color correction using the Color Correction Node with desired saturation and contrast values
- **Tags:** Drone Cinematography, Color Grading, DaVinci Resolve Techniques

### 2. Cinematic Drone Moves
**Video ID:** `C1HDtWBvZYH` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Node for Color Correction, Node for Motion Tracking
- **Parameters:** Param1: LUT for Cinematic Look, Param2: Motion Tracking Settings
- **Steps:**
  1. Import Drone Footage
  2. Apply LUT for Cinematic Look
  3. Perform Motion Tracking
- **Tags:** Drone Filming, Cinematic Techniques

### 3. Cinematic Drone Moves Tutorial Thumbnail
**Video ID:** `C11pkkePnC4` | **Difficulty:** Beginner | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Text+, Color Correction
- **Parameters:** Text+: Font: Impact, Size: 100, Color: Yellow, Outline Color: Black, Outline Width: 2; Color Correction: Contrast: 1.2, Saturation: 1.1, Gamma: 0.9
- **Steps:**
  1. Import the drone footage into DaVinci Resolve
  2. Add a Text+ node to the timeline
  3. Type "3 CINEMATIC DRONE MOVES PART 6" into the Text+ node
  4. Adjust the font, size, color, and outline of the text to match the example
  5. Apply color correction to the footage to enhance the colors and contrast
  6. Position the text and drone footage to create a compelling thumbnail
- **Tags:** thumbnail, text overlay, drone footage, tutorial, cinematic

### 4. Artificial Depth of Field / Focus Blur for Drone
**Video ID:** `Cv2MWyANfG7` | **Difficulty:** Intermediate | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Gaussian Blur, Magic Mask
- **Parameters:** Blur Radius: 25.0, Strength: 1.0
- **Steps:**
  1. Import footage and go to the Color Page
  2. Use the Magic Mask to isolate the subject (the drone)
  3. Create a new node for the background
  4. Add a Gaussian Blur or Lens Blur effect to the background node
  5. Adjust the blur radius to create a cinematic shallow depth of field
- **Tags:** cinematic, drone, depth-of-field, tutorial

### 5. Teal and Orange Cinematic Grade (Aerial)
**Video ID:** `Cve9BKQocVN` | **Difficulty:** Beginner | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Primary Wheels, Curves, Hue/Saturation/Luma
- **Parameters:** Saturation: +15, Contrast: Increased, Midtones: Warm/Orange, Shadows: Teal/Blue
- **Steps:**
  1. Add a primary node to adjust contrast and white balance
  2. Use the Color Wheels to push shadows toward teal/blue
  3. Use the Offset or Wheels to push midtones/highlights toward a warm orange/yellow
  4. Use the Hue/Saturation curve to de-saturate greens if they appear distracting
  5. Apply a slight vignette to draw focus to the central island formation
- **Tags:** color grading, cinematic, aerial, teal-and-orange

### 6. Instagram Reel CxFqbyWSgxs Drone Photography
**Video ID:** `CxFqbyWSgxs` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Tags:** drone photography, Instagram Reel, DaVinci Resolve

---

## Drone Footage Characteristics & Challenges

### Typical Drone Camera Profiles
| Drone | Log Profile | Color Space | Bit Depth |
|-------|-------------|-------------|-----------|
| DJI Mavic 3 | D-Log / D-Log M | Rec.709 / DCI-P3 | 10-bit |
| DJI Air 2S | D-Log | Rec.709 | 10-bit |
| DJI Mini 3/4 Pro | D-Cinelike | Rec.709 | 10-bit |
| Autel EVO II | A-Log | Rec.709 | 10-bit |
| FPV (GoPro) | Flat / Protune | Rec.709 | 8-10 bit |

### Common Issues
- **High contrast** (bright sky + dark ground)
- **Color casts** (magenta/green from IR pollution)
- **Compression artifacts** (banding in skies)
- **Rolling shutter** (fast moves)
- **Vibration/jello** (prop resonance)

---

## Color Grading Pipeline for Drone

### Node Structure (Recommended)
```
Node 01: CST (Camera → DaVinci WG / ACEScct)
    └── Input: DJI D-Log / D-Cinelike / A-Log
    └── Output: DaVinci Wide Gamut Intermediate

Node 02: Primary Balance (Exposure, WB, Contrast)
    └── Lift/Gamma/Gain + Temperature/Tint
    └── Target: Protect highlights (sky), lift shadows (ground)

Node 03: Highlight Recovery (Optional)
    └── Qualifier: Select sky → Highlight Roll-off
    └── Or: HDR Wheels → Highlight compression

Node 04: Creative LUT / Look
    └── Drone-specific LUT (see below)
    └── Key Output Gain: 0.5-0.8 for subtlety

Node 05: Aerial Atmosphere
    └── Haze/Dehaze (Color Warper or Curves)
    └── Distance-based grading (Depth Map if available)

Node 06: Sky Enhancement
    └── Power Window: Sky region
    └── Gradient: Blue saturation, exposure balance

Node 07: Vignette / Focus Pull
    └── Circular Window: Center interest
    └── Softness: 70-90

Node 08: Output CST (DaVinci WG → Rec.709 / P3)
```

### Drone-Specific LUT Recommendations
| Look | LUT Source | Use Case |
|------|------------|----------|
| **Natural/Documentary** | DJI Official D-Log → Rec.709 | Real estate, survey |
| **Cinematic Teal/Orange** | Custom / FilmConvert / Kodak 2383 | Narrative, travel |
| **High Contrast** | ARRI LogC → Rec.709 + Contrast | Dramatic landscapes |
| **Golden Hour** | Custom warm LUT | Sunset/sunrise |
| **Moody/Desaturated** | Bleach Bypass / Custom | Overcast, stormy |

---

## Depth of Field Simulation for Drone

### Why Drone Footage Needs DOF
- Small sensors = deep focus (everything sharp)
- Cinematic look = shallow focus separation
- Subject isolation (drone, building, person)

### Color Page Method (Used in Technique)
```
Node: Background Blur
├── Magic Mask → Select Subject (Drone/Building/Person)
├── Invert Mask → Background
├── Gaussian Blur: Radius 15-35
├── Lens Blur (Studio): Bokeh shape, rotation
└── Mix: Opacity 0.6-0.8 for realism
```

### Fusion Page Method (Advanced)
```
MediaIn → Depth Map (DaVinci Depth Map OFX)
    │
    ├──→ Lens Blur (Depth Input: Depth Map)
    │       └── Focus Distance: Animated
    │       └── Aperture: f/1.8-f/2.8 equivalent
    │
    └──→ Merge (Sharp FG over Blurred BG)
```

### Pro Tips
- **Animate Focus Distance** for "rack focus" effect
- **Match Bokeh** to lens being simulated (circular, hexagonal, anamorphic)
- **Don't Overdo:** Subtle 15-25 radius usually sufficient
- **Edge Mask:** Feather subject edges (2-5px) to avoid halo

---

## Cinematic Drone Moves Enhancement

### In-Camera Moves → Post Enhancement
| Move Type | Post Technique |
|-----------|----------------|
| **Reveal (Tilt Up)** | Speed ramp at horizon line |
| **Orbit (POI)** | Stabilize center, enhance parallax |
| **Top Down (Nadir)** | Symmetry crop, grid overlay |
| **Dolly/Tracking** | Motion blur enhancement |
| **Rise/Descend** | Scale keyframe (dolly zoom feel) |
| **FPV Dive** | Speed ramp + motion blur + shake |

### Motion Tracking for Graphics
```
Color/Fusion → Tracker → Track Drone/Subject
    → Export Track Data → Text+/Graphics
    → Attach Callouts, Labels, Distance Markers
```

---

## Sky Replacement / Enhancement

### When to Replace Sky
- Blown out highlights (unrecoverable)
- Wrong time of day for narrative
- Add dramatic clouds

### Workflow (Fusion)
```
MediaIn → DeltaKeyer (Blue/Green Screen: Sky)
    → Clean Plate (Garbage Matte)
    → New Sky (Loader: Sky HDR/EXR)
    → Merge (New Sky under Foreground)
    → Color Match (Sky → Foreground lighting)
    → Edge Blur (1-2px)
    → Light Wrap (Subtle)
```

### Sky Enhancement (Color Page - No Replace)
```
Node: Sky Window (Power Window + Gradient)
    → Saturation: +20-30 (Blue)
    → Lift: -5 to -10 (Darker sky)
    → Gamma: +5 (Cloud detail)
    → Hue: Slight cyan shift (natural)
```

---

## Export Settings for Drone Content

### YouTube / Social (Rec.709)
```
Format: MP4 (H.264/H.265)
Resolution: 4K (3840×2160) or 2.7K
Frame Rate: 24/30/60 (match source)
Bitrate: 45-60 Mbps (4K H.264), 25-35 Mbps (H.265)
Color: Rec.709, Limited Range
Audio: AAC 320 kbps
```

### Client Delivery (ProRes)
```
Format: QuickTime (ProRes 422 HQ / 4444)
Resolution: Native (4K/5.2K/6K)
Color: Rec.709 or P3 (per spec)
Audio: PCM 24-bit 48kHz
```

### HDR Delivery (If graded in HDR)
```
Format: MP4 (H.265/HEVC 10-bit)
Color: Rec.2020 / PQ (ST.2084) or HLG
Mastering Display: 1000 nits (typical)
Metadata: HDR10+ / Dolby Vision (if licensed)
```

---

## Skill Trigger Examples

- "How do I color grade DJI D-Log footage?"
- "Best LUTs for drone footage in DaVinci Resolve"
- "Create shallow depth of field on drone shots"
- "Cinematic drone moves post-production"
- "Sky replacement for drone footage"
- "Teal orange grade for aerial footage"
- "Drone footage looks flat how to fix"
- "Export drone video for YouTube 4K"