--- 
name: email-setup 
description: Unified email configuration guide for Himalaya CLI across multiple providers 
category: email 
versions: [1.0] 
--- 
## Unified Email Configuration for Himalaya CLI

This reference covers setting up multiple email providers (Gmail, Outlook/iCloud, generic IMAP) with proper folder alias mapping and app password handling.

### Gmail Setup
- **Email**: your-email@gmail.com  
- **App Password**: 16-character password from Google Account → Security → App Passwords  
- **IMAP Settings**:  
  - Host: imap.gmail.com  
  - Port: 993  
  - TLS Encryption  
- **SMTP Settings**:  
  - Host: smtp.gmail.com  
  - Port: 587  
  - StartTLS Encryption  
- **Folder Aliases**:  
  - inbox = "INBOX"  
  - sent = "[Gmail]/Sent Mail"  
  - drafts = "[Gmail]/Drafts"  
  - trash = "[Gmail]/Trash"

### Outlook via Apple Mail (Unified Inbox)
Use Outlook App Password with Apple Mail:
1. Generate an App Password in your Microsoft account security settings.
2. In Apple Mail → Preferences → Accounts → Add Account → Other Mail Account.
3. Enter your Outlook email address and paste the App Password as the password.
4. The account appears in the unified inbox alongside iCloud and Gmail.
5. Search and manage messages directly; no separate gateway or MCP configuration needed.

**IMAP/SMTP (reference only)**
- **IMAP**: Host `outlook.office365.com`, Port `993`, TLS encryption.
- **SMTP**: Host `smtp.office365.com`, Port `587`, StartTLS encryption.

**Critical Notes**
- Microsoft deprecated basic auth; you **must** use an App Password.
- Ensure IMAP access is enabled in Outlook.com under **Settings → View all Outlook settings → Mail → Sync email → IMAP**.
- Apple Mail does **not** expose MCP or gateway settings; it treats the account like any other IMAP server.

### iCloud Setup
- **Email**: your-email@icloud.com  
- **App Password**: Generate via appleid.apple.com → Security → App-Specific Passwords  
- **IMAP Settings**:  
  - Host: imap.mail.me.com  
  - Port: 993  
  - TLS Encryption  
- **SMTP Settings**:  
  - Host: smtp.mail.me.com  
  - Port: 587  
  - StartTLS Encryption  
- **Folder Aliases**:  
  - inbox = "INBOX"  
  - sent = "Sent"  
  - drafts = "Drafts"  
  - trash = "Trash"

### Security Notes
- Never store raw passwords in config files. Use `security find-generic-password` command on macOS or a password manager like `pass`.  
- Ensure each provider's "App Password" is used instead of account password.  
- Verify folder mapping matches your provider's actual folder names to avoid save failures.
### Hermes Integration Tips

- Use `--output json` for programmatic parsing.
- For sending non-interactive emails, pipe via `cat << EOF | himalaya template send`.
- When moving/copying messages between folders across providers, verify alias mappings.

### Gmail Setup (Hermes) - Concise Steps

1. Install Himalaya: `brew install himalaya`
2. Generate Gmail App Password
3. Create `~/.config/himalaya/config.toml` with Gmail settings:

```toml
[accounts.gmail]
email = "your-email@gmail.com"
display-name = "Your Name"
default = true
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.auth.type = "password"
backend.auth.cmd = "security find-generic-password -a your-email@gmail.com -s \"Himalaya Gmail\""
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "security find-generic-password -a your-email@gmail.com -s \"Himalaya Gmail\""
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

4. Connect via Hermes OAuth flow (auto-browser)
5. List emails: `himalaya envelope list --output json`

*Security: App passwords revoke on password change.*