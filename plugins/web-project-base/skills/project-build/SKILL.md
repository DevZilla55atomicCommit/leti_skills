---
name: project-build
description: Milestone-gated web project build protocol — one milestone per session, verify after every task, keep context lean to avoid auto-compact thrash. Use for any Next.js one-pager or brochure site built from docs/PLAN.md.
---

# Project Build Skill (leti_skills marketplace — `web-project-base` plugin)

Read this file at the start of EVERY session on a project built from this template, before touching code.

## 0. Startup check (prove the context loaded — do this FIRST, in your first reply)
Quote back, from the project files (not memory):
1. Restaurant/project name (from `docs/PLAN.md` header or `src/config/site.ts`)
2. Address (from `src/config/site.ts` or `assets/manifest.json`)
3. Image count: `ls public/images | wc -l` and the manifest count — they must match

If any file is missing or counts disagree: STOP, report what's missing, do not write code.

## 1. Session budget (anti auto-compact-thrash)
- **ONE milestone per session, then STOP and report.** Never chain milestones in a single session.
- Keep each session under ~40 tool calls. If `/context` passes 60%, run `/compact` immediately — do not push through.
- Fresh session per milestone. State lives in files (`docs/PLAN.md`, `PROJECT-STATUS.md`), never in your head across sessions.

## 2. Source-of-truth order (read before coding)
1. `.claude/skills/project-build/SKILL.md` (this file) + `docs/DESIGN-BRIEF.md` + `docs/BUILD-CHECKLISTS.md`
2. `docs/PLAN.md` — milestones, acceptance criteria
3. `content/menu.md` (or equivalent content source) — copy source (never invent, never lorem ipsum)
4. `assets/manifest.json` — every `/images/*` ref must already exist in `public/images/`
5. `CLAUDE.md` — stack + conventions

## 3. After EVERY task (no exceptions)
Run the task's own gate before moving to the next task:
```bash
npm run typecheck && npm run lint && npm run test && npm run verify:assets
```
- If ANY gate fails: fix it now, do not proceed, do not rationalize ("pre-existing", "will fix later").
- New images: add to `public/images/` + `assets/manifest.json` FIRST, then reference in code.
- Update `PROJECT-STATUS.md` (what shipped, what's next) before reporting.

## 4. End-of-session report (paste this shape)
```
MILESTONE: M#__ — <name>
SHIPPED: <files created/modified>
GATES: typecheck ✅/❌ · lint ✅/❌ · test ✅/❌ · verify:assets ✅/❌ · build ✅/❌
NEXT: M#__ — <name> (fresh session)
OPEN: <anything unresolved, or "none">
```

## 5. Stack rules (non-negotiable)
- Next.js 15 App Router, TS strict, no `any`, no inline styles, Tailwind classes + `@theme` tokens only.
- Server Components default; `'use client'` only for motion/nav/form islands.
- Palette via `@theme` — deliberate choices per `docs/DESIGN-BRIEF.md`, never framework defaults.
- Accessibility floor: landmarks, visible focus, `prefers-reduced-motion`, contrast-checked.
