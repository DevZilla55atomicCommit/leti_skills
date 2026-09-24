---
name: sports-tournament-tracking
description: Track live sports tournaments (World Cup, Olympics, major leagues) — fetch current standings, fixtures, results, and qualification status from authoritative sources. Handles dynamic data that changes daily during active tournaments.
category: research
triggers:
  - User asks for current tournament status, standings, or fixtures
  - User wants qualification updates for major tournaments
  - Live match results needed during active competition
  - Cross-referencing multiple sports sources for accuracy
---

# Sports Tournament Tracking

## Purpose
Systematic approach to fetching, verifying, and presenting live sports tournament data from authoritative sources. Handles the challenge of dynamic data that updates daily during active competitions.

## Core Workflow

### 1. Identify Authoritative Sources (Priority Order)
| Tier | Sources | Use Case |
|------|---------|----------|
| **Primary** | FIFA.com, UEFA.com, IOC, official league sites | Official schedules, standings, qualifications |
| **Secondary** | Wikipedia (tournament pages) | Structured historical + current data, group tables, brackets |
| **Tertiary** | BBC Sport, ESPN, Reuters, AP News | Live match updates, breaking news, analysis |
| **Verification** | Cross-reference 2+ sources before reporting | Eliminate stale/cached data |

### 2. Data Extraction Patterns

**Wikipedia Tournament Pages** (most reliable structured data):
- URL pattern: `https://en.wikipedia.org/wiki/{Year}_{Tournament}_qualification` or `https://en.wikipedia.org/wiki/{Year}_{Tournament}`
- Key anchors: `#Qualified_teams`, `#Format`, `#Group_stage`, `#Knockout_stage`, `#Schedule`
- Use `browser_console` with DOM queries to extract tables directly:
  ```javascript
  document.querySelector('#Qualified_teams').parentElement.parentElement.innerText
  ```

**Official Federation Sites** (FIFA, UEFA):
- Often have cookie walls / bot detection — use `browser_click` on consent buttons first
- Navigate to `/tournaments/mens/worldcup/{year}/qualifiers` or `/matches`
- Prefer `browser_snapshot(full=true)` over visual for structured data

**Live Match Sources** (BBC, ESPN):
- BBC: `https://www.bbc.com/sport/football/world-cup` — check "LIVE UPDATES" section
- ESPN: League-specific pages often redirect to Women's WC — use direct tournament URLs
- Element clicking often fails on dynamic content — use `browser_console` to extract text content

### 3. Verification Protocol
- **Never trust a single source** for live data
- Cross-check: Wikipedia (structure) + Official site (authority) + News (live updates)
- Note timestamps: "as of {date}" on all live data
- Flag projected vs. confirmed dates (Wikipedia often shows projected knockout dates)

### 4. Output Format Standards
- **Tables** for standings, groups, fixtures (Markdown pipe syntax)
- **Key storylines** section for narrative context
- **Schedule overview** with upcoming milestones
- **Venue/broadcast info** if user is in specific region (US default)

## Tool Usage Patterns

| Task | Preferred Tool | Fallback |
|------|----------------|----------|
| Structured tournament data (groups, brackets) | `browser_navigate` → `browser_console` DOM extraction | `browser_snapshot(full=true)` |
| Live match updates | `browser_navigate` to BBC/ESPN → `browser_snapshot` | `browser_console` text extraction |
| Official qualification lists | FIFA.com → consent click → scroll → snapshot | Wikipedia qualification page |
| Historical context | Wikipedia tournament page | Official archive |

## Common Pitfalls & Fixes

| Pitfall | Fix |
|---------|-----|
| FIFA.com shows "referee" error page | Click "I'm OK with that" (consent), then scroll |
| ESPN redirects to Women's WC | Use `https://www.espn.com/soccer/fifa-world-cup` not `/league/_/name/fifa.wwc/` |
| BBC element clicks fail (CDP error) | Use `browser_console` to extract `innerText` from known selectors |
| Wikipedia shows projected future dates | Label as "projected" — actual dates confirmed after draw |
| Stale qualification data | Check page "last edited" timestamp; prefer official source for final teams |
| Dynamic content not in snapshot | Use `browser_console` with `document.querySelector` on known IDs |

## Source-Specific Selectors (Quick Reference)

**Wikipedia 2026 WC:**
- Qualified teams: `#Qualified_teams` → parent → `innerText`
- Format/schedule: `#Format` → parent → `innerText`
- Knockout bracket: `#Knockout_stage` → parent → `innerText`
- Group tables: `#Group_stage` → parent → `innerText`

**BBC Sport:**
- Live updates container: `heading "LIVE UPDATES"` → following siblings
- Match links: look for `ref` elements with "LIVE" prefix
- Live match articles: direct navigation to `/sport/football/live/...` URLs
- Element clicks fail (CDP error) — use `browser_console` text extraction

**FIFA.com:**
- Consent button: `button "I'm OK with that"` (usually `@e22`)
- Qualifiers page: `/en/tournaments/mens/worldcup/2026/qualifiers`

**ESPN Scoreboard:**
- URL: `https://www.espn.com/soccer/scoreboard/_/league/fifa.world`
- Date selector: combobox `Sports Dates` with options for each day
- Match cards: `.Scoreboard__Card` (generic structure)
- Team names: `.Scoreboard__TeamName`
- Scores: `.Scoreboard__Score`
- Status: `.Scoreboard__Status` (shows "FT", "LIVE", time)
- Reliable for final scores — check "FT" status

### ESPN Scoreboard (Live Final Scores) — Detailed Extraction
- URL: `https://www.espn.com/soccer/scoreboard/_/league/fifa.world`
- Use date selector combobox `Sports Dates` to pick match day
- Match cards show: team names, scores, status (FT/LIVE/time)
- Extract via `browser_snapshot(full=true)` — snapshot captures score text reliably
- Console extraction for structured data:
  ```javascript
  document.querySelectorAll('main main .Scoreboard__Card').forEach(card => {
    const teams = card.querySelectorAll('.Scoreboard__TeamName');
    const scores = card.querySelectorAll('.Scoreboard__Score');
    const status = card.querySelector('.Scoreboard__Status');
    if (teams.length >= 2 && scores.length >= 2) {
      console.log(`${teams[0].textContent} ${scores[0].textContent} - ${scores[1].textContent} ${teams[1].textContent} | ${status?.textContent || 'Live'}`);
    }
  });
  ```

## Lessons Learned (Updated July 2026)
1. **Wikipedia is the most reliable structured source** during active tournaments — editors update in near real-time
2. **DOM extraction via browser_console** beats snapshot parsing for large tables
3. **Official sites have bot detection** — consent walls, Cloudflare/DataDome challenges
4. **BBC dynamic content** — element clicks fail; use console text extraction
5. **ESPN URL structure** — avoid `/league/_/name/fifa.wwc/` (Women's WC); use direct tournament path
6. **Projected dates on Wikipedia** — knockout dates before draw are projections; label clearly
7. **Cross-reference minimum 2 sources** — Wikipedia + BBC + official for live data
8. **ESPN scoreboard** — reliable for final scores during active tournament; use date selector for historical match days
9. **Round of 16 data updates rapidly** — capture timestamp on every query; BBC live pages give fastest narrative updates

## Skill Maintenance
- Update selectors when sites redesign (check annually before major tournaments)
- Add new tournament patterns as they emerge (e.g., expanded 48-team format)
- Document any API endpoints discovered for programmatic access