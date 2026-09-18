# Sports Data Sources for Dashboards

## Tier 1: Reliable Structured APIs

### ESPN (Best for Live Scores)
```
Base: https://site.api.espn.com/apis/site/v2/sports/soccer
Scoreboard: /soccer/scoreboard?league=fifa.world&dates=20260705
Standings: /soccer/standings?league=fifa.world
Team: /soccer/teams/{id}
Match: /soccer/summary?event={eventId}
```
- No auth required for basic endpoints
- JSON responses, well-documented structure
- Rate limits: ~180 req/min (respectful use)
- CORS allowed from browsers

### FIFA.com (Official but Protected)
- Heavy Cloudflare/DataDome bot protection
- Not suitable for automated scraping
- Use only for manual reference

## Tier 2: Semi-Structured Sources

### Wikipedia (Historical/Qualification Data)
```
2026 Qualification: https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification
2026 Tournament: https://en.wikipedia.org/wiki/2026_FIFA_World_Cup
```
- Stable URLs, well-structured tables
- Use `#Qualified_teams` anchor for direct section access
- Parse with `document.querySelector('table.wikitable')` or similar
- No rate limits but be respectful

### BBC Sport (Narratives + Some Scores)
```
https://www.bbc.com/sport/football/world-cup
```
- Good for match reports, analysis
- HTML structure changes occasionally
- Live text commentaries have structured data attributes

## Tier 3: Manual/Reference Only

### The Guardian, Sky Sports, Reuters
- Paywalls, dynamic JS, anti-scraping
- Use for qualitative context only

## Extraction Patterns

### ESPN Scoreboard (Live Matches)
```javascript
// From browser console or headless
const matches = document.querySelectorAll('.Scoreboard__Card');
matches.forEach(card => {
  const teams = [...card.querySelectorAll('.Scoreboard__TeamName')].map(t => t.textContent);
  const scores = [...card.querySelectorAll('.Scoreboard__Score')].map(s => s.textContent);
  const status = card.querySelector('.Scoreboard__Status')?.textContent;
  console.log({ teams, scores, status });
});
```

### Wikipedia Qualified Teams Table
```javascript
const table = document.querySelector('#Qualified_teams + table.wikitable');
const rows = [...table.querySelectorAll('tr')].slice(1);
rows.forEach(row => {
  const cells = [...row.querySelectorAll('td, th')].map(c => c.textContent.trim());
  // cells = [Team, Method, Date, Apps, Last, Streak, Best]
});
```

## Caching Strategy for Dashboards

| Data Type | TTL | Source |
|-----------|-----|--------|
| Live scores | 30 sec | ESPN scoreboard |
| Match events | 60 sec | ESPN match summary |
| Standings | 5 min | ESPN standings |
| Qualified teams | 1 hour | Wikipedia |
| Historical stats | 24 hr | Wikipedia/ESPN |

## CORS Workaround for Local Files
When opening `file://` dashboard:
- Use a local server: `npx serve` or `python -m http.server`
- Or disable CORS in browser (dev only): `--disable-web-security`

## Rate Limit Handling
```javascript
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    const res = await fetch(url);
    if (res.ok) return res.json();
    if (res.status === 429) await new Promise(r => setTimeout(r, 1000 * (i+1)));
  }
  throw new Error('Max retries');
}
```