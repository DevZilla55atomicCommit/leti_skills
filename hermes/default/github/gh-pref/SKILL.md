---
name: gh-pref
description: "User prefers gh CLI for GitHub auth."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Preference, Authentication]
    related_skills: [github-auth]
---

# User Preference: GitHub Authentication

**User explicitly prefers Option A (gh CLI)** when available for connecting to existing repositories.

## Priority Flow

1. **Check if `gh` CLI is installed and authenticated** → use `gh auth` flow
2. **Only fall back to git-only token flows** when `gh` is unavailable

**Rationale**: User indicated Option A is "more reliable" for their workflow.

**Implementation**
- **First check**: `command -v gh &>/dev/null && gh auth status &>/dev/null`
- **If true**: Proceed with `gh auth login` / `gh auth setup-git`
- **If false**: Fall back to git token methods (HTTPS with PAT or SSH keys)

This preference should be referenced in any GitHub-related setup instructions.