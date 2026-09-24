# Outlook.com IMAP Setup (Personal Accounts)

If you're using a personal Outlook.com, Hotmail, or Live account, follow these steps to enable IMAP and create an app password:

1. **Enable IMAP in Outlook.com**
   - Go to <https://outlook.live.com/mail/> → Settings (⚙️) → **View all Outlook settings** → **Mail** → **Sync email** → **POP and IMAP** → **Enable IMAP** → **Save**.

2. **Create an App Password**
   - Visit <https://account.microsoft.com/security> → **Advanced security options** → **App passwords** → **Create new app password**.
   - Name it 'Himalaya IMAP' → **Save** → copy the 16-character password.

3. **Configure Himalaya with Outlook Settings**
   - In `~/.config/himalaya/config.toml`, add an account section:
     ```toml
     [accounts.outlook]
     email = "alfred.kamisese@outlook.com"
     display-name = "Alfred Kamisese"
     default = true

     backend.type = "imap"
     backend.host = "imap-mail.outlook.com"
     backend.port = 993
     backend.encryption.type = "tls"
     backend.login = "alfred.kamisese@outlook.com"
     backend.auth.type = "password"
     backend.auth.cmd = "security find-generic-password -a alfred.kamisese@outlook.com -s \"himalaya-outlook-imap\" -w"
     ```
   - For SMTP (sending), configure similarly with 'imap-mail.outlook.com' on port 587 and STARTTLS.

4. **Troubleshooting**
   - If authentication fails, ensure:
     - IMAP is enabled on Outlook.com.
     - You are using the generated app password (not your main Microsoft password).
     - The correct server hostname ('imap-mail.outlook.com') is used.
     - Test connectivity with `openssl s_client -connect imap-mail.outlook.com:993` to verify TLS.