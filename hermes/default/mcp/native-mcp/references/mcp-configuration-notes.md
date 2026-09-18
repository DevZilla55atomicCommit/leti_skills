# Safe MCP Server Configuration

## Do Not Edit `config.yaml` Manually (When Restricted)
If you are inside a constrained Hermes session, use the built‑in configurator instead of directly editing `~/.hermes/config.yaml`:

```bash
# Set command (example for Claude Code)
hermes config set mcp_servers.claude-code.command "/Users/alfredkamisese/.local/bin/claude"

# Define server arguments
hermes config set mcp_servers.claude-code.args "- mcp - serve"
hermes config set mcp_servers.claude-code.enabled true
hermes config set mcp_servers.claude-code.timeout 120
hermes config set mcp_servers.claude-code.connect_timeout 60
```

This persists changes through Hermes’ configuration guard and survives restarts.

## Rate Limiting
Some MCP providers enforce a **40 RPM** ceiling.

- **Batch** related queries into a single tool call.
- **Cache** identical responses during the session.
- **Set** `sampling.max_rpm` in the server config to a lower value (e.g., `max_rpm: 30`).

## Common Pitfall

*Pitfall*: Editing `config.yaml` directly bypasses Hermes’ security guard and may be reverted or cause startup failures.

*Fix*: Always use `hermes config` commands or edit the file via `skill_manage` with `cross_profile: true` (only after explicit user permission).