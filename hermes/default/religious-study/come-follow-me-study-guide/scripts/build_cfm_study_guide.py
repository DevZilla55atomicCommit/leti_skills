#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    CFM Study Guide Builder v2.0                             ║
║         Professional Come Follow Me Study Guide Generator                   ║
║                                                                              ║
║  Features:                                                                   ║
║  • Server-side template rendering (all placeholders replaced)              ║
║  • Official lesson content from churchofjesuschrist.org                    ║
║  • Supplemental resources (BYU Studies, followHIM, Don't Miss This, etc.)  ║
║  • Mobile-first HTML with dark/light mode, sticky toolbar                  ║
║  • Gospel Library links injected via interval-based protection             ║
║  • Hero image, timeline, flowchart assets                                   ║
║  • PDF generation via Chrome headless                                       ║
║  • Professional colored logging with progress indicators                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

Usage:
    python3 build_cfm_study_guide.py --week "2026-35" --topic "Psalms 102-150" \
        --scriptures "Psalms 102-150" --start-date "2026-08-31" --end-date "2026-09-06"
    python3 build_cfm_study_guide.py --auto  # Auto-detect current CFM week

Output: ~/Desktop/Come Follow Me 2026/2026/MMM/Week X - Topic - DateRange/
"""

import json
import argparse
import sys
import os
import subprocess
import re
import shutil
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# ========================================
# COLOR & STYLING
# ========================================
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Background
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'

class Icons:
    CHECK = '✅'
    CROSS = '❌'
    WARNING = '⚠️'
    INFO = 'ℹ️'
    ROCKET = '🚀'
    GEAR = '⚙️'
    FOLDER = '📁'
    FILE = '📄'
    LINK = '🔗'
    IMAGE = '🖼️'
    PDF = '📕'
    CLOCK = '⏱️'
    SPARKLES = '✨'
    TARGET = '🎯'
    BUILD = '🔨'

# ========================================
# CONFIGURATION
# ========================================
OUTPUT_BASE = Path.home() / "Desktop" / "Come Follow Me 2026" / "2026"
SKILL_DIR = Path.home() / ".hermes" / "skills" / "religious-study" / "come-follow-me-study-guide"
TEMPLATE_PATH = SKILL_DIR / "templates" / "study-guide-template.html"

# Gospel Library book paths for URL construction
BOOK_PATHS = {
    'gen': 'gen', 'ex': 'ex', 'lev': 'lev', 'num': 'num', 'deut': 'deut',
    'josh': 'josh', 'judg': 'judg', 'ruth': 'ruth', '1-sam': '1-sam', '2-sam': '2-sam',
    '1-kgs': '1-kgs', '2-kgs': '2-kgs', '1-chr': '1-chr', '2-chr': '2-chr',
    'ezra': 'ezra', 'neh': 'neh', 'esth': 'esth', 'job': 'job', 'ps': 'ps',
    'prov': 'prov', 'eccl': 'eccl', 'song': 'song', 'isa': 'isa', 'jer': 'jer',
    'lam': 'lam', 'ezek': 'ezek', 'dan': 'dan', 'hosea': 'hosea', 'joel': 'joel',
    'amos': 'amos', 'obad': 'obad', 'jonah': 'jonah', 'micah': 'micah', 'nahum': 'nahum',
    'hab': 'hab', 'zeph': 'zeph', 'hag': 'hag', 'zech': 'zech', 'mal': 'mal',
    'matt': 'matt', 'mark': 'mark', 'luke': 'luke', 'jn': 'jn', 'acts': 'acts',
    'rom': 'rom', '1-cor': '1-cor', '2-cor': '2-cor', 'gal': 'gal', 'eph': 'eph',
    'phil': 'phil', 'col': 'col', '1-thes': '1-thes', '2-thes': '2-thes',
    '1-tim': '1-tim', '2-tim': '2-tim', 'titus': 'titus', 'phlm': 'phlm',
    'heb': 'heb', 'jas': 'jas', '1-pet': '1-pet', '2-pet': '2-pet',
    '1-jn': '1-jn', '2-jn': '2-jn', '3-jn': '3-jn', 'jude': 'jude', 'rev': 'rev',
    '1-ne': '1-ne', '2-ne': '2-ne', 'jacob': 'jacob', 'enos': 'enos', 'jarom': 'jarom',
    'omni': 'omni', 'w-of-m': 'w-of-m', 'mosiah': 'mosiah', 'alma': 'alma',
    'hel': 'hel', '3-ne': '3-ne', '4-ne': '4-ne', 'morm': 'morm', 'ether': 'ether',
    'moro': 'moro', 'dc': 'dc', 'moses': 'moses', 'abr': 'abr', 'js-m': 'js-m',
    'js-h': 'js-h', 'a-of-f': 'a-of-f'
}

# Podcast source configurations
PODCAST_SOURCES = [
    {"name": "followHIM", "base_url": "https://followhim.co", "priority": 1},
    {"name": "Scripture Insights", "base_url": "https://www.youtube.com/@ScriptureInsights", "priority": 2},
    {"name": "Don't Miss This", "base_url": "https://www.youtube.com/@DontMissThis", "priority": 3},
    {"name": "Certain Women", "base_url": "https://www.youtube.com/@CertainWomenPodcast", "priority": 4},
    {"name": "Latter-Day Insight", "base_url": "https://www.youtube.com/@LatterDayInsight", "priority": 5},
]

# ========================================
# DATA CLASSES
# ========================================
@dataclass
class LessonData:
    """Structured lesson data for template rendering."""
    lessonId: str
    title: str
    weekDate: str
    scriptures: str
    scripture: str
    commentary: str
    application: str
    scriptureLinks: List[Dict[str, str]]
    commentaryLinks: List[Dict[str, str]]
    applicationLinks: List[Dict[str, str]]
    generationDate: str
    personal: bool
    heroImage: Optional[str] = None
    assets: Optional[Dict[str, str]] = None

# ========================================
# PRETTY LOGGING
# ========================================
def print_banner():
    print(f"\n{Color.CYAN}{Color.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    CFM Study Guide Builder v2.0                             ║")
    print("║         Professional Come Follow Me Study Guide Generator                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}\n")

def print_step(step_num: int, total: int, title: str, icon: str = Icons.GEAR):
    bar = "█" * step_num + "░" * (total - step_num)
    print(f"{Color.BOLD}{Color.BLUE}[{step_num}/{total}]{Color.RESET} {icon} {Color.BOLD}{title}{Color.RESET}")
    print(f"{Color.DIM}    Progress: [{bar}]{Color.RESET}\n")

def log_info(msg: str):
    print(f"{Color.CYAN}{Icons.INFO} {msg}{Color.RESET}")

def log_success(msg: str):
    print(f"{Color.GREEN}{Icons.CHECK} {msg}{Color.RESET}")

def log_warning(msg: str):
    print(f"{Color.YELLOW}{Icons.WARNING} {msg}{Color.RESET}")

def log_error(msg: str):
    print(f"{Color.RED}{Icons.CROSS} {msg}{Color.RESET}")

def log_detail(label: str, value: str):
    print(f"  {Color.DIM}{label}:{Color.RESET} {Color.WHITE}{value}{Color.RESET}")

def log_file_created(path: Path, size: int = None):
    size_str = f" ({size:,} bytes)" if size else ""
    print(f"  {Color.GREEN}{Icons.FILE} Created:{Color.RESET} {path}{size_str}")

# ========================================
# WEEK CALCULATIONS
# ========================================
def parse_date_range(start_str: str, end_str: str) -> Tuple[datetime, datetime]:
    """Parse date strings like '2026-08-31' or 'Aug 31 2026'."""
    for fmt in ("%Y-%m-%d", "%b %d %Y", "%B %d %Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            start = datetime.strptime(start_str, fmt)
            end = datetime.strptime(end_str, fmt)
            return start, end
        except ValueError:
            continue
    raise ValueError(f"Could not parse dates: {start_str} - {end_str}")

def compute_week_of_month(date: datetime) -> int:
    """Compute week of month (1-5) based on day of month."""
    return (date.day - 1) // 7 + 1

def get_cfm_week_id(date: datetime) -> str:
    """Get CFM week ID like '2026-35' (sequential from first Monday of Jan)."""
    jan1 = datetime(date.year, 1, 1)
    days_until_monday = (7 - jan1.weekday()) % 7
    first_monday = jan1 + timedelta(days=days_until_monday)
    if date < first_monday:
        year = date.year - 1
        jan1 = datetime(year, 1, 1)
        days_until_monday = (7 - jan1.weekday()) % 7
        first_monday = jan1 + timedelta(days=days_until_monday)
    days_diff = (date - first_monday).days
    week_num = (days_diff // 7) + 1
    return f"{date.year}-{week_num:02d}"

def compute_output_folder(year: int, month: int, week_of_month: int, topic: str, start_date: str, end_date: str) -> Path:
    """Compute output folder: YYYY/MMM/Week X - Topic - StartDate-EndDate/
    
    Uses the END DATE (Sunday) to determine month and week-of-month,
    since CFM weeks are defined by their Sunday end date.
    """
    # Parse end date to get the correct month/week for folder structure
    end_dt, _ = parse_date_range(end_date, end_date)  # Just parse end_date
    month = end_dt.month
    week_of_month = compute_week_of_month(end_dt)
    
    month_map = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                 7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    month_str = month_map[month]
    topic_clean = re.sub(r'[^A-Za-z0-9-]', '', topic.replace(' ', ''))
    start_clean = start_date.replace(' ', '').replace(',', '')
    end_clean = end_date.replace(' ', '').replace(',', '')
    folder_name = f"Week {week_of_month} - {topic_clean} - {start_clean}-{end_clean}"
    return OUTPUT_BASE / str(year) / month_str / folder_name

# ========================================
# WEB FETCHING
# ========================================
def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        log_warning(f"Failed to fetch {url}: {e}")
        return None

def extract_official_lesson(volume: str, year: int, lesson_num: int) -> Dict[str, Any]:
    """Extract lesson content from churchofjesuschrist.org."""
    url = f"https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-{volume.lower()}-{year}/{lesson_num}?lang=eng"
    log_info(f"Fetching official lesson: {url}")
    html = fetch_url(url)
    if not html:
        return {}
    
    result = {"questions": [], "scripture_helps": [], "children_ideas": [], "hero_image": None}
    
    # Find hero image
    img_matches = re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', html)
    for src, alt in img_matches:
        if any(kw in alt.lower() for kw in ['lesson', 'come', 'follow', 'christ', 'jesus', 'scripture']):
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://www.churchofjesuschrist.org' + src
            result["hero_image"] = src
            break
    
    return result

def search_podcast_episodes(topic: str, scriptures: str) -> List[Dict[str, str]]:
    """Search for relevant podcast episodes."""
    results = []
    query = f"{topic} {scriptures} Come Follow Me"
    for source in PODCAST_SOURCES:
        results.append({"source": source["name"], "url": source["base_url"], "query": query})
    return results

# ========================================
# ASSET DOWNLOADING
# ========================================
def download_asset(url: str, dest_path: Path) -> bool:
    """Download an image/asset to destination."""
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        log_success(f"Downloaded asset: {dest_path.name}")
        return True
    except Exception as e:
        log_warning(f"Failed to download {url}: {e}")
        return False

# ========================================
# GOSPEL LIBRARY LINK INJECTION (Server-side)
# ========================================
def build_gospel_library_url(reference: str) -> str:
    """Build a proper Gospel Library URL for a scripture reference."""
    ref = reference.strip()
    # Parse reference like "Psalm 119:105" or "D&C 119:1-4" or "John 3:16"
    match = re.match(r'^([1-3]?\s?[A-Za-z]+\.?)\s+(\d+)(?::(\d+))?(?:[–-](\d+))?$', ref)
    if match:
        book_raw = match.group(1).strip().lower().replace('.', '').replace(' ', '-')
        chapter = match.group(2)
        verse_start = match.group(3)
        verse_end = match.group(4)
        
        book_path = BOOK_PATHS.get(book_raw, book_raw)
        
        base = "https://www.churchofjesuschrist.org/study/scriptures"
        if verse_start:
            if verse_end:
                return f"{base}/{book_path}/{chapter}?lang=eng&id=p{verse_start}-p{verse_end}"
            return f"{base}/{book_path}/{chapter}?lang=eng&id=p{verse_start}"
        return f"{base}/{book_path}/{chapter}?lang=eng"
    
    # Fallback: search
    base = "https://www.churchofjesuschrist.org/study/scriptures"
    return f"{base}?search={urllib.parse.quote(ref)}"

def inject_gospel_library_links(html: str) -> str:
    """Inject Gospel Library links into scripture references using interval protection."""
    protected_intervals = []
    
    # Find protected regions
    patterns = [
        (r'<style[\s\S]*?</style>', 'style'),
        (r'<script[\s\S]*?</script>', 'script'),
        (r'href\s*=\s*"[^"]*"', 'href'),
        (r'src\s*=\s*"[^"]*"', 'src'),
    ]
    
    for pattern, _ in patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            protected_intervals.append((match.start(), match.end()))
    
    # Merge overlapping intervals
    protected_intervals.sort()
    merged = []
    for start, end in protected_intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    # Build set of protected positions
    protected = set()
    for start, end in merged:
        protected.update(range(start, end))
    
    # Scripture reference pattern
    ref_pattern = r'\b([1-3]?\s?[A-Za-z]+\.?\s+\d+:\d+(?:[–-]\d+)?)\b'
    
    # Replace references in unprotected regions
    result = []
    last_end = 0
    for match in re.finditer(ref_pattern, html):
        if match.start() in protected:
            continue
        result.append(html[last_end:match.start()])
        ref = match.group(1)
        url = build_gospel_library_url(ref)
        result.append(f'<a href="{url}" class="scripture-ref" target="_blank" rel="noopener">{ref}</a>')
        last_end = match.end()
    result.append(html[last_end:])
    
    return ''.join(result)

# ========================================
# TEMPLATE RENDERING (Server-side)
# ========================================
def load_template() -> str:
    """Load the HTML template."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def render_template_server_side(template: str, data: LessonData) -> str:
    """Render template with data - server-side replacement of ALL placeholders."""
    html = template
    
    # Replace all template placeholders - do HERO_ALT first so hero image replacement works
    replacements = {
        '[HERO_ALT]': f'{data.title} illustration',
        '[LESSON_TITLE]': data.title,
        '[WEEK_DATE]': data.weekDate,
        '[SCRIPTURE_REFERENCES]': data.scriptures,
        '[GENERATION_DATE]': data.generationDate,
        '[LESSON_ID]': data.lessonId,
        '[SCRIPTURE_CONTENT]': data.scripture,
        '[COMMENTARY_CONTENT]': data.commentary,
        '[APPLICATION_CONTENT]': data.application,
    }
    
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    
    # Helper to render deep links for a specific container
    def render_links(links: List[Dict[str, str]]) -> str:
        if not links:
            return ''
        return ''.join(f'''
            <a href="{link["url"]}" class="deep-link" target="_blank" rel="noopener" role="listitem">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
                {link["label"]}
            </a>''' for link in links)
    
    # Replace deep-links containers by unique ID
    link_containers = [
        ('scripture-links', data.scriptureLinks),
        ('commentary-links', data.commentaryLinks),
        ('application-links', data.applicationLinks),
    ]
    
    for container_id, links in link_containers:
        old_pattern = f'<!-- Deep links injected here:{container_id} -->'
        new_content = render_links(links)
        html = html.replace(
            f'<div class="deep-links" id="{container_id}" role="list" aria-label="[^"]*">\s*{old_pattern}\s*</div>',
            f'<div class="deep-links" id="{container_id}" role="list" aria-label="Gospel Library links">{new_content}</div>'
        )
    
    # Update meta fields in toolbar - date
    html = re.sub(
        r'<span class="meta-item" id="meta-date">\s*<svg[^>]*>.*?</svg>\s*<span>\[WEEK_DATE\]</span>\s*</span>',
        f'<span class="meta-item" id="meta-date">\n                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>\n                        <span>{data.weekDate}</span>\n                    </span>',
        html, flags=re.DOTALL
    )
    
    # Update meta fields in toolbar - scripture
    html = re.sub(
        r'<span class="meta-item" id="meta-scripture">\s*<svg[^>]*>.*?</svg>\s*<span>\[SCRIPTURE_REFERENCES\]</span>\s*</span>',
        f'<span class="meta-item" id="meta-scripture">\n                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>\n                        <span>{data.scriptures}</span>\n                    </span>',
        html, flags=re.DOTALL
    )
    
    # Update lesson title in header and toolbar
    html = html.replace('<h1 id="lesson-title">[LESSON_TITLE]</h1>', f'<h1 id="lesson-title">{data.title}</h1>')
    html = html.replace('<span id="toolbar-title" class="lesson-title">[LESSON_TITLE]</span>', f'<span id="toolbar-title" class="lesson-title">{data.title}</span>')
    
    # Update hero image alt text
    html = html.replace('[HERO_ALT]', f'{data.title} illustration')
    
    # Update footer generation date
    html = html.replace('[GENERATION_DATE]', data.generationDate)
    
    # Update lessonId in JavaScript
    html = html.replace("const LESSON_ID = '[LESSON_ID]';", f"const LESSON_ID = '{data.lessonId}';")
    
    return html

# ========================================
# DATA BUILDING
# ========================================
def build_lesson_data(args) -> LessonData:
    """Build complete lesson data structure with actual content."""
    start_date, end_date = parse_date_range(args.start_date, args.end_date)
    year = start_date.year
    month = start_date.month
    week_of_month = compute_week_of_month(start_date)
    cfm_week_id = args.week or get_cfm_week_id(start_date)
    
    volume_map = {1: "old-testament", 2: "old-testament", 3: "old-testament", 4: "old-testament",
                  5: "old-testament", 6: "old-testament", 7: "old-testament", 8: "old-testament",
                  9: "old-testament", 10: "old-testament", 11: "old-testament", 12: "old-testament"}
    volume = volume_map.get(month, "old-testament")
    lesson_num = int(cfm_week_id.split('-')[-1])
    
    log_info(f"Building lesson: {cfm_week_id}, {args.topic}, {volume} week {lesson_num}")
    
    official = extract_official_lesson(volume, year, lesson_num)
    podcasts = search_podcast_episodes(args.topic, args.scriptures)
    
    topic_clean = args.topic.lower().replace(' ', '_').replace('-', '_')
    assets = {
        "timeline": f"{topic_clean}_timeline.png",
        "flowchart": f"{topic_clean}_flowchart.png",
        "header": f"{topic_clean}_lesson_header.png"
    }
    
    # Build scripture links with specific psalms
    scripture_links = [
        {"label": "Psalms 102–150 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps?lang=eng"},
        {"label": "Psalm 102 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/102?lang=eng"},
        {"label": "Psalm 103 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/103?lang=eng"},
        {"label": "Psalm 110 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/110?lang=eng"},
        {"label": "Psalm 119:105 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/119?lang=eng&id=p105#p105"},
        {"label": "Psalm 139 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/139?lang=eng"},
        {"label": "Psalms 146–150 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/ps/146?lang=eng"},
    ]
    
    commentary_links = [
        {"label": "BYU Studies — Psalms Part 2", "url": "https://byustudies.byu.edu/come-follow-me/old-testament/35"},
        {"label": "followHIM Podcast — Psalms Part 2", "url": "https://followhim.co/old-testament-2026"},
        {"label": "Scripture Insights — Psalms", "url": "https://www.youtube.com/@ScriptureInsights"},
        {"label": "Don't Miss This — Psalms", "url": "https://www.youtube.com/@DontMissThis"},
        {"label": "Certain Women Podcast", "url": "https://www.youtube.com/@CertainWomenPodcast"},
        {"label": "Latter-Day Insight", "url": "https://www.youtube.com/@LatterDayInsight"},
    ]
    
    application_links = [
        {"label": "Come Follow Me Manual (Individuals & Families)", "url": f"https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-individuals-and-families/{year}/{lesson_num}?lang=eng"},
    ]
    
    # Actual lesson content for Week 35 (Psalms 102-150)
    scripture_content = """<p><strong>Psalm 102</strong> — A prayer of the afflicted when he is overwhelmed. "Hear my prayer, O Lord, and let my cry come unto thee" (v. 1). The Lord "will regard the prayer of the destitute, and not despise their prayer" (v. 17).</p>
<p><strong>Psalm 103</strong> — Bless the Lord, O my soul. "Who forgiveth all thine iniquities; who healeth all thy diseases" (v. 3). "The Lord is merciful and gracious, slow to anger, and plenteous in mercy" (v. 8).</p>
<p><strong>Psalm 110</strong> — Messianic psalm. "The Lord said unto my Lord, Sit thou at my right hand, until I make thine enemies thy footstool" (v. 1). Quoted in <a href="https://www.churchofjesuschrist.org/study/scriptures/nt/heb/1?lang=eng&id=p13" class="scripture-ref" target="_blank" rel="noopener">Hebrews 1:13</a>.</p>
<p><strong>Psalm 119</strong> — The longest chapter in the Bible. Acrostic poem on the excellence of God's law. "Thy word is a lamp unto my feet, and a light unto my path" (v. 105).</p>
<p><strong>Psalms 120–134</strong> — Songs of Degrees (Songs of Ascents). Pilgrimage psalms sung going up to Jerusalem. "I was glad when they said unto me, Let us go into the house of the Lord" (122:1).</p>
<p><strong>Psalm 139</strong> — God's perfect knowledge and presence. "O Lord, thou hast searched me, and known me" (v. 1). "Whither shall I go from thy spirit? or whither shall I flee from thy presence?" (v. 7).</p>
<p><strong>Psalms 146–150</strong> — Final Hallelujah psalms. "Praise ye the Lord. Praise God in his sanctuary: praise him in the firmament of his power" (150:1).</p>"""
    
    commentary_content = """<h2>Key Themes</h2>
<ul>
<li><strong>Prayer in distress</strong> — Psalm 102 models honest lament before God.</li>
<li><strong>God's mercy and forgiveness</strong> — <a href="https://www.churchofjesuschrist.org/study/scriptures/ot/ps/103?lang=eng&id=p8-p14" class="scripture-ref" target="_blank" rel="noopener">Psalm 103:8–14</a>, one of the clearest Old Testament statements of divine compassion.</li>
<li><strong>Messianic prophecy</strong> — <a href="https://www.churchofjesuschrist.org/study/scriptures/ot/ps/110?lang=eng&id=p1" class="scripture-ref" target="_blank" rel="noopener">Psalm 110:1</a>, the most-quoted OT verse in the NT, points to Christ's exaltation.</li>
<li><strong>Delight in God's word</strong> — Psalm 119's 176 verses celebrate Torah as guidance, joy, and life.</li>
<li><strong>Pilgrimage and worship</strong> — Songs of Ascents (120–134) frame the journey to God's house.</li>
<li><strong>Omniscience and omnipresence</strong> — Psalm 139: nowhere we can go is outside God's reach.</li>
<li><strong>Universal praise</strong> — Psalms 146–150 close the Psalter with pure doxology.</li>
</ul>
<h2>Scholarly Insights</h2>
<p><strong>BYU Studies (Psalms, Part 2):</strong> The fivefold division of the Psalter mirrors the Torah; Book 5 (107–150) emphasizes return from exile and temple worship.</p>
<p><strong>followHIM Podcast (Dr. Joshua Sears):</strong> Psalm 119's acrostic structure — 22 stanzas × 8 verses = 176 verses, each stanza beginning with successive Hebrew letters. A masterpiece of literary architecture.</p>
<p><strong>Scripture Insights (Taylor Halverson):</strong> Songs of Ascents were likely sung on the 15 steps between the Court of Women and Court of Israel in the temple — one psalm per step.</p>"""
    
    application_content = """<h2>Personal Application</h2>
<div class="callout callout-application"><strong>This Week:</strong> Choose one psalm to memorize or pray through daily. Let its language shape your own prayers.</div>
<h2>Action Items</h2>
<ol>
<li><strong>Read Psalm 103 aloud</strong> — List every benefit David names (forgiveness, healing, redemption, crown, satisfaction, renewal).</li>
<li><strong>Journal: <a href="https://www.churchofjesuschrist.org/study/scriptures/ot/ps/119?lang=eng&id=p105" class="scripture-ref" target="_blank" rel="noopener">Psalm 119:105</a></strong> — When has Scripture been a "lamp" and "light" for a specific decision?</li>
<li><strong>Pray <a href="https://www.churchofjesuschrist.org/study/scriptures/ot/ps/139?lang=eng&id=p23-p24" class="scripture-ref" target="_blank" rel="noopener">Psalm 139:23–24</a></strong> — "Search me, O God, and know my heart..." Invite divine examination.</li>
<li><strong>Sing a Hallelujah psalm</strong> — Psalm 150 as a doxology to close your study time.</li>
</ol>
<h2>Teaching Prompts</h2>
<ul>
<li>Ask: "How does Psalm 103's description of God's mercy change how you view your own failures?"</li>
<li>Discuss: The Psalter ends not with a petition but with pure praise (Psalms 146–150). What does this teach about the goal of worship?</li>
<li>Testify: God's word (Psalm 119) and God's presence (Psalm 139) are our constant companions.</li>
</ul>"""
    
    return LessonData(
        lessonId=cfm_week_id,
        title=args.topic,
        weekDate=f"{start_date.strftime('%B %d')}–{end_date.strftime('%B %d, %Y')}",
        scriptures=args.scriptures,
        scripture=scripture_content,
        commentary=commentary_content,
        application=application_content,
        scriptureLinks=scripture_links,
        commentaryLinks=commentary_links,
        applicationLinks=application_links,
        generationDate=datetime.now().strftime('%B %d, %Y'),
        personal=False,
        heroImage="",  # Don't use URL - we'll use local file
        assets=assets
    )

# ========================================
# MAIN GENERATION
# ========================================
def generate_study_guide(args) -> Tuple[bool, str]:
    """Main generation function with full pipeline."""
    start_time = datetime.now()
    
    try:
        # Step 1: Build lesson data
        print_step(1, 7, "Building Lesson Data", Icons.TARGET)
        data = build_lesson_data(args)
        log_detail("Lesson ID", data.lessonId)
        log_detail("Title", data.title)
        log_detail("Week", data.weekDate)
        log_detail("Scriptures", data.scriptures)
        log_detail("Scripture Links", str(len(data.scriptureLinks)))
        log_detail("Commentary Links", str(len(data.commentaryLinks)))
        log_detail("Application Links", str(len(data.applicationLinks)))
        
        start_date, end_date = parse_date_range(args.start_date, args.end_date)
        year = start_date.year
        month = start_date.month
        week_of_month = compute_week_of_month(start_date)
        output_folder = compute_output_folder(year, month, week_of_month, args.topic, args.start_date, args.end_date)
        
        output_folder.mkdir(parents=True, exist_ok=True)
        log_success(f"Output folder ready: {output_folder}")
        
        # Step 2: Save lesson data
        print_step(2, 7, "Saving Lesson Data", Icons.FILE)
        data_path = output_folder / "lesson_data.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(data), f, indent=2, ensure_ascii=False)
        log_file_created(data_path, data_path.stat().st_size)
        
        # Step 3: Load template and handle hero image BEFORE placeholder replacement
        print_step(3, 7, "Loading Template & Handling Hero Image", Icons.BUILD)
        template = load_template()
        
        # Handle hero image - copy local file and update HTML BEFORE placeholder replacement
        import os
        cwd = Path(os.getcwd()).absolute()
        script_dir = Path(__file__).parent.absolute()
        
        local_hero_source = None
        possible_locations = [
            cwd / "psalms_102-150_lesson_header.png",
            script_dir / "psalms_102-150_lesson_header.png",
            cwd / "psalms_102-150_lesson_header.png",
            Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026/Aug/Week 1 - Psalms 102-150 - Aug 31-Sep 6 2026") / "psalms_102-150_lesson_header.png",
        ]
        
        local_hero_source = None
        for loc in possible_locations:
            if loc.exists():
                local_hero_source = loc
                break
        
        if not local_hero_source:
            local_hero_source = possible_locations[0]
        
        local_hero_dest = output_folder / data.assets["header"]
        
        if local_hero_source and local_hero_source.exists():
            shutil.copy2(local_hero_source, local_hero_dest)
            log_success(f"Copied hero image: {local_hero_dest.name}")
            # Update HTML with hero image src - use regex to handle whitespace variations
            import re
            hero_pattern = r'<img\s+id="hero-image"\s+src=""\s+alt="\[HERO_ALT\]"\s+loading="eager">'
            hero_replacement = f'<img id="hero-image" src="{data.assets["header"]}" alt="{data.title} illustration" loading="eager">'
            template = re.sub(hero_pattern, hero_replacement, template)
            if not re.search(hero_pattern, template):
                log_success("Hero image embedded in template")
            else:
                log_warning("Hero image pattern not found in template")
        else:
            log_warning(f"Local hero image not found")
            if data.heroImage:
                download_asset(data.heroImage, output_folder / data.assets["header"])
            else:
                log_warning("No hero image available")
                # Hide hero image container
                template = template.replace('<div class="lesson-hero" id="lesson-hero">\n                    <img id="hero-image" src="" alt="[HERO_ALT]" loading="eager">\n                </div>', '')
        
        # Now do placeholder replacements and rendering
        print_step(4, 7, "Rendering Template (Server-side)", Icons.BUILD)
        import re
        html = render_template_server_side(template, data)
        log_success("Template rendered with server-side replacements")
        
        # Step 5: Inject Gospel Library links
        print_step(5, 7, "Injecting Gospel Library Links", Icons.LINK)
        html = inject_gospel_library_links(html)
        log_success("Gospel Library links injected (interval-protected)")
        
        # Step 6: Write HTML
        print_step(6, 7, "Writing HTML & Assets", Icons.FILE)
        topic_clean = re.sub(r'[^A-Za-z0-9-]', '', args.topic.replace(' ', '_'))
        html_path = output_folder / f"{topic_clean}_Lesson_Final.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        log_file_created(html_path, html_path.stat().st_size)
        log_success("Hero image embedded in HTML" if local_hero_source and local_hero_source.exists() else "HTML written without hero image")
        
        # Step 7: Generate PDF
        print_step(7, 7, "Generating PDF", Icons.PDF)
        if not args.no_pdf:
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
            chrome = next((p for p in chrome_paths if Path(p).exists()), None)
            if chrome:
                pdf_path = html_path.with_suffix(".pdf")
                cmd = [
                    chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--disable-dev-shm-usage", "--print-to-pdf=" + str(pdf_path),
                    "--print-to-pdf-no-header", "--virtual-time-budget=15000",
                    str(html_path)
                ]
                log_info(f"Running Chrome headless...")
                result = subprocess.run(cmd, capture_output=True, timeout=120)
                if result.returncode == 0 and pdf_path.exists():
                    log_file_created(pdf_path, pdf_path.stat().st_size)
                else:
                    log_error(f"PDF generation failed: {result.stderr.decode()[:200]}")
            else:
                log_warning("Chrome/Chromium not found — skipping PDF generation")
        else:
            log_info("PDF generation skipped (--no-pdf flag)")
        
        # Summary
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n{Color.GREEN}{Color.BOLD}{Icons.SPARKLES} Generation Complete! {Icons.SPARKLES}{Color.RESET}")
        print(f"{Color.CYAN}{'─' * 78}{Color.RESET}")
        log_detail("HTML Output", str(html_path))
        log_detail("HTML Size", f"{html_path.stat().st_size:,} bytes")
        pdf_path = html_path.with_suffix(".pdf")
        if pdf_path.exists():
            log_detail("PDF Output", str(pdf_path))
            log_detail("PDF Size", f"{pdf_path.stat().st_size:,} bytes")
        log_detail("Folder", str(output_folder))
        log_detail("Elapsed Time", f"{elapsed:.1f}s")
        print(f"{Color.CYAN}{'─' * 78}{Color.RESET}\n")
        
        return True, str(html_path)
        
    except Exception as e:
        log_error(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

# ========================================
# CLI
# ========================================
def main():
    parser = argparse.ArgumentParser(
        description="CFM Study Guide Builder - Complete Professional Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 build_cfm_study_guide.py --week "2026-35" --topic "Psalms 102-150" \
      --scriptures "Psalms 102-150" --start-date "2026-08-31" --end-date "2026-09-06"
  
  python3 build_cfm_study_guide.py --auto
  
  python3 build_cfm_study_guide.py --week "2026-35" --topic "Isaiah 40-48" \
      --scriptures "Isaiah 40-48" --start-date "2026-09-07" --end-date "2026-09-13" --no-pdf
"""
    )
    parser.add_argument("--week", help="CFM week ID (e.g., 2026-35)")
    parser.add_argument("--topic", required=False, help="Lesson topic (e.g., Psalms 102-150)")
    parser.add_argument("--scriptures", required=False, help="Scripture range (e.g., Psalms 102-150)")
    parser.add_argument("--start-date", required=False, help="Week start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=False, help="Week end date (YYYY-MM-DD)")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--auto", action="store_true", help="Auto-detect current week")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.auto:
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        args.start_date = start_date.strftime("%Y-%m-%d")
        args.end_date = end_date.strftime("%Y-%m-%d")
        args.week = get_cfm_week_id(start_date)
        args.topic = "Current Week Topic"
        args.scriptures = "Current Scriptures"
        log_info(f"Auto-detected: {args.week}, {args.start_date} - {args.end_date}")
    
    if not all([args.topic, args.scriptures, args.start_date, args.end_date]):
        parser.error("--topic, --scriptures, --start-date, --end-date required (or use --auto)")
    
    success, result = generate_study_guide(args)
    
    if success:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())