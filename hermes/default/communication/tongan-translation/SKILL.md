---
name: tongan-translation
title: Tongan Translation (Lea Faka-Tonga)
description: English↔Tongan via Lea Faka-Tonga translation pack.
category: communication
author: maddie
version: 1.0.0
---

# Tongan Translation Skill

Provides English↔Tongan translation using the **lea-faka-tonga** repository's compiled assets — the most comprehensive Tongan language resource on GitHub (updated 2026-08-17).

## What This Gives You

1. **Tier-1 LLM Translation Prompt** (`translate-pack.json`) — A 9-10K token system prompt that translates English→Tongan with:
   - 64 grammar frames (closed set, lint-enforced)
   - Full possessive class table (185 nouns, a-class vs o-class)
   - Negation paradigm (§A — 'ikai with te/ke disambiguation)
   - 5 marker disambiguators (te/ke, na'a/na'e, ka/kae, e/he, aspect)
   - 10 house rules (standing project rulings)
   - 29 verified EN→TO examples from the deep citation-checked method

2. **Token Allow-Set** (`translate-allowset.json`) — 37K folded tokens for output validation (P4 guard against fabricated Tongan)

3. **Full Grammar Engine** (`translate.js`) — Compositional Tongan→English translator (90KB) for reverse direction

## Installation

```bash
# Clone the repo (one-time)
git clone https://github.com/joakimandrew-cloud/lea-faka-tonga.git ~/.hermes/skills/tongan-translation/repo

# Or use the pre-built assets directly from GitHub (no clone needed)
# The skill downloads translate-pack.json and translate-allowset.json on first use
```

## Usage

### As an LLM System Prompt (Recommended for English→Tongan)

```python
# Load the translation pack
with open('repo/lea-faka-tonga-app/src/data/translate-pack.json') as f:
    pack = json.load(f)

system_prompt = pack['system_prompt']
# Use with any LLM: "Translate: I am going to the market"
```

### As a Hermes Skill Tool

```bash
# In Hermes, after skill is loaded:
tongan-translate "I am going to the market"
tongan-translate "Thank you very much" --escalate-on-idiom
```

### Reverse Translation (Tongan→English)

Uses the repo's `translate.js` engine locally via Node:

```bash
tongan-translate-back "'Oku ou 'alu ki he maketi"
```

## Assets

| File | Source | Size | Updated |
|------|--------|------|---------|
| translate-pack.json | GitHub raw | 57KB | Auto-fetched |
| translate-allowset.json | GitHub raw | 37KB | Auto-fetched |
| book-vocabulary.json | GitHub raw | 158KB | On-demand |
| grammar-graph.json | GitHub raw | 259KB | On-demand |

## Translation Quality Notes

- **UNCERTIFIED**: The pack's status is "uncertified — verify before use" until the project's accuracy gate passes
- **Escalation is correct**: If the pack returns `{"escalate": true, "escalate_reason": "..."}`, the sentence needs the deep 6-step method (idioms, >2 clauses, reported speech, counterfactuals, unknown possessed nouns)
- **Frames are closed**: Only the 64 frame tags in the pack are valid; inventing one is a hard error
- **Possessive nouns**: 185 nouns in the index; unknown nouns → escalate

## Commands

| Command | Description |
|---------|-------------|
| `tongan-translate <english>` | Translate English→Tongan using the Tier-1 pack |
| `tongan-translate-back <tongan>` | Translate Tongan→English using the grammar engine |
| `tongan-vocab <tongan>` | Look up a Tongan word in the vocabulary |
| `tongan-validate <tongan>` | Validate a Tongan sentence against the allow-set |
| `tongan-update-assets` | Re-fetch latest assets from GitHub |

## Dependencies

- `node` (for Tongan→English via translate.js)
- `curl` / `fetch` (for asset downloads)
- Python 3 (for the translate CLI wrapper)

## Repository

- **Source**: https://github.com/joakimandrew-cloud/lea-faka-tonga
- **Description**: Interactive course for learning Tongan (Lea Faka-Tonga)
- **Last push**: 2026-08-17
- **Language**: JavaScript (React + Vite)
- **License**: None specified

## ⚠ CRITICAL RELIABILITY LESSON (2026-08-18)

After extensive testing, the following is TRUE:
- The Lea Faka-Tonga **system prompt pack** correctly translates simple course-vocabulary
  sentences but **escalates** on religious/theological terms (shepherd, refuge, mercy,
  covenant, atonement, soul, grace, temple, Messiah, prophecy) and idiomatic prose —
  it only knows its own curriculum vocabulary.
- The **cloud LLM** (nemotron-3-ultra:cloud) produces GOOD simple Tongan but
  **UNRELIABLE, FABRICATED Tongan** for teaching prose: invented words (`Siēpeli`
  for shepherd, `Fēfē` for God), 6+ inconsistent spellings of "Psalms"
  (`Siaeli/Sālama/Sāmoa/Sālimo/Siama/Palamu`), garbled verb forms, and ANSI-garbage
  mixing. Its prose is NOT usable for a Sunday School lesson.
- **Local models** (gemma4:12b-mlx, qwen3.5) fabricate even worse (proven: `'Ekisi`,
  `tangitongi`).

### RELIABLE sources (use these, in order)
1. **Official Church Tongan scriptures** — churchofjesuschrist.org with `?lang=ton`
   (e.g. `/study/scriptures/ot/ps/23?lang=ton`). This is the authoritative source for
   every scripture quotation. Extract text by stripping tags with BeautifulSoup/regex.
2. **A fluent Tongan speaker** — for all teaching prose. Do NOT substitute a model.
3. The Lea Faka-Tonga pack — ONLY for simple course-vocabulary sentences.

### The ONLY correct workflow for a bilingual lesson
1. Keep official Church Tongan scripture quotations (verified from the lang=ton pages).
2. Keep teaching prose in English.
3. Generate a **translation worksheet** (English prose + blank line for Tongan) for a
   fluent speaker to complete.
4. Label any machine translation "UNUSABLE — needs full speaker review", never ship it.
5. NEVER hand-fabricate Tongan from memory (the one unrecoverable error the pack warns
   about) — e.g. "tauhi sipa" for shepherd is WRONG; official is `tauhi` (Ko hoku tauhi
   a Jihova).

### ANChOR VERSES ALREADY VERIFIED (official Church Tongan)
Stored in `references/official-scripture-verses.md`. Includes Ps 2:1,7, 8:1, 19:1,
22:1, 23:1-6, 24:1, 25:1, 27:1, 28:1, 46:1,10.

## Creating a Local Wrapper Script

See `scripts/tongan-translate.py` for a Python CLI that:
1. Loads the system prompt from translate-pack.json
2. Calls the configured LLM (Ollama, Hermes, etc.)
3. Validates output against translate-allowset.json
4. Returns structured JSON: `{tongan, frame, confidence, notes, escalate, escalate_reason}`