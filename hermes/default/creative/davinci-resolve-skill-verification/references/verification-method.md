## Verification Method

This verification script checks DaVinci Resolve skills by:

1. Finding all directories matching `davinci-resolve*` under `~/.hermes/skills/creative`.
2. For each directory, checking existence and readability of `SKILL.md`.
3. Validating that `SKILL.md` contains proper YAML frontmatter (`---` at start) and non-empty content.
4. Reporting results in a JSON structure saved to the vault.

### Validation Logic

- **SKILL.md Presence**: Must exist as a file.
- **Frontmatter Check**: First non-empty line must be `---` indicating YAML frontmatter.
- **Size Check**: File size must be greater than 0 bytes.
- **Error Reporting**: Any failure is recorded with an error message in the results JSON.

### Extending the Validation

To add custom checks (e.g., specific required fields in frontmatter), modify the script in `scripts/verify_davinci_skills.py` and update this documentation accordingly.