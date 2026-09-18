# LDS.org Navigation Reference

## General Conference Talk URL Patterns

### Direct Talk URL
```
https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}/{talk-slug}?lang=eng
```

### Conference Session URL
```
https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}?lang=eng
```

### Search URL
```
https://www.churchofjesuschrist.org/search?query={search-term}&lang=eng
```

## Navigation Patterns for Browser Automation

### 1. Landing on General Conference Page
- Navigate to `https://www.churchofjesuschrist.org/study/general-conference?lang=eng`
- Wait 3-5 seconds for React rendering
- Verify `element_count > 0` on snapshot

### 2. Finding a Specific Conference
- Click conference link (e.g., "April 2026" → ref from snapshot)
- Re-capture snapshot after click
- Wait for session list to load

### 3. Finding a Specific Talk
- Use search combobox (ref=e8 on main page)
- Type speaker name + talk title
- Press Enter
- Click first result (ref=e86 pattern)

### 4. Extracting Talk Content
- After clicking talk link, wait 3-5 seconds
- Look for `article` element with talk content
- Extract all paragraphs, scripture links, headings
- Hero image typically in `img` within article or sectionheader

## JavaScript Rendering Notes
- **Critical**: churchofjesuschrist.org uses React — content loads dynamically
- **Always wait 3-5 seconds** after navigation before extracting
- **Re-capture snapshot** after every click — element indices shift
- **Verify** `article` element exists before extracting text

## Element Patterns from Snapshots

### Search Results
- Each result: `listitem` with `link` containing talk title
- Ref pattern: `e86`, `e87`, etc. (changes per search)

### Talk Page Structure
- `sectionheader` with talk title (h1)
- `article` with full talk content
- Scripture references as `link` elements with `href` containing `/scriptures/`
- Hero image in `sectionheader` or `article` first `img`

### Common Ref Patterns (April 2026 example)
- Talk link in session list: `e60` (Tithing—Putting God First)
- Talk content article: appears after click, new refs assigned
- Scripture links: `e47` (Alma 5:12), `e48` (Alma 7:3), `e51` (James 1:8), `e52` (Matthew 6:33), `e53` (Moses 5:5–7), `e54` (Moses 5:5), `e55` (Moses 5:9), `e56` (Malachi 3:10), `e57` (The Windows of Heaven)

## Extraction Checklist
- [ ] Full talk text (all paragraphs)
- [ ] All scripture references with URLs
- [ ] Speaker name and calling
- [ ] Conference date/session
- [ ] Hero image URL
- [ ] Talk slug for folder naming

## Rate Limiting
- Add 2-3 second pauses between rapid clicks
- If 429/rate limit: wait 30s, retry
- Cache results locally for reuse

## Fallback: Search API
If direct navigation fails:
1. Use search: `https://www.churchofjesuschrist.org/search?query={speaker}+{title}&lang=eng`
2. Click first result
3. Proceed with extraction

## Related Resources
- Gospel Topics: `https://www.churchofjesuschrist.org/study/manual/gospel-topics/{topic}?lang=eng`
- BYU Speeches: `https://speeches.byu.edu/speakers/{speaker-name}/`
- Handbook: `https://www.churchofjesuschrist.org/study/handbooks/general-handbook/{section}?lang=eng`