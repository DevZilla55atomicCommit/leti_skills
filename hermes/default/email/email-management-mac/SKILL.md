---
name: email-management-mac
title: Email Management for macOS (Unified Apple Mail)
description: Unified inbox handling for Gmail, iCloud, and Outlook/Exchange via native Apple Mail + AppleScript automation.
tags: [email, macos, automation, apple-script, hermes, mail.app]
author: alfred
created: 2026-07-13
---

# Email Management for macOS (Unified Apple Mail)

**Purpose**: Unified inbox handling for Gmail, iCloud, and Outlook/Exchange via native Apple Mail + AppleScript automation. Avoids heavy `computer_use` overhead.

## Core Approaches

| Approach | When to Use | Key Commands |
|----------|-------------|--------------|
| **Direct AppleScript** | Quick checks, cron jobs, low‑resource environments | `osascript` to query Mail.app |
| **Himalaya IMAP** | Full read/write via CLI for Gmail/iCloud | `himalaya` skill |
| **Outlook Forwarding** | When Outlook must stay in Exchange | Forward to Gmail → Himalaya |

## Step‑by‑Step: Checking Unread Count

```bash
osascript -e 'tell application "Mail" to get count of messages of mailbox "Inbox" of account "iCloud"'
osascript -e 'tell application "Mail" to get count of messages of mailbox "Inbox" of account "Gmail"'
osascript -e 'tell application "Mail" to get count of messages of mailbox "Inbox" of account "Exchange"'
```

### Pitfalls

- **Exact account names**: Use the names shown in Mail.app → Preferences → Accounts.
- **AppleScript timeout**: Background jobs default to 10 s; wrap with `timeout 5` or use `launchd`.
- **Folder paths**: Use `mailbox "Inbox"` for top‑level inboxes; sub‑folders need full hierarchy (e.g., `mailbox "INBOX"` for Gmail).
- **Gmail mailbox name is `INBOX` (uppercase)** — not `Inbox`. This is a common source of "Can't get mailbox" errors.
- **iCloud account** — may return empty mailbox list if not fully synced; verify in Mail.app first.

## Automation

- **Cron job**: `0 8 * * * /Users/alfredkamisese/.hermes/scripts/sync_step_beyond_memory_push.py`
- **Daily 8 AM briefing**: “Good Morning Email Briefing” job triggers at 8:00 AM Pacific.

## References

- `references/email-setup-mac.md` – Detailed setup guide.
- `references/applescript-patterns.md` – Working AppleScript patterns for Mail.app (account names, mailbox names, unread queries, marking read).
- `scripts/check_unread.scpt` – Ready‑to‑run AppleScript for unread counts.
- `templates/email-check.template` – Boilerplate for new checks.

## User Collaboration Preferences

The user emphasizes:
- **Draft-first, send-never** – never auto-send; always iterate on email drafts collaboratively before sending.
- **Concise, direct answers** – avoid verbose tables or exploratory explanations unless explicitly requested.
- **Newsletter summaries** – provide a brief bullet list of key topics.
- **Actionable steps** – prioritize clear next actions over procedural fluff.

Updated references to include: `references/email-preferences.md` – captures user email workflow preferences and style guidance.