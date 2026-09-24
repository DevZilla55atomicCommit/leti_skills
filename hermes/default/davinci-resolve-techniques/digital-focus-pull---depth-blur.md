---
name: Digital Focus Pull / Depth Blur
description: DaVinci Resolve technique from Instagram Reel C-tul9VgTZp
trigger: "digital focus pull / depth blur"
page: Fusion
difficulty: intermediate
tags: ['focus-pull', 'depth-of-field', 'fusion', 'cinematic']
video_id: C-tul9VgTZp
source: instagram-reel
updated: 2026-07-28T19:46:41.693345
---

# Digital Focus Pull / Depth Blur

**Source:** Instagram Reel `C-tul9VgTZp`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Gaussian Blur
- Merge

## Parameters
- **Blur Radius:** Interpolated via keyframes
- **Edge Range:** All
- **Softness:** Keyframed adjusted

## Steps to Reproduce
1. Import the clip into the Fusion page.
2. Add a Gaussian Blur node after the MediaIn.
3. Create a Mask (Polygon or Ellipse) to isolate the foreground object.
4. Keyframe the Blur Radius to start at 0 when the object is in focus.
5. Keyframe the Blur Radius to a high value when the focus shifts to the background subject.
6. Adjust the mask feather to ensure a natural transition between planes.

## Tags
- #focus-pull
- #depth-of-field
- #fusion
- #cinematic
