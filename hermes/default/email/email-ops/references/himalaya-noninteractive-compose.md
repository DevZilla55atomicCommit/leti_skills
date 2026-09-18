# Himalaya Non-Interactive Compose Pattern

## Problem
`himalaya message write`, `message forward`, and `message reply` all open `$EDITOR` interactively. They do NOT accept body text via stdin. This causes failures in non-TTY environments (agents, scripts, background processes).

## Solution
Use `himalaya template send` with piped MML input for all non-interactive sends.

## Commands

### Send New Email
```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

### Forward Email
```bash
# Get forward template, modify To header, and send
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### Reply to Email
```bash
# Get reply template, inject body after blank line, and send
himalaya template reply 42 | sed 's/^$/\\nYour reply text here\\n/' | himalaya template send
```

## MML Notes
- MML (MIME Meta Language) is simple XML-based syntax
- Headers first, blank line, then body
- Use `<#part>` tags for attachments (see `himalaya/references/message-composition.md`)
- `template send` compiles MML → MIME and sends via SMTP

## Verified
- Works in non-TTY environments
- No `$EDITOR` required
- Exit code 0 on success, non-zero on failure (check for duplicate delivery risk if retrying)

## Related
- `himalaya/references/message-composition.md` — MML syntax reference
- `email-ops/references/email-send-policy.md` — Draft collaboration policy (user must confirm before send)