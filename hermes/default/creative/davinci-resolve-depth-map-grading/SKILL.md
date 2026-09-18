---
name: davinci-resolve-depth-map-grading
description: "DaVinci Resolve Depth Map grading: Native tool for layer-based grading, atmospheric perspective, and selective masking by distance."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Depth Map, Atmospheric, Masking, Creative Control]
---

# DaVinci Resolve — Depth Map Grading

Learn the **Depth Map** technique from @mastermotion__cinematographer — using DaVinci Resolve's native Depth Map tool to grade by distance layers (foreground/midground/background), create atmospheric perspective, and selectively mask by depth instead of manual rotoscoping.

## When to Use
- Grading by distance layers (FG/MG/BG) independently
- Adding atmospheric haze/fog to background only
- Selective focus/sharpening by distance
- Avoiding manual rotoscoping for depth-based isolation
- "Shaping emotion" through depth-aware creative control

## Prerequisites
- DaVinci Resolve Studio (Depth Map requires Studio)
- Footage with sufficient parallax/depth information
- DaVinci Resolve 18.5+ (Depth Map improved significantly)

## How to Run
Open Depth Map in Color Page → Effects Library → Resolve FX → **Depth Map**. Apply to node, adjust parameters, use output as mask for grading.

## Quick Reference
| Step | Tool | Setting | Purpose |
|------|------|---------|---------|
| 1 | Depth Map OFX | Cleanliness, Balance, Range | Generate clean depth matte |
| 2 | Key Output | Enable | Verify depth map (white=close, black=far) |
| 3 | Layer Mixer | Connect depth as Alpha | Isolate FG/MG/BG for grading |
| 4 | Grade Layers | Independent per layer | Creative control by distance |

## Procedure

### 1. Generate Depth Map
1. Add **Serial Node** (label: `DEPTH_MAP`)
2. Effects Library → Resolve FX → **Depth Map** → Drag to node
3. **Inspector Settings:**
   - **Cleanliness:** 0.5-0.8 (reduce noise in depth)
   - **Balance:** 0.3-0.7 (adapt to scene depth range)
   - **Range:** Auto or manual (near/far clip)
   - **Quality:** High (Studio)
4. **Key Output ON** → Verify: White = Close, Black = Far

### 2. Split by Depth (Layer Mixer)
```
INPUT → [DEPTH_MAP] → Layer Mixer
                    │
                    ├─ FG Layer: Depth Map → Alpha (Invert OFF, threshold high)
                    ├─ MG Layer: Depth Map → Alpha (mid-range)
                    └─ BG Layer: Depth Map → Alpha (Invert ON, threshold low)
```

### 3. Grade Each Layer Independently
| Layer | Typical Grade |
|-------|---------------|
| **FG** | Sharp, saturated, warm, high contrast |
| **MG** | Balanced, natural skin tones |
| **BG** | Desaturated, cool, hazy, low contrast, glow |

### 4. Atmospheric Perspective (The "Breathing" Effect)
- **BG Layer:** Add haze (Lift ↑, Contrast ↓, Saturation ↓, Temp → Cool)
- **Glow OFX** on BG: Large, soft, low intensity
- **FG Layer:** Sharpen, increase clarity, warm highlights

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Noisy/blocky depth | Low texture, flat lighting | Increase Cleanliness; shoot with more parallax |
| Edges flicker | Temporal instability | Temporal NR before Depth Map; keyframe Balance |
| FG/BG bleed | Threshold too broad | Narrow range per layer; add softness |
| Requires Studio | Depth Map is Studio-only | Manual rotoscope (Free) or upgrade |

## Verification
1. Key Output on Depth Map: Clean grayscale separation
2. Layer Mixer: FG/MG/BG isolated cleanly
3. Scrub timeline: Depth holds, no swimming
4. Toggle layers: Each grades independently

## References
- Source: Instagram @mastermotion__cinematographer — "Depth Map is where your story starts to breathe... It's not just focus, it's how you shape emotion—letting the audience feel every layer in your scene." (4 weeks ago at capture)
- Hashtags: #davinciresolve #cinematography #colorgrading #creativecontrol
- Comment: "Free version?" → Answer: Depth Map is Studio feature

## Related Skills
- `davinci-resolve-cinematic-haze-effect` (Atmospheric haze on BG)
- `davinci-resolve-masking-power-masking` (Magic Mask for subject isolation)
- `davinci-resolve-cinematic-grading-3-mistakes` (Layer structure)