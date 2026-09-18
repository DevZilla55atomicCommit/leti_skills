#!/usr/bin/env python3
"""
CFM Mobile Adapter — Renders Come Follow Me weekly lessons using Apollo's mobile template
with Elder's Quorum color scheme.

Usage:
    from cfm_mobile_adapter import render_cfm_mobile
    html = render_cfm_mobile(cfm_data, color_scheme='eq')
"""

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Elder's Quorum Color Scheme
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

# Default lesson artwork (Mike Malm style)
DEFAULT_HERO_ARTWORK = "https://www.churchofjesuschrist.org/media/image/adam-eve-altar-6752507"

def slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def build_callouts(cfm_data: dict) -> list:
    """Build 4 pinpoint highlight callouts from CFM lesson data."""
    callouts = []
    
    # Callout 1: Core Message
    if cfm_data.get('core_message'):
        callouts.append({
            "badge": "Core Message",
            "title": cfm_data['core_message'].get('title', 'The Core Message'),
            "text": cfm_data['core_message'].get('text', ''),
            "scripture": cfm_data['core_message'].get('key_verse', ''),
            "scripture_url": build_gospel_url(cfm_data['core_message'].get('key_verse', ''))
        })
    
    # Callout 2: Story Summary (3 sentences)
    if cfm_data.get('story_summary'):
        sentences = cfm_data['story_summary']
        if isinstance(sentences, list):
            text = ' '.join(sentences)
        else:
            text = sentences
        callouts.append({
            "badge": "The Story",
            "title": "The Story in Three Sentences",
            "text": text,
            "scripture": cfm_data.get('scripture_references', ''),
            "scripture_url": build_gospel_url(cfm_data.get('scripture_references', ''))
        })
    
    # Callout 3: Key Doctrine
    if cfm_data.get('sections'):
        first_section = cfm_data['sections'][0]
        callouts.append({
            "badge": "Key Doctrine",
            "title": first_section.get('title', 'Key Doctrine'),
            "text": first_section.get('summary', 'Core doctrinal principle from this week\'s lesson.'),
            "scripture": first_section.get('questions', [{}])[0].get('scripture_ref', '') if first_section.get('questions') else '',
            "scripture_url": build_gospel_url(first_section.get('questions', [{}])[0].get('scripture_ref', '') if first_section.get('questions') else '')
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
        resources.append({
            "type": "audio",
            "title": f"{podcast.get('name', 'Podcast')} — {podcast.get('guest', '')}",
            "author": podcast.get('guest', 'Host'),
            "source": podcast.get('name', 'Podcast'),
            "url": podcast.get('url', '#')
        })
    
    # BYU Studies
    for study in cfm_data.get('byu_studies', []):
        resources.append({
            "type": "article",
            "title": study.get('article', 'BYU Studies Article'),
            "author": study.get('author', 'BYU Studies'),
            "source": "BYU Studies Quarterly",
            "url": study.get('url', '#')
        })
    
    # Add Gospel Library link
    resources.append({
        "type": "article",
        "title": f"Full Lesson: {cfm_data.get('lesson_title', 'Come Follow Me')}",
        "author": "The Church of Jesus Christ of Latter-day Saints",
        "source": "Gospel Library",
        "url": build_lesson_url(cfm_data)
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

def build_cheat_sheet(cfm_data: dict) -> list:
    """Build cheat sheet items from CFM data."""
    cheat_items = []
    for item in cfm_data.get('cheat_sheet', []):
        cheat_items.append({
            "question": item.get('question', ''),
            "answer": item.get('answer', ''),
            "scripture": item.get('scripture', '')
        })
    return cheat_items

def build_gospel_url(scripture_ref: str) -> str:
    """Build Gospel Library URL from scripture reference."""
    if not scripture_ref:
        return "#"
    # Simple mapping - in production use the full BOOK_PATHS from CFM skill
    import re
    # Extract book and chapter:verse
    match = re.search(r'([A-Za-z0-9\s]+)\s+(\d+):(\d+)', scripture_ref)
    if match:
        book = match.group(1).strip().lower().replace(' ', '-')
        chapter = match.group(2)
        verse = match.group(3)
        book_map = {
            'alma': 'bofm/alma',
            'moses': 'pgp/moses',
            'matthew': 'nt/matt',
            'james': 'nt/james',
            'malachi': 'ot/mal',
            '1 nephi': 'bofm/1-ne',
            '2 nephi': 'bofm/2-ne',
        }
        book_path = book_map.get(book, f'bofm/{book}')
        return f"https://www.churchofjesuschrist.org/study/scriptures/{book_path}/{chapter}?lang=eng&id=p{verse}"
    return "https://www.churchofjesuschrist.org/study/scriptures"

def build_lesson_url(cfm_data: dict) -> str:
    """Build Come Follow Me lesson URL."""
    volume = cfm_data.get('volume_year', '').lower().replace(' ', '-')
    # Simplified - real implementation would use lesson number
    return f"https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-{volume}?lang=eng"

def render_cfm_mobile(cfm_data: dict, color_scheme: str = 'eq') -> str:
    """
    Render a CFM weekly lesson as mobile-optimized HTML using Apollo's template.
    
    Args:
        cfm_data: Dictionary with CFM lesson structure (see docstring)
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
        # CFM default colors (from original template)
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
        # Inject EQ colors as CSS custom properties override
        "eq_colors": colors,
        "helios_hues": hues,
        "helios_hues_dark": hues_dark,
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
    
    # Render with custom color injection
    html = template.render(**template_data)
    
    # Inject EQ color overrides into the rendered HTML
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
        # Inject before </head>
        html = html.replace('</head>', color_css + '\n</head>')
    
    return html

def render_cfm_mobile_to_file(cfm_data: dict, output_path: str, color_scheme: str = 'eq') -> Path:
    """Render CFM lesson and save to file."""
    html = render_cfm_mobile(cfm_data, color_scheme)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding='utf-8')
    return output

# Example usage
if __name__ == '__main__':
    # Test with sample data
    sample_cfm = {
        "lesson_title": "The Lord Delivers His People",
        "scripture_references": "Exodus 1–6",
        "date_range": "January 6–12, 2025",
        "volume_year": "Old Testament 2025",
        "hero_artwork": DEFAULT_HERO_ARTWORK,
        "story_summary": [
            "The children of Israel multiply in Egypt but are enslaved by a new Pharaoh who fears them.",
            "Moses is born, saved from the Nile, raised in Pharaoh's court, then flees to Midian.",
            "At the burning bush, the Lord calls Moses to deliver Israel with the promise: \"I will be with thee.\""
        ],
        "core_message": {
            "title": "God Delivers Through His Chosen Servants",
            "text": "The Lord hears His people's cries and raises up deliverers — anciently Moses, ultimately Jesus Christ — to bring them out of bondage into covenant relationship.",
            "key_verse": "Exodus 3:12"
        },
        "sections": [
            {
                "title": "God Remembers His Covenant",
                "summary": "The Lord remembers His covenant with Abraham, Isaac, and Jacob.",
                "questions": [
                    {
                        "question": "What does it mean that God \"remembered\" His covenant?",
                        "scripture_ref": "Exodus 2:24",
                        "simple_answer": "God's \"remembering\" means He is ready to act on His promises — not that He forgot.",
                        "ponder": "When have you felt God \"remember\" you in a difficult time?"
                    },
                    {
                        "question": "How does the burning bush reveal God's nature?",
                        "scripture_ref": "Exodus 3:2–6",
                        "simple_answer": "God is holy, self-existent (I AM), and condescends to call Moses personally.",
                        "ponder": "What \"holy ground\" moments have changed your direction?"
                    }
                ]
            },
            {
                "title": "Moses' Reluctance and God's Assurance",
                "summary": "Moses doubts his ability; God provides signs and Aaron as spokesman.",
                "questions": [
                    {
                        "question": "Why did Moses resist his calling?",
                        "scripture_ref": "Exodus 4:1–17",
                        "simple_answer": "Moses felt inadequate — not eloquent, not credible, not willing.",
                        "ponder": "What inadequacies do you bring to the Lord, and how does He compensate?"
                    }
                ]
            }
        ],
        "teaching_children": [
            {
                "scripture": "Exodus 3:14",
                "kid_answer": "\"I AM\" means Jesus is always with us — He never changes, never leaves.",
                "resource": "Children's Songbook: \"I Am a Child of God\""
            }
        ],
        "podcast_insights": [
            {
                "name": "followHIM",
                "guest": "Dr. Kerry Muhlestein",
                "duration": "75 min",
                "url": "https://followhim.co/old-testament-2025"
            }
        ],
        "byu_studies": [
            {
                "article": "The Burning Bush as Temple Theophany",
                "author": "Dr. Stephen Ricks",
                "insight": "The burning bush experience mirrors temple endowment patterns.",
                "url": "https://byustudies.byu.edu"
            }
        ],
        "cheat_sheet": [
            {"question": "Who did the Lord call to deliver Israel?", "answer": "Moses", "scripture": "Exodus 3:10"},
            {"question": "What was God's name revealed to Moses?", "answer": "I AM THAT I AM", "scripture": "Exodus 3:14"}
        ],
        "teaching_summary": "Help learners see that God delivers His people today just as He did anciently — through chosen servants, covenant faithfulness, and the power of Jesus Christ."
    }
    
    html = render_cfm_mobile(sample_cfm, 'eq')
    output = Path('cfm_test_output.html')
    output.write_text(html, encoding='utf-8')
    print(f"Test output written to {output.absolute()}")
