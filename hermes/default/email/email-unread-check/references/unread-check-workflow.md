# Unread Email Detection Workflow

## Overview
This document captures the end‑to‑end process for reviewing unread messages across Himalaya‑managed email accounts (Gmail, iCloud, Outlook) using the `himalaya` CLI.

## Command Workflow

### 1. List Available Accounts
```bash
himalaya account list
```

Output example:
```
| NAME    | BACKENDS   | DEFAULT |
|---------|------------|---------|
| gmail   | IMAP, SMTP | yes     |
| icloud  | IMAP, SMTP |         |
| outlook | IMAP, SMTP |         |
```

### 2. Enumerate Inbox Messages per Account

#### Gmail
```bash
himalaya envelope list --account gmail --folder INBOX --page-size 20 --output json
```

#### iCloud
```bash
himalaya envelope list --account icloud --folder INBOX --page-size 20 --output json
```

#### Outlook (Exchange)
```bash
himalaya envelope list --account outlook --folder INBOX --page-size 20 --output json
```

> **Note**: Outlook often fails with authentication errors (`AUTHENTICATE failed`). Use Apple Mail for Outlook/Exchange accounts when possible.

### 3. Parse Output
Each message object contains `id`, `flags`, `subject`, `from`, `date`.
Filter for messages where `flags` does **not** include `Seen` to identify unread messages.

### 4. Common Pitfalls & Fixes
- **Outlook Authentication Failure**: The CLI cannot log in via IMAP; use Apple Mail or configure credentials via macOS Keychain.
- **Folder Alias Syntax**: Pre‑v1.2.0 configurations used singular `[accounts.NAME.folder.alias]`. Starting with v1.2.0, use plural dotted keys (`folder.aliases.X`) directly under `[accounts.NAME]`. Using the old singular form silently fails when saving to "Sent" because the alias resolver never reads the setting, leading to duplicate email deliveries on retry.
- **Duplicate Delivery on Retry**: When a send operation fails after SMTP success (e.g., due to alias mis‑configuration) the client may re‑send the message, causing duplicates. Always verify alias keys are correctly spelled and placed.
- **Missing Mailbox Names**: Some providers use non‑canonical names (e.g., "iCloud" vs "INBOX"). Explicitly specify `--folder` to avoid ambiguity.

### 5. Example Summary Script (Optional)

```bash
#!/usr/bin/env bash
# List unread counts per account
for acc in gmail icloud outlook; do
  echo "=== $acc ==="
  himalaya envelope list --account "$acc" --folder INBOX --output json
done
```

Make the script executable (`chmod +x check-unread.sh`) and run it to get a concise unread summary.

## References
- Detailed command breakdown and error transcripts are captured in session logs.
- The workflow incorporates pitfalls observed during recent debugging sessions.