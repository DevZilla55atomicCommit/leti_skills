---
name: tongan-scripture-link-injection
title: Tongan Scripture Link Injection
description: Tongan (lang=ton) Gospel Library links with correct paths.
version: 1.0.0
author: Maddie
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [scripture, tongan, gospel-library, links, injection]
    category: religious-study
    related_skills: [inject_links, personal_gc_talk_study_guide, come-follow-me-study-guide]
---

# Tongan Scripture Link Injection

## Purpose
Create Gospel Library links that point to Tongan (lea faka-Tonga) translations with correct URL paths for all standard works.

## Key Changes from Default

### 1. Language Parameter
- Default: `lang=eng` (English)
- Tongan: `lang=ton` (Tongan)

### 2. Book Path Mapping (Critical Fix)
The Gospel Library URL format is:
```
https://www.churchofjesuschrist.org/study/scriptures/{work}/{book_path}/{chapter}?lang={lang}&id={verse}
```

**BOOK_PATHS must NOT include work prefix** (ot/, nt/, bofm/, pgp/, dc/) since the work is added automatically by `BOOK_TO_WORK`.

### Correct BOOK_PATHS Format
```python
BOOK_PATHS = {
    # Old Testament - NO 'ot/' prefix
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
    
    # New Testament - Use FULL book names (not abbreviations)
    'matthew': 'matthew', 'mark': 'mark', 'luke': 'luke', 'john': 'john',
    'acts': 'acts', 'romans': 'romans', '1 corinthians': '1-corinthians', '2 corinthians': '2-corinthians',
    'galatians': 'galatians', 'ephesians': 'ephesians', 'philippians': 'philippians', 'colossians': 'colossians',
    '1 thessalonians': '1-thessalonians', '2 thessalonians': '2-thessalonians', '1 timothy': '1-timothy',
    '2 timothy': '2-timothy', 'titus': 'titus', 'philemon': 'philemon', 'hebrews': 'hebrews',
    'james': 'james', '1 peter': '1-peter', '2 peter': '2-peter', '1 john': '1-john',
    '2 john': '2-john', '3 john': '3-john', 'jude': 'jude', 'revelation': 'revelation',
    
    # Book of Mormon - Use short forms (correct as-is)
    '1 nephi': '1-ne', '2 nephi': '2-ne', 'jacob': 'jacob', 'enos': 'enos',
    'jarom': 'jarom', 'omni': 'omni', 'words of mormon': 'w-of-m',
    'mosiah': 'mosiah', 'alma': 'alma', 'helaman': 'hel', '3 nephi': '3-ne',
    '4 nephi': '4-ne', 'mormon': 'morm', 'ether': 'ether', 'moroni': 'moro',
    
    # Doctrine and Covenants
    'doctrine and covenants': 'dc',
    
    # Pearl of Great Price - NO 'pgp/' prefix
    'moses': 'moses', 'abraham': 'abraham', 'joseph smith—matthew': 'js-m', 'joseph smith—history': 'js-h',
}
```

### URL Construction
```python
def make_gospel_library_url(book_key: str, chapter: int, verse: Optional[str] = None, lang: str = "ton") -> Optional[str]:
    book_lower = book_key.lower()
    if book_lower not in BOOK_PATHS:
        return None
    
    path = BOOK_PATHS[book_lower]
    work = BOOK_TO_WORK.get(book_lower, 'ot')
    
    if verse:
        return f"https://www.churchofjesuschrist.org/study/scriptures/{work}/{path}/{chapter}?lang={lang}&id={verse}"
    else:
        return f"https://www.churchofjesuschrist.org/study/scriptures/{work}/{path}/{chapter}?lang={lang}"
```

