# Vision Analysis Lessons Learned

## Session History

| Session | Progress | Notes |
|---------|----------|-------|
| 20260728 | 659 pending → processing | Local worker `proc_95f01d68347d` running |
| 20260727 | 665 errors reset → pending | Frame-not-found: 45 left as error |
| 20260727 | 436 complete, 306 timeouts | llama-server instability |
| 20260726 | 235 quality results (DaVinci Core) | Cloud vision_analyze (20 RPM) |

---

## Ollama Cloud API Reality Check (2026-07-28)

**Critical finding**: Ollama Cloud API does NOT provide vision models.

```bash
# Models available on ollama.com/api with API key:
curl -H "Authorization: Bearer $KEY" https://ollama.com/api/tags

# Returns: nemotron-3-ultra, gpt-oss:20b, gpt-oss:120b, kimi-k3, 
#          deepseek-v4-pro/flash, glm-5.1/5.2, minimax-m2.5/2.7/m3,
#          gemma4:31b, qwen3.5:397b, mistral-large-3:675b...

# NO vision models (qwen3-vl, llama3.2-vision, gemma3, etc.)
```

**Conclusion**: Ollama Cloud API is for **text inference only**. Cannot use for vision analysis.

---

## Hardware Constraints Documented (2026-07-28)

**Mac Mini M4 16GB unified memory** — local qwen3-vl:8b Q4_K_M (~9GB) exceeds practical VRAM:
- llama-server spawns, allocates, OOMs/hangs, restarts on new port
- Process churn: 52317 → 53776 → 55618 → 62165 → ...
- 100% failure rate after first few calls

**No local vision model is viable on 16GB M4** for this workload.

---

## Architectural Implication

**Sequential vision_analyze is the only working path.** Accept ~8-10 hours for 2,370 remaining videos and parallelize skill authoring/vault rebuild instead.

*Update these lessons when hardware or provider offerings change.*