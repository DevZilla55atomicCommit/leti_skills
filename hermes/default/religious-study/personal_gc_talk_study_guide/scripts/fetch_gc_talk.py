#!/usr/bin/env python3
"""
Fetch General Conference Talk from churchofjesuschrist.org

Uses Playwright to handle JS-rendered pages. Extracts:
- Full talk text
- Speaker metadata (name, calling, bio)
- Conference session, date
- All scripture references (inline + footnotes)
- Talk structure (paragraphs, sections)

Usage:
    python fetch_gc_talk.py --url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng" --output talk.json
"""

import json
import re
import sys
import argparse
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
    sys.exit(1)


@dataclass
class ScriptureReference:
    reference: str
    book: str
    chapter: int
    verse: Optional[str] = None
    context: str = ""
    is_footnote: bool = False
    footnote_id: Optional[str] = None


@dataclass
class TalkSection:
    title: str
    content: str
    paragraphs: List[str] = field(default_factory=list)
    scriptures: List[ScriptureReference] = field(default_factory=list)


@dataclass
class GCTalk:
    url: str
    title: str = ""
    speaker: str = ""
    speaker_calling: Optional[str] = None
    speaker_bio: Optional[str] = None
    conference: str = ""
    session: str = ""
    date: str = ""
    speaker_photo: Optional[str] = None
    full_text: str = ""
    sections: List[TalkSection] = field(default_factory=list)
    all_scriptures: List[ScriptureReference] = field(default_factory=list)
    key_quotes: List[str] = field(default_factory=list)


# Scripture reference regex patterns
SCRIPTURE_PATTERNS = [
    # Standard: "Book Chapter:Verse" or "Book Chapter:Verse-Verse"
    r'\b([1-3]\s?[A-Za-z]+\.?\s+\d+:\d+(?:[–-]\d+)?)\b',
    # "Chapter Verse" without book (context-dependent)
    r'\b([A-Za-z]+\s+\d+:\d+(?:[–-]\d+)?)\b',
    # Footnote references: "footnote a", "fn. 3"
    r'(?:footnote|fn\.?)\s*([a-z])',
]

