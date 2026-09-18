# Course Folder Structure Template

## Pattern: Structured Pre-Course + Course-Week + Capstone Layout

When a student wants a complete file-based course structure they can work in directly (VS Code) with instructor review via file reads, create this vault structure:

```
COURSE-STRUCTURE/
├── ASSESSMENT/                          # Prerequisite exercises (files ready to edit)
│   ├── exercise1.html   → HTML semantics
│   ├── exercise2.css    → CSS layout/specificity
│   ├── exercise3.js     → JS fundamentals
│   ├── exercise4.js     → Async JS
│   ├── exercise5.sh     → Git/GitHub Pages
│   ├── exercise6.md     → DevTools
│   └── exercise7.css    → Responsive design
│
├── PHASE-1-FOUNDATIONS/                 # Pre-course Phase 1 (2 weeks)
│   ├── PHASE-1-WEEK-1/  (Days 1-7)     # HTML/CSS/JS/Git/DevTools
│   └── PHASE-1-WEEK-2/  (Days 8-14)    # Fetch/async/Modules/DevTools
│
├── PHASE-2-WDD231-PREP/                 # Pre-course Phase 2 (2 weeks)
│   ├── PHASE-2-WEEK-1/  (Days 15-21)   # Accessibility/Forms/Animations
│   └── PHASE-2-WEEK-2/  (Days 22-28)   # Performance/Lighthouse/CI
│
├── COURSE-WEEK-1/ through COURSE-WEEK-5/  # Course weeks (aligned to syllabus)
│   ├── assignments/                      # Student repos per week
│   ├── instructor-sessions/              # Tue/Thu session notes
│   └── notes/                            # Class + struggled items
│
└── CAPSTONE-CHAMBER/
    ├── progressive-build/                # 5-week deliverable map + rubric
    ├── grading-rubric/                   # Rubric alignment + A-grade strategy
    ├── technical-excellence/             # TS, ESLint, a11y, perf, git, docs
    ├── portfolio-case-study/             # Post-course portfolio writeup
    └── post-course/                      # React/Next.js evolution roadmap
```

## Daily Task File Pattern

Each day directory gets a `README.md` with:
- **Tasks** — Checklist with specific, measurable goals
- **Resources** — Links to PDFs, MDN, external guides
- **Deliverable** — What to build/create
- **Files to Create** — Exact filenames for student to create

Student works in VS Code, saves files, tells instructor "Day 3 done" → instructor reads files via `read_file` and reviews.

## Assessment Workflow

Each exercise gets its own folder with README.md and solution file. See `references/assessment-folder-pattern.md` for the detailed template.

### Legacy Flat Pattern (deprecated)
1. Create exercise template files with self-check criteria as comments
2. Student edits in place (no copy-paste needed)
3. Instructor reads file, checks against criteria, gives pass/fail per item
4. Gap map generated → personalized study plan adjusted

## Instructor Session Notes Pattern

```
instructor-sessions/
├── session-1-design-first.md    # Tue: Design First protocol notes
├── session-2-review.md          # Thu: Review + Debrief protocol notes
```

## Capstone Progressive Build Tracking

Each week's assignment repo maps to a capstone deliverable:
- Week 1 → Course Home Page (10%)
- Week 2 → Chamber Directory (15%)
- Week 3 → Chamber Home Page (20%)
- Week 4 → Chamber Join Page (20%)
- Week 5 → Chamber Discover + Site Plan (20% + 15%)

Technical excellence standards (TypeScript, ESLint, a11y, perf budgets, CI) documented in `technical-excellence/README.md` for student to exceed rubric.