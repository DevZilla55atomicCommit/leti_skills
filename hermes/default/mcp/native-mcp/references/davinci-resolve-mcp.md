# DaVinci Resolve MCP Server Configuration Reference

Discovered during session: connecting Hermes Agent to DaVinci Resolve via MCP.

## Available MCP Servers

### 1. samuelgursky/davinci-resolve-mcp (Recommended — 1.4k stars)
- **Tools**: 34 compound / 341 full (granular)
- **Works with**: DaVinci Resolve 18.5+ **Free and Studio**
- **Language**: Python 3.10+ (3.10-3.12 lowest risk; 3.13/3.14 work on Resolve 20.3.2+)
- **Install**: `npx davinci-resolve-mcp setup` or `pip install davinci-resolve-mcp`
- **Launch**: `npx davinci-resolve-mcp server` (compound) or `npx davinci-resolve-mcp server --full` (granular)
- **Features**: Full API coverage (100%), source-safe media analysis, local control panel, Fusion/Fairlight/Color/Render/Timeline/Media Pool

### 2. guycochran/resolve-mcp-server (53 stars)
- **Tools**: 53 across 11 categories
- **Requires**: **DaVinci Resolve Studio (paid)** — scripting API not in free version
- **AI Vision**: Moondream API (requires API key, free tier available)
- **Remote Access**: HTTP mode + Cloudflare Tunnel support
- **Install**: Manual venv + pip install requirements

## macOS Paths (DaVinci Resolve 21.0.2 Free)

| Variable | Path |
|----------|------|
| `RESOLVE_SCRIPT_API` | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting` |
| `RESOLVE_SCRIPT_LIB` | `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so` |
| `PYTHONPATH` | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules` |
| `DAVINCI_RESOLVE_MCP_PYTHON` | `/opt/homebrew/bin/python3.11` (or your preferred Python 3.10-3.12) |

## Hermes Config Snippet

Add to `~/.hermes/config.yaml` under `mcp_servers:`:

**Option A: Using managed install (recommended — auto-updates, validated paths)**
```yaml
davinci-resolve:
  command: "/opt/homebrew/opt/python@3.11/bin/python3.11"
  args:
    - "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"
  env:
    RESOLVE_SCRIPT_API: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB: "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
```

**Option B: Using npx (auto-installs but slower startup)**
```yaml
davinci-resolve:
  command: npx
  args:
    - "-y"
    - davinci-resolve-mcp
    - server
  env:
    RESOLVE_SCRIPT_API: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB: "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
    DAVINCI_RESOLVE_MCP_PYTHON: "/opt/homebrew/bin/python3.11"
```

> **Key learning from session**: Option A (managed install) is preferred. The `npx davinci-resolve-mcp doctor` command outputs the exact paths. The managed install handles Python venv, dependency isolation, and auto-updates.

## Prerequisites

1. **DaVinci Resolve running** with Preferences → General → "External scripting using" set to **Local**
2. **Node.js** installed (for `npx`)
3. **Python 3.10-3.12** recommended (3.13/3.14 work on Resolve 20.3.2+)
4. **MCP SDK** installed: `pip install mcp` (already present in this environment)

## Important: Config File Editing

**Hermes blocks direct writes to `~/.hermes/config.yaml`** for security. You cannot use `patch` tool or `write_file` tool on this file. Instead:

- Use `hermes config edit` to open in your editor
- Or manually edit the file with your preferred editor
- The agent can read the config but not write it directly

## Tool Naming

Tools will be registered as `mcp_davinci_resolve_*`:
- `mcp_davinci_resolve_resolve_control` — app/project control
- `mcp_davinci_resolve_media_pool` — media pool operations
- `mcp_davinci_resolve_timeline_item` — timeline editing (retime, transform, crop, composite, audio, keyframes)
- `mcp_davinci_resolve_analyze_media` — source-safe analysis with visual/transcription
- `mcp_davinci_resolve_color` — color grading (CDL, LUTs, node graph)
- `mcp_davinci_resolve_fusion` — Fusion compositions
- `mcp_davinci_resolve_render` — render queue management
- `mcp_davinci_resolve_setup` — config and diagnostics

## Verification

After adding config and restarting Hermes, test with:
- "List all DaVinci Resolve projects"
- "Get current timeline info"
- "Show media pool contents"

### Session Learnings (July 2025)

### DaVinci Resolve Free Edition Works!
The samuelgursky/davinci-resolve-mcp server works with **DaVinci Resolve Free** (not just Studio). The free edition supports external scripting for the Fusion page. Resolve 21.0.2 Free was successfully connected.

