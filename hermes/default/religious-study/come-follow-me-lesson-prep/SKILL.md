---
name: come-follow-me-lesson-prep
title: Come Follow Me Lesson Preparation
description: Fetch and simplify Come Follow Me lessons with answers.
category: religious-study
tags: [lds, come-follow-me, teaching, lesson-prep, gospel-doctrine]
---

# Come Follow Me Lesson Preparation

## Trigger
Use when preparing to teach or study a weekly Come Follow Me lesson. Covers: fetching the official lesson from churchofjesuschrist.org, supplementing with BYU Studies academic resources, extracting every discussion question, and producing simple, student-friendly answers with scripture references.

## Core Workflow

### 1. Fetch Official Lesson
- Navigate to `https://www.churchofjesuschrist.org/study/come-follow-me`
- Click current year's manual (e.g., "For Home and Church: Old Testament 2026")
- Click the current week's date range (e.g., "August 10–16")
- Capture full page text — includes overview, all section questions, teaching ideas, scripture helps

### 2. Supplement with BYU Studies
- Navigate to `https://byustudies.byu.edu/come-follow-me/old-testament/<week-number>`
- Week numbers: Jan 1 = week 1, etc. (August 10–16 = week 33)
- Capture: scholarly articles, podcasts, conference talk references, historical context

### 3. Extract Every Question
Search the lesson text for all questions (marked by `?`). Categories:
- **Main section questions** (under each scripture block)
- **Scripture Helps** (end of lesson)
- **Teaching Children questions** (separate section)
- **Application/personal questions**

### 4. Produce Student-Friendly Answers
For each question, provide:
- **Simple Answer** — 2–3 sentences, no doctrinal jargon
- **Where to Find It** — exact scripture references + Gospel Library paths
- **Think About It** — one personal application prompt
- **Deeper Resource** — optional BYU Studies article, conference talk, or scholar commentary

### 5. Create Teaching Materials
- One-page cheat sheet (question → answer → scripture)
- Kid-level answers for Teaching Children section
- Personal prep checklist (5 min: read key verses, pick one question, bring visual)

## Key Principles (User Preferences)

| Principle | Implementation |
|-----------|----------------|
| **No doctrinal jargon** | Replace "theodicy," "epistemological," "soteriological" with plain English |
| **Every question answered** | No "discuss as a class" — give a clear, cited answer first |
| **Source every claim** | Scripture reference + Gospel Library path + optional scholarly source |
| **Kid-level = distinct** | Separate "Teaching Children" answers from adult answers |
| **Visual/concrete** | Suggest object lessons, nature metaphors, hymn lines, artwork |
| **HTML output with PDF export** | Produce color-coded HTML with tables, timeline cards, cheat sheets; user saves via Cmd+P → Save as PDF |
| **Iterative refinement workflow** | Timeline → All Q&A → Podcast insights → Common questions → Specific details (names, symbolism) |
| **Podcast integration** | Include followHIM, BYU Studies podcast insights as distinct colored sections with attribution |
| **Common questions section** | Anticipate and answer meta-questions (e.g., "Did Job know about the wager?" "Who wrote Job?") |

## Pitfalls

- **Week number calculation**: BYU Studies uses sequential weeks from Jan 1. Verify: `week = (date - Jan 1).days // 7 + 1`
- **ChurchofJesusChrist.org JS rendering**: Page content loads dynamically. Wait 3s after navigation before extracting text.
- **Element indices shift**: After clicking a month/week link, re-capture before extracting.
- **Manual vs. supplement**: Official lesson = authoritative; BYU Studies = enrichment. Label clearly.
- **Question extraction**: Some questions are implicit ("Ponder..." "Consider..."). Convert to explicit Q format.

## Support Files

- `references/lesson-template.md` — starter template for a new week's prep
- `references/week-number-guide.md` — calendar mapping for BYU Studies week numbers
- `scripts/extract-questions.py` — (future) regex to pull all `?` sentences from lesson text

## Verification Checklist

Before delivering lesson prep:
- [ ] Every `?` in manual has an answer
- [ ] Every answer has scripture reference
- [ ] Kid answers are separate and simpler
- [ ] One-page cheat sheet exists
- [ ] Personal prep items are concrete (not "study more")
- [ ] No undefined doctrinal terms