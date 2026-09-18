---
name: apple-mail-performance
description: "Apple Mail automation via osascript performance guide."
category: apple
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Apple, Mail, Email, macOS, automation, osascript]
    category: apple
---

## Purpose
Provide performance and robustness guidelines for automating Apple Mail using `osascript`, addressing large mailboxes, Gmail/IMAP quirks, thread handling, iCloud structure, and uniqueness considerations.

## Core Commands
- **Limit iteration** to recent messages or apply sender filters to avoid timeouts.
- **Enumerate mailboxes** to locate the correct inbox name case‑insensitively.
- **Filter on `message id`** to deduplicate conversations.
- **Test filter conditions** with small `osascript -l JavaScript` snippets before scaling.

## Pitfalls & Fixes
- **Large Mailboxes (>5,000 messages)**: Use date‑received filters or limit to recent N messages.
- **Gmail/IMAP Account Quirks**: Some inboxes use non‑standard names; enumerate mailboxes first.
- **Thread/Duplicate Handling**: Use `message id` for uniqueness.
- **iCloud Mailbox Structure**: Primary inbox may not be named “INBOX”; match case‑insensitively.
- **Message ID Uniqueness**: Process each message only once.

## Testing Tips
- Validate filter conditions with a minimal `osascript -l JavaScript` snippet.
- Use `osascript -e '...'` to experiment before embedding in larger workflows.

## Attachment & Draft Notes (From Session)
- **Attachments**: Adding multiple attachments at once often fails (only 2 attach). Add one, `save`, `delay 1`, add next.
- **Drafts**: Always saved to default account's Drafts, even when targeting another account. Cannot move between mailboxes programmatically.
- **Subject/Content updates on existing drafts**: Fails with -10006. Recreate instead.