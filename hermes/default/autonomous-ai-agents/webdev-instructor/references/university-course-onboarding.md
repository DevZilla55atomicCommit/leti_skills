# University Course Onboarding Reference

## Course-Specific Onboarding Flow

When a student identifies a specific university course (e.g., "WDD231 at BYU-Idaho"), run this extended onboarding:

### 1. Course Material Extraction
```
"Let me extract and organize your course materials first."
- Locate course folder (PDFs, syllabi, assignments)
- Extract all content to vault
- Create week-by-week breakdown
- Build key concepts index
```

### 2. Prerequisite Assessment (Course-Tailored)
Run the standard 7-exercise assessment PLUS course-specific exercises:
- Map assessment results to course week dependencies
- Identify gaps for each upcoming week
- Generate targeted pre-course study plan

### 3. Course Plan Creation
Save to vault at: `App Development/00 Education/[COURSE-CODE]/`
- COURSE-MASTER-PLAN.md
- PREREQUISITE-ASSESSMENT.md
- PRE-COURSE-STUDY-PLAN.md
- CAPSTONE-STRATEGY.md
- WEEK-BY-WEEK/ (one per week)
- RESOURCES/ (extracted content + concept index)

### 4. Cross-Device Sync Confirmation
Verify vault location and symlinks:
- Obsidian vault on shared drive (PNY128GBLED)
- Symlinks: `~/TamaZila_Obsidian_Vault` → vault
- webdev-instructor profile at `~/.ai-teacher/profile.md` (shared)
- Session notes in vault `SESSION-NOTES/`

---

## WDD231-Specific Additions (Template for Other Courses)

### Course Metadata
- **Course:** WDD231 - Web Frontend Development II
- **Institution:** BYU-Idaho
- **Term:** Term 02 2026
- **Progressive Project:** Chamber of Commerce Website (5 weeks)

### Week Dependency Map
```
Week 1: HTML/CSS/JS Foundations → Course Home Page
    ↓
Week 2: Fetch/async/await + JSON → Directory Planning
    ↓
Week 3: Accessibility + ES Modules → Home Page (API consumption)
    ↓
Week 4: Modals/Animations/Forms → Join Page
    ↓
Week 5: Performance → Discover Page + Site Plan
```

### Assessment Exercises by Week
| Week | Added Exercises |
|------|-----------------|
| 1 | Semantic HTML, CSS Grid/Flex, GitHub Pages deploy |
| 2 | Fetch wrapper, Promise.all, JSON parsing |
| 3 | Accessibility audit, ES Module refactor |
| 4 | Form GET + URLSearchParams, accessible modal |
| 5 | Lighthouse audit, Core Web Vitals optimization |

### Capstone Strategy Integration
- Grading rubric alignment (typical: 30% functional, 25% code quality, 20% design, 15% docs, 10% deploy)
- Technical excellence standards beyond requirements
- Portfolio case study template
- Post-course evolution roadmap

---

## General Template for Any University Course

When student provides course code and institution:

1. **Create vault structure:** `App Development/00 Education/[INSTITUTION]-[COURSE]/`
2. **Extract all materials** (PDFs, syllabi, LMS exports)
3. **Build week-by-week dependency map**
4. **Generate prerequisite assessment** mapped to week dependencies
5. **Create pre-course study plan** (4 weeks default, adjustable)
6. **Design capstone/project strategy** if applicable
7. **Save everything to vault** for cross-device access
8. **Update webdev-instructor profile** with course context