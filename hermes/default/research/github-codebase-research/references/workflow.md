# Research Workflow

## Overview
This document captures the reproducible workflow for researching a GitHub repository using Hermes Agent's tools. Two approaches are supported:

- **Option A: Local clone + file tools** — recommended for large repos, deep analysis, or when you need to search across many files.
- **Option B: Browser-based** — quick lookups, no clone needed, good for single-file fetches.

---

## Option A: Local Clone + File Tools (Recommended)

### Step-by-Step

1. **Identify repository URL**  
   `REPO_URL="https://github.com/nexu-io/open-design"`

2. **Clone locally (shallow for speed)**  
   `git clone --depth 1 "$REPO_URL" /tmp/open-design`

3. **Explore structure**  
   ```bash
   ls -la /tmp/open-design
   find /tmp/open-design -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" \) | head -50
   ```

4. **Read key files directly**  
   Use `read_file` for:
   - `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `QUICKSTART.md`
   - `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`
   - Docs index: `docs/README.md`, `docs/architecture.md`, `docs/skills-protocol.md`, `docs/design-systems.md`

5. **Search for patterns**  
   Use `search_files` to locate:
   - Config files: `search_files(target='files', pattern='*.config.*')`
   - Specific terms: `search_files(pattern='design-system', target='content')`
   - CLI entry points: `search_files(pattern='mcp install', target='content')`

6. **Summarize findings**  
   Extract key metadata into a concise report (name, purpose, architecture, key directories, integration points).

7. **Store findings**  
   Append a concise summary to `references/summary.md` for future sessions.

---

## Option B: Browser-based (Quick Lookups)

1. **Navigate to repository homepage**  
   `browser_navigate --url "$REPO_URL"`

2. **Snapshot the AX tree**  
   `browser_snapshot --full` → inspect numbered overlays (`@e1`, `@e2`, …).

3. **Fetch critical raw files**  
   - `package.json`: `curl -s "https://raw.githubusercontent.com/nexu-io/open-design/main/package.json"`
   - `README.md`: `curl -s "https://raw.githubusercontent.com/nexu-io/open-design/main/README.md"`
   - Documentation: `browser_navigate --url "https://github.com/nexu-io/open-design/tree/main/docs"` → `browser_snapshot --full`

4. **Summarize key metadata**  
   - Name, version, description from `package.json`.
   - Main scripts (`build`, `test`, `lint`).
   - Dependency graph (optional).

---

## Pitfalls & Fixes

- **HTML vs raw**: Browsing a GitHub tree returns an HTML page; to get plain text you must request the raw file (`.raw.githubusercontent.com`).
- **Truncation**: Large snapshots may be truncated; use `browser_snapshot(full=true)` to get full content.
- **Missing element IDs**: When clicking elements, verify the element index via `element` overlay in `som` mode.
- **Rate limiting**: GitHub may block repeated raw requests; add a delay or use a cached copy.
- **Large repos**: Browser approach struggles with 10k+ file repos; prefer Option A (local clone).
- **System `od` binary conflict**: On macOS, `/usr/bin/od` (octal dump) shadows the Open Design `od` CLI. Use absolute path or `brew install nexu-io/tap/open-design` and ensure `/opt/homebrew/bin` is before `/usr/bin` in PATH.

---

## Support Files

- `references/workflow.md` – this file, full reproduction of the research process.
- `scripts/reproduce.sh` – placeholder script that can be expanded to automate the fetch sequence.
- `references/summary.md` – accumulating summary of researched repos (append-only).