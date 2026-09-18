#!/usr/bin/env python3
"""
CFM Mobile Renderer — Standalone module for cron job integration.

Usage:
    from render_cfm_mobile import render_cfm_mobile
    html = render_cfm_mobile(cfm_data, color_scheme='eq')
    
    # Or CLI:
    python render_cfm_mobile.py lesson.json output.html
"""

import json
import sys
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ============================================================
# ELDER'S QUORUM COLOR SCHEME
# ============================================================
EQ_COLORS = {
    "color_scripture": "#0d5d3a",   # Deep green — priesthood/authority
    "color_gold": "#b8963e",        # Brass — EQ branding
    "color_dark_brass": "#8b7330",
    "color_warm_white": "#fdfbf7",
    "color_light_gold": "#f5ebe0",
    "color_ink": "#1f2a2e",
    "color_ink_soft": "#3d4a4d",
    "color_border": "#e8e4dc",
    "color_bg": "#faf9f6",
    "color_card": "#ffffff",
    "color_shadow": "rgba(31, 42, 46, 0.08)",
    "color_focus": "#b8963e",
}

# Helios' 6 Hues for question sections
HELIOS_HUES = [
    "#e85d2a",  # Ember Orange
    "#d4a83c",  # Solar Gold
    "#4a9e4f",  # Verdant Green
    "#3a7bc8",  # Azure Blue
    "#8b5fb8",  # Amethyst Purple
    "#c84a6a",  # Rose Crimson
]

HELIOS_HUES_DARK = [
    "#f57c4a",
    "#e4c05c",
    "#6acc6f",
    "#6aa8e8",
    "#b88df8",
    "#f87aa8",
]

DEFAULT_HERO_ARTWORK = "https://www.churchofjesuschrist.org/media/image/adam-eve-altar-6752507"

# ============================================================
# GOSPEL LIBRARY URL BUILDER
# ============================================================
BOOK_PATHS = {
    'genesis': 'ot/gen', 'exodus': 'ot/ex', 'leviticus': 'ot/lev', 'numbers': 'ot/num', 'deuteronomy': 'ot/deut',
    'joshua': 'ot/josh', 'judges': 'ot/judg', 'ruth': 'ot/ruth', '1 samuel': 'ot/1-sam', '2 samuel': 'ot/2-sam',
    '1 kings': 'ot/1-kgs', '2 kings': 'ot/2-kgs', '1 chronicles': 'ot/1-chr', '2 chronicles': 'ot/2-chr',
    'ezra': 'ot/ezra', 'nehemiah': 'ot/neh', 'esther': 'ot/esth', 'job': 'ot/job', 'psalms': 'ot/ps',
    'proverbs': 'ot/prov', 'ecclesiastes': 'ot/eccl', 'song of solomon': 'ot/song', 'isaiah': 'ot/isa',
    'jeremiah': 'ot/jer', 'lamentations': 'ot/lam', 'ezekiel': 'ot/ezek', 'daniel': 'ot/dan',
    'hosea': 'ot/hosea', 'joel': 'ot/joel', 'amos': 'ot/amos', 'obadiah': 'ot/obad', 'jonah': 'ot/jonah',
    'micah': 'ot/micah', 'nahum': 'ot/nahum', 'habakkuk': 'ot/hab', 'zephaniah': 'ot/zeph', 'haggai': 'ot/hag',
    'zechariah': 'ot/zech', 'malachi': 'ot/mal',
    'matthew': 'nt/matt', 'mark': 'nt/mark', 'luke': 'nt/luke', 'john': 'nt/jn', 'acts': 'nt/acts',
    'romans': 'nt/rom', '1 corinthians': 'nt/1-cor', '2 corinthians': 'nt/2-cor', 'galatians': 'nt/gal',
    'ephesians': 'nt/eph', 'philippians': 'nt/phil', 'colossians': 'nt/col', '1 thessalonians': 'nt/1-thes',
    '2 thessalonians': 'nt/2-thes', '1 timothy': 'nt/1-tim', '2 timothy': 'nt/2-tim', 'titus': 'nt/titus',
    'philemon': 'nt/phlm', 'hebrews': 'nt/heb', 'james': 'nt/james', '1 peter': 'nt/1-pet', '2 peter': 'nt/2-pet',
    '1 john': 'nt/1-jn', '2 john': 'nt/2-jn', '3 john': 'nt/3-jn', 'jude': 'nt/jude', 'revelation': 'nt/rev',
    '1 nephi': 'bofm/1-ne', '2 nephi': 'bofm/2-ne', 'jacob': 'bofm/jacob', 'enos': 'bofm/enos',
    'jarom': 'bofm/jarom', 'omni': 'bofm/omni', 'words of mormon': 'bofm/w-of-m', 'mosiah': 'bofm/mosiah',
    'alma': 'bofm/alma', 'helaman': 'bofm/hel', '3 nephi': 'bofm/3-ne', '4 nephi': 'bofm/4-ne',
    'mormon': 'bofm/morm', 'ether': 'bofm/ether', 'moroni': 'bofm/moro',
    'doctrine and covenants': 'dc', 'd&c': 'dc', 'dc': 'dc',
    'moses': 'pgp/moses', 'abraham': 'pgp/abr', 'joseph smith—matthew': 'pgp/js-m', 'joseph smith—history': 'pgp/js-h',
    'articles of faith': 'pgp/a-of-f',
}

