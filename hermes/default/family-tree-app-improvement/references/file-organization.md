# File Organization & Scaffold Workflow

This skill captures the standardized project structure used for the Kasini Tree App and related family tree initiatives.

## Directory Structure

```
/plans/           # Improvement plans (KASINI_STREAM_PLAN.md, etc.)
 /analysis/        # Episode 6 breakdown and gaps
 /transcripts/     # Audio and video transcripts
 /scaffold/        # Professional Expo scaffold (package.json, src/, etc.)
 /design/          # Figma assets and design tokens
 /docs/            # API documentation, READMEs
 /references/      # Session-specific detail, knowledge banks, reference material
 /templates/       # Boilerplate configs and starter files
 /scripts/         # Reusable scripts (schema validation, verification)
```

## Recent Updates (2026-07-12)

- All project files have been moved into this standardized structure.
- Scaffold created at `/scaffold/kasini-tree-app/` with core components.
- Design tokens extracted to `constants/design-tokens.json`.
- Core types and components scaffolded.
- README and planning files placed in appropriate directories.

## How to Use

When starting a new family tree project:

1. Copy the entire scaffold directory.
2. Populate `/plans/` with project-specific plans.
3. Use `/references/` for session-specific notes.
4. Refer to `/templates/` for boilerplate files.
5. Run `npm install && npm run dev` to verify scaffold integrity.

## Reference Files

- `references/kasini-data-model.md` — Detailed schema and type definitions.
- `templates/expo-project-scaffold.zip` — Pre-configured Expo starter.
- `scripts/verify-schema.js` — Schema validation script.

*Keep this file updated with new organization patterns and workflow improvements.*