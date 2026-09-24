---
name: davinci-sunset-beach-montage
description: DaVinci Resolve technique: Sunset Beach Montage from Instagram Reel DAQ30GGP5tj
category: creative/davinci-resolve-techniques
tags: ["montage", "triptych", "sunset", "beach", "editing", "layout", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DAQ30GGP5tj"
collection: "DaVinci_Tricks"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Sunset Beach Montage

**Source:** Instagram Reel `DAQ30GGP5tj` (DaVinci_Tricks)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Sunset Beach Montage](DAQ30GGP5tj.gif)

## Node Graph Structure

- Timeline
- Clip
- Transform

## Parameters

- **scaling**: Zoom in/out to frame each panel
- **positioning**: Adjust X/Y position to create the triptych layout
- **cropping**: Crop to create distinct panels if needed

## Steps to Reproduce in DaVinci Resolve

1. Import the video clip into DaVinci Resolve.
2. Place the clip on the timeline.
3. Duplicate the clip two times to create three identical clips stacked on top of each other.
4. On the first clip (top panel), use the Transform controls in the Inspector to scale and position it to fill the top third of the frame.
5. On the second clip (middle panel), use the Transform controls to scale and position it to fill the middle third of the frame.
6. On the third clip (bottom panel), use the Transform controls to scale and position it to fill the bottom third of the frame.
7. Adjust the scaling and positioning of each clip until the desired triptych layout is achieved.

## Tags
`montage`, `triptych`, `sunset`, `beach`, `editing`, `layout`
