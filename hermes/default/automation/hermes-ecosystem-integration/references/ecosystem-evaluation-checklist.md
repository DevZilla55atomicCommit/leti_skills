---
source: session evaluation pattern for agent ecosystems
date: 2026-08-04
purpose: reusable checklist for evaluating any large agent ecosystem for Hermes integration
---

# Ecosystem Evaluation Checklist

Use this checklist when evaluating a new AI agent ecosystem (Agentic OS, custom framework, etc.) for Hermes integration.

## 1. Harness Support Detection

| Check | Pass Criteria | Location |
|-------|---------------|----------|
| Hermes-specific docs | `.hermes/README.md` or `docs/HERMES-*.md` exists | Repo root / docs/ |
| Target-aware installer | `install.sh` or `install.ps1` accepts `--target hermes` | Repo root |
| Skill packaging | Skills in `.agents/skills/` or `skills/` as standalone dirs | Repo root |
| Plugin manifest | `.codex-plugin/plugin.json` or similar showing skill structure | Repo root |
| Config isolation statement | Explicit note that harness config files are NOT touched | `.hermes/README.md` |

**If ≥3 checks pass → ecosystem has native Hermes support.**

## 2. Component Boundaries

Identify and catalog each component type:

| Component | Location in Repo | Hermes Mapping | Install Method |
|-----------|------------------|----------------|----------------|
| Agents | `agents/*.md` | Delegation targets | Copy to `~/.hermes/agents/` or via installer |
| Skills | `.agents/skills/` or `skills/` | Hermes skills | Installer or manual copy |
| Commands | `commands/*.md` | Slash-commands | Installer or manual copy |
| Rules | `rules/<language>/` | Always-loaded context | Manual copy to `~/.hermes/rules/` |
| Hooks | `hooks/` or `.hooks/` | Hook runtime | Installer `--modules hooks-runtime` |
| MCP Configs | `mcp-configs/` or `.mcp.json` | MCP servers | Copy to project `.mcp.json` |
| Memory/Handoff | Custom CLI or MCP | Cross-harness memory | Separate install (`npm i -g pkg`) |

## 3. Install Profile Assessment

| Profile | Components Included | Risk Level | Hermes Rec |
|---------|---------------------|------------|------------|
| `minimal` | Rules + core skills only | Low | ✅ Recommended |
| `core` | + baseline hooks | Medium | ⚠️ If hooks needed |
| `full` | Everything + all hooks | High | ❌ Avoid (plugin conflicts) |

**Decision rule:** Start with `minimal`. Add `--modules hooks-runtime` only if hook automation is explicitly needed.

## 4. Config Isolation Verification

Before installing, verify:

- [ ] Installer does NOT modify `~/.hermes/config.yaml`
- [ ] Installer does NOT modify `~/.hermes/.env`
- [ ] Installer does NOT overwrite existing `~/.hermes/skills/` without warning
- [ ] Installer creates namespaced directories (`ecc-imports/`, `ecc/`) not flat
- [ ] Uninstall path exists and is documented

## 5. Skill Discovery Test

After install (or manual copy), verify:

```bash
# Skills appear in Hermes skill list
ls ~/.hermes/skills/ecc-imports/ | wc -l
# Should match expected count

# Skill loads without error
# (In Hermes chat) invoke skill by name
```

## 6. Resource Cost Estimation

| Factor | Estimation Method | Threshold |
|--------|-------------------|-----------|
| Context window (rules) | Sum of rule pack file sizes | >50KB = consider selective rules |
| Skill count | `ls skills/ | wc -l` | >100 = prefer cherry-pick |
| Hook count | `cat hooks/hooks.json \| jq '.hooks \| length'` | >10 = evaluate necessity |
| Memory vault | Separate process? | Yes = additional RAM/CPU |

## 7. Maintenance Model

| Question | Good Signal | Bad Signal |
|----------|-------------|------------|
| Versioning | Semantic version tags, changelog | No tags, only main branch |
| Release cadence | Monthly/quarterly | Years between releases |
| Breaking changes | Documented migration guide | Silent breaking changes |
| Hermes-specific issues | Tracked in issue tracker | No Hermes label/component |
| Community | Active Discord/GitHub discussions | Single maintainer, no community |

## 8. Decision Matrix

| Score | Action |
|-------|--------|
| Native Hermes support + minimal profile + config isolation | **Install via ecosystem installer** |
| Native support but heavy hooks/rules | **Cherry-pick skills only** |
| No native support but skills are portable | **Manual skill copy + adapt** |
| No skill portability, monolithic | **Don't integrate — use in native harness** |

## Quick Reference: Red Flags

- ❌ "Just copy the whole repo to ~/.hermes/"
- ❌ Installer overwrites `config.yaml` or `.env`
- ❌ Skills nested under `skills/ecosystem-name/` (Hermes expects flat)
- ❌ No uninstall documentation
- ❌ Hooks.json meant to be copied directly to `settings.json`
- ❌ Single massive skill directory instead of modular skills
- ❌ Requires global npm package that conflicts with Hermes deps

---

## Usage

Run this checklist when:
1. User asks about a new ecosystem
2. You encounter an unfamiliar agent framework in a repo
3. Evaluating whether to adopt a framework for a project

Document findings in `references/<ecosystem>-evaluation.md` for future reference.