def build_gospel_url(scripture_ref: str) -> str:
    """Build Gospel Library URL from scripture reference."""
    if not scripture_ref or not scripture_ref.strip():
        return "https://www.churchofjesuschrist.org/study/scriptures"
    
    # Handle multiple references - take first
    first_ref = scripture_ref.split(';')[0].split(',')[0].strip()
    
    # Pattern: Book Chapter:Verse or Book Chapter:Verse-Verse
    match = re.search(r'([A-Za-z0-9\s.]+)\s+(\d+):(\d+)(?:[-–](\d+))?', first_ref)
    if match:
        book = match.group(1).strip().lower().replace('.', '').replace('–', '-')
        chapter = match.group(2)
        verse = match.group(3)
        
        # Normalize book name
        book_key = book.strip()
        for key in BOOK_PATHS:
            if key in book_key or book_key in key:
                book_path = BOOK_PATHS[key]
                return f"https://www.churchofjesuschrist.org/study/scriptures/{book_path}/{chapter}?lang=eng&id=p{verse}"
        
        # Fallback
        book_path = book_key.replace(' ', '-')
        return f"https://www.churchofjesuschrist.org/study/scriptures/{book_path}/{chapter}?lang=eng&id=p{verse}"
    
    return "https://www.churchofjesuschrist.org/study/scriptures"

def build_lesson_url(cfm_data: dict) -> str:
    """Build Come Follow Me lesson URL."""
    volume = cfm_data.get('volume_year', '').lower().replace(' ', '-').replace('2025', '').replace('2026', '').strip('-')
    return f"https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-{volume}?lang=eng"

# ============================================================
# DATA TRANSFORMERS
# ============================================================
def build_callouts(cfm_data: dict) -> list:
    """Build 4 pinpoint highlight callouts from CFM lesson data."""
    callouts = []
    
    # Callout 1: Core Message
    core_msg = cfm_data.get('core_message', '')
    key_verse = cfm_data.get('key_verse', '')
    if core_msg:
        callouts.append({
            "badge": "Core Message",
            "title": "The Core Message",
            "text": core_msg,
            "scripture": key_verse,
            "scripture_url": build_gospel_url(key_verse)
        })
    
    # Callout 2: Story Summary (3 sentences)
    story = cfm_data.get('story_summary', [])
    if story:
        text = ' '.join(story) if isinstance(story, list) else str(story)
        callouts.append({
            "badge": "The Story",
            "title": "The Story in Three Sentences",
            "text": text,
            "scripture": cfm_data.get('scripture_references', ''),
            "scripture_url": build_gospel_url(cfm_data.get('scripture_references', ''))
        })
    
    # Callout 3: Key Doctrine (first section)
    sections = cfm_data.get('sections', [])
    if sections:
        first = sections[0]
        first_q = first.get('questions', [{}])[0] if first.get('questions') else {}
        callouts.append({
            "badge": "Key Doctrine",
            "title": first.get('title', 'Key Doctrine'),
            "text": first.get('summary', 'Core doctrinal principle from this week\'s lesson.'),
            "scripture": first_q.get('scripture_ref', ''),
            "scripture_url": build_gospel_url(first_q.get('scripture_ref', ''))
        })
    
    # Callout 4: Application
    callouts.append({
        "badge": "Live It",
        "title": "Personal Application",
        "text": cfm_data.get('teaching_summary', 'How will you apply this week\'s lesson in your life and teaching?'),
        "scripture": "",
        "scripture_url": ""
    })
    
    return callouts[:4]

