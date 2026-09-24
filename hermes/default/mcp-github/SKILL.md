---
name: mcp-github
description: GitHub MCP server configuration for PR, issue, and repo operations
category: infrastructure
tags: [mcp, github, pr, issues, claude-code, hermes]
---

# GitHub MCP Server

## Purpose
Provide agents with GitHub API access via MCP for PR management, issues, and repo operations.

## Configuration

### Hermes (in `~/.hermes/config.yaml`)
```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    enabled: true
    timeout: 60
    connect_timeout: 15
```

### Claude Code (in `~/.claude/settings.json`)
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

## Required Token

Create a GitHub Personal Access Token (Classic) with scopes:
- `repo` — Full repository access
- `workflow` — GitHub Actions workflows
- `read:org` — Organization membership
- `user:email` — User email

Add to `~/.hermes/.env` and `~/.claude/.env`:
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

## Available Tools

| Tool | Description |
|------|-------------|
| `create_pull_request` | Create a PR |
| `get_pull_request` | Get PR details |
| `list_pull_requests` | List PRs with filters |
| `merge_pull_request` | Merge a PR |
| `create_issue` | Create an issue |
| `get_issue` | Get issue details |
| `list_issues` | List issues with filters |
| `add_issue_comment` | Comment on issue |
| `search_code` | Search code in repo |
| `get_file_contents` | Read file from repo |
| `create_branch` | Create new branch |
| `get_commits` | Get commit history |

## Usage Examples

### Hermes
```bash
# Via tool calling with ollama-launch provider
"Create a PR for the auth refactor with title 'feat: refactor auth'"
"List open issues labeled 'bug' in my-org/my-repo"
"Search for 'TODO' comments in the codebase"
```

### Claude Code
```bash
claude "Create a PR with the changes I just made"
claude "Find all issues related to the payment flow"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "401 Unauthorized" | Check GITHUB_TOKEN is valid and has correct scopes |
| "Rate limited" | Token may have low limits; use fine-grained PAT |
| "Repo not found" | Token must have access to the repo (org approval?) |

## Token Setup

```bash
# 1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
# 2. Generate new token (classic)
# 3. Select scopes: repo, workflow, read:org, user:email
# 4. Copy token and add to .env files
```