---
name: local-image-generation
description: Use when generating images locally with Flux on this Mac.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [image-generation, flux, mflux, poster, offline-first]
    related_skills: [claude-design]
---

# Local Image Generation (Flux on Apple Silicon)

Offline-first image pipeline for this Mac (M4, 16 GB RAM). Validated end to end: real PNGs generated, inspected, and composed into posters.

## Route selection

Two routes exist. Probe before committing, never assume:

1. **mflux (working route)** — `mflux-generate-flux2`, runs Flux weights natively via MLX, no Ollama involved.
2. **Ollama-native (unverified on this box)** — the `ollama_flux` MCP tool and `ollama run` against `x/flux2-klein`.

Probe model-class support with a cheap read before any multi-GB pull: `ollama show <model>` costs nothing and reveals whether the binary accepts that model class at all. Pulling first and discovering the refusal second wastes gigabytes and the whole session's momentum.

## Validated mflux workflow

```bash
uv tool install mflux   # one-time, user-scoped
mkdir -p ~/Pictures/Flux_Generations/<project>/
mflux-generate-flux2 --model flux2-klein-4b --low-ram \
  --width 1024 --height <768|1024> \
  --metadata --output ~/Pictures/Flux_Generations/<project>/<name>.png \
  --prompt "<perfected prompt>"
```

Standing constraints for 16 GB RAM:

- Neither dimension above 1024. Landscape scenes (1024x768) suit left-to-right staging; square (1024x1024) suits hero subjects.
- Always pass `--low-ram` and `--metadata` (the JSON receipt records model, seed, steps, time).
- First run downloads ~15 GB of Hugging Face weights (`black-forest-labs/FLUX.2-klein-4B`); inference alone runs ~2.5 min. Peak memory can exceed physical RAM (~18 GB observed) — it survives on swap, so close nothing, but do not stack concurrent generations.
- Run generations in background with completion notify; watch progress via process liveness plus output-file appearance (HF cache growth is the download signal, CPU hold is the inference signal).

## Sign-off gate

A generation costs minutes plus user attention. Always show the perfected prompt (and headline, for posters) for approval before executing. Lock a seed only after a liked version exists; leave seed random for first attempts.

## Flux prompt craft (klein, few-step distilled models)

- One flowing descriptive paragraph, subject and action front-loaded; ~100-150 words.
- Face budget: at most ~5 distinct faces per frame — beyond that the distilled steps melt features. Reduce headcount before generating, not after.
- On-image text: short fragments only (scoreboards, signs). Full sentences mangle. Set real typography afterward (see Scene-then-type).
- Describe real people instead of naming them ("muscular smiling Maori captain" over the actual name) — likeness output is approximate either way, description avoids uncanny-valley framing.
- State camera, light, and finish explicitly: "cinematic photorealistic wide shot", "golden-hour rim light", "shallow depth of field".

## Scene-then-type poster assembly

Generate the scene clean, then compose the poster in HTML (see `claude-design` for the artifact process):

- Hero `<img>` references the generated PNG by relative path in the same project folder.
- Titles, kickers, and footers live in HTML type, never in pixels.
- Keep a gradient wash over the image so type stays legible regardless of scene brightness.
- Record the generation receipt (model, dims, steps, seed, seconds) in a caption line and keep the `.metadata.json` beside the PNG.

## Output layout

`~/Pictures/Flux_Generations/<project>/` holds `<name>.png`, `<name>.metadata.json`, and `poster.html` together so the folder is a self-contained artifact.

## Pitfalls

- Pulling a model before probing class support burns gigabytes on a route that may be closed — `ollama show` first, `ollama pull` second.
- Raising dimensions past 1024 on 16 GB RAM trades swap pressure for zero visible gain at poster sizes — cap dims, not ambition.
- Baking sentences into the image prompt guarantees re-renders — keep pixels text-free and set type in HTML.
- Fixing a seed on the first attempt burns the exploration lottery — random seed first, lock seed on the keeper.
