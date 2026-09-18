# TurboQuant-MLX Testing Notes (This Session + Updated Recommendations)

## Context
User has M2 MacBook Pro 16GB. Tested TurboQuant-MLX models via native MLX runtime (not Ollama).

## Models Tested

| Model | Quantization | Disk Size | RAM (Peak) | Speed | Verdict |
|-------|-------------|-----------|------------|-------|---------|
| Qwen3-235B-A22B | tq3a-tqTe (3-bit attn + 1.58-bit ternary experts) | ~53 GB | ~10-11 GB (streaming) | ~0.05 tok/s | **Too slow** — disk-bound on M2 SSD |
| Nemotron-3-Nano-4B | tq3 (3-bit) | ~2.2 GB | ~4.3 GB | ~75 tok/s | **Excellent** — fast, fits easily |
| Qwen3.6-35B-A3B | tq3-g32 | ~16 GB | ~9-10 GB (streaming) | ~4.5 tok/s | Usable but slow |
| Qwen3.6-27B | tq3-g32 | ~13 GB | ~17.5 GB (resident) | ~14 tok/s | Needs 48GB+; OOM on 16GB |

## Key Findings for 16GB M2

1. **Streaming MoE (235B, 35B) works but is disk-bound** — M2 SSD ~3 GB/s sequential, random 4K ~50-100 MB/s. Expert paging kills throughput.
2. **Resident models >16 GB peak RAM need `iogpu.wired_limit_mb` raised** — Default ~8 GB cap. `sudo sysctl iogpu.wired_limit_mb=12288` needed for 27B.
3. **TurboQuant 3-bit quality is excellent** — Near-BF16 perplexity at 3-bit.
4. **Nemotron-3-Nano-4B is the sweet spot** — 75 tok/s, 4.3 GB, strong reasoning for size.
5. **User chose Ollama as daily driver** — Standard GGUF, OpenAI-compatible API, huge model zoo.

## Ollama Alternative (Chosen by User)

```bash
# Fast, standard GGUF, huge model zoo
ollama pull nemotron-3-nano:4b   # ~2.8 GB, ~30-50 tok/s
ollama pull qwen2.5:14b          # ~9 GB, ~30 tok/s, stronger coding
ollama pull qwen2.5:32b          # ~20 GB, ~15 tok/s, SOTA coding (tight on 16GB)
```

## TTS Provider Decision (This Session)

User evaluated ElevenLabs vs Edge TTS for Hermes voice output:

| Factor | ElevenLabs | Edge TTS |
|--------|-----------|----------|
| **Voices** | ~100+ library + custom | 323 fixed neural voices |
| **British English** | Many (cloned/custom) | 5 neural (en-GB) |
| **Quality** | Higher (commercial) | Very good (neural) |
| **Cost** | 10k chars/mo free | **Free, unlimited** |
| **API key** | Required | None |
| **Latency** | Low (cloud) | Low (cloud) |

**Recommendation**: For this user's use case (British female voice, moderate usage), ElevenLabs free tier is sufficient (~20-30 short responses/month). Switch to Edge TTS if usage exceeds free tier.

Current config: ElevenLabs with "British Lady" voice (voice_id: GbqQP1rsVFijH3q1FXHV), model: eleven_multilingual_v2.

## Final Recommendation for This User

- **Daily driver LLM**: Ollama `nemotron-3-nano:4b` or `qwen2.5:14b` — standard GGUF, OpenAI-compatible API, huge ecosystem
- **Experiment only**: TurboQuant-MLX streaming MoE — impressive tech demo, not practical daily driver on 16GB M2
- **Native NVIDIA API**: Use Hermes native provider for Nemotron-3-Ultra/Nemotron-3-Super via NVIDIA NIM (cloud), not local
- **TTS**: ElevenLabs free tier with British Lady voice; fallback to Edge TTS if character limit hit