---
name: davinci-resolve-version-tracker
description: "Process DaVinci Resolve version videos into vault notes."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Video Analysis, Version Tracking, Color Grading]
    related_skills: [youtube-content]
---

# DaVinci Resolve Version Tracker Skill

## When to Use

Use when a new DaVinci Resolve version announcement video is released (Blackmagic Design YouTube channel). Extracts features, organizes by page/category, creates timestamped catalog, and writes a structured vault note linked to the DaVinci Knowledge Base.

## Workflow

1. **Fetch transcript** using `youtube-content` skill (scripts/fetch_transcript.py)
2. **Parse features** by page: Edit, Cut, Color, Fusion, Fairlight, Deliver, Media, Photo
3. **Categorize** each feature: New Tool, Enhancement, AI Integration, Format Support, Performance, Workflow
4. **Generate vault note** in `Hermes Agent/DaVinci_Knowledge_Base/DaVinci Resolve 21/` (or appropriate version folder)
5. **Cross-reference** with existing skills, techniques, and tags
6. **Update MASTER_MAPPING.md** if new categories emerge

## Output Format

Vault note includes:
- Video metadata (ID, URL, date, duration)
- Executive summary (3-5 sentences)
- Feature catalog table grouped by Resolve page
- Timestamped transcript segments
- AI integration highlights (Claude, ChatGPT, Codex)
- New color spaces / camera support
- Fusion/Krokodove tools added
- Cross-reference links to existing vault techniques
- Suggested tags for tagging system

## Helper Script

```bash
# Fetch transcript with timestamps
uv run python SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps --language en
```

## Vault Integration

- Note location: `Hermes Agent/DaVinci_Knowledge_Base/DaVinci Resolve XX/`
- Naming: `davinci-resolve-XX.X-features-YYYY-MM-DD.md`
- Links to: `skills/`, `tags/`, `collections/`, `analysis/`
- Updates: `MASTER_MAPPING.md` statistics
