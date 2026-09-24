# Apple Mail Automation Guide

## Overview
Use the `computer_use` skill to interact with Apple Mail.app for unified email handling across Gmail, Outlook, and iCloud accounts. This guide covers common automation patterns for reading, composing, and managing messages in your unified inbox.

## Setup
1. **Scope to Mail.app**: Always specify `app="Mail"` in capture/click actions
2. **Avoid raising windows**: Use `focus_app` or default background routing
3. **Stable element targeting**: Use SOM overlays to identify interactable elements

## Common Actions

### Read Messages
```bash
# Capture inbox with SOM overlay
computer_use(action="capture", mode="som", app="Mail")

# Click on new message count badge (typically element #3)
computer_use(action="click", element=3)

# Read latest message subject
computer_use(action="type", text="")  # Focuses subject line field
subject=$(computer_use(action="key", keys="cmd+c")  # Copy subject
)
echo "Latest subject: $subject"
```

### Compose New Message
```bash
# Focus recipients field
computer_use(action="click", element=7)  # Adjust based on overlay

# Type recipient
computer_use(action="type", text="recipient@example.com")

# Tab to subject
computer_use(action="key", keys="tab")

# Type subject
computer_use(action="type", text="Automated Test")

# Tab to body
computer_use="key", keys="tab")

# Type body
computer_use(action="type", text="This is an automated test message.")
```

### Search & Filter
```bash
# Open search field
computer_use(action="click", element=12)  # Search magnifier icon

# Type search query
computer_use(action="type", text="from:John")

# Press Enter
computer_use(action="key", keys="return")
```

## Pitfalls & Best Practices
- **Element indices change** when new dialogs appear - always re-capture before clicking
- **Multiple accounts** may show separate inboxes - capture each account's root node
- **Large attachments** may trigger permission dialogs - stop and ask user before interacting
- **Unread count badges** update dynamically - verify element position before clicking

## Verification Workflow
After each action:
1. Re-capture the screen with `capture_after=True`
2. Verify expected element is in the same position
3. If UI changed, adjust element indices accordingly

</file_content>