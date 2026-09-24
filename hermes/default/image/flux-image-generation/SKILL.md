---
name: flux-image-generation
description: Local-first Flux image generation pipeline for Hermes Agent
category: image
tags:
  - image-generation
  - flux
  - ollama
  - mcp
  - herm image generates
deps:
  - ollama
  - python3
  - requests
  - Pillow
  - numpy
  - matplotlib
---

# Quickstart

This skill provides a standardized workflow for generating images using the Flask MCP server integrated with Hermes Agent's image generation pipeline. It handles:

- Model launching (Flux-Klein 4-step model)
- Image output management
- Metadata generation
- OOM-safe configuration for 16GB RAM systems

## Integration Points

- Works with Hermes Image Generates project directory: `~/Pictures/Flux_Generations/`
- Output format: PNG + accompanying `.json` metadata file
- Compatible with Hermes Agent's MCP tool integration
- System Python wrapper ensures venv bypass for stable `requests` usage

## Usage

1. Start the MCP server background process:
   ```bash
   python /Users/alfredkamisese/TamaZila\ Obsidian\ Vault/Hermes\ Agent/Hermes\ Image\ Generates/flux_wrapper.py
   ```

2. Generate an image via Hermes Agent chat:
   > "Maddie, generate a [prompt], project: [project_name]"

3. The agent will:
   - Call the `generate_image` MCP tool
   - Save to `~/Pictures/Flux_Generations/[project_name]/`
   - Get JSON metadata alongside the PNG

## Configuration

- **DEFAULT_MODEL**: `x/flux2-klein:4b` (5.7GB, OOM-safe)
- **MAX_IMAGE_DIMENSION**: 1024 (for 16GB systems)
- **DEFAULT_STEPS**: 8 (balances quality/performance)
- **TEMP_DIR**: `~/Pictures/Flux_Generations/`
- **AVAILABLE_MODELS**: `{'flux': 'x/flux2-klein:4b'}`

## Safety

- Never use >1024x1024 dimensions on 16GB systems
- Always validate model availability before generation
- Metadata is saved alongside images for traceability
- Pipeline exits cleanly if OOM detected

## Common Pitfalls

## User Display

After a successful image generation, automatically present the result to the user:

- **Save the output path**: The script writes the image to `~/Pictures/Flux_Generations/[project]/`. Store this path in session memory for future reference.
- **Open in preview**: Use Hermes' built‑in `open_preview` tool to show the PNG in the UI:
  ```python
  from hermes_tools import open_preview
  open_preview(url=f'file://{filepath}')
  ```
- **Inline in chat**: If you want the image to appear directly in the conversation, emit a `MEDIA:` link:
  ```python
  print(f'MEDIA:{filepath}')
  ```

This ensures the user sees the generated poster immediately, confirming the correct prompt was used and providing visual feedback.

1. **Venv ImportError**: When running system Python scripts, ensure venv paths aren't in `sys.path`. Fix: `sys.path = [p for p in sys.path if '.hermes/hermes-agent/venv' not in p]`
2. **Model Not Found**: Verify `x/flux2-klein:4b` exists in Ollama with `ollama list`
3. **OOM Crash**: Reduce dimensions or steps if process dies silently
4. **Permission Errors**: Ensure `~/Pictures/Flux_Generations/` is writable

## Verification

Test with minimal prompt:
```bash
python3 -c "
import requests, base64, json, os
from datetime import datetime
from pathlib import Path
# ... [rest of test code] ...
"
"