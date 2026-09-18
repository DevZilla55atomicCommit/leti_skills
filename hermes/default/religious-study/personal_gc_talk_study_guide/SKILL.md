---
name: personal_gc_talk_study_guide
title: Personal General Conference Talk Study Guide
description: Create a comprehensive single-file personal study guide for any General Conference talk with doctrinal threads, Q&A, resources, and Lectio Divina reflection.
category: religious-study
tags: [lds, general-conference, personal-study, lectio-divina, tithing, consecration]
author: Alfred Kamisese
version: 1.0.0
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [general-conference, personal-study, study-guide]
    category: religious-study
    related_skills:
      - come-follow-me-study-guide
      - elder_quorum_lessons-study_guide
      - churchofjesuschrist-navigation
    config:
      output_directory: "~/Desktop/Elders Quorum Lessons 2025.2026"
      default_export_pdf: true
      visual_identity: "eq-brass-gold"
---

# Personal General Conference Talk Study Guide

## Trigger
Use when you want a comprehensive, single-file personal study guide for any General Conference talk. Creates a professional HTML + PDF with doctrinal thread analysis, scripture-backed Q&A, related resources, and Lectio Divina reflection framework.

## Core Workflow

### 1. Fetch General Conference Talk
- Input: Talk URL (e.g., `https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng`)
- Uses Playwright for JS-rendered pages
- Extracts: full text, speaker metadata, conference session, date, hero image, all scripture references

### 2. Doctrinal Thread Analysis (Helios Color-Science Methodology)
Map the talk's "spectral signature" across 5 doctrinal threads:
- **Thread 1 — Tithing/Consecration Law** (Hue: `#1A3C5E`): D&C 119, Malachi 3:10–12, D&C 64:23, Council on Disposition
- **Thread 2 — Firstlings/Adam's Offering** (Hue: `#D4A537`): Moses 5:5–7, bekōrâ (firstborn right), typology, Nauvoo affidavits
- **Thread 3 — Double-Mindedness → Single Eye** (Hue: `#8B6914`): James 1:8 (dipsychos), Alma 5:12; 7:3,18, D&C 88:67–68, faith-action
- **Thread 4 — Putting God First (Prōton)** (Hue: `#2C5F7C`): Matthew 6:33, JST Matt 6:38, Helaman 3:35, covenantal identity, Christ's example
- **Thread 5 — Windows of Heaven / Spiritual Capacity** (Hue: `#3D7A9E`): Malachi 3:10 (arubbah), 3 Nephi 24:10, D&C 119:6, dynamic range, devourer, witness

Each thread includes: **4 Q&A pairs** with scripture citations, **cross-references** spanning all 4 standard works + modern prophets, **CSS color variables** for template theming.

### 3. Deep Doctrine Addendum (Tiered)
- **Essential** (teach/study this week): 6 BYU Studies/RSC articles (Harper D&C 119, Bednar Windows, Millet Consecration, Skinner Sacrifice, Jackson Firstlings, Reynolds Double-Mindedness)
- **Deepening** (personal study): 4 resources (Welch Seek Ye First, Smoot Covenant Sign, Griffin Spiritual Capacity, Ludlow Melchizedek)
- **Podcast Integration** (curated 5): FollowHIM, BYU Studies, Scripture Insights, Don't Miss This, Certain Women

### 4. Related Resource Discovery (4 Modules)
| Module | Sources | Output |
|--------|---------|--------|
| **Related GC Talks** | Conference archive | 8 talks with relevance scores & connection explanations |
| **Gospel Topics Essays** | churchofjesuschrist.org/study/gospel-topics/ | 10 mapped topics with insights |
| **BYU Speeches** | speeches.byu.edu | 10 speeches with topics & relevance |
| **Scripture Chain** | Talk's footnotes + Topical Guide | Cross-refs spanning all standard works |

### 5. Personal Reflection — Lectio Divina Framework (Hestia)
**4 Movements:**
1. **LECTIO** (Read — 10–15 min): Slow reading prompts, paragraph-by-paragraph, scripture anchor identification
2. **MEDITATIO** (Meditate — 15–30 min): Thread-specific reflection questions, imagery engagement, personal application
3. **ORATIO** (Pray — 10–15 min): Guided prayer prompts per thread, covenant alignment prayers
4. **CONTEMPLATIO** (Contemplate — 5–20 min): Silent presence with anchor phrase

**Plus:**
- **Weekly Application Challenges** (Seed → Root → Branch → Fruit rotation)
- **Journaling Prompts** (Daily 2-min / Weekly 15-min / Monthly 30-min)
- **Personal Covenant Tracker** (Alignment grid + Monthly Pulse checklist)

