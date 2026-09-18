---
name: coding-workflow
description: Standardized coding workflow: lint → typecheck → test → commit
category: development
tags: [workflow, lint, typecheck, test, git, quality-gates]
---

# Coding Workflow Skill

## Purpose
Enforce consistent quality gates across all coding tasks. Every change must pass the pipeline before commit.

## Pipeline Stages

### 1. Pre-Change (Before Writing Code)
- [ ] Read relevant conventions (`project-conventions` skill)
- [ ] Check `CLAUDE.md` in project root for overrides
- [ ] Understand existing patterns in codebase (use Graphify)
- [ ] Plan changes in todo list

### 2. During Development
- [ ] Write code following conventions
- [ ] Add types (no `any`)
- [ ] Add Zod validations at boundaries
- [ ] Write/update tests for new logic
- [ ] Keep components focused and small

### 3. Pre-Commit Quality Gates (MANDATORY)

Run **in order** — stop at first failure:

```bash
# Stage 1: Format (auto-fix)
pnpm format

# Stage 2: Lint (must pass)
pnpm lint

# Stage 3: Typecheck (must pass)
pnpm typecheck

# Stage 4: Tests (must pass)
pnpm test

# Stage 5: Build (must pass)
pnpm build
```

### 4. Commit
```bash
# Only after ALL gates pass
git add -A
git commit -m "feat: descriptive message"
git push
```

## Agent Enforcement

When agent makes changes:
1. **Auto-run gates** after each logical change set
2. **Block commit** if any gate fails
3. **Show exact error** and suggest fix
4. **Re-run** after fix until all pass

## Quality Gate Details

### Lint (`pnpm lint`)
```bash
# Config: eslint.config.mjs (Next.js flat config)
# Rules: TypeScript ESLint recommended + Next.js core-web-vitals
# Auto-fix: eslint --fix
```
Common issues to catch:
- Unused variables/imports
- Missing React hooks dependencies
- `any` types (error level)
- Console.log in production code

### Typecheck (`pnpm typecheck`)
```bash
# Command: tsc --noEmit
# Config: tsconfig.json (strict: true)
# Must pass: zero errors
```
Common issues:
- Missing return types on exported functions
- Implicit `any` in callbacks
- Type mismatches in API responses

### Tests (`pnpm test`)
```bash
# Command: vitest run
# Coverage: target >80% for new code
# Patterns: *.test.ts, *.test.tsx, *.spec.ts, *.spec.tsx
```
Test requirements:
- Unit tests for utilities/lib code
- Component tests for complex UI
- Integration tests for API routes
- Mock external dependencies

### Build (`pnpm build`)
```bash
# Command: next build
# Catches: Type errors in production, missing env vars, import issues
```

## Workflow Automation

### Git Hooks (Husky + lint-staged)
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

### CI Pipeline (GitHub Actions)
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
```

## Agent Commands

### Run Full Pipeline
```bash
# Single command for agents
pnpm format && pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

### Quick Check (During Development)
```bash
# Faster iteration - run after each file change
pnpm typecheck && pnpm lint
```

### Fix Auto-Fixable Issues
```bash
pnpm format && pnpm lint --fix
```

## Failure Handling

| Gate | On Failure | Agent Action |
|------|------------|--------------|
| Format | Never fails (auto-fix) | Continue |
| Lint | Errors present | Show errors, suggest fixes, re-run |
| Typecheck | Type errors | Show exact errors with file:line, fix, re-run |
| Tests | Failures | Show failing test output, fix code/tests, re-run |
| Build | Errors | Show build error, fix, re-run |

## Integration with Kanban

When Kanban creates a task:
1. Task includes `quality-gates: required` label
2. Agent runs pipeline after implementation
3. Task auto-moves to "Review" only when all gates pass
4. Failed gates = task stays "In Progress" with error details

## Project-Specific Overrides

Check `CLAUDE.md` or `.hermes/WORKFLOW.md` in project root for:
- Additional lint rules
- Different test commands
- Custom quality gates
- Monorepo-specific pipelines (turbo, nx)

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE COMMIT — RUN IN ORDER                              │
├─────────────────────────────────────────────────────────────┤
│  1. pnpm format        # Auto-fix formatting               │
│  2. pnpm lint          # Must pass (eslint)                │
│  3. pnpm typecheck     # Must pass (tsc --noEmit)          │
│  4. pnpm test          # Must pass (vitest run)            │
│  5. pnpm build         # Must pass (next build)            │
│                                                             │
│  THEN: git add -A && git commit -m "msg" && git push       │
└─────────────────────────────────────────────────────────────┘
```