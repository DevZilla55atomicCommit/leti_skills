---
name: multitext-align-layers
description: "Align text layers with Multitext Align To Selection."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Edit, Multitext, Titles, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Multitext Layer-to-Layer Alignment

## When to Use

Use when you need to precisely reposition multiple text layers relative to each other for pixel-perfect placement. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 10:02-10:19
- **Resolve Page:** Edit

## Tool Location
Edit page → Multitext Title → Layout tab → Align To → Selection

## Workflow
1. Add Multitext Title to timeline
2. Open Inspector → Layout tab
3. Set "Align To" dropdown to "Selection"
4. Select multiple text layers (Cmd/Ctrl+click)
5. Use Align buttons: Left, Center, Right, Top, Middle, Bottom
6. Layers align relative to each other

## Alignment Options
| Button | Action |
|--------|--------|
| Align Left | Left edges match |
| Align Center | Horizontal centers match |
| Align Right | Right edges match |
| Align Top | Top edges match |
| Align Middle | Vertical centers match |
| Align Bottom | Bottom edges match |
| Distribute Horizontal | Equal horizontal spacing |
| Distribute Vertical | Equal vertical spacing |

## Use Cases
- Lower thirds with multiple text lines
- Credit rolls with aligned names/roles
- Kinetic typography layouts
- Multi-language subtitle alignment
- Logo + tagline positioning

## Tips
- Works with both text box and free text layers
- Combine with box-relative alignment for complex layouts
- Use Distribute for even spacing
- Group layers for persistent alignment

## Cross-References
- **Related Skills:** `multitext-box-alignment`, `title-design-basics`
- **Tags:** `multitext`, `titles`, `alignment`, `edit-page`, `v21.1`
- **Collection:** `title-tools`