# Apple Mail Multi-Account Unread Check — Working Recipes (2026-08)

Session-derived, verified command transcript for checking unread across iCloud,
Google (Gmail), and Exchange accounts in Apple Mail via `osascript`.

## Account enumeration

```bash
osascript -e 'tell application "Mail" to get name of every account'
# -> "iCloud, Google, Exchange"   (display names; NOT valid mailbox targets)
```

## Per-account mailbox list (RELIABLE map)

```bash
osascript -e 'tell application "Mail"
set out to {}
repeat with a in accounts
  set end of out to (name of a) & " => " & (name of every mailbox of a as string)
end repeat
return out
end tell'
```

In this session it produced:
- iCloud   => `Archive INBOX Drafts Sent Messages Deleted Messages Junk`
- Google   => `...Notes INBOX`  (many Gmail labels incl. INBOX)
- Exchange => `...Inbox Outbox Drafts Sent Items Deleted Items Junk Email`

Note: iCloud's first two names render contiguous (`ArchiveINBOX`) with no delimiter.

## Unread counts per mailbox (reliable — does NOT time out)

```bash
osascript -e 'tell application "Mail"
set out to {}
repeat with a in accounts
  repeat with bn in (name of every mailbox of a)
    try
      set cnt to unread count of mailbox bn of a
      set end of out to (name of a) & "/" & bn & "=" & cnt
    on error
      set end of out to (name of a) & "/" & bn & "=ERR"
    end try
  end repeat
end repeat
return out
end tell'
```

Returns per-mailbox counts even when per-message fetches fail. In this session:
- iCloud/INBOX = 0
- Google/INBOX = 27
- Exchange/Inbox = 4, Exchange/Junk Email = 6

> ⚠️ Counts are unreliable while Mail is still syncing a large mailbox. The "27"
> above was a partial count; once Mail settled the true Google/INBOX unread was
> **278**, and Exchange/Inbox was ~20, not 4. Always re-query after letting Mail
> settle before acting on a suspiciously-low count, and treat counts taken during
> an initial dump as provisional.

Some mailboxes return ERR (e.g. Google's `Important`, `Starred`, `All Mail`,
`Spam`) — those are virtual Gmail views; rely on INBOX and the special-folder counts.

## Error signatures

| Error | Meaning | Handling |
|-------|---------|----------|
| `-1728` Can't get inbox of account | Account name used as mailbox target | Enumerate `every mailbox of a` first; use real mailbox name |
| `-1712` AppleEvent timed out | Large/heavily-synced INBOX during per-message fetch | Use `unread count` (reliable); fetch detail one small account at a time; retry later, don't hammer |

## Per-message detail — the LOOP form times out on big inboxes, the SINGLE-LIST form works

The per-message `repeat` loop below **timed out (-1712)** for Google/INBOX (backlog
was actually 278) — per-message AppleScript formatting is too heavy at that scale:

```bash
osascript -e 'tell application "Mail"
set out to {}
repeat with m in (every message of mailbox "Inbox" of account "Exchange" whose read status is false)
  set end of out to (date received of m as string) & " | " & subject of m & " | " & sender of m
end repeat
return out
end tell'
```

The **single whole-list fetch** (no `repeat`, one field per call) succeeded even on
the 278-item Gmail INBOX — run subject and sender as SEPARATE calls:

```bash
osascript -e 'tell application "Mail" to get subject of every message of mailbox "INBOX" of account "Google" whose read status is false'
osascript -e 'tell application "Mail" to get sender of every message of mailbox "INBOX" of account "Google" whose read status is false'
```

Prefer this form for any large inbox. Bundle subject+sender in one call only on
small inboxes. Send a `sender` fetch occasionally returns `-609 Connection is
invalid` under heavy Mail load — a single retry after a few seconds usually clears it.

## Environment note
`himalaya` CLI was NOT installed and no Hermes email gateway adapter was configured on
this machine (2026-08-10); Apple Mail via osascript is the operative path.