# Book name normalization
BOOK_ALIASES = {
    'gen': 'Genesis', 'gen.': 'Genesis', 'genesis': 'Genesis',
    'ex': 'Exodus', 'ex.': 'Exodus', 'exod': 'Exodus', 'exodus': 'Exodus',
    'lev': 'Leviticus', 'lev.': 'Leviticus', 'leviticus': 'Leviticus',
    'num': 'Numbers', 'num.': 'Numbers', 'numbers': 'Numbers',
    'deut': 'Deuteronomy', 'deut.': 'Deuteronomy', 'deuteronomy': 'Deuteronomy',
    'josh': 'Joshua', 'josh.': 'Joshua', 'joshua': 'Joshua',
    'judg': 'Judges', 'judg.': 'Judges', 'judges': 'Judges',
    'ruth': 'Ruth',
    '1 sam': '1 Samuel', '1 sam.': '1 Samuel', '1 samuel': '1 Samuel',
    '2 sam': '2 Samuel', '2 sam.': '2 Samuel', '2 samuel': '2 Samuel',
    '1 kgs': '1 Kings', '1 kgs.': '1 Kings', '1 kings': '1 Kings',
    '2 kgs': '2 Kings', '2 kgs.': '2 Kings', '2 kings': '2 Kings',
    '1 chr': '1 Chronicles', '1 chr.': '1 Chronicles', '1 chronicles': '1 Chronicles',
    '2 chr': '2 Chronicles', '2 chr.': '2 Chronicles', '2 chronicles': '2 Chronicles',
    'ezra': 'Ezra', 'neh': 'Nehemiah', 'neh.': 'Nehemiah', 'nehemiah': 'Nehemiah',
    'esth': 'Esther', 'esth.': 'Esther', 'esther': 'Esther',
    'job': 'Job',
    'ps': 'Psalms', 'ps.': 'Psalms', 'psalm': 'Psalms', 'psalms': 'Psalms',
    'prov': 'Proverbs', 'prov.': 'Proverbs', 'proverbs': 'Proverbs',
    'eccl': 'Ecclesiastes', 'eccl.': 'Ecclesiastes', 'ecclesiastes': 'Ecclesiastes',
    'song': 'Song of Solomon', 'song of solomon': 'Song of Solomon',
    'isa': 'Isaiah', 'isa.': 'Isaiah', 'isaiah': 'Isaiah',
    'jer': 'Jeremiah', 'jer.': 'Jeremiah', 'jeremiah': 'Jeremiah',
    'lam': 'Lamentations', 'lam.': 'Lamentations', 'lamentations': 'Lamentations',
    'ezek': 'Ezekiel', 'ezek.': 'Ezekiel', 'ezekiel': 'Ezekiel',
    'dan': 'Daniel', 'dan.': 'Daniel', 'daniel': 'Daniel',
    'hosea': 'Hosea', 'joel': 'Joel', 'amos': 'Amos', 'obad': 'Obadiah', 'obad.': 'Obadiah', 'obadiah': 'Obadiah',
    'jonah': 'Jonah', 'micah': 'Micah', 'nahum': 'Nahum', 'hab': 'Habakkuk', 'hab.': 'Habakkuk', 'habakkuk': 'Habakkuk',
    'zeph': 'Zephaniah', 'zeph.': 'Zephaniah', 'zephaniah': 'Zephaniah',
    'hag': 'Haggai', 'hag.': 'Haggai', 'haggai': 'Haggai',
    'zech': 'Zechariah', 'zech.': 'Zechariah', 'zechariah': 'Zechariah',
    'mal': 'Malachi', 'mal.': 'Malachi', 'malachi': 'Malachi',
    'matt': 'Matthew', 'matt.': 'Matthew', 'mt': 'Matthew', 'mt.': 'Matthew', 'matthew': 'Matthew',
    'mark': 'Mark', 'mk': 'Mark', 'mk.': 'Mark',
    'luke': 'Luke', 'lk': 'Luke', 'lk.': 'Luke',
    'john': 'John', 'jn': 'John', 'jn.': 'John',
    'acts': 'Acts', 'acts.': 'Acts',
    'rom': 'Romans', 'rom.': 'Romans', 'romans': 'Romans',
    '1 cor': '1 Corinthians', '1 cor.': '1 Corinthians', '1 corinthians': '1 Corinthians',
    '2 cor': '2 Corinthians', '2 cor.': '2 Corinthians', '2 corinthians': '2 Corinthians',
    'gal': 'Galatians', 'gal.': 'Galatians', 'galatians': 'Galatians',
    'eph': 'Ephesians', 'eph.': 'Ephesians', 'ephesians': 'Ephesians',
    'phil': 'Philippians', 'phil.': 'Philippians', 'philippians': 'Philippians',
    'col': 'Colossians', 'col.': 'Colossians', 'colossians': 'Colossians',
    '1 thess': '1 Thessalonians', '1 thess.': '1 Thessalonians', '1 thessalonians': '1 Thessalonians',
    '2 thess': '2 Thessalonians', '2 thess.': '2 Thessalonians', '2 thessalonians': '2 Thessalonians',
    '1 tim': '1 Timothy', '1 tim.': '1 Timothy', '1 timothy': '1 Timothy',
    '2 tim': '2 Timothy', '2 tim.': '2 Timothy', '2 timothy': '2 Timothy',
    'titus': 'Titus', 'phlm': 'Philemon', 'phlm.': 'Philemon', 'philemon': 'Philemon',
    'heb': 'Hebrews', 'heb.': 'Hebrews', 'hebrews': 'Hebrews',
    'james': 'James', 'jas': 'James', 'jas.': 'James',
    '1 pet': '1 Peter', '1 pet.': '1 Peter', '1 peter': '1 Peter',
    '2 pet': '2 Peter', '2 pet.': '2 Peter', '2 peter': '2 Peter',
    '1 jn': '1 John', '1 jn.': '1 John', '1 john': '1 John',
    '2 jn': '2 John', '2 jn.': '2 John', '2 john': '2 John',
    '3 jn': '3 John', '3 jn.': '3 John', '3 john': '3 John',
    'jude': 'Jude',
    'rev': 'Revelation', 'rev.': 'Revelation', 'revelation': 'Revelation',
    '1 ne': '1 Nephi', '1 ne.': '1 Nephi', '1 nephi': '1 Nephi',
    '2 ne': '2 Nephi', '2 ne.': '2 Nephi', '2 nephi': '2 Nephi',
    'jacob': 'Jacob', 'enos': 'Enos', 'jarom': 'Jarom', 'omni': 'Omni',
    'w of m': 'Words of Mormon', 'words of mormon': 'Words of Mormon',
    'mosiah': 'Mosiah', 'alma': 'Alma', 'hel': 'Helaman', 'hel.': 'Helaman', 'helaman': 'Helaman',
    '3 ne': '3 Nephi', '3 ne.': '3 Nephi', '3 nephi': '3 Nephi',
    '4 ne': '4 Nephi', '4 ne.': '4 Nephi', '4 nephi': '4 Nephi',
    'morm': 'Mormon', 'morm.': 'Mormon', 'mormon': 'Mormon',
    'ether': 'Ether', 'moro': 'Moroni', 'moro.': 'Moroni', 'moroni': 'Moroni',
    'dc': 'Doctrine and Covenants', 'd&c': 'Doctrine and Covenants', 'd and c': 'Doctrine and Covenants', 'doctrine and covenants': 'Doctrine and Covenants',
    'moses': 'Moses', 'abr': 'Abraham', 'abr.': 'Abraham', 'abraham': 'Abraham',
    'js-m': 'Joseph Smith—Matthew', 'js-h': 'Joseph Smith—History', 'js-matthew': 'Joseph Smith—Matthew', 'js-history': 'Joseph Smith—History',
}

