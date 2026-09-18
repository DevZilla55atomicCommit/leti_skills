---
name: mobile-documentation-scaffold
title: Mobile Documentation Scaffold
description: Generate docs for mobile planning.
---

# Markdown Documentation Scaffold

Use this skill to generate structured documentation files for mobile app planning including:

- Feature specifications
- Screen specifications
- Architecture decision records (ADRs)
- Permission priming screens
- API contracts
- Research comparisons

## Process

1. **Identify target**: Determine which type of documentation is needed (feature, screen, ADR, etc.).
2. **Select template**: Choose appropriate markdown template from `templates/` directory.
3. **Fill details**: Populate sections using information from Linear tickets, Figma designs, and research.
4. **Save to vault**: Write the completed markdown file to the appropriate path in the Obsidian vault.
5. **Reference**: Add entry to `references/scaffolded-docs-paths.md` for future scaffolding.

## Templates

Templates are stored in the `templates/` directory and include:

- `feature-spec.md.tmpl`
- `screen-spec.md.tmpl`
- `adr.md.tmpl`
- `permissions-spec.md.tmpl`

## References

See `references/scaffolded-docs-paths.md` for a list of paths of documents generated in this session.

## Related Skills

- `project-management` — for tracking documentation tasks in Linear
- `automation` — for scripting repetitive documentation steps
- `hermes-agent` — for orchestrating multi-step documentation workflows