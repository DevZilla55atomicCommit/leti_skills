# Working AppleScript Patterns for macOS Mail.app

Discovered during session: checking unread counts and marking messages as read across Google, Exchange, and iCloud accounts.

## Account Names (as shown in Mail.app → Preferences → Accounts)
- **Google** — Gmail account (mailbox name: `INBOX`, not `Inbox`)
- **Exchange** — Outlook/Exchange account (mailbox name: `Inbox`)
- **iCloud** — iCloud account (no accessible mailboxes found in this session)

## Unread Count Queries

```applescript
-- Gmail (Google account)
tell application "Mail" to get unread count of mailbox "INBOX" of account "Google"

-- Exchange/Outlook
tell application "Mail" to get unread count of mailbox "Inbox" of account "Exchange"

-- iCloud (not working in this session)
tell application "Mail" to get unread count of mailbox "Inbox" of account "iCloud"
```

## Mark All Unread as Read (Gmail)

```applescript
tell application "Mail" to set read status of messages of mailbox "INBOX" of account "Google" whose read status is false to true
```

## List Mailboxes for an Account

```applescript
tell application "Mail" to get name of every mailbox of account "Google"
```

## Get Unread Message Subjects

```applescript
tell application "Mail" to get subject of every message of mailbox "INBOX" of account "Google" whose read status is false
```

## Get Message Content by Index

```applescript
tell application "Mail" to get content of message 2 of mailbox "INBOX" of account "Google"
```

## Key Findings

1. **Gmail uses `INBOX` (uppercase)** — not `Inbox` — as the mailbox name in Apple Mail
2. **Exchange uses `Inbox` (capitalized)** — standard naming
3. **iCloud account** — returned empty mailbox list; may need different approach or account may not be fully synced
4. **Timeouts** — fetching full message content can timeout; prefer fetching subject/sender/date first, then content for specific messages
5. **Marking read** — the `set read status ... to true` pattern works reliably for bulk operations
6. **Drafts mailbox is `Drafts` on both Google and Exchange** — Exchange junk is `Junk Email`

## Draft Lifecycle (create, prove, clean up)

```applescript
-- Create: the sender address routes the draft to that account's Drafts
tell application "Mail"
  set theMessage to make new outgoing message with properties {sender:"reeves.kamisese@gmail.com", subject:"...", content:"...", visible:false}
  tell theMessage
    make new to recipient at end of to recipients with properties {address:"..."}
  end tell
  save theMessage
end tell
```

- **Verify (never trust the save alone)**: re-query `get subject of every message of mailbox "Drafts" of account "Google"` and confirm the subject is there.
- **Visual proof**: `activate` Mail, then `open` each matching Drafts message — this opens real editor windows the user can see.
- **Clean up test drafts**: `delete` each matching message; it lands in Trash, so the operation is reversible.
- Bare `save theMessage` files under the sender's account automatically; `save theMessage in mailbox "Drafts" of account "..."` works when explicit routing is needed.