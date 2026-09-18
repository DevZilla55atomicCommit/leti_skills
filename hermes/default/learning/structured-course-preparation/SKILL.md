---
name: structured-course-preparation
version: 1.0.0
description: "University course prep: assessment, phased plans, capstone."
tags: [university, course-prep, study-plan, assessment, capstone, BYUI, WDD231]
related_skills: [webdev-instructor, teacher-mode, continuous-learning-v2]
author: Alfred Kamisese
license: MIT
metadata:
  hermes:
    tags: [university, course-prep, study-plan, assessment, capstone, BYUI, WDD231]
    related_skills: [webdev-instructor, teacher-mode, continuous-learning-v2]
---

# Structured Course Preparation

Student-facing workflow for preparing for university-level technical courses. Mirrors the instructor-side `webdev-instructor` skill — this is what the student does between sessions.

## When to Use
- Starting a new university course (CS, web dev, data science, etc.)
- 2-8 weeks before course start
- Need to identify gaps, create study plan, and build progressively toward capstone

## Core Workflow

### 1. Assessment First (Session 1)
- Run prerequisite assessment (5-7 exercises from memory)
- Each exercise in own folder with criteria + resources
- No references — honest gap identification
- Map gaps → priority → study days

### 2. Phased Study Plan
| Phase | Focus | Duration | Pattern |
|-------|-------|----------|---------|
| **Phase 1** | Foundations (HTML/CSS/JS/Git/DevTools) | 2 weeks | Daily 1-2hr + weekend deep dive |
| **Phase 2** | Course-specific topics (APIs, a11y, forms, perf) | 2 weeks | Daily 1.5-2hr + weekend project |
| **Phase 3** | During course (weekly rhythm) | Course length | Tue/Thu instructor sessions |

### 3. Capstone Progressive Build
- Week-by-week deliverables aligned to syllabus
- Technical excellence standards beyond requirements
- Grading rubric alignment from day 1
- Portfolio case study documentation

### 4. Instructor Session Rhythm
- **Tuesday (90 min):** Design First → Implementation Gates
- **Thursday (60 min):** Review → Debrief → Transfer Problem
- **Weekend:** Pre-read next week + spaced revisit

## Vault Structure (Cross-Device Sync)
```
/Vault/COURSE-CODE/
├── COURSE-STRUCTURE/
│   ├── ASSESSMENT/              # 7 exercises, folder-per-exercise
│   ├── PHASE-1-FOUNDATIONS/     # Week 1-2 daily tasks
│   ├── PHASE-2-COURSE-PREP/     # Week 3-4 daily tasks
│   ├── COURSE-WEEK-1/ through COURSE-WEEK-N/
│   │   ├── assignments/         # Your repos
│   │   ├── instructor-sessions/ # Tue/Thu notes
│   │   └── notes/               # Class + struggled items
│   └── CAPSTONE/
│       ├── progressive-build/   # Week deliverables map
│       ├── grading-rubric/      # Rubric alignment
│       └── technical-excellence/# TS, ESLint, a11y, perf, git, docs
```

## Assessment Folder Pattern
Each exercise gets:
```
exerciseN-domain/
├── README.md    # Task, self-check criteria, curated resources (MDN, etc.)
└── exerciseN.ext # Your solution file
```

## Key Principles
- **Assessment before study** — gaps dictate timeline
- **Daily deliverables** — every day produces a file
- **Weekend integration** — combine week's learning into deployed project
- **Instructor sessions as forcing functions** — Tue/Thu accountability
- **Cross-device vault** — Obsidian on shared drive + symlinks
- **Technical excellence from day 1** — TypeScript, ESLint, a11y, perf budgets

## WDD231 Implementation (Example)
See `references/wdd231-course-structure.md` for the full BYUI WDD231 implementation created in this session.