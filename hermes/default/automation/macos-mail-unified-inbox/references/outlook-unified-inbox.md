# Outlook Unified Inbox via Apple Mail

## Quick Setup

1. **Generate an Outlook App Password**
   - Sign in to your Microsoft account → **Security** → **App passwords** → **Create a new app password**.
   - Copy the 16‑character password (no spaces).

2. **Add Outlook to Apple Mail**
   - Open **Mail** → **Preferences** → **+** → **Other Mail Account**.
   - Enter your Outlook email address (`your-email@outlook.com`) and paste the App Password as the **password**.
   - Complete the setup; the account appears alongside iCloud and Gmail in the unified inbox.

3. **Verify (Optional)**
   - **IMAP**: `outlook.office365.com`, Port `993`, TLS.
   - **SMTP**: `smtp.office365.com`, Port `587`, StartTLS.
   - These are handled automatically; no manual alias configuration needed.

## Benefits
- Unified view of Outlook, iCloud, and Gmail emails.
- No duplicates; messages stay in their native accounts.
- Full search and filter capabilities via Apple Mail.

## Common Pitfalls
- **Basic Auth Blocked** – Use the App Password; basic authentication is disabled.
- **IMAP Not Enabled** – Enable IMAP under **Settings → Mail → Sync email → IMAP** on Outlook.com.
- **Password Changes** – Regenerate the App Password if you change your Microsoft password.

## When to Use
- **Use** for a simple native integration without separate gateways or MCP setups.
- **Avoid** if you need advanced server‑side filtering not supported by Apple Mail’s unified inbox.