# macOS Email Setup Guide (Gmail, iCloud, Outlook)

## Overview
- Use **Himalaya** for Gmail/iCloud IMAP.
- Use **AppleScript** for Outlook/Exchange checks.
- Avoid `computer_use` for speed and quota safety.

## Gmail & iCloud Setup
1. Install **Himalaya**:
   ```bash
   npm i -g himalaya-cli
   ```
2. Generate app passwords:
   - Gmail: https://myaccount.google.com/apppasswords
   - iCloud: https://appleid.apple.com/account/manage
3. Configure `~/.config/himalaya/config.toml` with credentials.

## Outlook/Exchange Setup
### Forward to Gmail (Fastest)
1. In Outlook.com → Settings → **Mail > Forwarding**.
2. Enable forwarding to your Gmail address.
3. Verify via Gmail → Settings → **See all settings > Forwarding and POP/IMAP**.

### Direct AppleScript Check (No Forward)
```bash
osascript -e 'tell application "Mail" to get count of messages of mailbox "Inbox" of account "Exchange"'
```

## AppleScript Snippets
- **Check unread**: `tell application "Mail" to get count of messages of mailbox "Inbox" of account "iCloud"`
- **Mark as read**: `tell application "Mail" to mark fully read messages of mailbox "Inbox" as read`

## Automation
- **Cron jobs**:
  - Daily 8 AM: `Good Morning Email Briefing`
  - Every 30 min: `Step Beyond Memory Sync`