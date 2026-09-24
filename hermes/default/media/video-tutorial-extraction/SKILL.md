---
name: video-tutorial-extraction
description: "Extract structured tutorials from YouTube videos and convert to markdown for knowledge bases. Covers color grading, software workflows, and technical domains."
platforms: [linux, macos, windows]
---

# Video Tutorial Extraction Workflow

## When to Use

Use when the user wants to:
- Search YouTube for tutorials on a specific technical topic
- Extract transcripts and convert to structured markdown
- Build a knowledge base from video tutorials (color grading, software dev, ML ops, etc.)
- Cross-reference extracted content with existing documentation

## Core Workflow

### 1. Search & Identify
```bash
# Browser-based search for relevant videos
# Use specific queries: "S-Log3 color grading DaVinci Resolve 19 tutorial"
# Target channels: Kyle White, Danny Gan, Cullen Kelly, Mehran Hadad, Russell Wofford, CineMirage, FujiCinema
```

### 2. Fetch Transcript
Use the `youtube-content` skill's helper script via Hermes venv Python:
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python /Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py "VIDEO_URL" --timestamps --language en
```

**Note:** The `uv pip install` approach has permission issues on this system; youtube-transcript-api is pre-installed in the Hermes venv.

### 3. Extract Video ID
From browser console after navigating to video:
```javascript
window.location.href
// Returns: https://www.youtube.com/watch?v=VIDEO_ID
```

### 4. Structure as Markdown
Follow the template in `references/tutorial-markdown-template.md`

### 5. Cross-Reference in Knowledge Base
Update the domain's `Memory.md` with new entry in YouTube Tutorials section.

## Hermes Environment Notes

- **Python path:** `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python`
- **Transcript script:** `/Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py`
- **Vault location:** `/Users/alfredkamisese/TamaZila Obsidian Vault/`

## Domain-Specific Templates

See `references/` for templates:
- `color-grading-template.md` — DaVinci Resolve color grading tutorials
- `software-dev-template.md` — Software development tutorials
- `general-technical-template.md` — Generic technical tutorials
- `slog3-template.md` — Sony S-Log3 specific tutorials (FX3, A7S III, A7 IV, Venice)
- `apple-log-template.md` — iPhone Apple Log/Apple Log 2 tutorials

## Organization Patterns (Learned This Session)

### Folder Structure for Color Grading Tutorials
```
Color Grading & Looks/
├── Apple Log 2/          # iPhone Apple Log / Apple Log 2 tutorials
└── S-Log3/               # Sony S-Log2/3 tutorials
```

### Memory.md Cross-Reference Pattern
Use categorized sections with emoji headers:
```markdown
### 🎬 S-Log3 (Sony) Tutorials
*   **[Title]** :: `Color Grading & Looks/S-Log3/filename.md` — Summary...

### 🍎 Apple Log 2 (iPhone) Tutorials
*   **[Title]** :: `Color Grading & Looks/Apple Log 2/filename.md` — Summary...
```

### Transcript Fetching Command (Verified Working)

**Preferred: Direct file output (avoids terminal truncation)**
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python \
  /Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --timestamps --language en \
  > /path/to/output_transcript.json
```

**Alternative: Stream to file via Python**
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -c "
import json, sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts')
from fetch_transcript import main
import subprocess, json
result = subprocess.run([
    '/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python',
    '/Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py',
    'https://www.youtube.com/watch?v=VIDEO_ID',
    '--timestamps', '--language', 'en'
], capture_output=True, text=True)
with open('transcript_output.json', 'w') as f:
    f.write(result.stdout)
"
```

**Direct terminal (works but output may truncate):**
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python \
  /Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --timestamps --language en
```

### Video ID Extraction
From browser console after navigating to video page:
```javascript
window.location.href
// Returns full URL with VIDEO_ID
```

## Quality Checklist

- [ ] All CST/input/output parameters documented
- [ ] Node/workflow order matches video
- [ ] Domain-specific terminology used correctly
- [ ] Before/after philosophy explained
- [ ] Cross-references to existing vault docs
- [ ] Tags follow vault conventions

## Error Handling

- **Transcript disabled:** Note in markdown; suggest checking subtitles on video page
- **Private/unavailable:** Relay error, ask user to verify URL
- **No matching language:** Retry without `--language`, note actual language
- **Chunking:** If transcript >50K chars, split into overlapping chunks (~40K/2K overlap)