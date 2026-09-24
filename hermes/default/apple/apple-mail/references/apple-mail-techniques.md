# Apple Mail Techniques (Reference)

## Alfred's Account Setup (Verified 2026-08-13)

| Account | Inbox Mailbox Name | Status |
|---------|-------------------|--------|
| Exchange | "Inbox" | ✅ Works |
| iCloud | Likely "INBOX" | ⚠️ Needs verification |
| Google (Gmail) | Likely "INBOX" | ⚠️ Needs verification |

**Accounts list**: `osascript -e 'tell application "Mail" to get name of every account'` → iCloud, Google, Exchange

## Date-Range Query (Yesterday → Today) — Working Pattern

```bash
osascript -l JavaScript << 'EOF'
function run() {
  const Mail = Application('Mail');
  const results = [];
  const accounts = ["iCloud", "Google", "Exchange"];
  
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  yesterday.setHours(0, 0, 0, 0);
  today.setHours(23, 59, 59, 999);
  
  for (const accName of accounts) {
    try {
      const account = Mail.accounts.byName(accName);
      if (!account) continue;
      
      // Try both "Inbox" and "INBOX"
      let inbox = null;
      try { inbox = account.mailboxes.byName("Inbox"); } catch(e) {}
      if (!inbox) { try { inbox = account.mailboxes.byName("INBOX"); } catch(e) {} }
      if (!inbox) continue;
      
      const messages = inbox.messages();
      const count = messages.length;
      
      for (let i = 0; i < count; i++) {
        const msg = messages[i];
        const dateReceived = msg.dateReceived();
        
        if (dateReceived >= yesterday && dateReceived <= today) {
          results.push({
            account: accName,
            subject: msg.subject(),
            sender: msg.sender(),
            date: dateReceived.toISOString(),
            read: msg.readStatus(),
            id: msg.id()
          });
        }
      }
    } catch (e) {
      results.push({account: accName, error: e.toString()});
    }
  }
  return JSON.stringify(results, null, 2);
}
EOF
```

## Unread Message Detection Script

```bash
osascript -l JavaScript -e '
const Mail = Application("Mail");
const results = [];
for (const acct of Mail.accounts()) {
    const inbox = acct.mailboxes.byName("Inbox");
    if (inbox) {
        const msgs = inbox.messages.whose({readStatus:false});
        msgs.forEach(m => {
            results.push({
                account: acct.name(),
                subject: m.subject(),
                sender: m.sender(),
                date: m.dateReceived(),
                id: m.id()
            });
        });
    }
}
console.log(JSON.stringify(results));
'
```

## Handling Case-Sensitive Mailbox Names

```bash
# Check available mailbox names
osascript -e 'tell application "Mail" to get name of every mailbox of account "Exchange"'
```

## Automation Permission Checklist

- System Settings → Privacy & Security → Automation
- Enable your terminal (e.g., Terminal, iTerm) → Mail.app

## Common Errors & Fixes

- `Not authorized to send Apple events` → Grant Automation permission.
- `Can't get mailbox "X"` → Verify exact mailbox name using `osascript` command above.