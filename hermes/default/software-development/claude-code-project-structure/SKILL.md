---
name: claude-code-project-structure
description: Creates Gold Standard structure for new Claude Code project.
---

# Claude Code Project Structure Skill

Creates the **Gold Standard: Universal Base Structure** for any Claude Code project.

## Structure
```
project-root/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   ├── docs/
│   └── templates/
├── .claudeignore
├── src/
│   ├── app/
│   ├── components/{ui,features,layouts}/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   ├── styles/
│   └── config/
├── tests/{unit,integration,e2e,visual,fixtures}/
├── content/
├── docs/
├── scripts/
├── .github/workflows/
├── package.json, tsconfig.json, tailwind.config.ts, next.config.js
└── README.md
```

## Key Principles
1. CLAUDE.md at root — loaded every session
2. Flat src/ — feature-based organization
3. Tests mirror source — co-located tests
4. .claudeignore — blocks generated files
5. .claude/settings.json — permissions + hooks
6. .claude/agents/ — specialized sub-agents
7. Design tokens in CSS — Tailwind v4 @theme

## Files Generated
CLAUDE.md, .claude/settings.json, .claudeignore, package.json, tsconfig.json, next.config.js, tailwind.config.ts, postcss.config.js, src/app/globals.css, src/types/index.ts, src/lib/utils.ts, src/lib/animations.ts, src/lib/content.ts, src/config/site.ts, src/components/ui/Button.tsx, src/components/ui/Card.tsx, tests/unit/utils.test.ts, tests/e2e/navigation.spec.ts, .github/workflows/ci.yml, README.md, content/ATTRIBUTION.md

## Usage
```bash
claude-code --agent @claude-code-project-structure --task "init-project"
```