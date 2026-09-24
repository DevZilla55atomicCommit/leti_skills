# Open Design Integration with Hermes Agent

## Overview
Open Design (OD) is a local-first design workspace that runs as a packaged macOS app. It exposes an MCP server that Hermes Agent can consume to generate design artifacts (prototypes, decks, dashboards, images, video, HyperFrames).

This reference documents the complete setup for integrating Open Design with Hermes Agent, complementing the MCP configuration in `mcp-configuration` skill.

## Prerequisites
- Open Design app installed: `/Applications/Open Design.app`
- Hermes Agent running (default profile)
- Node.js available (for the `od` CLI wrapper)

## Setup Steps

### 1. Install Open Design
```bash
# Download DMG from GitHub Releases
# https://github.com/nexu-io/open-design/releases/latest
# Mount and drag to /Applications
```

### 2. Start the Open Design Daemon (headless)
```bash
# Runs the packaged app in headless mode on an ephemeral port
"/Applications/Open Design.app/Contents/MacOS/Open Design" --headless

# Output example:
#  Open Design is running
#  ➜ http://127.0.0.1:58267
```
**Note:** The port changes on each restart. The MCP config uses `--daemon-url` as a hint; the MCP client will auto-discover the live port on next spawn.

### 3. Configure Hermes MCP Server
Edit `~/.hermes/config.yaml` (or use `hermes config set`):

```bash
hermes config set mcp_servers.open-design.command "node"
hermes config set mcp_servers.open-design.args '["/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs", "mcp", "--daemon-url", "http://127.0.0.1:58267"]'
hermes config set mcp_servers.open-design.enabled true
```

Resulting YAML block:
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

### 4. Restart Hermes
- Desktop app: Cmd+R or quit/relaunch
- CLI: `hermes stop && hermes start`

### 5. Verify in Hermes
In a Hermes chat:
```
> Use open-design to list all available design systems
> Use open-design to generate a SaaS landing page with the Linear design system
```

## Available MCP Tools (25)
- `collect_brief` — open interactive brief card
- `confirm_brief` — confirm brief choices
- `list_projects` — list all OD projects
- `get_active_context` — current project/file user has open
- `get_artifact` — pull design bundle (entry + all referenced files)
- `get_project` — project metadata + preview URL
- `get_file` — read one project file
- `search_files` — substring search across project files
- `list_files` — project file metadata
- `create_artifact` — create artifact entry file
- `write_file` — write/overwrite project file
- `delete_file` — delete project file
- `delete_project` — permanently delete project
- `create_project` — create new empty project
- `list_skills` — list available skills (recipes)
- `list_plugins` — list installed plugins (packaged workflows)
- `start_vela_login` — OD Cloud sign-in
- `get_vela_login_status` — check Cloud sign-in
- `start_run` — commission OD to generate/refine design
- `get_run` — poll run status (returns previewUrl on success)
- `cancel_run` — abort in-flight run
- `list_agents` — list available agent CLIs (Claude Code, Codex, etc.)

## Design Systems Available (151)
Linear, Vercel, Stripe, Apple, Figma, Notion, Tesla, Nvidia, Airbnb, Shopify, Spotify, GitHub, Discord, Slack, and 138 more.

## Plugins Available (452)
Scenarios: `od-default`, `od-figma-migration`, `od-code-migration`, `od-react-export`, `od-nextjs-export`, `od-vue-export`, `od-media-generation`, `od-new-generation`, `od-tune-collab`, `od-plugin-authoring`, `od-share-to-community`, `od-web-effect-extractor`.
Design systems: 143 brand systems wrapped as plugins.
Atoms: 13 reusable UI fragments.
Examples: 183 reference outputs.
Image templates: 45 one-shot prompts.
Video templates: 63 HyperFrames/Seedance/Veo templates.

## Quick CLI Commands (without Hermes)
```bash
# Start daemon
"/Applications/Open Design.app/Contents/MacOS/Open Design" --headless

# Test MCP server directly
node "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs" mcp --daemon-url http://127.0.0.1:58267

# List plugins via CLI
node "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs" plugin list --daemon-url http://127.0.0.1:58267 --json

# Apply a plugin
node "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs" plugin apply example-saas-landing --inputs '{"product_name":"ForexIQ","tagline":"Real-time forex analytics"}' --daemon-url http://127.0.0.1:58267 --json
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| MCP tools not appearing | Restart Hermes after config change; verify `hermes config get mcp_servers.open-design` |
| Daemon not reachable | Ensure `"/Applications/Open Design.app/Contents/MacOS/Open Design" --headless` is running; check port in output |
| Port changed | Update `--daemon-url` in config, or let MCP client auto-discover (it reads the sidecar IPC) |
| better-sqlite3 ERR_DLOPEN_FAILED | Node version mismatch; the packaged app bundles its own Node (v24.16.0). Use the app's CLI wrapper, not a separately built CLI. |
| Permission denied | Ensure the app is in `/Applications` (not a temp location) and has been launched once to clear Gatekeeper |

## Notes
- The MCP server runs as a **stdio** process spawned on-demand by Hermes. It exits when no client is connected.
- The packaged app includes its own Node runtime and compiled native modules (better-sqlite3, node-pty) — do not use a separately built CLI from source unless you rebuild native modules for your Node version.
- Design systems are selected at generation time via `designSystem` in `create_project` or via the active context.
- Artifacts are real HTML/CSS/JS files — hand off to Cursor/Codex/Claude Code to turn into React/Next/Vue.

## Related Skills
- `mcp-configuration` — MCP server configuration patterns (includes Open Design pattern)
- `hermes-agent` — Core Hermes configuration reference
- `hermes-provider-configuration` — Multi-provider setup patterns