def build_threads(cfm_data: dict) -> list:
    """Build question threads from CFM lesson sections."""
    threads = []
    sections = cfm_data.get('sections', [])
    
    for i, section in enumerate(sections):
        qa_pairs = []
        questions = section.get('questions', [])
        
        for q in questions:
            qa_pairs.append({
                "question": q.get('question', ''),
                "scripture": q.get('scripture_ref', ''),
                "scripture_url": build_gospel_url(q.get('scripture_ref', '')),
                "answer": f"<p><strong>Simple Answer:</strong> {q.get('simple_answer', '')}</p><p><strong>What to Ponder:</strong> {q.get('ponder', '')}</p>"
            })
        
        if qa_pairs:
            threads.append({
                "title": section.get('title', f'Section {i+1}'),
                "qa_pairs": qa_pairs
            })
    
    # Add Teaching Children as a thread
    if cfm_data.get('teaching_children'):
        qa_pairs = []
        for child in cfm_data['teaching_children']:
            qa_pairs.append({
                "question": f"Teaching Children: {child.get('scripture', '')}",
                "scripture": child.get('scripture', ''),
                "scripture_url": build_gospel_url(child.get('scripture', '')),
                "answer": f"<p><strong>Kid-Level Answer:</strong> {child.get('kid_answer', '')}</p><p><strong>Resource:</strong> {child.get('resource', '')}</p>"
            })
        threads.append({
            "title": "Teaching Children",
            "qa_pairs": qa_pairs
        })
    
    return threads

def build_resources(cfm_data: dict) -> list:
    """Build resources from podcast insights and BYU Studies."""
    resources = []
    
    # Podcast insights
    for podcast in cfm_data.get('podcast_insights', []):
        insights_html = ''
        if podcast.get('insights'):
            insights_html = '<ul>' + ''.join(f'<li>{i}</li>' for i in podcast['insights']) + '</ul>'
        resources.append({
            "type": "audio",
            "title": f"{podcast.get('name', 'Podcast')} — {podcast.get('guest', '')}",
            "author": podcast.get('guest', 'Host'),
            "source": f"{podcast.get('name', 'Podcast')} ({podcast.get('duration', '')})",
            "url": podcast.get('url', '#'),
            "insights_html": insights_html
        })
    
    # BYU Studies
    for study in cfm_data.get('byu_studies', []):
        resources.append({
            "type": "article",
            "title": study.get('article', 'BYU Studies Article'),
            "author": study.get('author', 'BYU Studies'),
            "source": f"BYU Studies — {study.get('scripture', '')}",
            "url": study.get('url', '#'),
            "insight": study.get('insight', '')
        })
    
    # Add Gospel Library link
    resources.append({
        "type": "article",
        "title": f"Full Lesson: {cfm_data.get('lesson_title', 'Come Follow Me')}",
        "author": "The Church of Jesus Christ of Latter-day Saints",
        "source": "Gospel Library",
        "url": build_lesson_url(cfm_data),
        "insight": ""
    })
    
    return resources

def build_reflections(cfm_data: dict) -> list:
    """Build reflection prompts from questions and teaching summary."""
    reflections = []
    
    # One reflection per question section
    for section in cfm_data.get('sections', []):
        for q in section.get('questions', []):
            if q.get('ponder'):
                reflections.append({
                    "question": q['ponder']
                })
    
    # Add teaching summary reflection
    if cfm_data.get('teaching_summary'):
        reflections.append({
            "question": f"Teaching Application: {cfm_data['teaching_summary']}"
        })
    
    # Limit to 5 reflections
    return reflections[:5]

