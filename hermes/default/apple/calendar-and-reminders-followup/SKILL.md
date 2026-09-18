---
name: calendar-and-reminders-followup
title: Schedule dated follow-ups across Apple Calendar + Reminders
description: Schedule a dated follow-up in both Calendar and Reminders.
category: apple
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [calendar, reminders, followup, schedule, osascript, remindctl, macos]
    category: apple
---

# Calendar + Reminders Follow-Up Scheduling

**Purpose**: When the user asks to be reminded of a dated follow-up — a claims/invoice review window, a callback, a deadline, a "check back on X" — create it in **both** Apple Calendar and Apple Reminders so it syncs to iPhone/iPad, and verify both landed. This is the user's expected pattern: primary entry PLUS a backup day, each in both apps.

## When to Use
- User asks to "set a reminder" and wants it on their phone / all devices.
- A business email states a review/decision window (e.g. "allow up to 60 days") and the user wants a follow-up call scheduled.
- Any dated task the user wants surfaced as both a block of time (Calendar) and a to-do (Reminders).
- A backup/second-attempt day is wanted in case the primary follow-up is unresolved.

## Target Dates Before You Probe
Compute the follow-up date FIRST, confirm the numeric date out loud, then schedule.
- Example: an email received **June 18, 2026** citing a 60-day window → follow-up is **Mon, Aug 17, 2026**; backup ~2 days later.

## Steps

### 1. Confirm target calendar / reminder list exist
```bash
osascript -e 'tell application "Calendar" to return name of every calendar'
remindctl list
```
Use a semantically-relevant calendar (e.g. "Health Appoinments" for healthcare claims), not the default "Calendar" blindly. remindctl uses the default list unless `--list` is passed.

### 2. Calendar event via osascript (.scpt file — see Pitfalls)
Write to `/tmp/foo.scpt`, then `osascript /tmp/foo.scpt`:
```applescript
tell application "Calendar"
    tell calendar "Health Appoinments"
        set newEvent to make new event with properties {summary:"...", start date:date "Monday, August 17, 2026 at 9:00:00 AM", end date:date "Monday, August 17, 2026 at 9:30:00 AM", description:"context / call number"}
        make new display alarm at newEvent with properties {trigger interval:-900}  -- 900 s = 15 min before
    end tell
end tell
```
- Date string must match system locale exactly: `"Weekday, Month DD, YYYY at HH:MM:SS AM"`.
- `display alarm` with `trigger interval` in **seconds** (negative = before).

### 3. Reminder via remindctl (separate --due and --alarm)
```bash
remindctl add --title "..." --due "2026-08-17 09:00" --alarm "2026-08-17 08:00"
```
- `--due` is the due time; `--alarm` is a separate earlier nudge. Pass both explicitly when the user wants an early notice.
- `--list Tasks` to target a specific list, or `--list Work`.

### 4. Verify BOTH (do not trust the create output alone)
```bash
remindctl 2026-08-17                                # reminder by date filter
osascript -e 'tell application "Calendar" ... every event whose summary contains "KEYWORD" ...'
```
- Reminders with a future due date are **not** in `remindctl today` — query the specific date instead.
- remindctl auto-mirrors as a "Scheduled Reminders" calendar event on iOS/macOS; that's expected, not a duplicate to remove.

## Pitfalls
- **Inline osascript with `&` breaks.** AppleScript uses `&` for string concatenation; the Hermes shell parses `&` as backgrounding and rejects the inline command. **Always write the script to a `.scpt` file with write_file, then `osascript /path/file.scpt`.** Do not inline `osascript <<'EOF'` blocks that contain `&`.
- **Calendar app must have Automation permission** (first run prompts in System Settings → Privacy & Security → Automation); remindctl needs Reminders permission (`remindctl authorize`).
- **Date locale mismatch** → Calendar event silently not created or throws. Match the exact system format; verify by re-query.
- **Typo'd/absent calendar names are fatal** — use exact names from step 1.

## Verification
Re-run the calendar query filtered by summary keyword and `remindctl <date>` after creation; confirm both rows are present before telling the user it's done.