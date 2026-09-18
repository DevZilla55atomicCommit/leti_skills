#!/usr/bin/env python3
"""
Interval-based Gospel Library Link Injection Script

This script safely injects clickable Gospel Library links into HTML study guides
without corrupting CSS, JavaScript, or existing attributes.

Usage:
    python inject-gospel-library-links.py input.html output.html

Or import as module:
    from inject_gospel_library_links import inject_links
    inject_links(html_string, scripture_refs, book_paths)
"""

import re
from typing import Dict, Tuple, Optional, List, Set

# =============================================================================
# CONFIGURATION
# =============================================================================

# Valid book keys that should be linked
VALID_BOOKS = {
    'job', 'ps', 'gen', 'isa', 'matt', 'luke', 'jn', 'acts', 'rom', '1-jn',
    'rev', '2-ne', 'mosiah', 'alma', 'ether', 'dc', 'moses', 'abr', 'zech',
}

# Book path map for Gospel Library URLs
BOOK_PATHS = {
    'job': 'job', 'ps': 'ps', 'gen': 'gen', 'isa': 'isa', 'matt': 'matt',
    'luke': 'luke', 'jn': 'jn', 'acts': 'acts', 'rom': 'rom', '1-jn': '1-jn',
    'rev': 'rev', '2-ne': '2-ne', 'mosiah': 'mosiah', 'alma': 'alma',
    'ether': 'ether', 'dc': 'dc', 'moses': 'moses', 'abr': 'abr', 'zech': 'zech',
}

