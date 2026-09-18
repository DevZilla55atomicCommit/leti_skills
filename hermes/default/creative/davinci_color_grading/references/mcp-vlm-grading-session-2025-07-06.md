# MCP + VLM Grading Session Notes (2025-07-06)

## Session Summary
User (Alfred/Maddie) workflow: Professional colorist/creative director using DaVinci Resolve + Hermes Agent. Wants to use NVIDIA VLM models via MCP to analyze frames and get directional color wheel guidance, then apply via Resolve scripting.

## Key Discoveries

### 1. DaVinci Resolve MCP Server
- **Package:** `davinci-resolve-mcp` (npm, v2.58.0)
- **34 compound tools** covering 100% of Resolve Scripting API
- **Key tool:** `timeline_item_color` with actions:
  - `grade_evidence_base` — **always first** (versions + node graph + color groups + coverage)
  - `grade_boundary_report` — full capabilities snapshot
  - `probe_node_graph` — node count, LUTs, cache mode
  - `safe_set_cdl` — validated primary correction (dry-run support)
  - `safe_copy_grade` — copy to N items (dry-run)
  - `safe_apply_drx` — apply .drx (replaces graph, snapshots first)
  - `bulk_match_to_hero` — bin-wide hero matching (confirm_token flow)
  - `propose_grade` — structured recommendation with preview
  - `grade_version_snapshot/restore` — version control

### 2. NVIDIA VLM Models for Grading
| Model | ID | Best For |
|-------|-----|----------|
| NEVA 22B | `nvidia/neva-22b` | Strongest general VLM, good color reasoning |
| VILA | `nvidia/vila` | Multi-frame, temporal reasoning |
| Nemotron Nano 12B VL | `nvidia/nemotron-nano-12b-v2-vl` | Fast/cheap |
| Llama 3.1 Nemotron Nano VL 8B | `nvidia/llama-3.1-nemotron-nano-vl-8b-v1` | Lightweight |

**Endpoint:** `https://integrate.api.nvidia.com/v1` (OpenAI-compatible)
**Auth:** `NVIDIA_API_KEY` env var

### 3. Effective Grading Prompt for VLM
```
You are a colorist assistant. Compare REFERENCE (look to match) vs MY FRAME (current).
For each tonal range, give directional wheel moves:
- Lift (shadows): push crosshair toward [hue], saturation [+/-]
- Gamma (midtones): push crosshair toward [hue], saturation [+/-]
- Gain (highlights): push crosshair toward [hue], saturation [+/-]
- Offset (global): push crosshair toward [hue], saturation [+/-]
Global: Saturation [+/-], Contrast [+/-], Color Boost [+/-]
No exact numbers — I tune by eye. Just directions.
```

### 4. Workflow: Frame-First Grading Loop
1. `timeline_markers.get_thumbnail_image` → returns MCP Image
2. Send to VLM with prompt above
3. Parse directional guidance → derive CDL values
4. `timeline_item_color.safe_set_cdl` with derived CDL
5. `timeline_item_color.grade_version_snapshot` (auto-version)
6. `timeline_markers.get_thumbnail_image` → compare before/after

### 5. Hero Clip Matching (Bin-Wide)
```python
# 1. Analyze hero clip
media_analysis(action="analyze_clip", params={"selected": true})

# 2. Get evidence base
timeline_item_color(action="grade_evidence_base", params={"min_source_trust": "high"})

# 3. Analyze target bin
media_analysis(action="analyze_bin", params={"recursive": true})

# 4. Dry-run match
timeline_item_color(
  action="bulk_match_to_hero",
  params={
    "hero_id": "<hero-clip-id>",
    "target_ids": ["clip-1", "clip-2"],
    "method": "copy_grade",  # or "match_to_reference", "skin_match"
    "dry_run": true
  }
)

# 5. Execute with confirm_token
timeline_item_color(action="bulk_match_to_hero", params={... "dry_run": false, "confirm_token": "..." })
```

### 6. Visual Analysis Pipeline (host_chat_paths)
- `media_analysis(analyze_clip, vision={enabled: true, provider: "host_chat_paths"})`
- Returns `frame_paths` + `vision_token` + JSON schema
- **Must read frames as images**, produce JSON per schema
- Call `media_analysis(commit_vision, params={clip_id, visual: <JSON>, vision_token})`
- **Critical:** Don't skip `commit_vision` — leaves analysis in `pending_host_vision_analysis`

### 7. Config for Hermes
```yaml
# ~/.hermes/config.yaml
mcp_servers:
  davinci-resolve:
    command: "npx"
    args: ["-y", "davinci-resolve-mcp"]
    timeout: 120
    connect_timeout: 60
```

### 8. Prerequisites
- DaVinci Resolve running (Studio preferred)
- External Scripting: Preferences → System → General → "External scripting using" → "Local"
- Project open, timeline on Color page
- First MCP call auto-launches Resolve (~30-60s)

## Pitfalls to Avoid
- ❌ Don't use raw `set_cdl`/`copy_grades` — prefer `safe_*` variants (validation, dry-run)
- ❌ Don't skip `grade_evidence_base` before any grade recommendation
- ❌ Don't forget `commit_vision` — analysis stays pending
- ❌ Don't assume exact numeric values from VLM — it gives directions, you tune
- ❌ Don't apply DRX without `safe_apply_drx` (replaces graph, no append mode)

## Next Steps for User
1. Add MCP config to `~/.hermes/config.yaml`
2. Restart Hermes
3. Start Resolve, open project, go to Color page
4. Test: `mcp_davinci_resolve_timeline_item_color(action="grade_boundary_report")`
5. Then try frame extraction + VLM analysis loop