# Outlook via Apple Mail – Unified Inbox Setup

## Quick Summary
- **Goal**: Access Outlook emails inside Apple Mail’s unified inbox without separate gateway or MCP configuration.
- **Method**: Use an Outlook **App Password** and add the account directly to Apple Mail.

## Step‑by‑Step

1. **Generate an App Password**
   - Sign in to your Microsoft account → **Security** → **App passwords** → **Create a new app password**.
   - Copy the 16‑character password (no spaces).

2. **Add Outlook to Apple Mail**
   - Open **Mail** → **Preferences** → **Accounts** → **+** → **Other Mail Account**.
   - Enter your Outlook email address (`your-email@outlook.com`) and paste the App Password as the **password**.
   - Complete the setup; the account appears alongside iCloud and Gmail in the unified inbox.

3. **Verify IMAP Settings (Optional)**
   - **IMAP Host**: `outlook.office365.com`
   - **Port**: `993`
   - **Encryption**: TLS
   - **SMTP Host**: `smtp.office365.com`
   - **Port**: `587`
   - **Encryption**: StartTLS
   - *These are for reference only; Apple Mail handles them automatically.*

4. **Folder Mapping**
   - Apple Mail auto‑maps:
     - **Inbox** → Outlook’s **Inbox**
     - **Sent** → **Sent Items**
     - **Drafts** → **Drafts**
     - **Trash** → **Deleted Items**
   - No manual alias configuration needed.

## Common Pitfalls

- **Basic Auth Blocked**: Microsoft deprecated basic authentication; you **must** use an App Password.
- **IMAP Not Enabled**: Ensure IMAP is enabled under **Settings → Mail → Sync email → IMAP** on Outlook.com.
- **Password Changes**: If you change your Microsoft password, you must regenerate the App Password.

## Benefits

- Unified view of all emails (Outlook, iCloud, Gmail) in one inbox.
- No duplicates; messages stay in their original accounts.
- Full search and filter capabilities via Apple Mail’s UI.

## When to Use This vs. Other Methods
- **Use this** when you want a simple, native integration without separate gateways or cloud‑based MCP setups.
- **Avoid if** you need advanced filtering techniques that require server‑side rules not supported by Apple Mail’s unified inbox.