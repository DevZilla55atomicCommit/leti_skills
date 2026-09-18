---
name: mcp-linear
description: Linear MCP server configuration for issue tracking and project management
category: infrastructure
tags: [mcp, linear, issues, project-management, claude-code, hermes]
---

# Linear MCP Server

## Purpose
Provide agents with Linear API access via MCP for issue tracking, project management, and sprint operations.

## Configuration

### Hermes (in `~/.hermes/config.yaml`)
```yaml
mcp_servers:
  linear:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-linear"]
    env:
      LINEAR_API_KEY: "${LINEAR_API_KEY}"
    enabled: true
    timeout: 30
    connect_timeout: 10
```

### Claude Code (in `~/.claude/settings.json`)
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
    }
  }
}
```

## Required Token

Create a Linear API Key:
1. Go to Linear Settings > API > Personal API keys
2. Create new key with appropriate scopes
3. Add to `~/.hermes/.env` and `~/.claude/.env`:
```bash
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxx
```

## Available Tools

| Tool | Description |
|------|-------------|
| `create_issue` | Create a Linear issue |
| `get_issue` | Get issue details |
| `update_issue` | Update issue (status, assignee, labels) |
| `search_issues` | Search issues with filters |
| `create_project` | Create a project |
| `get_project` | Get project details |
| `create_cycle` | Create a cycle (sprint) |
| `get_cycle` | Get cycle details |
| `create_team` | Create a team |
| `get_user` | Get user info |
| `list_teams` | List teams |
| `create_comment` | Add comment to issue |

## Usage Examples

### Hermes
```bash
# Via tool calling with ollama-launch provider
"Create a Linear issue for the auth bug with label 'bug'"
"Move issue ENG-123 to 'In Progress'"
"List all issues in the current sprint"
```

### Claude Code
```bash
claude "Create a Linear issue for the payment refactor"
claude "Show me all issues assigned to me in the current cycle"
```

## Integration with Kanban

When Kanban creates tasks:
1. Auto-create Linear issue with same title/description
2. Sync status changes (Kanban ↔ Linear)
3. Link PRs to Linear issues via branch naming (`feat/ENG-123-description`)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "401 Unauthorized" | Check LINEAR_API_KEY is valid |
| "Team not found" | Key must have access to the team/workspace |
| "Rate limited" | Linear has generous limits; check for loops |

## Team/Project Context

Agents should know:
- **Team ID:** Check with `list_teams` tool
- **Default Project:** Set in Linear settings
- **Cycle naming:** Current sprint = active cycle
- **Label conventions:** `bug`, `feature`, `tech-debt`, `docs`