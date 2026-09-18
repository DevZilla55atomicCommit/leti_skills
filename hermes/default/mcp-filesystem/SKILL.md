---
name: mcp-filesystem
description: Filesystem MCP server configuration for agent file operations
category: infrastructure
tags: [mcp, filesystem, tools, claude-code, hermes]
---

# Filesystem MCP Server

## Purpose
Provide agents (Hermes, Claude Code) with secure file system access via MCP protocol.

## Configuration

### Hermes (in `~/.hermes/config.yaml`)
```yaml
mcp_servers:
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/alfredkamisese/projects"]
    enabled: true
    timeout: 30
    connect_timeout: 10
```

### Claude Code (in `~/.claude/settings.json`)
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/alfredkamisese/projects"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write file (overwrite) |
| `edit_file` | Edit file (find/replace) |
| `list_directory` | List directory contents |
| `create_directory` | Create directory |
| `move_file` | Move/rename file |
| `search_files` | Search files by pattern |
| `get_file_info` | Get file metadata |

## Security

- **Root path restricted** to `/Users/alfredkamisese/projects`
- Cannot access system files, ~/.ssh, ~/.aws, etc.
- Read/write/delete all allowed within root

## Usage in Agents

### Hermes
```bash
# Automatic via tool calling when using ollama-launch provider
# Agent can: read, write, edit, list, search files
```

### Claude Code
```bash
# Automatic when MCP server connected
claude "Read the auth middleware and explain it"
# Claude will call filesystem tools
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Permission denied" | Check root path in config matches project location |
| "Server not found" | Run `npx -y @modelcontextprotocol/server-filesystem /path` manually to test |
| "Timeout" | Increase timeout in config (large directories) |

## Path Mapping

| Agent Request | Resolved Path |
|---------------|---------------|
| `src/lib/auth.ts` | `/Users/alfredkamisese/projects/current-project/src/lib/auth.ts` |
| `../../config.json` | Blocked (outside root) |
| `~/projects/app/package.json` | Resolved to absolute within root |