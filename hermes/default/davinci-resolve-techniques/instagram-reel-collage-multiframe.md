---
name: instagram-reel-collage-multiframe
description: Instagram Reel collage and multi-frame layout techniques in DaVinci Resolve. Use for photo/video grids, split screens, before/after comparisons, and multi-image storytelling in vertical 9:16 format.
trigger: User wants to create collages, split screens, or multi-frame layouts for Instagram Reels in DaVinci Resolve.
category: davinci-resolve
tags:
  - instagram reel
  - collage
  - split screen
  - multi-frame
  - grid layout
  - davinci resolve
  - vertical video
steps:
  - name: edit-page-grid-layout
    description: Create collage grids using Edit page Transform and Crop tools
    parameters:
      - name: grid_type
        type: string
        enum: ["2x2", "3x3", "1x3_horizontal", "3x1_vertical", "2x1_split", "custom"]
        default: "2x2"
      - name: gap_size
        type: string
        default: "2-5%"
        description: Gap between frames as percentage of frame
      - name: border
        type: string
        default: "None or thin white"
        description: Border style around each cell
      - name: animation
        type: boolean
        default: false
        description: Animate cells in sequentially
    difficulty: beginner
  - name: fusion-advanced-collage
    description: Advanced collages with Fusion (masks, 3D transforms, animated reveals)
    parameters:
      - name: layout_style
        type: string
        enum: ["Grid", "Masonry", "Overlapping", "Polaroid", "Film Strip", "Custom Shapes"]
        default: "Grid"
      - name: perspective_3d
        type: boolean
        default: true
        description: Enable 3D transforms for depth
      - name: shadow_depth
        type: string
        default: "Medium"
        description: Drop shadow for layer separation
    difficulty: intermediate
  - name: before-after-comparison
    description: Split-screen before/after with slider or wipe reveal
    parameters:
      - name: reveal_type
        type: string
        enum: ["Vertical Slider", "Horizontal Slider", "Radial Wipe", "Animated Mask"]
        default: "Vertical Slider"
      - name: label_text
        type: string
        default: "BEFORE / AFTER"
      - name: animation_duration
        type: string
        default: "1-2 seconds"
    difficulty: intermediate
parameters:
  - name: aspect_ratio
    type: string
    default: "9:16 (1080x1920)"
    description: Instagram Reel vertical format
  - name: resolve_page
    type: string
    default: "Edit|Fusion"
    description: Edit for simple grids, Fusion for advanced
  - name: node_graph_type
    type: string
    default: "parallel|layer_mixer"
---

# Instagram Reel Collage & Multi-Frame Layouts

Create engaging multi-image/video layouts for Instagram Reels: grids, split screens, before/after comparisons, and animated collages in DaVinci Resolve.

## Video References

| Technique | Video ID | Key Nodes/Tools | Tags |
|-----------|----------|-----------------|------|
| Instagram Reel C4G58-kJ6t3 Collage | C4G58-kJ6t3 | node1, node2 | collage, instagram reel |
| Instagram Reel Cz6N-q1LCJJ Collage Technique | Cz6N-q1LCJJ | node1, node2 | color correction, grading, instagram reel |
| Instagram Reel C4G58-kJ6t3 Collage (creative) | - | - | collage |

## Core Workflows

### 1. Edit Page Grid Collage (Simplest)
**Reference**: C4G58-kJ6t3, Cz6N-q1LCJJ

**Setup**:
```
Timeline: 1080x1920 (9:16), 30fps
Video Tracks:
├── V1: Background (solid color, gradient, or blurred base)
├── V2-V5: Collage cells (one per track)
└── V6: Labels/Overlays (optional)
```

**Steps**:
1. Create 1080x1920 timeline
2. Add background on V1 (color solid or blurred version of main image)
3. Place each image/video on separate track (V2, V3, V4...)
4. Select clip → Inspector → Transform
5. Set **Zoom** to fit cell size (e.g., 50% for 2x2 grid)
6. Set **Position X/Y** to place in grid
7. Add **Crop** if needed to maintain aspect ratio
8. Optional: Add **Drop Shadow** in Inspector for depth

