---
name: ai-assistant-integration
description: "Connect AI assistants to DaVinci Resolve."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, AI, Claude, ChatGPT, Codex, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# DaVinci Resolve AI Assistant Integration

## When to Use

Use when you want to connect AI assistants to control DaVinci Resolve via natural language. New in DaVinci Resolve Studio 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 0:27-1:23
- **Resolve Page:** All (cross-page)

## Setup
1. Open DaVinci Resolve Studio 21.1+
2. File → Setup AI Assistants
3. Wait for confirmation
4. Connect Claude, Claude Code, or ChatGPT Codex
5. Use AI chat interface to control Resolve

## Verified Prompts (from video)
- "Create a 3-minute highlight edit from media pool clip [name]"
- "Remove all edits shorter than 1 second on current timeline"
- "Render H.265 proxy for review at 1080p"
- "Analyze project for color space consistency"
- "Organize media pool by camera type and date"
- "Batch render all timelines in 'Deliver' folder"
- "Change project settings to 4K DCI 24fps"
- "Apply Kodak 2383 LUT to all clips on timeline 1"

## Supported Operations
| Category | Examples |
|----------|----------|
| Editing | Create edits, trim, ripple delete, reorganize |
| Color | Apply grades, LUTs, match shots, balance |
| Media | Organize, relink, proxy, archive |
| Render | Batch render, preset selection, delivery |
| Project | Settings, timelines, bins, markers |
| Fusion | Add tools, connect nodes, animate |
| Fairlight | Mix, effects, automation |

## Requirements
- DaVinci Resolve **Studio** (not free version)
- Internet connection for AI API
- AI assistant account (Claude/ChatGPT/Codex)
- macOS/Windows/Linux

## Tips
- Be specific: clip names, timeline numbers, settings values
- Chain commands: "Then render H.264 for review"
- Use "undo" if AI makes unwanted changes
- Test on duplicate project first

## Cross-References
- **Related Skills:** `davinci-scripting-v21`, `batch-render-automation`
- **Tags:** `ai-assistant`, `claude`, `chatgpt`, `codex`, `automation`, `v21.1`
- **Collection:** `ai-workflows`