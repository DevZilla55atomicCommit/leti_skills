# Model Capability Matrix — Current Session

*Last updated: 2026-08-19*
*Hardware: Mac Mini M4 (16GB RAM, 256GB SSD) + MacBook Pro*
*Providers: Ollama (local), NVIDIA Cloud, Custom Cloud*

---

## Ollama Local Models

| Model | Size | Tool Calling | Context | Speed (tok/s) | RAM | Best For |
|-------|------|--------------|---------|---------------|-----|----------|
| qwen3.5:4b | 3.4 GB | ✅ | 32K | ~40-50 | ~4 GB | Fast local edits, quick grading, first-pass code |
| llava:7b | 4.7 GB | ❌ | 4K | ~20-30 | ~5 GB | Vision: frame analysis, storyboard review, UI screenshots |
| qwen3.5-32k:latest | 6.6 GB | ✅ | 32K | ~25-35 | ~7 GB | Long-context code review, docs analysis |
| qwen3.5-128k:latest | 6.6 GB | ✅ | 128K | ~20-30 | ~7 GB | Very long context (full codebases, large specs) |
| gemma4:12b | 7.6 GB | ✅ | 8K | ~20-30 | ~8 GB | Balanced general-purpose, good reasoning |
| nomic-embed-text:latest | 274 MB | ❌ | 8K | N/A | ~300 MB | Embeddings for RAG, not chat |

---

## Cloud Models

| Model | Provider | Tool Calling | Context | Speed | Cost | Best For |
|-------|----------|--------------|---------|-------|------|----------|
| nemotron-3-ultra:cloud | NVIDIA | ✅ | Large | Medium | Cloud | Architecture, creative direction, complex analysis, multi-step reasoning |
| gpt-oss:120b-cloud | Custom Cloud | ✅ | Very Large | Medium | Cloud | Code generation, long-context reasoning, refactoring large files |

---

## Routing Decisions (This Session)

| Task Type | Primary Model | Fallback | Rationale |
|-----------|---------------|----------|-----------|
| DaVinci grading (simple/quick) | qwen3.5:4b | nemotron-3-ultra:cloud | Fast local iteration for CDL values, node ops |
| DaVinci grading (complex/creative) | nemotron-3-ultra:cloud | gpt-oss:120b-cloud | Creative look design, shot matching, client briefs |
| Vision/frame analysis | llava:7b | nemotron-3-ultra:cloud (if multimodal) | Only local vision model available |
| Web dev / Next.js / React | nemotron-3-ultra:cloud | gpt-oss:120b-cloud | Architecture, type safety, complex components |
| Code review / long context | qwen3.5-32k:latest | gpt-oss:120b-cloud | 32K context handles full PRs |
| Creative direction / storyboards | nemotron-3-ultra:cloud | gpt-oss:120b-cloud | Artistic judgment, visual reasoning |
| Forex analysis | nemotron-3-ultra:cloud | gpt-oss:120b-cloud | Macro + technical synthesis, structured output |
| Terminal automation / scripts | qwen3.5:4b | nemotron-3-ultra:cloud | Fast, tool-capable, low latency |
| Skill authoring / docs | nemotron-3-ultra:cloud | qwen3.5:4b | Structured writing, conventions knowledge |

---

## Notes

- **No MLX models currently configured** — Phase 2 when `mlx-local` provider is uncommented in config.yaml
- **Vision gap**: Only llava:7b for vision; 4K context limits multi-frame analysis. Consider qwen-vl or gpt-4v via cloud for complex storyboards.
- **Context gap**: 128K model (qwen3.5-128k) available but slower; use for full-codebase tasks only.
- **Speed priority**: qwen3.5:4b is the workhorse for high-frequency, low-complexity tasks.
- **Reasoning priority**: nemotron-3-ultra:cloud for anything requiring judgment, synthesis, or creative decisions.