#!/usr/bin/env python3
"""make_pdf.py — render a content spec (JSON) to PDF with reportlab. No HTML.

Modes:
  poster  single landscape page, headline + column blocks
  manual  multi-page A4 document, sections with body/bullets/tables

Usage:
  python3 make_pdf.py spec.json -o out.pdf [--preview] [--preview-dir previews]

The --preview flag renders PNGs of the result via PyMuPDF for visual review.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A3, A4, LETTER, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

PAGE_SIZES = {"A3": A3, "A4": A4, "LETTER": LETTER}
WARNINGS = []
SKILL_DIR = Path(__file__).parent.parent

# Register better fonts if available
try:
    pdfmetrics.registerFont(TTFont('Garamond', '/System/Library/Fonts/Garamond.ttc'))
    pdfmetrics.registerFont(TTFont('Garamond-Bold', '/System/Library/Fonts/Garamond Bold.ttc'))
    pdfmetrics.registerFont(TTFont('SourceSans', '/System/Library/Fonts/SourceSansPro-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSans-Bold', '/System/Library/Fonts/SourceSansPro-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('SourceSans-Italic', '/System/Library/Fonts/SourceSansPro-Italic.ttf'))
    HAS_GARAMOND = True
except:
    HAS_GARAMOND = False

# Font fallbacks
FONT_SERIF = 'Garamond' if HAS_GARAMOND else 'Times-Roman'
FONT_SERIF_BOLD = 'Garamond-Bold' if HAS_GARAMOND else 'Times-Bold'
FONT_SERIF_ITALIC = 'Garamond' if HAS_GARAMOND else 'Times-Italic'
FONT_SANS = 'SourceSans' if HAS_GARAMOND else 'Helvetica'
FONT_SANS_BOLD = 'SourceSans-Bold' if HAS_GARAMOND else 'Helvetica-Bold'
FONT_SANS_ITALIC = 'SourceSans-Italic' if HAS_GARAMOND else 'Helvetica-Oblique'

def warn(msg):
    WARNINGS.append(msg)
    print(f"WARNING: {msg}", file=sys.stderr)

def build_poster(spec, path):
    pal = {k: HexColor(v) for k, v in spec["palette"].items()}
    W, H = landscape(PAGE_SIZES.get(spec.get("page", "A3"), A3))
    m = 48
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setFillColor(pal["bg"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    y = H - m - 20
    y = draw_wrapped(c, spec["title"], m, y, W - 2 * m,
                     FONT_SANS_BOLD, 96, pal["ink"], leading=104)
    y -= 12
    if spec.get("subtitle"):
        y = draw_wrapped(c, spec["subtitle"], m, y, W - 2 * m,
                         FONT_SANS, 34, pal["muted"], leading=42)
    y -= 30

    c.setStrokeColor(pal["accent"])
    c.setLineWidth(6)
    c.line(m, y, W - m, y)
    y -= 44

    blocks = spec.get("blocks", [])
    cols = min(max(len(blocks), 1), 3)
    gutter = 56
    col_w = (W - 2 * m - (cols - 1) * gutter) / cols

    for i, b in enumerate(blocks):
        col = i % cols
        row = i // cols
        x = m + col * (col_w + gutter)
        by = y - row * (H * 0.32)
        by = draw_wrapped(c, b["heading"], x, by, col_w,
                          FONT_SANS_BOLD, 34, pal["accent"], leading=40)
        by -= 14
        for bullet in b.get("bullets", []):
            by = draw_wrapped(c, "\u2022  " + bullet, x + 10, by, col_w - 10,
                              FONT_SANS, 24, pal["ink"], leading=32)
            by -= 10
        by -= 26

    c.showPage()
    c.save()


def wrap(text, font, size, max_w):
    """Greedy word-wrap using real font metrics."""
    words, lines, line = text.split(), [], ""
    for w in words:
        t = (line + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            line = t
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, max_w, font, size, color, leading=None):
    """Draw wrapped text downward from (x, y). Returns new y."""
    leading = leading or size * 1.25
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, max_w):
        if y < 0:
            warn(f"text overflow at '{text[:40]}...'")
            return y
        c.drawString(x, y, line)
        y -= leading
    return y


def build_manual(spec, path):
    pal = {k: HexColor(v) for k, v in spec["palette"].items()}
    page_size = PAGE_SIZES.get(spec.get("page", "A4"), A4)

    # Custom doc template with footer on every page
    class CFMDocTemplate(SimpleDocTemplate):
        def __init__(self, *args, **kwargs):
            self.footer_text = kwargs.pop('footer_text', '')
            self.footer_color = kwargs.pop('footer_color', HexColor("#B8860B"))
            super().__init__(*args, **kwargs)

        def afterFlowable(self, flowable):
            pass

        def build(self, story, onFirstPage=None, onLaterPages=None):
            def add_page_number(canvas, doc):
                canvas.saveState()
                canvas.setFont(FONT_SANS_BOLD, 9)
                canvas.setFillColor(self.footer_color)
                # Gold rule
                canvas.setStrokeColor(self.footer_color)
                canvas.setLineWidth(0.8)
                canvas.line(18*mm, 16*mm, doc.pagesize[0] - 18*mm, 16*mm)
                # Footer text + page number combined
                footer_with_page = f"{self.footer_text}  |  Page {doc.page}"
                canvas.drawCentredString(
                    doc.pagesize[0] / 2, 10*mm,
                    footer_with_page
                )
                canvas.restoreState()

            super().build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

    doc = CFMDocTemplate(
        path, pagesize=page_size,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=22*mm,  # Extra space for footer
        footer_text="Come Follow Me Unified  •  churchofjesuschrist.org  •  Gospel Library  •  BYU Studies  •  followHIM",
        footer_color=HexColor("#B8860B")
    )

    bg = pal["bg"]
    ink = pal["ink"]
    accent = pal["accent"]
    gold = pal.get("gold", accent)
    warm = pal.get("warm", accent)
    teal = pal.get("teal", accent)
    red = pal.get("red", accent)
    muted = pal.get("muted", ink)

    # Styles - Serif for headings, Sans for body
    s_title = ParagraphStyle("title", fontName=FONT_SERIF_BOLD, fontSize=28,
                             textColor=accent, spaceAfter=4, alignment=TA_LEFT, leading=34)
    s_sub = ParagraphStyle("sub", fontName=FONT_SERIF, fontSize=14,
                           textColor=muted, spaceAfter=16, alignment=TA_LEFT, leading=18)
    s_h1 = ParagraphStyle("h1", fontName=FONT_SERIF_BOLD, fontSize=16,
                          textColor=accent, spaceBefore=18, spaceAfter=6,
                          borderWidth=0, borderPadding=0, leading=20)
    s_h1_num = ParagraphStyle("h1_num", parent=s_h1, fontSize=15,
                              textColor=accent, spaceBefore=14, spaceAfter=4)
    s_sum = ParagraphStyle("sum", fontName=FONT_SERIF, fontSize=11,
                           textColor=muted, spaceAfter=8, leading=16,
                           alignment=TA_JUSTIFY)
    s_body = ParagraphStyle("body", fontName=FONT_SERIF, fontSize=11,
                            textColor=ink, leading=16, spaceAfter=6,
                            alignment=TA_JUSTIFY)
    s_bul = ParagraphStyle("bul", parent=s_body, leftIndent=18,
                           bulletIndent=6, spaceAfter=3)
    s_bul2 = ParagraphStyle("bul2", parent=s_body, leftIndent=36,
                            bulletIndent=12, spaceAfter=2, fontSize=10)
    s_scripture = ParagraphStyle("scripture", fontName=FONT_SANS, fontSize=9.5,
                                 textColor=gold, leading=13, spaceAfter=2,
                                 leftIndent=18, bulletIndent=6)
    s_why_label = ParagraphStyle("why_label", fontName=FONT_SANS_BOLD, fontSize=7.5,
                                 textColor=warm, spaceAfter=1, leftIndent=36)
    s_why_text = ParagraphStyle("why_text", parent=s_body, fontSize=9.5,
                                textColor=ink, leading=13, spaceAfter=4,
                                leftIndent=36)
    s_cheat_num = ParagraphStyle("cheat_num", fontName=FONT_SERIF_BOLD, fontSize=10,
                                 textColor=gold, spaceAfter=1)
    s_cheat_text = ParagraphStyle("cheat_text", fontName=FONT_SERIF, fontSize=9.5,
                                  textColor=ink, leading=13, spaceAfter=3,
                                  leftIndent=18)
    s_footer = ParagraphStyle("footer", fontName=FONT_SANS, fontSize=8,
                              textColor=muted, alignment=TA_CENTER, spaceBefore=12)

    # Table style
    def make_table_style(header_color):
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), header_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), bg),
            ("FONTNAME", (0, 0), (-1, 0), FONT_SANS_BOLD),
            ("FONTNAME", (0, 1), (-1, -1), FONT_SANS),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, muted),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [bg, HexColor("#ffffff")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("MINROWHEIGHT", (0, 0), (-1, -1), 60),
        ])

    story = []

    # ===== HERO SECTION WITH IMAGE =====
    # Hero image at top - use spec-provided path or fallback to assets folder
    hero_image_path = spec.get("hero_image_path")
    if hero_image_path and Path(hero_image_path).exists():
        from reportlab.platypus import Image
        hero_img = Image(str(hero_image_path))
        # Scale to full page width (A4 = 595pt, margins 18mm each side = ~595-51 = 544pt usable)
        hero_img.drawWidth = 544
        hero_img.drawHeight = 280  # Fixed height for hero
        story.append(hero_img)
    else:
        # Fallback to assets folder
        fallback_path = SKILL_DIR / "assets" / "hero_image.jpg"
        if fallback_path.exists():
            from reportlab.platypus import Image
            hero_img = Image(str(fallback_path))
            hero_img.drawWidth = 544
            hero_img.drawHeight = 280
            story.append(hero_img)
        else:
            story.append(Spacer(1, 20))  # Fallback space
    
    # Hero image alt text for accessibility (not rendered but stored for reference)
    hero_alt = spec.get("hero_image_alt", "Lesson artwork")

    # ===== HERO AREA =====
    # Title should be the official lesson title (subtitle in spec)
    hero_title_style = ParagraphStyle("hero_title", parent=s_title,
        fontSize=28, leading=34, textColor=accent, spaceAfter=6)
    lesson_title = spec.get("subtitle", spec.get("title", ""))
    story.append(Paragraph(lesson_title, hero_title_style))

    # Date range below title
    hero_sub_style = ParagraphStyle("hero_sub", parent=s_sub,
        fontSize=14, leading=18, textColor=muted, spaceAfter=12)
    story.append(Paragraph(spec.get("title", ""), hero_sub_style))

    # Meta info
    meta_style = ParagraphStyle("meta", fontName=FONT_SERIF, fontSize=10,
        textColor=muted, alignment=TA_LEFT, leading=14)
    story.append(Paragraph(f"Week {spec.get('week', '—')}  |  {spec.get('scriptures', '')}", meta_style))
    story.append(Spacer(1, 8))

    # Gold double rule under hero
    story.append(HRFlowable(width="100%", thickness=2, color=gold, spaceAfter=4, spaceBefore=2))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#EAB30B"), spaceAfter=12, spaceBefore=2))

    # Track section index for color coding
    section_colors = {
        "accent": accent, "gold": gold, "warm": warm,
        "teal": teal, "red": red, "muted": muted
    }

    for sec_idx, sec in enumerate(spec.get("sections", [])):
        sec_color_key = sec.get("color", "accent")
        sec_accent = section_colors.get(sec_color_key, accent)

        # Section header with colored left border simulation
        heading_text = sec["heading"]
        heading_text = f"{sec_idx + 1}. {heading_text}"

        # Create a styled header with left indent and color
        header_style = ParagraphStyle(
            f"h1_sec_{sec_idx}", parent=s_h1_num,
            textColor=sec_accent,
            leftIndent=8,
            borderWidth=3,
            borderColor=sec_accent,
            borderPadding=(2, 0, 2, 8),
            backColor=HexColor("#FAF8F3"),  # Slight warm bg
            spaceBefore=14, spaceAfter=4
        )
        story.append(Paragraph(heading_text, header_style))

        if sec.get("summary"):
            story.append(Paragraph(sec["summary"], s_sum))

        if sec.get("body"):
            story.append(Paragraph(sec["body"], s_body))

        # Handle bullets
        for bullet in sec.get("bullets", []):
            if bullet.startswith("Q: "):
                parts = bullet.split(" | ")
                q = a = s = w = ""
                for p in parts:
                    if p.startswith("Q: "):
                        q = p[3:]
                    elif p.startswith("A: "):
                        a = p[3:]
                    elif p.startswith("S: "):
                        s = p[3:]
                    elif p.startswith("W: "):
                        w = p[3:]
                if q:
                    q_style = ParagraphStyle("qa_q", parent=s_body,
                            fontName=FONT_SANS_BOLD, textColor=ink,
                            spaceBefore=8, spaceAfter=2, leading=14)
                    story.append(Paragraph(q, q_style))
                if a:
                    story.append(Paragraph(a, s_bul))
                if s:
                    story.append(Paragraph(f"Scripture: {s}", s_scripture))
                if w:
                    story.append(Paragraph("Why This Matters:", s_why_label))
                    story.append(Paragraph(w, s_why_text))
            else:
                story.append(Paragraph(bullet, s_bul))

        tbl = sec.get("table")
        if tbl:
            story.append(Spacer(1, 6))
            raw_data = [tbl["header"]] + tbl["rows"]
            num_cols = len(tbl["header"])
            
            # Calculate column widths based on table type - use absolute points for precise control
            usable_width = 544  # 595pt - 18mm margins each side = 544pt
            
            if num_cols == 4:
                # 4 columns - explicit point widths for content
                col_widths = [80, 120, 130, 214]
            elif num_cols == 3:
                # 3 columns
                col_widths = [160, 70, 284]
            else:
                # Default: equal widths
                col_widths = [usable_width / num_cols] * num_cols
            
            # Convert all cell content to Paragraph objects for proper text wrapping
            def make_cell_paragraph(text, is_header=False, col_idx=None):
                """Convert cell text to Paragraph with appropriate style for wrapping."""
                if is_header:
                    style = ParagraphStyle(
                        f"tbl_hdr_{col_idx}", 
                        fontName=FONT_SANS_BOLD, 
                        fontSize=9, 
                        textColor=bg, 
                        leading=11,
                        alignment=TA_LEFT,
                        wordWrap='CJK'  # Force wrapping
                    )
                else:
                    if col_idx == 0:  # First column
                        style = ParagraphStyle(
                            f"tbl_cell_0_{col_idx}", 
                            fontName=FONT_SANS, 
                            fontSize=8, 
                            textColor=ink, 
                            leading=10,
                            alignment=TA_LEFT,
                            wordWrap='CJK'
                        )
                    elif col_idx == num_cols - 1:  # Last column
                        style = ParagraphStyle(
                            f"tbl_cell_last_{col_idx}", 
                            fontName=FONT_SANS, 
                            fontSize=8, 
                            textColor=ink, 
                            leading=10,
                            alignment=TA_LEFT,
                            wordWrap='CJK'
                        )
                    else:  # Middle columns
                        style = ParagraphStyle(
                            f"tbl_cell_{col_idx}", 
                            fontName=FONT_SANS, 
                            fontSize=8, 
                            textColor=ink, 
                            leading=10,
                            alignment=TA_LEFT,
                            wordWrap='CJK'
                        )
                return Paragraph(text, style)
            
            # Convert all data to Paragraphs
            wrapped_data = []
            for row_idx, row in enumerate(raw_data):
                wrapped_row = []
                for col_idx, cell_text in enumerate(row):
                    is_header = (row_idx == 0)
                    wrapped_row.append(make_cell_paragraph(str(cell_text), is_header, col_idx))
                wrapped_data.append(wrapped_row)
            
            t = Table(wrapped_data, colWidths=col_widths, repeatRows=1)
            header_color = section_colors.get(tbl.get("header_color", "accent"), accent)
            t.setStyle(make_table_style(header_color))
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 8))

        # Spacer between sections
        story.append(Spacer(1, 10))

    # Build with page numbers
    doc.build(story)


def render_previews(pdf_path, out_dir):
    try:
        import fitz
    except ImportError:
        warn("PyMuPDF not installed; skipping previews (pip install pymupdf)")
        return
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        p = os.path.join(out_dir, f"page-{i + 1}.png")
        page.get_pixmap(dpi=110).save(p)
        print(f"preview: {p}")


def main():
    ap = argparse.ArgumentParser(description="Render spec.json to PDF (no HTML).")
    ap.add_argument("spec", help="content spec JSON file")
    ap.add_argument("-o", "--output", default="out.pdf")
    ap.add_argument("--preview", action="store_true",
                    help="render PNG previews of the built PDF")
    ap.add_argument("--preview-dir", default="previews")
    args = ap.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)

    mode = spec.get("mode", "poster")
    if mode == "poster":
        build_poster(spec, args.output)
    elif mode == "manual":
        build_manual(spec, args.output)
    else:
        sys.exit(f"unknown mode: {mode!r} (use 'poster' or 'manual')")

    print(f"built: {args.output}")
    if args.preview:
        render_previews(args.output, args.preview_dir)
    if WARNINGS:
        sys.exit(f"{len(WARNINGS)} layout warning(s) — check spec and re-run")


if __name__ == "__main__":
    main()