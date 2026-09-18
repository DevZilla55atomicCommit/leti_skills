---
name: claude-code-desktop-plugins
description: "Use when working with Claude Code Desktop plugin skills."
---

# Claude Code Desktop Plugins

Plugin skills resolve in the Desktop app only through the marketplace system — never by bare skill name, never by copying CLI legacy files.

## Procedure

1. **Add the marketplace once per machine:** `claude plugin marketplace add <owner>/<repo>` — validates the manifest. "Already added" means CLI and app share the entry; stop, do not re-add.
2. **Install user-scope:** `claude plugin install <plugin>@<marketplace>`. Confirm with `claude plugin list` (Status: enabled) and the `enabledPlugins` map in `~/.claude/settings.json`.
3. **Invoke namespaced, always:** `<plugin>:<skill>` in prompts and docs. Bare names return SKILL NOT FOUND even when the plugin is installed — that is a resolution rule, not an install failure. Do not reinstall to fix it; qualify the name.
4. **Probe in the runtime that will build** (see `references/probe-patterns.md`): demand verbatim section text, never accept a fluent summary as proof. Probe CLI and Desktop separately; one passing never proves the other.
5. **Bump the version on every skill edit:** the updater keys off `plugin.json` version, so text-only changes report "already at the latest" and keep serving stale content. Bump patch per edit; reinstall to force a refresh.

## Pitfalls

- Legacy `~/.claude/skills/*.md` single files do not transfer to the app — only marketplace plugins and project-local `.claude/skills/` resolve there. Do not bulk-copy them; port one skill at a time into plugin format.
- If the app's Plugins tab has no Discover or marketplace-add UI, use the CLI commands or in-session `/plugin` — same store, same result.
- Project docs should vendor the briefs/checklists inline and instruct the app to fall back to them (noting the miss in its report) — a build must never stall on skill resolution.
