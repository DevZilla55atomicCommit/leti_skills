# GC Talk URL Patterns

## General Conference Talk URLs

### Current Format (2020+)
```
https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}/{talk-id}?lang=eng
```

### Components
- **year**: 4-digit year (2026, 2025, etc.)
- **month**: 2-digit month (01=January, 04=April, 10=October)
- **talk-id**: Unique identifier (often speaker initials + number, e.g., `18becerra`, `15nelson`)

### Examples
- April 2026: `https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng`
- October 2025: `https://www.churchofjesuschrist.org/study/general-conference/2025/10/15nelson?lang=eng`
- April 2024: `https://www.churchofjesuschrist.org/study/general-conference/2024/04/12holland?lang=eng`

### Legacy Format (pre-2020)
```
https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}/{speaker-lastname}?lang=eng
```

### Session Identifiers
- **Saturday Morning**: `sat-am` or `saturday-morning`
- **Saturday Afternoon**: `sat-pm` or `saturday-afternoon`
- **Sunday Morning**: `sun-am` or `sunday-morning`
- **Sunday Afternoon**: `sun-pm` or `sunday-afternoon`

### Speaker Biography URLs
```
https://www.churchofjesuschrist.org/learn/{speaker-slug}
```
Example: `https://www.churchofjesuschrist.org/learn/jorge-t-becerra`

### Search URLs
```
https://www.churchofjesuschrist.org/search?q={query}&facet=general-conference
```
Example: `https://www.churchofjesuschrist.org/search?q=tithing+consecration&facet=general-conference`