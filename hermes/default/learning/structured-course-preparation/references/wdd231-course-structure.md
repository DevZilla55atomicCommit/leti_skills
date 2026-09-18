# WDD231 Course Structure Implementation

Full BYUI WDD231 Web Frontend Development II structure created in this session.

## Vault Path
```
/Volumes/PNY128GBLED/TamaZila Obsidian Vault/App Development/00 Education/BYUI-WDD231/COURSE-STRUCTURE/
```

## Assessment (7 Exercises)
```
ASSESSMENT/
├── exercise1-html-semantics/      # HTML5 semantic page, landmarks, accessibility
├── exercise2-css-specificity/     # 3 centering methods, 5 specificity calculations
├── exercise3-js-fundamentals/     # Fetch wrapper, 5 array one-liners, 5 concept explanations
├── exercise4-async-js/            # Sequential vs parallel fetch, error handling bug
├── exercise5-git-github/          # GitHub Pages deploy commands from memory
├── exercise6-devtools/            # 8 DevTools scenarios (panel + feature)
└── exercise7-responsive-design/   # Mobile-first grid: 1/2/3 columns
```
Each folder: `README.md` (task, criteria, resources) + `exerciseN.ext` (solution file)

## Phase 1: Foundations (2 Weeks)

### Week 1 (Days 1-7) — HTML/CSS/JS/Git/DevTools
| Day | Focus | Deliverable |
|-----|-------|-------------|
| 1 | HTML Semantics & Accessibility | Semantic page from memory |
| 2 | CSS Box Model, Flexbox, Grid | 3 responsive layouts |
| 3 | CSS Specificity & Cascade | 10 selector calculations |
| 4 | JavaScript ES6+ Refresher | 5 utility functions |
| 5 | Git Workflow + GitHub Pages | Deploy test site |
| 6 | DevTools Mastery | Debug 3 broken pages |
| 7 | Rest / Light Review | Confidence check |

**Weekend Deep Dive:** Complete landing page → GitHub Pages

### Week 2 (Days 8-14) — Fetch/Async/Modules/DevTools
| Day | Focus | Deliverable |
|-----|-------|-------------|
| 8 | async/await + Fetch Deep Dive | Weather dashboard v1 |
| 9 | Promise Patterns | Sequential vs parallel comparison |
| 10 | Error Handling Strategies | Robust fetch wrapper |
| 11 | JSON & Data Transformation | Parse/transform API data |
| 12 | ES Modules | Refactor dashboard to modules |
| 13 | DevTools Network/Performance | Profile dashboard |
| 14 | Rest / Integration Review | Full integration test |

**Weekend Deep Dive:** Weather Dashboard v2 (modules, parallel fetch, error UI, deployed, Lighthouse 90+)

## Phase 2: WDD231-Specific Prep (2 Weeks)

### Week 1 (Days 15-21) — Accessibility/Forms/Animations
| Day | Focus | Deliverable |
|-----|-------|-------------|
| 15 | Accessibility Fundamentals | Audit 2 pages, fix all |
| 16 | Semantic HTML + ARIA | Accessible component library |
| 17 | Color Contrast + Focus | Contrast audit tool |
| 18 | Forms + URLSearchParams | Multi-step form with confirmation |
| 19 | Form Validation (HTML + JS) | Validated form component |
| 20 | CSS Animations @keyframes | Animated card + modal |
| 21 | CSS Transitions + Performance | 60fps hover/tap animations |

**Weekend Deep Dive:** Join Chamber page (accessible form, animated modal, stagger animations)

### Week 2 (Days 22-28) — Performance/Lighthouse/CI
| Day | Focus | Deliverable |
|-----|-------|-------------|
| 22 | Core Web Vitals Theory | Explain LCP/INP/CLS |
| 23 | Lighthouse Audit Practice | Audit dashboard, fix top 5 |
| 24 | Image Optimization | WebP/AVIF + srcset |
| 25 | Font + Critical CSS | Optimized font loading |
| 26 | Caching + Resource Hints | Preconnect/preload/dns-prefetch |
| 27 | Performance Budget + CI | GitHub Action with budgets |
| 28 | Final Integration Test | Full Chamber prototype |

**Weekend Deep Dive:** Complete Chamber prototype (4 pages, Lighthouse 90+, a11y passed, deployed)

## Course Weeks (5 Weeks During Term)

### Week 1: Foundations & Setup → Course Home Page
### Week 2: Data & Async JS → Chamber Directory Page
### Week 3: APIs & Accessibility → Chamber Home Page
### Week 4: Advanced UI → Chamber Join Page
### Week 5: Performance → Chamber Discover Page + Site Plan

Each course week has:
- `assignments/` — Your repo
- `instructor-sessions/` — Tue (Design First) / Thu (Review) notes
- `notes/` — Class notes + struggled items for spaced revisit

## Capstone Strategy

### Progressive Deliverables
| Week | Deliverable | Weight |
|------|-------------|--------|
| 1 | Course Home Page | 10% |
| 2 | Chamber Directory Page | 15% |
| 3 | Chamber Home Page | 20% |
| 4 | Chamber Join Page | 20% |
| 5 | Chamber Discover Page | 20% |
| 5 | Site Plan Proposal | 15% |

### Technical Excellence Standards (Beyond Requirements)
- TypeScript on all JS
- ESLint + Prettier (CI enforced)
- Component architecture (shared Header, Nav, Footer, Card, Modal)
- Error boundaries + loading states
- WCAG 2.1 AA accessibility
- Lighthouse 90+ all categories
- Conventional commits + PRs + clean history
- README + Site Plan + ADRs + API docs
- GitHub Pages + Lighthouse CI budgets

## Instructor Session Rhythm (During Course)
| Day | Session | Focus |
|-----|---------|-------|
| Tue (90 min) | Session 1 | Design First → Implementation Gates |
| Thu (60 min) | Session 2 | Review → Debrief → Transfer Problem |
| Weekend | Pre-read | Next week PDFs + spaced revisit |

## Cross-Device Sync
- Vault: `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/...` (ExFAT, 74× faster writes)
- Symlink: `~/TamaZila_Obsidian_Vault` → vault
- Profile: `~/.ai-teacher/profile.md` (shared via webdev-instructor)
- Session notes: vault `SESSION-NOTES/`

## Resources
- Course PDFs: `WEEK-BY-WEEK/` (extracted to `RESOURCES/EXTRACTED-PDF-CONTENT.json`)
- Key concepts: `RESOURCES/KEY-CONCEPTS-INDEX.md`
- Web Dev Instructor: activates on `webdev instructor`