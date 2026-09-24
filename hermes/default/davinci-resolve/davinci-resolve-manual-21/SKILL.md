---
name: davinci-resolve-manual-21
description: Use when answering questions from the Resolve 21.1 manual.
---

# DaVinci Resolve 21.1 Manual — Question Answering

Authoritative source for Resolve facts: the 21.1 Reference Manual (4,351 pages),
distilled into 8 indexed study notes plus the full PDF.

## Answer procedure (in order)

1. **Study notes first.** Check the vault index, then the matching Part note:
   `~/TamaZila_Obsidian_Vault/Hermes Agent/DaVinci_Knowledge_Base/DaVinci Resolve 21/Reference_Manual_21.1/00-MASTER-INDEX.md`
   | Topic | Note | Manual pp. |
   |---|---|---|
   | Setup, prefs, projects, RAW, proxies, RCM/ACES, HDR, sizing | Part-01 | 10–340 |
   | Ingest, bins, conform, Photo page, Cut page | Part-02 | 341–790 |
   | Edit, trim, multicam, transitions, titles, speed, subs | Part-03 | 791–1276 |
   | Fusion nodes, tracking, roto, 3D, particles | Part-04 | 1277–1910 |
   | Fusion tool catalog (37 categories) | Part-05 | 1911–3031 |
   | Color grading palettes, secondaries, node trees | Part-06 | 3032–3484 |
   | Color FX, Resolve FX | Part-07 | 3485–3744 |
   | Fairlight, Deliver, Cloud, collaboration, menus | Part-08 | 3745–4351 |
2. **Exact page lookup.** If the note lacks the detail, query the PDF TOC and read the pages:
   `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -c "import pymupdf; d=pymupdf.open('/Users/alfredkamisese/Desktop/Resolve Manual copy.pdf'); print([x for x in d.get_toc() if 'KEYWORD' in x[1]]"` — then `d[i].get_text()` on the hit (PDF index = printed page − 1).
3. **Answer with a manual page cite** (e.g. "Manual p. 3210 — ColorSlice"). If the manual doesn't cover it, say so and fall back to technique skills.

## Rules

- Manual beats memory: when a palette name, menu path, or default value is in doubt, look it up — never guess.
- Keep answers procedural: where it lives, what it does, key controls, one practical tip.
- Tag manual-sourced answers `#manual-21.1`.
