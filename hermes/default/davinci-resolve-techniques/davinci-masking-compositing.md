---
name: davinci-masking-compositing
description: Masking, compositing, and text-behind-subject techniques in DaVinci Resolve — Power Windows, Magic Mask, Polygon masks, Fusion compositing
trigger: Use when isolating subjects, creating text-behind-subject effects, compositing layers, or tracking masks in DaVinci Resolve
steps:
  - name: Text Behind Subject (Edit Page - Power Window)
    description: Place text behind a moving subject using Power Window on Color page
    resolve_page: Edit|Color
    difficulty: intermediate
    key_nodes: [Background Clip, Duplicate Clip, Text+]
    parameters:
      mask_method: "Power Window or Magic Mask"
      feathering: "Soft"
      blend_mode: "Normal"
    steps:
      - Place your video clip on the timeline
      - Duplicate the clip (Alt+Drag) to create a second layer directly above
      - Add a Text+ title on a layer between the two video clips
      - Select the top video clip and go to Color page
      - Use the Power Window or Magic Mask to isolate the subject
      - Track the mask across the clip to follow the movement
      - Adjust the text layer position so it appears behind the masked subject
    tags: [masking, text effect, motion tracking, compositing, text behind subject]

  - name: Text Behind Subject (Fusion Page - Depth Masking)
    description: Advanced text-behind-subject using Fusion Magic Mask and Alpha channel
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [Text+, Alpha Output, Magic Mask]
    parameters:
      font_style: "Bold Serif"
      tracking: "wide"
      mask_softness: "low-to-medium"
    steps:
      - Import the clip to the Fusion page
      - Add a Text+ node and type the desired text
      - Use the Magic Mask tool or manual Polygon mask to select the subject
      - Connect the mask to the Alpha channel of the Text+ node
      - Adjust the text position so the subject overlaps with the letters
      - Merge the masked text over the original background footage
    tags: [vfx, text-effect, masking, fusion, davinci-resolve, depth masking]

  - name: Selective Subject Polygon Masking
    description: Custom polygon window with tracking for selective color grading
    resolve_page: Color
    difficulty: intermediate
    key_nodes: [Qualifier/Window, Primary Grade]
    parameters:
      window_type: "Polygon"
      tracking: "Active"
      offset: "25.00"
    steps:
      - Go to the Color page
      - Select the Polygon Window tool from the Window tab
      - Draw a custom path around the desired subject
      - Go to the Tracker tab and click play to track the mask to subject movement
      - Apply color adjustments using Primary Wheels or Curves to affect masked area
    tags: [masking, color-grading, polygon, isolation, power window, tracking]

  - name: Magic Mask (AI-Powered)
    description: Use DaVinci Resolve's AI Magic Mask for automatic subject isolation
    resolve_page: Color|Fusion
    difficulty: intermediate
    key_nodes: [Magic Mask, Tracker]
    parameters:
      mode: "F (forward) | B (backward) | BI (bidirectional)"
      feather: "adaptive"
      refinement: "enabled"
    steps:
      - Select clip on Color page
      - Open Magic Mask panel (Color page toolbar)
      - Draw rough stroke over subject
      - Choose tracking mode (F/B/BI)
      - Click Track — AI generates and tracks mask
      - Refine with feather, expansion, cleanup strokes
      - Use mask for grading, blur, or compositing
    tags: [magic mask, ai masking, subject isolation, tracking, davinci resolve studio]

  - name: Power Window Shapes & Tracking
    description: Built-in window shapes (circle, square, curve, gradient) with tracker
    resolve_page: Color
    difficulty: beginner
    key_nodes: [Window, Tracker]
    parameters:
      shapes: ["Circle", "Square", "Curve", "Gradient", "Polygon"]
      tracking: "Position, Rotation, Zoom, 3D"
      feather: "Inside/Outside"
    steps:
      - Open Window panel on Color page
      - Select shape tool (Circle, Square, Curve, Gradient, Polygon)
      - Draw shape over area of interest
      - Open Tracker panel → select tracking mode
      - Track forward/backward
      - Adjust feather, position, shape as needed
    tags: [power window, window, tracking, color grading, vignette, shape]

parameters:
  - name: mask_feather
    type: number
    description: Mask feather amount (0-100)
    default: 10
  - name: tracking_mode
    type: string
    description: Magic Mask tracking mode
    default: "BI"
  - name: window_shape
    type: string
    description: Power Window shape type
    default: "Circle"

tags: [masking, compositing, power window, magic mask, polygon, tracking, text behind subject, fusion, davinci resolve]
category: davinci-resolve-masking
---

# DaVinci Resolve Masking & Compositing

Essential masking and compositing techniques covering Power Windows, Magic Mask (AI), polygon windows, and Fusion-based depth compositing for text-behind-subject effects.

## Skills Included

1. **Text Behind Subject (Edit Page)** — Power Window + duplicate clip method
2. **Text Behind Subject (Fusion Page)** — Magic Mask + Alpha channel compositing
3. **Selective Subject Polygon Masking** — Custom polygon with tracker
4. **Magic Mask (AI-Powered)** — AI subject isolation and tracking
5. **Power Window Shapes & Tracking** — Built-in shapes with multi-parameter tracking

## Quick Reference

| Task | Page | Method | Difficulty |
|------|------|--------|------------|
| Text behind subject | Edit/Color | Power Window + duplicate | Intermediate |
| Text behind subject | Fusion | Magic Mask + Alpha | Intermediate |
| Selective grading | Color | Polygon Window | Intermediate |
| AI subject mask | Color/Fusion | Magic Mask | Intermediate |
| Vignette/spot grade | Color | Circle/Square Window | Beginner |

## Tips

- **Magic Mask requires DaVinci Resolve Studio** (free version has limited tracking)
- For text behind subject: Alt+drag clip to duplicate, place Text+ between layers
- Polygon window: fewer points = smoother tracking; add points only where needed
- Tracker modes: Position only (fast) → Position+Rotation → Position+Rotation+Zoom → 3D
- Use "Invert" on window to affect everything EXCEPT the masked area
- Save complex masks as PowerGrades for reuse across clips

## Related Skills

- `davinci-resolve-techniques/davinci-color-masking-tracking` — Advanced tracking, stabilize, refine
- `davinci-resolve-techniques/davinci-fusion-compositing` — Fusion node-based compositing
- `davinci-resolve-techniques/davinci-depth-map-grading` — Depth Map for 3D masking (Resolve 20+ Studio)