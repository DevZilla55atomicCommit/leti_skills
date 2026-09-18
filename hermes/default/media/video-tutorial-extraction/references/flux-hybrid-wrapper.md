# Flux Hybrid Wrapper — MCP + Python Script Integration

## Overview

Created a dual-purpose Flux image generation wrapper (`flux_wrapper.py`) that serves both:
1. **Python script import** — Direct use in automation scripts
2. **MCP server** — Hermes Agent integration for chat-based generation

## File Location

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Image Generates/flux_wrapper.py
```

## Architecture

```python
# Core generation logic (shared)
def _generate(prompt, width=512, height=512, steps=4, project=None, ...):
    # Ollama API call → base64 decode → save PNG + JSON metadata
    return filepath

# Public API for scripts
def generate_flux(prompt, **kwargs): ...

# MCP tool for Hermes
@mcp.tool()
def generate_image(prompt, width=512, height=512, steps=4, project=None, ...): ...

# MCP tool for browsing
@mcp.tool()
def list_recent(project=None, limit=10): ...

# MCP tool for metadata
@mcp.tool()
def get_image_info(filepath): ...

if __name__ == "__main__":
    mcp.run()  # Start MCP server for Hermes
```

## Usage Modes

### 1. Python Script Import
```python
from flux_wrapper import generate_flux, batch_generate

# Single
path = generate_flux("Kodak 2383 portrait, Sony A7IV S-Log3", project="Commercial_003", width=1024)

# Batch (storyboard)
paths = batch_generate([
    "INT. COFFEE SHOP - DAY wide 16:9",
    "Close-up Spy A 85mm",
    "Close-up Spy B 85mm"
], project="Storyboard_Commercial_003", width=768, height=432)
```

### 2. MCP Server for Hermes
```bash
cd /Users/alfredkamisese/TamaZila\ Obsidian\ Vault/Hermes\ Agent/Hermes\ Image\ Generates
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python flux_wrapper.py
```

Then in Hermes chat: *"Maddie, generate a Kodak 2383 test frame for project Commercial_003"*

### 3. Direct CLI
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python -c "
from flux_wrapper import generate_flux
generate_flux('test prompt', project='MyProject')
"
```

## Key Features

| Feature | Implementation |
|---------|----------------|
| **Project-based organization** | `~/Pictures/Flux_Generations/{project}/` or date-based |
| **Auto-naming** | `{timestamp}_{sanitized_prompt}.png` |
| **Metadata sidecars** | Matching `.json` with prompt, settings, timestamp, project |
| **Flexible params** | width, height, steps, negative_prompt, seed, project |
| **MCP tools** | generate_image, list_recent, get_image_info |
| **Batch generation** | Sequential with project grouping |

## Tested Configuration

- **Model:** `x/flux2-klein:4b` (5.7GB, downloaded via Ollama)
- **Ollama URL:** `http://localhost:11434`
- **Python:** Hermes venv (`/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python`)
- **Default:** 512x512, 4 steps (Flux-Klein fast path)
- **Output:** `~/Pictures/Flux_Generations/`

## Color Grading Prompt Examples

```python
# Kodak 2383 + S-Log3
generate_flux(
    "cinematic portrait, Sony A7IV S-Log3, Kodak 2383 film emulation, golden hour, 85mm f/1.4",
    project="Commercial_003"
)

# Storyboard frame
generate_flux(
    "storyboard frame: INT. COFFEE SHOP - DAY, two spies tense conversation, wide shot 16:9, cinematic lighting, S-Log3",
    project="Storyboard_Commercial_003",
    width=768, height=432
)

# Negative prompt
generate_flux(
    "portrait, 85mm, Kodak Portra 400, natural skin tones",
    project="Portrait_Test",
    negative_prompt="blurry, distorted, cartoon, painting, low quality, ugly, deformed",
    steps=8
)
```

## Integration with Video Tutorial Extraction

After extracting color grading tutorials from YouTube (using this skill), use the extracted parameters (CST settings, node structures, film emulation types) to build Flux prompts for:
- Previsualization / mood boards
- Storyboard frames matching tutorial looks
- Film emulation reference frames (Kodak 2383 D55, Fuji, etc.)
- Skin tone test frames with different film stocks

## Running the MCP Server

```bash
cd /Users/alfredkamisese/TamaZila\ Obsidian\ Vault/Hermes\ Agent/Hermes\ Image\ Generates
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python flux_wrapper.py
```

Keep running in background; Hermes will call tools via MCP protocol.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `requests` import error | Use Hermes venv Python (3.11), not system Python (3.9) |
| Model not found | `ollama pull x/flux2-klein:4b` |
| Timeout | Increase `REQUEST_TIMEOUT` (default 180s) |
| MCP not connecting | Ensure Hermes config has MCP server pointing to this script |