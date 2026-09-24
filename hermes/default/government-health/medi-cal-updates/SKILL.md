---
title: Medi-Cal Updates Research
category: government-health
description: Fetch and summarize the latest Medi-Cal program updates from official California government sources (DHCS, Covered California)
name: medi-cal-updates
---

# Medi-Cal Updates Research Skill

## Purpose
Fetch and summarize the latest Medi-Cal program updates from official California government sources (DHCS, Covered California).

## Process
1. Navigate to DHCS Newsroom: https://www.dhcs.ca.gov/newsroom/
2. Review recent news releases for program updates.
3. Check Covered California newsroom: https://www.coveredca.com/newsroom/
4. Extract key updates (date, summary).
5. Compile into a concise bullet list.
6. Reference official pages for details.

## Sources
- DHCS News: https://www.dhcs.ca.gov/
- Covered California Newsroom: https://www.coveredca.com/newsroom/

## Output Format
- Table of recent updates with date and summary.
- Links to source pages.

## Notes
- **Use native browser tools** (`browser_navigate`, `browser_click`, `browser_snapshot`) instead of MCP `WebSearch`.
- **Be concise** — bullet points only, no verbose explanations.
- **Handle 404 gracefully** — if a link is broken, search within the site for the relevant page before giving up.
- **Verify accessibility** — ensure the page loads fully before extracting content.

## Support Files
- `references/latest-updates.md` — recent updates snapshot.
- `templates/check-links.sh` — script to validate source URLs (run before output).
- `scripts/summarize-recent-updates.py` — deterministic summarization script using extractive methods.