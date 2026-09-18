# Scripture Reference Extraction Patterns

## Regex Patterns for Extracting Scripture References from GC Talks

### Primary Patterns (in order of specificity)

```python
# 1. Full reference with book, chapter, verse(s)
# "Alma 5:12", "Alma 7:3,18", "Malachi 3:10-12", "Matthew 6:33"
PATTERN_FULL = r'\b([1-3]?\s?[A-Za-z][A-Za-z\s]*\.?\s+\d+:\d+(?:[–-]\d+)?(?:,\s*\d+(?:[–-]\d+)?)*?)\b'

# 2. Book + Chapter only (context dependent)
# "Alma 5", "Malachi 3", "Moses 5"
PATTERN_CHAPTER = r'\b([1-3]?\s?[A-Za-z][A-Za-z\s]*\.?\s+\d+)(?!\s*:\d)'

# 3. Footnote references
# "footnote a", "fn. 3", "footnotes 1–3"
PATTERN_FOOTNOTE = r'(?:footnote|fn\.?)\s*([a-z\d]+(?:[–-][a-z\d]+)?)'

# 4. "Verse X" or "verses X-Y" (when book/chapter established)
PATTERN_VERSE_ONLY = r'\b(?:verse|verses)\s+(\d+(?:[–-]\d+)?)\b'
```

### GC Talk HTML-Specific Patterns

```python
# Footnote links in GC HTML
# <a href="#fn1" class="footnote-ref">1</a>
# <sup class="footnote-ref"><a href="#fn1">a</a></sup>
FOOTNOTE_LINK_PATTERN = r'<a\s+href="#fn(\d+)"[^>]*>.*?</a>'

# Scripture links in GC HTML (sometimes pre-linked)
# <a href="/study/scriptures/bofm/alma/5?lang=eng&id=p12" class="scripture-ref">Alma 5:12</a>
SCRIPTURE_LINK_PATTERN = r'<a\s+href="[^"]*/scriptures/[^"]*"[^>]*>([^<]+)</a>'
```

### Book Name Normalization Map

