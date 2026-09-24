#!/usr/bin/env python3
"""Strip ANSI escape sequences from the model draft and add a clear 'unusable' warning."""
import re
from pathlib import Path

path = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan_DRAFT.md")

content = path.read_text(encoding="utf-8")

# Remove ANSI escape sequences
ansi = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|\x1b\][^\x1b]*\x1b\\')
cleaned = ansi.sub('', content)

# Remove duplicated text artifacts (e.g. "fusia[5D[K\nfusia" -> "fusia")
# Collapse doubled words split across lines that were ANSI redraws
cleaned = re.sub(r'([A-Za-zāēīōūāēīōūʻ])\1{1,}(?=[\s,.;"])', r'\1', cleaned)  # avoid over-collapsing

# Replace the header to clearly warn
header = """# Psalms Lesson — Tongan Translation DRAFT (UNUSABLE — do NOT use)

**Status: NOT FIT FOR USE.** This file was machine-translated by a cloud LLM
and CONTAINS FABRICATED and inconsistent Tongan (six+ spellings of "Psalms",
invented words for "shepherd"/"God", garbled verb forms, ANSI-garbage mixing).
It is preserved only as a rough reference of which words the model attempted.

⚠ = doctrinal term present; model output for it is NOT trustworthy.

**Use INSTEAD:**
1. `Psalms_Lesson_Tongan.html` — bilingual: official Church Tongan scripture + English prose (reliable)
2. `Psalms_Lesson_Tongan_Translation_Worksheet.md` — 76 clean blanks for a fluent Tongan speaker to fill (reliable path)

Every scripture quotation should use the OFFICIAL rendering in the HTML,
NOT anything in this file.
"""
cleaned = header + cleaned.split('---\n', 1)[1] if '---\n' in cleaned else header + "\n" + cleaned

path.write_text(cleaned, encoding="utf-8")
print(f"Cleaned ANSI from draft. Final size: {path.stat().st_size} bytes")
print("Draft clearly labeled UNUSABLE — preserved as rough reference only.")