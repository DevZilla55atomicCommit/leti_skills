---
name: professional-web-dev-skills
description: Curated list of essential web development skills for professional web development using Claude Code and Hermes Agent.
category: software-development
---

# Professional Web Development Skills (Class-Level)

This umbrella skill defines **class-level web development skills** with rich documentation and reference material. Each class-level skill resides in its own directory under `~/.hermes/skills/` and includes:

- `SKILL.md` — comprehensive guide, triggers, workflows.
- `references/` — session-specific details, pitfalls, external research.
- `templates/` — starter boilerplates.
- `scripts/` — reusable verification scripts.

## Core Class-Level Skills

| Skill | Focus | Linked Reference |
|-------|-------|-------------------|
| `frontend-ui-engineering` | Accessibility, design systems, responsive UI | `references/frontend-ui-engineering.md` |
| `spec-driven-development` | Specification-driven workflow | `references/spec-driven-development.md` |
| `test-driven-development` | RED/GREEN/REFACTOR cycles | `references/test-driven-development.md` |
| `modern-web-design` | 2024-25 design trends & micro-interactions | `references/modern-web-design.md` |
| `threejs-webgl` | Custom 3D scenes with WebGL | `references/threejs-webgl.md` |
| `react-three-fiber` | Declarative 3D in React | `references/react-three-fiber.md` |
| `gsap-scrolltrigger` | Scroll-driven animations, pinning, scrubbing | `references/gsap-scrolltrigger.md` |
| `motion-framer` | React animations, layout animations, gesture support | `references/motion-framer.md` |
| `locomotive-scroll` | Smooth scroll with momentum | `references/locomotive-scroll.md` |
| `barba-js` | Page transitions | `references/barba-js.md` |
| `lightweight-3d-effects` | Vanta.js backgrounds, subtle 3D accents | `references/lightweight-3d-effects.md` |
| \`playcanvas-engine\` | Full-featured 3D engine | \`references/playcanvas-engine.md\` |

| \`obsidian-dashboard-plugin\` | Visualize pipeline stages and track metrics from daily notes | \`references/obsidian-dashboard-plugin.md\` |

## Adding a New Class-Level Skill

1. Create a directory under `~/.hermes/skills/<skill-name>/`.
2. Place the required files:
   - `SKILL.md` with the skill's content.
   - `references/` directory for session-specific details.
   - `templates/` for starter boilerplates.
   - `scripts/` for reusable verification scripts.
3. Update this index to link to the new skill's `references/` file.
4. Add an entry to `references/skill-index.md` for quick lookup.

## Maintenance Checklist

- Review `references/` after each skill update.
- Verify all linked files exist and are up‑to‑date.
- Quarterly audit of skill relevance and accuracy.

## Pitfalls

- **Scaffolding into a non-empty directory**: `create-next-app` aborts on ANY pre-existing file, including hidden directories — stash docs aside OUTSIDE the target dir (e.g. `/tmp/<name>-bak/`), scaffold, then restore, since it writes nothing before aborting.

- **Non-whitelisted tool writes**: Using `write_file` directly on a skill’s supporting files fails in background sessions. Use `skill_manage(action='patch' or 'write_file')` after loading the file with `skill_view` to ensure the edit is permitted.
- **Missing `references/skill-index.md`**: Without a central index, new skills can be hard to locate. Create and maintain `references/skill-index.md` to list all installed skill references.
- **Stale verification**: Skills that haven’t been verified in 90 days may be outdated. Add a quarterly reminder to re‑run `ls -la ~/.claude/skills/` and confirm each skill’s presence.

## User-Enforced Response Style Preferences (Class-Level)

The following constraints are now mandatory for all Hermes Agent responses in this skill's scope:

- NO PRELUDE: All responses MUST open with the technical answer/result. Absolutely NO filler phrases, greetings, or explanatory preamble.
- SINGLE-LINE FIRST: Default to single-line terminal commands. Only expand when workflow genuinely requires 5+ tool calls or non-trivial sequence.
- VERIFICATION FIRST: All tool outputs MUST be validated before reporting. Unverified outcomes MUST be prefixed with "UNVERIFIED" or "PENDING VERIFICATION".
- DIRECT CORRECTION: When user corrects style/format, the correction becomes an immutable rule in the relevant skill until explicitly overridden via clarify.
- NEVER ASSUME USER KNOWLEDGE: If missing context blocks progress, issue a single-sentence clarifying question.
- EXPLANATORY TEXT MUST IMMEDIATELY SUPPORT THE CORE ANSWER without narrative detour.
- PRECISION OVER PITY: Replace speculative language with explicit uncertainty phrasing: "I don't know, here's how we'd find out".

## References

- Installation best practices: `references/installation-best-practices.md`
- Top-level reference: `references/top-web-dev-skills-reference.md`

- Graphify Vault Integration: `references/graphify-vault-integration.md`