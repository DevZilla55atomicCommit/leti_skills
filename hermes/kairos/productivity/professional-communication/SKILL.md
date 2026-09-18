---
name: professional-communication
description: "Draft pro emails and calendar events per user prefs."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Communication, Email, Calendar, Drafting, Formatting]
    related_skills: [email-inbox-triage, apple-reminders, google-workspace]
---

# Professional Communication

Draft, format, and deliver professional communications (email replies, calendar invites, messages) following the user's established preferences.

## When to Use

- User needs a reply drafted for an email or message
- User needs an appointment added to a specific calendar
- User asks for a draft to copy-paste
- Any professional correspondence task

## User Preferences (MUST follow)

### Email/Message Draft Format
- **Always deliver drafts in raw code blocks** (```text```) for direct copy-paste
- Never render as formatted prose or markdown outside a code block
- Include subject line when applicable
- Keep tone: professional, friendly, short and sweet (unless user specifies otherwise)

### Calendar Events
- Target calendar: **"Health Appoinments"** for medical appointments
- Include relevant details in description: provider, location, prep instructions, contact who scheduled
- Default duration: 45 minutes for specialist follow-ups
- Use osascript / Calendar.app automation (Apple Calendar on macOS)

## Procedure

### 1. Email Reply Drafting

1. Parse incoming message for: sender, key dates, action items, tone
2. Draft response matching user's stated reason + tone
3. Deliver in ```text``` code block only
4. No extra commentary outside the code block

### 2. Calendar Event Creation

1. Identify target calendar (default: Health Appoinments for medical)
2. Parse date/time from message
3. Create event via osascript with:
   - Summary: clear, descriptive title
   - Start/end: parsed datetime
   - Description: provider, location, prep notes, scheduler contact
4. Confirm event ID returned

## Pitfalls

- Delivering drafts as rendered markdown instead of raw code blocks
- Omitting subject line from email drafts
- Using wrong calendar (always verify "Health Appoinments" for medical)
- Missing prep instructions in event description (labs, medications, etc.)
- Adding explanatory text outside the code block when user wants raw copy-paste

## Verification

- [ ] Draft delivered in ```text``` code block only
- [ ] Subject line included
- [ ] Tone matches: professional, friendly, short
- [ ] Calendar event created in correct calendar
- [ ] Event description includes all relevant details
- [ ] Event ID confirmed
