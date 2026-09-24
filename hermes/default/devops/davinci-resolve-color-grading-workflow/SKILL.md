---
name: davinci-resolve-apple-log2-workflow
description: "DaVinci Resolve color grading workflow for Apple Log 2 footage - 8-node Apple Log 2 → DWG → Rec.709 pipeline with CDL corrections per node"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, MCP, CDL, Apple Log 2, DaVinci Wide Gamut]
    related_skills: [native-mcp]
---

# DaVinci Resolve Color Grading Workflow

This skill documents the color grading workflow for DaVinci Resolve using the MCP server (samuelgursky/davinci-resolve-mcp). It covers the 8-node pipeline for Apple Log → DWG → Rec.709 pipeline with per-node CDL corrections.

## Prerequisites

- DaVinci Resolve Studio 18.5+ (tested on 21.0.2)
- Python 3.11+ (3.10-3.12 recommended)
- MCP Python package: `pip install mcp`
- samuelgursky/davinci-resolve-mcp installed via `npx davinci-resolve-mcp setup` or Python installer

## Hermes MCP Configuration

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  davinci-resolve:
    command: "/opt/homebrew/opt/python@3.11/bin/python3.11"
    args:
      - "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"
    env:
      RESOLVE_SCRIPT_API: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
      RESOLVE_SCRIPT_LIB: "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
      PYTHONPATH: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
    timeout: 300
    connect_timeout: 120
plugins:
  enabled:
    - mcp
```

Restart Hermes after adding.

## 8-Node Pipeline Structure

| Node | Label | Purpose | Tools |
|------|-------|---------|-------|
| 1 | (empty) | Base/Input | — |
| 2 | **CST-DWG** | OFX Color Space Transform: Apple Log 2 → DaVinci Wide Gamut | `OFX: Color Space Transform` |
| 3 | **EXP** | Primary Exposure (CDL) | CDL |
| 4 | **WB** | White Balance (CDL) | CDL |
| 5 | **EXP** | Secondary Exposure (CDL) | CDL |
| 6 | **SAT** | Saturation (CDL) | CDL |
| 7 | **CST-OUT** | OFX Color Space Transform: DWG → Rec.709 | `OFX: Color Space Transform` |
| 8 | **Creative Look** | Creative Grade (CDL/LUT) | CDL/LUT |

## Project Settings (Auto Color Management)

```yaml
# Verify/enable via project_settings tool:
isAutoColorManage: "1"
colorSpaceTimeline: "DaVinci WG/Intermediate"
colorSpaceInput: "Apple Log 2"  # Clip-level
colorSpaceOutput: "Rec.709-A"
colorScienceMode: "davinciYRGB"
```

## Key MCP Tools Used

| Tool | Purpose |
|------|---------|
| `mcp_davinci_resolve_project_manager` | List/load projects |
| `mcp_davinci_resolve_project_settings` | Color management settings |
| `mcp_davinci_resolve_media_pool` | Browse clips, probe properties |
| `mcp_davinci_resolve_timeline_item_color` | Grading operations (CDL, versions, LUTs) |
| `mcp_davinci_resolve_graph` | Node graph inspection (labels, tools, LUTs) |
| `mcp_davinci_resolve_media_analysis` | Visual analysis (exposure, waveforms) |

## Workflow Steps

### 1. Load Project & Version
```python
# Load project
mcp_davinci_resolve_project_manager(action="load", params={"name": "My_AI_Colorgrading"})

# Load grading version
mcp_davinci_resolve_timeline_item_color(action="load_version", params={"name": "Apple Log2 to DWG Grade", "type": 0})
```

### 2. Inspect Node Structure
```python
# Get node labels and tools
for i in range(1, 9):
    mcp_davinci_resolve_graph(action="get_node_label", params={"node_index": i, "source": "item"})
    mcp_davinci_resolve_graph(action="get_tools_in_node", params={"node_index": i, "source": "item"})
