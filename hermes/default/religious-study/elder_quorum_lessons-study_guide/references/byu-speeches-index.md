# BYU Speeches Index

## Search Patterns for BYU Speeches

### Site Search URL
```
https://speeches.byu.edu/?s={query}
https://speeches.byu.edu/search/?q={query}
```

### Speaker-Specific URLs
```
https://speeches.byu.edu/speakers/{speaker-slug}/
```

### Topic/Category URLs
```
https://speeches.byu.edu/topics/{topic-slug}/
```

### Date-Based URLs
```
https://speeches.byu.edu/{year}/{month}/{day}/
```

## Key Search Queries for Tithing/Consecration Themes

| Query | Expected Results |
|-------|-----------------|
| `tithing` | Talks on law of tithing, D&C 119, blessings |
| `consecration` | Higher law, all things dedicated |
| `law of sacrifice` | Sacrifice from Adam to Christ |
| `firstlings` | Firstfruits, Adam's offering |
| `windows of heaven` | Malachi 3:10, spiritual blessings |
| `double-mindedness` | James 1:8, single eye |
| `seek ye first` | Matthew 6:33, priorities |
| `obedience` | First law of heaven |
| `covenants` | Covenant keeping, signs |

## Notable Speakers on These Topics

| Speaker | Expertise | Notable Talks |
|---------|-----------|---------------|
| **Russell M. Nelson** | Tithing, Sacrifice, Consecration | "The Law of Tithing", "The Law of Sacrifice", "Firstlings of the Flock" |
| **David A. Bednar** | Windows of Heaven, Spiritual Capacity | "The Windows of Heaven" |
| **Neal A. Maxwell** | Consecration, Sacrifice, Discipleship | "Consecration: The Only Way to Happiness" |
| **Dieter F. Uchtdorf** | Priorities, First Things First | "Seek Ye First the Kingdom of God", "First Things First" |
| **Gordon B. Hinckley** | Tithing, Practical Faith | "Tithing" (GA Training), "The Blessings of Tithing" |
| **James E. Faust** | Blessings of Tithing | "The Blessings of Tithing" |
| **Robert D. Hales** | Tithing as Test of Faith | "The Law of Tithing", "Tithing: A Test of Faith" |
| **Jeffrey R. Holland** | Double-Mindedness, Single Eye | "Double-Mindedness and the Single Eye" |
| **Bruce R. McConkie** | Obedience | "Obedience: The First Law of Heaven" |
| **D. Todd Christofferson** | Covenants | "Covenants", "The Power of Covenants" |
| **M. Russell Ballard** | Sacrifice and Consecration | "Sacrifice and Consecration" |
| **Ezra Taft Benson** | Mighty Change of Heart | "A Mighty Change of Heart" |

## Talk Types

| Type | Description | Length | Best For |
|------|-------------|--------|----------|
| **Devotional** | Weekly BYU devotional | 30-45 min | Doctrinal depth, personal application |
| **Forum** | BYU Forum address | 45-60 min | Broader audience, intellectual rigor |
| **General Conference** | GC talks mirrored on BYU | 10-20 min | Authoritative, prophetic |
| **Education Week** | BYU Education Week | 60-90 min | Deep scholarly treatment |
| **Scholarly/Symposium** | Academic conferences | 45-90 min | Historical/contextual analysis |

## Filtering Tips

### By Date
- Recent talks (2010+) have video + transcript
- Older talks may have only transcript or audio
- Use "Sort by: Newest" for current prophetic emphasis

### By Topic Tags
BYU Speeches uses tags like:
- `tithing`, `consecration`, `sacrifice`, `firstlings`
- `malachi`, `windows-of-heaven`, `dc-119`
- `obedience`, `covenants`, `blessings`
- `adam`, `firstfruits`, `double-mindedness`

### By Scripture Reference
Search for specific verses:
- `malachi 3:10`, `matthew 6:33`, `james 1:8`
- `dc 119`, `moses 5`, `alma 5:12`, `alma 7:18`

## Curated BYU Speeches for Tithing/Consecration

| Title | Speaker | Date | Type | URL | Topics |
|-------|---------|------|------|-----|--------|
| The Law of Tithing | Robert D. Hales | 1998-10-06 | Devotional | `/talks/robert-d-hales/law-tithing/` | tithing, obedience |
| The Windows of Heaven | David A. Bednar | 2013-11-12 | Devotional | `/talks/david-a-bednar/windows-heaven/` | windows_heaven, tithing |
| Consecration: The Only Way to Happiness | Neal A. Maxwell | 1975-10-14 | Devotional | `/talks/neal-a-maxwell/consecration-way-happiness/` | consecration, sacrifice |
| Firstlings of the Flock | Russell M. Nelson | 2022-03-29 | Devotional | `/talks/russell-m-nelson/firstlings-flock/` | firstlings, Adam |
| Seek Ye First the Kingdom of God | Dieter F. Uchtdorf | 2017-01-10 | Devotional | `/talks/dieter-f-uchtdorf/seek-ye-first-kingdom-god/` | put_god_first |
| Double-Mindedness and the Single Eye | Jeffrey R. Holland | 1995-03-21 | Devotional | `/talks/jeffrey-r-holland/double-mindedness-single-eye/` | double_mindedness |
| The Law of Sacrifice | Russell M. Nelson | 2011-10-01 | General Conference | `/talks/russell-m-nelson/law-sacrifice/` | consecration, firstlings |
| Tithing: A Test of Faith | James E. Faust | 1998-04-05 | General Conference | `/talks/james-e-faust/blessings-tithing/` | tithing, blessings |
| Obedience: The First Law of Heaven | Bruce R. McConkie | 1972-02-22 | Devotional | `/talks/bruce-r-mcconkie/obedience-first-law-heaven/` | obedience |
| Covenants and Sacraments | D. Todd Christofferson | 2009-10-03 | General Conference | `/talks/d-todd-christofferson/covenants/` | covenants |

## API/Programmatic Access

BYU Speeches doesn't have a public API, but you can:
1. Use the search URL with `requests` + BeautifulSoup
2. Parse the JSON-LD structured data on talk pages
3. Use the sitemap: `https://speeches.byu.edu/sitemap.xml`

## Citation Format for Study Guides
```markdown
**BYU Speeches — {Speaker} ({Date}) — {Type}**
- {Key Insight 1}
- {Key Insight 2}
- {URL}
```