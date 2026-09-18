---
name: browser-first-search
description: Prefer native browser tools over MCP WebSearch for live site interaction
category: desktop
---

# Browser-First Search Workflow (User Preference)

When a user asks for up-to-date information or wants to explore a live site:

1. **Prefer native browser tools** (`browser_navigate`, `browser_click`, `browser_snapshot`, `browser_type`) over MCP `WebSearch`.
2. Navigate directly to the target URL.
3. Use element indices (`element=N`) for reliable clicks and extracts.
4. Capture with `capture_after=true` to verify state changes.
5. Return concise, verbatim findings without extra formatting unless asked.

**Why**: Native tools render the actual page, handle dynamic content, and avoid third‑party API limits. They also let you inspect the page directly for verification.

**When to fall back to MCP WebSearch**: 
- The target is a pure API endpoint that returns structured data (JSON/XML) and does not require browser interaction.
- The user explicitly requests a summary from the search index rather than live page inspection.

**Common pitfalls**:
- Forgetting to verify with a second capture after a click; always re‑capture to confirm the UI updated.
- Clicking by pixel coordinates; always use element indices unless the page is known to be pixel‑stable.
- Assuming an element persists across navigation; always re‑capture before interacting with a new page state.