```python
BOOK_ALIASES = {
    # Old Testament
    'gen': 'Genesis', 'genesis': 'Genesis',
    'ex': 'Exodus', 'exod': 'Exodus', 'exodus': 'Exodus',
    'lev': 'Leviticus', 'leviticus': 'Leviticus',
    'num': 'Numbers', 'numbers': 'Numbers',
    'deut': 'Deuteronomy', 'deuteronomy': 'Deuteronomy',
    'josh': 'Joshua', 'joshua': 'Joshua',
    'judg': 'Judges', 'judges': 'Judges',
    'ruth': 'Ruth',
    '1 sam': '1 Samuel', '1 samuel': '1 Samuel',
    '2 sam': '2 Samuel', '2 samuel': '2 Samuel',
    '1 kgs': '1 Kings', '1 kings': '1 Kings',
    '2 kgs': '2 Kings', '2 kings': '2 Kings',
    '1 chr': '1 Chronicles', '1 chronicles': '1 Chronicles',
    '2 chr': '2 Chronicles', '2 chronicles': '2 Chronicles',
    'ezra': 'Ezra', 'neh': 'Nehemiah', 'nehemiah': 'Nehemiah',
    'esth': 'Esther', 'esther': 'Esther',
    'job': 'Job',
    'ps': 'Psalms', 'psalm': 'Psalms', 'psalms': 'Psalms',
    'prov': 'Proverbs', 'proverbs': 'Proverbs',
    'eccl': 'Ecclesiastes', 'ecclesiastes': 'Ecclesiastes',
    'song': 'Song of Solomon',
    'isa': 'Isaiah', 'isaiah': 'Isaiah',
    'jer': 'Jeremiah', 'jeremiah': 'Jeremiah',
    'lam': 'Lamentations', 'lamentations': 'Lamentations',
    'ezek': 'Ezekiel', 'ezekiel': 'Ezekiel',
    'dan': 'Daniel', 'daniel': 'Daniel',
    'hosea': 'Hosea', 'joel': 'Joel', 'amos': 'Amos',
    'obad': 'Obadiah', 'obadiah': 'Obadiah',
    'jonah': 'Jonah', 'micah': 'Micah', 'nahum': 'Nahum',
    'hab': 'Habakkuk', 'habakkuk': 'Habakkuk',
    'zeph': 'Zephaniah', 'zephaniah': 'Zephaniah',
    'hag': 'Haggai', 'haggai': 'Haggai',
    'zech': 'Zechariah', 'zechariah': 'Zechariah',
    'mal': 'Malachi', 'malachi': 'Malachi',
    
    # New Testament
    'matt': 'Matthew', 'matthew': 'Matthew', 'mt': 'Matthew',
    'mark': 'Mark', 'mk': 'Mark',
    'luke': 'Luke', 'lk': 'Luke',
    'john': 'John', 'jn': 'John',
    'acts': 'Acts',
    'rom': 'Romans', 'romans': 'Romans',
    '1 cor': '1 Corinthians', '1 corinthians': '1 Corinthians',
    '2 cor': '2 Corinthians', '2 corinthians': '2 Corinthians',
    'gal': 'Galatians', 'galatians': 'Galatians',
    'eph': 'Ephesians', 'ephesians': 'Ephesians',
    'phil': 'Philippians', 'philippians': 'Philippians',
    'col': 'Colossians', 'colossians': 'Colossians',
    '1 thess': '1 Thessalonians', '1 thessalonians': '1 Thessalonians',
    '2 thess': '2 Thessalonians', '2 thessalonians': '2 Thessalonians',
    '1 tim': '1 Timothy', '1 timothy': '1 Timothy',
    '2 tim': '2 Timothy', '2 timothy': '2 Timothy',
    'titus': 'Titus', 'phlm': 'Philemon', 'philemon': 'Philemon',
    'heb': 'Hebrews', 'hebrews': 'Hebrews',
    'james': 'James', 'jas': 'James',
    '1 pet': '1 Peter', '1 peter': '1 Peter',
    '2 pet': '2 Peter', '2 peter': '2 Peter',
    '1 jn': '1 John', '1 john': '1 John',
    '2 jn': '2 John', '2 john': '2 John',
    '3 jn': '3 John', '3 john': '3 John',
    'jude': 'Jude',
    'rev': 'Revelation', 'revelation': 'Revelation',
    
    # Book of Mormon
    '1 ne': '1 Nephi', '1 nephi': '1 Nephi',
    '2 ne': '2 Nephi', '2 nephi': '2 Nephi',
    'jacob': 'Jacob', 'enos': 'Enos', 'jarom': 'Jarom', 'omni': 'Omni',
    'w of m': 'Words of Mormon', 'words of mormon': 'Words of Mormon',
    'mosiah': 'Mosiah', 'alma': 'Alma', 'hel': 'Helaman', 'helaman': 'Helaman',
    '3 ne': '3 Nephi', '3 nephi': '3 Nephi',
    '4 ne': '4 Nephi', '4 nephi': '4 Nephi',
    'morm': 'Mormon', 'mormon': 'Mormon',
    'ether': 'Ether', 'moro': 'Moroni', 'moroni': 'Moroni',
    
    # D&C
    'dc': 'Doctrine and Covenants', 'd&c': 'Doctrine and Covenants',
    'doctrine and covenants': 'Doctrine and Covenants',
    
    # Pearl of Great Price
    'moses': 'Moses', 'abr': 'Abraham', 'abraham': 'Abraham',
    'js-m': 'Joseph Smith—Matthew', 'js-h': 'Joseph Smith—History',
}
```

### Extraction Algorithm

