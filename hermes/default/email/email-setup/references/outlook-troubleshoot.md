# Outlook.com IMAP Troubleshooting

## Common Issues
- **Authentication failed**: Ensure you generated an *App Password* (not your regular password) at https://account.microsoft.com/security/app-passwords.
- **Host selection**: Use `outlook.office365.com` for Microsoft 365 (work/school) accounts and `imap-mail.outlook.com` for consumer Outlook.com accounts.
- **IMAP enabled**: Enable IMAP in Outlook settings → Mail → Sync email → POP and IMAP → Enable IMAP.

## Test Connectivity
```bash
himalaya envelope list -a outlook -s 5
```

## Debug Logging
Enable debug logs:
```bash
RUST_LOG=debug himalaya envelope list -a outlook -s 5
```

## Sample Config
```toml
[accounts.outlook]
email = "alfred.kamisese@outlook.com"
display-name = "Alfred Kamisese"
backend.type = "imap"
backend.host = "outlook.office365.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "alfred.kamisese@outlook.com"
backend.auth.type = "password"
backend.auth.raw = "<your-app-password>"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.office365.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "alfred.kamisese@outlook.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "<your-app-password>"

folder.aliases.inbox = "Inbox"
folder.aliases.sent = "Sent Items"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Deleted Items"