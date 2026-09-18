# DaVinci Resolve MCP Server Configuration Reference

Discovered during session: connecting Hermes Agent to DaVinci Resolve via MCP.

## Available MCP Servers

### 1. samuelgursky/davinci-resolve-mcp (Recommended — 1.4k+ stars, actively maintained)
- **Tools**: 32 compound / 329+ full (granular) — covers 100% of Resolve Scripting API
- **Works with**: DaVinci Resolve 18.5+ **Free and Studio**
- **Language**: Python 3.10+ (3.10-3.12 lowest risk; 3.13/3.14 work on Resolve 20.3.2+)
- **Install**: `npx davinci-resolve-mcp setup` or `pip install davinci-resolve-mcp`
- **Launch**: `npx davinci-resolve-mcp server` (compound) — auto-detects paths
- **Features**: Full API coverage, source-safe media analysis, local control panel, Fusion/Fairlight/Color/Render/Timeline/Media Pool, versioning, color grade boundary reports, bulk matching

### 2. guycochran/resolve-mcp-server (53 stars)
- **Tools**: 53 across 11 categories
- **Requires**: **DaVinci Resolve Studio** (paid) — scripting API not in free version
- **Features**: Moondream AI Vision for frame analysis, HTTP mode with Cloudflare tunnels for remote access
- **Launch**: `TRANSPORT=http PORT=3001 python src/server.py`

## Hermes MCP Configuration for DaVinci Resolve (Current Working Setup)

Add to `~/.hermes/config.yaml` under `mcp_servers:`

```yaml
mcp_servers:
  davinci-resolve:
    command: "npx"
    args:
      - "-y"
      - "davinci-resolve-mcp"
    timeout: 120
    connect_timeout: 60
```

**Note:** The `davinci-resolve-mcp` package auto-detects Resolve paths on macOS/Windows/Linux — no manual env vars needed in most cases.

### Prerequisites
1. **DaVinci Resolve running** with Preferences → General → "External scripting using" = **Local**
2. **Python 3.10+** installed (3.11 recommended for macOS Homebrew)
3. **MCP Python SDK** installed: `pip install mcp`
4. **Node.js/npx** available for npm-based launch

### macOS Paths (DaVinci Resolve 21+ Free/Studio) — auto-detected
| Component | Path |
|-----------|------|
| Scripting API | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting` |
| Modules (DaVinciResolveScript.py) | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules` |
| Fusion Script Library | `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so` |

## Available Tool Namespaces (after connection)

Tools are prefixed with `mcp_davinci_resolve_`:

| Namespace | Compound Tools | Description |
|-----------|----------------|-------------|
| `resolve_control` | 1 | App/project control, version, page switching |
| `project_manager` | 5 | Projects, databases, folders, cloud |
| `timeline` | 4 | Timelines, tracks, structure |
| `timeline_item` | 5 | Retime, transform, crop, composite, audio |
| `timeline_item_color` | **Main color tool** | CDL, LUTs, node graph, versions, gallery, color groups, bulk match |
| `timeline_item_takes` | 1 | Take management |
| `gallery` | 1 | Album management |
| `gallery_stills` | 1 | **Grab/export stills + .drx grades** |
| `media_pool` | 3 | Import, bins, clips, metadata |
| `media_analysis` | 1 | Source-safe analysis, vision, transcription |
| `timeline_markers` | 2 | Markers, thumbnails, frame images |
| `graph` | 1 | Raw node graph operations |
| `fusion_comp` | 2 | Fusion compositions |
| `render` | 2 | Queue, settings, Quick Export |
| `script_plugin` | 1 | Extension authoring |
| **Total** | **32+** | Compound mode |

Full/granular mode exposes **300+ tools** (one per API method) via `--full` flag.

## Key Color Grading Tools (New in v2.58+)

