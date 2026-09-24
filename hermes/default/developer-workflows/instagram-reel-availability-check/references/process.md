# Bulk Instagram Reel Availability Audit – 2026-07-11

**Scope**: Verified 50 Instagram reel URLs (short links) from `Block 2.rtf` for public accessibility and basic metadata. All URLs were confirmed reachable without login barriers; no unavailable or private reels were found.

## Process Followed

1. **URL Enumeration**  
   - Compiled a list of 50 reel IDs (e.g., `DSecyrrDOTK`, `DSjw-PhDUyp`, …, `DKOnyyEAApg`).  
   - Constructed full URLs: `https://www.instagram.com/reel/<ID>/`.

2. **Automated Verification Loop**  
   - For each URL:  
     - `browser_navigate` to the URL.  
     - Captured a **compact snapshot** (`browser_snapshot`).  
     - Checked for:  
       - Presence of a `Video` element → indicates a public reel.  
       - Absence of “Log In” / “Sign Up” text → not behind a login wall.  
     - If both conditions held, marked the reel **Available**; otherwise **Unavailable** and logged the reason.

3. **Result Compilation**  
   - After processing all 50 URLs, generated a markdown table summarizing:  
     - Reel ID, Profile/Author, Topic Snippet, and ✅ **Available** status.  
   - The table is included in the skill’s main documentation under **Verification** (see `instagram-reel-availability-check` skill).

4. **Quality Assurance**  
   - No inaccessible or deleted reels detected.  
   - All snapshots returned successfully; no HTTP errors observed.  
   - Noted potential rate‑limiting concerns; added `browser_press('Escape')` or `terminal(command='sleep 1')` as optional throttling.

## Outcome

- **All 50 URLs are available** and can be safely added to learning queues, reference vaults, or content‑monitoring pipelines.  
- The audit provides a reproducible template for future batch checks of Instagram reel links.

## Notes for Future Runs

- **Rate Limiting**: Instagram may block rapid navigation; insert a `sleep 1` between requests if processing > 30 URLs.  
- **Login Wall Detection**: Any snapshot containing “Log In” or “Sign Up” should be treated as unavailable.  
- **Dynamic Captions**: Use `browser_scroll` to ensure full page load before snapshot when captions load asynchronously.

---  
*Document generated on 2026‑07‑11 as part of the `instagram-reel-availability-check` skill.*