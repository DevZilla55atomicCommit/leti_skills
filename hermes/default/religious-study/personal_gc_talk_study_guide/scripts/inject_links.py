#!/usr/bin/env python3
"""
Interval-Based Gospel Library Link Injection

Adapted from come-follow-me-study-guide skill.
Safely injects clickable Gospel Library links into HTML without corrupting
CSS, JavaScript, or existing attributes.

Usage:
    python inject_links.py input.html output.html --refs talk_refs.json
    python inject_links.py input.html output.html --inline "Alma 5:12" "Malachi 3:10"
"""

import json
import re
import sys
import argparse
from typing import Dict, Tuple, Optional, List, Set
from pathlib import Path


# =============================================================================
# CONFIGURATION
# =============================================================================

# Book path map for Gospel Library URLs
BOOK_PATHS = {
    # Old Testament
    'genesis': 'genesis', 'exodus': 'exodus', 'leviticus': 'leviticus', 'numbers': 'numbers',
    'deuteronomy': 'deuteronomy', 'joshua': 'joshua', 'judges': 'judges', 'ruth': 'ruth',
    '1 samuel': '1-samuel', '2 samuel': '2-samuel', '1 kings': '1-kings', '2 kings': '2-kings',
    '1 chronicles': '1-chronicles', '2 chronicles': '2-chronicles', 'ezra': 'ezra', 'nehemiah': 'nehemiah',
    'esther': 'esther', 'job': 'job', 'psalms': 'psalms', 'proverbs': 'proverbs',
    'ecclesiastes': 'ecclesiastes', 'song of solomon': 'song-of-solomon', 'isaiah': 'isaiah',
    'jeremiah': 'jeremiah', 'lamentations': 'lamentations', 'ezekiel': 'ezekiel', 'daniel': 'daniel',
    'hosea': 'hosea', 'joel': 'joel', 'amos': 'amos', 'obadiah': 'obadiah',
    'jonah': 'jonah', 'micah': 'micah', 'nahum': 'nahum', 'habakkuk': 'habakkuk',
    'zephaniah': 'zephaniah', 'haggai': 'haggai', 'zechariah': 'zechariah', 'malachi': 'malachi',
    
    # New Testament - Use full book names (not abbreviations)
    'matthew': 'matthew', 'mark': 'mark', 'luke': 'luke', 'john': 'john',
    'acts': 'acts', 'romans': 'romans', '1 corinthians': '1-corinthians', '2 corinthians': '2-corinthians',
    'galatians': 'galatians', 'ephesians': 'ephesians', 'philippians': 'philippians', 'colossians': 'colossians',
    '1 thessalonians': '1-thessalonians', '2 thessalonians': '2-thessalonians', '1 timothy': '1-timothy',
    '2 timothy': '2-timothy', 'titus': 'titus', 'philemon': 'philemon', 'hebrews': 'hebrews',
    'james': 'james', '1 peter': '1-peter', '2 peter': '2-peter', '1 john': '1-john',
    '2 john': '2-john', '3 john': '3-john', 'jude': 'jude', 'revelation': 'revelation',
    
    # Book of Mormon
    '1 nephi': '1-ne', '2 nephi': '2-ne', 'jacob': 'jacob', 'enos': 'enos',
    'jarom': 'jarom', 'omni': 'omni', 'words of mormon': 'w-of-m',
    'mosiah': 'mosiah', 'alma': 'alma', 'helaman': 'hel', '3 nephi': '3-ne',
    '4 nephi': '4-ne', 'mormon': 'morm', 'ether': 'ether', 'moroni': 'moro',
    
    # Doctrine and Covenants
    'doctrine and covenants': 'dc',
    
    # Pearl of Great Price
    'moses': 'moses', 'abraham': 'abraham', 'joseph smith—matthew': 'js-m', 'joseph smith—history': 'js-h',
}

# Valid book keys that should be linked
VALID_BOOKS = set(BOOK_PATHS.keys())