### BOOK_TO_WORK Mapping
```python
BOOK_TO_WORK = {
    # Old Testament
    'genesis': 'ot', 'exodus': 'ot', 'leviticus': 'ot', 'numbers': 'ot', 'deuteronomy': 'ot',
    'joshua': 'ot', 'judges': 'ot', 'ruth': 'ot', '1 samuel': 'ot', '2 samuel': 'ot',
    '1 kings': 'ot', '2 kings': 'ot', '1 chronicles': 'ot', '2 chronicles': 'ot',
    'ezra': 'ot', 'nehemiah': 'ot', 'esther': 'ot', 'job': 'ot', 'psalms': 'ot',
    'proverbs': 'ot', 'ecclesiastes': 'ot', 'song of solomon': 'ot', 'isaiah': 'ot',
    'jeremiah': 'ot', 'lamentations': 'ot', 'ezekiel': 'ot', 'daniel': 'ot',
    'hosea': 'ot', 'joel': 'ot', 'amos': 'ot', 'obadiah': 'ot', 'jonah': 'ot',
    'micah': 'ot', 'nahum': 'ot', 'habakkuk': 'ot', 'zephaniah': 'ot', 'haggai': 'ot',
    'zechariah': 'ot', 'malachi': 'ot',
    
    # New Testament
    'matthew': 'nt', 'mark': 'nt', 'luke': 'nt', 'john': 'nt', 'acts': 'nt',
    'romans': 'nt', '1 corinthians': 'nt', '2 corinthians': 'nt', 'galatians': 'nt',
    'ephesians': 'nt', 'philippians': 'nt', 'colossians': 'nt', '1 thessalonians': 'nt',
    '2 thessalonians': 'nt', '1 timothy': 'nt', '2 timothy': 'nt', 'titus': 'nt',
    'philemon': 'nt', 'hebrews': 'nt', 'james': 'nt', '1 peter': 'nt', '2 peter': 'nt',
    '1 john': 'nt', '2 john': 'nt', '3 john': 'nt', 'jude': 'nt', 'revelation': 'nt',
    
    # Book of Mormon
    '1 nephi': 'bofm', '2 nephi': 'bofm', 'jacob': 'bofm', 'enos': 'bofm',
    'jarom': 'bofm', 'omni': 'bofm', 'words of mormon': 'bofm', 'mosiah': 'bofm',
    'alma': 'bofm', 'helaman': 'bofm', '3 nephi': 'bofm', '4 nephi': 'bofm',
    'mormon': 'bofm', 'ether': 'bofm', 'moroni': 'bofm',
    
    # Doctrine and Covenants
    'doctrine and covenants': 'dc',
    
    # Pearl of Great Price
    'moses': 'pgp', 'abraham': 'pgp', 'joseph smith—matthew': 'pgp', 'joseph smith—history': 'pgp',
}
```

## Usage Example

### In inject_links.py
```python
# Tongan is now the default
def make_gospel_library_url(book_key: str, chapter: int, verse: Optional[str] = None, lang: str = "ton") -> Optional[str]:
    # ... implementation
```

### In personal_study.py
```python
# Talk summary
talk_summary = generate_talk_summary(talk, title=mobile_data["talk_title"])

# Convert markdown to HTML for template
try:
    import markdown
    talk_summary_html = markdown.markdown(talk_summary, extensions=['tables', 'fenced_code', 'codehilite'])
except ImportError:
    talk_summary_html = talk_summary

# Talk summary with Tongan links
talk_summary = generate_talk_summary(talk, title=mobile_data["talk_title"])
```

## Verification Checklist
- [ ] All links use `lang=ton`
- [ ] Book of Mormon links: `/bofm/alma/7?lang=ton&id=3` ✅
- [ ] New Testament links: `/nt/james/1?lang=ton&id=8` ✅
- [ ] Old Testament links: `/ot/malachi/3?lang=ton&id=10` ✅
- [ ] Pearl of Great Price: `/pgp/moses/5?lang=ton&id=5` ✅
- [ ] No double prefixes (e.g., no `bofm/bofm/alma`)

## Files Modified
1. `scripts/inject_links.py` - BOOK_PATHS, make_gospel_library_url(), DEFAULT_SCRIPTURE_REFS
2. `scripts/personal_study.py` - Added `talk_summary_html` to template data, markdown conversion

## Backup Strategy
Always create backup before modifying:
```bash
cp study-guide.pdf study-guide_backup_$(date +%Y%m%d_%H%M%S).pdf
```