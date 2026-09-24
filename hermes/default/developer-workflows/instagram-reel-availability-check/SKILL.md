---
name: instagram-reel-availability-check
title: Instagram Reel Availability Bulk Checker
description: Check a list of Instagram reel URLs to verify public accessibility and basic metadata without manual browsing. Designed for batch validation of educational content links.
author: user
tags: [instagram, verification, batch, color-grading, davinci-resolve, learning]
---

# Instagram Reel Availability Bulk Checker

## Purpose
Automate verification that a set of Instagram reel URLs (typically pointing to DaVinci Resolve tutorial reels) are publicly accessible and load correctly. Useful for maintaining a curated learning queue.

## Trigger
When you have a list of Instagram reel URLs (short links) and need to confirm they are available for inclusion in a knowledge base or learning track.

## Workflow
1. **Prepare URL list**  
   - Store URLs in a plain-text file (one per line) or pass them directly as arguments.  
   - Example: `urls.txt` with each reel ID or full URL.

2. **Iterate through URLs**  
   - For each URL:  
     - `browser_navigate` to the URL.  
     - Wait for page load (snapshot returns without error).  
     - Capture `browser_snapshot` (compact view).  
     - Check for presence of key indicators:  
       - `Video` element in snapshot → likely public reel.  
       - Absence of "Log In" or "Sign Up" buttons → not gated.  
     - Optionally extract title, view count, or engagement markers via regex on snapshot text.

3. **Determine Availability**  
   - If both indicators confirm a public reel, record as **Available**.  
   - If login wall or error page appears, record as **Unavailable** and note reason.  
   - Continue to next URL.

3b. **Enhanced Classification** (v1.1+)  
   - For available reels, run quick content classification:  
     - **Mobile app editing** (Magimir, Snapseed, VSCO, etc.) → Route to Photography/Lightroom/  
     - **Lightroom/Photoshop tutorials** → Route to Photography/Lightroom/  
     - **Promo/Marketing** (preset packs, masterclass promos, "link in bio") → Skip  
     - **Meme/Humor** → Skip (Not Educational)  
     - **Camera Theory** (RAW vs LOG, sensor tech, etc.) → Reclassify to Camera Theory/  
     - **DaVinci Resolve tutorials** → Process normally  
   - Check for age-restricted content ("Age-restricted content", "Log in to continue")  
   - Check for removed/unavailable content ("Content unavailable", "Page not found")

4. **Summarize Results**  
   - After processing all URLs, generate a markdown table summarizing:  
     - Reel ID, Profile, Topic, Status (✅ Available / ⏭️ Skipped / 📸 Photography / 📚 Theory / 🔒 Age-Restricted / ❌ Unavailable).  
   - Use the table as part of your learning queue audit.

## Pitfalls & Fixes
- **Rate limiting** – Instagram may block rapid navigation; add a short `browser_press('Escape')` or `terminal(command='sleep 1')` between requests if needed. 
- **Login wall** – Some URLs may redirect to login; treat any snapshot containing "Log In" as unavailable. 
- **Deleted/Private reels** – Absence of "Video" element indicates removal; mark as unavailable. 
- **Dynamic content** – Captions may load asynchronously; use `browser_scroll` to ensure full load before snapshot.
- **Mobile app detection** – Look for mobile UI overlays, app-specific tool names, finger-touch interactions, portrait orientation with app chrome.
- **Promo detection** – CTA language ("link in bio", "comment X for link", "DM for access"), marketing language ("50+ page guide", "masterclass", "preset pack").
- **404/Deleted content** – Some reels return 404 (deleted, private, expired); skip gracefully with logged reason in SKIPPED_URLS.txt.
- **Age-gated content** – Some reels require age verification; detect "Age-restricted content" or "Log in to continue" patterns.
- **Private accounts** – Cannot be accessed even when logged in; skip immediately.

## Verification
After running the workflow, inspect the generated summary table.  
Example output:
```
| # | Reel ID | Profile | Topic | Status |
|---|---------|---------|-------|--------|
| 1 | DSecyrrDOTK | marcoherbst.work | Skin Separation | ✅ Available |
| 2 | DFgheS3ylWy | lowlight.co | 📚 Camera Theory | RAW vs LOG |
| 3 | DFQOtTcMeD9 | creatorsergeant | ✅ Available | Halation Effect |
| 4 | DFX7MojPCHT | filmsbychristian | ⏭️ Skipped (Meme) | Humor content |
| 5 | DFkhTiNpo7f | moizxmhd | 📸 Photography | Lightroom Vintage |
| 6 | C_rm3h-zMM2 | colorgradeshala | 🔒 Age-Restricted | Blocked |
| 7 | DC1xyivvktJ | takuto_graphy | ❌ Unavailable | Removed |
```

## Extensions
- Integrate with `github-pr-workflow` to automatically open an issue if any URL becomes unavailable.  
- Hook into `cronjob` to schedule weekly availability checks for a curated list.  
- Integrate with `instagram-davinci-learning-pipeline` for automated end-to-end processing.

## Support Files (see `references/` and `scripts/`)
- `references/process.md` – Detailed reproduction of the 50‑URL audit performed on 2026‑07‑11.  
- `references/skip-patterns.md` – Documented skip patterns and classification rules.  
- `scripts/check_reels.py` – Python helper that reads a list of URLs and automates the navigation/snapshot steps via Hermes' toolset.

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-11 | Initial release — batch availability check for 50 URLs |
| 1.1.0 | 2025-07-14 | Enhanced classification: mobile app routing, camera theory reclassification, promo detection, age-restriction handling, removed content detection |