---
name: conference-study-guide-pipeline
version: 1.0.0
description: Build Elders Quorum study PDFs from conference talks.
category: creative
tags:
- religious-study
- pdf-generation
- elders-quorum
- general-conference
---

# Conference Study Guide Pipeline

**Class-level skill** for building Elders Quorum study guides from a single General Conference talk URL as PDF-only output. Distinct from `cfm-study-guide-pipeline`, which covers weekly Come Follow Me manual lessons — this skill covers one talk → one lesson PDF.

## When to Use

- User drops a `churchofjesuschrist.org/study/general-conference/...` talk URL and asks for an Elders Quorum lesson guide
- PDF-only study guide from any conference talk (summary, doctrines, Q&A, lesson plan)
- Route here, never to the CFM scraper pipeline, whenever the source is a talk URL rather than a CFM manual unit

## Procedure

### 1. Fetch the talk

Extract the talk page with a high char budget so the full discourse is captured:

- `web_extract` the talk URL (`char_limit` 25000), collecting title, speaker, all body paragraphs, inline image URLs, and every linked scripture/Handbook URL.
- Record talk title, speaker, session, and the 2–4 anchor stories or metaphors — these drive the cover and summary.

### 2. Fetch cross-linked doctrine

Extract each scripture and Handbook section the talk cites (D&C, Book of Mormon, New Testament, General Handbook ministering chapters):

- `web_extract` 2–4 cited URLs at `char_limit` 8000 to capture exact verses and Handbook duty lists.
- Keep verse text verbatim for callout boxes; never paraphrase scripture in quote blocks.

### 3. Download talk images and reject placeholders

Download 2–3 inline images from the talk page into the lesson folder with curl, then compare MD5s — placeholder banners are byte-identical across talks, so distinct hashes prove real artwork.

```bash
mkdir -p ~/Desktop/'Elders Quorum Lessons 2025.2026'/2026/<MM-Speaker>/
cd ~/Desktop/'Elders Quorum Lessons 2025.2026'/2026/<MM-Speaker>/
curl -sL -o hero.jpg '<first-talk-image-url>'
curl -sL -o second.jpg '<second-talk-image-url>'
md5 hero.jpg second.jpg
```

**Pitfall**: Ship only images with distinct MD5s and talk-specific captions — reuse of one banner image across lessons means the extractor drifted to a site-wide placeholder, so re-pick from the talk's inline `<img>` set.

### 4. Build print-safe HTML (WeasyPrint-safe CSS)

Write one self-contained HTML file (embedded CSS, local relative image paths) with this section order:

1. Cover bar (title, speaker, session, "Elders Quorum Study Guide • PDF-Only • 45-minute lesson") + hero image
2. One-page summary + key-doctrine table (doctrine | one-line truth | anchor scripture)
3. One section per major charge in the talk (2 typical), each with image, Handbook/scholar cross-link box, verse callout
4. Three real-world Q&A blocks, each with SCRIPTURE answer + PROPHETS/TEACHINGS answer
5. 45-minute lesson plan cards (0–8 / 8–20 / 20–32 / 32–42 / close) + commitments table + notes box
6. Sources footer (talk, scriptures, Handbook, image credits, "study aid only" disclaimer)

**Pitfall**: Never use CSS Grid or Flexbox for multi-page card layouts — WeasyPrint treats flex containers as monolithic and pushes all cards onto one page, leaving fully blank pages behind. Use `display: block` wrappers with `display: inline-block; width: 47%` cards and keep `break-inside: avoid` on cards only.

**Pitfall**: Never put `page-break-after: always` on the cover or `linear-gradient()` on body/large containers — both trigger WeasyPrint `assert not page_is_empty` failures. Use solid background colors, with gradients only on small badges or accent bars.

### 5. Render PDF via WeasyPrint CLI

Use the Homebrew WeasyPrint binary directly (it carries its own runtime; no DYLD wrapper needed for CLI use):

```bash
/opt/homebrew/bin/weasyprint <Guide>.html <Guide>.pdf
```

**User preference**: PDF-only output. Ship the PDF as the deliverable; keep the HTML and JPGs in the lesson folder as source, never as the deliverable.

### 6. Verify no blank pages before shipping

System Homebrew python is externally managed (PEP 668), so do not `pip install` into it — spin a throwaway venv for the `pypdf` probe, then dump per-page character counts. Any page near ~100 chars (headers/footers only) is blank and must be fixed in layout, not shipped.

```bash
python3 -m venv /tmp/pdfcheck --system-site-packages
/tmp/pdfcheck/bin/pip install -q pypdf
/tmp/pdfcheck/bin/python -c "from pypdf import PdfReader; r=PdfReader('<Guide>.pdf'); print('pages:', len(r.pages)); [print(f'p{i+1}: chars={len(p.extract_text() or \"\")}') for i,p in enumerate(r.pages)]"
```

**Pitfall**: Treat a successful `weasyprint` exit code as render-complete only, never as quality-verified — always run the per-page char-count probe, since blank-page failures from unbreakable containers exit 0.

## Output Locations

| Artifact | Directory | Naming |
|----------|-----------|--------|
| PDF (deliverable) | `~/Desktop/Elders Quorum Lessons 2025.2026/2026/<MM-Speaker>/` | `<Speaker>_<Topic>_Study_Guide.pdf` |
| HTML + JPGs (source) | Same folder | Same basename `.html`, descriptive `.jpg` names |

## References

- `cfm-study-guide-pipeline` — the Come Follow Me weekly pipeline; consult for WeasyPrint macOS setup and scraper patterns, but never run it for talk-URL lessons.
