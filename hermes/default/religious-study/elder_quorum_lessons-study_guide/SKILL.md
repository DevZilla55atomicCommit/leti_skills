---
name: elder_quorum_lessons-study_guide
title: Elder's Quorum Lesson Study Guide from General Conference Talks
description: Create comprehensive study guides for Elder's Quorum lessons from single General Conference talks with doctrinal depth, visual identity, and discussion-focused materials.
category: religious-study
tags: [lds, general-conference, elders-quorum, teaching, lesson-prep, gospel-doctrine, tithing, consecration]
author: Alfred Kamisese
version: 1.0.0
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [elder-quorum, general-conference, study-guide, teaching]
    category: religious-study
    related_skills:
      - come-follow-me-lesson-prep
      - come-follow-me-study-guide
      - churchofjesuschrist-navigation
    config:
      output_directory: "~/Desktop/Elders Quorum Lessons 2025.2026"
      default_export_pdf: true
      visual_identity: "eq-brass-gold"
---

# Elder's Quorum Lesson Study Guide from General Conference Talks

## Trigger
Use when preparing to teach or study an Elder's Quorum lesson based on a General Conference talk. Creates a complete lesson package: teacher guide, pocket card, class handout, with doctrinal depth, visual identity, and discussion-focused materials.

**Audience routing:** default to the teacher package. When the requester is attending as a class member rather than teaching, build the personal-study framing instead — takeaways-to-share plus a notes box — and drop the timed lesson plan, since timing blocks are useless to someone not running the room.

**PDF-only pipeline lives in the Apollo profile:** `conference-study-guide-pipeline` renders one WeasyPrint PDF per talk and supersedes this skill's Chrome-based export whenever the deliverable is a single PDF. It is invisible to `skill_view` from other profiles — read its SKILL.md directly at `~/.hermes/profiles/apollo/skills/conference-study-guide-pipeline/SKILL.md` and follow it instead of steps 5–8 below.

## Core Workflow

Run the skill pipeline scripts (`scripts/cli.py build ...`) before hand-authoring any artifact — the scripts encode the fetch → discover → render → inject → export order that manual work silently skips.

### 1. Fetch General Conference Talk
- Input: Talk URL (e.g., `https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng`)
- Use Playwright for JS-rendered pages
- Extract: full text, speaker metadata, conference session, date, all scripture references (including footnotes)

