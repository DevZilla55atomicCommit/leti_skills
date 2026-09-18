---
name: instagram-unavailable-content-handling
title: Instagram Unavailable Content Handling
description: How to detect and log unavailable Instagram reel URLs.
---

# Instagram Unavailable Content Handling

## Typical Causes
- Post deleted by creator
- Post made private
- Content removed due to policy violation
- **Account deleted/suspended**
- **Content expired** (Stories/limited-time content like Stories highlights)
- **Geo-blocked**content restricted in certain regions
- **Age-restricted**requires age verification
- **Copyright claim**content taken down

## Detection Pattern
The Instagram web UI returns a page with title `Post isn't available • Instagram` and a snapshot containing:
- Link `Instagram`
- Link `Log in`
- Button `Sign up for Instagram`

## Bot Detection Considerations
- No residential proxies used
- Aggressive bot detection may block access to private/invite-only content
- Use Browserbase with residential proxies for reliable access

## Workflow
1. Navigate to URL via `browser_navigate`
2. If the URL appears in a Block *.rtf file (e.g., `/Users/alfredkamisese/Desktop/Block 2.rtf`), open it with `read_file` and search for the reel ID using `search_files` or regex to verify its status locally before proceeding.
3. Check snapshot for `Post isn't available` text
4. If present, log as ❌ Unavailable and skip
5. Optionally record URL and status in queue file

## Detection Patterns
- **Page Title**: `Post isn't available • Instagram`
- **Snapshot Elements**:
  - Link labeled `Instagram`
  - Link labeled `Log in`
  - Button `Sign up for Instagram`
- **Common Triggers**:
  - Deleted posts (`https://www.instagram.com/reel/...`)
  - Private accounts restricting content visibility
  - Posts removed due to policy violations
  - Account deleted/suspended
  - Content expired (Stories/Highlights)
  - Geo-blocked content
  - Age-restricted content
  - Copyright claims

## Bot Detection Notes
- Occurs when accessing without residential proxies
- Aggressive bot detection may block invite-only/private content
- Workaround: Use Browserbase with residential proxy rotation

## Logging Template
When identified as unavailable:
- Mark status as ❌ Unavailable
- Append note: `Deleted/private – inaccessible due to Instagram removal or privacy settings`
- Record in queue file with timestamp if needed for future reference

## Example Logging
- Mark as ❌ Unavailable in queue
- Add note: `Deleted/private – inaccessible due to Instagram removal or privacy settings`
- Record in queue file with timestamp if needed for future reference