```python
def extract_scriptures_from_gc_talk(html_or_text: str) -> List[ScriptureReference]:
    """
    Extract all scripture references from a GC talk.
    Handles inline citations, footnotes, and pre-linked scriptures.
    """
    scriptures = []
    
    # 1. Extract from pre-linked scripture anchors
    for match in re.finditer(SCRIPTURE_LINK_PATTERN, html_or_text):
        ref_text = match.group(1)
        parsed = parse_scripture_ref(ref_text)
        if parsed:
            parsed.context = get_surrounding_context(html_or_text, match.start())
            scriptures.append(parsed)
    
    # 2. Extract from footnote links
    footnote_ids = set()
    for match in re.finditer(FOOTNOTE_LINK_PATTERN, html_or_text):
        footnote_ids.add(match.group(1))
    
    # 3. Extract inline citations from text
    text = strip_html_tags(html_or_text)
    
    # Full references
    for match in re.finditer(PATTERN_FULL, text):
        ref = match.group(1)
        parsed = parse_scripture_ref(ref)
        if parsed:
            parsed.context = text[max(0, match.start()-100):match.end()+100]
            scriptures.append(parsed)
    
    # Chapter-only (validate with context)
    for match in re.finditer(PATTERN_CHAPTER, text):
        ref = match.group(1)
        # Only keep if near a verse reference or in scripture discussion context
        context = text[max(0, match.start()-200):match.end()+200]
        if any(kw in context.lower() for kw in ['verse', 'chapter', 'scripture', 'read', 'study']):
            parsed = parse_scripture_ref(ref)
            if parsed:
                parsed.context = context
                scriptures.append(parsed)
    
    # 4. Footnote content extraction
    footnote_blocks = extract_footnote_blocks(html_or_text)
    for fn_id, fn_text in footnote_blocks.items():
        if fn_id in footnote_ids or any(kw in fn_text.lower() for kw in ['malachi', 'matthew', 'james', 'alma', 'moses', 'dc', 'd&c']):
            for match in re.finditer(PATTERN_FULL, fn_text):
                ref = match.group(1)
                parsed = parse_scripture_ref(ref)
                if parsed:
                    parsed.is_footnote = True
                    parsed.footnote_id = fn_id
                    parsed.context = fn_text[:200]
                    scriptures.append(parsed)
    
    # 5. Deduplicate
    seen = set()
    unique = []
    for s in scriptures:
        key = (s.book.lower(), s.chapter, s.verse, s.is_footnote)
        if key not in seen:
            seen.add(key)
            unique.append(s)
    
    return unique
```

### Context Extraction Helper

```python
def get_surrounding_context(text: str, position: int, radius: int = 150) -> str:
    """Get text context around a position."""
    start = max(0, position - radius)
    end = min(len(text), position + radius)
    return text[start:end].strip()

def strip_html_tags(html: str) -> str:
    """Remove HTML tags, preserve text content."""
    # Remove script/style
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Replace block elements with newlines
    html = re.sub(r'</(p|div|h[1-6]|li|br)>', '\n', html, flags=re.IGNORECASE)
    # Strip remaining tags
    html = re.sub(r'<[^>]+>', '', html)
    # Decode entities
    html = html.replace('&nbsp;', ' ').replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"')
    # Normalize whitespace
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

def extract_footnote_blocks(html: str) -> Dict[str, str]:
    """Extract footnote content by ID."""
    footnotes = {}
    # Pattern: <div id="fn1" class="footnote">...</div>
    for match in re.finditer(r'<div\s+id=["\']fn(\d+)["\'][^>]*>(.*?)</div>', html, flags=re.DOTALL | re.IGNORECASE):
        footnotes[match.group(1)] = strip_html_tags(match.group(2))
    return footnotes
```

### Validation Rules

```python
def validate_scripture_ref(ref: ScriptureReference) -> bool:
    """Validate a parsed scripture reference."""
    # Book must be known
    if ref.book.lower() not in VALID_BOOKS:
        return False
    
    # Chapter must be reasonable
    if ref.chapter < 1 or ref.chapter > 150:
        return False
    
    # Verse format validation
    if ref.verse:
        # Single verse: "12"
        # Range: "12-15" or "12–15"
        # Multiple: "12, 15" (handled as separate refs)
        verse_str = ref.verse.replace('–', '-')
        parts = verse_str.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                if not (start.isdigit() and end.isdigit()):
                    return False
                if int(start) >= int(end):
                    return False
            elif not part.isdigit():
                return False
    
    return True
```

### Common False Positives to Filter

```python
FALSE_POSITIVE_PATTERNS = [
    r'\b\d{1,2}:\d{2}\s*(?:am|pm)\b',  # Time: "10:30 am"
    r'\b\d{4}:\d{2}\b',                 # Date-like: "2026:04"
    r'\b\d+:\d+:\d+\b',                 # Time with seconds
    r'^\d+:\s',                         # List numbering
]

def is_false_positive(text: str, position: int) -> bool:
    """Check if a match at position is a false positive."""
    context = text[max(0, position-10):position+20]
    for pattern in FALSE_POSITIVE_PATTERNS:
        if re.search(pattern, context, re.IGNORECASE):
            return True
    return False
```

### Output Format for Skill

```json
{
  "reference": "Alma 5:12",
  "book": "Alma",
  "chapter": 5,
  "verse": "12",
  "context": "...have a mighty change of heart as disciples of Jesus Christ (Alma 5:12)...",
  "is_footnote": false,
  "footnote_id": null,
  "standard_work": "Book of Mormon"
}
```