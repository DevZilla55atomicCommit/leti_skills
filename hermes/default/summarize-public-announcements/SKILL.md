---
name: summarize-public-announcements
description: Summarize public announcements into concise bullet points.
category: research
tags:
  - summary
  - news
  - public-announcement

---

**Trigger**: Use when the user asks for a concise summary of a public press release, news article, or event announcement (e.g., “Summarize the SDCC 2026 Marvel panel”, “What new characters were announced at Comic‑Con”, “List new actors for Marvel movies”).

**Goal**: Produce a short, bullet‑point summary that highlights:
- New characters/roles announced
- Actors attached
- Associated projects and release dates
- Notable production details (directors, special formats, etc.)
- Any unique or viral moments (e.g., surprise appearances, giveaways)

**Workflow**:
1. Identify the source (URL or attached text) – typically a news article, blog post, or transcript.
2. Scan for headings/subheadings that denote “Cast”, “Announcements”, “Reveals”, or “Key Highlights”.
3. Extract bullet‑level data points:
   - Character name
   - Actor/actress
   - Project (film/series) and announced release window
   - Notable creative staff (director, showrunner)
   - Any special format (e.g., 70mm, IMAX, musical)
4. Verify dates and titles against any provided tables or quoted statements.
5. Assemble bullet points in the user’s preferred style (concise, no fluff, sentence fragments ok).
6. Include a “Sources:” list with markdown links to the original URLs.

**Pitfalls & Tips**:
- **Over‑summarizing**: Resist the urge to add context not requested; keep to the user’s “just the facts” brief.
- **Missing dates**: If a release date is only mentioned as “2028” without month, keep the vague term; do not invent a month.
- **Multiple announcements**: When several characters are listed in a table, extract each row as a separate bullet.
- **User style corrections**: If the user previously said “stop using tables”, “use hyphens instead of pipes”, or “don’t bold anything”, encode that as a hard constraint in the workflow step 5.
- **Fact‑check**: If a date or casting is contradictory across sources, flag it with “⚠️ Inconsistent info – verify”.

**Reference Files**:
- `references/sdcc-2026-summary.md` – example summary of the SDCC 2026 Marvel Hall H panel (includes cast, dates, and key moments).

**See also**: `templates/summary-bullet-template.md` (optional starter template for bullet creation).