### 6. Visual Identity (Apollo)
- **Colors**: Thread hues + EQ Brass-Gold system (`#1A3C5E`, `#D4A537`, `#8B6914`, `#2C5F7C`, `#3D7A9E`, `#F5F0E8`, `#B8860B`)
- **Typography**: Crimson Pro (headings), IBM Plex Sans (body), JetBrains Mono (scriptures)
- **Layout**: Single-file HTML, embedded CSS/JS, SVG icons, collapsible sections, dark/light toggle
- **Print**: 300 DPI, bleed marks, facing pages, embedded fonts
- **Hero**: Mike Malm's "Similitude of the Sacrifice of the Only Begotten of the Father" (Adam & Eve firstlings, angel, Christ vision)

### 7. Gospel Library Link Injection
Reuse interval-based scripture link injector — protects CSS/JS/href/src, replaces only in free text regions.

### 8. Export
Save to: `~/Desktop/Elders Quorum Lessons 2025.2026/{YEAR}/{MM}/Personal Study/`
Files: `study-guide.html`, `study-guide.pdf`, `sources.md`

## Commands

```bash
# Build single talk (full pipeline)
python -m personal_gc_talk_study build \
  --talk-url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng" \
  --output-dir "~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Personal Study" \
  --export-pdf

# Step-by-step
python scripts/personal_study.py fetch \
  --talk-url "..." \
  --output-json talk.json

python scripts/personal_study.py discover \
  --talk-json talk.json \
  --output-json resources.json

python scripts/personal_study.py render \
  --talk-json talk.json \
  --resources-json resources.json \
  --template templates/personal-study.html \
  --output-dir ./output
```

## Key Differences from Elder's Quorum Skill

| Aspect | Elder's Quorum Lesson Guide | Personal Study Guide |
|--------|---------------------------|---------------------|
| **Audience** | EQ Teacher + Class | Individual |
| **Duration** | 50-min Sunday lesson | Self-paced (hours/days) |
| **Output** | 3 files (teacher, pocket, handout) | 1 file (comprehensive) |
| **Pedagogy** | Discuss → Share → Act | Lectio Divina (Read → Meditate → Pray → Contemplate) |
| **Reflection** | Discussion questions | 4-movement Lectio Divina + journaling |
| **Covenant Focus** | Class application | Personal covenant tracker |
| **Format** | Multiple HTML/PDF | Single HTML + PDF |

## Pitfalls

- **GC pages need JS rendering** — use Playwright, not simple HTTP fetch
- **Hero image** — use official Church artwork (Mike Malm's "Similitude..." for tithing/firstlings talks)
- **Scripture references in footnotes** — parse `footnote` anchors, not just inline citations
- **Folder naming** — separate `Teacher Lessons/` and `Personal Study/` folders
- **PDF export** — verify 300 DPI, embedded fonts, bleed marks
- **Playwright EPIPE** — browser crashes can occur; retry with adjusted settings

## Verification Checklist

Before delivering study guide:
- [ ] Talk fetched completely (no truncation)
- [ ] All 5 threads identified with hues
- [ ] 4 Q&A per thread with scripture citations
- [ ] Cross-references spanning all 4 standard works
- [ ] Deep doctrine: 6 essential + 4 deepening + 5 podcasts
- [ ] Related resources: 8 GC talks, 10 Gospel Topics, 10 BYU speeches, scripture chain
- [ ] Lectio Divina: 4 movements with prompts
- [ ] Application challenges: Seed/Root/Branch/Fruit
- [ ] Covenant tracker: Alignment grid + Monthly Pulse
- [ ] Gospel Library links injected without CSS corruption
- [ ] Hero image: Mike Malm artwork (or talk-appropriate)
- [ ] PDF exports at 300 DPI with embedded fonts
- [ ] Output folder matches naming convention

## References

- `references/doctrinal-threads.md` — 5 threads with Q&A, hues, cross-refs
- `references/deep-doctrine.md` — Tiered BYU Studies, podcasts
- `references/related-resources.md` — GC talks, Gospel Topics, BYU speeches, scripture chain
- `references/lectio-divina.md` — 4 movements, challenges, journaling, covenant tracker
- `references/gc-talk-url-patterns.md` — URL construction
- `references/hero-images.md` — Official Church artwork mapping

## Scripts

- `scripts/personal_study.py` — Main CLI orchestrator
- `scripts/fetch_gc_talk.py` — Playwright-based talk fetcher
- `scripts/discover.py` — 4-module resource discovery
- `scripts/inject_links.py` — Adapted interval-based link injector
- `scripts/render_template.py` — Template renderer

## Templates

- `templates/personal-study.html` — Single-file template (Apollo)

## Assets

- `assets/hero-images/` — Official Church artwork
- `assets/brand/` — CSS variables, thread colors