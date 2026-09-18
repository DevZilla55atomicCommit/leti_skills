---
name: reel-skill-template
description: Template for Hermes skills generated from Instagram reel analysis
---

# Reel Technique: {{reel_code}}

## Source
- **URL:** [{{url}}]({{url}})
- **Creator:** {{creator}}
- **Discipline:** {{discipline}}
- **Extraction Method:** {{method}}
- **Duration:** {{duration}}s
- **Extracted:** {{extracted_date}}

## Caption
{{caption}}

## Technique Summary
{{technique_summary}}

### Key Frames
| Frame | Timestamp | Description |
|-------|-----------|-------------|
| 0 | 0% | {{frame_0_desc}} |
| 1 | 14% | {{frame_1_desc}} |
| 2 | 28% | {{frame_2_desc}} |
| 3 | 42% | {{frame_3_desc}} |
| 4 | 57% | {{frame_4_desc}} |
| 5 | 71% | {{frame_5_desc}} |
| 6 | 86% | {{frame_6_desc}} |
| 7 | 100% | {{frame_7_desc}} |

## DaVinci Resolve Implementation

### Node Structure
```
Node 1: Primary Correction (Balance/Exposure)
Node 2: Creative Look (LUT/Grade)
Node 3: Texture/Effects (Grain/Halation/Glow)
Node 4: Output Transform
```

### Key Parameters
| Node | Tool | Parameter | Value |
|------|------|-----------|-------|
| 1 | Primaries | Lift/Gamma/Gain | {{node01_values}} |
| 2 | Curves/LUT | {{node02_tool}} | {{node02_values}} |
| 3 | OpenFX | {{node03_tool}} | {{node03_values}} |
| 4 | CST | Input/Output Space | {{node04_values}} |

## Frame Assets
Frames stored in `frames/` directory:
- `frame_00.png` through `frame_07.png` (8 frames at 0%, 14%, 28%, 42%, 57%, 71%, 86%, 100%)
- `reel_{{reel_code}}.gif` (2fps preview)

## Metadata
```json
{{metadata_json}}
```

## Usage
This skill documents a specific videography technique extracted from an Instagram Reel.
Reference the frame images for visual breakdown. Adapt the node graph template for your footage.

## Tags
{{tags}}