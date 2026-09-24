---
name: object-removal-using-patch-replacement-clone
description: 'DaVinci Resolve technique: Object Removal using Patch Replacement/Clone
  from Instagram Reel C_yv2diSvey'
category: davinci-resolve
tags:
- davvinciresolve
- vfx
- objectremoval
- fusion
- fusion
- intermediate
version: 1.0.0
source_reel_id: C_yv2diSvey
resolve_page: Fusion
node_graph_type: layer_mixer
key_nodes:
- MediaIn
- Paint Node
- Merge
- MediaOut
parameters:
  Paint Tool: Clone
  Stroke Type: Smart
  Opacity: '1.0'
steps_to_reproduce:
- Import the clip into the Fusion page
- Add a Paint node and connect it after MediaIn
- Select the Paint tool and choose Clone mode
- Hold Alt and click on a clean source area near the fishing wire
- Paint over the fishing wire to cover it with the clean pixels
- Adjust stroke smoothness to blend the patch seamlessly
difficulty: intermediate
---
# Object Removal using Patch Replacement/Clone

**Source Reel:** C_yv2diSvey
**Resolve Page:** Fusion
**Node Graph Type:** layer_mixer
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C_yv2diSvey.

## Key Nodes
- MediaIn
- Paint Node
- Merge
- MediaOut

## Parameters
Paint Tool: Clone
Stroke Type: Smart
Opacity: '1.0'


## Steps to Reproduce
1. Import the clip into the Fusion page
2. Add a Paint node and connect it after MediaIn
3. Select the Paint tool and choose Clone mode
4. Hold Alt and click on a clean source area near the fishing wire
5. Paint over the fishing wire to cover it with the clean pixels
6. Adjust stroke smoothness to blend the patch seamlessly

## Tags
davvinciresolve, vfx, objectremoval, fusion
