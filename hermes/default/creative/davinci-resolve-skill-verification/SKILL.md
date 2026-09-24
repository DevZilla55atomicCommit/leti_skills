---
name: davinci-resolve-skill-verification
description: Skill to verify DaVinci Resolve skills have valid SKILL.md files.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Verification, Tool]
---
# DaVinci Resolve Skills Verification

This skill provides a verification mechanism to ensure all DaVinci Resolve skills under `~/.hermes/skills/creative` have valid `SKILL.md` files.

## Verification Script

The script `verify_davinci_skills.py` scans the skills directory for any folder matching `davinci-resolve*`, checks for the presence and validity of `SKILL.md`, and outputs a JSON report.

### Output

The JSON report includes:
- Timestamp
- Skills directory path
- Pattern used
- Total skills found
- Counts of valid, missing, invalid files
- Detailed list of each skill with its status and any errors

### Usage

```bash
python3 verify_davinci_skills.py
```

The script exits with code 1 if any skill is missing or invalid, otherwise 0.

### Pitfalls

- Ensure the script has execute permissions if you plan to run it directly.
- The script assumes the skills are located at `~/.hermes/skills/creative`.
- Verify that the vault path (`/Users/alfredkamisese/tony-ai-agent/vault/...`) is writable.

## Support Files

- `scripts/verify_davinci_skills.py` – the verification script.
- `references/verification-method.md` – detailed explanation of the validation logic and how to extend the script.

## Extending

To add new checking criteria, modify the script in `scripts/` and update this skill's documentation accordingly.