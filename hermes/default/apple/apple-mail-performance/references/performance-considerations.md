# Performance & Robustness for Apple Mail Automation

## 1. Large Mailboxes (>5,000 messages)
- **Problem**: Full iteration can exceed script timeouts.
- **Mitigation**: 
  - Limit to recent N messages (e.g., 500) or filter by `date received`.
  - Apply sender filters before full iteration.

## 2. Gmail/IMAP Account Quirks
- Some accounts expose inbox under non‑standard names (e.g., “All Mail”).
- **Solution**: Enumerate mailboxes and fallback to case‑insensitive match on “inbox”.

## 3. Thread / Duplicate Handling
- Multiple replies inflate message count.
- **Fix**: Filter on unique `message id` to process each conversation once.

## 4. iCloud Mailbox Structure
- Primary inbox may not be named “INBOX”; use case‑insensitive matching on known inbox substrings.

## 5. Message ID Uniqueness
- Use `message id` to de‑duplicate across threads.

> **Testing tip**: Run filter conditions with a small `osascript -l JavaScript` snippet before scaling to full iteration.