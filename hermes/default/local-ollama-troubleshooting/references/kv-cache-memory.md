# KV-Cache Memory Math (9B-class GQA on 16GB Apple Silicon)

Formula (K + V stored): `KV_bytes = 2 × layers × kv_heads × head_dim × tokens × bytes_per_elem` (fp16 = 2B, q8_0 = 1B, q4_0 = 0.5B).

9B-class example (32 layers, 4 KV heads, 256 head-dim):

| Context | fp16 | q8_0 | q4_0 |
|---|---|---|---|
| 32k | 4.3GB | 2.15GB | 1.1GB |
| 64k | 8.6GB | 4.3GB | 2.15GB |
| 98k | 12.5GB | 6.25GB | 3.1GB |

Rules:
- Default to `OLLAMA_KV_CACHE_TYPE=q8_0` (halves KV, negligible quality loss, no throughput penalty); q4_0 only past 64k single-session need.
- Total footprint = weights (9B Q4 ≈ 6–9GB by quant) + KV above + ~2GB OS reserve; recompute before raising any `num_ctx`.
- Server knobs via daemon env (needs app restart to activate, per parent skill): `OLLAMA_KEEP_ALIVE=300` (kills cold-reload stalls), `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_PARALLEL=2` (two slots share the budget; 1 for a single ultra-long session).
- Watch `memory_pressure`; sustained swap during inference means the KV budget exceeds RAM — lower ctx or raise compression, never push through.
