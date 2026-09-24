---
name: churchofjesuschrist-navigation
title: ChurchofJesusChrist.org Navigation
description: Guide to browse LDS resources.
category: religious-study
---

## Trigger
Use when researching official LDS resources: scriptures, general conference, come Follow Me, church handbooks, media, music, topics, life help, temples, ordinances, donations, LCR, JustServe, etc.

## Steps
1. Navigate to `https://www.churchofjesuschrist.org/study` for the main study library.
2. Use `browser_navigate` to enter specific sections (e.g., `/media`, `/study/music`, `/study/handbooks`).
3. Use `browser_snapshot` to capture the page and obtain interactive element refs.
4. Click target elements with `browser_click` (prefer element indices from the snapshot).
5. Verify the action succeeded (`effect: 'confirmed'`) and capture a follow‑up snapshot.
6. Extract required data via `browser_console`, `browser_vision`, or `browser_text` as appropriate.
7. Record the final URL and key element refs in a `references/<topic>.md` file for future reuse.

## Pitfalls (Extended)
- Some sections return 404/503; always verify with `browser_snapshot` before proceeding.
- JavaScript‑heavy pages may require a short `seconds` wait before elements render.
- Rapid successive clicks can trigger rate‑limit warnings; add a `seconds` pause if needed.
- Element indices can shift after page interaction; re‑capture to confirm stability.
- **YouTube transcript extraction often fails** — the `browser-use` CLI cannot reliably access YouTube's transcript UI. Workaround: extract from video description/comments, or use a dedicated YouTube transcript API.
- **Come Follow Me lesson pages use dynamic React rendering** — wait 3–5 seconds after navigation before extracting text content.

## Verification
After each `browser_click`, re‑capture to ensure `effect: 'confirmed'`. Use `browser_snapshot` to check that the expected heading or title appears and that `element_count` > 0. If verification fails, scroll (`browser_scroll`) or re‑navigate.

## Support Files
- `references/ldsorg-navigation.md` – session-specific transcripts, error logs, and provider quirks.
- `references/complementary-resources.md` – BYU Studies, followHIM podcast, Gospel Library cross-references.
- `references/come-follow-me-workflow.md` – patterns for weekly Come Follow Me lesson prep (lesson extraction, BYU Studies cross-ref, followHIM podcast integration, visual aid creation).
- `templates/ldsorg-nav-template.md` – starter template for gathering resource metadata.
- `templates/lesson-study-guide-template.md` – HTML template for printable Come Follow Me study guides (timeline, Q&A, cheat sheets, podcast insights).
- `scripts/ldsorg-nav-verify.py` – optional deterministic verification script.