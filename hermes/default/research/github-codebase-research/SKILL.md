---
name: github-codebase-research
description: Research an open-source GitHub repository using Hermes Agent's browsing tools.
category: research
license: MIT
---

# GitHub Codebase Research Skill

This skill captures the workflow for exploring, analyzing, and extracting information from a GitHub repository using the Hermes Agent's browsing toolset.

## When to Use

- Investigating a new library or package
- Understanding project structure, entry points, and documentation
- Extracting configuration files (e.g., package.json, README, docs)
- Setting up environment or discovering extension points

## Core Workflow

### Option A: Local clone + file tools (recommended for large repos)
1. **Clone locally**  
   `git clone --depth 1 <repo-url> /tmp/<repo-name>`

2. **Explore structure**  
   `ls -la /tmp/<repo-name>` → `find /tmp/<repo-name> -type f -name "*.md" -o -name "*.json" -o -name "*.yaml" | head -50`

3. **Read key files directly**  
   Use `read_file` for `README.md`, `package.json`, `AGENTS.md`, `CONTRIBUTING.md`, docs/ index files.

4. **Search for patterns**  
   Use `search_files` to locate config, docs, or specific terms across the codebase.

5. **Summarize findings**  
   Extract key details into a concise report.

### Option B: Browser-based (for quick lookups / no clone)
1. **Navigate to repository homepage**  
   Use `browser_navigate` to load the repo URL.

2. **Inspect file tree**  
   Use `browser_snapshot` (full) to get a searchable AX tree and identify key directories.

3. **Fetch critical files**  
   - `package.json` via raw URL (`https://raw.githubusercontent.com/.../package.json`)  
   - `docs/` index or quickstart files (`docs/index.md`, `docs/quickstart.md`)  
   - `README.md`, `CONTRIBUTING.md`, `docs/providers.md`, `docs/skills.md`

4. **Capture documentation**  
   Use `browser_navigate` + `browser_snapshot` to view docs in raw form for full text access.

5. **Summarize findings**  
   Extract key details (name, version, description, scripts, dependencies) into a concise report.

6. **Store support files**  
   - `references/workflow.md` – detailed step‑by‑step reproduction.  
   - `scripts/reproduce.sh` – optional script scaffold for automating the fetch process.

## Pitfalls & Fixes

- **HTML vs raw**: Browsing a GitHub tree returns an HTML page; to get plain text you must request the raw file (`.raw.githubusercontent.com`).  
- **Truncation**: Large snapshots may be truncated; use `browser_snapshot(full=true)` to get full content.  
- **Missing element IDs**: When clicking elements, verify the element index via `element` overlay in `som` mode.  
- **Rate limiting**: GitHub may block repeated raw requests; add a delay or use a cached copy.

## Support Files

- `references/workflow.md` – full reproduction of the research process, including terminal commands and browser interactions.  
- `scripts/reproduce.sh` – placeholder script that can be expanded to automate the fetch sequence.

---

## Example Usage

```
/skill:github-codebase-research https://github.com/earendil-works/pi
```

The skill will guide you through each step, loading the appropriate documentation and extracting the necessary metadata.