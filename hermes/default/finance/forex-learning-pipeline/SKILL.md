---
name: forex-learning-pipeline
description: 'Use when adding forex education research to the vault.'
version: 1.0.0
platforms: [macos]
---

# Forex Learning Pipeline (Vault Research Workflow)

End-to-end pattern for turning web/YouTube/X research into Obsidian study notes under `Hermes Agent/Forex Center/`. Built 2026-09-10; reuse for any future topic batch.

## Vault root

- Physical: `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/` (USB, exFAT — junk `._*`/`.DS_Store` reappear; clean per batch)
- Symlink: `~/TamaZila_Obsidian_Vault`. Forex hub: `Hermes Agent/Forex Center/MASTER_INDEX.md`.
- Prefer file tools (`write_file`, `patch`, `read_file`) over shell; `cp`/`mkdir`/`ls` via terminal are safe without approval, `find -delete` ALWAYS needs explicit user approval first.

## Workflow

### 1. Discover (web_search, broad → narrow)

Rankings first (`best forex trading YouTube channels beginners`, `best free forex courses 2026`, `best forex accounts X beginners`), then specifics. Record source URLs; NEVER invent video URLs, channel URLs, or X handles — if a handle isn't in a source, mark it "find via ranking page".

### 2. Verify (web_extract before cataloging)

Extract ranking pages + curriculum pages (3–5 URLs per call). Only catalog entries confirmed by page content. Mark everything unwatched/unverified with `status: catalog-v1-unwatched` frontmatter until consumed.

### 3. YouTube transcripts (youtube-content script, macOS notes)

- Script: `/Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py`. Run with system `python3`, NOT `uv run` (no venv on this Mac; `uv pip install --system` also fails on system site-packages — package is already in user site-packages, just call `python3 <script>`).
- `--text-only` to `/tmp`, then sample BEFORE writing: head 3KB + tail 1.5KB + a middle word-slice + chapter signals via `grep -io "chapter ..."`. 80K-word transcripts are multi-hour courses — never pretend full consumption from samples.
- Archive raw transcript to `Momentum/Transcripts/<Name>_<videoID>_transcript.txt` (searchable future input), then write a structured study note: author, chapter map, study method, cross-links to Concepts notes, and an **Honest flags** section (marketing/funnel claims called out, income screenshots unverified).

### 4. Web synthesis notes

One note per extraction batch: distill (not paste) into sections with source links, map each section to the roadmap phase or concept note it feeds (`Beginner_Roadmap`, `Position_Sizing_101`, `Glossary_Pips_Lots_Leverage`).

### 5. X (strict boundary)

- `xurl` CLI may be installed by agent (`~/.local/bin/xurl`), but app registration + OAuth is USER-ONLY, outside agent sessions; never touch secrets. Until authed, X is manual-observation: sourced handles + scam filter only, zero fabricated posts.
- Handles go in notes only when a ranking article prints them; otherwise names with "find via ranking page".

### 6. Index wiring (every batch)

- Frontmatter on all notes: `type` (guide/reference/concept/study-notes), `domain: forex`, `area`, `status`, `updated: YYYY-MM-DD`.
- Add a MASTER_INDEX.md table row per new note; update README stubs' status lines if touched.
- NEVER invent the user's trading numbers (pairs, risk %, platform) — stubs stay TODO until user supplies them.

## Lessons (why)

- Raw transcripts in-vault beat re-fetching: chunked study notes can be generated later without network.
- Honest-flags sections preserve trust: lifestyle marketing and course funnels get named, mechanics get verified against existing concept notes.
- Delete-gating once cost a full blocked turn: separate destructive (`find -delete`) from constructive work and get junk-cleanup approval up front alongside scope approval.
