---
name: flux-storyboard-generation
description: Generate a storyboard of Golden Gate Bridge photography using the local Flux image generation pipeline.
category: image
tags: [storyboard, flux, sony, golden-gate, photography, cinematography]
---

# Flux Storyboard Generation

A class-level skill for building an 8‑frame visual storyboard that captures distinct shooting conditions around the Golden Gate Bridge using a Sony A6700 with specified lenses. It orchestrates prompt templating, Flux image synthesis, metadata annotation, and HTML preview generation for client presentation or internal review.

## Overview
- **Purpose**: Create a cohesive 8‑frame storyboard showing different GG Bridge vantage points, each annotated with lens, location, time of day, and technical specs.
- **Output**: PNG sequence under `~/Pictures/Flux_Generations/GG_Bridge_Storyboard_A6700/` plus a self‑contained `storyboard.html` preview.
- **Workflow**: Prompt template → Flux generation → metadata sidecar → HTML assembly.

## Core Steps
1. **Prompt Template Creation**
   - Define eight templates covering:
     - Establishing wide shot (16mm)
     - Medium portrait (75mm f/1.2)
     - Action sequence (28‑75mm)
     - Intimate detail (75mm f/1.2)
     - Environmental panorama (16mm)
     - Silhouette at sunset (28‑75mm)
     - Macro insert (75mm f/1.2)
     - Blue hour cityscape (28‑75mm)
   - Embed tags: `Sony A6700`, `Kodak 2383`, `S-Log3`, `film grain`, lens spec, location, time.

2. **Image Synthesis**
   - Run `generate_flux` for each template:
     - `project='GG_Bridge_Storyboard_A6700'`
     - `steps=4`
     - Appropriate `width`/`height` (1024×576 or 1024×1024)
     - Capture returned output path.

3. **Metadata Annotation**
   - Create JSON sidecar per frame with:
     - `frame_number`, `title`, `lens`, `location`, `aspect`, `prompt_snippet`.
   - Store alongside PNG.

4. **HTML Storyboard Generation**
   - Execute `scripts/generate-storyboard-html.sh`:
     - Scans project folder.
     - Builds responsive grid with hover specs.
     - Outputs `storyboard.html`.

## Configuration
| Parameter | Value |
|-----------|-------|
| **Base folder** | `~/Pictures/Flux_Generations/` |
| **Project name** | `GG_Bridge_Storyboard_A6700` |
| **Lens mappings** | 16mm → Sigma 16mm f/2.8 (24mm equiv) <br> 24mm → Sigma 16mm f/2.8 (24mm equiv) <br> 35mm → Tamron 28‑75mm f/2.8 @ 35mm (52.5mm equiv) <br> 50mm → Tamron 28‑75mm f/2.8 @ 50mm (75mm equiv) <br> 75mm → Tamron 28‑75mm f/2.8 @ 75mm (112.5mm equiv) <br> 112.5mm → 75mm f/1.2 (112.5mm equiv) |
| **Aspect ratios** | 16:9 (wide), 1:1 (portrait/detail) |
| **File naming** | `{frame_number}_{slug}__{camera}__{lens}.png` |

## Pitfalls & Mitigations
- **Wrong aspect ratio** → Verify width/height before generation.
- **Prompt term overlap** → Keep phrasing distinct; avoid ambiguous adjectives.
- **Missing lens tag** → Include `Lens:` label; pipeline strips unknown tags.
- **Missing JSON fields** → Ensure `lens`, `location`, `aspect` present.
- **Ollama port conflict** → Only one `ollama serve` process; kill stray instances if `listen tcp 127.0.0.1:11434: bind: address already in use`.

## Dependencies
- `flux_wrapper.py` (local Flux MCP server)
- `generate_flux` function (exposed via `flux_wrapper.py`)
- `scripts/generate-storyboard-html.sh`

## Quick‑Start
```bash
cd "$HOME/TamaZila\\ Obsidian\\ Vault/Hermes\\ Agent/Hermes\\ Image\\ Generates"
python3 -c "
import sys, os
sys.path.append('.')
from flux_wrapper import generate_flux

shots = [
  ('01_Establishing_Wide', 'Establishing — Marshall's Beach', 'Sigma 16mm f/2.8 (24mm equiv)', 1024, 576),
  ('02_Portrait', 'Portrait — Battery Spencer', '75mm f/1.2 (112.5mm equiv)', 1024, 1024),
  ('03_Action', 'Action — Crissy Field', 'Tamron 28-75mm @ 50mm (75mm equiv)', 1024, 576),
  ('04_Detail', 'Detail — Fort Point', '75mm f/1.2 (112.5mm equiv)', 1024, 1024),
  ('05_Environmental', 'Environmental — Hawk Hill', 'Sigma 16mm f/2.8 (24mm equiv)', 1024, 576),
  ('06_Silhouette', 'Silhouette — Baker Beach', 'Tamron 28-75mm @ 35mm (52.5mm equiv)', 1024, 576),
  ('07_Macro', 'Macro Insert — Cable', '75mm f/1.2 (112.5mm equiv)', 1024, 1024),
  ('08_BlueHour', 'Blue Hour — Crissy Field', 'Tamron 28-75mm @ 75mm (112.5mm equiv)', 1024, 576),
]

for slug, title, lens, w, h in shots:
    prompt = f\"{title}, {lens}, Kodak 2383 film emulation, S-Log3 graded, film grain, 8K detail\"
    generate_flux(prompt=prompt, project='GG_Bridge_Storyboard_A6700', width=w, height=h, steps=4)
"
```

[Skill created at `~/.hermes/skills/flux-storyboard-generation` with YAML frontmatter, `references/`, `scripts/` ready for future updates.]