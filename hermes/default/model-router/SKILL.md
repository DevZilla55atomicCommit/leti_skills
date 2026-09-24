---
name: model-router
description: Route tasks to Ollama (tools) or MLX (fast) based on intent
category: automation
tags: [routing, ollama, mlx, model-selection]
---

# Model Router Skill

## Purpose
Automatically route coding tasks to the optimal local model:
- **Ollama `qwen2.5-coder:7b`** — tasks requiring tool calling (git, filesystem, GitHub, lint, test)
- **MLX `qwen-coder-7b-3bit`** — fast generation tasks (code writing, refactoring, creative coding, data scripts)

## Routing Rules

| Task Type | Provider | Model | Reason |
|-----------|----------|-------|--------|
| Git operations (commit, diff, push, log) | ollama-launch | qwen2.5-coder:7b | Native tool calling |
| Filesystem read/write/list | ollama-launch | qwen2.5-coder:7b | Native tool calling |
| GitHub PR/issue actions | ollama-launch | qwen2.5-coder:7b | Native tool calling |
| Lint/typecheck/test runs | ollama-launch | qwen2.5-coder:7b | Native tool calling |
| Code generation/edits | mlx-local | qwen-coder-7b-3bit | 38 tok/s, 3.5 GB RAM |
| Refactoring | mlx-local | qwen-coder-7b-3bit | Large context, fast |
| Creative coding (p5.js, Three.js) | mlx-local | qwen-coder-7b-3bit | Speed + quality |
| Data analysis scripts | mlx-local | qwen-coder-7b-3bit | Fast iteration |
| Architecture questions | ollama-launch | qwen2.5-coder:7b | Tool access for exploration |
| Documentation writing | mlx-local | qwen-coder-7b-3bit | Fast, good prose |

## Usage in Hermes

### Explicit Routing
```bash
# Force Ollama (tools)
@model-router:tools "Create a git commit with the changes"

# Force MLX (fast)
@model-router:fast "Write a p5.js particle system"
```

### Automatic via Kanban Labels
| Label | Routes To |
|-------|-----------|
| `tools` | ollama-launch (qwen2.5-coder:7b) |
| `fast` | mlx-local (qwen-coder-7b-3bit) |
| `auto` | Kanban decides via this skill |

## Implementation Notes

The router works by:
1. Detecting task intent from prompt/label
2. Selecting appropriate provider in Hermes config
3. Setting `model.provider` and `model.default` for the request

When MLX model is ready, uncomment the `mlx-local` provider in `~/.hermes/config.yaml` and the router will automatically use it for `fast` tasks.

## Future: MLX Setup (Phase 2)

When ready to add MLX:
```bash
# 1. Build 3-bit model
pip install mlx-lm
python -m mlx_lm.convert \
  --hf-path Qwen/Qwen2.5-Coder-7B \
  --mlx-path ~/.hermes/models/qwen-coder-7b-3bit \
  -q 3bit

# 2. Start MLX server
python -m mlx_lm.server --model ~/.hermes/models/qwen-coder-7b-3bit --port 8080

# 3. Uncomment mlx-local provider in config.yaml
# 4. Test: @model-router:fast "Hello world"
```