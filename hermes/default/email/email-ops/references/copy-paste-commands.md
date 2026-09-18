## Ready-to-copy commands for Hermes Mac mini

```bash
# 1. Check Gmail (default)
himalaya envelope list

# 2. Check iCloud
himalaya envelope list --account icloud

# 3. Check Outlook
himalaya envelope list --account outlook

# Read a specific message (replace <ID> with the number shown)
himalaya message read <ID>

# Bonus: copy all three listings at once
himalaya envelope list && echo "--- ICLOUD ---" && himalaya envelope list --account icloud && echo "--- OUTLOOK ---" && himalaya envelope list --account outlook
```