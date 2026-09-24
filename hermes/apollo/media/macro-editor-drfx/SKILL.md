---
name: macro-editor-drfx
description: "Load macros from DRFX bundles with Krokodove Macro Editor."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, Macros, DRFX, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Macro Editor DRFX Loading

## When to Use

Use when you need to load macro definitions from DRFX template bundles with automatic single/multi-macro detection. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 8:52-9:02
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Macro Editor

## Features
- Auto-detect single macro vs multiple macros in DRFX bundle
- Selection UI for multi-macro bundles
- Preserve control layouts and customizations
- Direct integration with Fusion flow

## Workflow
1. Open Macro Editor (Fusion page)
2. Click "Load from DRFX"
3. Select .drfx template bundle file
4. Auto-detection identifies macro count
5. Single macro: loads directly
6. Multiple macros: selection dialog appears
7. Choose desired macro(s) to load
8. Macro appears in flow with all controls

## Use Cases
- Template sharing across projects
- Version-controlled macro libraries
- Collaborative macro development
- Quick macro deployment
- Backup/restore macro setups

## Tips
- DRFX bundles include control metadata
- Works with both Fusion and Edit page macros
- Combine with "Save To Template Category" for organization
- Test macros before bundling

## Cross-References
- **Related Skills:** `macro-save-template-category`, `macro-update-selected-tools`, `macro-thumbnail-management`
- **Tags:** `krokodove`, `fusion`, `macros`, `drfx`, `templates`, `v21.1`
- **Collection:** `krokodove-tools`