# Standard work for URL construction
BOOK_TO_WORK = {
    **{k: 'ot' for k in ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth',
                         '1 samuel', '2 samuel', '1 kings', '2 kings', '1 chronicles', '2 chronicles', 'ezra',
                         'nehemiah', 'esther', 'job', 'psalms', 'proverbs', 'ecclesiastes', 'song of solomon',
                         'isaiah', 'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos',
                         'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi']},
    **{k: 'nt' for k in ['matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1 corinthians', '2 corinthians',
                         'galatians', 'ephesians', 'philippians', 'colossians', '1 thessalonians', '2 thessalonians',
                         '1 timothy', '2 timothy', 'titus', 'philemon', 'hebrews', 'james', '1 peter', '2 peter',
                         '1 john', '2 john', '3 john', 'jude', 'revelation']},
    **{k: 'bofm' for k in ['1 nephi', '2 nephi', 'jacob', 'enos', 'jarom', 'omni', 'words of mormon',
                           'mosiah', 'alma', 'helaman', '3 nephi', '4 nephi', 'mormon', 'ether', 'moroni']},
    'doctrine and covenants': 'dc',
    **{k: 'pgp' for k in ['moses', 'abraham', 'joseph smith—matthew', 'joseph smith—history']},
}


# Default scripture references to link (can be extended from talk data)
DEFAULT_SCRIPTURE_REFS = {
    # From Elder Becerra talk
    'Alma 5:12': ('alma', 5, 12),
    'Alma 7:3': ('alma', 7, 3),
    'Alma 7:18': ('alma', 7, 18),
    'James 1:8': ('james', 1, 8),
    'Matthew 6:33': ('matthew', 6, 33),
    'Moses 5:5': ('moses', 5, 5),
    'Moses 5:6': ('moses', 5, 6),
    'Moses 5:7': ('moses', 5, 7),
    'Moses 5:9': ('moses', 5, 9),
    'Malachi 3:10': ('malachi', 3, 10),
    'Malachi 3:11': ('malachi', 3, 11),
    'Malachi 3:12': ('malachi', 3, 12),
    '3 Nephi 24:10': ('3 nephi', 24, 10),
    'D&C 119:4': ('doctrine and covenants', 119, 4),
    'D&C 119:5': ('doctrine and covenants', 119, 5),
    'D&C 119:6': ('doctrine and covenants', 119, 6),
    'Genesis 14:20': ('genesis', 14, 20),
    'Hebrews 7:2': ('hebrews', 7, 2),
    'D&C 88:67': ('doctrine and covenants', 88, 67),
    'D&C 88:68': ('doctrine and covenants', 88, 68),
    'Helaman 3:35': ('helaman', 3, 35),
}


def make_gospel_library_url(book_key: str, chapter: int, verse: Optional[str] = None, lang: str = "ton") -> Optional[str]:
    """Build a Gospel Library URL for a scripture reference."""
    book_lower = book_key.lower()
    if book_lower not in BOOK_PATHS:
        return None
    
    path = BOOK_PATHS[book_lower]
    work = BOOK_TO_WORK.get(book_lower, 'ot')
    
    if verse:
        return f"https://www.churchofjesuschrist.org/study/scriptures/{work}/{path}/{chapter}?lang={lang}&id={verse}"
    else:
        return f"https://www.churchofjesuschrist.org/study/scriptures/{work}/{path}/{chapter}?lang={lang}"


def find_protected_intervals(html: str) -> List[Tuple[int, int]]:
    """
    Find all intervals in the HTML that should be protected from replacement.
    Returns list of (start, end) tuples, merged and non-overlapping.
    """
    intervals = []
    
    # Style blocks
    for match in re.finditer(r'<style[^>]*>.*?</style>', html, flags=re.DOTALL | re.IGNORECASE):
        intervals.append((match.start(), match.end()))
    
    # Script blocks
    for match in re.finditer(r'<script[^>]*>.*?</script>', html, flags=re.DOTALL | re.IGNORECASE):
        intervals.append((match.start(), match.end()))
    
    # href attributes
    for match in re.finditer(r'href\s*=\s*"[^"]*"', html):
        intervals.append((match.start(), match.end()))
    for match in re.finditer(r"href\s*=\s*'[^']*'", html):
        intervals.append((match.start(), match.end()))
    
    # src attributes
    for match in re.finditer(r'src\s*=\s*"[^"]*"', html):
        intervals.append((match.start(), match.end()))
    for match in re.finditer(r"src\s*=\s*'[^']*'", html):
        intervals.append((match.start(), match.end()))
    
    # data-* attributes that might contain scripture-like text
    for match in re.finditer(r'data-[a-z-]+\s*=\s*"[^"]*"', html):
        intervals.append((match.start(), match.end()))
    for match in re.finditer(r"data-[a-z-]+\s*=\s*'[^']*'", html):
        intervals.append((match.start(), match.end()))
    
    # Merge overlapping intervals
    if not intervals:
        return []
    
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    return merged