### 2. Extract Doctrinal Threads (Helios Color-Science Methodology)
Map the talk's "spectral signature" across 5 doctrinal threads:
- **Thread 1 — Law of Tithing/Consecration** (Hue: Gold #DAA520): Malachi 3:10–12, D&C 119, Moses 5:5–7, Abraham 2:10–11
- **Thread 2 — Firstlings/Adam's Offering** (Hue: Brass #B8860B): Moses 5:5–7, JST Genesis 4, D&C 138:12–13
- **Thread 3 — Double-Mindedness → Single Eye** (Hue: Dark Brass #8B7355): James 1:8, Alma 5:12; 7:3,18, D&C 88:67–68
- **Thread 4 — Putting God First (Prōton)** (Hue: Warm White #F5F0E8): Matthew 6:33, JST Matt 6:38, Helaman 3:35
- **Thread 5 — Windows of Heaven / Spiritual Capacity** (Hue: Light Gold #E6C87A): Malachi 3:10, 3 Nephi 24:10, Becerra's unique contribution

Each thread has: **CDL** (core thesis), **Node Tree** (sub-arguments), **Layer Mixer** (scholarly+prophetic+personal blend), **Qualifier** (isolate doctrinal hue), **Power Windows** (teacher focus), **Gamut Mapping** (align to "God First").

### 3. Discover Related Resources (4 Modules)
| Module | Sources | Query Strategy |
|--------|---------|----------------|
| **Related GC Talks** | General Conference corpus | Keyword: tithing, consecration, firstlings, double-mindedness, Malachi 3:10, "windows of heaven" |
| **Gospel Topics Essays** | `churchofjesuschrist.org/study/gospel-topics/` | Tithing, Consecration, Sacrifice, Law of Sacrifice, Windows of Heaven |
| **BYU Speeches** | `speeches.byu.edu` | Speaker + topic search; filter for Scholarly/Devotional |
| **Scripture Cross-Refs** | Talk's footnotes + Topical Guide | All cited verses + chain references |

### 4. Build Deep Doctrine Addendum (Scholarly Tiered)
- **Essential** (teach Sunday): Bednar "Windows of Heaven", Hinckley 2001 tithing, Nelson "Law of Sacrifice", Maxwell "Consecration"
- **Deepening** (personal study): BYU Studies tithing articles, RSC "Law of Tithing in D&C 119", Interpreter Foundation "Consecration & Zion"
- **Podcast Integration** (curated 1-2): FollowHIM + BYU Studies podcasts on tithing

### 5. Create Teacher Materials (Hestia EQ Pedagogy)
| Output | Audience | Format | Purpose |
|--------|----------|--------|---------|
| **Teacher Guide** | EQ Teacher | HTML + PDF | Full lesson with notes, timing, discussion prompts |
| **Pocket Card** | Teacher | 4×6 laminated | Quick reference during lesson |
| **Class Handout** | EQ Members | 1-page PDF | Take-home with key scriptures, quotes, challenge |
| **Hero Image** | All | PNG | Speaker photo + title + conference badge |

### 6. Visual Identity System (Apollo EQ Brass-Gold)
- **Colors**: Dark Brass #1a1a1a, Brass #B8860B, Warm Gold #DAA520, Light Gold #E6C87A, Warm White #F5F0E8, Ink #1a1a1a
- **Typography**: Crimson Pro (headings), IBM Plex Sans (body), JetBrains Mono (scriptures)
- **Layout**: 2-column doctrinal core, card-based discussion actions, print-optimized
- **Components**: Doctrine cards, Discussion cards, Quote blocks, Action cards
- **Print CSS**: 300 DPI, bleed marks, facing pages, embedded fonts

### 7. Inject Gospel Library Links
Reuse interval-based scripture link injector from Come Follow Me skill — protects CSS/JS/href/src, replaces only in free text regions.

### 8. Export (PDF-only deliverable)
Save to: `~/Desktop/Elders Quorum Lessons 2025.2026/{YEAR}/{MM}/Teacher Lessons/{YYYY-MM_slug_LastName}/`
The deliverable is ONE PDF (`teacher-guide.pdf`) at the folder top level — HTML drafts, cards, JSON, and sources live under `source/` as build provenance, never as deliverables.

**Note**: Personal study guides (single-file HTML/PDF) are created by the companion skill `personal_gc_talk_study_guide` and saved to `~/Desktop/Elders Quorum Lessons 2025.2026/{YEAR}/{MM}/Personal Study/`

## Key Differences from Come Follow Me Skills

| Aspect | Come Follow Me Study Guide | Elder's Quorum Lesson Guide |
|--------|---------------------------|----------------------------|
| **Audience** | Individuals/families (all ages) | Adult men (EQ) |
| **Duration** | Week-long personal study | 50-min Sunday lesson |
| **Source** | Weekly scripture block | Single GC talk |
| **Questions** | Provided in manual | Derived from talk segments |
| **Pedagogy** | Learn → Ponder → Apply | Discuss → Share → Act |
| **Podcasts** | 7+ sources | 1–2 curated |
| **Children** | Dedicated section | "Teach Your Family" challenge |
| **Output** | Multi-page HTML + cheat sheet | One PDF (teacher guide); intermediates under `source/` |

## Commands

```bash
# Build single talk (full pipeline)
python -m elder_quorum_lessons build \
  --talk-url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng" \
  --output-dir "~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Teacher Lessons" \
  --export-pdf

# Fetch only
python -m elder_quorum_lessons fetch \
  --talk-url "..." \
  --output-json talk.json

# Discover resources only
python -m elder_quorum_lessons discover \
  --talk-json talk.json \
  --output-json resources.json

# Build from fetched data
python -m elder_quorum_lessons render \
  --talk-json talk.json \
  --resources-json resources.json \
  --template templates/teacher-guide.html \
  --output-dir ./output
```

## Pitfalls

- **GC pages need JS rendering** — use Playwright, not simple HTTP fetch (`/usr/bin/python3 -m playwright install chromium` on this Mac; system python 3.9 owns the playwright install)
- **Template data is talk-specific (Becerra/tithing)** — `prepare_template_data()` in scripts/cli.py hardcodes core_message + 5 doctrinal threads for the Becerra talk; ALWAYS grep rendered HTML for the previous talk's keywords before delivering a different talk, and author talk-specific content when they leak through
- **Speaker portraits** — extract from biography page (`/learn/{speaker-slug}`), process with brass ring mask
- **Scripture references in footnotes** — parse `footnote` anchors, not just inline citations
- **Folder naming** — use `YYYY-MM_Talk-Slug_SpeakerLastName` format
- **PDF export** — verify 300 DPI, embedded fonts, bleed marks before distributing
- **Visual identity** — keep distinct from Come Follow Me; brass/gold = EQ, blue/gold = CFM

## Verification Checklist

Before delivering lesson guide:
- [ ] Talk fetched completely (no truncation)
- [ ] All scripture references extracted (inline + footnotes)
- [ ] 5 doctrinal threads identified with CDL/Node Tree
- [ ] Related resources: 3+ GC talks, 2+ Gospel Topics, 2+ BYU Speeches
- [ ] Deep Doctrine Addendum has Essential + Deepening tiers
- [ ] Teacher guide has 5-7 discussion questions, timing notes
- [ ] Pocket card fits 4×6, readable at arm's length
- [ ] Class handout is 1 page, includes "Putting It First" challenge
- [ ] Gospel Library links injected without CSS corruption
- [ ] PDF exports at 300 DPI with embedded fonts
- [ ] Output folder matches naming convention (`{YYYY-MM_slug_LastName}`)
- [ ] Folder top level holds only the single deliverable PDF; intermediates archived under `source/`

## References

- `references/gc-talk-url-patterns.md` — URL construction for GC talks
- `references/gospel-topics-index.md` — Gospel Topics essay mapping
- `references/byu-speeches-index.md` — BYU Speeches search patterns
- `references/related-talks-discovery.md` — How to find related conference talks
- `references/scripture-ref-patterns.md` — Regex for extracting refs from talk text
- `references/doctrinal-thread-map.md` — Becerra talk thread map (5 threads, 23 sub-nodes)
- `references/byu-studies-tithing-index.md` — Curated BYU Studies articles on tithing
- `references/eq-pedagogy-guide.md` — Elder's Quorum teaching best practices

## Scripts

- `scripts/fetch_gc_talk.py` — Playwright-based talk fetcher
- `scripts/discover.py` — 4-module resource discovery
- `scripts/inject_links.py` — Adapted interval-based link injector
- `scripts/cli.py` — Full pipeline orchestration
- `scripts/render_template.py` — Jinja2 template renderer

## Templates

- `templates/teacher-guide.html` — Full teacher guide with notes
- `templates/pocket-card.html` — 4×6 quick reference card
- `templates/class-handout.html` — 1-page member handout
- `templates/hero-image.svg` — Hero image template

## Assets

- `assets/brand/eq-colors.css` — EQ Brass-Gold color system
- `assets/brand/eq-typography.css` — Typography system
- `assets/brand/components.css` — Reusable component styles
- `assets/brand/print.css` — Print-optimized CSS (300 DPI, bleed)
- `assets/brass-textures/` — Subtle background patterns