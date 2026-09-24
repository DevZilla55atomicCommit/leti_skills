# Hardware Check Verdict Interpretation

- `ok` → Sufficient GPU (>=8 GB VRAM) or >=32 GB unified memory.
  - Recommended: Local install with `--nvidia`, `--amd`, or `--m-series`.
  - Ready for SDXL, Flux, and video pipelines.

- `marginal` → Entry‑level GPU (6–8 GB VRAM) or 16–32 GB unified memory.
  - SD 1.5 works; SDXL tight; Flux/video likely OOM.
  - Local install possible (`--nvidia`/`--m-series`) but expect performance limits.
  - Consider Comfy Cloud for heavier workloads.

- `cloud` → No compatible accelerator (no NVIDIA/AMD/Apple GPU, <6 GB VRAM, <16 GB unified memory).
  - Local install not advised; CPU‑only will be unusably slow.
  - Use Comfy Cloud (hosted on RTX 6000 Pro) or upgrade hardware.