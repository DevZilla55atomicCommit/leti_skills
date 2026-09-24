---
name: email-ops
description: "Unified email operations hub for Hermes Agent, consolidating apple-mail and himalaya workflows with documented pitfalls and verified patterns."
category: email
version: 1.0.0
tags: ["email", "automation", "outlook", "gmail", "icloud", "imap", "mail", "crash"]
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: ["email", "automation", "outlook", "gmail", "icloud", "imap", "mail"]
    category: email
---

# Email Ops — Unified Workflow & Pitfall Reference

**Purpose**: Central knowledge hub for reliable email operations in Hermes, combining `himalaya` (IMAP/SMTP) and `apple-mail` (Apple Mail scripting) while documenting verified pitfalls and preferred patterns.

## Why This Exists

Previous sessions discovered critical issues:
- Outlook.com forwarding can take 15-45 minutes to deliver to Gmail [Tested]
- Personal Outlook.com accounts no longer support app passwords after 2026
- Duplicate delivery risk with outdated TOML alias syntax in `himalaya` v1.2.0
- Real-time checks require `apple-mail` instead of relying on IMAP forwarding

This skill consolidates those lessons into reusable workflows.

## Class-Level Scope

This umbrella skill governs all email operations that require:
- Cross-account email enumeration
- Message retrieval without GUI automation
- Forwarding delay awareness
- App password alternatives
- Structured message processing for Hermes workflows

## Core Skills in This Ecosystem

| Skill | Purpose | Primary Commands |
|-------|---------|------------------|
| `himalaya` | IMAP/SMTP email management | `himalaya envelope list`, `himalaya message read` |
| `apple-mail` | Direct Apple Mail control via osascript | `osascript` queries, message flags |
| `email-ops` | Orchestrates email workflows & documents pitfalls | This skill |

## Verified Workflows

### 1. Draft Creation per Account
- **Gmail**: use `himalaya template save` — IMAP works and the `[Gmail]/Drafts` mapping is configured.
  ```bash
  cat << 'EOF' | himalaya template save --account gmail --folder "[Gmail]/Drafts"
  From: reeves.kamisese@gmail.com
  To: recipient@example.com
  Subject: Draft subject

  Draft body.
  EOF
  ```
- **Outlook/Exchange**: `himalaya` cannot touch it (IMAP password auth rejected) — create the draft via Apple Mail scripting instead. The `sender` address routes the draft to that account's Drafts mailbox:
  ```applescript
  -- write to /tmp/make_draft.scpt, then run: osascript /tmp/make_draft.scpt
  tell application "Mail"
    set theMessage to make new outgoing message with properties {sender:"alfred.kamisese@outlook.com", subject:"Draft subject", content:"Draft body.", visible:false}
    tell theMessage
      make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
    end tell
    save theMessage
  end tell
  ```
  The same pattern works for Gmail (`sender:"reeves.kamisese@gmail.com"`, account `"Google"`) — verified in both Drafts mailboxes.
- **Verify every draft by reading it back** — list `subject of every message of mailbox "Drafts" of account "Google"` / `"Exchange"` and confirm the subject is present. A `save` that reports success without a read-back is unverified.

### 2. Safe Outlook Handling
- **Problem**: App passwords deprecated; forwarding delays cause stale data
- **Solution**: Use `apple-mail` skill for immediate checks; verify forwarding manually before relying on automated workflows
- **Example**:
  ```bash
  # Check unread across all accounts instantly
  /skill apple-mail "Show all unread emails"
  ```

### 3. Forwarding Delay Shield
- **Mechanism**: Add delay awareness to cron jobs
- **Implementation**: Cron uses `apple-mail` skill with `--status` check before processing
- **Reference**: `references/forwarding-delay-check.md`

### 4. Alias Syntax Enforcement
- **Rule**: Always use `folder.aliases.X` (plural) syntax in TOML
- **Pitfall**: Pre‑v1.2.0 used `[accounts.NAME.folder.alias]` which is silently ignored
- **Verification**: `grep -r "folder.aliases" ~/.config/himalaya/`

### 5. Cross-Account Sender Search (Apple Mail)
Search every account's Inbox for messages from a specific sender/domain — the durable pattern when you need "is there any mail from X across all my mailboxes".

```applescript
-- write to /tmp/search_sender.scpt, then run: osascript /tmp/search_sender.scpt
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
        end try
    end repeat
    return foundMessages
end tell
```

- **Use `sender contains` with a domain fragment** — catches both `Membersupport@example.org` *and* `Jane.Doe@example.org` under one query.
- **Query at the mailbox level, never `every message of <account>`** — account-level message queries throw `-1728` ("Can't get every message of account"). Querying `mailbox "INBOX" of a` (or `"Inbox"` for iCloud, `"INBOX"` for Gmail) avoids this. Try both Inbox spellings in a try/on-error fallback since account folder naming differs.
- **Read a message's body** with `content of m` after locating it by sender; compose subject + body in a second pass.
- See `references/apple-mail-sender-search.md` for a fuller script with a body-read pass.

### 6. Himalaya CLI Argument Shapes
- Pass `--account` and `--folder` on the subcommand (`himalaya envelope list --account gmail --folder INBOX`) — the account flag does not go before the subcommand.
- IDs and flags are positional with no `--id` / `--flag` options: `himalaya message read --account gmail --folder INBOX 110999`, `himalaya flag add --account gmail --folder INBOX 110986 110987 seen` — anything parseable as an integer is an ID, anything else a flag.
- Pipe stderr away when parsing `--output json` — IMAP codec warnings print on stderr and corrupt JSON parsing under `2>&1`. Use `2>/dev/null`.

## Integration Points

- **Draft Collaboration Policy**: All email reply drafts must be collaboratively refined with the user before any send operation. The system must never execute `himalaya template send` or any send command without explicit user confirmation phrase ('send it', 'send now').

- **Cron Automation**: `Good Morning Email Briefing` job now references this skill
- **Onboarding**: New users must read `references/outlook-pitfalls.md` before setup
- **Error Recovery**: When `himalaya` returns duplicate delivery errors, consult this skill

## References (Session-Specific Detail)

- `references/outlook-pitfalls.md` — Full reproduction of Outlook forwarding delay test results
- `references/email-send-policy.md` — Draft Collaboration Safety Policy with explicit send phrase requirements and enforcement mechanism
- `references/himalaya-alias-fix.md` — TOML syntax correction guide
- `references/apple-mail-sender-search.md` — Verified cross-account sender search (two-pass .scpt, -1728 pitfall, write-to-file trap)
- `scripts/check-forwarding.sh` — Delay verification script