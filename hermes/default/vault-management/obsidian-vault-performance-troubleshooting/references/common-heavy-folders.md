# Common Heavy Folders Checklist

When troubleshooting slow Obsidian vaults, check for these folders first:

## High Priority (Almost Always Problematic)

| Folder | Why | Typical Size | Action |
|--------|-----|--------------|--------|
| `node_modules/` | 1000s of tiny files, npm packages | 50-500 MB | Move outside vault; use symlink if needed for dev |
| `Transcripts/` / `exports/` / `output/` | Auto-generated content, 1000s of files | 100 MB - 2 GB | Move outside vault; these are rarely edited in Obsidian |
| `.git/` (inside vault) | Git history, objects, refs | 50 MB - 5 GB | Move repo outside vault; use submodule or separate clone |
| `dist/` / `build/` / `.next/` / `out/` | Build artifacts | 10-500 MB | Exclude from vault; build outputs don't belong in notes |
| `.cache/` / `cache/` / `tmp/` | Temporary files | Variable | Delete or move outside vault |

## Medium Priority (Often Problematic)

| Folder | Why | Typical Size | Action |
|--------|-----|--------------|--------|
| `backups/` / `.obsidian/backups/` | Obsidian auto-backups | 10-500 MB | Configure backup location outside vault |
| `attachments/` with media | Large binary files | Variable | Consider external media library |
| `plugins/` (dev repos) | Full source repos, not built plugins | 10-100 MB | Build plugin, install built version only |
| `venv/` / `.venv/` / `env/` | Python virtual envs | 50-500 MB | Never keep in vault |
| `__pycache__/` / `.pytest_cache/` | Python cache | 10-100 MB | Add to .gitignore, delete |

## Low Priority (Check If Others Clean)

| Folder | Why | Typical Size | Action |
|--------|-----|--------------|--------|
| `.obsidian/plugins/` (many) | Many community plugins = many main.js files | 10-100 MB | Disable unused plugins |
| Large image folders | Many high-res images | Variable | Consider external asset management |
| PDF folders | Large PDFs | Variable | Link to external files instead |

## Quick Scan Command

```bash
# Find top 20 largest folders in vault
du -sh /path/to/vault/* 2>/dev/null | sort -hr | head -20

# Find folders with most files
find /path/to/vault -maxdepth 2 -type d | xargs sh -c 'for d; do echo "$(find "$d" -type f | wc -l) $d"; done' _ | sort -nr | head -20

# Find node_modules anywhere in vault
find /path/to/vault -name "node_modules" -type d 2>/dev/null
```

## Decision Tree

```
Is folder > 50 MB?
  ├─ Yes → Is it generated/derived content? (node_modules, dist, transcripts)
  │         ├─ Yes → MOVE OUTSIDE VAULT (archive, don't delete)
  │         └─ No → Is it source you edit in Obsidian?
  │                   ├─ Yes → Keep, but consider splitting
  │                   └─ No → MOVE OUTSIDE VAULT
  └─ No → Does it have > 1000 files?
            ├─ Yes → MOVE OUTSIDE VAULT
            └─ No → Probably fine
```