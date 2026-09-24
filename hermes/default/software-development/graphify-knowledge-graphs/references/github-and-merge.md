---
title: "Graphify GitHub Clone & Cross-Repo Merge"
source: "Graphify repository (tools/skillgen/fragments/references/github-and-merge.md)"
version: "0.9.9"
---

# Graphify GitHub Clone & Cross-Repo Merge

## Clone & Build Single Repo

```bash
# Clone and run full pipeline
/graphify https://github.com/owner/repo

# Specific branch
/graphify https://github.com/owner/repo --branch develop

# With Obsidian export
/graphify https://github.com/owner/repo --obsidian --obsidian-dir ~/vault/Graphify-repo
```

### What Happens

1. Clones to `./raw/github.com_owner_repo/`
2. Runs full pipeline on cloned repo
3. Outputs in `graphify-out/` (relative to where command run)
4. Manifest tracks repo URL for future updates

---

## Cross-Repo Merge

Build multiple repos into a single unified graph.

```bash
# Multiple URLs - builds each, merges into one graph
/graphify https://github.com/owner/repo1 https://github.com/owner/repo2

# Mixed: local path + URL
/graphify ./my-project https://github.com/owner/repo
```

### Merge Strategy

1. Each repo cloned to `./raw/github.com_owner_repo/`
2. Each repo extracted independently (parallel)
3. Extractions merged by node ID (deduplicated)
4. Single graph built from merged extractions
5. Single clustering run on combined graph
6. Cross-repo connections emerge via:
   - Shared package dependencies (package nodes are canonicalized)
   - Similar concept names (semantic similarity edges)
   - Explicit cross-references

### Package Manifest Canonicalization

Package manifests (`pyproject.toml`, `go.mod`, `pom.xml`, etc.) create **canonical package nodes**:
- One node per package name (not per manifest file)
- `depends_on` edges between packages
- A package referenced from 10 repos = 1 node with 10 `depends_on` edges
- Enables cross-repo dependency analysis

---

## Monorepo Support

For monorepos with multiple packages:

```bash
# Auto-detects subpackages via package manifests
/graphify https://github.com/owner/monorepo

# Or local monorepo
/graphify ./monorepo
```

### What Gets Detected

- Each `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` = package
- Package nodes linked to their source files
- Inter-package `depends_on` edges from manifest parsing
- Cross-package call/import edges from AST

---

## Updating Cloned Repos

```bash
# Pull latest and incremental update
/graphify https://github.com/owner/repo --update

# Or from the raw clone directory
cd ./raw/github.com_owner_repo
git pull
/graphify . --update
```

---

## GitHub Authentication

For private repos or rate limit avoidance:

```bash
# Set token (classic PAT with repo scope)
export GITHUB_TOKEN=ghp_xxx

# Or use gh CLI auth
gh auth login
# Graphify uses gh CLI if available
```

---

## Large Repo Handling

For repos > 500 files or > 2M words:

```bash
# Skip expensive clustering
/graphify https://github.com/owner/huge-repo --no-cluster

# Or narrow to subdirectory
# 1. Clone first
git clone https://github.com/owner/huge-repo ./raw/huge-repo

# 2. Run on specific subfolder
/graphify ./raw/huge-repo/src/core --obsidian --obsidian-dir ~/vault/Graphify-core
```

---

## Merge Graphs from Separate Runs

If you built graphs separately and want to combine:

```bash
# Build each separately
/graphify ./project-a
/graphify ./project-b

# Merge graphs
graphify merge-graphs project-a/graphify-out/graph.json project-b/graphify-out/graph.json --out merged.json

# Use merged graph
graphify query "question" --graph merged.json
```

---

## Cross-Repo Query Examples

```bash
# After merging multiple service repos:
/graphify query "which services call the User API?"

# Trace path across repos
/graphify path "AuthService" "PaymentService"

# Find shared dependencies
/graphify query "what packages do all services depend on?"
```

---

## CI/CD Integration

```yaml
# .github/workflows/graphify.yml
name: Graphify
on: [push, pull_request]
jobs:
  graph:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Graphify
        run: curl -LsSf https://astral.sh/uv/install.sh | sh && uv tool install graphifyy
      - name: Build graph
        run: /graphify . --no-viz
      - name: Upload graph artifacts
        uses: actions/upload-artifact@v4
        with:
          name: graphify-out
          path: graphify-out/
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Clone fails (private repo) | Set `GITHUB_TOKEN` or `gh auth login` |
| Rate limited | Use `GITHUB_TOKEN`; or clone manually first |
| Merge creates duplicates | Package canonicalization handles most; run `--force` full rebuild |
| Cross-repo edges missing | Check semantic extraction ran (needs API key for docs); AST-only won't infer cross-repo calls |
| Monorepo not detected | Ensure package manifests in subdirectories |