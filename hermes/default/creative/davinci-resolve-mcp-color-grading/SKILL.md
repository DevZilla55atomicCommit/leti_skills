---
name: davinci-resolve-mcp-color-grading
description: "Configure and use DaVinci Resolve MCP for AI-assisted color grading workflows in Hermes Agent"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [davinci-resolve, mcp, color-grading, video, creative, ai-assisted]
    related_skills: [hermes-agent, macos-computer-use]
---

# DaVinci Resolve MCP Color Grading

This skill covers the complete workflow for using the DaVinci Resolve MCP server with Hermes Agent to build AI-assisted color grading pipelines: frame extraction → vision model analysis → structured grade recipes → programmatic application via MCP.

## Prerequisites

- DaVinci Resolve Studio (Free works with limited API)
- External Scripting enabled: Preferences → System → General → "External scripting using" → "Local"
- `davinci-resolve-mcp` installed: `npx -y davinci-resolve-mcp setup`
- Hermes config updated with MCP server (see Configuration below)
- OpenRouter API key with access to `anthropic/claude-sonnet-4.6` (recommended) or `openai/gpt-4o` / `google/gemini-2.5-pro`

## Configuration

Add to `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  davinci-resolve:
    command: "npx"
    args: ["-y", "davinci-resolve-mcp"]
    timeout: 120
    connect_timeout: 60
```

**Restart Hermes** after editing config (native MCP client only connects at startup).

## Available MCP Tools

After restart, tools are prefixed `mcp_davinci_resolve_*`:

| Tool | Purpose |
|------|---------|
| `timeline_item_color` | **Main color tool** — grade_evidence_base, bulk_match_to_hero, propose_grade, safe_set_cdl, safe_copy_grade, safe_apply_drx, safe_export_lut, probe_node_graph, grade_boundary_report |
| `gallery_stills` | Grab/export Gallery stills + `.drx` grades |
| `media_analysis` | Analyze clips visually (vision + transcription) |
| `timeline_markers` | Get thumbnails, markers, frame images |
| `resolve_control` | Get version, page, open control panel |
| `project_manager` | Project operations |
| `timeline` | Timeline operations |

## Color Grading Workflow

### 1. Get Current Frame
```
"Call mcp_davinci_resolve_timeline_markers with action='get_thumbnail_image'"
```
Returns MCP Image (visible in chat).

### 2. Analyze with Vision Model
Switch to best grading model:
```
/model anthropic/claude-sonnet-4.6
```
Then:
```
"Analyze this frame for a cinematic teal-orange look. Return structured Resolve node recipe with Lift/Gamma/Gain/Offset values, curves, and LUT recommendations."
```

### 3. Apply Grade (Two Paths)

**Path A: Programmatic (Primary Wheels Only)**
```
mcp_davinci_resolve_timeline_item_color(
  action="safe_set_cdl",
  params={"cdl": {"Slope": [1.05, 1.02, 0.98], "Offset": [0.01, 0.0, -0.01], "Power": [0.99, 1.0, 1.01], "Saturation": 1.05}}
)
```

**Path B: Manual (Full Node Graph)**
Build nodes in Resolve from the model's structured recipe.

### 4. Verify & Iterate
```
"Call mcp_davinci_resolve_timeline_markers with action='get_thumbnail_image'"
```
Model compares new frame to reference → refines directions.

## Advanced: Hero Clip Matching

```python
# 1. Analyze hero clip
media_analysis(action="analyze_clip", params={"selected": true})

# 2. Get evidence base
timeline_item_color(action="grade_evidence_base", params={"min_source_trust": "high"})

# 3. Analyze target bin
media_analysis(action="analyze_bin", params={"recursive": true})

# 4. Match bin to hero (dry run)
timeline_item_color(
  action="bulk_match_to_hero",
  params={
    "hero_id": "<hero-clip-id>",
    "target_ids": ["clip-1", "clip-2"],
    "method": "copy_grade",
    "dry_run": true
  }
)

# 5. Execute with confirm_token
timeline_item_color(action="bulk_match_to_hero", params={... "dry_run": false, "confirm_token": "..." })
```

## Model Selection

| Model | Use Case |
|-------|----------|
| **`anthropic/claude-sonnet-4.6`** (OpenRouter) | **Best** — understands Resolve node architecture, color science, ACES/CST, qualifiers, curves, LUTs |
| `openai/gpt-4o` / `gpt-5.5` | Excellent visual reasoning, good look matching |
| `google/gemini-2.5-pro` | Best multi-frame comparison (hero vs target) |
| `nvidia/neva-22b` / `vila` | **Directional only** — "push Gamma warm" but no precise values, no node graphs |

**NVIDIA VLMs cannot do grading** — they describe images but don't know Resolve controls, color spaces, or node graphs.

## Key MCP Actions Reference

### `timeline_item_color` — Critical Actions

| Action | Description |
|--------|-------------|
| `grade_evidence_base` | **Pre-flight for any grade** — composes version_snapshot + node_graph + color_group + coverage_report into one `evidence_base` line |
| `grade_boundary_report` | Full capabilities + current item snapshot + color groups + Gallery |
| `probe_node_graph` | Inspect item/timeline/color-group graph availability |
| `safe_set_cdl` | Validated CDL with dry_run support — **use for primary wheels** |
| `safe_copy_grade` | Copy grade to N items with dry_run |
| `safe_apply_drx` | Apply `.drx` grade file (replaces graph) |
| `safe_export_lut` | Export LUT to temp path (`.cube`) |
| `bulk_match_to_hero` | Match bin clips to hero (returns confirm_token) |
| `propose_grade` | Formalize recommendation as validated structured output |
| `grade_version_snapshot` / `grade_version_restore` | Non-destructive versioning |

### `gallery_stills` — Critical Actions

| Action | Description |
|--------|-------------|
| `grab_and_export` | Grab still from playhead + export `.dpx` + `.drx` in one call, returns base64 |
| `get_stills` | Count stills in album |
| `export_stills` | Export selected stills |

## Pitfalls & Gotchas

1. **Resolve must be running** — first MCP call auto-launches (30-60s delay)
2. **External Scripting must be "Local"** — not "Network" or "None"
3. **MCP tools need Resolve project open** with timeline on Color page
4. **`safe_set_cdl` only controls primary wheels** — for curves/qualifiers/LUTs, use manual or `safe_apply_drx`
5. **Model sees frames, not live session** — must send thumbnails each iteration
6. **`mcp_servers` config requires restart** — no hot-reload
7. **NVIDIA models ≠ grading models** — they describe, don't prescribe
8. **Version snapshots are automatic** on destructive ops — but call `grade_version_snapshot` before major changes

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| No MCP tools appear | Restart Hermes; check `mcp_servers` YAML syntax |
| "Resolve not running" | Start Resolve; enable External Scripting → Local |
| "Gallery not available" | Open Gallery panel on Color page (Workspace → Gallery) |
| CDL values seem wrong | CDL uses Resolve panel units (Sat 0-100, neutral 50) — model may output 0-1; normalize |
| Permissions errors | Grant Accessibility + Screen Recording to Terminal/Hermes |

## References

- `references/color-grading-workflow.md` — detailed workflow with prompts
- `references/mcp-tools-reference.md` — full tool/action reference
- `references/model-prompts.md` — proven prompts for grading tasks
- `references/instagram-pipeline-integration.md` — **Instagram Reels → DaVinci MCP color analysis integration (v2 Phase 2)** — updated 2026-07-20 with validated Hermes browser tools method (92/93 reels)