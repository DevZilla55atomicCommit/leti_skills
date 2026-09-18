# Fork vs. Upstream Checklist

Quick commands to resolve fork identity and freshness.

## GitHub UI

1. Open repo page → look under repo name: "forked from **owner/repo**"
2. Click the upstream link → compare "X commits behind" badge

## CLI (requires `gh`)

```bash
# Get upstream URL from fork
gh repo view DevZilla55atomicCommit/loop-engineering --json parent -q .parent.url

# Compare commit counts
gh api repos/DevZilla55atomicCommit/loop-engineering/compare/cobusgreyling:main...DevZilla55atomicCommit:main --jq '.ahead_by, .behind_by'

# Or with git (after cloning both)
git remote add upstream https://github.com/cobusgreyling/loop-engineering.git
git fetch upstream
git rev-list --count HEAD..upstream/main   # commits behind
git rev-list --count upstream/main..HEAD   # commits ahead (fork-only)
```

## Quick Heuristics

| Signal | Meaning |
|--------|---------|
| `behind_by > 10` | Fork is stale; use upstream |
| `behind_by == 0` | Fork is current; safe to use |
| No "forked from" badge | Not a fork — single origin |
| Fork has unique releases | Fork may be the real upstream now |

## When to Use Fork Anyway

- Fork has critical bugfix not yet merged upstream
- Fork publishes to npm/PyPI under different name (`@devzilla/loop-init` vs `@cobusgreyling/loop-init`)
- Upstream is abandoned; fork is active maintainer

## Cognee Example

```
DevZilla55atomicCommit/cognee → forked from topoteretes/cognee
  → "This branch is up to date with topoteretes/cognee:main"
  → USE UPSTREAM (topoteretes/cognee)
```