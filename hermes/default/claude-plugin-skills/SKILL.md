---
name: claude-plugin-skills
description: "Use when shipping Claude Code skills across runtimes."
---

# Claude Plugin Skills — Distribute and Resolve Across Runtimes

Ship skills once, resolve everywhere: a GitHub marketplace both the CLI and
managed desktop runtimes install from, with probes that prove resolution and
a fallback that survives it failing.

## Procedure

1. **Lay out the marketplace.** Repo root holds `.claude-plugin/marketplace.json`
   (registry: name, owner, plugins[] with name + source + version); each
   plugin lives at `plugins/<name>/` with `.claude-plugin/plugin.json`
   (name, description, version, `skills: "./skills/"`) and
   `skills/<skill>/SKILL.md` (frontmatter name + description, imperative body).
2. **Validate before publishing.** `claude plugin validate <marketplace-dir>`
   must pass, and both JSON files must parse — push only after green.
3. **Install per machine.** `claude plugin marketplace add <owner>/<repo>`
   then `claude plugin install <plugin>@<marketplace>` (user scope for
   cross-project use). Confirm with `claude plugin list` (enabled).
4. **Probe resolution, don't assume it.** Managed runtimes may fail bare skill
   names while the namespaced `plugin:skill` form works — invoke the
   namespaced form and demand a quote-back of content only that skill
   contains. Generic descriptions hallucinate; verbatim unique text does not.
5. **Bump `plugin.json` version on every content edit.** The updater keys off
   the version string, not content — without a bump it reports "already
   latest" while serving stale text. Reinstall cleanly to force a re-pull.
6. **Vendor critical guidance inline in the project** (briefs, checklists as
   files the project already reads). A resolution failure then degrades to a
   note in the report, never a skipped phase. Add a startup gate to the
   project skill: quote back project facts from files in the first reply,
   STOP if anything is missing.

## Pitfalls

- A bare-name "not found" proves nothing about installation — always re-probe
  namespaced before diagnosing, because the two forms resolve independently.
- "Marketplace already added" on a second runtime means shared state, not an
  error — check the installed list before reinstalling, since duplicates are
  impossible and retries waste the session.
- Keep skill names project-neutral once installed globally — a name tied to
  one project confuses every future build that loads it.
