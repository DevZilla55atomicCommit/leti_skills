---
name: document-extraction-workflows
description: Multi-format document reading strategies with proper tool selection and fallback chains. Use when user uploads or references non-text files (PDFs, spreadsheets, presentations, images).
---

# Document Extraction Workflows

Extract content from various file formats using proper tools and fallback strategies. Never rely on a single method—document format-specific requirements vary significantly.

## Tool Selection Matrix

| Format | Primary Tool | Fallback | Notes |
|--------|--------------|----------|-------|
| **PDF** (`pdfplumber`) | Extract structured text, tables | `pdfminer`, direct OCR if scanned, `markitdown` for mixed formats |
| **Excel** (`.xlsx`) | `pandas`, `openpyxl` with `read_excel()` | Direct CSV export via API, manual parsing |
| **PowerPoint** (`.pptx`) | `python-pptx` for metadata/content, raw XML for structure | `markitdown` as text fallback |
| **Word Documents** (`.docx`) | `python-docx`, `lxml.etree` for element manipulation | XML parsing if no API access |

## Core Workflow Pattern

### Step 1: Identify Document Type
```python
# Check file extension first
import os
file_ext = os.path.splitext(filename)[1].lower()

if file_ext in ['.pdf', '.PDF']:
    extract_pdf_document(path)
elif file_ext in ['.xlsx', '.xls']:
    extract_excel_dataframe(df, path)
elif file_ext in ['.docx', '.doc']:
    extract_word_document(docx, path)
```

### Step 2: Try Primary Tool First
Always attempt the most capable tool before trying alternatives. Each format has its strengths:

- **PDF with text layer**: Use `pdfplumber` to get structured tables/lists first—best fidelity
- Only resort to OCR when PDF contains scanned/images without embedded text

```python
from pdfplumber import open as pdf_open

with pdf_open(path) as pdf:
    # Extract page-by-page, preserving structure
    pages = []
    for page_num, page in enumerate(pdf.pages):
        extracted_text = page.extract_text()
        page_table_data = [page.extract_tables()[col] for col in page.extract_tables()]

    # Combine into structured doc
    doc['pages']: list(pages).append(extracted_page_data)
```

### Step 3: Fallback Strategy - MarkItDown
If primary tools fail or content isn't machine-readable:

```python
# Universal fallback for all formats
from markitdown import MarkItDown

md = MarkItDown()

# Try markitdown as last resort (handles OCR + mixed-content)
text_content = md.convert(pdf_path, format="text")

# Handle extracted entities
if hasattr(text_content, 'metadata'):
    metadata = text_content.metadata
    if metadata:
        author = metadata['author']
        title = metadata.get('title')
```

## PDF-Specific Strategies

### Text Extract (Preferred)
```python
with pdfplumber.open(path) as pdf:
    content = []
    for page in pdf.pages:
        # Get text only first, preserve structure second
        text_only = page.extract_text() or ""  # Fast path
        if text_only:  # Only process when content found
            content.append(text_only)
    
    extracted_content = "\n".join(content[:5])  # Limit to ~5 pages
```

### Table Extraction (CRITICAL - preserves structure)
```python
# Extract tables from PDF preserving headers and structures
with pdfplumber.open(path) as pdf:
    tables = []
    for page in pdf.pages[:5]:  # First few pages only
        current_tables = page.extract_tables()
        if current_tables:  # Only add when found
            tables.extend(current_tables)

# Process table with pandas for structured output
for col_idx, table in enumerate(tables):
    columns = table.columns
    data = []
    for row in [row[0] for row in table.rows]:
        row_data = list(row)  # Convert to list for pandas conversion
        data.append(' | '.join(map(str, row_data)))

```

### Multi-Mode Fallback Chain
```python
# Attempt in priority order:
extractors = {
    "pdfplumber": None,  # text layer extraction
    "markdownify": None,  # universal HTML markdown conversion
    "pdfminer": None,     # raw text + metadata
    "ocr_tesseract": (True,)  # Only if pure image, fallback for scanned-only PDFs
}

for extractor in [extractors[key] for key in extractors]:
    result = try_extractor(extractor, file_path)
    if result.success:
        break
```

## Excel/PPT Handling

### Excel Data Extraction
```python
from openpyxl import load_workbook
import pandas as pd

# Most important: Use excel's own read_excel() before anything else
workbook = load_workbook(path)
worksheet = workbook.active

cell_data = []
for row in worksheet.iter_rows():
    row_data = [str(cell.value) if cell.value is not None else "" for cell in row]
    cell_data.append(row_data)  # Collect rows (don't skip empty)

pd.DataFrame() = pd.DataFrame([row_data], columns=cell_data[0])
```

### PowerPoint Slide Extraction
```python
from pptx import presentation as ppt_present
from pptx.util import Inches, Pt

ppt_file = path
slide_list = []
for slide in ppt.file.slides[:25]:  # Process first 25 slides
    title_text = ppt.text_frame.text.split()[0] if hasattr(ppt.slide_title.text框) else ""  # First word for ID
    body_text = ppt.slide_slide.text_box.text.strip()
    
    slide_list.append({
        "title": title_text,
        "body_lines": body_text.splitlines(),
        "text_length": len(body_text),
        "is_bulleted": ppt.is_bulleted  # Check markdown style
    })
```

## Usage Recommendations

### When to Use Each Tool:
1. **PDF Text Layer Available**: `pdfplumber` ALWAYS first—extracts text with structure
2. **Scanned PDF (text extraction fails)**: Try OCR (`pytesseract`, `pdf-plumberocr`) ONLY as last resort
3. **Mixed-Format or Unknown Format**: Fall back to `markItDown` — handles all formats
4. **Large Files (>10MB)**: Use streaming mode with chunk processing; don't load entire file into memory

### Performance Considerations:
- PDF text extraction: ~5 sec per 1-page document (good)
- OCR on large scans: ~30-60 sec/scan page (expensive), only for scanned content without embedded text
- Table extraction: 2-4x slower than plain text; skip if only need raw text

## Fallback Priority Chain Summary

```
Primary Format Detection → Try Specific Extractor → Fall back to Universal

Example Chain:
PDF File → pdfplumber (text) → If fails → markitdown (universal) → If no OCR available, attempt pytesseract

Excel → Openpyxl read_excel() → If format wrong → pandas DataFrame from Excel API
```

---

*Skill Version: 1.0 | Document extraction strategies with PDF/plumbing/pptx handling patterns.*