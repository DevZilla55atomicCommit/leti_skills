---
name: davinci-fusion-fairlight-vfx
description: Fusion page VFX workflows and Fairlight audio pipeline — Grid Warp distortion, Paint/Clone object removal, Fairlight VFX pipeline management
trigger: Use when doing VFX work in Fusion, object removal, warp distortion, or managing Fairlight-to-Fusion pipeline in DaVinci Resolve
steps:
  - name: Luffy Stretch / Grid Warp Distortion
    description: Rubber-hose limb stretching using Grid Warp node in Fusion
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [MediaIn, Grid Warp, Transform, MediaOut]
    parameters:
      gridWarp_type: "Bilinear"
      mesh_density: "High"
      smoothness: "Medium"
    steps:
      - Add the clip to the Fusion page
      - Add a Grid Warp node after the MediaIn
      - Increase the mesh density to allow for finer control over the subject limbs
      - Keyframe the vertex points of the grid to stretch the arms or torso rubbery
      - Apply a Transform node to adjust the final framing after the distortion
      - Add a Blur node if necessary to soften the edges of the distortion
    tags: [fusion, warp, vfx, grid warp, distortion, special effects]

  - name: Object Removal using Paint/Clone
    description: Remove unwanted objects (wires, rigs, blemishes) using Paint node Clone tool
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [MediaIn, Paint Node, Merge, MediaOut]
    parameters:
      Paint Tool: "Clone"
      Stroke Type: "Smart"
      Opacity: "1.0"
    steps:
      - Import the clip into the Fusion page
      - Add a Paint node and connect it after MediaIn
      - Select the Paint tool and choose Clone mode
      - Hold Alt and click on a clean source area near the object
      - Paint over the unwanted object to cover it with clean pixels
      - Adjust stroke smoothness to blend the patch seamlessly
      - Animate strokes if object moves (keyframe stroke position)
    tags: [fusion, paint, clone, object removal, vfx, wire removal, cleanup]

  - name: FVPM — Fairlight VFX Pipeline Management
    description: Organized pipeline from Fairlight audio edit through Color to Fusion VFX
    resolve_page: Color|Edit|Fusion|Fairlight
    difficulty: intermediate
    key_nodes: [Node1: Color Correction, Node2: Fusion for Visual Effects]
    parameters:
      param1: "LUT (Look-Up Table) for color grading"
      param2: "FX settings for visual effects"
    steps:
      - Step 1: Import and organize footage in Fairlight (audio sync, cleanup)
      - Step 2: Apply LUTs and color correction in Color page
      - Step 3: Send clips to Fusion for VFX work (right-click → Open in Fusion)
      - Step 4: Composite VFX in Fusion node graph
      - Step 5: Return to Color for final grade unification
      - Step 6: Deliver from Deliver page with proper render settings
    tags: [fairlight, vfx, color grading, post-production, pipeline, workflow]

  - name: Fusion Node Graph Basics
    description: Core Fusion compositing nodes and workflow
    resolve_page: Fusion
    difficulty: beginner
    key_nodes: [MediaIn, MediaOut, Merge, Transform, ColorCorrector, Blur]
    parameters:
      merge_mode: "Over"
      transform_mode: "Match Move"
    steps:
      - Open Fusion page (clip selected on timeline)
      - MediaIn = source footage input
      - Add nodes: Merge (combine), Transform (position/scale/rotate), ColorCorrector (grade), Blur (soften)
      - Connect nodes: MediaIn → Transform → Merge → MediaOut
      - Use Inspector to adjust node parameters
      - Use Spline/Keyframes for animation
    tags: [fusion, compositing, node graph, merge, transform, color corrector]

  - name: Text+ & Title Animation in Fusion
    description: Create and animate text using Fusion Text+ tool
    resolve_page: Fusion
    difficulty: beginner
    key_nodes: [Text+, Merge, Transform]
    parameters:
      font: "Impact"
      size: "100"
      color: "Yellow"
      outline_color: "Black"
      outline_width: "2"
    steps:
      - Add Text+ node in Fusion
      - Type text in StyledText field (Inspector)
      - Format: font, size, color, outline, tracking
      - Connect Text+ to Merge node over background
      - Animate with Transform (position, scale, rotation) or Text+ built-in animation
      - Add keyframes in Spline editor
    tags: [fusion, text+, title, animation, typography, motion graphics]

