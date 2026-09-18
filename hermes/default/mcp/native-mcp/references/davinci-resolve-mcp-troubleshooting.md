# DaVinci Resolve MCP Troubleshooting Reference

## Common Issues & Solutions

### 1. "Connection closed" / "Connection failed" in `hermes mcp test`

**Symptom:** `hermes mcp test davinci-resolve` fails with "Connection failed (8000ms): Connection closed" but the server works when run manually.

**Root Cause:** The `hermes mcp test` command has a hardcoded ~8 second timeout that doesn't respect the `connect_timeout` config setting. DaVinci Resolve's scripting API takes 10-15 seconds to initialize on first connection.

**Workaround:** 
- Ignore the test failure — the tools still work in conversation
- Or increase `mcp_discovery_timeout: 30.0` in config.yaml (helps but may not fully fix)
- The server auto-launches Resolve if needed, which adds delay

**Verification:** Test manually:
```bash
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "resolve_control", "arguments": {"action": "get_version"}}}' | /opt/homebrew/opt/python@3.11/bin/python3.11 "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"
```

### 2. "No current timeline" Error

**Symptom:** Tools return `{"error": {"message": "No current timeline", ...}}`

**Solution:** Open a timeline in DaVinci Resolve. The project must have at least one timeline created and it must be the active/current timeline.

### 3. External Scripting Not Enabled

**Symptom:** "Resolve Studio may not be installed or external scripting is disabled"

**Solution:** In DaVinci Resolve:
1. Preferences → General
2. Set "External scripting using" to "Local"
3. Restart Resolve

**macOS defaults command:**
```bash
defaults write com.blackmagic-design.DaVinciResolve21 GeneralExternalScriptingUsing -string "Local"
```

### 4. Python Version Issues

**Symptom:** Connection fails on Python 3.13+ with older Resolve builds

**Solution:** Use Python 3.10-3.12 for maximum compatibility. The config uses Python 3.11 explicitly:
```yaml
command: "/opt/homebrew/opt/python@3.11/bin/python3.11"
```

### 5. Resolve Free vs Studio Edition

**Good News:** The samuelgursky/davinci-resolve-mcp server works with **DaVinci Resolve Free** (not just Studio). The free edition supports external scripting for Fusion page operations.

### 6. Config Changes Not Taking Effect

**Solution:** Must **fully quit Hermes** (Cmd+Q) and relaunch. Config is only read at startup.

### 7. Tool Names in Hermes

Tools are prefixed: `mcp_davinci_resolve_<tool_name>`

Examples:
- `mcp_davinci_resolve_resolve_control(action="get_version")`
- `mcp_davinci_resolve_project_manager(action="list")`
- `mcp_davinci_resolve_timeline_item_color(action="grade_evidence_base", params={})`
- `mcp_davinci_resolve_analyze_media(action="analyze", params={...})`

### 8. Environment Variables Required

The server requires these env vars (set in config.yaml):
```yaml
env:
  RESOLVE_SCRIPT_API: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  RESOLVE_SCRIPT_LIB: "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  PYTHONPATH: "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
```

### 9. Multiple Resolve Versions

If you have multiple Resolve versions, the server connects to whichever is running. Use `resolve_control(action="get_version")` to verify.

### 10. Project Must Be Loaded

The server operates on the **currently loaded project** in Resolve. Use `project_manager(action="load", params={"name": "Project Name"})` to switch projects.

---

## Configuration Checklist

- [ ] `pip install mcp` (if not installed)
- [ ] DaVinci Resolve running
- [ ] Preferences → General → External scripting = "Local"
- [ ] Config in `~/.hermes/config.yaml` with correct paths
- [ ] `mcp_discovery_timeout: 30.0` in config
- [ ] Hermes fully restarted (Cmd+Q → relaunch)
- [ ] Project open in Resolve with at least one timeline

---

## Manual Test Commands

```bash
# Quick version check
echo -e '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "resolve_control", "arguments": {"action": "get_version"}}}' | /opt/homebrew/opt/python@3.11/bin/python3.11 "/Users/alfredkamisese/Library/Application Support/davinci-resolve-mcp/src/server.py"

# Run full test suite
./scripts/test-davinci-resolve-mcp.sh
```