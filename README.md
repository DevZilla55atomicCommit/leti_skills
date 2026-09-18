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