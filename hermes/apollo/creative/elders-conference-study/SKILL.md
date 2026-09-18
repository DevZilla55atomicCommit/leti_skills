---
name: elders-conference-study
version: 1.0.0
description: Build Elders Quorum PDF guides from Conference talks.
category: creative
tags:
- elders-quorum
- general-conference
- pdf-generation
- study-guide
---

# Elders Conference Study Pipeline

**Class-level skill** for turning any General Conference talk into a PDF-only Elders Quorum study guide: fetch talk, pull scriptures + Handbook, build lesson, render professional PDF.

## When to Use

- Elders Quorum lesson prep from a `@url:` conference talk link
- Building 45-minute lesson PDFs with summary, doctrines, Q&A
- Regenerating or restyling an existing Stevenson-style guide

## Pipeline Overview

```
FETCH TALK → PULL SCRIPTURES/HANDBOOK → BUILD LESSON HTML → WEASYPRINT PDF → VERIFY → OUTPUT
```

### Step 1: Fetch talk

- `web_extract` the `churchofjesuschrist.org/study/general-conference/YYYY/MM/NNname?lang=eng` URL (char_limit 25000).
- Keep: title, speaker, session, opening story/analogy, 2-4 core charges, closing testimony, all inline scripture links, all `churchofjesuschrist.org/imgs/...` image URLs.
- Download talk images at hi-res (`!1000` width param, not `!500`) and the speaker portrait at `!1200` into the /tmp build dir (never the destination). Verify distinct MD5s — identical hashes mean a placeholder banner drifted in; always prefer talk-body `imgs/` URLs. NOTE: hi-res variants can differ in aspect from thumbnails (e.g. a square `!500` collage served landscape at `!1000`) — never assume aspect; aspect-match after render.

### Step 2: Pull supporting knowledge (Gospel Library)

- `web_extract` every scripture + Handbook URL cited in the talk (D&C, Book of Mormon, NT, General Handbook chapter).
- Add 2-4 cross-links that abide with the talk theme (e.g. ministering: Handbook 21.1 four duties, Mosiah 23:18, James 1:27, Luke 10:1-17; youth: 2 Ne 25:26, D&C 46:7, Uchtdorf/Nelson counsel as cited).
- Every doctrinal claim in the guide must trace to one fetched source. List all sources in the PDF footer; mark the guide as a study aid, not an official publication.

### Step 3: Build lesson HTML

Required sections in order:
1. Cover bar (title, speaker, session, `Elders Quorum Study Guide - PDF-Only - 45-minute lesson`) + source URL line.
2. One-page summary + key box (story, pivot, charges, closing line).
3. Key doctrines table (Doctrine | One-line truth | Anchor scripture, 4-6 rows).
4. One section per charge with inline image + verse callout + `New knowledge` box tying in Handbook/scripture cross-links plus one concrete quorum action.
5. Three real-world Q&A cards, each with SCRIPTURE answer + PROPHETS answer.
6. 45-minute lesson plan cards (0-8 / 8-20 / 20-32 / 32-42 / close). No commitments/notes section — user removed it.
7. Compact sources footer (navy band, 7.5pt). Keep all navy blocks slim: cover padding 12px, section bars 11pt/4px padding, footer 6px — never large background slabs.

### Step 4: Render PDF (WeasyPrint CLI)

- Design is colorful + professional: navy cover bar with the speaker's official portrait (gold-bordered, from `churchofjesuschrist.org/imgs/...` at !1200 res) beside the title; navy section bars with gold number chips; tinted callout boxes (gold/blue/green); color-coded Q&A cards (blue/green/purple left borders + matching tags). All body text left-aligned; headings Georgia serif, body Helvetica/Arial.
- WeasyPrint rules (blank-page pitfalls): solid colors only, never `linear-gradient()` on body/large containers; never Grid or Flex for multi-page card layouts — use `display: block` wrapper + `display: inline-block; width: 47%` cards with `break-inside: avoid` on cards only; no `page-break-after: always` on the first element.
- `@page { size: Letter; margin: 0.6in 0.6in 0.75in 0.6in; @bottom-center { page numbers } }`; serif headings (Georgia), sans body (Helvetica/Arial).
- Render with the CLI (works without DYLD hacks): `/opt/homebrew/bin/weasyprint guide.html guide.pdf`.

### Step 5: Verify + output

- Verify with a venv (system python is PEP-668 managed): `python3 -m venv /tmp/pdfcheck; /tmp/pdfcheck/bin/pip install -q pypdf pymupdf`, then (a) per-page char counts — every page must exceed ~500 chars or the layout shipped a blank; (b) fitz `get_image_rects` per page — each rendered rect's aspect must match its source file's aspect (mismatch = cropping bug) and sizes should stay modest (hero ~160x120pt, inline ~160-190x~110pt, portrait ~95x115pt).
- Display images at restrained caps so they never dominate: portrait 20% cover column, hero 70% width / 170px max-height, inline 60% / 150px centered, wide collages at 52% width. Always `object-fit: contain` + `height: auto` (never `cover` with fixed height — that slices heads off).
- Output is PDF-ONLY in the destination root. Final organized path: `'/Users/alfredkamisese/Desktop/Elders Quorum Lessons 2025.2026'/YYYY/MonthTaught/YYYY-MM_NNspeaker_Topic/` containing exactly ONE file: `YYYY-MM_NNspeaker_Study-Guide.pdf`. Build the HTML + download JPGs in /tmp (never in the destination), render, verify, then delete intermediates. Never leave .html/.jpg/.json/.md in the destination.
- Deliver with `MEDIA:/absolute/path/to.pdf` plus `desktop_preview` open on the PDF so the user can review it in the preview pane.

## Pitfalls & Lessons

1. Talk pages omit the author in text extraction — derive speaker from the URL slug plus in-talk self-reference, and confirm before printing the cover.
2. Placeholder hero drift: byte-identical downloads across weeks/talks mean a generic banner was grabbed; always prefer talk-body `imgs/` URLs.
3. Flex/Grid containers do not fragment in WeasyPrint — they push cards onto one page and leave blanks; use block + inline-block cards.
4. System python cannot `pip install` (externally managed) and has no `fitz`/`pypdf`/`pdfinfo` — verify page counts from a `/tmp` venv with pypdf.
5. PDF-only is mandatory — destination holds just the final .pdf. HTML/JPGs live in /tmp during the build and are deleted after verification.

6. Rendered image rects are ground truth — trust fitz measurements over vision-model impressions of cropping/size (models hallucinate grids and mistake tight source framing for cropping). Confirm aspect-match, then eyeball-verify one rendered page PNG via `vision_analyze` before delivery.

## Commands Quick Reference

```bash
# Download talk images
curl -sL -o hero.jpg '<imgs-url>'; md5 *.jpg

# Render
/opt/homebrew/bin/weasyprint Guide.html Guide.pdf

# Verify (no blanks)
python3 -m venv /tmp/pdfcheck 2>/dev/null; /tmp/pdfcheck/bin/pip install -q pypdf
/tmp/pdfcheck/bin/python -c "from pypdf import PdfReader; r=PdfReader('Guide.pdf'); print(len(r.pages)); [print(len(p.extract_text() or '')) for p in r.pages]"
```

## References

- Proven build: `~/Desktop/Elders Quorum Lessons 2025.2026/2026/September/2026-09_23stevenson_Lost-Luggage-Redeemed-Souls/2026-09_23stevenson_Study-Guide.pdf` (4 pp, Sept 2026; intermediates were /tmp-only, destination holds just the PDF).
