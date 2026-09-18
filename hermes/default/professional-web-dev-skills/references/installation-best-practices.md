# Installation Best Practices

## General
- Install one skill at a time to avoid API rate limiting (429 errors).
- If API fails, manually copy the skill file from the repo to `~/.claude/skills/`.
- Verify installation by reading the skill file.

## Handling Large Skills
- Skills exceeding ~1000 lines may need to be processed in chunks.
- Use `skill_view` to inspect content before installation.
- For very large skills, consider splitting into smaller functional units.

## Verification
- After installing, run `ls -la ~/.claude/skills/` to confirm file presence.
- Use `head -n 20 ~/.claude/skills/<skill>.md` to preview.
- Test natural-language trigger: `/<skill-name> Create a brief example`.