---
title: "Graphify Add URL & Watch Mode"
source: "Graphify repository (tools/skillgen/fragments/references/add-watch.md)"
version: "0.9.9"
---

# Graphify Add URL & Watch Mode

## /graphify add: Fetch External Content

Fetch a URL, save to `./raw/`, and update the graph.

### Commands

```bash
# Fetch paper (arXiv, DOI, direct PDF)
/graphify add https://arxiv.org/abs/1706.03762

# Fetch YouTube video (requires [video] extra)
/graphify add https://youtube.com/watch?v=...

# Fetch any webpage
/graphify add https://example.com/blog/post

# With author/contributor metadata
/graphify add https://arxiv.org/abs/1706.03762 --author "Vaswani et al." --contributor "Alfred"
```

### What Happens

1. **Downloads** content to `./raw/<domain>_<timestamp>.<ext>`
2. **Extracts** based on type:
   - PDFs → text via pypdf
   - YouTube → transcript via yt-dlp + faster-whisper
   - Webpages → main content via readability
   - GitHub → repo metadata + README
3. **Updates graph** - runs incremental extraction on new file
4. **Saves manifest** - tracks source URL, author, contributor

### Supported Sources

| Source | Handler | Extras Needed |
|--------|---------|---------------|
| arXiv | PDF + metadata | [pdf] |
| YouTube | Transcript | [video] |
| GitHub | Repo clone + README | - |
| Direct PDF | pypdf | [pdf] |
| Webpage | Readability extraction | - |
| DOI | Resolves to PDF | [pdf] |

---

## --watch: Auto-Rebuild on File Changes

Watch a directory and auto-rebuild graph when files change.

### Command

```bash
# Watch current directory
/graphify . --watch

# Watch specific directory
/graphify ./src --watch

# With custom debounce (default 2s)
/graphify . --watch --debounce 5
```

### How It Works

1. **File watcher** (watchdog) monitors directory
2. **Debounce** - waits for quiet period (default 2s)
3. **Incremental update** - runs `--update` on changed files
4. **AST only for code** - no LLM cost for code changes
5. **Full semantic for docs/media** - if docs/images/video changed

### Use Cases

- **Development** - graph updates as you code
- **Documentation** - graph updates as you write docs
- **Meeting recordings** - drop video in folder, graph auto-updates

### Stopping

Press `Ctrl+C` to stop watcher. Graph state preserved in `graphify-out/`.

---

## Combined Workflow: Live Research

```bash
# Terminal 1: Start watcher
/graphify . --watch

# Terminal 2: Add papers as you find them
/graphify add https://arxiv.org/abs/1706.03762
/graphify add https://arxiv.org/abs/1810.04805

# Terminal 3: Query live graph
/graphify query "attention mechanism improvements"
```

---

## Implementation Details

### Add Flow

```
add URL
  → download to ./raw/
  → detect type (PDF, video, webpage, GitHub)
  → extract content (Pass 2/3)
  → save to ./raw/ + ./graphify-out/cache/
  → run --update on new file
  → update manifest with URL metadata
```

### Watch Flow

```
file change detected
  → debounce (wait for quiet)
  → detect changed files
  → if code: AST extraction (Pass 1)
  → if doc/image/video: semantic extraction (Pass 2/3)
  → merge + rebuild graph
  → update HTML viz
```

---

## Configuration

### Raw Directory

Default: `./raw/` (relative to project root)

Override: `GRAPHIFY_RAW_DIR=/custom/path`

### Debounce

Default: 2 seconds

Override: `--debounce N` or `GRAPHIFY_WATCH_DEBOUNCE=N`

### Video Transcription Model

Default: `base` (faster-whisper)

Override: `--whisper-model medium` or `GRAPHIFY_WHISPER_MODEL=medium`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `add` fails on YouTube | Install `[video]` extra: `uv tool install "graphifyy[video]"` |
| `add` fails on PDF | Install `[pdf]` extra: `uv tool install "graphifyy[pdf]"` |
| Watch not detecting changes | Check `watchdog` installed; try `--debounce 5` |
| Watch using too much CPU | Increase debounce; exclude `graphify-out/` in `.graphifyignore` |
| `add` metadata not in graph | Check `--author`/`--contributor` saved in manifest |