# Himalaya CLI for Unified Inbox

- `himalaya inbox:unread --format=summary` – Shows unread count per account.
- `himalaya message:first --account=Google --folder=INBOX --unread --output=subject` – Retrieves the subject of the first unread message in Google's inbox.
- Authentication via OAuth; works across Exchange, Google, and iCloud accounts.
- Provides consistent JSON output, avoiding AppleScript limitations with iCloud mailboxes.

**Example: List all unread subjects across accounts**

```bash
himalaya messages:list --unread --fields=subject,account | jq -r '.[] | "\(.account): \(.subject)"'
```