BOOK_TO_STANDARD_WORK = {
    **{k: 'Old Testament' for k in [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
        '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
        'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
        'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
        'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'
    ]},
    **{k: 'New Testament' for k in [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
        '1 John', '2 John', '3 John', 'Jude', 'Revelation'
    ]},
    **{k: 'Book of Mormon' for k in [
        '1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Words of Mormon',
        'Mosiah', 'Alma', 'Helaman', '3 Nephi', '4 Nephi', 'Mormon', 'Ether', 'Moroni'
    ]},
    **{k: 'Doctrine and Covenants' for k in ['Doctrine and Covenants']},
    **{k: 'Pearl of Great Price' for k in ['Moses', 'Abraham', 'Joseph Smith—Matthew', 'Joseph Smith—History']},
}


def normalize_book_name(book: str) -> str:
    """Normalize book name to standard form."""
    key = book.lower().strip().rstrip('.')
    return BOOK_ALIASES.get(key, book)


def parse_scripture_ref(ref: str) -> Optional[ScriptureReference]:
    """Parse a scripture reference string into components."""
    # Pattern: "Book Chapter:Verse" or "Book Chapter:Verse-Verse"
    match = re.match(r'^([1-3]?\s?[A-Za-z\s]+)\.?\s+(\d+):(\d+(?:[–-]\d+)?)$', ref.strip())
    if not match:
        return None
    
    book_raw = match.group(1).strip()
    chapter = int(match.group(2))
    verse = match.group(3)
    
    book = normalize_book_name(book_raw)
    
    return ScriptureReference(
        reference=ref.strip(),
        book=book,
        chapter=chapter,
        verse=verse,
    )


def extract_scriptures_from_text(text: str, context: str = "", is_footnote: bool = False) -> List[ScriptureReference]:
    """Extract all scripture references from text."""
    scriptures = []
    
    # Pattern 1: "Book Chapter:Verse" with optional verse range
    pattern1 = re.compile(r'\b([1-3]?\s?[A-Za-z][A-Za-z\s]*\.?\s+\d+:\d+(?:[–-]\d+)?)\b')
    for match in pattern1.finditer(text):
        ref = match.group(1)
        parsed = parse_scripture_ref(ref)
        if parsed:
            parsed.context = context[:200] if context else text[max(0, match.start()-50):match.end()+50]
            parsed.is_footnote = is_footnote
            scriptures.append(parsed)
    
    return scriptures


