# Podcast Discovery Guide — Come Follow Me Lesson Prep

## followHIM Podcast (Primary Supplemental Resource)

### YouTube Channel
- **Channel**: `@followHIM` (166K subscribers)
- **Search pattern**: `followHIM + [scripture block] + [week dates] + "Come, Follow Me"`

### Direct Search URLs
```bash
# YouTube search for specific week
https://www.youtube.com/results?search_query=followHIM+[scripture]+[dates]+2026

# Channel videos page
https://www.youtube.com/@followHIM/videos
```

### Example Searches (2026 Old Testament)
```
followHIM Job August 10-16 2026
followHIM Psalms 1-2 8 19-33 40 46 August 17-23 2026
followHIM "The Lord Is My Shepherd" 2026
```

### Video Structure (Typical)
- **Part 1** — First half of lesson (~45-60 min)
- **Part 2** — Second half (~45-60 min)
- **Guest**: Usually a BYU professor, scholar, or expert
- **Chapters**: YouTube chapters = topic segments (great for finding specific insights)

### Key Data to Extract
| Field | Where to Find |
|-------|---------------|
| Guest name | Video title / description |
| Guest bio | Description / "Show Notes" link |
| Key insights | Chapter titles + first 2 min of each chapter |
| Memorable quotes | Listen to chapter openings/closings |
| Personal stories | Often in Part 2, middle sections |

## followhim.co Website (Secondary)

### Site Structure
```
https://followhim.co/old-testament-2026
```
- Lists episodes by date range
- "PART 1" / "PART 2" links → direct to YouTube
- "SHOW NOTES" links → PDF with outline + references
- "DOWNLOAD PDF" → full transcript with citations

### Week Navigation
- "2026 Episodes 1-10", "2026 Episodes 11-20", etc.
- Date ranges in bold (e.g., "August 17 - 23")
- Guest name listed below date

### Show Notes PDF (High Value)
- Direct PDF download
- Contains: outline, key quotes, scripture references, guest bibliography
- Often more organized than video chapters

## BYU Studies Podcast

### YouTube Search
```
BYU Studies [scripture] Come Follow Me 2026
```

### Articles (Often More Detailed Than Podcasts)
```
https://byustudies.byu.edu/come-follow-me/old-testament/{week_number}
```
- Multiple scholarly articles per scripture
- Filter by scripture reference in page content
- Conference talk references embedded

## Extraction Workflow (Per Week)

### 1. Find Official Week Dates
- From Come Follow Me manual page → date range

### 2. Calculate BYU Studies Week Number
```python
week = ((date - Jan1).days // 7) + 1
```

### 3. Search YouTube for followHIM
```
"followHIM [main scripture] [date range] 2026"
```
- Open first 2-3 results (usually Part 1, Part 2, Preview)
- Note: Guest name, key chapter topics

### 3b. Check followhim.co for Show Notes
- Navigate to followhim.co/old-testament-2026
- Find week by date range
- Download SHOW NOTES PDF
- Extract: guest bio, key quotes, conference talk refs

### 4. Check BYU Studies Page
```
https://byustudies.byu.edu/come-follow-me/old-testament/{week}
```
- Scan for relevant articles
- Note: author, title, key insight

### 5. Compile Podcast Insights Table
| Source | Guest | Key Insight | Quote to Use | Scripture |
|--------|-------|-------------|--------------|-----------|

## Common Guests & Their Specialties (2026)

| Guest | Specialty | Episodes |
|-------|-----------|----------|
| Dr. Marcus Martins | Job, suffering, temple | Job (Aug 10-16) |
| Steven Sharp Nelson (The Piano Guys) | Psalms, music, worship | Psalms (Aug 17-23) |
| Dr. Shon Hopkin | Hebrew, Psalms, Isaiah | Psalms, Isaiah |
| Dr. Sarah Emanuel | Jewish/Christian dialogue, Job | Job |
| Dr. Kerry Muhlestein | Moses, Abraham, temple | Genesis/Moses |
| Dr. John Hilton III | Fall, atonement, teaching | Genesis 3-4 |
| Dr. Jennifer Lane | Abraham, covenant | Genesis 12-17 |

## Quality Checklist
- [ ] Both Part 1 & Part 2 located
- [ ] Guest name & credentials noted
- [ ] 3-5 key insights extracted with timestamps/chapters
- [ ] 1-2 memorable quotes for teaching
- [ ] Show Notes PDF downloaded (if available)
- [ ] BYU Studies articles scanned for unique angles
- [ ] All insights attributed to speaker + source