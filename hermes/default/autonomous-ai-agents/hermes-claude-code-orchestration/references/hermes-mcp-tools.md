# Hermes MCP Server Tools Reference

When `hermes mcp serve` runs, it exposes these tools to any MCP client (including Claude Code).

## Tool List

| Tool | Description | Parameters |
|------|-------------|------------|
| `mcp_hermes_conversations_list` | List active messaging conversations | `platform` (optional), `limit` (default 50), `search` (optional) |
| `mcp_hermes_conversation_get` | Get detailed conversation info | `session_key` (required) |
| `mcp_hermes_messages_read` | Read recent messages | `session_key` (required), `limit` (default 50) |
| `mcp_hermes_attachments_fetch` | List attachments for a message | `session_key` (required), `message_id` (required) |
| `mcp_hermes_events_poll` | Poll for new events | `after_cursor` (default 0), `session_key` (optional), `limit` (default 20) |
| `mcp_hermes_events_wait` | Long-poll for next event | `after_cursor` (required), `session_key` (optional), `timeout_ms` (default 30000) |
| `mcp_hermes_messages_send` | Send message to platform | `target` (required, "platform:chat_id"), `message` (required) |
| `mcp_hermes_channels_list` | List available channels | `platform` (optional) |
| `mcp_hermes_permissions_list_open` | List pending approvals | (none) |
| `mcp_hermes_permissions_respond` | Respond to approval | `id` (required), `decision` (required: "allow-once"\|"allow-always"\|"deny") |

## Usage from Claude Code

After connecting: `claude mcp add hermes -- hermes mcp serve`

```bash
# In Claude Code, use tools naturally:
"Use mcp_hermes_conversations_list to show my Telegram chats"
"Use mcp_hermes_messages_send with target='telegram:123456' and message='Hello from Claude Code'"
"Use mcp_hermes_channels_list to see all available channels"
```

## Tool Naming Convention

Tools are prefixed with `mcp_hermes_` (server name = "hermes").

## Event Types

The event bridge polls Hermes' SQLite session database for:
- `message` — New user/assistant message
- `approval_requested` — Permission request (exec/plugin)
- `approval_resolved` — Approval decision made

## Configuration

No additional config needed. The server reads from:
- `~/.hermes/sessions/sessions.json` — Gateway session index
- `~/.hermes/state.db` — Message transcripts (SQLite + FTS5)
- `~/.hermes/channel_directory.json` — Cached channel list

## Limitations

- **Stdio only** — No HTTP/StreamableHTTP transport yet
- **Read-only gateway** — Can't start/stop gateway via MCP
- **Live approvals only** — Only sees approvals since bridge started
- **No sampling** — Server-initiated LLM requests not implemented