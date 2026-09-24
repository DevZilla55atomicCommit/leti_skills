#!/usr/bin/env python3
"""
Come Follow Me Study Guide Generator
Generates mobile-first HTML study guides from structured data.
Organizes output by Year/Month: ~/Desktop/Come Follow Me Study Guides/YYYY/MM/WeekX_Topic/

Used by Hermes default profile cron job (Mondays 7 AM PDT).

Usage:
    python3 generate_study_guide.py --data lesson_data.json --output-base ~/Desktop/Come Follow Me Study Guides
    python3 generate_study_guide.py --data lesson_data.json --output-base ~/Desktop/Come Follow Me Study Guides --personal
"""

import json
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from string import Template

# ========================================
# TEMPLATE LOADING
# ========================================
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "study-guide-template.html"

def load_template():
    """Load the HTML template."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

# ========================================
# DATA VALIDATION & DEFAULTS
# ========================================
REQUIRED_FIELDS = ['title', 'weekDate', 'scriptures', 'lessonId']

DEFAULTS = {
    'scripture': '',
    'commentary': '',
    'application': '',
    'scriptureLinks': [],
    'commentaryLinks': [],
    'applicationLinks': [],
    'generationDate': datetime.now().strftime('%B %d, %Y'),
    'personal': False
}

def validate_data(data):
    """Validate required fields and apply defaults."""
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Apply defaults
    for key, default in DEFAULTS.items():
        data.setdefault(key, default)
    
    return data

# ========================================
# CONTENT PROCESSING
# ========================================
def format_scripture_refs(text):
    """Convert scripture references like 'John 3:16' to deep links."""
    import re
    # Pattern: Book Chapter:Verse (e.g., "Moses 5:5–7", "D&C 119:1–4", "James 1:8")
    pattern = r'\b([1-3]?\s?[A-Za-z]+\.?\s+\d+:\d+(?:[–-]\d+)?)\b'
    
    def replace_ref(match):
        ref = match.group(1).strip()
        # Build Gospel Library URL
        url = build_gospel_library_url(ref)
        return f'<a href="{url}" class="scripture-ref" target="_blank" rel="noopener">{ref}</a>'
    
    return re.sub(pattern, replace_ref, text)

def build_gospel_library_url(reference):
    """Build a churchofjesuschrist.org study URL for a scripture reference."""
    # Simplified - in production, use a proper parser
    # Format: https://www.churchofjesuschrist.org/study/scriptures/[book]/[chapter]?lang=eng&id=p[verse]
    base = "https://www.churchofjesuschrist.org/study/scriptures"
    # This is a placeholder - real implementation would parse book/chapter/verse
    return f"{base}?search={reference.replace(' ', '+')}"

def process_content(data):
    """Process content fields: format scripture refs, etc."""
    for field in ['scripture', 'commentary', 'application']:
        if data.get(field):
            data[field] = format_scripture_refs(data[field])
    return data

# ========================================
# FOLDER STRUCTURE: YYYY/MMM/Week X - Topic - DateRange/
# ========================================
def compute_output_folder(output_base: Path, lesson_id: str, title: str, week_date: str) -> Path:
    """
    Compute output folder: ~/Desktop/Come Follow Me 2026/2026/MMM/Week X - Topic - DateRange/
    
    lesson_id format: "2026-36" or "2026-09-week-36"
    title: "Job", "Psalms", etc.
    week_date: "September 7–13, 2026"
    """
    # Parse year from lesson_id
    parts = lesson_id.replace('week-', '').replace('-week-', '-').split('-')
    year = int(parts[0])
    
    # Compute week-of-month (1-5) and month from week_date
    month_num = 1
    week_of_month = 1
    if week_date:
        try:
            import re
            # Parse "August 31–September 6, 2026" or "September 7–13, 2026"
            date_match = re.search(r'([A-Za-z]+)\s+(\d+)', week_date)
            if date_match:
                month_name = date_match.group(1)[:3].capitalize()
                day = int(date_match.group(2))
                month_map = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
                            'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
                month_num = month_map.get(month_name, 1)
                
                # Compute week of month (1-5): (day-1)//7 + 1
                week_of_month = (day - 1) // 7 + 1
        except:
            pass
    
    # Fallback: calculate from week number in lesson_id
    if month_num == 1 and not (week_date and 'jan' in week_date.lower()):
        try:
            week_num = int(parts[-1])
            month_num = min(12, max(1, (week_num - 1) // 4 + 1))
            # Approximate week of month
            week_of_month = ((week_num - 1) % 4) + 1
        except:
            pass
    
    # Format: YYYY/MMM/
    year_str = str(year)
    month_map_rev = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                     7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    month_str = month_map_rev.get(month_num, 'Jan')
    
    # Topic from title (clean for filesystem)
    topic = title.strip().replace('"', '').replace("'", '').replace(' ', '')
    # Remove special chars but keep hyphens
    import re
    topic = re.sub(r'[^A-Za-z0-9-]', '', topic)
    
    # Week label with space: "Week X" (week of month)
    week_label = f"Week {week_of_month}"
    
    # Date range for folder name
    date_range = week_date.replace(' ', '').replace('–', '-').replace(',', '')
    
    # Folder: YYYY/MMM/Week X - Topic - DateRange/
    folder_name = f"{week_label} - {topic} - {date_range}"
    
    return output_base / year_str / month_str / folder_name

# ========================================
# TEMPLATE RENDERING
# ========================================
def render_template(template, data):
    """Render template with data using string replacement."""
    # Simple placeholder replacement for the static template
    # The template uses JavaScript CFMTemplate.setLessonData() for dynamic content
    
    # We inject a script tag at the end of body to initialize with data
    init_script = f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.CFMTemplate) {{
                window.CFMTemplate.setLessonData({json.dumps(data, ensure_ascii=False)});
            }}
        }});
    </script>
    """
    
    # Insert before closing body tag
    html = template.replace('</body>', init_script + '\n</body>')
    return html