def fetch_gc_talk(url: str) -> GCTalk:
    """Fetch a General Conference talk using Playwright."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to {url}...")
        # Try with domcontentloaded first, then wait for content
        page.goto(url, wait_until='domcontentloaded', timeout=90000)
        
        # Wait for content to load with multiple selector attempts
        content_loaded = False
        for selector in ['main', 'article', '.body-block', '.article-body', '.content', '#main-content']:
            try:
                page.wait_for_selector(selector, timeout=15000)
                content_loaded = True
                print(f"Content loaded via selector: {selector}")
                break
            except:
                continue
        
        if not content_loaded:
            print("Warning: Could not find standard content selectors, proceeding anyway...")
        
        page.wait_for_timeout(5000)  # Extra wait for dynamic content
        
        # Get page content
        html = page.content()
        
        # Extract using page evaluation for better accuracy
        talk_data = page.evaluate("""
            () => {
                // Title
                const titleEl = document.querySelector('h1.title, h1.chapter-title, h1[itemprop="name"], .article-title');
                const title = titleEl ? titleEl.textContent.trim() : '';
                
                // Speaker
                const speakerEl = document.querySelector('.author-name, .byline-author, [itemprop="author"]');
                const speaker = speakerEl ? speakerEl.textContent.trim() : '';
                
                // Speaker calling
                const callingEl = document.querySelector('.author-calling, .byline-calling');
                const speaker_calling = callingEl ? callingEl.textContent.trim() : null;
                
                // Conference/Session/Date
                const metaEl = document.querySelector('.article-meta, .conference-meta, .byline-meta');
                const meta = metaEl ? metaEl.textContent.trim() : '';
                
                // Full text content
                const contentEl = document.querySelector('.body-block, .article-body, main article, .content');
                const fullText = contentEl ? contentEl.innerText : document.body.innerText;
                
                // Speaker photo
                const photoEl = document.querySelector('.author-photo img, .speaker-photo img');
                const speaker_photo = photoEl ? photoEl.src : null;
                
                // Extract sections (h2, h3 headers with following content)
                const sections = [];
                const headers = document.querySelectorAll('h2, h3');
                headers.forEach(h => {
                    const sectionTitle = h.textContent.trim();
                    let content = '';
                    let next = h.nextElementSibling;
                    while (next && !['H2', 'H3'].includes(next.tagName)) {
                        if (next.tagName === 'P') {
                            content += next.innerText + '\\n\\n';
                        }
                        next = next.nextElementSibling;
                    }
                    if (content.trim()) {
                        sections.push({ title: sectionTitle, content: content.trim() });
                    }
                });
                
                // Footnotes
                const footnotes = [];
                document.querySelectorAll('.footnote, .fn, sup a[href^="#fn"]').forEach(fn => {
                    const id = fn.id || fn.getAttribute('href')?.replace('#', '');
                    const text = fn.textContent.trim();
                    if (text) footnotes.push({ id, text });
                });
                
                return {
                    title, speaker, speaker_calling, meta, fullText, speaker_photo,
                    sections, footnotes
                };
            }
        """)
        
        browser.close()
    
    # Parse metadata
    talk = GCTalk(url=url)
    talk.title = talk_data['title']
    talk.speaker = talk_data['speaker']
    talk.speaker_calling = talk_data['speaker_calling']
    talk.speaker_photo = talk_data['speaker_photo']
    talk.full_text = talk_data['fullText']
    
    # Parse conference, session, date from meta
    meta = talk_data['meta']
    if meta:
        # Pattern: "April 2026 General Conference • Saturday Morning Session"
        conf_match = re.search(r'(\w+\s+\d{4})\s+General Conference', meta)
        if conf_match:
            talk.conference = conf_match.group(1) + " General Conference"
        
        session_match = re.search(r'(Saturday Morning|Saturday Afternoon|Sunday Morning|Sunday Afternoon) Session', meta)
        if session_match:
            talk.session = session_match.group(1) + " Session"
        
        date_match = re.search(r'(\w+\s+\d{1,2},?\s+\d{4})', meta)
        if date_match:
            talk.date = date_match.group(1)
    
    # Parse sections
    for sec in talk_data['sections']:
        section = TalkSection(title=sec['title'], content=sec['content'])
        # Extract scriptures from this section
        section.scriptures = extract_scriptures_from_text(sec['content'], sec['content'][:200])
        talk.sections.append(section)
    
    # Extract all scriptures from full text
    talk.all_scriptures = extract_scriptures_from_text(talk.full_text, "")
    
    # Add footnote scriptures
    for fn in talk_data['footnotes']:
        fn_scriptures = extract_scriptures_from_text(fn['text'], fn['text'], is_footnote=True)
        for s in fn_scriptures:
            s.footnote_id = fn['id']
        talk.all_scriptures.extend(fn_scriptures)
    
    # Deduplicate scriptures
    seen = set()
    unique_scriptures = []
    for s in talk.all_scriptures:
        key = (s.book, s.chapter, s.verse, s.is_footnote)
        if key not in seen:
            seen.add(key)
            unique_scriptures.append(s)
    talk.all_scriptures = unique_scriptures
    
    # Extract key quotes (sentences with doctrinal weight indicators)
    sentences = re.split(r'(?<=[.!?])\s+', talk.full_text)
    doctrinal_keywords = ['tithing', 'consecration', 'firstlings', 'double-minded', 'windows of heaven', 
                          'spiritual capacity', 'put God first', 'firstlings of the flock', 'Adam',
                          'sacrifice', 'obedience', 'blessing', 'covenant', 'law of tithing']
    for sent in sentences:
        if len(sent) > 50 and len(sent) < 500:
            if any(kw in sent.lower() for kw in doctrinal_keywords):
                talk.key_quotes.append(sent.strip())
    
    # Limit quotes
    talk.key_quotes = talk.key_quotes[:10]
    
    return talk


def main():
    parser = argparse.ArgumentParser(description='Fetch General Conference talk')
    parser.add_argument('--url', required=True, help='Talk URL')
    parser.add_argument('--output', '-o', help='Output JSON file')
    parser.add_argument('--json', action='store_true', help='Print JSON to stdout')
    
    args = parser.parse_args()
    
    try:
        talk = fetch_gc_talk(args.url)
        
        # Convert to dict
        talk_dict = asdict(talk)
        # Convert scripture objects
        talk_dict['all_scriptures'] = [asdict(s) for s in talk.all_scriptures]
        talk_dict['sections'] = [
            {**asdict(s), 'scriptures': [asdict(sc) for sc in s.scriptures]}
            for s in talk.sections
        ]
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(talk_dict, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")
        
        if args.json or not args.output:
            print(json.dumps(talk_dict, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()