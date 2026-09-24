# Hermes MCP Server Tool Reference

## Server Command

```bash
# Start the MCP server (runs on stdio)
hermes mcp serve

# Verbose logging
hermes mcp serve --verbose
```

## Client Configuration (Claude Code)

```bash
# Add to Claude Code
claude mcp add hermes -- hermes mcp serve
```

## Available Tools (10 Total)

### 1. conversations_list

List active messaging conversations across connected platforms.

```json
{
  "name": "conversations_list",
  "arguments": {
    "platform": "telegram|discord|slack|...",  // optional filter
    "limit": 50,                               // optional, default 50
    "search": "text to filter by name"         // optional
  }
}
```

**Returns:** Conversations with session keys, platform, chat type, display name, last activity.

---

### 2. conversation_get

Get detailed info about one conversation by session key.

```json
{
  "name": "conversation_get",
  "arguments": {
    "session_key": "telegram:123456789"
  }
}
```

---

### 3. messages_read

Read recent messages from a conversation.

```json
{
  "name": "messages_read",
  "arguments": {
    "session_key": "telegram:123456789",
    "limit": 50  // optional, default 50 (most recent)
  }
}
```

**Returns:** Message history in chronological order with role, content, timestamp.

---

### 4. attachments_fetch

List non-text attachments for a specific message.

```json
{
  "name": "attachments_fetch",
  "arguments": {
    "session_key": "telegram:123456789",
    "message_id": "msg_abc123"
  }
}
```

**Returns:** Images, media files, non-text content blocks.

---

### 5. events_poll

Poll for new conversation events since a cursor position.

```json
{
  "name": "events_poll",
  "arguments": {
    "after_cursor": 0,           // required, 0 for all events
    "session_key": "telegram:...", // optional filter
    "limit": 20                  // optional, default 20
  }
}
```

**Event types:** `message`, `approval_requested`, `approval_resolved`

**Returns:** Events array + `next_cursor` for subsequent polls.

---

### 6. events_wait

Wait for the next conversation event (long-poll).

```json
{
  "name": "events_wait",
  "arguments": {
    "after_cursor": 100,
    "session_key": "telegram:...",  // optional
    "timeout_ms": 30000             // optional, default 30000
  }
}
```

**Returns:** Single event or null on timeout.

---

### 7. messages_send

Send a message to a platform conversation.

```json
{
  "name": "messages_send",
  "arguments": {
    "target": "telegram:123456789",  // or "discord:#general", "slack:#engineering"
    "message": "Hello from Claude Code via Hermes!"
  }
}
```

**Target formats:**
- `telegram:6308981865` (user ID)
- `discord:#general` (channel)
- `slack:#engineering` (channel)
- Human-friendly names auto-resolved

---

### 8. channels_list

List available messaging channels and targets across platforms.

```json
{
  "name": "channels_list",
  "arguments": {
    "platform": "telegram"  // optional filter
  }
}
```

**Returns:** Channels with target strings usable in `messages_send`.

---

### 9. permissions_list_open

List pending approval requests observed during this bridge session.

```json
{
  "name": "permissions_list_open",
  "arguments": {}
}
```

**Returns:** Exec and plugin approval requests seen since bridge started.

---

### 10. permissions_respond

Respond to a pending approval request.

```json
{
  "name": "permissions_respond",
  "arguments": {
    "id": "approval_xyz123",
    "decision": "allow-once|allow-always|deny"
  }
}
```

**Decisions:**
- `allow-once` — Approve this specific request
- `allow-always` — Approve and remember for future
- `deny` — Block the request

---

## Error Handling

All tools return JSON with either:
- Success: `{"result": "...", ...}`
- Error: `{"error": "description"}`

Common errors:
- `"session_key not found"` — Use `conversations_list` first
- `"cursor too old"` — Reset to `after_cursor: 0`
- `"approval not found"` — Use `permissions_list_open` first

---

## Rate Limits & Performance

- `events_poll` / `events_wait`: 200ms polling interval internally
- `conversations_list`: Cached, fast
- `messages_read`: Queries SQLite, typically <100ms
- Bridge maintains in-memory queue (1000 event limit)

---

## Full JSON Schemas

Available via MCP `list_tools` — each tool has complete input/output schemas with descriptions.