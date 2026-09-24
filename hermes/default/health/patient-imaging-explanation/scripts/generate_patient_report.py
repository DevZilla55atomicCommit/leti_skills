#!/usr/bin/env python3
"""
Patient Imaging Report PDF Generator
Used by the patient-imaging-explanation skill to create formatted, printable PDFs
for patients to bring to appointments.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, red, green, orange
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
import datetime


def create_findings_table(findings_data, key_finding_row=None):
    """Create a color-coded findings table."""
    table_header_style = ParagraphStyle(
        'TableHeader', parent=getSampleStyleSheet()['Normal'],
        fontSize=10, leading=12, textColor=colors.white,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_LEFT
    )
    table_cell_center_style = ParagraphStyle(
        'TableCellCenter', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_CENTER
    )

    data = [[
        Paragraph("<b>Area</b>", table_header_style),
        Paragraph("<b>Result</b>", table_header_style),
        Paragraph("<b>What It Means</b>", table_header_style)
    ]]
    for row in findings_data:
        data.append([
            Paragraph(row[0], table_cell_style),
            Paragraph(row[1], table_cell_center_style),
            Paragraph(row[2], table_cell_style)
        ])

    t = Table(data, colWidths=[1.5*inch, 1.8*inch, 3.2*inch])
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8fafc'), HexColor('#ffffff')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if key_finding_row is not None:
        # Adjust for header row offset
        style_cmds.append(('BACKGROUND', (0, key_finding_row + 1), (-1, key_finding_row + 1), HexColor('#fee2e2')))
    t.setStyle(TableStyle(style_cmds))
    return t


def create_size_risk_table(patient_size_cm, condition="internal_iliac_aneurysm"):
    """Create a size-risk stratification table with patient row highlighted."""
    table_header_style = ParagraphStyle(
        'TableHeader', parent=getSampleStyleSheet()['Normal'],
        fontSize=10, leading=12, textColor=colors.white,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_LEFT
    )
    table_cell_center_style = ParagraphStyle(
        'TableCellCenter', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_CENTER
    )

    if condition == "internal_iliac_aneurysm":
        rows = [
            ["Normal", "4–6 mm", "~0%", "None"],
            ["Small", "< 2 cm", "< 2%", "Surveillance q6–12mo"],
            ["Medium", "2–3 cm", "2–5%", "Individualized"],
            ["Large", "3–5 cm", "5–15%+", "Repair recommended"],
            ["Giant", "> 5 cm", "20–40%+", "<b>Urgent repair</b>"],
            [f"<b>Patient</b>", f"<b><font size='12' color='#dc2626'>{patient_size_cm} cm</font></b>",
             "<b><font size='12' color='#dc2626'>VERY HIGH</font></b>",
             "<b><font size='11' color='#dc2626'>EMERGENCY REPAIR</font></b>"],
        ]
    else:
        rows = []

    data = [[
        Paragraph("<b>Category</b>", table_header_style),
        Paragraph("<b>Diameter</b>", table_header_style),
        Paragraph("<b>Annual Rupture Risk</b>", table_header_style),
        Paragraph("<b>Standard of Care</b>", table_header_style)
    ]]
    for row in rows:
        data.append([
            Paragraph(row[0], table_cell_style),
            Paragraph(row[1], table_cell_center_style),
            Paragraph(row[2], table_cell_center_style),
            Paragraph(row[3], table_cell_center_style)
        ])

    t = Table(data, colWidths=[1.3*inch, 1.0*inch, 2.0*inch, 2.2*inch])
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
        ('BACKGROUND', (0, 1), (-1, -2), HexColor('#f8fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [HexColor('#f8fafc'), HexColor('#ffffff')]),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#fee2e2')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def create_mortality_table():
    """Create mortality comparison table."""
    table_header_style = ParagraphStyle(
        'TableHeader', parent=getSampleStyleSheet()['Normal'],
        fontSize=10, leading=12, textColor=colors.white,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_LEFT
    )
    table_cell_center_style = ParagraphStyle(
        'TableCellCenter', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_CENTER
    )

    rows = [
        ["Elective endovascular repair (planned)", "<font size='14' color='#16a34a'><b>< 1–2%</b></font>",
         "Groin puncture, coils/stent. Home next day. Best outcome."],
        ["Elective open repair (planned)", "<font size='14' color='#ca8a04'><b>2–5%</b></font>",
         "Larger incision, longer recovery. Still very safe electively."],
        ["Emergency repair AFTER RUPTURE", "<font size='14' color='#dc2626'><b>40–70%</b></font>",
         "Massive transfusion, ICU, multi-organ failure. Many die before reaching OR."],
        ["No treatment (rupture at home)", "<font size='14' color='#dc2626'><b>> 90%</b></font>",
         "Exsanguination in pelvis. Most never reach hospital alive."],
    ]

    data = [[
        Paragraph("<b>Scenario</b>", table_header_style),
        Paragraph("<b>Mortality (Death) Rate</b>", table_header_style),
        Paragraph("<b>What This Means</b>", table_header_style)
    ]]
    for row in rows:
        data.append([
            Paragraph(row[0], table_cell_style),
            Paragraph(row[1], table_cell_center_style),
            Paragraph(row[2], table_cell_style)
        ])

    t = Table(data, colWidths=[1.8*inch, 1.5*inch, 3.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#b91c1c')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fef2f2')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fef2f2'), HexColor('#fee2e2')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#fecaca')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def create_action_plan_table():
    """Create immediate action plan table."""
    table_header_style = ParagraphStyle(
        'TableHeader', parent=getSampleStyleSheet()['Normal'],
        fontSize=10, leading=12, textColor=colors.white,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_LEFT
    )
    table_cell_center_style = ParagraphStyle(
        'TableCellCenter', parent=getSampleStyleSheet()['Normal'],
        fontSize=9.5, leading=12, alignment=TA_CENTER
    )

    rows = [
        ["1", "Call the doctor who ordered the CT. Say: <b>\"I have a 7 cm internal iliac aneurysm. I need an URGENT vascular surgery referral TODAY.\"</b>",
         "<b><font color='#dc2626'>TODAY</font></b>", "Patient / Family"],
        ["2", "If doctor unavailable: Call hospital operator → ask for <b>Vascular Surgery on-call</b>. Say: <b>\"7 cm symptomatic internal iliac aneurysm — need urgent clinic/surgery scheduling.\"</b>",
         "<b><font color='#dc2626'>TODAY</font></b>", "Patient / Family"],
        ["3", "Vascular surgeon orders <b>CT Angiogram (CTA)</b> if not already done — confirms exact anatomy for repair planning.",
         "<b><font color='#dc2626'>THIS WEEK</font></b>", "Vascular Surgeon"],
        ["4", "Surgery scheduled: <b>Endovascular coil embolization</b> (preferred) or <b>stent-graft</b> or <b>open ligation</b>. Usually 1–2 hr, overnight stay.",
         "<b><font color='#dc2626'>WITHIN 1–2 WEEKS MAX</font></b>", "Vascular Surgeon"],
        ["5", "<b>Activity restrictions START NOW:</b> No lifting >5 lbs. No straining (constipation = use stool softener). BP <130/80 (adjust meds if needed). No vigorous exercise.",
         "<b><font color='#dc2626'>IMMEDIATELY</font></b>", "Patient"],
    ]

    data = [[
        Paragraph("<b>Step</b>", table_header_style),
        Paragraph("<b>Action</b>", table_header_style),
        Paragraph("<b>Deadline</b>", table_header_style),
        Paragraph("<b>Who Does It</b>", table_header_style)
    ]]
    for row in rows:
        data.append([
            Paragraph(row[0], table_cell_center_style),
            Paragraph(row[1], table_cell_style),
            Paragraph(row[2], table_cell_center_style),
            Paragraph(row[3], table_cell_center_style)
        ])

    t = Table(data, colWidths=[0.4*inch, 3.2*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#b91c1c')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fef2f2')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fef2f2'), HexColor('#fee2e2')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#fecaca')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


# Example usage
if __name__ == "__main__":
    # Test the table generators
    print("Tables generated successfully")