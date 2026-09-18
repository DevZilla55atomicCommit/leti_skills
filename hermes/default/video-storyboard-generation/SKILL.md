---
name: video-storyboard-generation
description: Scaffold for video storyboard generation workflow.
category: videography
---

This skill provides a reusable workflow for generating video storyboards using the Hermes Flux pipeline. It includes:

## Core Steps
1. **Prompt Engineering** – Use cinematographic language (shot type, lens, lighting, color grade) and include photography reference cues.
2. **Frame Generation** – Call `generate_flux` for each shot, specifying width/height and steps.
3. **HTML Documentation** – Assemble generated frames into a self‑contained `storyboard.html` with per‑frame metadata.
4. **Reference Integration** – Link photography reference frames stored in the vault for lighting/DOF/grade consistency.

## Files Created
- `video_storyboard.html` – Interactive preview of all frames; press <kbd>Space</kbd> to play, <kbd>←/→</kbd> to navigate, click thumbnails to jump.
- `references/video-storyboard-notes.md` – Session‑specific notes and pitfalls.
- `templates/storyboard.html` – Template used to generate the HTML.
- `scripts/generate_storyboard.sh` – Bash wrapper that calls the Python flux wrapper with supplied prompts and parameters.

## Pitfalls
- **Token Limits**: Prompts exceeding model token limits should be truncated to essential cinematographic descriptors.
- **Missing Reference Links**: Ensure photography reference frames are correctly linked in `references/` to avoid broken cross‑links.
- **Aspect Ratio Mismatch**: Maintain consistent aspect ratio (1920×1080) across all generated frames.
- **HTML Preview Failures**: Verify the generated `storyboard.html` loads; open in browser and use <kbd>Space</kbd> to start playback. If blank, check that image paths are correct.

## Session Notes (2026‑07‑24)
- Confirmed Ollama server running (`ollama serve`) and Flux model `x/flux2-klein:4b` installed (5.7 GB).  
- Generated storyboard frames successfully; HTML preview (`storyboard.html`) loads and plays with controls.  
- Added photography reference frames to `references/` and linked them in prompts.  
- Exported a JSON manifest of the 8‑shot sequence for import into DaVinci/Frame.io.  
- Script `scripts/generate_storyboard.sh` now wraps the flux command with project, prompt, and optional size/step args.

## Example Command
```bash
generate_flux \
  --prompt "Drone pullback sunset, Sony A6700 Sigma 16mm f/2.8, rising from Crissy Field revealing full Golden Gate Bridge illuminated, model small on beach, San Francisco skyline, Kodak 2383, S-Log3" \
  --project "GG_Bridge_Video_Storyboard" \
  --width 1920 --height 1080 --steps 4
```

This skill can be loaded via `/skill video-storyboard-generation` or inspected with `skill_view(name='video-storyboard-generation')"