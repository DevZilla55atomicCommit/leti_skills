# Cron Job Configuration (Updated 2026-09-03)

## Current Job ID: `32b9ccc7d337`

## Configuration
- **Schedule**: `0 7 * * 1` (Mondays 7:00 AM PDT)
- **Profile**: Hermes Default (Maddie) — NOT Helios profile
- **Model**: nvidia/nemotron-3-ultra-550b-a55b
- **Provider**: NVIDIA
- **Skills**: ["come-follow-me-study-guide"] (global skill)
- **Toolsets**: file, terminal, web_search, web_extract, browser
- **Workdir**: ~/.hermes/skills/religious-study/come-follow-me-study-guide
- **Origin**: Default profile (desktop)
- **Delivery**: local

## Pipeline (Clean - No Bots, No EQ)
```
Cron Trigger (Mon 7 AM)
    │
    ▼
Hermes Default Profile (Maddie) — Agent Mode
    │
    ├──▶ Model: nvidia/nemotron-3-ultra-550b-a55b
    ├──▶ Skill: come-follow-me-study-guide (global)
    ├──▶ Tools: file, terminal, web_search, web_extract, browser
    └──▶ Workdir: ~/.hermes/skills/religious-study/come-follow-me-study-guide
    │
    ▼
Agent executes skill workflow:
    │
    ├──▶ 1. Fetch official lesson (churchofjesuschrist.org) via web_extract
    ├──▶ 2. Fetch supplements (BYU Studies, followHIM, etc.) via web_search + web_extract
    ├──▶ 3. Run skill's generate_study_guide.py via terminal
    │         ▶ Loads template: templates/study-guide-template.html
    │         ▶ Injects data via CFMTemplate.setLessonData()
    │         ▶ Runs inject-gospel-library-links.py for scripture links
    ├──▶ 4. Write HTML to ~/Desktop/Come Follow Me Study Guides/YYYY/MM/WeekX_Topic/
    ├──▶ 5. Chrome headless → PDF (via browser tool)
    │
    ▼
Deliver: HTML + PDF in clean folder (no EQ, no Teacher/Personal split)
```

## Output Structure (Monthly with Short Month Names)
```
~/Desktop/Come Follow Me 2026/2026/
└── Aug/
    ├── Week 1 - Psalms102-150 - Aug31-Sep62026/
    │   ├── Psalms_102-150_Lesson_Final.html
    │   ├── Psalms_102-150_Lesson_Final.pdf
    │   ├── psalms102-150_lesson_header.png
    │   ├── psalms102-150_timeline.png (if applicable)
    │   └── psalms102-150_flowchart.png (if applicable)
    ├── Week 3 - Job - Aug10-162026/
    ├── Week 4 - Psalms - Aug17-232026/
    └── Week 5 - Psalms - Aug24-302026/
└── Sep/
    └── Week 1 - Job - Sep7-132026/  (first run: Monday Sep 7, 2026)
```

**Folder naming**: `Week X - Topic - MMMdd-MMMddyyyy/` (e.g., `Week 1 - Psalms102-150 - Aug31-Sep62026/`)
- **Week X**: Week-of-month (1-5) per CFM lesson sequence
- **Topic**: Scripture block title, no spaces, hyphens preserved
- **DateRange**: Short month names, no spaces, compact

**Target path for cron**: `~/Desktop/Come Follow Me 2026/2026/MMM/Week X - Topic - DateRange/`

## Key Fixes Applied (2026-09-03)
1. **Removed bot/agent dependencies** — Runs entirely under Hermes default profile
2. **Removed Elder's Quorum coupling** — Clean output to Come Follow Me Study Guides/
3. **Removed Helios/Apollo profile dependency** — Uses global skill only
4. **Monthly folder structure** — YYYY/MM/WeekX_Topic/ (not flat YYYY-MM-WeekX_Topic/)
5. **Dynamic week detection** — Skill calculates current CFM week from date
6. **Retry on HTTP 500** — Explicit retry logic in prompt for Church site reliability

## Previous Issues (Resolved)
- **Old job ID**: `b174ee93649a` — Used Helios profile, hardcoded EQ paths, tangled with EQ task
- **Old script**: `cron_command.py` — Bypassed Hermes, hardcoded paths, fell back to sample data
- **HTTP 500 errors** — Added exponential backoff retry pattern (see cron-job-http500-retry.md)

## Test Commands
```bash
# Dry-run skill directly
python3 ~/.hermes/skills/religious-study/come-follow-me-study-guide/scripts/generate_study_guide.py \
  --data ~/.hermes/skills/religious-study/come-follow-me-study-guide/sample-lesson-data.json \
  --output-base ~/Desktop/Test_CFM_Monthly

# Trigger via Hermes (full pipeline)
# In Hermes: "Run the Come Follow Me Weekly Study Guide cron job now"
```

## First Scheduled Run
**Monday, September 7, 2026 at 7:00 AM PDT**
Target folder: `~/Desktop/Come Follow Me Study Guides/2026/09/Week36_Job_Sep07-Sep13/`