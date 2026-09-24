# WeasyPrint PDF Render (house renderer)

Preferred over Chrome headless for weekly guides: precise page control,
reliable `break-inside: avoid`, TOC/bookmarks/metadata, no GUI needed.

## Run

```bash
~/.hermes/scripts/generate_cfm_pdf.sh --auto          # cron path (current week)
~/.hermes/scripts/generate_cfm_pdf.sh --week 2026-38  # pinned week
```

The wrapper sets `DYLD_LIBRARY_PATH` for Homebrew's pango/cairo/gdk-pixbuf
and calls `cfm_pdf_generator.py`, which holds the print CSS (`PAGE_CSS`)
and all per-week content branches. `brew install pango cairo gdk-pixbuf libffi`
provides the system libraries; never `pip install` into system Homebrew python
(PEP 668) — use a throwaway venv for probe packages.

## CSS constraints (WeasyPrint fragments poorly otherwise)

- Multi-page card layouts: `display: block` wrapper +
  `display: inline-block` cards. Never Grid or Flex — unbreakable containers
  get pushed whole onto one page, leaving blank pages behind (exit code
  stays 0, so the build looks successful).
- Keep `break-inside: avoid` on cards only, never on the container.
- No `page-break-after: always` on the cover; no `linear-gradient()` on
  body or large containers (both trigger `assert not page_is_empty`).
  Gradients are safe only on small badges/accent bars; use solid colors elsewhere.

## Verify every build (exit 0 means rendered, not correct)

```bash
python3 -m venv /tmp/pdfcheck --system-site-packages
/tmp/pdfcheck/bin/pip install -q pypdf
/tmp/pdfcheck/bin/python -c "from pypdf import PdfReader; r=PdfReader('<Guide>.pdf'); print('pages:', len(r.pages)); [print(f'p{i+1}: chars={len(p.extract_text() or \"\")}') for i,p in enumerate(r.pages)]"
```

- Exclude page 1: the image cover legitimately extracts to ~65–115 chars.
- Any other page near ~100 chars (headers/footers only) is blank — fix the
  layout, never ship it.
- After a week-mapping correction, grep the extracted text for the OLD
  scripture range (must be empty) and the new one (must be present).