parameters:
  - name: grid_warp_density
    type: string
    description: Grid Warp mesh density
    default: "High"
  - name: paint_stroke_type
    type: string
    description: Paint stroke type for cloning
    default: "Smart"
  - name: fusion_comp_mode
    type: string
    description: Fusion composition mode
    default: "Over"

tags: [fusion, fairlight, vfx, grid warp, paint, clone, object removal, pipeline, compositing, text+, davinci resolve]
category: davinci-resolve-fusion
---

# DaVinci Resolve Fusion & Fairlight VFX Pipeline

Fusion page visual effects workflows and Fairlight-to-Fusion post-production pipeline management for VFX-heavy projects.

## Skills Included

1. **Luffy Stretch / Grid Warp Distortion** — Rubber-hose character distortion
2. **Object Removal using Paint/Clone** — Wire/rig/blemish removal
3. **FVPM — Fairlight VFX Pipeline Management** — Organized audio→color→VFX→final grade pipeline
4. **Fusion Node Graph Basics** — Core compositing nodes and connections
5. **Text+ & Title Animation** — Motion graphics text in Fusion

## Quick Reference

| Task | Page | Nodes | Difficulty |
|------|------|-------|------------|
| Grid Warp distortion | Fusion | MediaIn, Grid Warp, Transform, MediaOut | Intermediate |
| Object removal (Clone) | Fusion | MediaIn, Paint, Merge, MediaOut | Intermediate |
| Fairlight→VFX pipeline | All pages | Color Correction → Fusion VFX | Intermediate |
| Basic comp | Fusion | MediaIn, Merge, Transform, MediaOut | Beginner |
| Text+ animation | Fusion | Text+, Merge, Transform | Beginner |

## Tips

- **Grid Warp**: Higher mesh density = more control but heavier computation; use "Bilinear" for smoother results
- **Paint Clone**: Hold Alt+Click to set source point; use "Smart" stroke for auto-feathering
- **Paint Animation**: Keyframe stroke Center point for moving objects; use multiple strokes for complex removal
- **Fusion Pipeline**: Color grade BEFORE sending to Fusion for consistent lighting; final grade AFTER VFX
- **Fairlight First**: Sync and clean audio in Fairlight before picture lock to avoid re-syncing VFX
- **Text+**: Use "Write On" effect for typewriter animation; "Following" path for text on curve

## Fusion Node Reference

| Node | Purpose | Common Use |
|------|---------|------------|
| MediaIn | Source input | Footage, images |
| MediaOut | Final output | Render result |
| Merge | Combine A over B | Compositing layers |
| Transform | Position/Scale/Rotate | Match move, animation |
| ColorCorrector | Grade (Lift/Gamma/Gain) | Quick color fix |
| Blur | Soften | Edge feather, DOF |
| Grid Warp | Mesh distortion | Character stretch, morph |
| Paint | Clone/Brush/Rotoscoping | Object removal, cleanup |
| Text+ | Advanced text | Titles, motion graphics |
| Tracker | Planar/Point tracking | Match move, stabilize |

## Related Skills

- `davinci-resolve-techniques/davinci-masking-compositing` — Power Windows, Magic Mask, tracking
- `davinci-resolve-techniques/davinci-color-grading-fundamentals` — Color pipeline before/after VFX
- `davinci-resolve-techniques/davinci-depth-map-grading` — Depth Map for 3D compositing (Studio)