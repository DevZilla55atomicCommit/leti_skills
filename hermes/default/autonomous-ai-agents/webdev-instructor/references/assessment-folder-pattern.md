# Assessment Folder Pattern for Course Onboarding

## Structure
Each prerequisite exercise gets its own folder under `ASSESSMENT/`:
```
ASSESSMENT/
├── exercise1-html-semantics/
│   ├── README.md          # Task, self-check criteria, resources, YouTube videos
│   └── exercise1.html     # Student solution file
├── exercise2-css-specificity/
│   ├── README.md
│   └── exercise2.css
...
```

## README.md Template
Each exercise README contains:
1. **Task** — Clear, one-sentence objective
2. **Self-Check Criteria** — Checklist Maddie verifies against (explicit, testable items)
3. **Your Solution** — Points to the solution file
4. **Resources for Review** — MDN, CSS-Tricks, etc.
5. **YouTube Videos** — 3-6 curated videos (5-20 min) from trusted channels:
   - Kevin Powell (CSS, responsive, DevTools)
   - Web Dev Simplified (JS, fetch, array methods)
   - Fireship (Git, var/let/const, commits)
   - Jack Franklin (Arrow functions, Promise patterns)
   - Chrome Developers (DevTools panels, performance, accessibility)
6. **Quick Reference Cheatsheet** — Minimal working example (for reference only, student writes from memory)

## Workflow
1. Student opens folder in VS Code
2. Reads README.md (task + criteria + resources)
3. Writes solution in exercise file FROM MEMORY
4. Saves, says "Exercise X done"
4. Maddie reads file, verifies against criteria, reports pass/fail with details
5. Repeat for all exercises

## Gap Mapping
After all exercises:
- Count HIGH-priority gaps per domain
- Generate personalized study plan (adjust Phase 1/2 days)
- Update `~/.ai-teacher/profile.md` mastery map

## macOS ExFAT Note
On ExFAT drives (e.g., PNY128GBLED), macOS creates `._*` resource fork files. These are artifacts — ignore them. Only the main files matter.

## Why This Works
- Separation of concerns: instructions (README) vs solution (exercise file)
- Self-check criteria makes verification objective and fast
- YouTube videos accommodate different learning styles (visual/auditory)
- Folder structure scales to any number of exercises
- Student stays in VS Code; Maddie handles verification