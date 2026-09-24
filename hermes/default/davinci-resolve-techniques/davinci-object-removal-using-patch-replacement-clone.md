---
name: davinci-object-removal-using-patch-replacement-clone
description: DaVinci Resolve technique: Object Removal using Patch Replacement/Clone from Instagram Reel C_yv2diSvey
category: creative/davinci-resolve-techniques
tags: ["davvinciresolve", "vfx", "objectremoval", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_yv2diSvey"
collection: "DaVinci_Tricks"
resolve_page: "Fusion"
node_graph: "layer_mixer"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Removal using Patch Replacement/Clone

**Source:** Instagram Reel `C_yv2diSvey` (DaVinci_Tricks)  
**Page:** Fusion | **Graph:** layer_mixer | **Difficulty:** intermediate

![Object Removal using Patch Replacement/Clone](C_yv2diSvey.gif)

## Node Graph Structure

- MediaIn
- Paint Node
- Merge
- MediaOut

## Parameters

- **Paint Tool**: Clone
- **Stroke Type**: Smart
- **Opacity**: 1.0

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Fusion page
2. Add a Paint node and connect it after MediaIn
3. Select the Paint tool and choose Clone mode
4. Hold Alt and click on a clean source area near the fishing wire
5. Paint over the fishing wire to cover it with the clean pixels
6. Adjust stroke smoothness to blend the patch seamlessly

## Tags
`davvinciresolve`, `vfx`, `objectremoval`, `fusion`