### Critical: External Scripting Must Be "Local"
In DaVinci Resolve Preferences → General → "External scripting using" **must be set to "Local"**. This is NOT the default. Without this, the scripting API returns no connection.

Set via terminal if needed:
```bash
defaults write com.blackmagic-design.DaVinciResolve21 GeneralExternalScriptingUsing -string "Local"
```
Then restart Resolve.

### Hermes Config: Cannot Write Directly
**Hermes blocks direct writes to `~/.hermes/config.yaml`** via `patch` or `write_file` tools. The agent can read but not modify this security-sensitive file.

**Workaround**: Use `hermes config edit` to open in editor, or manually edit with your preferred editor. The agent can generate the exact YAML snippet needed.

### Managed Install vs npx
The `npx davinci-resolve-mcp doctor` command reveals the managed install paths. The managed install (Option A) is preferred because:
- Creates isolated Python venv with correct dependencies
- Handles dependency isolation
- Auto-updates via GitHub releases
- `doctor` command outputs exact config for any MCP client

### Server Mode: Compound (34 tools) vs Full (341 tools)
The compound server (`src/server.py`) is the default and recommended. It groups related Resolve operations behind action parameters to keep context usage low. The full/granular server (`src/resolve_mcp_server.py` or `--full` flag) exposes one MCP tool per Resolve API method — for power users who need maximum granularity.

### Tool Call Pattern
All tools follow the pattern: `action` + `params`. Examples:
- `resolve_control(action="get_version")`
- `project_manager(action="list")`
- `timeline(action="get_current")`
- `media_pool(action="get_root_folder")`
- `timeline_item(action="get_transform", params={...})`

### Testing Without Hermes Restart
You can test the MCP server directly via stdio:
```bash
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "resolve_control", "arguments": {"action": "get_version"}}}' | "/opt/homebrew/opt/python@3.11/bin/python3.11" "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"
```

### Resolve Must Be Running
The MCP server auto-launches Resolve if not running (may take up to 60s on first call). For faster response, keep Resolve running with a project open.

---

### Additional Session Learnings (July 2025 - Extended Session)

### Hermes mcp test Timeout Issue
The `hermes mcp test <server>` command has a **hardcoded ~8 second timeout** that doesn't respect the `connect_timeout` config setting. The DaVinci Resolve MCP server takes ~8-12 seconds to fully initialize and connect to Resolve's scripting API, causing the test to fail even though the server works perfectly when called directly.

**Workaround**: The test command failure is a false negative. The server works correctly in actual use. Test manually via stdio pipe to verify.

### Config Timeout Settings Still Helpful
Even though `hermes mcp test` ignores them, the `timeout` and `connect_timeout` settings in config.yaml are still useful for actual tool calls during conversation. Set generous values:
```yaml
davinci-resolve:
  command: "/opt/homebrew/opt/python@3.11/bin/python3.11"
  args:
    - "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"
  env:
    RESOLVE_SCRIPT_API: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB: "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
  timeout: 300          # 5 minutes per tool call
  connect_timeout: 120  # 2 minutes for initial connection
```

### mcp_discovery_timeout Config
The global `mcp_discovery_timeout` setting (default 1.5s) is too short for DaVinci Resolve MCP. Increase it:
```yaml
mcp_discovery_timeout: 30.0  # Allow 30 seconds for tool discovery
```
This is separate from per-server `connect_timeout`.

### Environment Variables Must Be Passed Explicitly
The `npx davinci-resolve-mcp server` launcher may not pass the required environment variables (`RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, `PYTHONPATH`) to the subprocess. The **managed install (direct Python path)** is more reliable because the `doctor` command outputs the exact environment needed.

### Resolve Free Edition Limitations
While the free edition works for Fusion page scripting, some features may be limited compared to Studio. Tested working: project management, media pool, timeline operations, Fusion compositions, basic color grading. Color page advanced features may require Studio.

### Project Must Be Open for Timeline Operations
If no project is loaded, `timeline` and `timeline_item` tools will return "No current timeline" or similar errors. Always ensure a project is open and a timeline is active before using timeline tools.

### Color Page Must Be Active for Some Operations
Some color grading tools require the Color page to be active. Use `resolve_control(action="open_page", params={"page": "color"})` if needed.

### Node.js Not Required After Setup
Once the managed install is complete (`npx davinci-resolve-mcp setup`), Node.js is no longer required. The MCP server runs as a Python process directly.

### Verification Checklist After Config Changes
1. Restart Hermes completely (Cmd+Q → relaunch)
2. Run `hermes mcp list` — should show "davinci-resolve" as "enabled"
3. Ignore `hermes mcp test davinci-resolve` failures (known timeout issue)
4. Test in conversation: "List my DaVinci Resolve projects" or "Get current timeline info"