#!/usr/bin/env python3
"""
Extract all English prose blocks from the dual-language lesson into a
translation worksheet. Each entry: section, English text, blank line for
Tongan. Scripture quotes already have official Tongan in the HTML.
"""
from pathlib import Path
import re
from bs4 import BeautifulSoup

path = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan.html")
out = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan_Translation_Worksheet.md")

html = path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

lines = []
lines.append("# Psalms Lesson — Tongan Translation Worksheet")
lines.append("")
lines.append(f"Source: {path.name}")
lines.append("")
lines.append("Every scripture quotation already has its OFFICIAL Church Tongan in the HTML.")
lines.append("Below are the English teaching-prose blocks that still need Tongan.")
lines.append("Add the correct Tongan in each blank line. Use official Church Tongan orthography.")
lines.append("")
lines.append("---")
lines.append("")

def add_block(label, text, idx):
    text = text.strip()
    if not text or len(text) < 3:
        return
    # Skip pure scripture refs
    if re.match(r'^[\d\s;–:.-]+$', text):
        return
    lines.append(f"## {label} {idx}")
    lines.append("")
    lines.append(f"**English:** {text}")
    lines.append("")
    lines.append("**Tongan:**")
    lines.append("")
    lines.append("_____")
    lines.append("")

# Walk through in document order
count = 0
for elem in soup.find_all(True):
    if elem.name in ("h1", "h2", "h3", "h4"):
        txt = elem.get_text(strip=True)
        # skip ones that contain scripture class marker
        if txt and len(txt) > 2:
            count += 1
            add_block("Heading", txt, count)
    elif elem.name == "div" and "question-text" in (elem.get("class") or []):
        txt = elem.get_text(strip=True)
        if txt:
            count += 1
            add_block("Question", txt, count)
    elif elem.name == "div" and "answer-text" in (elem.get("class") or []):
        txt = elem.get_text(strip=True)
        if txt and len(txt) > 4:
            count += 1
            add_block("Answer", txt, count)
    elif elem.name == "div" and "key-point" in (elem.get("class") or []):
        txt = elem.get_text(strip=True)
        if txt and len(txt) > 4:
            count += 1
            add_block("Key Point", txt, count)
    elif elem.name == "div" and "cheat-question" in (elem.get("class") or []):
        txt = elem.get_text(strip=True)
        if txt:
            count += 1
            add_block("Cheat Q", txt, count)
    elif elem.name == "div" and "cheat-answer" in (elem.get("class") or []):
        txt = elem.get_text(strip=True)
        if txt and len(txt) > 4:
            count += 1
            add_block("Cheat A", txt, count)

out.write_text("\n".join(lines), encoding="utf-8")
print(f"Extracted {count} prose blocks → {out.name}")