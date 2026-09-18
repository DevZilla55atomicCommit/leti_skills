# BYU Studies URL Patterns for Come Follow Me

## Base URL Structure
```
https://byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]
```

## Volume Identifiers
| Volume | URL Segment |
|--------|-------------|
| Old Testament | old-testament |
| New Testament | new-testament |
| Book of Mormon | book-of-mormon |
| Doctrine & Covenants | doctrine-and-covenants |
| Pearl of Great Price | pearl-of-great-price |

## Lesson Number Mapping
| Week Range | Lesson Numbers |
|------------|----------------|
| Jan 1-7 | 1 |
| Jan 8-14 | 2 |
| Jan 15-21 | 3 |
| Jan 22-28 | 4 |
| Feb 1-7 | 5 |
| Feb 8-14 | 6 |
| Feb 15-21 | 7 |
| Feb 22-28 | 8 |
| Mar 1-7 | 9 |
| Mar 8-14 | 10 |
| Mar 15-21 | 11 |
| Mar 22-28 | 12 |
| Mar 29-Apr 4 | 13 |
| Apr 5-11 | 14 |
| Apr 12-18 | 15 |
| Apr 19-25 | 16 |
| Apr 26-May 2 | 17 |
| May 3-9 | 18 |
| May 10-16 | 19 |
| May 17-23 | 20 |
| May 24-30 | 21 |
| May 31-Jun 6 | 22 |
| Jun 7-13 | 23 |
| Jun 14-20 | 24 |
| Jun 21-27 | 24 |
| Jun 28-Jul 4 | 25 |
| Jul 5-11 | 26 |
| Jul 12-18 | 27 |
| Jul 19-25 | 28 |
| Jul 26-Aug 1 | 29 |
| Aug 2-8 | 30 |
| Aug 9-15 | 31 |
| Aug 16-22 | 32 |
| Aug 23-29 | 33 |
| Aug 30-Sep 5 | 34 |
| Sep 6-12 | 35 |
| Sep 13-19 | 36 |
| Sep 20-26 | 37 |
| Sep 27-Oct 3 | 38 |
| Oct 4-10 | 39 |
| Oct 11-17 | 40 |
| Oct 18-24 | 41 |
| Oct 25-31 | 42 |
| Nov 1-7 | 43 |
| Nov 8-14 | 44 |
| Nov 15-21 | 45 |
| Nov 22-28 | 46 |
| Nov 29-Dec 5 | 47 |
| Dec 6-12 | 48 |
| Dec 13-19 | 49 |
| Dec 20-26 | 50 |
| Dec 27-Jan 2 | 51 |

## URL Construction
```
https://byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]
```

## Examples
- **Job (Aug 10-16, 2026)**: `https://byustudies.byu.edu/come-follow-me/old-testament/33`
- **Psalms 1-2; 8; 19-33; 40; 46 (Aug 17-23, 2026)**: `https://byustudies.byu.edu/come-follow-me/old-testament/34`
- **Psalms 49-51; 61-66; 69-72; 77-78; 85-86 (Aug 24-30, 2026)**: `https://byustudies.byu.edu/come-follow-me/old-testament/35`

## Page Structure
Each lesson page contains:
1. **Header**: Scripture references, date range, title
2. **Article List**: Scholarly articles organized by scripture reference
3. **Article Cards**: Title, author, publication, year, preview
4. **Categories**: Grouped by scripture reference (e.g., "Job 1", "Job 19", "Job 38")

## Article Types
| Type | Description |
|------|-------------|
| Scholarly Articles | Peer-reviewed from BYU Studies Quarterly |
| Sperry Symposium Classics | Conference proceedings on OT topics |
| Ensign Articles | General audience articles from Ensign/Liahona |
| Book Excerpts | From BYU Studies publications |
| Encyclopedia Entries | From Encyclopedia of Mormonism |

## Scraping Notes
- Page is JavaScript-rendered; use browser automation
- Articles load dynamically; wait for content
- Some articles require BYU Studies subscription
- Look for `data-article-id` or similar attributes
- Article previews often truncated; click "Read More" for full text

## Key Article Categories by Scripture Book

### Job
- Theological discussions on suffering
- Literary structure analysis
- Hebrew word studies (*ha-satan*, *go'el*, *riyb*)
- Restoration perspectives on suffering
- Temple/journey symbolism in daughters' names

### Psalms
- Psalms as temple hymnal
- Messianic prophecies (Ps 2, 22, 110)
- Literary structures (acrostics, chiasmus)
- Music in ancient worship
- Shepherd imagery (Ps 23)
- Temple ascent (Ps 24, 84)
- Lament vs. praise patterns

### Genesis
- Creation accounts
- Abrahamic covenant
- Joseph narrative
- Temple themes in patriarchal narratives

### Isaiah
- Messianic prophecies
- Temple symbolism
- Covenant theology
- Restoration fulfillment

## Search Tips
1. **Direct URL**: Use lesson number mapping above
2. **Search**: `site:byustudies.byu.edu "come follow me" [scripture]`
3. **Author search**: `site:byustudies.byu.edu "Shon Hopkin" Job`
4. **Topic search**: `site:byustudies.byu.edu "kinsman redeemer" Psalms`

## Citation Format for Study Guides
```markdown
**BYU Studies — Come Follow Me Week 33 (Job)**
- "The Book of Job as a Biblical 'Guide of the Perplexed'" — Raphael Jospe (2014)
- "The Theology of Bristlecone Pines: Reflections on Job" — Steve Peck (2026)
- "Hast Thou Considered My Servant Job?" — John S. Tanner (2005)
- "A Precious and Powerful Witness of Jesus Christ" — John M. Madsen (2005)

**BYU Studies — Come Follow Me Week 34 (Psalms)**
- "Psalm 22: The Psalm of the Cross" — Shon D. Hopkin (2013)
- "The Psalms Sung: The Power of Music in Sacred Worship" — J. Arden Hopkin & Shon D. Hopkin (2013)
- "Seeing God in His Temple" — Andrew C. Skinner (2013)
- "Temple Worship and a Possible Reference to a Prayer Circle in Psalm 24" — Donald W. Parry (1992)
```

## API/Automation
- No public API available
- Use browser automation (browser-use, Playwright, Selenium)
- Respect robots.txt and rate limits
- Cache results locally for reuse

## Update Notes
- New articles added throughout the year
- Check for updates before each lesson week
- Some articles published after lesson week (retrospective)
- Archive older years at `https://byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]?year=2025`