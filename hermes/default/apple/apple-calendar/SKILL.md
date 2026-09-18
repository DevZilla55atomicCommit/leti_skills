---
name: apple-calendar
description: "Apple Calendar via osascript: list, read, create events."
category: apple
version: "1.0.0"
author: "Maddie"
license: "MIT"
metadata:
  hermes:
    tags: ["apple", "calendar", "osascript", "automation"]
    related_skills: ["apple-reminders", "apple-mail", "apple-notes"]
---

## When to Use
Use when you need to interact with macOS Calendar.app: list calendars, read upcoming events, create new events with optional alerts, or search events by title. Requires macOS and Calendar access permission.

# Apple Calendar via osascript

Manage macOS Calendar.app using `osascript` (AppleScript). Requires macOS and Calendar app with events.

## List all calendars
```bash
osascript << 'EOF'
tell application "Calendar"
    return name of every calendar
end tell
EOF
```

## Read upcoming events (next N days)
```bash
osascript << 'EOF'
tell application "Calendar"
    set now to current date
    set endDate to now + (7 * days)  -- change 7 to desired days
    set eventList to {}
    
    repeat with cal in every calendar
        try
            set calEvents to every event of cal whose start date >= now and start date <= endDate
            repeat with ev in calEvents
                set evTitle to summary of ev
                set evStart to start date of ev
                set evFinish to end date of ev
                set evCal to name of cal
                set end of eventList to {title:evTitle, start:evStart, finish:evFinish, calendar:evCal}
            end repeat
        end try
    end repeat
    
    return eventList
end tell
EOF
```

## Create a new event
```bash
osascript << 'EOF'
tell application "Calendar"
    tell calendar "Work"  -- change to target calendar name
        make new event with properties {
            summary: "Meeting Title",
            start date: date "Monday, August 10, 2026 at 10:30:00 AM",
            end date: date "Monday, August 10, 2026 at 11:30:00 AM",
            location: "Conference Room A",
            description: "Notes here"
        }
    end tell
end tell
EOF
```

## Create event with alert (reminder)
```bash
osascript << 'EOF'
tell application "Calendar"
    tell calendar "Work"
        set newEvent to make new event with properties {
            summary: "Meeting Title",
            start date: date "Monday, August 10, 2026 at 10:30:00 AM",
            end date: date "Monday, August 10, 2026 at 11:30:00 AM"
        }
        -- Add alert 15 minutes before
        make new display alarm at newEvent with properties {trigger interval: -900}  -- seconds before
    end tell
end tell
EOF
```

## Search events by title (case-insensitive)
```bash
osascript << 'EOF'
tell application "Calendar"
    set searchTerm to "meeting"
    set now to current date
    set endDate to now + (365 * days)
    set matches to {}
    
    repeat with cal in every calendar
        try
            set calEvents to every event of cal whose start date >= now and start date <= endDate
            repeat with ev in calEvents
                if (summary of ev) contains searchTerm then
                    set end of matches to {title:summary of ev, start:start date of ev, calendar:name of cal}
                end if
            end repeat
        end try
    end repeat
    
    return matches
end tell
EOF
```

## Pitfalls
- **Date format**: Must match system locale (e.g., `Monday, August 10, 2026 at 10:30:00 AM`)
- **Calendar name**: Must match exactly (case-sensitive)
- **Permissions**: First run prompts for Calendar access in System Settings > Privacy & Security > Automation
- **All-day events**: Use `start date`/`end date` with time at 12:00 AM; `allday event` property exists but is read-only in older macOS
- **Recurring events**: `make new event` creates single instance; recurrence rules require `recurrence rule` property (complex)
- **Time zones**: Calendar uses system time zone; specify in date string if needed

## Verification
After creating an event, re-run the "Read upcoming events" script to confirm it appears.