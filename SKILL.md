---
name: manual-pdf-reportlab
description: "Generate PDFs from JSON specs via reportlab — zero HTML."
version: 1.0.0
author: Maddie
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pdf, reportlab, document-generation, cli]
    related_skills: [pdf, nano-pdf]
---

# Manual PDF ReportLab Skill

Generate professional PDFs directly from structured JSON specifications using reportlab. No HTML, no WeasyPrint, no Chrome headless — pure Python PDF generation.

## When to Use

- User wants to generate PDFs programmatically from structured data
- Need precise layout control (margins, typography, tables, images)
- Zero external dependencies beyond reportlab + PyMuPDF (for previews)
- Works in headless/CI environments without browser
- Alternative to HTML-to-PDF pipelines (WeasyPrint, Chrome, wkhtmltopdf)

## Prerequisites

```bash
# Core dependencies
pip install reportlab

# Optional: for --preview flag (PNG renders of generated PDF)
pip install pymupdf
```

## CLI Usage

```bash
# Generate PDF from spec
python make_pdf.py spec.json -o output.pdf

# With preview images
python make_pdf.py spec.json -o output.pdf --preview --preview-dir previews/
```

## Spec Format

```json
{
  "mode": "manual",
  "page": "A4",
  "title": "Document title (date range, etc.)",
  "subtitle": "Main heading displayed prominently",
  "palette": {
    "bg": "#FAF8F3",
    "ink": "#1A1A2E",
    "accent": "#1B3A6B",
    "gold": "#B8860B",
    "warm": "#C05A2A",
    "teal": "#0D6E6E",
    "red": "#8B2500",
    "muted": "#6B5B4A"
  },
  "hero_image_path": "/optional/path/to/hero.jpg",
  "sections": [
    {
      "heading": "Section Title",
      "color": "accent",
      "summary": "Brief summary paragraph",
      "body": "Full body text with justification",
      "bullets": [
        "Simple bullet point",
        "Q: Question? | A: Answer | S: Scripture ref | W: Why it matters"
      ],
      "table": {
        "header_color": "gold",
        "header": ["Col 1", "Col 2", "Col 3"],
        "rows": [
          ["cell", "cell", "cell"]
        ]
      }
    }
  ]
}
```

## Spec Fields

| Field | Required | Description |
|-------|----------|-------------|
| `mode` | Yes | `"manual"` (multi-page) or `"poster"` (single landscape) |
| `page` | No | `"A4"`, `"A3"`, `"LETTER"` (default: A4 for manual, A3 for poster) |
| `title` | Yes | Top-line title (date, context) |
| `subtitle` | Yes | Main heading under title |
| `palette` | Yes | Color tokens (hex strings) — see defaults above |
| `hero_image_path` | No | Path to hero image (placed at top of first page) |
| `sections[]` | Yes | Array of section objects |
| `sections[].heading` | Yes | Section title |
| `sections[].color` | No | Palette key for accent color: `accent`, `gold`, `warm`, `teal`, `red`, `muted` |
| `sections[].summary` | No | Intro paragraph (muted style) |
| `sections[].body` | No | Full justified body text |
| `sections[].bullets[]` | No | Bullet points; special format `"Q: ... | A: ... | S: ... | W: ..."` renders as Q&A with scripture + why |
| `sections[].table` | No | Table object with `header`, `rows`, `header_color` |

## Features

- **Typography**: Garamond/Source Sans Pro if available, Times/Helvetica fallback
- **Hero image**: Full-width at top of document (scales to page width)
- **Colored section headers**: Left border + tinted background per section color
- **Q&A bullets**: Parses `Q: | A: | S: | W:` format into styled question/answer/scripture/why blocks
- **Tables**: Auto-column-width for 3/4 column layouts, Paragraph cells for wrapping
- **Footer**: Gold rule + page number + custom text on every page
- **Previews**: `--preview` renders each page to PNG via PyMuPDF

## Architecture

```
manual-pdf-reportlab/
├── SKILL.md
├── scripts/
│   └── make_pdf.py          # Main CLI
├── templates/
│   └── spec-template.json   # Example spec
└── references/
    └── spec-schema.json     # JSON schema for validation
```

## Integration

Import as a module:

```python
from manual_pdf_reportlab.scripts.make_pdf import build_manual

spec = json.load(open("spec.json"))
build_manual(spec, "output.pdf")
```

## Pitfalls

- **Font registration**: System fonts vary; script registers Garamond/SourceSans from macOS paths — on Linux/Windows, add your own font paths
- **Table column widths**: Hardcoded for 3/4 column layouts in `build_manual`; add cases for other column counts
- **Text overflow**: `draw_wrapped` warns but doesn't auto-create new pages in poster mode
- **Image paths**: Must be absolute or relative to working directory
- **Page breaks**: reportlab handles flowable page breaks; tables may split awkwardly — use `KeepTogether` for critical groups

## Verification

```bash
# Basic generation
python scripts/make_pdf.py templates/spec-template.json -o test.pdf

# With preview
python scripts/make_pdf.py templates/spec-template.json -o test.pdf --preview --preview-dir previews/

# Check output
ls -la test.pdf previews/page-*.png
```

## Origin
Extracted from `religious-study/come-follow-me-unified/scripts/make_pdf.py` — generalized for reusable PDF generation from JSON specs.