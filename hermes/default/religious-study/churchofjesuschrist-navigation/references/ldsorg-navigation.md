# LDS.org Navigation Reference

## URLs Visited
- https://www.churchofjesuschrist.org/topics (404/503 errors)
- https://www.churchofjesuschrist.org/life-help (404)
- https://www.churchofjesuschrist.org/media (empty)
- https://www.churchofjesuschrist.org/study/music (empty)
- https://www.churchofjesuschrist.org/study (main library)
- https://www.churchofjesuschrist.org/study/handbooks (404)
- https://www.churchofjesuschrist.org/study/general-handbook (404)
- https://www.churchofjesuschrist.org/resources/all (404)
- https://www.churchofjesuschrist.org/all-resources (503)
- https://www.churchofjesuschrist.org (main homepage)
- https://newsroom.churchofjesuschrist.org (newsroom)

## Snapshot Details (study page)
- element_count: 18
- Key element refs:
  - e2: link "Notes"
  - e3: button "Study Sets"
  - e4: button "Bookmarks"
  - e5: button "Options"
  - e6: heading "Music Resources"
  - e7: link "Hymns for Home and Church"
  - e8: link "Hymns"
  - e9: link "Children’s Songbook"
  - e10: link "Conference Music"
  - e11: link "Youth Music"
  - e12: link "Songs of Devotion"
  - e13: link "Christmas"
  - e14: link "Sing-Along Videos"
  - e15: link "Hymn Helps"

## Common Pitfalls
- Many sections return 404/503; always verify with `browser_snapshot` before proceeding.
- JavaScript-heavy pages may need a short `seconds` wait before elements render.
- Element indices can shift after interaction; re‑capture to confirm stability.
- Rapid successive clicks can trigger rate‑limit warnings; add a `seconds` pause if needed.
- Empty pages (e.g., `/media`, `/study/music`) yield `element_count: 0`; skip or re‑navigate.

## Verification Checklist
1. After each `browser_click`, re‑capture to ensure `effect: 'confirmed'`.
2. Use `browser_snapshot` to verify expected headings/titles appear and `element_count` > 0.
3. If verification fails, consider `browser_scroll` or re‑navigate.