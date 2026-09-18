# Video Tutorial Extraction Pattern

## Overview
This document captures the repeatable workflow for extracting technical tutorials from YouTube and converting them to structured markdown files for knowledge bases.

## Complete Workflow

### Phase 1: Search & Discovery
```
# Browser-based search with specific queries:
"S-Log3 color grading DaVinci Resolve 19 tutorial"
"Apple Log 2 DaVinci Resolve tutorial"
"Cinematic color grading DaVinci Resolve 21"

# Target authoritative channels:
- Kyle White (commercial/cinematic S-Log3)
- Danny Gan (minimalist CST workflows)
- Cullen Kelly (pro techniques, noise/highlight management)
- Mehran Hadad (Resolve 21, portrait PowerGrades)
- Russell Wofford (Apple Log 2, DWG Intermediate)
- CineMirage (LUT packs + manual grading)
- FujiCinema (beginner-friendly, film looks)
```

### Phase 2: Transcript Extraction
```bash
# Reliable execution path (Hermes venv):
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python \
  /Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py \
  "VIDEO_URL" --timestamps --language en
```

### Phase 3: Video ID Retrieval
```javascript
// Browser console after navigating to video:
window.location.href
// Returns: https://www.youtube.com/watch?v=VIDEO_ID
```

### Phase 4: Markdown Structuring
Use templates in `references/`:
- `color-grading-template.md` — DaVinci Resolve color grading
- `general-technical-template.md` — Other domains

### Phase 5: Knowledge Base Integration
1. Save markdown to domain folder (e.g., `Color Grading & Looks/`)
2. Update domain's `Memory.md` with entry in `## 🟣 YOUTUBE TUTORIALS` section
3. Format: `*   **[Title]** :: \`Path/File.md\` — [One-line technical summary]`

## Quality Standards

### Required Sections
- [ ] Metadata header (source, channel, duration, views, date, Resolve version, camera/log)
- [ ] Overview (2-3 sentences)
- [ ] Node/Workflow structure table
- [ ] Step-by-step with Resolve-specific terminology
- [ ] Settings reference tables (CST, exposure, contrast, etc.)
- [ ] Key principles/philosophy
- [ ] Assets & resources
- [ ] Cross-references to existing vault docs
- [ ] Tags following vault conventions

### Terminology Standards (DaVinci Resolve)
| Use This | Not This |
|----------|----------|
| Serial Node | Node (ambiguous) |
| Color Space Transform (CST) | Color space conversion |
| HDR Wheels | High Dynamic Range wheels |
| Primaries / Color Wheels | Color wheels (vague) |
| Power Window | Window (ambiguous) |
| Outside Node | Inverted window |
| Key Output | Key gain / LUT intensity |
| DaVinci Wide Gamut Intermediate | DWG Intermediate (define first) |
| ST2084 / PQ | HDR curve (vague) |
| Lum vs Sat | Luminance vs Saturation |

## Error Handling

- **Transcript disabled:** Note in markdown; suggest checking subtitles on video page
- **Private/unavailable:** Relay error, ask user to verify URL
- **No matching language:** Retry without `--language`, note actual language found
- **Chunking:** If transcript >50K chars, split into overlapping chunks (~40K/2K overlap)

## Hermes-Specific Notes

- **Python interpreter:** `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python`
- **Transcript script:** `/Users/alfredkamisese/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py`
- **Vault root:** `/Users/alfredkamisese/TamaZila Obsidian Vault/`
- **DaVinci KB:** `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`
- **Color Grading folder:** `.../Color Grading & Looks/`

## Cross-Reference Protocol

Every tutorial markdown MUST update the domain `Memory.md`:
```markdown
## 🟣 YOUTUBE TUTORIALS — Color Grading & Looks
*   **[Descriptive Title — Creator]** :: `Color Grading & Looks/Filename.md` — [Technical one-liner]
```

Tags must use vault conventions:
- `#S-Log3` `#S-Gamut3` `#S-Gamut3.Cine`
- `#Apple-Log` `#Apple-Log-2` `#Rec2020` `#Rec709`
- `#ColorSpaceTransform` `#CST` `#DWG-Intermediate` `#ST2084`
- `#Kodak-2383` `#Film-Look` `#Commercial-Look`
- `#NodeTree` `#PowerGrade` `#RetouchMe`
- `#DaVinciResolve19` `#DaVinciResolve21`