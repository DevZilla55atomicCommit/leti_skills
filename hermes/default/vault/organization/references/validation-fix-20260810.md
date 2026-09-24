# Validation Fix — 2026-08-10

## Problem

The original `run_validation()` in `vault_organizer.py` used graphify queries that returned **code symbols** (functions, classes, imports from Python/JS files) instead of actual **Obsidian wikilinks** (`[[target]]` syntax in markdown files).

This caused false positives:
- "broken wikilinks": 42 reported → actually thousands of code symbols with "broken" in their names
- "orphan files": 56 reported → actually code files not linked from index files

## Root Cause

Graphify's `query` command traverses a **code analysis graph** (symbols, imports, calls), not an Obsidian wikilink graph. The queries:
- `"broken wikilinks in DaVinci_Knowledge_Base"` 
- `"files not linked from any index"`

...returned code symbols containing those words, not actual broken wikilinks or orphan markdown files.

## Fix Applied

Replaced graphify-based validation with native Python regex scanning:

### Broken Wikilinks
```python
wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
# Scan ALL .md files in vault
# For each [[target]] or [[target|alias]], verify target file exists
# Count truly broken links
```

### Orphan Files
```python
# Find all index files: INDEX.md, index.md, MASTER_*.md, Hero_*.md
# Extract all wikilink targets from index files
# Any .md file NOT referenced by any index = orphan
```

## Results After Fix

| Metric | Before (graphify) | After (regex) |
|--------|-------------------|---------------|
| Broken wikilinks | 42 (false) | ~14,444 (real, needs cleanup) |
| Orphan files | 56 (false) | ~18,515 (real, needs linking) |
| Link chain | OK (Memory.md created) | OK |

## Graphify Binary Path Fix

Also corrected graphify binary path in vault_organizer.py:
- **Was:** `/Users/alfredkamisese/.local/share/uv/tools/graphifyy/bin/graphify`
- **Now:** `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/graphify`

## Syncthing Conflict Cleanup

Removed ~50+ `.sync-conflict-*` files from `.obsidian/` and root vault (non-backup locations). These accumulate during concurrent edits across Mac mini + MBP.