def is_in_protected_region(pos: int, protected_intervals: List[Tuple[int, int]]) -> bool:
    """Check if a position falls within any protected interval."""
    for start, end in protected_intervals:
        if start <= pos < end:
            return True
    return False


def process_free_text(text: str, scripture_refs: Dict[str, Tuple[str, int, Optional[str]]]) -> str:
    """Process a free text region, replacing scripture references with links."""
    result = text
    
    # Sort refs by length descending to avoid partial matches
    sorted_refs = sorted(scripture_refs.items(), key=lambda x: -len(x[0]))
    
    for ref_text, (book_key, chapter, verse) in sorted_refs:
        if book_key.lower() not in VALID_BOOKS:
            continue
        
        url = make_gospel_library_url(book_key, chapter, verse)
        if not url:
            continue
        
        replacement = f'<a href="{url}" target="_blank" class="scripture-link" style="color: #B8860B; text-decoration: underline;">{ref_text}</a>'
        pattern = rf'(?<![\w\\"])({re.escape(ref_text)})(?![\w\\"])'
        result = re.sub(pattern, replacement, result)
    
    return result


def inject_links(html: str, scripture_refs: Dict[str, Tuple[str, int, Optional[str]]] = None) -> str:
    """
    Main entry point: inject Gospel Library links into HTML.
    Uses interval-based protection to avoid corrupting CSS/JS/attributes.
    """
    if scripture_refs is None:
        scripture_refs = DEFAULT_SCRIPTURE_REFS
    
    # Find protected intervals
    protected_intervals = find_protected_intervals(html)
    
    # Build result by iterating through protected intervals
    result_parts = []
    last_pos = 0
    
    for start, end in protected_intervals:
        # Process free region before this protected interval
        if start > last_pos:
            free_text = html[last_pos:start]
            processed = process_free_text(free_text, scripture_refs)
            result_parts.append(processed)
        
        # Add protected region as-is
        result_parts.append(html[start:end])
        last_pos = end
    
    # Process final free region
    if last_pos < len(html):
        free_text = html[last_pos:]
        processed = process_free_text(free_text, scripture_refs)
        result_parts.append(processed)
    
    return ''.join(result_parts)


def load_refs_from_json(json_path: str) -> Dict[str, Tuple[str, int, Optional[str]]]:
    """Load scripture references from a JSON file (output of discover.py)."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    refs = {}
    for item in data.get('scripture_chain', []):
        ref = item.get('reference', '')
        book = item.get('book', '').lower()
        chapter = item.get('chapter', 0)
        verse = item.get('verse')
        
        if ref and book and chapter:
            refs[ref] = (book, chapter, verse)
    
    return refs


def main():
    parser = argparse.ArgumentParser(description='Inject Gospel Library links into HTML')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('output', help='Output HTML file')
    parser.add_argument('--refs', help='JSON file with scripture references (from discover.py)')
    parser.add_argument('--inline', nargs='+', help='Inline scripture references to add')
    
    args = parser.parse_args()
    
    try:
        # Load base references
        scripture_refs = DEFAULT_SCRIPTURE_REFS.copy()
        
        # Load from JSON if provided
        if args.refs:
            extra_refs = load_refs_from_json(args.refs)
            scripture_refs.update(extra_refs)
        
        # Add inline references
        if args.inline:
            for ref in args.inline:
                # Try to parse: "Book Chapter:Verse"
                match = re.match(r'^([1-3]?\s?[A-Za-z\s]+)\.?\s+(\d+):(\d+(?:[–-]\d+)?)$', ref.strip())
                if match:
                    book_raw = match.group(1).strip().lower()
                    chapter = int(match.group(2))
                    verse = match.group(3)
                    
                    # Normalize book name
                    book_aliases = {
                        'alma': 'alma', 'matthew': 'matt', 'matt': 'matt',
                        'james': 'jas', 'malachi': 'mal', 'moses': 'moses',
                        '3 nephi': '3-ne', 'dc': 'dc', 'd&c': 'dc',
                        'genesis': 'gen', 'hebrews': 'heb', 'helaman': 'hel',
                    }
                    book_key = book_aliases.get(book_raw, book_raw)
                    scripture_refs[ref] = (book_key, chapter, verse)
        
        # Read input HTML
        with open(args.input, 'r') as f:
            html = f.read()
        
        # Inject links
        result = inject_links(html, scripture_refs)
        
        # Write output
        with open(args.output, 'w') as f:
            f.write(result)
        
        print(f"Processed {args.input} -> {args.output}")
        print(f"Injected {len(scripture_refs)} scripture references")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()