# ========================================
# FILE OUTPUT
# ========================================
def write_output(html, output_folder, lesson_id, topic):
    """Write HTML file to output folder."""
    output_path = Path(output_folder).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"{topic}_Lesson_Final.html"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

# ========================================
# MAIN
# ========================================
def main():
    parser = argparse.ArgumentParser(description='Generate CFM Study Guide HTML')
    parser.add_argument('--data', required=True, help='Path to lesson data JSON file')
    parser.add_argument('--output-base', default='~/Desktop/Come Follow Me 2026/2026', help='Base output directory')
    parser.add_argument('--personal', action='store_true', help='Generate personal study version')
    parser.add_argument('--template', help='Custom template path (optional)')
    
    args = parser.parse_args()
    
    # Load data
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data['personal'] = args.personal
    
    # Validate
    data = validate_data(data)
    
    # Process content
    data = process_content(data)
    
    # Load template
    if args.template:
        with open(args.template, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        template = load_template()
    
    # Compute output folder with YYYY/MM/WeekX_Topic structure
    output_base = Path(args.output_base).expanduser()
    output_folder = compute_output_folder(
        output_base, 
        data['lessonId'], 
        data['title'], 
        data.get('weekDate', '')
    )
    
    # Render
    html = render_template(template, data)
    
    # Write output
    topic = data['title'].strip().replace('"', '').replace("'", '').replace(' ', '_')
    import re
    topic = re.sub(r'[^A-Za-z0-9_-]', '', topic)
    
    filepath = write_output(html, output_folder, data['lessonId'], topic)
    
    print(f"✅ Generated: {filepath}")
    print(f"   Title: {data['title']}")
    print(f"   Week: {data['weekDate']}")
    print(f"   Folder: {output_folder}")
    print(f"   Mode: {'Personal Study' if args.personal else 'Standard'}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())