---
name: davinci-speed-ramp-with-motion-blur-emulation
description: DaVinci Resolve technique: Speed Ramp with Motion Blur Emulation from Instagram Reel DN1VXAp2pkW
category: creative/davinci-resolve-techniques
tags: ["sports", "speed-ramp", "cinematic", "reels", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DN1VXAp2pkW"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Speed Ramp with Motion Blur Emulation

**Source:** Instagram Reel `DN1VXAp2pkW` (Ideas_for_Shooting_Videos)  
**Page:** Edit | **Graph:** serial | **Difficulty:** intermediate

![Speed Ramp with Motion Blur Emulation](DN1VXAp2pkW.gif)

## Node Graph Structure

- Speed Curve
- Optical Flow

## Parameters

- **Ramp Speed**: Variable
- **Flow Type**: Speed Warp
- **Motion Blur**: Enabled

## Steps to Reproduce in DaVinci Resolve

1. Place clip on the timeline and open Inspector
2. Right-click clip and select 'Retime Controls'
3. Add keyframes to the Speed Curve editor to slow down the action and speed up the transitions
4. Go to Inspector > Retime Settings and change Flow Type to 'Speed Warp'
5. Enable Motion Blur to smooth out the fast transitions

## Tags
`sports`, `speed-ramp`, `cinematic`, `reels`
