---
title: Benchmark Visualization for Local LLMs
description: Interactive HTML benchmark charts for local LLMs on macOS.
trigger: Use when generating interactive benchmark charts for coding models on macOS (M1/M2) with 16GB RAM.
role: visual-analyst
name: benchmark-visualization
---

# Purpose
Create interactive HTML benchmark visualizations that compare:
- RAM usage
- Tokens/second speed
- Coding benchmarks (HumanEval, MBPP, LiveCodeBench, MultiPL‑E)
- Memory pressure
- Overall weighted score

The output is a self‑contained `benchmark.html` file that opens in the Hermes preview pane or browser. It includes four views:
1. **Table** – sortable rows with expanded detail sections
2. **Radar** – multi‑dimensional tradeoff view
3. **Bar Charts** – breakdowns of coding scores, memory vs speed, etc.
4. **Scatter Plot** – RAM vs Speed vs Coding score (bubble size)

# Workflow
1. **Collect data** – Pull model info from GitHub releases, HF model cards, and benchmark leaderboards.
2. **Populate `models` array** – Each entry contains `name`, `engine`, `quant`, `ram`, `speed`, `humanEval`, `mbpp`, `liveCodeBench`, `multiPL_E`, `memoryPressure`, `verdict`.
3. **Render the chart** – Use the embedded Chart.js + Tailwind CSS template.
4. **Open preview** – `open_preview` with `file:///…/benchmark.html`.

# Core Data Model (example entry)
```json
{
  "id": "qwen25-coder-7b-mlx-3bit",
  "name": "Qwen2.5‑Coder‑7B",
  "engine": "MLX",
  "quant": "3‑bit",
  "ram": 3.5,
  "speed": 38,
  "humanEval": 78.7,
  "mbpp": 72.4,
  "liveCodeBench": 38.5,
  "multiPL_E": 68.2,
  "memoryPressure": 22,
  "verdict": "Best Balance",
  "details": {
    "pros": [...],
    "cons": [...],
    "bestFor": "...",
    "notes": "..."
  }
}
```

# Pitfalls & Fixes
- **Pitfall:** Over‑estimating speed on CPU‑only runs.  
  **Fix:** Use Metal‑accelerated backends (MLX, Ollama Metal) and measure with `timeit` for warm‑up cycles.
- **Pitfall:** Memory pressure mis‑calculated when KV cache isn’t accounted for.  
  **Fix:** Add KV cache estimate (`~0.5 GB per 2K context`) to RAM total.
- **Pitfall:** Benchmark data out‑of‑date.  
  **Fix:** Pull the latest release notes before generating; cache the JSON payload locally.

# References
- **Model Cards**  
  - [Qwen2.5‑Coder Technical Report](https://github.com/QwenLM/Qwen2.5-Coder)  
  - [Nemotron‑3‑Nano Model Card](https://huggingface.co/nvidia/Nemotron-3-Nano-4B)  
  - [DeepSeek‑Coder‑V2 Paper](https://github.com/deepseek-ai/DeepSeek-Coder-V2)

- **Benchmarks**  
  - [BigCode Models Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard)  
  - [MLX Benchmarks](https://github.com/ml-explore/mlx-examples/tree/main/llms)

- **Visualization Library**  
  - Chart.js (v4) – `type: radar`, `type: bar`, `type: scatter`, `type: bubble`  
  - TailwindCSS – utility classes used for layout and theming  

# Related Skills
- `ecc-installation` – ensures the environment is set up for local model execution.  
- `hermes-desktop-plugins` – for opening the generated HTML in the preview pane.  
- `skill-scout` – for locating existing benchmark‑related skills.

# Auto‑Update Hook
Add this skill to your cron job `benchmark-update` to refresh data nightly.