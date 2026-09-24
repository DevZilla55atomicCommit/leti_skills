---
name: markitdown
description: Convert various file formats (PDF, Excel, PowerPoint, DOCX, images) to Markdown using MarkItDown's AI-native extraction. Use when users need structured text extraction from documents.
---

# MarkItDown Skill: File-to-Markdown Conversion

**AI-Native document converter**. Extracts content from PDFs, spreadsheets, presentations, and Word docs into formatted Markdown with semantic structure.

## Install Binary & Dependencies

```bash
# For Python 3.11+ (macOS/Windows)
python3.11 -m pip install markitdown[all] --user --no-cache-dir

# Or use the bundled CLI if available
curl -fsSL https://github.com/microsoft/markitdown/releases/latest/download/markitdown-macos-arm64 -o ~/bin/markitdown
chmod +x ~/bin/markitdown
```

## Core Commands

### Direct File Conversion (CLI)
```bash
# Convert any document to Markdown
markitdown path-to-file.pdf > output.md
markitdown excel.xlsx --output report.md
markitdown powerpoint.pptx --format markdown --output presentation.mdx
```

### Python API (for embedding in scripts/workflows)
```python
from markitdown import MarkItDown

# Initialize with default settings
md = MarkItDown()

# Convert files and extract structured content
result = md.convert("financial-report.xlsx")
md_result = md.convert("technical-manual.pdf")
ppt_data = md.convert("deck.pptx", format="markdown")

# Access extracted content
print(md_result.text_content)  # Raw text
print(md_result.metadata["author"])  # Author info
print(md_result.entities[0].description)  # Rich text entities (tables, lists, code)
```

## Supported Format Conversions

| Source Format | Tool Usage | Notes |
|----------------|------------|-------|
| **PDF** (.pdf) | `md.convert(file.pdf)` | Extracts text from pages; handles OCR for scanned docs if available |
| **Excel** (.xlsx, .xls) | `md.convert(file.xlsx)` | Returns table data as Markdown tables with headers preserved |
| **PowerPoint** (.pptx) | `md.convert(file.pptx, format="markdown")` | Converts slides to bulleted lists with titles and speaker notes |
| **Word** (.docx) | `md.convert(file.docx)` | Preserves paragraph hierarchy and Markdown-formatted elements |
| **Images** | `md.convert.jpg/png/webp`) | Extracts embedded text, captions, and OCR'd content from images |

## Advanced Options (Python API)

```python
# Specify format-specific settings
pdf_data = md.convert("scan.pdf", settings={"extract_text": True})
table_data = md_result.tables  # Extracted tables as arrays of arrays
headers_only = result["header_rows"]  # Column headers only

# Handle large documents efficiently
large_doc = md.convert_file_stream(data, format="markdown")
```

## Integration Strategy

**MarkItDown is designed for RAG pipelines, document ingestion, and automated summarization workflows.**

### Use Cases:

1. **Document Ingestion Pipelines**: Convert incoming files from various Office formats into a consistent Markdown representation for indexing.

2. **Structured Data Extraction**: Pull tabular data from Excel/PowerPoint presentations programmatically—useful for financial model processing when building RAG context.

3. **Text-based Analysis**: Extract plain-text content from PDF technical manuals or scanned documents where formatting analysis is critical.

4. **Automated Summarization**: Use extracted entity descriptions to build summaries of complex presentations without full slide enumeration.

## MCP & Agent Integration

MarkItDown integrates with Hermes' skill system for automated document processing in conversational AI agents. The tool supports:

- Automatic format inference from file extensions
- Default fallback strategies (e.g., `pdf` defaults to text extraction)
- JSON output mode for structured agent workflows

### Typical Agent Workflow Pattern:

```python
from markitdown import MarkItDown

md = MarkItDown()
content = md.convert("meeting-notes.pdf")

# Return structured response to user
print(f"""{content}
**Key insights:** {content.summary()}
""")
```

## Performance Notes

- **PDFs with scanned pages**: May require OCR integration—check `magika` dependency for this capability.
- **Large files (>100 MB)**: Consider streaming mode or batch conversion to avoid memory overhead.

---

*Skill Version: 1.0 | Created for macOS Python 3.11+ environments*