---
name: come-follow-me-study-guide
title: Come Follow Me Weekly Study Guide Creation
description: Create Come Follow Me guides with Gospel Library links.
category: religious-study
tags: [come-follow-me, lds, study-guide, gospel-library, podcast, byu-studies, html, pdf]
---

# Come Follow Me Weekly Study Guide Creation

## Trigger
Use when the user wants a comprehensive weekly study guide for the Come Follow Me curriculum (Old Testament, New Testament, Book of Mormon, Doctrine & Covenants). Activated by requests like "create study guide for [scripture block]", "this week's Come Follow Me lesson", or "weekly lesson guide with podcasts".

## Prerequisites
- Access to churchofjesuschrist.org for official lesson
- BYU Studies Come Follow Me index (byustudies.byu.edu/come-follow-me)
- followHIM Podcast (YouTube or followhim.co)
- Optional: Don't Miss This, Scripture Insights, Certain Women, Latter-Day Insight, Unshaken, Line Upon Line

## Workflow

### 1. Fetch Official Lesson
Navigate to lesson page:
`https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-[volume]-[year]/[lesson-number]?lang=eng`

**Lesson number = Church URL number, verified by page title.** The date-math formula is only a URL guess and runs ~1 behind Church numbering (verified: Church lesson 38 = Sep 14–20, 2026 = formula week 37; lesson 37 = Sep 7–13 Proverbs). Example: 2026 Old Testament:
- Lesson 37 = Sep 7-13 (Proverbs)
- Lesson 38 = Sep 14-20 (Isaiah 1-12, “God Is My Salvation”)

**To find the correct lesson for a date**:
1. Guess with the formula: `(target_date - first_monday_of_jan).days // 7 + 2` (the +2 corrects the off-by-one; e.g., Jan 5, 2026 → lesson 38 ≈ Sep 14-20)
2. Open the guessed URL and **confirm via the page title/date before generating** — the title is authoritative, the formula is not.

Extract:
- All "Ideas for Learning at Home and Church" questions
- "Scripture Helps" questions
- "Ideas for Teaching Children"
- **Hero image**: Select the most appropriate content image from the lesson page. The first `<img>` with `data-assetId` and lesson-relevant alt text/title is usually the best candidate. Prefer images with titles like "Young Men Discuss the Scriptures", "Watchman on the Tower", "Come Unto Christ", "Pool of Bethesda", or other content-relevant images over generic banner images (like year banners or icons). Example: `https://www.churchofjesuschrist.org/imgs/25b1565c0e5611efa383eeeeac1eb9023c30de14/full/%21500%2C/0/default`
- Download and save as `topic_lesson_header.png` in the lesson folder

### 2. Fetch Supplemental Resources
| Source | URL Pattern | Key Content |
|--------|-------------|-------------|
| BYU Studies | `https://byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]` | Scholarly articles per scripture block |
| followHIM Podcast | `https://followhim.co/[volume]-[year]` or YouTube `@followHIM` | Expert commentary, Hebrew insights |
| Don't Miss This | YouTube `Don't Miss This` | Dave & Cali Black, practical application |
| Scripture Insights | YouTube `Scripture Insights` | Taylor Halverson & Mike Harris, structural analysis |
| Certain Women | YouTube `Certain Women Podcast` | Women's perspectives, shepherd/sheep imagery |
| Latter-Day Insight | YouTube `Latter-Day Insight` | 5-act structure, thematic organization |

### Preview Gate (required — preview before you build)
Render the week's pipeline plan (lesson title/date verified from the official page, folder path, sections to generate, supplements to fetch) as HTML, open it in the preview pane, and wait for user approval — never create folders, fetch supplements, or generate HTML/PDF until the preview is approved, because rebuilding a wrong-week guide wastes a full fetch+render cycle.

### 3. Create Folder Structure (Monthly Organization)
```
/Users/alfredkamisese/Desktop/Come Follow Me 2026/
└── MMM/
    └── Week N - Topic - Month Day–Day, Year/
        ├── Topic_Lesson_Final.pdf
        ├── Topic_Lesson_Final.html (temp render source — delete after PDF when deliverable is PDF-only)
        ├── topic_lesson_header.png
        ├── topic_timeline.png (if applicable)
        ├── topic_flowchart.png (if applicable)
        └── topic_daughters_temple.png (if applicable)
