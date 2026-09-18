# Ollama Vision Models — Comparison Notes

## Tested Models (this session)

| Model | Size | RAM | Quality | JSON | Status |
|-------|------|-----|---------|------|--------|
| `llava:7b` | 8.5 GB | ~9 GB | Good | ✅ Valid | **Recommended** |
| `qwen3-vl:8b` | 15 GB | ~16 GB | Better | ✅ Valid | Too large for 16GB |
| `moondream:1.8b` | 1.8 GB | ~2 GB | Poor | ❌ "urn" | Broken |
| `gemma3:4b` | ~4 GB | ~5 GB | Unknown | ? | Pull timed out |
| `bakllava:7b` | ~7 GB | ~8 GB | Unknown | ? | Pull timed out |

## Key Findings

### llava:7b (Recommended)
- Produces valid JSON with the DaVinci schema
- ~10-15 sec/frame (3 frames = ~35-45 sec/video)
- Uses 100% GPU, 8.5 GB RAM
- Fits on 16GB alongside gemma4:12b (7.6 GB) with careful memory management
- Hallucinates some details but structure is reliable

### qwen3-vl:8b
- Better quality but 15 GB RAM — exceeds 16GB limit when combined with text model
- Only viable if text model is unloaded

### moondream:1.8b
- Returns "urn" for all vision prompts — fundamentally broken for this use case
- Do not use

### gemma3:4b / bakllava:7b
- Pulls timed out — untested
- Would be good alternatives if available

## Model Selection Rule for 16GB Mac

```
IF running text model (gemma4:12b = 7.6 GB):
  ONLY llava:7b fits (8.5 GB) → total ~16.1 GB (swaps but works)
  
IF text model unloaded:
  qwen3-vl:8b possible (15 GB)
```

## Pull Commands

```bash
# Recommended
ollama pull llava:7b

# Alternative (if text model not needed)
ollama pull qwen3-vl:8b

# Small but broken
ollama pull moondream:1.8b

# Untested
ollama pull gemma3:4b
ollama pull bakllava:7b
```