```

### 3. Apply CDL Corrections Per Node

**Node 3 - Primary Exposure (EXP):**
```python
mcp_davinci_resolve_timeline_item_color(
    action="safe_set_cdl",
    params={
        "cdl": {
            "slope": [1.15, 1.1, 1.05],    # R, G, B gain
            "offset": [0.02, 0.01, 0.0],    # R, G, B lift
            "power": [0.95, 0.98, 1.0],     # R, G, B gamma
            "saturation": 1.0,
            "NodeIndex": 3
        },
        "dry_run": false
    }
)
```

**Node 4 - White Balance (WB):**
```python
mcp_davinci_resolve_timeline_item_color(
    action="safe_set_cdl",
    params={
        "cdl": {
            "slope": [1.05, 1.0, 1.0],     # Slight R gain for warmth
            "offset": [0.0, 0.0, 0.0],
            "power": [1.0, 1.0, 1.0],
            "saturation": 1.0,
            "NodeIndex": 4
        },
        "dry_run": false
    }
)
```

**Node 5 - Secondary Exposure (EXP):**
```python
mcp_davinci_resolve_timeline_item_color(
    action="safe_set_cdl",
    params={
        "cdl": {
            "slope": [1.05, 1.02, 1.0],    # Fine exposure trim
            "offset": [0.01, 0.0, 0.0],
            "power": [1.0, 1.0, 1.0],
            "saturation": 1.0,
            "NodeIndex": 5
        },
        "dry_run": false
    }
)
```

**Node 6 - Saturation (SAT):**
```python
mcp_davinci_resolve_timeline_item_color(
    action="safe_set_cdl",
    params={
        "cdl": {
            "slope": [1.0, 1.0, 1.0],
            "offset": [0.0, 0.0, 0.0],
            "power": [1.0, 1.0, 1.0],
            "saturation": 1.15,             # +15% saturation
            "NodeIndex": 6
        },
        "dry_run": false
    }
)
```

### 4. Visual Analysis (Exposure Check)

```python
# Select clip in Media Pool
mcp_davinci_resolve_media_pool(action="set_selected", params={"clip_ids": ["<media_pool_item_id>"]})

# Run visual analysis
mcp_davinci_resolve_media_analysis(
    action="analyze_clip",
    params={
        "selected": true,
        "include_visuals": true,
        "sampling_mode": "adaptive_capped",
        "include_transcription": false,
        "publish_metadata": false,
        "timed_markers": "no"
    }
)
# Returns frame paths forame paths for visual analysis via host_chat_paths
```

### 5. Commit & Verify
```python
# Load version to ensure changes applied
mcp_davinci_resolve_timeline_item_color(action="load_version", params={"name": "Apple Log2 to DWG Grade", "type": 0})

# Verify grade
mcp_davinci_resolve_timeline_item_color(action="grade_evidence_base", params={"include_coverage": true, "max_nodes": 10})
```

## CDL Parameter Guide

| Parameter | Range | Effect | Typical Range |
|-----------|-------|--------|---------------|
| `slope` (R,G,B) | 0.0-4.0 | Gain/Contrast | 0.9-1.3 |
| `offset` (R,G,B) | -1.0-1.0 | Lift/Shadows | -0.1-0.1 |
| `power` (R,G,B) | 0.1-3.0 | Gamma/Midtones | 0.9-1.1 |
| `saturation` | 0.0-3.0 | Color intensity | 0.8-1.3 |

## Node Indexing Notes

- Node indices are **1-based** (1, 2, 3...)
- `NodeIndex` in CDL params targets specific node
- Without `NodeIndex`, applies to node 1 by default
- Use `dry_run: true` to validate before applying

## Version Management

```python
# Create new version
mcp_davinci_resolve_timeline_item_color(action="add_version", params={"name": "My Grade v2", "type": 0})

# List versions
mcp_davinci_resolve_timeline_item_color(action="get_version_names", params={"type": 0})

# Restore version
mcp_davinci_resolve_timeline_item_color(action="load_version", params={"name": "Version Name", "type": 0})
```

## Visual Analysis via Host Chat Paths

The `analyze_clip` action with `include_visuals: true` returns:
```json
{
  "frame_paths": ["/path/to/frame1.png", "/path/to/frame2.png", ...],
  "schema": {...},
  "confirmation_token": "xxx"
}
```

Read frames as images, produce JSON per schema, then call:
```python
mcp_davinci_resolve_media_analysis(action="commit_vision", params={"clip_id": "...", "visual": {...}, "vision_token": "..."})
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection closed" | Increase `connect_timeout: 120`, `timeout: 300` |
| "No current timeline" | Load project with `project_manager(action="load")` |
| CDL not applying | Use `safe_set_cdl` with `dry_run: true` first, check `NodeIndex` |
| Auto Color Manage not working | Verify `isAutoColorManage=1` and clip `Input Color Space` is set |

## References

- MCP Server: https://github.com/samuelgursky/davinci-resolve-mcp
- DaVinci Resolve Scripting API
- ASC CDL Specification (SOP/SAT)
- Hermes Native MCP Skill: `native-mcp`