---
name: macos-mail-unified-inbox
category: automation
description: Manage unified Apple Mail across Exchange, Google, iCloud accounts.
tags:
  - apple
  - mail
  - scripting
---

# macOS Mail Unified Inbox

A class-level skill for interacting with the unified Apple Mail client on macOS, focusing on reading, searching, and composing emails across Exchange, Google, and iCloud accounts without relying on Outlook or Microsoft Graph.

## When to Use
- Manage emails directly from Apple Mail.
- Read unread counts or fetch specific messages across all accounts.
- Create drafts or replies programmatically.

## Steps
1. List all mail accounts and their types.
2. Retrieve unread message subjects from a specific account (e.g., Exchange).
3. Open the Mail application if not already running.
4. Create a draft reply to a selected message.

## AppleScript Examples

### List Accounts
```applescript
tell application "Mail" to get name of every account
```

### Get Unread Messages (Exchange)
```applescript
tell application "Mail" to get {subject, sender} of every message of mailbox "Inbox" of account "Exchange" whose read status = false
```

### Create Draft Reply
```applescript
tell application "Mail" to reply of front message of process "Mail"
```

## Pitfalls
- Direct access to `enabled` property fails; use `account type` to differentiate.
- Outlook.com (Exchange) may require fresh app passwords; ensure they are valid.
- When switching from Outlook computer use to Mail.app, avoid duplicate forwards.

### Account names are NOT mailbox targets
`get name of every account` returns friendly display names (iCloud, Google, Exchange),
but `inbox of account "iCloud"` FAILS with AppleEvent error **-1728** (`Can't get
inbox of account...`). You cannot address the inbox by account name alone. Enumerate
the mailboxes each account actually exposes first:

```applescript
tell application "Mail"
  set out to {}
  repeat with a in accounts
    set end of out to (name of a) & " => " & (name of every mailbox of a as string)
  end repeat
  return out
end tell
```

### Mailbox names vary and can concatenate
Each account names its inbox differently — `INBOX` (iCloud, Google), `Inbox`
(Exchange) — and the `as string` join concatenates mailbox names WITHOUT separators,
so a list renders like `ArchiveINBOX...Drafts...Sent Messages`. Do not parse the
joined string; read `name of every mailbox of a` as a proper AppleScript list and
match the exact inbox name per account before querying `unread count` or messages.

### Summarize large backlogs by SIGNAL, not by enumerated dump — user preference
When an inbox has a large unread backlog (dozens to hundreds — a Gmail INBOX showed
278 unread after Mail settled), do NOT pull and present the full subject/sender list.
This user explicitly cut off that firehose ("stop, I think we need to reconsider our
approach"). The correct workflow:
1. Get unread counts per mailbox (reliable even under load).
2. Pull senders (or subjects) so you can bucket by domain.
3. Group into **noise** (retail/food/newsletter promos: Shutterfly, Uber Eats, IHOP,
   Whole Foods, CVS, Pinterest, LinkedIn promos, etc.) vs **signal** (real people,
   security logins, account/billing, job alerts, healthcare, neighborhood/local).
4. Deliver a ONE-SCREEN summary that flags only the signal items and reports the
   noise as a count, then OFFER next actions (retry details, bulk-mark-read / bulk
   delete a confirmed sender list, or leave for a manual sweep). Never dump the full
   list at the user without asking.
Common signal senders this user cares about: Instagram security@, Google
noreply-accounts@ (settings/security), Apple Billing, X account security, LinkedIn
job alerts, Stanford Health Care, banking/bill pay (PG&E), Nextdoor neighborhood
alerts, church (LDS) communication, photography/creative dev newsletters from known
creators (Dehancer, SIRUI, Photzy Contrastly, gamut.io).

### Get unread COUNTS first, per-message detail second
On large, heavily-synced Gmail INBOXes, the per-message `repeat with m in (every
message ... whose read status is false)` loop (with per-message formatting) can
throw **AppleEvent timed out (-1712)**. Prefer the **single whole-list fetch**,
one field per call — `get subject of every message of mailbox "INBOX" of account
"Google" whose read status is false` succeeded even on a 278-item Gmail INBOX;
run subject and sender as SEPARATE calls (see `references/apple-mail-unread-check.md`).
The `unread count of mailbox X of account Y` call also returns reliably even when
detail fetches hang. Graceful degradation:

1. `unread count` per mailbox → trustworthy counts even if detail fails. ⚠️ Counts
   are PROVISIONAL while Mail is still sync-fetching a large mailbox (saw 27, then
   278 after it settled) — re-query before trusting a surprising low number.
2. Sum across accounts so none is silently missed.
3. Only then fetch per-message subjects/senders via the single-list form, smallest
   inbox first. If a large INBOX still times out, report the reliable count and offer
   to retry detail once Mail settles — do NOT re-hammer it, since repeated AppleEvent
   queries make Mail progressively unresponsive.

### Availability of the CLI path matters
Apple Mail via `osascript` is the reliable unified path on this machine; the
`himalaya` CLI and any Hermes email gateway adapter may be absent/unconfigured.
Check which path exists (`which himalaya`, config) before assuming the CLI route;
do not treat an absent CLI as an error with the osascript path still viable.

## References
- See `references/apple-mail-observations.md` for session-specific notes.
- See `references/apple-mail-unread-check.md` for a verified multi-account unread-checking command transcript (account/mailbox mapping, -1728/-1712 error table, robust count-then-detail workflow).
- Script `scripts/check_unread.applescript` provides a ready-to-run AppleScript for fetching unread subjects.
- See `references/apple-mail-observations.md` (2026-07-13) for detailed session observations.

## Additional Notes (2026-07-15)

-* AppleScript `unread count` is not accessible for all accounts; consider using `himalaya` CLI for unified inbox queries.
-* Accessing iCloud mailboxes via AppleScript may return empty results; verify account type and consider using IMAP or `himalaya` for cross-account visibility.
-* Running AppleScript via `osascript` in background processes can cause “backgrounding” errors; use `terminal(background=true)` for loops and ensure proper quoting.
-* App passwords for Exchange may expire; schedule periodic re-authentication.

## Alternative: Using Himalaya CLI

For a more robust, scriptable approach across Exchange, Google, and iCloud, consider using the `himalaya` CLI:

```bash
# List unread counts per account
himalaya inbox:unread --format=summary

# Fetch the subject of the first unread message in Google's inbox
himalaya message:first --account=Google --folder=INBOX --unread --output=subject
```

The CLI handles authentication via OAuth and provides consistent output across providers.