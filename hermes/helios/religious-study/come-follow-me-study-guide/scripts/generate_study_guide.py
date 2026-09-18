#!/usr/bin/env python3
"""
Come Follow Me Study Guide Generator
Generates mobile-first HTML study guides from structured data.
Used by Helios cron job (Mondays 7 AM PDT).

Outputs to:
- ~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Teacher Lessons/
- ~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Personal Study/

Usage:
    python3 generate_study_guide.py --data lesson_data.json --output-dir ~/Desktop/.../Teacher Lessons
    python3 generate_study_guide.py --data lesson_data.json --output-dir ~/Desktop/.../Personal Study --personal
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
def write_output(html, output_dir, lesson_id, personal=False):
    """Write HTML file to output directory."""
    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)
    
    suffix = '-personal' if personal else '-teacher'
    filename = f"{lesson_id}{suffix}.html"
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
    parser.add_argument('--output-dir', required=True, help='Output directory')
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
    template = load_template()
    
    # Render
    html = render_template(template, data)
    
    # Write output
    filepath = write_output(html, args.output_dir, data['lessonId'], args.personal)
    
    print(f"✅ Generated: {filepath}")
    print(f"   Title: {data['title']}")
    print(f"   Week: {data['weekDate']}")
    print(f"   Mode: {'Personal Study' if args.personal else 'Teacher Lesson'}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())