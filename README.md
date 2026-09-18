# leti_skills
Alfred's Claude Code skill library — installable as a plugin marketplace in Claude Code (CLI + Desktop app).

## Install (once per machine)
```
plugin marketplace add DevZilla55atomicCommit/leti_skills
plugin install web-project-base
```

## Plugins
| Plugin | Contents |
|---|---|
| `web-project-base` | `project-build` skill (milestone-gated builds, anti auto-compact-thrash), design brief, build checklists, asset verifier script |

## Use in a project
The project template points at this repo: after installing, the `project-build` skill resolves by name in any session. Project folders also vendor the briefs/checklists inline (belt and suspenders), so builds never stall on skill resolution.

---

## Hermes Agent Skills Backup
This repo also serves as a backup for Hermes Agent skills across 6 specialized profiles.

### Structure
```
hermes/
├── default/        # 162 shared skills + default profile
├── apollo/         # 21 profile-specific skills (creative, study guides, knowledge graphs)
├── helios/         # 16 profile-specific skills (DaVinci Resolve, doctrine)
├── hephaestus/     # 15 profile-specific skills (code, engineering)
├── hestia/         # 15 profile-specific skills (operations, infra)
└── kairos/         # 15 profile-specific skills (Forex, markets)
```

### Profile Purposes
| Profile | Role | Specialization |
|---|---|---|
| `default` | Maddie (orchestrator) | General-purpose, all shared skills |
| `apollo` | Creative director | Video/photo, study guides, knowledge graphs |
| `helios` | DaVinci/doctrine | Color grading, Resolve workflows, religious study |
| `hephaestus` | Code/engineering | Software dev, build, debugging |
| `hestia` | Operations | Infra, cron, devops, maintenance |
| `kairos` | Forex analyst | Market analysis, trading automation |

### Restoring
```bash
# Restore shared skills to Hermes
cp -r hermes/default/* ~/.hermes/skills/

# Restore a profile's skills
cp -r hermes/apollo/* ~/.hermes/profiles/apollo/skills/
```

> **Note**: These are Hermes-format skills (SKILL.md + refs/), not Claude Code plugins. They are backed up here for portability across machines, not for installation via `plugin install`.

---

## Claude Code Skills Backup
Full `~/.claude/skills/` directory backed up — includes local skills + resolved symlinks to external sources (mattpocock_skills, ai-teacher).

### Structure
```
claude/
└── skills/         # 155 skills (128 local + 27 resolved symlinks)
```

### Categories
- **Frontend/React/Next.js**: `nextjs-master`, `nextjs-architect`, `react-mastery`, `react-patterns`, `shadcn`, `tailwind-master`, `tailwindcss`, `motion`, `motion-react`, `vercel-optimize`
- **Components/Design**: `building-components`, `css-craftsman`, `interface-design`, `canvas-design`, `brand-*`, `frontend-design-direction`, `landing-page-design`
- **Backend/API**: `nodejs-backend`, `create-node-api`, `api-designer`, `graphql-expert`, `clerk-*`, `supabase`, `stripe-*`
- **Testing/QA**: `vitest`, `testing-arsenal`, `qa-test-planner`, `test-antipatterns`, `webapp-testing`, `playwright` (in codex)
- **Debugging/Workflow**: `systematic-debugging`, `debugging-detective`, `executing-plans`, `creating-spec`, `git-workflow`, `delivery-gate`, `loop-design-check`
- **AI/Tools**: `mcp-builder`, `context7`, `nano-banana-pro`, `nano-banana-prompting`, `web-artifacts-builder`, `skill-creator`
- **External (resolved)**: mattpocock_skills (27 skills), ai-teacher (2 skills)

### Restoring
```bash
cp -r claude/skills/* ~/.claude/skills/
```

---

## Codex Skills Backup
Full `~/.codex/skills/` directory backed up.

### Structure
```
codex/
└── skills/         # 40 skills
```

### Categories
- **Deployment**: `vercel-deploy`, `netlify-deploy`, `cloudflare-deploy`, `render-deploy`, `migrate-to-codex`
- **Figma**: `figma`, `figma-*` (8 skills for design→code)
- **Notion**: `notion-knowledge-capture`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation`
- **Testing**: `playwright`, `playwright-interactive`, `screenshot`
- **Security**: `security-best-practices`, `security-threat-model`, `security-ownership-map`, `sentry`
- **AI/ML**: `chatgpt-apps`, `speech`, `transcribe`, `jupyter-notebook`, `openai-docs`
- **GitHub**: `gh-fix-ci`, `gh-address-comments`, `linear`
- **Misc**: `define-goal`, `cli-creator`, `hatch-pet`, `yeet`, `aspnet-core`, `pdf`, `winui-app`

### Restoring
```bash
cp -r codex/skills/* ~/.codex/skills/
```