# Detection Patterns for Unavailable Instagram Reels

## Page Title Indicator
- Look for `"Post isn't available • Instagram"` in the page title

## Snapshot Signature
- Presence of these interactive elements:
  - Link labeled "Instagram"
  - Link labeled "Log in"
  - Button labeled "Sign up for Instagram"

## URL Context
- Applies to any Instagram reel URL that returns this UI state
- Particularly relevant for:
  - Deleted posts (`https://www.instagram.com/reel/...`)
  - Private accounts restricting content visibility
  - Posts removed due to policy violations

## Bot Detection Notes
- Occurs when accessing without residential proxies
- Bot detection may aggressively block access to invite-only or private content
- Workaround: Use Browserbase with residential proxy rotation for reliable access

## Logging Template
When identified as unavailable:
- Mark status as ❌ Unavailable
- Append note: `Deleted/private – inaccessible due to Instagram removal or privacy settings`
- Record in queue file with timestamp if needed for future reference