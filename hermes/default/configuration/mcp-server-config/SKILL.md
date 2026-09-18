---
name: mcp-server-config
description: Guide for configuring MCP servers in Hermes Agent, handling unknown config keys, and respecting rate limits.
version: 1.0
tags: [mcp, configuration, tutorial, rate-limit]
---

# Configuring MCP Servers in Hermes Agent

When connecting external tools via the Model Context Protocol (MCP), you must declare servers in your `~/.hermes/config.yaml`. This skill explains the correct syntax, how to respect provider rate limits, and how to handle unknown configuration keys.

## Basic Server Configuration

Add your servers under the `mcp_servers:` key:

```yaml
mcp_servers:
  claude-code:
    command: claude
    args:
      - mcp
      - serve
    enabled: true
    timeout: 120
    rate_limit_rpm: 40   # NVIDIA API enforces 40 RPM; unknown keys are logged but ignored
  my-api:
    command: "uvx"
    args: ["@modelcontextprotocol/server-my-api", "/path/to/data"]
    env:
      API_KEY: "sk-..."
```

### Configuration Fields

| Field          | Required | Description |
|----------------|----------|-------------|
| `command`      | Yes (stdio) | Executable to run |
| `args`         | No | Command arguments |
| `enabled`      | No | Whether to start the server (default: true) |
| `timeout`      | No | Per-tool timeout in seconds |
| `rate_limit_rpm` | Yes | Set to your provider's limit (e.g., 40 for NVIDIA) |
| `url` + `headers` | For HTTP | Alternative to `command` for remote servers |

## Handling Unknown Configuration Keys

Hermes logs warnings like:

```
WARNING hermes_cli.config: providers.nvidia: unknown config keys ignored: concurrency_limit, max_retries, max_retry_delay, rate_limit_rpm, retry_delay, retry_jitter, retry_on
```

- Unknown keys are ignored and do not break functionality.
- Only documented keys (e.g., `command`, `args`, `enabled`, `timeout`, `rate_limit_rpm`) are processed.
- You can safely add provider-specific keys; unknown ones will be logged but disregarded.

## Respecting Rate Limits

- NVIDIA's API enforces a 40 RPM limit. Set `rate_limit_rpm: 40` to track usage.
- Exceeding the limit may cause errors; stay within the configured RPM.
- The system will log when the limit is approached; implement your own throttling if needed.

## Verifying MCP Server Registration

After restarting Hermes (Cmd+R or `/reset`), verify tools are registered:

```bash
hermes tools list | grep mcp_
```

You should see tools prefixed with `mcp_claude_code_` etc.

## Advanced: Multiple Servers

You can configure multiple servers simultaneously. Each runs independently and their tools are automatically discovered.

## Complete Example

```yaml
mcp_servers:
  claude-code:
    command: claude
    args:
      - mcp
      - serve
    enabled: true
    timeout: 120
    rate_limit_rpm: 40
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

By following this guide, you can integrate any MCP server while respecting provider limits and handling unknown configuration gracefully.