| Tool | Key Actions |
|------|-------------|
| `timeline_item_color` | `grade_evidence_base`, `grade_boundary_report`, `probe_node_graph`, `safe_set_cdl`, `safe_copy_grade`, `safe_apply_drx`, `safe_export_lut`, `bulk_match_to_hero`, `propose_grade`, `grade_version_snapshot/restore` |
| `gallery_stills` | `grab_and_export` — grabs still from current frame, exports `.dpx` + `.drx` |
| `media_analysis` | `analyze_clip`, `analyze_bin`, `analyze_project`, `commit_vision` (host_chat_paths protocol) |

## Pitfalls & Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `scriptapp("Resolve")` returns `None` | Python 3.13+ on older Resolve build | Use Python 3.10-3.12 or upgrade Resolve to 20.3.2+ |
| "Failed to connect to MCP server" | npx not on PATH or package not found | Ensure Node.js installed; try `npx -y davinci-resolve-mcp server` manually first |
| Tools not appearing | Config indentation error or wrong section | Verify YAML under `mcp_servers:` (not `mcp:` or `servers:`) |
| Free version limitations | Some APIs require Studio | samuelgursky server works on Free for Fusion page; guycochran requires Studio |
| `args` written as string | `hermes config set` writes arrays as strings | **Fix:** Edit YAML manually or use `execute_code` with PyYAML to write proper array |

## Verification Steps

1. Add config to `~/.hermes/config.yaml`
2. **Restart Hermes Agent** (native MCP client connects at startup only — no hot-reload)
3. Ask agent: `"List available MCP tools"` → should show `mcp_davinci_resolve_*` tools
4. Test: `"Call mcp_davinci_resolve_timeline_item_color with action='grade_boundary_report' for the current clip"`

## MCP edit-session build order

Connection order: `resolve_control.runtime_mode` → `get_version` → `project_manager.get_current` → `project_settings.project_summary` (pool inventory + timeline count) → `project_settings.get_setting` (confirm fps, resolution, color science from the live project — never assume) → `media_pool.create_timeline` → `media_pool.append_to_timeline` in story order → color-group assign → `project_manager.save` after every mutation.

- `probe_clip_properties` and `probe_edit_kernel_item` require explicit `clip_ids` (or `selected=True`) — bare calls error out, so carry IDs forward from `project_summary` / append readbacks.
- Bulk per-item ops (e.g. `assign_color_group` across N timeline items) are one call per item: Hermes `tool_call` accepts a single local invocation per call, so fan out with one single-entry `tool_call` per message in the same turn, then verify once (e.g. `color_group.get_clips`) instead of reading back each item.
- Trust the `before`/`after` item-count readback on appends over the `success` flag alone — it confirms which track each item actually landed on.

## Verified API limits — build these by hand in the Resolve UI

The scripting API exposes no primitive for these; failed calls return generic errors, so do not retry — hand off a click recipe instead:

- Timeline transitions (Cross Dissolve, Dip to Black): `edit_kernel_capabilities` lists `transition_cloning` as unsupported and there is no add-transition action.
- Opacity/transform keyframes: `AddKeyframe` / `GetKeyframeCount` report unavailable on video timeline items — fades, push-ins, and text reveals must be keyframed on the Edit page.
- `timeline.insert_title` / `insert_fusion_title` fail even with the Edit page active — create Text+ titles by hand (Effects Library → Titles → Text+).
- Group Pre-Clip / Post-Clip CST nodes: the API can create the group (`add_color_group`) and assign clips to it, but cannot author nodes inside it — set the input/output CSTs on the Color page or via a `.drx` PowerGrade.
- Clip speed has no safe setter (`timeline_item.set_retime` only sets the interpolation process, not speed %) — set slow-mo percentages in Clip Attributes / Retime Curve by hand.

## Session-Specific Notes (2025-07-06)

- **Config fix applied:** `hermes config set` wrote `args` as a string `'["-y", "davinci-resolve-mcp"]'` instead of YAML array. Fixed via `execute_code` with PyYAML.
- **Restart required:** After config change, Hermes must be fully restarted (`/quit` in TUI, or quit desktop app).
- **Resolve must be running** for first tool call (auto-launches if not, ~30-60s first call).
- **External scripting** must be enabled in Resolve Preferences → General.