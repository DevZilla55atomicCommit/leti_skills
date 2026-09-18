---
name: vault-note-template
description: Template for Obsidian vault notes generated from Instagram reel analysis
---

# {{reel_code}} — {{discipline}}

## Source
- **Reel:** [{{url}}]({{url}})
- **Creator:** {{creator}}
- **Extracted:** {{extracted_date}}
- **Method:** {{method}}
- **Duration:** {{duration}}s

## Caption
{{caption}}

## Discipline Classification
**Primary:** {{discipline}}
**Tags:** {{tags}}

## Technique Analysis

### Overview
{{technique_summary}}

### Key Frames
| Frame | Time | Description |
|-------|------|-------------|
| 0 | 0% | {{frame_0_desc}} |
| 1 | 14% | {{frame_1_desc}} |
| 2 | 28% | {{frame_2_desc}} |
| 3 | 42% | {{frame_3_desc}} |
| 4 | 57% | {{frame_4_desc}} |
| 5 | 71% | {{frame_5_desc}} |
| 6 | 86% | {{frame_6_desc}} |
| 7 | 100% | {{frame_7_desc}} |

### Technical Breakdown
{{technical_breakdown}}

## DaVinci Resolve Node Graph

### Structure
```
Node 01: Primary Correction (Balance/Exposure)
Node 02: Creative Grade (LUT/Look)
Node 03: Texture/Effects (Grain/Halation/Glow)
Node 04: Output Transform (CST/ODT)
```

### Key Parameters
| Node | Tool | Parameter | Value |
|------|------|-----------|-------|
| 01 | Primaries | Lift / Gamma / Gain | {{node01_values}} |
| 02 | Curves/LUT | {{node02_tool}} | {{node02_values}} |
| 03 | OpenFX | {{node03_tool}} | {{node03_values}} |
| 04 | CST | Input/Output Space | {{node04_values}} |

## Assets
Frames: `frames/frame_00.png` – `frames/frame_07.png`
Preview: `reel_{{reel_code}}.gif`

## Metadata
```json
{{metadata_json}}
```

## Links
- [[Videographer/{{discipline}}/{{reel_code}}]] — This note
- `~/.hermes/skills/videographer/reel_{{reel_code}}/SKILL.md` — Hermes skill