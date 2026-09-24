---
name: comfyui-extended
description: Extends bundled comfyui skill with hardware-verdict interpretation and install guidance.
version: 1.0
tags:
  - comfyui
  - hardware-verdict
  - image-generation
  - stable-diffusion
  - flux
  - sd3
  - wan-video
  - creative
  - generative-ai
  - video-generation
---

# ComfyUI Extended

This skill augments the official `comfyui` skill by adding:

## Hardware Verdict Interpretation
- `ok` → Sufficient GPU or >=32 GB unified memory. Recommended for local install.
- `marginal` → Entry‑level GPU (6‑8 GB VRAM) or 16‑32 GB unified memory. Works for SD 1.5; limits on SDXL/Flux.
- `cloud` → No compatible accelerator. Must use Comfy Cloud.

Reference: `{{> references/hardware-verdict-interpretation.md}}`

## Install Guidance Flow
1. **Ask Local vs Cloud** first.
2. If **Local** and verdict is `ok` → run `bash scripts/comfyui_setup.sh --m-series` (or `--nvidia`/`--amd`).
3. If **Local** and verdict is `marginal` → local install possible but expect limits; suggest Comfy Cloud for heavy workloads.
4. If **Local** and verdict is `cloud` → must use Comfy Cloud.

## Linked Reference Files
- `references/hardware-verdict-interpretation.md` — quick lookup of verdict outcomes.
- `scripts/decision_tree.py` — optional helper to auto‑select install path from hardware‑check JSON.

---