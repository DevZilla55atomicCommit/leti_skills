---
name: split-screen-comparison-technique
description: Creating split-screen and comparative visual layouts
category: photography
tags: [split-screen, comparison, layout, before-after, fusion, edit]
difficulty: beginner
---

# Split-Screen Comparison Technique

Creating side-by-side, before/after, and multi-view compositions in DaVinci Resolve.

## Edit Page Method (Fastest)

### Horizontal Split (Top/Bottom)
1. Place Clip A on V1, Clip B on V2
2. Select Clip B → Inspector → **Crop**
3. **Crop Top**: 50 (or 0.5 normalized)
4. Adjust **Position Y** to align content
5. Add **Solid Color** on V3 for divider line (optional)

### Vertical Split (Left/Right)
1. Clip A on V1, Clip B on V2
2. Clip B → Inspector → **Crop**
3. **Crop Right**: 50
4. Adjust **Position X** to align

### Diagonal / Custom Shape
1. Use **Crop** with keyframes for animated reveals
2. Or use **Fusion** for complex masks

## Fusion Page Method (Advanced)

### Node Setup
```
MediaIn1 ──────────┐
                   ├── Merge (Foreground) ─── MediaOut
MediaIn2 ──────────┘
         ▲
         │
    RectangleMask ───► Mask Input
```

### Animated Wipe
1. Add **Rectangle Mask** to Merge foreground input
2. Animate **Center X/Y** or **Width/Height** over time
3. Increase **Soft Edge** for feathered transition
4. Use **Spline Editor** for easing curves

## Common Layouts

| Layout | Use Case | Setup |
|--------|----------|-------|
| **50/50 Horizontal** | Before/After grading | Crop Top: 50% |
| **50/50 Vertical** | Lens comparison | Crop Right: 50% |
| **Picture-in-Picture** | BTS overlay | Scale: 0.3, Position corner |
| **Triptych** | 3-way comparison | 3 tracks, each Crop 33% |
| **Quad** | 4-cam multicam | 4 tracks, 50% each axis |

## Text & Labeling

### Edit Page
1. **Titles → Text+** on track above split
2. Position at seam line
3. **Background** opacity for readability

### Fusion (Cleaner)
```
Text+ ──────────────┐
                    ├── Merge (Over) ─── MediaOut
Merge Output ───────┘
```

## Sync & Alignment

### Temporal Sync
- **Edit → Auto Align Clips** (waveform)
- Or manual: Match action peak (door open, foot strike)

### Spatial Alignment
1. **Transform → Position/Zoom** on each clip
2. Use **Grid** overlay (Timeline → View → Show Grid)
3. Match horizon lines, vertical edges

## Export Presets

### Social Media (Vertical)
- **Timeline**: 1080x1920
- **Split**: Horizontal (top/bottom)
- **Labels**: Large, centered

### YouTube (Horizontal)
- **Timeline**: 1920x1080 or 3840x2160
- **Split**: Vertical (left/right) or 4K quad
- **Labels**: Bottom third

## DaVinci Resolve Shortcuts

| Action | Shortcut |
|--------|----------|
| New Fusion Clip | Right-click clip → New Fusion Clip |
| Open Fusion Page | Click Fusion tab (bottom) |
| Toggle Inspector | Cmd/Ctrl + 3 |
| Keyframe | Click diamond next to param |

## Tags
`split-screen` `comparison` `layout` `before-after` `fusion` `edit` `masking` `transitions`