# Scripture references to link: exact_string -> (book_key, chapter, verse)
# verse can be None (chapter only), string (single verse), or range string "1-3"
SCRIPTURE_REFS = {
    # Job
    'Job 1:1': ('job', 1, 1),
    'Job 1:8': ('job', 1, 8),
    'Job 1:9–11': ('job', 1, '9–11'),
    'Job 1:11': ('job', 1, 11),
    'Job 1:12': ('job', 1, 12),
    'Job 1:14–15': ('job', 1, '14–15'),
    'Job 1:16': ('job', 1, 16),
    'Job 1:17': ('job', 1, 17),
    'Job 1:18–19': ('job', 1, '18–19'),
    'Job 1:20–22': ('job', 1, '20–22'),
    'Job 1:21': ('job', 1, 21),
    'Job 2:3': ('job', 2, 3),
    'Job 2:4–5': ('job', 2, '4–5'),
    'Job 2:6': ('job', 2, 6),
    'Job 2:7': ('job', 2, 7),
    'Job 2:8': ('job', 2, 8),
    'Job 2:9–10': ('job', 2, '9–10'),
    'Job 2:10': ('job', 2, 10),
    'Job 3': ('job', 3, None),
    'Job 4–5': ('job', '4-5', None),
    'Job 4:7–8': ('job', 4, '7–8'),
    'Job 8': ('job', 8, None),
    'Job 8:4–6': ('job', 8, '4–6'),
    'Job 11': ('job', 11, None),
    'Job 11:13–15': ('job', 11, '13–15'),
    'Job 12:10': ('job', 12, 10),
    'Job 12:13': ('job', 12, 13),
    'Job 12:16': ('job', 12, 16),
    'Job 13:15': ('job', 13, 15),
    'Job 13:33': ('job', 13, 33),
    'Job 16:19': ('job', 16, 19),
    'Job 19:23–27': ('job', 19, '23–27'),
    'Job 19:25': ('job', 19, 25),
    'Job 19:25–27': ('job', 19, '25–27'),
    'Job 23:3–7': ('job', 23, '3–7'),
    'Job 28': ('job', 28, None),
    'Job 38:4': ('job', 38, 4),
    'Job 38:7': ('job', 38, 7),
    'Job 38–41': ('job', '38-41', None),
    'Job 40:1–5': ('job', 40, '1–5'),
    'Job 40:15–24': ('job', 40, '15–24'),
    'Job 41': ('job', 41, None),
    'Job 42:1–6': ('job', 42, '1–6'),
    'Job 42:5': ('job', 42, 5),
    'Job 42:5–6': ('job', 42, '5–6'),
    'Job 42:7': ('job', 42, 7),
    'Job 42:7–9': ('job', 42, '7–9'),
    'Job 42:10': ('job', 42, 10),
    'Job 42:12': ('job', 42, 12),
    'Job 42:13': ('job', 42, 13),
    'Job 42:14': ('job', 42, 14),
    'Job 42:14–15': ('job', 42, '14–15'),
    'Job 42:15': ('job', 42, 15),
    'Job 42:16–17': ('job', 42, '16–17'),
    
    # Psalms
    'Psalm 1': ('ps', 1, None),
    'Psalm 2': ('ps', 2, None),
    'Psalm 2:1–3': ('ps', 2, '1–3'),
    'Psalm 2:7': ('ps', 2, 7),
    'Psalm 2:8–9': ('ps', 2, '8–9'),
    'Psalm 8': ('ps', 8, None),
    'Psalm 19': ('ps', 19, None),
    'Psalm 19:1': ('ps', 19, 1),
    'Psalm 19:7–11': ('ps', 19, '7–11'),
    'Psalm 22': ('ps', 22, None),
    'Psalm 22:1': ('ps', 22, 1),
    'Psalm 22:7–8': ('ps', 22, '7–8'),
    'Psalm 22:16': ('ps', 22, 16),
    'Psalm 22:18': ('ps', 22, 18),
    'Psalm 23': ('ps', 23, None),
    'Psalm 23:1': ('ps', 23, 1),
    'Psalm 23:2': ('ps', 23, 2),
    'Psalm 23:4': ('ps', 23, 4),
    'Psalm 23:5': ('ps', 23, 5),
    'Psalm 23:6': ('ps', 23, 6),
    'Psalm 24': ('ps', 24, None),
    'Psalm 24:3': ('ps', 24, 3),
    'Psalm 24:3–4': ('ps', 24, '3–4'),
    'Psalm 26': ('ps', 26, None),
    'Psalm 26–28': ('ps', '26-28', None),
    'Psalm 26:1': ('ps', 26, 1),
    'Psalm 26:11': ('ps', 26, 11),
    'Psalm 27': ('ps', 27, None),
    'Psalm 27:1': ('ps', 27, 1),
    'Psalm 27:9': ('ps', 27, 9),
    'Psalm 27:13–14': ('ps', 27, '13–14'),
    'Psalm 27:14': ('ps', 27, 14),
    'Psalm 28': ('ps', 28, None),
    'Psalm 28:2': ('ps', 28, 2),
    'Psalm 29': ('ps', 29, None),
    'Psalm 30:5': ('ps', 30, 5),
    'Psalm 31:5': ('ps', 31, 5),
    'Psalm 33': ('ps', 33, None),
    'Psalm 33:1–6': ('ps', 33, '1–6'),
    'Psalm 37:3–9': ('ps', 37, '3–9'),
    'Psalm 40': ('ps', 40, None),
    'Psalm 46': ('ps', 46, None),
    'Psalm 46:1': ('ps', 46, 1),
    'Psalm 46:10': ('ps', 46, 10),
    'Psalm 119': ('ps', 119, None),
    'Psalm 113–118': ('ps', '113-118', None),
    'Psalm 148': ('ps', 148, None),
    'Psalm 150': ('ps', 150, None),
    
    # Genesis
    'Genesis 3:4–5': ('gen', 3, '4–5'),
    
    # Isaiah
    'Isaiah 40:26': ('isa', 40, 26),
    
    # Matthew
    'Matthew 27:35': ('matt', 27, 35),
    'Matthew 27:39–43': ('matt', 27, '39–43'),
    'Matthew 27:45–46': ('matt', 27, '45–46'),
    
    # Luke
    'Luke 23:32–33': ('luke', 23, '32–33'),
    'Luke 23:46': ('luke', 23, 46),
    
    # John
    'John 10': ('jn', 10, None),
    'John 9:1–3': ('jn', 9, '1–3'),
    
    # Acts
    'Acts 4:24–28': ('acts', 4, '24–28'),
    'Acts 4:25–26': ('acts', 4, '25–26'),
    'Acts 13:30–33': ('acts', 13, '30–33'),
    
    # Romans
    'Romans 5:12–21': ('rom', 5, '12–21'),
    'Romans 8:28': ('rom', 8, 28),
    
    # 1 John
    '1 John 2:1': ('1-jn', 2, 1),
    
    # Revelation
    'Revelation 12:10': ('rev', 12, 10),
    
    # 2 Nephi
    '2 Nephi 2:11–13': ('2-ne', 2, '11–13'),
    
    # Mosiah
    'Mosiah 23:21–23': ('mosiah', 23, '21–23'),
    'Mosiah 24:10–16': ('mosiah', 24, '10–16'),
    
    # Alma
    'Alma 11:42–44': ('alma', 11, '42–44'),
    
    # Ether
    'Ether 12:27': ('ether', 12, 27),
    
    # D&C
    'D&C 45:3–5': ('dc', 45, '3–5'),
    'D&C 58:3–5': ('dc', 58, '3–5'),
    'D&C 76:25–29': ('dc', 76, '25–29'),
    'D&C 121:1–12': ('dc', 121, '1–12'),
    'D&C 122': ('dc', 122, None),
    'D&C 122:8': ('dc', 122, 8),
    'D&C 130:2': ('dc', 130, 2),
    
    # Moses
    'Moses 1:6': ('moses', 1, 6),
    'Moses 1:10': ('moses', 1, 10),
    'Moses 1:11': ('moses', 1, 11),
    'Moses 1:8–10': ('moses', 1, '8–10'),
    'Moses 4:1–4': ('moses', 4, '1–4'),
    
    # Abraham
    'Abraham 3:22–26': ('abr', 3, '22–26'),
    'Abraham 3:22': ('abr', 3, 22),
    'Abraham 3:28': ('abr', 3, 28),
    
    # Zechariah
    'Zechariah 3:1': ('zech', 3, 1),
}

