---
source: live session installing ECC into Hermes
date: 2026-08-04
harness: hermes
ecosystem: ECC (Everything Claude Code / Engineering Control Center)
version: 2.1.0
profile: minimal → full
---

# ECC Install Session Notes (2026-08-04)

## Actual Commands That Worked

### Step 1: Install npm package (provides binaries and full skill set)
```bash
npm install -g ecc-universal
# Installs to ~/.npm-global/lib/node_modules/ecc-universal/
```

### Step 2: Run installer via node (not `ecc-install` binary which wasn't on PATH)
```bash
# Minimal profile
node ~/.npm-global/lib/node_modules/ecc-universal/scripts/install-apply.js --profile minimal --target hermes

# Full profile (run after minimal to add more skills)
node ~/.npm-global/lib/node_modules/ecc-universal/scripts/install-apply.js --profile full --target hermes
```

## What Actually Installed

### Minimal Profile
- **67 agents** → `~/.hermes/agents/`
- **39 Hermes-native skills** → `~/.hermes/.agents/skills/` (with `agents/openai.yaml`)
- **94 commands** → `~/.hermes/commands/`
- **23 rule packs** → `~/.hermes/rules/`
- **134 ECC standard skills** → `~/.hermes/skills/` (from `skill-unified-memory` + `workflow-quality` modules)
- **MCP configs** → `~/.hermes/mcp-configs/mcp-servers.json`

### Full Profile (adds on top of minimal)
- **ito-compute skill** added to `~/.hermes/skills/`
- Same 39 Hermes-native skills in `.agents/skills/`
- **Total skills in `~/.hermes/skills/`: 134** (not 280)

## Modules Skipped by Full Profile

The installer output showed these modules as "Skipped modules":
- `hooks-runtime`, `framework-language`, `database`, `optimization-workflows`, `security`, `research-apis`, `business-content`, `operator-workflows`, `prediction-market-skills`, `social-distribution`, `media-generation`, `orchestration`, `swift-apple`, `agentic-patterns`, `devops-infra`, `machine-learning`, `supply-chain-domain`, `document-processing`

## Key Findings

1. **"Full" ≠ all 280 skills** — The npm package has 280 skills in `skills/`, but the installer's "full" profile only maps to a curated subset of modules. Many specialized modules are skipped.

2. **Two skill locations with different formats:**
   - `~/.hermes/.agents/skills/` — 39 skills with `agents/openai.yaml` for agent delegation (Hermes-native)
   - `~/.hermes/skills/` — 134 standard ECC skills (no agent delegation metadata)

3. **Remaining ~146 skills** are only in the npm package:
   ```
   ~/.npm-global/lib/node_modules/ecc-universal/skills/
   ```
   Cherry-pick with:
   ```bash
   cp -r ~/.npm-global/lib/node_modules/ecc-universal/skills/<skill-name> ~/.hermes/skills/
   ```

4. **`ecc-install` binary not on PATH** after global npm install — use `node scripts/install-apply.js` directly or add `$(npm bin -g)` to PATH.

5. **Doctor check passes:**
   ```bash
   node ~/.npm-global/lib/node_modules/ecc-universal/scripts/ecc.js doctor --target hermes
   # Status: OK, Issues: none
   ```

## Profile Comparison

| Aspect | Minimal | Full |
|--------|---------|------|
| Agents | 67 | 67 |
| Hermes-native skills (.agents/skills/) | 39 | 39 |
| Standard skills (skills/) | 134 | 134 |
| Commands | 94 | 94 |
| Rule packs | 23 | 23 |
| ito-compute skill | No | Yes |

## Recommendation for This User

Given focused stack (TypeScript/Next.js, Python, DaVinci, Forex, macOS):
- Current 134 skills cover: TDD, security-review, verification-loop, unified-memory, video-editing, api-design, frontend-patterns, python-patterns, etc.
- Add from npm package only if needed: `security-scan`, `fastapi-patterns`, `django-patterns`, `trading-*`, `forex-*` skills
- Don't chase "all 280" — most are niche (Laravel, Spring Boot, Kubernetes, HIPAA, DeFi, etc.)