# ============================================================
# MAIN RENDER FUNCTION
# ============================================================
def render_cfm_mobile(cfm_data: dict, color_scheme: str = 'eq') -> str:
    """
    Render a CFM weekly lesson as mobile-optimized HTML using Apollo's template.
    
    Args:
        cfm_data: Dictionary with CFM lesson structure (see module docstring)
        color_scheme: 'eq' for Elder's Quorum, 'cfm' for Come Follow Me
    
    Returns:
        Complete HTML string ready to save as .html file
    """
    
    # Select color scheme
    if color_scheme == 'eq':
        colors = EQ_COLORS.copy()
        hues = HELIOS_HUES
        hues_dark = HELIOS_HUES_DARK
    else:
        colors = {
            "color_scripture": "#0d5d3a",
            "color_gold": "#c9a84c",
            "color_dark_brass": "#8b7330",
            "color_warm_white": "#fdfbf7",
            "color_light_gold": "#f5ebe0",
            "color_ink": "#1f2a2e",
            "color_ink_soft": "#3d4a4d",
            "color_border": "#e8e4dc",
            "color_bg": "#faf9f6",
            "color_card": "#ffffff",
            "color_shadow": "rgba(31, 42, 46, 0.08)",
            "color_focus": "#c9a84c",
        }
        hues = HELIOS_HUES
        hues_dark = HELIOS_HUES_DARK
    
    # Build template data
    template_data = {
        "speaker_name": "Come, Follow Me",
        "speaker_title": f"For Home and Church — {cfm_data.get('volume_year', '')}",
        "talk_title": cfm_data.get('lesson_title', 'Weekly Lesson'),
        "conference": cfm_data.get('volume_year', 'Come Follow Me'),
        "session": cfm_data.get('date_range', ''),
        "date": cfm_data.get('date_range', ''),
        "hero_artwork": cfm_data.get('hero_artwork', DEFAULT_HERO_ARTWORK),
        "callouts": build_callouts(cfm_data),
        "threads": build_threads(cfm_data),
        "resources": build_resources(cfm_data),
        "reflections": build_reflections(cfm_data),
    }
    
    # Load mobile template
    template_dir = Path(__file__).parent.parent / 'templates'
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template('personal-study.html')
    
    # Render
    html = template.render(**template_data)
    
    # Inject EQ color overrides
    if color_scheme == 'eq':
        color_css = f"""
    <style>
    :root {{
      --color-scripture: {colors['color_scripture']};
      --color-gold: {colors['color_gold']};
      --color-dark-brass: {colors['color_dark_brass']};
      --color-warm-white: {colors['color_warm_white']};
      --color-light-gold: {colors['color_light_gold']};
      --color-ink: {colors['color_ink']};
      --color-ink-soft: {colors['color_ink_soft']};
      --color-border: {colors['color_border']};
      --color-bg: {colors['color_bg']};
      --color-card: {colors['color_card']};
      --color-shadow: {colors['color_shadow']};
      --color-focus: {colors['color_focus']};
    }}
    [data-theme="dark"] {{
      --color-scripture: #4ade80;
      --color-gold: #c4a452;
      --color-dark-brass: #a68a42;
      --color-warm-white: #1f2a2e;
      --color-light-gold: #2d3a3d;
      --color-ink: #fdfbf7;
      --color-ink-soft: #e8e4dc;
      --color-border: #3d4a4d;
      --color-bg: #162023;
      --color-card: #1f2a2e;
      --color-shadow: rgba(0, 0, 0, 0.3);
      --color-focus: #c4a452;
    }}
    .question-1 .section-header {{ background: linear-gradient(90deg, {hues[0]} 0%, color-mix(in srgb, {hues[0]} 70%, black) 100%); }}
    .question-2 .section-header {{ background: linear-gradient(90deg, {hues[1]} 0%, {colors['color_dark_brass']} 100%); }}
    .question-3 .section-header {{ background: linear-gradient(90deg, {hues[2]} 0%, color-mix(in srgb, {hues[2]} 70%, black) 100%); }}
    .question-4 .section-header {{ background: linear-gradient(90deg, {hues[3]} 0%, color-mix(in srgb, {hues[3]} 70%, black) 100%); }}
    .question-5 .section-header {{ background: linear-gradient(90deg, {hues[4]} 0%, color-mix(in srgb, {hues[4]} 70%, black) 100%); }}
    .question-6 .section-header {{ background: linear-gradient(90deg, {hues[5]} 0%, color-mix(in srgb, {hues[5]} 70%, black) 100%); }}
    @media print {{
      .callout-1 {{ border-left-color: {hues[0]} !important; }}
      .callout-2 {{ border-left-color: {hues[1]} !important; }}
      .callout-3 {{ border-left-color: {hues[2]} !important; }}
      .callout-4 {{ border-left-color: {hues[3]} !important; }}
      .question-1 .section-header {{ background: linear-gradient(90deg, {hues[0]} 0%, color-mix(in srgb, {hues[0]} 70%, black) 100%) !important; }}
      .question-2 .section-header {{ background: linear-gradient(90deg, {hues[1]} 0%, {colors['color_dark_brass']} 100%) !important; }}
      .question-3 .section-header {{ background: linear-gradient(90deg, {hues[2]} 0%, color-mix(in srgb, {hues[2]} 70%, black) 100%) !important; }}
      .question-4 .section-header {{ background: linear-gradient(90deg, {hues[3]} 0%, color-mix(in srgb, {hues[3]} 70%, black) 100%) !important; }}
      .question-5 .section-header {{ background: linear-gradient(90deg, {hues[4]} 0%, color-mix(in srgb, {hues[4]} 70%, black) 100%) !important; }}
      .question-6 .section-header {{ background: linear-gradient(90deg, {hues[5]} 0%, color-mix(in srgb, {hues[5]} 70%, black) 100%) !important; }}
    }}
    </style>
"""
        html = html.replace('</head>', color_css + '\n</head>')
    
    return html

# ============================================================
# CLI ENTRY POINT
# ============================================================
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python render_cfm_mobile.py input.json output.html [color_scheme]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    color_scheme = sys.argv[3] if len(sys.argv) > 3 else 'eq'
    
    with open(input_path, 'r') as f:
        cfm_data = json.load(f)
    
    html = render_cfm_mobile(cfm_data, color_scheme)
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding='utf-8')
    
    print(f"✅ Rendered: {output.absolute()}")
    print(f"   Lesson: {cfm_data.get('lesson_title')}")
    print(f"   Sections: {len(cfm_data.get('sections', []))}")
    print(f"   Color scheme: {color_scheme}")
