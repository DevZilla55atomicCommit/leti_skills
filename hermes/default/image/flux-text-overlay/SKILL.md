---
name: flux-text-overlay
description: Overlay custom text on Flux-generated images to ensure legibility of critical characters like "BBQ".
category: image
tags:
  - text-overlay
  - flux
  - typography
  - typography-workaround
deps:
  - pillow
  - requests
  - numpy
---

## Overview

Diffusion models such as Flux often struggle with precise text rendering, especially characters like "Q", "B", and "G". For professional outputs where exact text is required (e.g., logos, labels), generate a clean background without text using Flux.

## Workflow

1. Generate a clean background image without text using Flux.
2. Use `scripts/text_overlay.py` to overlay the desired text with professional styling.
3. Save the final composition and optionally generate a preview.

## Common Pitfalls

- **Text Rendering Errors**: Characters may appear incorrectly; avoid relying on model text rendering for critical labels.
- **Font Availability**: Use system fonts available at paths like `/System/Library/Fonts/HelveticaNeue.ttc`.
- **Path Handling**: Ensure the working directory is correctly set; use absolute paths to avoid confusion.

## Scripts

- `scripts/text_overlay.py` – Example script to overlay "KAILAHI BBQ" on a background.

## References

- `references/hawaiian-bbq-poster-case.md` – Case study from July 2026 project.