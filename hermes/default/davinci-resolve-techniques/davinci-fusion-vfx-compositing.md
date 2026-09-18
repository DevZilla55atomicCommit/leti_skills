---
name: davinci-fusion-vfx-compositing
description: Fusion page VFX and compositing techniques - text behind subject, warp distortion, object removal, depth masking
category: davinci-resolve
tags: [fusion, vfx, compositing, text-effects, masking, warp, object-removal, paint, grid-warp]
trigger: Use when user asks about Fusion page, VFX, compositing, text behind subject, warp effects, object removal, or masking in Fusion
---

# DaVinci Resolve Fusion VFX & Compositing

Advanced Fusion page techniques for visual effects, compositing, and motion graphics extracted from Instagram Reels.

## Techniques Included

### 1. Text Behind Subject (Masking Overlay - Edit Page Method)
**Video ID:** `C-Nty_eP-Rk` | **Difficulty:** Intermediate | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Background Clip, Duplicate Clip, Text+
- **Parameters:** Mask Method: Power Window or Magic Mask, Feathering: Soft, Blend Mode: Normal
- **Steps:**
  1. Place your video clip on the timeline
  2. Duplicate the clip (Alt+Drag) to create a second layer directly above
  3. Add a Text+ title on a layer between the two video clips
  4. Select the top video clip and go to Color page
  5. Use the Power Window or Magic Mask to isolate the subject
  6. Track the mask across the clip to follow the movement
  7. Adjust the text layer position so it appears behind the masked subject
- **Tags:** masking, text effect, motion tracking, compositing

### 2. Text Behind Subject (Depth Masking - Fusion Page Method)
**Video ID:** `C_x0IZRODYf` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Serial
- **Key Nodes:** Text+, Alpha Output, Magic Mask
- **Parameters:** Font Style: Bold Serif, Tracking: Wide, Mask Softness: Low-to-Medium
- **Steps:**
  1. Import the clip to the Fusion page
  2. Add a Text+ node and type the desired text (GLOW TEXT EFFECT)
  3. Use the Magic Mask tool or a manual Polygon mask to select the subject (the person)
  4. Connect the mask to the Alpha channel of the Text+ node
  5. Adjust the text position so the subject overlaps with the letters
  6. Merge the masked text over the original background footage
- **Tags:** vfx, text-effect, masking, fusion, davinci-resolve

### 3. Luffy Stretch / Warp Distortion
**Video ID:** `C-nf4xytQUu` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Serial
- **Key Nodes:** MediaIn, Grid Warp, Transform, MediaOut
- **Parameters:** Grid Warp Type: Bilinear, Mesh Density: High, Smoothness: Medium
- **Steps:**
  1. Add the clip to the Fusion page
  2. Add a Grid Warp node after the MediaIn
  3. Increase the mesh density to allow for finer control over the subject limbs
  4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
  5. Apply a Transform node to adjust the final framing after the distortion
  6. Add a Blur node if necessary to soften the edges of the distortion
- **Tags:** fusion, warp, vfx, onepiece, specialeffects

### 4. Object Removal using Patch Replacement / Clone
**Video ID:** `C_yv2diSvey` | **Difficulty:** Intermediate | **Page:** Fusion | **Node Graph:** Layer Mixer
- **Key Nodes:** MediaIn, Paint Node, Merge, MediaOut
- **Parameters:** Paint Tool: Clone, Stroke Type: Smart, Opacity: 1.0
- **Steps:**
  1. Import the clip into the Fusion page
  2. Add a Paint node and connect it after MediaIn
  3. Select the Paint tool and choose Clone mode
  4. Hold Alt and click on a clean source area near the fishing wire
  5. Paint over the fishing wire to cover it with the clean pixels
  6. Adjust stroke smoothness to blend the patch seamlessly
- **Tags:** davvinciresolve, vfx, objectremoval, fusion

---

## Usage Notes

### Text Behind Subject - Two Approaches
| Approach | Page | Best For |
|----------|------|----------|
| Duplicate Clip + Power Window | Edit/Color | Quick editorial workflow, simple backgrounds |
| Fusion Magic Mask + Alpha | Fusion | Complex motion, multiple subjects, refined edges |

### Grid Warp Tips
- **Mesh Density:** Higher = more control but more keyframes needed
- **Keyframe Strategy:** Keyframe on major movement beats, let interpolation handle in-betweens
- **Edge Handling:** Add slight blur to warped edges to hide stretching artifacts
- **Transform After Warp:** Always use Transform node post-warp for final framing

### Paint Node Clone Workflow
- **Source Selection:** Alt+Click on clean reference area (hold Alt, click)
- **Stroke Type:** "Smart" stroke blends better; "Normal" for precise control
- **Multiple Strokes:** Use multiple small strokes rather than one large stroke
- **Temporal Consistency:** Clone from adjacent frames for moving objects (use time offset)

### Fusion Node Graph Conventions
- **Left to Right:** MediaIn → Processing Nodes → MediaOut
- **Merge Node:** Foreground (green input) over Background (yellow input)
- **Mask Input:** Blue input on most tools for alpha masking
- **Viewers:** Dual viewers (1/2) for comparing before/after

---

## Skill Trigger Examples

- "How do I put text behind a person in DaVinci Resolve?"
- "Create a rubber stretch warp effect like One Piece Luffy"
- "Remove an object using the Paint node in Fusion"
- "Text behind subject masking tutorial"
- "Fusion page compositing workflow"
- "Grid Warp node keyframing tips"