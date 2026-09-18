# Harness Comparison: ECC Profiles and Components

## Profile Matrix

| Component | Minimal | Core | Full |
|-----------|---------|------|------|
| rules-core | ✅ | ✅ | ✅ |
| agents-core | ✅ | ✅ | ✅ |
| commands-core | ✅ | ✅ | ✅ |
| platform-configs | ✅ | ✅ | ✅ |
| skill-unified-memory | ✅ | ✅ | ✅ |
| workflow-quality | ✅ | ✅ | ✅ |
| hooks-runtime | ❌ | ✅ | ✅ |
| legacy-command-shims | ❌ | ❌ | ✅ |
| All skills | ❌ | ❌ | ✅ |
| All agents | ❌ | ❌ | ✅ |
| All commands | ❌ | ❌ | ✅ |

## Harness-Specific Install Methods

### Hermes
```bash
# Via ecc-universal (recommended)
npm install -g ecc-universal
ecc-install --profile minimal --target hermes

# Direct script (if PATH issues)
node $(npm root -g)/ecc-universal/scripts/install-apply.js --profile minimal --target hermes
```
**Installs to:** `~/.hermes/`
**Skill formats:** Dual — `.agents/skills/` (Hermes-native) + `skills/` (standard)
**Config preserved:** `config.yaml`, `.env`, existing skills

### Claude Code
```bash
# Plugin-first (recommended)
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc

# Manual rules copy (plugins can't distribute rules)
git clone https://github.com/affaan-m/ECC.git
cd ECC
mkdir -p ~/.claude/rules/ecc
cp -R rules/common ~/.claude/rules/ecc/
cp -R rules/typescript ~/.claude/rules/ecc/  # your stack

# Manual install (avoid stacking with plugin)
./install.sh --profile full --target claude
```
**Installs to:** `~/.claude/`
**Skill format:** Flat under `~/.claude/skills/<skill>/`
**Rules:** Manual copy required (plugin limitation)

### Codex
```bash
# Sync flow (recommended - preserves existing Codex config)
git clone https://github.com/affaan-m/ECC.git
cd ECC
npm install
bash scripts/sync-ecc-to-codex.sh

# Marketplace plugin (experimental)
codex plugin marketplace add affaan-m/ECC
codex plugin marketplace list
# Restart Codex, install/enable 'ecc'
```
**Installs to:** `~/.codex/`
**Preserves:** Existing Codex files with timestamped backups

### Cursor
```bash
# Project-local adapter
./install.sh --profile minimal --target cursor
```
**Installs to:** `.cursor/` (project-local)
**Agents:** Under `.cursor/agents/ecc-*.md`

### Other Harnesses
| Harness | Command |
|---------|---------|
| OpenCode | `npm install && npm run build:opencode && ./install.sh --profile full --target opencode` |
| Gemini CLI | `./install.sh --profile minimal --target gemini` |
| Zed | `./install.sh --profile minimal --target zed` |
| Antigravity | `./install.sh --profile minimal --target antigravity` |
| Qwen CLI | `./install.sh --profile minimal --target qwen` |
| OpenClaw | `./install.sh --profile minimal --target openclaw` |
| Kimi | `./install.sh --profile minimal --target kimi` |
| CodeBuddy | `./install.sh --profile minimal --target codebuddy` |
| JoyCode | `./install.sh --profile minimal --target joycode` |

## Component Breakdown

### Rules (23 packs)
All profiles include `rules-core` (common + 22 language packs):
- common, typescript, python, web, react, vue, angular
- rust, go, java, kotlin, swift, ruby, php, perl
- cpp, csharp, dart, fsharp, golang, nuxt, react-native, arkts

### Agents (67 total)
Core profiles include `agents-core` (subset). Full includes all 67:
- Planning: `planner`, `architect`, `code-architect`, `chief-of-staff`
- Review: `code-reviewer`, `security-reviewer`, `spec-miner`
- Build: `build-error-resolver`, `cpp-build-resolver`, `django-build-resolver`, `go-build-resolver`, `java-build-resolver`, `kotlin-build-resolver`, `pytorch-build-resolver`, `react-build-resolver`, `rust-build-resolver`, `swift-build-resolver`
- Language reviewers: `cpp-reviewer`, `csharp-reviewer`, `django-reviewer`, `fastapi-reviewer`, `flutter-reviewer`, `fsharp-reviewer`, `go-reviewer`, `java-reviewer`, `kotlin-reviewer`, `python-reviewer`, `rust-reviewer`, `swift-reviewer`, `typescript-reviewer`, `vue-reviewer`
- Specialized: `a11y-architect`, `agent-evaluator`, `database-reviewer`, `docs-lookup`, `e2e-runner`, `gan-evaluator`, `gan-generator`, `gan-planner`, `harmonyos-app-resolver`, `harness-optimizer`, `healthcare-reviewer`, `homelab-architect`, `loop-operator`, `marketing-agent`, `mle-reviewer`, `network-architect`, `network-config-reviewer`, `network-troubleshooter`, `opensource-forker`, `opensource-packager`, `opensource-sanitizer`, `performance-optimizer`, `php-reviewer`, `pr-test-analyzer`, `refactor-cleaner`, `seo-specialist`, `silent-failure-hunter`, `tdd-guide`, `type-design-analyzer`

### Commands (94 total)
Core profiles include `commands-core` (subset). Full includes all 94 + legacy shims.

### Skills (281+ total)
Minimal includes `skill-unified-memory` + `workflow-quality` (core skills only).
Full includes all 281+ skills.

## Key Differences Summary

| Aspect | Hermes | Claude Code | Codex |
|--------|--------|-------------|-------|
| **Primary method** | ecc-universal CLI | Plugin marketplace | Sync flow |
| **Config location** | `~/.hermes/` | `~/.claude/` | `~/.codex/` |
| **Skill format** | Dual (.agents/ + skills/) | Flat (skills/) | Synced to .codex/ |
| **Rules** | Auto-installed | Manual copy | Auto-synced |
| **Hooks** | Via skill-unified-memory | Via hooks-runtime module | Via sync |
| **MCP** | Opt-in from mcp-configs | Manual /mcp command | Auto-synced |
| **Memory Vault** | ecc-memory-mcp opt-in | ecc-memory-mcp opt-in | ecc-memory-mcp opt-in |
| **Config preserved** | Yes | Yes | Yes (backups) |

## Recommendation by Use Case

| Scenario | Recommended Profile | Harness |
|----------|-------------------|---------|
| New Hermes setup | `minimal` | Hermes |
| Full CI/CD with hooks | `core` | Hermes/Claude |
| Maximum features | `full` | Any |
| Quick trial | `minimal` | Any |
| Team shared config | `core` + rules | Hermes/Claude |

## Pitfalls Across Harnesses

1. **Don't stack methods** — Plugin + manual install = duplicates
2. **Rules in Claude Code** — Must manually copy from `rules/` after plugin install
3. **PATH issues** — Use `$(npm root -g)/ecc-universal/scripts/` if binaries not linked
4. **MCP servers** — Opt-in only; default is `chrome-devtools` only
5. **Codex marketplace plugin** — Experimental; sync flow more reliable
6. **Cursor agents** — Installed to `.cursor/agents/`, not global