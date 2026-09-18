# Come Follow Me Weekly Lesson Prep Workflow

## Overview
Pattern for extracting, enriching, and formatting weekly Come Follow Me lessons for teaching prep.

## Extraction Workflow (Proven)

### 1. Primary Source: churchofjesuschrist.org
**Target URL Pattern:**
```
https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026/{month}-{day}-{day}?lang=eng
```

**Steps:**
1. Navigate to `https://www.churchofjesuschrist.org/study` → "Come, Follow Me" → "For Home and Church: Old Testament 2026"
2. **Wait 3–5 seconds** after each click for React rendering
3. Find weekly lesson link by text content (e.g., "August 10–16")
4. Extract full lesson text via `document.body.innerText`
5. Parse for all lesson questions (typically 18+ questions across 4 sections + scripture helps + children's ideas)

### 2. Complementary Sources

| Resource | Access Method | Value |
|----------|---------------|-------|
| **BYU Studies** | `https://byustudies.byu.edu/come-follow-me/old-testament/{week}` | Academic articles, podcasts, reflection pieces |
| **followHIM Podcast** | YouTube search "followHIM Come Follow Me Old Testament {week}" | Expert commentary; extract insights from video description/comments |
| **Gospel Library** | In-app or web | Guide to Scriptures, Hymns, Conference talks referenced |

### 3. YouTube Podcast Extraction (Workaround)
**Problem:** `browser-use` CLI cannot reliably access YouTube's transcript UI.

**Working Approach:**
1. Navigate to video URL
2. Extract video description via `document.body.innerText`
3. Scroll comments for key insights (top comments often have timestamped summaries)
3. Use video title + description + top comments as source material

**Example (Job Week 33):**
- Part 1: Dr. Marcus Martins — 1:08:37 — "Why does bad news land on faithful people?"
- Part 2: Dr. Marcus Martins — 44:39 — "God answers with questions, not explanations"
- 8 key insights extracted from comments (vantage point widening, daughters' names = temple journey, resurrection = heavenly+earthly blend, etc.)

## Lesson Structure Template

Each lesson typically contains:
- **4 Main Sections** with 2–5 questions each
- **Scripture Helps** (3–5 additional questions)
- **Ideas for Teaching Children** (5–7 topics with questions)
- **Media Resources** (videos, music, artwork, PDF)

## Output Format: HTML Study Guide

Create printable study guide with:
1. **Lifetime Timeline** — visual chronology of Job's experience
2. **Every Question Answered** — simple English + scripture refs
3. **Podcast Insights** — expert commentary distilled
4. **Children's Teaching Table** — kid-level answers
5. **One-Page Cheat Sheet** — 12 quick-reference cards
6. **Common Questions** — FAQ (Job's knowledge, authorship, etc.)
7. **5-Minute Homework** — prep checklist

## PDF Generation
Use browser print: `Cmd + P` → "Save as PDF" from preview pane.

## Common Pitfalls
- **React rendering delay:** Always wait 3–5 seconds after navigation
- **YouTube transcripts:** Don't rely on browser-use; use description/comments
- **Element indices shift:** Re-capture after interactions
- **Rate limits:** Add `seconds` pause between rapid clicks
- **404/503 errors:** Verify with `browser_snapshot` before proceeding