```
Naming: `Week N - Topic - Month Day–Day, Year/` (e.g., `Week 38 - Isaiah 1-12 - September 14–20, 2026/`)

**Folder naming convention** (matches on-disk reality — no `/2026/` level, filed under the end-date month):
- **Week N**: **Church lesson number**, not computed week-of-month (lesson 38, not “week 3”)
- **Topic**: Scripture block, no spaces, hyphens preserved (Isaiah1-12, Job)
- **DateRange**: Full month names with spaces (`September 14–20, 2026`)

**Full path**: `~/Desktop/Come Follow Me 2026/MMM/Week N - Topic - Month Day–Day, Year/`

**Output files**: PDF is the deliverable; HTML is the required render source (Chrome headless) — keep both, or delete the HTML after the PDF lands when the user asks for PDF-only.

### 4. Generate HTML Study Guide
Template structure with sections:
1. **Hero Image** - Official Church artwork
2. **Core Message** - 3-sentence summary + takeaway box
3. **Every Lesson Question** - Each official question answered simply with scripture refs, and every answer must explain WHY the cited scripture answers the question (the mechanism: why this verse resolves this question, how the principle transfers to the reader) — never a bare quote plus citation
4. **Children's Teaching Table** - Kid-level answers
5. **Podcast Insights** - 7+ sources, key quotes, chapter lists
6. **BYU Studies Articles** - Table with article, author, key insight — use real titles/authors pulled from the BYU Studies lesson page (`byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]`), never hand-written generic summaries; link each row to the lesson page
7. **Deep Doctrine Addendum** - Scholarly insights beyond core lesson
8. **One-Page Cheat Sheet** - 12-card grid for class reference
9. **Scripture Helps** - Extra questions from lesson
10. **Sources & Footer**

**Preview/pipeline HTML styling (standing preference):** color-code each section card with an explicit light background, dark text, and a saturated left-border accent — theme CSS vars alone inherit the desktop app's dark mode and wash out to unreadable gray; prefer colorful section-coded cards over plain white.

### 5. Inject Clickable Gospel Library Links (CRITICAL)
**Process HTML with interval-based protection to avoid corrupting CSS/styles:**

1. Identify protected intervals: `<style>...</style>`, `<script>...</script>`, `href="..."`, `src="..."`
2. Merge overlapping intervals
3. Only replace scripture references in unprotected "free regions"
4. Use exact reference strings with word-boundary regex: `(?<![\w\"])({ref_text})(?![\w\"])`
5. Build URLs: `https://www.churchofjesuschrist.org/study/scriptures/ot/{path}/{chapter}?lang=eng&id={verse}`

**Book Path Map**:
```python
BOOK_PATHS = {
    'job': 'job', 'ps': 'ps', 'gen': 'gen', 'isa': 'isa', 'matt': 'matt',
    'luke': 'luke', 'jn': 'jn', 'acts': 'acts', 'rom': 'rom', '1-jn': '1-jn',
    'rev': 'rev', '2-ne': '2-ne', 'mosiah': 'mosiah', 'alma': 'alma',
    'ether': 'ether', 'dc': 'dc', 'moses': 'moses', 'abr': 'abr', 'zech': 'zech',
}
```

### 6. Export to PDF
Preferred path (verified): WeasyPrint via `~/.hermes/scripts/generate_cfm_pdf.sh` (see `references/weasyprint-pdf-render.md` for wrapper setup, print-CSS constraints, and the per-page verification probe) — then verify with a text-extraction page-count check before deleting any temp HTML. After every build, open the finished PDF in the preview pane and report week ID, path, page count, and placeholder count — the user reviews in preview, not in chat.
Manual path: open HTML in browser → `Cmd+P` → Save as PDF → AirDrop to phone → Open in Apple Books.
Legacy automated path: render headless with Chrome so cron builds never need a GUI — `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-sandbox --print-to-pdf="<name>.pdf" --print-to-pdf-no-header <file>.html` — kept as fallback only; WeasyPrint output is the house standard.

## Podcast Source Priority (2026 Season)
1. **followHIM** (current season) - Primary, expert guests
2. **Scripture Insights** (Halverson/Harris) - Structural analysis, temple themes
3. **Don't Miss This** - Practical application, "playlist" metaphor
4. **Certain Women** - Women's voices, shepherd/sheep, grace perspective
6. **Latter-Day Insight** - 5-act structure, thematic acts
6. **Previous season followHIM** (Dr. Shon Hopkin) - Psalm 22, music in worship

## Deep Doctrine Addendum Topics (when applicable)
- Courtroom language (*riyb*, *ed*, *go'el*, *melitz*)
- Satan as *ha-satan* (Accuser role vs. name)
- *Go'el* = Kinsman-Redeemer (3 duties: buy back, avenge, restore)
- Two Heavens (Premortal Council vs. Whirlwind Perspective)
- Eve/Job's wife parallel (shortcut vs. covenant faithfulness)

## Folder Naming Convention
Authoritative form (matches on-disk folders): `Week N - Topic - Month Day–Day, Year`
Examples:
- `Week 37 - Proverbs - September 7–13, 2026`
- `Week 38 - Isaiah 1-12 - September 14–20, 2026`
Older folders vary (`Week 3 - Job - Aug 10-16 2026`, compact `Aug31-Sep62026` forms) — follow the authoritative form for new builds; never invent a `/2026/` level under the root.
Comparison builds (two machines run the same cron job): suffix the folder with the machine tag, e.g. `Week 38 - Isaiah 1-12 - September 14–20, 2026 - Hermes Macbook/`, so competing outputs can be judged side by side before one is kept.

### Common Pitfalls
| Issue | Solution |
|-------|----------|
| **Wrong lesson number** | **Guess via date math, then confirm via the official page title/date — the Church URL number is authoritative.** The raw `(date - first_monday) // 7 + 1` formula runs ~1 behind Church numbering (lesson 38 = Sep 14–20, 2026), so never trust it blindly |
| **Wrong lesson fetched** | **Verify lesson title/date on the official page before generating — the Church lesson number in the URL is authoritative when it disagrees with the computed week number**; use the date-math formula only to guess the URL, then confirm via the page title |
| **Hero image not found / wrong image** | **Use the FIRST content image on the lesson page** (first `<img>` with `data-assetId` and lesson-relevant alt text/title); prefer titles like "Young Men Discuss the Scriptures", "Watchman on the Tower", "Come Unto Christ", "Pool of Bethesda" over generic banners/year banners |
| Podcast not yet posted | Check previous season (e.g., Dr. Shon Hopkin 2022 for Psalms) |
| Hero image path in HTML | Use relative path: `topic_lesson_header.png` |
| **Month/Week calculation wrong** | **Use END DATE (Sunday) to determine month and week-of-month; CFM weeks end on Sunday** (Aug 31-Sep 6 → September Week 1, not August Week 5) |
| **Wrong lesson URL** | **Guess `.../come-follow-me-for-home-and-church-[volume]-[year]/[n]?lang=eng` from date math, then verify the page title/date** — the URL number is authoritative only after the title confirms it (lesson 38 = “God Is My Salvation,” Sep 14–20) |
| **Wrong hero image selected** | **Use the FIRST content image** (first `<img>` with `data-assetId` and lesson-relevant alt/title); avoid year banners, icons, and later content images |
| Lesson title mismatch | **Verify lesson title/date on page title before generating** (e.g., lesson 37 = “Sep 7–13” Proverbs, lesson 38 = “Sep 14–20” Isaiah 1–12) |
| PDF-only deliverable requested | HTML is still the required render source — build it as a temp file in the folder, render the PDF, then delete the HTML so only the PDF remains; never skip the HTML stage, it is what the PDF is printed from. |
| Artwork caption scraped as a question | Treat caption-like scraped 'questions' (artist name, no question mark) as lesson artwork labels — answer the lesson's actual invitation for that section instead of the caption text. |
| Resolved QAs silently dropped from render | After resolving a string QA to a dict, render unconditionally — an `if isinstance(qa, str): ... else: render` structure skips resolved items; use a guard-`continue` for unresolved strings then a single render path. |
| Cover page flagged as blank by char-count probe | Exclude page 1 from the blank-page check — the image cover legitimately extracts to ~115 chars; only content pages near ~100 chars indicate a layout failure. |
| iCloud-evicted Desktop file unreadable (Resource deadlock avoided) | Check `ls -lO` for `dataless` flag and run `brctl download <path>` until the flag clears before reading — Desktop is iCloud-synced and evicted files fail every data read. |
| Placeholder answers left in guide | Extract PDF text and grep for `Answer not automatically extracted` after every build — the scraper returns plain-string questions while the WeasyPrint generator (`~/.hermes/scripts/cfm_pdf_generator.py::build_questions_html`) only answers dict-style QAs, so unmapped strings render placeholders; fix with a per-week answer map keyed by question substring, resolved before render. Normalize newlines to spaces before asserting any multi-word string's presence or absence — line breaks inside a page split matches and fake both passes and failures. |
| Scraped questions missing manual prompts | Diff the scraper's question list against the manual's section prompts before rendering — theme questions and Helps prompts can be absent entirely with no placeholder rendered, so grep won't catch them; hand-add the missing Q&A. |
| Q&A order doesn't match the manual | Sort resolved Q&A to the manual's Ideas-for-Learning sequence (key sort on lowercase question substrings), not scraper order — extraction order follows page layout, not pedagogy. |
| Preview HTML unreadable in dark mode | Ship explicit light cards (dark text + color-coded accents) for any preview-pane HTML — `var(--foreground)`-only styling inherits the app's dark theme and loses contrast. |
| Comparison build wins on content | Port the winner's distinctive content (real episode citations, addendum sections, Q&A depth) into the canonical renderer's week branch and rebuild — never just keep both files or swap filenames; the keeper is one rebuilt file in the canonical layout, verified as usual. |
| Scripture Helps rows read as bare quotes | Lead every helps row with meaning (what the passage is doing, why it matters), keep the verse as anchor, close with one pointed question — quote-only rows teach nothing. |
| Podcast rows read as index cards | Write each row as what-the-show-is plus one plain-language takeaway (deep dive / how-to / structure / family / big-picture), flag the entry point explicitly (START HERE), and expand jargon shorthand into the thing it refers to. |
| Week mapping corrected but old-lesson content still ships | **Grep every pipeline script for all three keys — the week ID (`2026-38`), the unit number (`"38"`), and the old scripture range (`40–49`) — and move every hardcoded per-week branch together** (schedule tables, Q&A/helps/children/cheat-sheet branches, podcast + BYU fallbacks, and topic-gated branches like `is_isaiah` that match the whole book) — a partial fix ships the right title with the wrong body. After rebuilding, grep the extracted PDF text for the old range (must be empty) and the new one. |
| Duplicate `" 2"` / `"copy"` PDF beside the deliverable | List the folder and verify content (cover line, page count) before rebuilding — Finder/iCloud duplicates on sync conflict instead of overwriting, so the latest build may sit under the dup name while the canonical file reverted. Promote with delete-then-rename, never by rebuilding blind. |

## References
- `references/gospel-library-url-patterns.md` — URL construction patterns
- `references/podcast-source-list.md` — Curated podcast list with URLs
- `references/byu-studies-url-pattern.md` — BYU Studies URL structure
- `references/cron-job-config.md` — Hermes cron job configuration (Mondays 7 AM PDT, default profile)
- `references/cron-job-http500-retry.md` — HTTP 500 retry handling for Church website
- `references/weasyprint-pdf-render.md` — House WeasyPrint render path: wrapper setup, print-CSS constraints, per-build verification probe
- `templates/study-guide-template.html` — Base HTML template (1437 lines, mobile-first, dark/light, sticky toolbar, collapsible sections, print styles)
- `scripts/generate_study_guide.py` — Main generator (used by cron, loads template, injects data via CFMTemplate.setLessonData())
- `scripts/inject-gospel-library-links.py` — Interval-based link injection script
- `scripts/build_cfm_study_guide.py` — Comprehensive builder for Claude Code (fetches official lesson, podcasts, downloads assets, server-side template rendering, generates HTML+PDF with actual content)