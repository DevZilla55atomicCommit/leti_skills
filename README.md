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