**Grid Position Calculator (9:16 frame)**:

| Grid | Cell Size | Positions (X, Y) | Zoom |
|------|-----------|------------------|------|
| 2x2 | 50%×50% | (-0.25,-0.25), (0.25,-0.25), (-0.25,0.25), (0.25,0.25) | 0.5 |
| 3x3 | 33%×33% | 9 positions, stepped | 0.33 |
| 1x3 Horizontal | 100%×33% | (0,-0.33), (0,0), (0,0.33) | X:1.0, Y:0.33 |
| 3x1 Vertical | 33%×100% | (-0.33,0), (0,0), (0.33,0) | X:0.33, Y:1.0 |
| 2x1 Split | 50%×100% | (-0.25,0), (0.25,0) | X:0.5, Y:1.0 |

**Gap Between Cells**:
- Reduce Zoom slightly (e.g., 0.48 instead of 0.5)
- Or use Crop: Left/Right/Top/Bottom = 1-2%

### 2. Fusion Advanced Collage (3D, Animated, Styled)
**Reference**: C4G58-kJ6t3 principles

```
Fusion Composition:
├── Background (MediaIn or Background tool)
├── Layout Grid (Transform3D or custom)
│   ├── Cell 1: MediaIn → Transform3D → DropShadow → Merge
│   ├── Cell 2: MediaIn → Transform3D → DropShadow → Merge
│   ├── Cell 3: MediaIn → Transform3D → DropShadow → Merge
│   └── Cell 4: MediaIn → Transform3D → DropShadow → Merge
├── Merge3D (if 3D layout) or Merge2D (flat)
├── Camera3D (for 3D perspective)
├── Renderer3D
└── MediaOut
```

**Fusion Tools for Collage**:
| Tool | Purpose |
|------|---------|
| Transform3D | 3D position, rotation, scale per cell |
| DropShadow | Layer separation depth |
| Polygon/BSpline Mask | Custom shapes (polaroid, circle, hexagon) |
| FrameHold | Freeze video frame for photo cell |
| Text+ | Labels, timestamps, captions |
| Expression | Animate grid formation (staggered entry) |

**Animated Grid Entry (Expression on Transform3D.Translate.Z)**:
```lua
-- Staggered pop-in: each cell delayed by 0.15s
time = comp.CurrentTime
cellIndex = 1 -- change per cell (1,2,3,4)
delay = (cellIndex - 1) * 5 -- 5 frames delay
if time < delay then
    return 10 -- Start behind camera
else
    local t = (time - delay) / 15 -- 15 frame animation
    return math.min(0, 10 * (1 - t^2)) -- Ease out back
end
```

**Polaroid Style (Fusion)**:
```
Cell Chain:
MediaIn → Crop (1:1 square) → Transform3D (rotate ±3°) 
    → RectangleMask (white border) → Merge (Add border)
    → DropShadow → Merge3D
```

### 3. Before/After Comparison (Slider Reveal)
**Popular for: Color grading demos, photo edits, transformations**

**Edit Page Method (Adjustment Clip + Crop)**:
```
Timeline:
├── V1: Before clip (full frame)
├── V2: After clip (full frame)
├── V3: Adjustment Clip (spans both)
│   └── Crop Effect: Right = 50% (animated 100%→0%)
└── V4: Slider Graphic (line + handle) + Labels
```

**Steps**:
1. Stack Before (V1) and After (V2) clips
2. Add Adjustment Clip on V3 spanning transition
3. Open Adjustment Clip → Inspector → Effects → Crop
4. Animate **Crop Right**: 100% (show Before) → 0% (show After)
5. Add line graphic on V4, animate Position X with Crop
6. Add "BEFORE" / "AFTER" text labels

