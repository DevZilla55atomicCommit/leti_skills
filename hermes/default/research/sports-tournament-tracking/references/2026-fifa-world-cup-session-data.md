# 2026 FIFA World Cup — Session Reference Data

*Captured: July 6, 2026 (during Round of 16)*

## Source URLs Accessed
| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| Wikipedia Qualification | `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification#Qualified_teams` | ✅ Success | 48 qualified teams extracted via DOM query |
| Wikipedia Tournament | `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup` | ✅ Success | Format, schedule, group stage, knockout bracket extracted |
| FIFA Official | `https://www.fifa.com/en/tournaments/mens/worldcup/2026/qualifiers` | ⚠️ Partial | Consent wall, "referee" error page, limited data |
| BBC Sport | `https://www.bbc.com/sport/football/world-cup` | ✅ Success | Live updates, match reports, R32 results visible |
| ESPN | `https://www.espn.com/soccer/fifa-world-cup` | ❌ Failed | Redirects to Women's WC |

## Extraction Techniques That Worked

### Wikipedia DOM Queries (Most Reliable)
```javascript
// Qualified teams table
document.querySelector('#Qualified_teams').parentElement.parentElement.innerText

// Format, schedule, rules
document.querySelector('#Format').parentElement.parentElement.innerText

// Knockout bracket & results
document.querySelector('#Knockout_stage').parentElement.parentElement.innerText

// Group stage tables & results
document.querySelector('#Group_stage').parentElement.parentElement.innerText
```

### BBC Sport
- Page loads "LIVE UPDATES" section with match links
- Element clicking fails (CDP error) — use console extraction instead
- Match reports accessible via direct navigation to article URLs

### FIFA.com
- Must click consent: `button "I'm OK with that"` (ref `@e22`)
- Then scroll to load content
- Qualifiers page has limited structured data in snapshot

## Verified Tournament State (as of July 6, 2026 — Updated July 7, 2026)

### Completed Stages
- ✅ Group Stage: June 11–27
- ✅ Round of 32: June 28 – July 3

### Current Stage
- 🔴 Round of 16: July 4–7 (in progress — **2 matches completed**)

### Upcoming
- Quarterfinals: July 9–11
- Semifinals: July 14–15
- 3rd Place: July 18
- Final: July 19 (MetLife Stadium)

### Key Results Extracted

**Round of 32 Winners:**
| Match | Winner | Score | Notes |
|-------|--------|-------|-------|
| South Africa vs Canada | **Canada** | 1–0 (90+2') | Eustáquio |
| Brazil vs Japan | **Brazil** | 2–1 | Casemiro, Martinelli |
| Germany vs Paraguay | **Paraguay** | 1–1 (3–4 pens) | Germany out early |
| Netherlands vs Morocco | **Morocco** | 1–1 (2–3 pens) | Giant killing |
| Ivory Coast vs Norway | **Norway** | 2–1 | Haaland 86' |
| France vs Sweden | **France** | 3–0 | Mbappé brace |
| Mexico vs Ecuador | **Mexico** | 2–0 | Quiñones, Jiménez |
| England vs DR Congo | **England** | 2–1 | Kane brace |
| Belgium vs Senegal | **Belgium** | 3–2 (a.e.t.) | Tielemans 2 pens |
| USA vs Bosnia & Herzegovina | **USA** | 2–0 | Balogun, Tillman |
| Spain vs Austria | **Spain** | 3–0 | Oyarzabal brace |
| Portugal vs Croatia | **Portugal** | 2–1 | |

**Round of 16 — Completed (as of July 7):**
| Match | Winner | Score | Venue | Notes |
|-------|--------|-------|-------|-------|
| Paraguay vs France | **France** | 1–0 | Lincoln Financial Field, Philadelphia | |
| Canada vs Morocco | **Morocco** | 2–1 (a.e.t.) | NRG Stadium, Houston | Morocco giant-kill continues |

**Round of 16 — Remaining Fixtures:**
- Jul 5: Brazil vs Norway (MetLife Stadium, East Rutherford)
- Jul 5: Mexico vs England (Estadio Azteca, Mexico City)
- Jul 6: Portugal vs Spain (AT&T Stadium, Arlington) — *Iberian derby*
- Jul 6: USA vs Belgium (Lumen Field, Seattle) — **USA eliminated 0–2** (BBC live)
- Jul 7: Argentina vs Egypt (Mercedes-Benz Stadium, Atlanta)
- Jul 7: Switzerland vs Colombia (BC Place, Vancouver)

**Quarterfinals Set (Partial):**
- France vs Morocco (July 9, Gillette Stadium, Foxborough)
- Winner Brazil/Norway vs Winner Mexico/England (July 10, SoFi Stadium, Inglewood)
- Winner Portugal/Spain vs Winner USA/Belgium (July 11, Hard Rock Stadium, Miami Gardens)
- Winner Argentina/Egypt vs Winner Switzerland/Colombia (July 11, Arrowhead Stadium, Kansas City)

## Format Changes for 2026 (Critical Context)
- **48 teams** (12 groups of 4) — first expansion since 1998
- **104 matches** (was 64)
- **Round of 32** new — top 2 + 8 best 3rd place advance
- **8 matches** for finalist (was 7)
- **39 days** (was 32)
- New rules: 10-sec subs, 5-sec restarts, medical 1-min rule, expanded VAR, mouth-cover red cards
- Tiebreaker: head-to-head points first (not GD)

## Broadcast (US)
- English: FOX / FS1
- Spanish: Telemundo / Universo / Peacock
- Streaming: FIFA+, Fubo, YouTube TV, Hulu + Live TV

## Selectors for Future Automation
| Target | Selector | Method |
|--------|----------|--------|
| Qualified teams table | `#Qualified_teams` → parent → parent | `browser_console` innerText |
| Format/schedule | `#Format` → parent → parent | `browser_console` innerText |
| Knockout bracket | `#Knockout_stage` → parent → parent | `browser_console` innerText |
| Group tables | `#Group_stage` → parent → parent | `browser_console` innerText |
| BBC live match links | Heading "LIVE UPDATES" → following siblings | snapshot + console |

## Lessons Learned
1. **Wikipedia is the most reliable structured source** during active tournaments — editors update in near real-time
2. **DOM extraction via browser_console** beats snapshot parsing for large tables
3. **Official sites have bot detection** — consent walls, Cloudflare/DataDome challenges
4. **BBC dynamic content** — element clicks fail; use console text extraction
5. **ESPN URL structure** — avoid `/league/_/name/fifa.wwc/` (Women's WC); use direct tournament path
6. **Projected dates on Wikipedia** — knockout dates before draw are projections; label clearly
7. **Cross-reference minimum 2 sources** — Wikipedia + BBC + official for live data