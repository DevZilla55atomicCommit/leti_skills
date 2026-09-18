---
name: apple-mail
description: "Manage Apple Mail via osascript: read, search, send, organize emails across all accounts (Exchange, Gmail, iCloud, etc.) without GUI automation."
tags: ["Apple", "Mail", "Email", "macOS", "automation", "osascript"]
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Apple, Mail, Email, macOS, automation, osascript]
    category: apple
prerequisites:
  commands: [osascript]
  permissions:
    - "Automation: Mail.app (System Settings → Privacy & Security → Automation → Terminal/Editor → Mail.app)"
---

**Purpose**: Query Apple Mail.app directly via `osascript` to enumerate unread messages across all accounts (iCloud, Gmail via Apple Mail, Outlook/Exchange) without using `computer_use`. Fast, zero external tooling.

## User Directive
- **Never use `computer_use` for email operations unless explicitly requested by the user.** All email queries **must** default to the `apple-mail` skill using `osascript`.

## Core Commands

- List unread subjects across all accounts:
  ```bash
  osascript -e 'tell application "Mail" to get subject of every message of mailbox "INBOX" of account 1 whose read status is false'
  ```

- Get unread count per account:
  ```bash
  osascript -e 'tell application "Mail" to get name of every mailbox of account 1 where unread count > 0'
  ```

## Steps

1. **Identify account names** in Apple Mail:
   ```bash
   osascript -e 'tell application "Mail" to get name of every account'
   ```
2. **Map inbox names**:
   - Some accounts expose "Inbox", others "INBOX". Use whichever exists.
3. **Extract message metadata**:
   ```bash
   osascript -e 'tell application "Mail" to repeat with m in (every message of mailbox "Inbox" of account 1 whose read status is false) ... end repeat; return {{subject:s, sender:s, date:d}} of m'
   ```
4. **Filter and format** results for Hermes via `himalaya` or direct display.

## Pitfalls & Fixes
- **Case-sensitive mailbox names**: Use "Inbox" or "INBOX" based on account; the script checks both.
- **Missing permissions**: Ensure Apple Mail is fully indexed; first run may prompt.
- **Multiple accounts with same name**: Disambiguate using `account` identifier in script.

## Attachment & Draft Handling (Verified)
- **Attachments require explicit `save` after each `make new attachment`** — adding multiple attachments at once often results in only 2 being attached. Add one, `save`, `delay 1`, add next, `save`, etc.
- **Drafts default to the default account's Drafts folder** — even if you target a specific account, the draft appears in the default account's Drafts (Exchange in tested setup).
- **Cannot move drafts between mailboxes** — `move msg to mailbox "[Gmail]/Drafts"` fails with error -10024.
- **Cannot create draft directly in non-default account's mailbox** — `make new outgoing message at mailbox "[Gmail]/Drafts"` fails with error -10024.
- **Workaround**: Create draft in default account, then manually drag in Mail.app, or use the default account's Drafts.
- **Attachment order**: Add attachments sequentially with `save` and `delay 1` between each for reliability.
- **Setting subject/content on existing messages**: `set subject of msg to "..."` fails with -10006. Recreate the draft instead.

## Example Output

```json
[
  {
    "account": "iCloud",
    "subject": "Test Forward - $(date)",
    "sender": "Anthropic",
    "date": "2026-06-19 16:42+00:00",
    "id": "12345678"
  }
]
```

## Integration with Hermes
- Use `/skill apple-mail` to run any of the above commands.
- Wrap output in a summary and forward to `/skill himalaya` for further processing (e.g., moving to archive).

## References
- `references/apple-mail-techniques.md` contains detailed reproduction of error cases and fix scripts.

## Rules
1. **Always use account name** (e.g., `"Exchange"`, `"Google"`, `"iCloud"`) — not index
2. **Use message `id`** for precise targeting — not position
3. **Test with `osascript -e '...'` first** before wrapping in skill
4. **Handle missing mailboxes gracefully** — not all accounts have the same folders
5. **Prefer JavaScript (osascript -l JavaScript)** for complex data — easier JSON output
6. **Never use `computer_use` for email operations unless explicitly requested by the user.** All email queries **must** default to the `apple-mail` skill using `osascript`.

## Example Workflow in Hermes
```bash
# 1. Check all unread
/skill apple-mail
"Show me all unread emails across all accounts"

# 2. Search
/skill apple-mail
"Search all accounts for emails from anthropic.com"

# 3. Read specific
/skill apple-mail
"Read the full content of that Exchange email about the test forward"

# 4. Reply
/skill apple-mail
"Reply to that email saying 'Received, thanks!'"

# 5. Organize
/skill apple-mail
"Move that email to Archive"