VALID_BOOKS = set(BOOK_PATHS.keys())


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def make_gospel_library_url(book_key: str, chapter, verse: Optional[str] = None) -> Optional[str]:
    """Build a Gospel Library URL for a scripture reference."""
    if book_key not in BOOK_PATHS:
        return None
    path = BOOK_PATHS[book_key]
    if verse:
        return f"https://www.churchofjesuschrist.org/study/scriptures/ot/{BOOK_PATHS[book_key]}/{chapter}?lang=eng&id={verse}"
    else:
        return f"https://www.churchofjesuschrist.org/study/scriptures/ot/{BOOK_PATHS[book_key]}/{chapter}?lang=eng"


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


def inject_links(html: str, 
                 scripture_refs: Dict[str, Tuple[str, any, Optional[str]]] = None,
                 book_paths: Dict[str, str] = None,
                 valid_books: Set[str] = None) -> str:
    """
    Inject clickable Gospel Library links into HTML.
    
    Args:
        html: Input HTML string
        scripture_refs: Dict of reference_string -> (book_key, chapter, verse)
        book_paths: Dict of book_key -> Gospel Library path
        valid_books: Set of valid book keys
    
    Returns:
        Modified HTML with clickable links
    """
    if scripture_refs is None:
        scripture_refs = SCRIPTURE_REFS
    if book_paths is None:
        book_paths = BOOK_PATHS
    if valid_books is None:
        valid_books = VALID_BOOKS
    
    # Find protected intervals
    protected_intervals = find_protected_intervals(html)
    
    # Build free regions (regions NOT in protected intervals)
    free_regions = []
    last_end = 0
    for start, end in protected_intervals:
        if start > last_end:
            free_regions.append((last_end, start))
        last_end = end
    if last_end < len(html):
        free_regions.append((last_end, len(html)))
    
    # Sort refs by length descending to avoid partial matches
    sorted_refs = sorted(SCRIPTURE_REFS.items(), key=lambda x: -len(x[0]))
    
    # Process each free region
    result_parts = []
    for free_start, free_end in free_regions:
        # Add protected region before this free region
        if free_regions.index((free_start, free_end)) > 0:
            # Find the protected interval before this free region
            pass  # We'll rebuild by iterating through the whole string
    
    # Better approach: build result by iterating through protected intervals
    result_parts = []
    last_pos = 0
    
    for start, end in protected_intervals:
        # Process free region before this protected interval
        if start > last_pos:
            free_text = html[last_pos:start]
            processed = process_free_text(free_text)
            result_parts.append(processed)
        
        # Add protected region as-is
        result_parts.append(html[start:end])
        last_pos = end
    
    # Process final free region
    if last_pos < len(html):
        free_text = html[last_pos:]
        processed = process_free_text(free_text)
        result_parts.append(processed)
    
    return ''.join(result_parts)


def process_free_text(text: str) -> str:
    """Process a free text region, replacing scripture references with links."""
    result = text
    
    for ref_text, (book_key, chapter, verse) in sorted(SCRIPTURE_REFS.items(), key=lambda x: -len(x[0])):
        if book_key not in VALID_BOOKS:
            continue
        path = BOOK_PATHS[book_key]
        
        if verse:
            url = f"https://www.churchofjesuschrist.org/study/scriptures/ot/{BOOK_PATHS[book_key]}/{chapter}?lang=eng&id={verse}"
        else:
            url = f"https://www.churchofjesuschrist.org/study/scriptures/ot/{BOOK_PATHS[book_key]}/{chapter}?lang=eng"
        
        replacement = f'<a href="{url}" target="_blank" style="color: #3d7a9e; text-decoration: underline;">{ref_text}</a>'
        escaped = re.escape(ref_text)
        pattern = rf'(?<![\w\"])({re.escape(ref_text)})(?![\w\"])'
        result = re.sub(pattern, replacement, result)
    
    return result


def inject_links(html: str) -> str:
    """
    Main entry point: inject Gospel Library links into HTML.
    Uses default SCRIPTURE_REFS, BOOK_PATHS, VALID_BOOKS.
    """
    return inject_links(html)


# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python inject_gospel_library_links.py input.html output.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r') as f:
        html = f.read()
    
    result = inject_links(html)
    
    with open(output_file, 'w') as f:
        f.write(result)
    
    print(f"Processed {input_file} -> {output_file}")