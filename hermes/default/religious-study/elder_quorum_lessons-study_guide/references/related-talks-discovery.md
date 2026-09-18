# Related Talks Discovery Guide

## How to Find Related General Conference Talks

### 1. Official Search (Best for Recent Talks)
```
https://www.churchofjesuschrist.org/search?q={query}&facet=general-conference
```

**Effective Queries:**
- `tithing consecration` — Core doctrine
- `Malachi 3:10` — Windows of heaven
- `firstlings Adam offering` — Moses 5 pattern
- `double-minded James 1:8` — Single eye
- `seek ye first kingdom` — Matthew 6:33
- `law of tithing D&C 119` — Covenant law
- `spiritual capacity tithing` — Becerra's unique contribution

### 2. Conference Archive by Year
```
https://www.churchofjesuschrist.org/study/general-conference/{year}
```
Browse by session (Saturday AM/PM, Sunday AM/PM) for comprehensive coverage.

### 3. Speaker-Based Discovery
```
https://www.churchofjesuschrist.org/study/general-conference/speakers/{speaker-slug}
```
Key speakers for tithing/consecration:
- Russell M. Nelson
- David A. Bednar
- Neal A. Maxwell
- Dieter F. Uchtdorf
- Gordon B. Hinckley
- James E. Faust
- Robert D. Hales
- Jeffrey R. Holland
- D. Todd Christofferson

### 4. Scripture-Based Discovery
Search for talks citing specific verses:
- `Malachi 3:10` → Talks on windows of heaven
- `Matthew 6:33` → Priorities/putting God first
- `James 1:8` → Double-mindedness
- `Alma 5:12` → Mighty change of heart
- `Alma 7:3,18` → Dilemma/double-mindedness
- `Moses 5:5-7` → Adam's firstlings
- `D&C 119` → Law of tithing

### 5. Topic Tag Discovery
General Conference talks have topic tags. Use the "Topics" filter on the GC archive page.

### 6. Era-Based Strategy

| Era | Focus | Key Speakers |
|-----|-------|--------------|
| **2020-Present** | Current prophetic emphasis, tithing as spiritual capacity | Nelson, Bednar, Uchtdorf, Becerra |
| **2000-2019** | Tithing as test of faith, windows of heaven | Hinckley, Faust, Hales, Bednar, Maxwell |
| **1980-1999** | Law of tithing, consecration preparation | Benson, Maxwell, Faust, Hinckley |
| **1970-1979** | Foundational consecration theology | Maxwell, McConkie, Kimball |

### 7. Cross-Reference Strategy

1. **Start with the talk's footnotes** — each footnote often links to a GC talk
2. **Check the "Related Content" sidebar** on the talk page
3. **Use the Gospel Library app** — "Related Content" section
4. **Search BYU Speeches** for same speaker + topic
5. **Check Gospel Topics essays** — "Related Conference Talks" section

### 8. Automated Discovery (for the skill)

The `discover.py` script uses:
- **Theme extraction** from talk text and scriptures
- **Keyword matching** against curated GC talk database
- **Relevance scoring** based on shared themes
- **Top 8 results** returned with connection explanations

### 9. Manual Curation Checklist

When manually adding talks to the database:

- [ ] Talk is from General Conference (not devotional, fireside, etc.)
- [ ] Talk directly addresses tithing/consecration/sacrifice/firstlings
- [ ] Talk cites relevant scriptures (Malachi 3, Matthew 6, James 1, Alma 5/7, Moses 5, D&C 119)
- [ ] Speaker is a General Authority or General Officer
- [ ] Talk is available on churchofjesuschrist.org with stable URL
- [ ] Connection to target talk is clearly articulable

### 10. Quality Indicators

**High Relevance (score 3+):**
- Same primary theme (tithing, consecration, firstlings)
- Same key scriptures cited
- Direct doctrinal development

**Medium Relevance (score 2):**
- Related theme (obedience, covenants, blessings)
- Shared supporting scriptures
- Complementary perspective

**Contextual Relevance (score 1):**
- Broader principle (faith, obedience, priorities)
- Indirect connection
- Useful for background

### 11. URL Stability

Use the canonical URL format:
```
https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}/{talk-id}?lang=eng
```

Avoid:
- Shortened URLs
- Redirect URLs
- Session-specific URLs that may change

The `talk-id` is stable and preferred over speaker-name URLs.