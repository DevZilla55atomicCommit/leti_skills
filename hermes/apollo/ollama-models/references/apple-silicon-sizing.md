# Apple Silicon Sizing for Ollama Context Variants

Estimate whether a context variant fits before creating it. KV cache dominates at large num_ctx.

## Per-token KV formula (FP16)

```
per_token_bytes = 2 (K+V) * n_layers * n_kv_heads * head_dim * 2 bytes
```

For a ~9B model with 36 layers, 8 KV heads, head_dim 128: ~144 KB/token FP16.

Get the real geometry from `ollama show <tag>` (architecture, parameters, embedding length) and compute with the terminal, never from memory.

## Fit method

1. Read host pressure live: `sysctl hw.memsize`, `vm_stat | head`, `sysctl vm.swapusage`, plus `df -h /` for free disk and `du -sh ~/.ollama/models` for current store weight.
2. Compute per variant: `total = weights_GB + per_token * num_ctx`.
3. Report a table of weights + KV per sibling (32k/48k/96k/128k) with a fits / at-limit / exceeds verdict against physical RAM minus ~3-4GB macOS reserve.
4. Recommend usage tiers: smallest fitting variant as daily default, larger ones as specialty tools for prompts that truly need the window.
5. For large MoE or unfamiliar families, add disk and vendor-floor checks — the download must fit in `df` free space with headroom, the vendor minimum RAM (weights + KV + context) must fit in physical RAM, and the README hardware floor overrules download size when they disagree; a tag that passes download size but fails either check is exceeds, not at-limit.

## q8_0 KV guidance

- `OLLAMA_KV_CACHE_TYPE=q8_0` roughly halves KV bytes with near-lossless recall; it does not touch weights, so reasoning and knowledge are unchanged.
- It is a server-wide flag (`ollama serve` startup), not per-model — every model loaded while the server runs with it uses q8 KV.
- Prefer q8_0 over q4_0 for long-context recall; q4_0 degrades distant-token fidelity noticeably.
- `num_predict` cuts only max output tokens per turn (~2048 tokens ≈ 1500 words / ~80 lines of code); input understanding is untouched, so cut it first when RAM is tight.
