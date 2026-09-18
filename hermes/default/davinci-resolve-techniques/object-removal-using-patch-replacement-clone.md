---
name: Object Removal using Patch Replacement/Clone
description: DaVinci Resolve technique from Instagram Reel C_yv2diSvey
trigger: "object removal using patch replacement/clone"
page: Fusion
difficulty: intermediate
tags: ['davvinciresolve', 'vfx', 'objectremoval', 'fusion']
video_id: C_yv2diSvey
source: instagram-reel
updated: 2026-07-28T10:54:08.243751
---

# Object Removal using Patch Replacement/Clone

**Source:** Instagram Reel `C_yv2diSvey`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** layer_mixer

## Key Nodes
- MediaIn
- Paint Node
- Merge
- MediaOut

## Parameters
- **Paint Tool:** Clone
- **Stroke Type:** Smart
- **Opacity:** 1.0

## Steps to Reproduce
1. Import the clip into the Fusion page
2. Add a Paint node and connect it after MediaIn
3. Select the Paint tool and choose Clone mode
4. Hold Alt and click on a clean source area near the fishing wire
5. Paint over the fishing wire to cover it with the clean pixels
6. Adjust stroke smoothness to blend the patch seamlessly

## Tags
- #davvinciresolve
- #vfx
- #objectremoval
- #fusion
