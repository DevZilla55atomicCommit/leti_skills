---
name: mcp-configuration
title: MCP Server Configuration for Hermes Agent
description: Documentation for adding, configuring, and troubleshooting MCP servers (e.g., Claude Code) within Hermes Agent's `config.yaml`. Includes install steps, YAML block example, verification, and common failure fixes.
tags: [mcp, configuration, hermes-agent]
owner: alfredkamisese
version: 1.0
status: active
---

# MCP Server Configuration for Hermes Agent

## Purpose
Add and manage MCP (Model Context Protocol) servers within the Hermes Agent configuration. This skill documents the exact steps required to:

1. Declare MCP servers in `~/.hermes/config.yaml`
2. Reference them via `mcp_<server_name>` keys
3. Use the native MCP client (`native-mcp`) to connect to them
4. Verify connectivity and troubleshoot common issues

## Process

### 1. Install the MCP client (if not already installed)
```bash
# Using npm (recommended)
npm install -g @anthropic-ai/claude-code   # provides the `claude` binary
# Or via direct installer
curl -fsSL https://claude.ai/install.sh | bash
```

### 2. Edit Hermes configuration
```bash
# Open the config file (or use Hermes CLI)
hermes config edit
```

Add a top‑level `mcp_servers` block (example for Claude Code):
```yaml
mcp_servers:
  claude-code:
    command: /Users/alfredkamisese/.local/bin/claude
    args:
      - mcp
      - serve
    enabled: true
    timeout: 120
    connect_timeout: 60
```

**Key fields**
- `command`: absolute path to the MCP binary (e.g., `/usr/local/bin/claude` or `~/bin/claude`)
- `args`: always `['mcp', 'serve']` for the server mode
- `enabled`: set to `true` to activate the server on startup
- `timeout` / `connect_timeout`: adjust if you see handshake failures

### 3. Persist the change
If you edited the file directly, save and exit.  
If you used `hermes config set`, the CLI writes the change atomically.

### 4. Restart Hermes Agent
- **Desktop app:** Cmd‑R (Restart) or quit and relaunch.
- **CLI/daemon:** `hermes stop && hermes start` (or `brew services restart hermes` if installed as a service).

### 5. Verify the server is registered
```bash
hermes config get mcp_servers
# Should output the block you added
```

You can also list available MCP tools:
```bash
hermes tools | grep mcp_
# Example output: mcp_claude_code_*   ← indicates the client sees the server
```

### 6. Troubleshooting checklist
| Symptom | Likely cause | Fix |
|---|---|---|
| `mcp_<name>_*` tools missing | `mcp_servers` block missing or malformed | Ensure the block is at the **end** of `config.yaml` and is valid YAML |
| 401 / authentication error | Wrong binary path or missing credentials | Verify the command path (`command:`) points to the actual binary; ensure the binary runs `claude --version` without errors |
| Server starts but no tools appear | Hermes was not restarted after config change | Restart the agent as described above |
| Connection timeout | Binary not reachable / slow launch | Increase `timeout`/`connect_timeout` values or check network/firewall settings |
| “command not found” | Binary not in PATH for the Hermes process | Use an **absolute** path in `command:` |

### 7. Common patterns
- **Multiple servers:** Duplicate the block with a new key (`claude-code`, `another-server`) and adjust `command`/`args` accordingly.
- **Disabled servers:** Set `enabled: false` to keep the entry in the config without loading the server.
- **Version pinning:** If you rely on a specific binary version, lock the path to that version (e.g., `/opt/claude/bin/claude-v2.1.205`).
- **Open Design (design workspace):** Uses the packaged app's CLI wrapper:
  ```yaml
  mcp_servers:
    open-design:
      command: node
      args:
        - "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs"
        - mcp
        - --daemon-url
        - http://127.0.0.1:58267
      enabled: true
  ```
  The daemon must be running (headless via `"/Applications/Open Design.app/Contents/MacOS/Open Design" --headless`). The port is ephemeral; update `--daemon-url` or let the MCP client discover it.

### 8. Related skills
- `native-mcp` – low‑level MCP client wrapper.
- `hermes-agent-skill-authoring` – authoring new HERMES skills.
- `provider-block-patterns` – generic provider block syntax for other APIs.

### 9. Reference files
- `references/open-design-mcp-setup.md` — Complete Open Design MCP server setup for Hermes Agent (install, daemon, config, tools, troubleshooting)

### 9. Updating this skill
When a new Hermes version changes the config schema:
1. Review the official `hermes config` docs.
2. Add any new required fields (e.g., `transport`, `tls`).
3. Update the example block accordingly.
4. Test with a fresh Hermes restart.