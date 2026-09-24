# Hybrid Text + Image Reference Strategy

For vaults with large media files (GIFs, videos, large images) where vision API calls are rate-limited or infeasible, use this hybrid approach:

## Strategy

1. **Extract all text/markdown/code** with full semantic extraction (LLM)
2. **Skip ALL image files from vision queue** using `--ignore` flags
3. **Images become reference nodes** in the graph — linked to their parent `.md` files via filename
4. **No vision API calls** — avoids rate limits, completes in ~30 min vs 100+ hours

## Command

```bash
graphify "/Volumes/PNY128GBLED/TamaZila Obsidian Vault" \
  --backend openai \
  --model "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning" \
  --obsidian \
  --obsidian-dir "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Graphify-FullVault" \
  --ignore "*.gif" --ignore "*.jpg" --ignore "*.jpeg" --ignore "*.png" --ignore "*.webp" \
  --ignore ".vault-organizer-backups/**"  # Skip Syncthing conflict copies
```

## What You Get

| Content | In Graph? | Extraction |
|---------|-----------|------------|
| DaVinci KB `.md` files | ✅ Full | Semantic LLM |
| Forex Center `.md`/`.py` | ✅ Full | Semantic LLM |
| Hermes Agent code/docs | ✅ Full | AST + Semantic |
| Photography notes | ✅ Full | Semantic LLM |
| Code symbols (Python, JS, etc.) | ✅ Full | AST + Semantic |
| PDFs | ✅ Full | Text + LLM |
| **Image files (GIF/JPG/PNG)** | ✅ Reference nodes only | **None** |
| Vision analysis | ❌ | N/A |

## Graph Structure

```
[DaVinci Technique: "CST Round-trip for Sony S-Log3"]
       │
       ├── references → [instagram-reel-C0Ck90GN.md]
       │                    │
       │                    └── contains → [C0Ck90GN.gif] (reference node)
       │
       └── semantically_similar_to → [Apple Log 2 Workflow]
```

- Image nodes have `source_file` metadata and `type: "image"`
- Clickable in Obsidian → opens the file
- No AI-generated description/analysis

## Time Comparison

| Approach | Vision API Calls | Est. Time |
|----------|------------------|-----------|
| Full vision (Nemotron Nano Omni) | 11,576 chunks | **100+ hours** (NVIDIA API limited)
| **Hybrid (text + refs)** | **0** | **~20–30 minutes** |

## When to Use Full Vision Instead

- Small image corpus (<500 images, all <5 MB)
- Need visual descriptions ("diagram shows X", "frame depicts Y")
- Cross-modal queries ("code that generates this chart")

## TamaZila Vault Specific

The `.vault-organizer-backups/` folder contains **180K+ Syncthing conflict-copy GIFs** (10–100 MB each) — NOT curated content. Always exclude:

```bash
--ignore ".vault-organizer-backups/**"
```

Real DaVinci KB images are in main folders. If needed, extract key frames as <5 MB JPGs and index separately.

## Rate Limit Reality (NVIDIA Cloud API)

```
Free tier limits:
- 16 concurrent requests per account
- 12 images max per prompt (VLLM validation)
- Token limits per minute

Result: ~0.03 chunks/sec effective rate for 204K images = ~100 hours
```

**Local NIM removes all limits** — deploy `nvcr.io/nim/meta/llama-3.2-90b-vision-instruct` for unlimited vision throughput.

## Related

- `references/nvidia-nim-setup.md` — model selection, local NIM deployment
- `references/troubleshooting.md` — vision model errors, large file handling
- `references/query-patterns.md` — querying reference-only image nodes