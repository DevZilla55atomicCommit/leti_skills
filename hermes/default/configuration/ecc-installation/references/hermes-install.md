# Hermes ECC Installation Log

**Date:** 2026-08-04
**Profile:** minimal
**Target:** hermes

## Steps Executed

### 1. Install ecc-universal
```bash
npm install -g ecc-universal
# added 8 packages in 797ms
```

### 2. Run minimal install for Hermes
```bash
# First attempt failed - ecc-install not on PATH
ecc-install --profile minimal --target hermes
# /bin/bash: line 2: ecc-install: command not found

# Workaround: direct script path
node $(npm root -g)/ecc-universal/scripts/install-apply.js --profile minimal --target hermes
```

### 3. Installation Output
```
Applying install plan:
Mode: manifest
Target: hermes
Adapter: hermes-home
Install root: /Users/alfredkamisese/.hermes
Install-state: /Users/alfredkamisese/.hermes/ecc-install-state.json
Profile: minimal
Included components: (none)
Excluded components: (none)
Requested modules: rules-core, agents-core, commands-core, platform-configs, workflow-quality
Selected modules: rules-core, agents-core, commands-core, platform-configs, skill-unified-memory, workflow-quality
Applied operations: 457
```

### 4. Verify Installation
```bash
ecc doctor --target hermes
# Status: OK
# Issues: none
```

## What Was Installed

### Agents (67)
Location: `~/.hermes/agents/`
Examples: `planner.md`, `architect.md`, `code-reviewer.md`, `security-reviewer.md`, `tdd-guide.md`, `build-error-resolver.md`, `spec-miner.md`, `loop-operator.md`, `harness-optimizer.md`

### Skills (281+)
Two formats installed for Hermes compatibility:

1. **Hermes-native** (`~/.hermes/.agents/skills/`) — with `agents/openai.yaml` for delegation
   - 40 skills: `agent-introspection-debugging`, `agent-sort`, `api-design`, `article-writing`, `backend-patterns`, `benchmark-methodology`, `brand-discovery`, `brand-voice`, `bun-runtime`, `coding-standards`, `competitive-platform-analysis`, `competitive-report-structure`, `content-engine`, `crosspost`, `deep-research`, `dmux-workflows`, `documentation-lookup`, `e2e-testing`, `eval-harness`, `everything-claude-code`, `exa-search`, `fal-ai-media`, `frontend-patterns`, `frontend-slides`, `investor-materials`, `investor-outreach`, `market-research`, `mcp-server-patterns`, `mle-workflow`, `nextjs-turbopack`, `plan-canvas`, `product-capability`, `security-review`, `strategic-compact`, `tdd-workflow`, `unified-memory`, `verification-loop`, `video-editing`, `x-api`

2. **Standard format** (`~/.hermes/skills/`) — SKILL.md only
   - Core skills: `configure-ecc`, `ecc-guide`, `ecc-recipes`, `tdd-workflow`, `unified-memory`, `verification-loop`, `continuous-learning`, `continuous-learning-v2`, `agent-self-evaluation`, `architecture-decision-records`, `browser-qa`, `ck`, `click-path-audit`, `code-tour`, `codebase-onboarding`, `codehealth-mcp`, `cognee`, `config-gc`, `context-budget`, `council`, `delivery-gate`, `error-handling`, `eval-harness`, `growth-log`, `hookify-rules`, `inherit-legacy-style`, `intent-driven-development`, `iterative-retrieval`, `loop-design-check`, `plan-canvas`, `plankton-code-quality`, `production-audit`, `repo-scan`, `rules-distill`, `santa-method`, `skill-scout`, `skill-stocktake`, `strategic-compact`, `windows-desktop-e2e`, `git-workflow`
   - Preserved existing: `davinci-resolve`, `davinci-resolve-techniques`, `videographer`, `video-effects`, `video-storyboard-generation`, `videography`, `apple-reminders-safety-workflow`, etc.

### Commands (94)
Location: `~/.hermes/commands/`
Examples: `plan.md`, `code-review.md`, `build-fix.md`, `security-scan.md`, `tdd-workflow.md`, `feature-dev.md`, `refactor-clean.md`, `review-pr.md`, `prp-plan.md`, `prp-implement.md`, `ecc-guide.md`, `multi-plan.md`, `multi-execute.md`, `multi-backend.md`, `multi-frontend.md`, `multi-workflow.md`, `loop-start.md`, `loop-status.md`, `harness-audit.md`, `hookify.md`, `instinct-export.md`, `instinct-import.md`, `save-session.md`, `resume-session.md`, `quality-gate.md`

### Rules (23 language packs)
Location: `~/.hermes/rules/`
Packs: `common`, `typescript`, `python`, `web`, `react`, `vue`, `angular`, `rust`, `go`, `java`, `kotlin`, `swift`, `ruby`, `php`, `perl`, `cpp`, `csharp`, `dart`, `fsharp`, `golang`, `nuxt`, `react-native`, `arkts`

### MCP Configs
Location: `~/.hermes/mcp-configs/mcp-servers.json`
Default enabled: `chrome-devtools` only
Others opt-in from bundled catalog

### Install State
Location: `~/.hermes/ecc-install-state.json`
Tracks all 457 applied operations for upgrades/uninstall

## Key Learnings

### PATH Issue with npm Global Binaries
The `ecc-install` binary from `npm install -g ecc-universal` was not on PATH. Workaround:
```bash
node $(npm root -g)/ecc-universal/scripts/install-apply.js --profile minimal --target hermes
```

### Two Skill Formats for Hermes
ECC installs skills in both:
- `.agents/skills/` — Hermes-native with agent delegation support
- `skills/` — Standard format for direct skill loading

Both are usable; choose based on whether you need agent delegation.

### Config Files Preserved
- `config.yaml` — NOT modified
- `.env` — NOT modified
- Existing skills/memories — NOT modified
- Only new ECC files added

## Verification Commands
```bash
# Doctor check
node $(npm root -g)/ecc-universal/scripts/ecc.js doctor --target hermes

# List installed skills
ls ~/.hermes/.agents/skills/
ls ~/.hermes/skills/

# List installed agents
ls ~/.hermes/agents/

# List installed commands
ls ~/.hermes/commands/

# List rule packs
ls ~/.hermes/rules/
```