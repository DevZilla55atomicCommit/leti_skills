---
name: claude-code-project-architecture
version: 1.0.0
author: Maddie
license: MIT
description: Use when architecting multi-phase projects for Claude Code.
---

# Claude Code Project Architecture & Planning Skill

**Use when:** Planning a multi-phase project for Claude Code execution.

## Project Structure Template

```
project-root/
├── SPEC.md
├── CLAUDE.md
├── STATUS.md
├── TASKS.md
├── README.md
├── SPECS/
│   ├── avengers-prompts.md
│   ├── phase-1-arch.md
│   ├── phase-2-hero.md
│   └── ...
├── .claude/skills/
│   ├── project-architecture-audit.md
│   ├── project-gallery-audit.md
│   └── project-legal-audit.md
├── scripts/
│   ├── extract-content.js
│   ├── download-assets.sh
│   ├── install-skills.sh
│   └── capture-state.js
├── tests/e2e/
├── src/
└── content/
```

## Phase Prompt Template

Each `SPECS/phase-X.md`:

```markdown
# Phase X: [Name]

## Context
- Repo path
- Target reference
- Spec reference
- Content layer
- Assets

## Execute Playbook 1: Stark → Vision → Cap → Jarvis

### Stark: Implementation
- Files to create/modify
- Code patterns
- Reuse components

### Self-Check Before Vision
- [ ] npm run typecheck
- [ ] npm run lint
- [ ] No console.log/TODOs
- [ ] Responsive at 4 breakpoints
- [ ] Reduced motion respected

### Vision: Code Review (READ ONLY)
- a11y, perf, security, best practices

### Cap: Testing
- Unit, E2E (4 viewports), Visual regression
- Coverage ≥80%

### Jarvis: Commit
- Conventional commit
- Branch: feature/phase-name
- PR creation
```

## Required Skills to Load

```bash
skill_view("graphify")
skill_view("motion-ui")
skill_view("tailwind-mastery")
skill_view("accessibility")
skill_view("project-architecture-audit")
```

## Quality Gates

```bash
npm run typecheck && npm run lint && npm run test && npm run test:e2e && npm run test:visual
```

## First Prompt for Claude Code

```text
Read: SPEC.md, CLAUDE.md, SPECS/phase-1-arch.md, src/lib/content.ts, src/components/...

Execute Phase 1: [Task]

Stark: Implementation
- [Steps]

Self-Check: typecheck, lint, responsive, reduced motion

Load Skills: graphify, motion-ui, tailwind-mastery, project-audit
```

## Agent Rules
- @Stark before @Vision on UI
- @Vision READ-ONLY
- @Vision + @Cap parallel on independent files
- @Jarvis last
- Conventional commits
- Branch: feature/phase-name

## Sub-Agent Reference Convention
- Always prefix sub-agent names with @ symbol: @Stark, @Vision, @Cap, @Jarvis, @Avengers
- Claude Code requires @ prefix to recognize sub-agent references
- Without @, Claude Code treats them as plain text, not agent invocations

## CLAUDE.md Required Sections
- Target Fidelity
- Content Source
- Asset Pipeline
- Visual Regression Baseline

## Quick Commands
```bash
npm run install:all-skills
npm run prepare:all
npm run dev
npm run typecheck && npm run lint && npm run test && npm run test:e2e && npm run test:visual
claude-code --agent Avengers --task "$(cat SPECS/phase-X.md)"
```

## Lessons Learned
1. Claude Code has NO auto-read — explicit prompt required
2. Single prompt per phase — self-contained
3. Skills loaded explicitly via skill_view()
4. Quality gates in SPEC.md
5. Project skills in .claude/skills/
6. Global skills in ~/.claude/skills/
7. Vault skills full folders
8. Reference repos for patterns
10. Status.md updated each phase