# Apple Mail — Cross-Account Sender Search (Verified)

Recipe for finding and reading all emails from a specific sender across every
account in Apple Mail, using osascript. Verified against a 3-account setup
(iCloud, Google/Gmail, Exchange).

## Why write the script to a file

AppleScript uses `&` for string concatenation. If you inline the script in a
terminal command, the shell treats `&` as backgrounding and the tool rejects
it ("Foreground command uses '&' backgrounding"). **Always write the script to
a `.scpt` file with `write_file`, then run `osascript /path/file.scpt`.**

## Key pitfalls

- **Account-level message queries fail.** `(every message of <account> whose
  sender contains ...)` throws `-1728` “Can't get every message of account”.
  Query the mailbox instead: `(every message of mailbox "INBOX" of a ...)`.
- **Inbox folder name differs by provider** — Gmail uses `"INBOX"`, iCloud
  may use `"Inbox"`. Wrap the query in `try`/`on error` and retry the other
  spelling, or just try/ignore and iterate accounts.
- **Body content:** `content of m` returns the message body. After locating a
  message by sender, re-run a second pass to build subject + received-date +
  body in one output string.

## Verified script (full two-pass)

Pass 1 — find senders:

```applescript
-- /tmp/check_sender.scpt
tell application "Mail"
    set foundMessages to {}
    set theAccounts to accounts
    repeat with a in theAccounts
        try
            set mb to mailbox "INBOX" of a
            set theseMsgs to (every message of mb whose sender contains "example.org")
            repeat with m in theseMsgs
                set end of foundMessages to (subject of m) & " | " & (sender of m) & " | " & (date received of m)
            end repeat
        on error errMsg
            try
                set mb to mailbox "Inbox" of a
                set theseMsgs to (every message of mb whose sender contains "example.org")
                repeat with m in theseMsgs
                    set end of foundMessages to (subject of m) & " | " & (sender of m) & " | " & (date received of m)
                end repeat
            end try
        end try
    end repeat
    return foundMessages
end tell
```

Pass 2 — read a specific sender's body:

```applescript
tell application "Mail"
    set theAccounts to accounts
    set outMsg to ""
    repeat with a in theAccounts
        try
            set mb to mailbox "INBOX" of a
            set theseMsgs to (every message of mb whose sender contains "Membersupport@example.org")
            repeat with m in theseMsgs
                set outMsg to outMsg & "=== SUBJECT: " & (subject of m) & " ===" & linefeed
                set outMsg to outMsg & "=== RECEIVED: " & (date received of m) & " ===" & linefeed
                set outMsg to outMsg & "=== FROM: " & (sender of m) & " ===" & linefeed
                set outMsg to outMsg & (content of m) & linefeed & linefeed
            end repeat
        end try
    end repeat
    return outMsg
end tell
```

## Domain-match note

Using `sender contains "example.org"` (a domain fragment) catches both the
generic box (`Membersupport@example.org`) and individual staff
(`Jane.Doe@example.org`) in one query — useful when only the organization is
known.