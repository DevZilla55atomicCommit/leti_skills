# Figma MCP — Connection Guide for Claude Code

## Access Requirements (Critical)

| Plan / Seat | Monthly Limit | Practical for Dev Work? |
|-------------|---------------|------------------------|
| **Starter (free)** | 20 tool calls/month | ❌ No — ~1 call/day |
| **View / Collab** (paid) | 6 tool calls/month | ❌ No |
| **Dev / Full** (Professional) | 200/day, 10/min | ✅ Yes |
| **Dev / Full** (Organization) | 600/day, 15/min | ✅ Yes |
| **Dev / Full** (Enterprise) | Unlimited, 20/min | ✅ Yes |
| **Education** | 200/day, 10/min | ✅ Yes |

**Bottom line:** Free Starter plan exists on paper but 20 calls/month makes it unusable. Need Dev/Full seat on paid plan.

## Setup Options

### Option 1: Remote Server (Recommended) — OAuth, no local app
```bash
# One-command install (plugin + agent skills)
claude plugin install figma@claude-plugins-official
```

**OR manually:**
```bash
# Add remote Figma MCP server (user scope = all projects)
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# Restart Claude Code, then authenticate
/mcp → select figma → Authenticate → Allow Access
```

### Option 2: Local Desktop Server — requires Figma desktop app
```bash
# 1. In Figma desktop: Menu → Preferences → Enable Dev Mode MCP Server
#    Runs at http://127.0.0.1:3845/sse

# 2. Connect to local server
claude mcp add --transport sse figma-dev-mode http://127.0.0.1:3845/sse
```

## Verify Connection
```bash
claude mcp list
# Should show: figma (connected)
```

## Capabilities
| Capability | Description |
|------------|-------------|
| Read frames/components | Pull design specs, variables, auto-layout |
| Write to canvas | Create/modify frames, components, variables |
| Code generation | Turn selected frames into React/Vue/Swift/Flutter |
| Design system sync | Code Connect keeps components consistent |
| FigJam diagrams | Generate architecture/ERD diagrams from prompts |
| Live UI capture | Capture web app UI → Figma (select clients) |

## Requirements
- Dev or Full seat Figma account (Starter not practical)
- At least one design file in your account
- OAuth authentication (handled automatically)

## Remote vs Local
| Aspect | Remote (https://mcp.figma.com/mcp) | Local (desktop app) |
|--------|-------------------------------------|---------------------|
| Works anywhere | ✅ | ❌ (needs desktop app) |
| No local install | ✅ | ❌ |
| Syncs across devices | ✅ | ❌ |
| Write to canvas | ✅ | ❌ |
| OAuth handled | ✅ | ✅ |

**Recommendation:** Use remote server — preferred by Figma, works everywhere, includes Agent Skills for common workflows.