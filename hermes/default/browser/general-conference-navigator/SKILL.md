---
name: general-conference-navigator
description: Navigator for General Conference talks in preview pane.
category: browser
---
# Trigger
Use when the user wants to open a specific General Conference talk (e.g., by year/speaker slug) in the Gospel Library preview pane, extract its text, and optionally save for later reference.

# Purpose
Enable reliable access to conference talks for quotation, analysis, or study without manual navigation errors.

# Core Workflow
1. Navigate to `https://www.churchofjesuschrist.org/study/general-conference/<year>/<slug>?lang=eng`.
2. Locate the desired talk link (e.g., “Prayers for Peace” → element `@e75`).
3. Click the link (`browser_click ref=e75`).
4. Capture the full page (`browser_snapshot full=true`).
5. Extract the article text: `document.querySelector('main').innerText`.
6. Verify extraction includes the talk title and speaker.
7. Optionally save the extracted text with `write_file` for later reference.
8. Return the extracted text or file path to the user.

# Pitfalls
- Do **not** rely on element indices without confirming via a fresh snapshot; page components may shift.
- Always request `full=true` before any text extraction or subsequent click.
- The preview pane does **not** retain state across actions; each command must re‑verify the target.
- If the URL structure changes, fall back to searching the General Conference index by keyword.

# Best‑Practice Checklist
- Use `full=true` for any snapshot that will be followed by text extraction or clicking.
- After each click, immediately re‑capture to verify the correct page loaded.
- Store extracted text under `~/.hermes/vault/` with a descriptive filename (e.g., `2026_eyring_prayers_for_peace.txt`).
- Keep a minimal `references/navigation-steps.md` file (see below) to document the exact sequence of tool calls.
- If the target URL changes, search the index page for the talk title before navigating.