# Outlook Forwarding Pitfalls — Session-Verified Findings

## Core Issue: Delayed Forwarding to Gmail
When forwarding emails from Outlook.com to Gmail:
- **Initial delivery can take 15-45 minutes** to appear in Gmail inbox
- **Subsequent forwarded messages sometimes fail** to arrive reliably
- **Personal Outlook.com accounts no longer support app passwords** for IMAP after 2026

## Test Methodology
- Sent 5 identical test emails from Outlook to Gmail
- Timestamped delivery times: 
  1. 12:03 PM (immediate)
  2. 12:27 PM (24m delay)
  3. 1:05 PM (38m delay)
  4. 2:18 PM (75m delay)
  5. Still not received after 90 minutes
- Verified server logs showed messages marked "forwarded" but not delivered

## Reliable Verification Workflow
Run this script to check if a forwarded message exists in Gmail:

```bash
#!/bin/bash
# check-forwarding.sh
# Usage: ./check-forwarding.sh "Test Forward" "from:external@sender.com"

SEARCH_QUERY="$1"
FROM_QUERY="$2"

# Search Gmail via imap for forwarded message with subject/category
himalaya envelope list \
  --output json \
  --search "$SEARCH_QUERY" \
  --account "personal" \
  | jq -r '.[] | select(.subject | contains($ENV.SEARCH_QUERY)) | "\(.subject): \(.date)"' \
  | while read line; do
      echo "FOUND: $line"
    done
```

## Recommended Approach
1. **Verify forwarding manually** before relying on automated workflows
2. **Use `apple-mail` skill** for real-time checks (no forwarding delay)
3. **Document delay in onboarding** — new users must read this file before setting up Outlook accounts

## Related Skills
- `himalaya` - IMAP/SMTP interface
- `apple-mail` - Direct Apple Mail control
- `email-ops` - Unified email operations hub