**Fusion Method (Professional Slider)**:
```
Fusion Comp:
├── MediaIn1 (Before)
├── MediaIn2 (After)
├── Merge (Foreground = After, Background = Before)
│   └── Mask: Rectangle animated X position
├── Rectangle (Slider line) → Transform (animate X)
├── Circle (Handle) → Transform (animate X, parent to line)
├── Text+ (BEFORE/AFTER labels)
└── MediaOut
```

**Mask Animation Expression** (on Rectangle Mask.Width):
```lua
-- Width follows playhead or slider position
sliderPos = comp:FindTool("SliderTransform").Transform[1] -- X position
return math.max(0, math.min(1, (sliderPos + 0.5))) -- Normalize -0.5→0.5 to 0→1
```

### 4. Creative Collage Styles

| Style | Description | Tools |
|-------|-------------|-------|
| **Masonry** | Uneven grid like Pinterest | Edit: Manual positioning / Fusion: Packer tool |
| **Overlapping** | Photos stack with rotation | Edit: Transform rotation / Fusion: Transform3D Z-offset |
| **Polaroid** | White border, caption area, shadow | Fusion: RectangleMask + DropShadow + Text+ |
| **Film Strip** | Sprocket holes, frame numbers | Fusion: Custom mask + Text+ |
| **Split Diagonal** | Angled split with feather | Edit: Linear Wipe / Fusion: Gradient Mask |
| **Kaleidoscope** | Mirrored repeating pattern | Fusion: Kaleido tool or Transform3D mirrors |

### 5. Color Grading Collage Cells
**Reference**: Cz6N-q1LCJJ (color correction per image)

```
Per-Cell Grade (on each track or Fusion branch):
├── Node 1: Match Exposure (Lift/Gamma/Gain)
├── Node 2: Match White Balance (Temp/Tint)
├── Node 3: Creative Look (Consistent LUT across cells)
│   └── LUT Intensity: 50-70% (subtle unity)
└── Node 4: Cell-Specific Pop
    ├── Subject: Power Window + Contrast/Sat boost
    └── Background: Desaturate slightly
```

**Consistency Tip**: Apply same creative LUT to all cells at reduced intensity, then individual primary correction per cell.

### 6. Export for Instagram Reels

| Setting | Value |
|---------|-------|
| Resolution | 1080x1920 |
| Frame Rate | 30fps |
| Codec | H.264 High Profile |
| Bitrate | 8-12 Mbps |
| Color Space | Rec.709 / sRGB |
| Audio | AAC 128kbps+ |

**Safe Zones** (keep critical content inside):
- **Title Safe**: 90% center (avoid top/bottom UI)
- **Action Safe**: 95% center
- **Reel UI Overlay**: Bottom ~15% (caption, audio, buttons)

## Templates (Save as Timeline/Compound Clips)

| Template Name | Structure | Use Case |
|---------------|-----------|----------|
| Reel_2x2_Grid | 4 cells, labeled | Photo dumps, product showcase |
| Reel_BeforeAfter | Slider + labels | Color grade demo, photo edit |
| Reel_3x1_Vertical | 3 stacked | Story sequence, step-by-step |
| Reel_FilmStrip | 5 frames horizontal | Behind-the-scenes, timeline |
| Reel_Polaroid_Stack | 3-4 angled polaroids | Travel, memories, aesthetic |

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Images stretched | Wrong Zoom/Crop | Use Crop to maintain aspect, then Zoom to fill |
| Gaps uneven | Manual positioning | Use Fusion expressions or calculator above |
| Blurry cells | Low-res source on 4K timeline | Use "Scale Full Frame with Crop", enable Super Scale (Studio) |
| Labels cut off | Outside safe zone | Keep text inside 85% center |
| Animation stutter | No render cache | Render Cache → User for Fusion comps |

## Related Skills
- `instagram-reel-editing-techniques` - General Reel editing
- `davinci-resolve-fusion-compositing` - Advanced Fusion
- `instagram-reel-color-grading-workflow` - Consistent grading
- `davinci-resolve-transitions-effects` - Animated transitions between cells