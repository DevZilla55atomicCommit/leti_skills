# Graphify Troubleshooting Guide

## Installation Issues

### `graphify: command not found`
```bash
# After uv tool install graphifyy
uv tool update-shell
# Restart shell or: source ~/.zshenv (or ~/.bashrc)
```

### Wrong Python environment
```bash
# Graphify writes interpreter path to graphify-out/.graphify_python
# Check it matches your environment:
cat graphify-out/.graphify_python
# Should be ~/.local/bin/... for uv tool installs
```

## NVIDIA NIM / OpenAI-Compatible Backend Issues

### NVIDIA Cloud API errors
```
# Invalid API key
curl -s "https://integrate.api.nvidia.com/v1/models" -H "Authorization: Bearer $NVIDIA_API_KEY"
# Should return model list; 401 = bad key
```

### Model lacks multimodal/vision support (CRITICAL)
```
# Error: "ValueError: Received multimodal data but multimodal processing is not enabled."
# Cause: Model doesn't support vision input (images/GIFs)
# Nemotron 3 Ultra (550B) is TEXT-ONLY despite being the best quality model

# Fix: Use a vision-capable NVIDIA model:
export OPENAI_MODEL="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"  # 30B, has vision
# Or:
export OPENAI_MODEL="meta/llama-3.2-90b-vision-instruct"              # 90B, has vision

# The error mentions "--enable-multimodal flag" — THIS FLAG DOES NOT EXIST in CLI.
# It's a model capability, not a CLI option.
```

### NVIDIA Model Vision Capability Matrix

| Model | Params | Vision? | Best For |
|-------|--------|---------|----------|
| `nvidia/nemotron-3-ultra-550b-a55b` | 550B MoE | ❌ NO | Text extraction, naming, reasoning |
| `nvidia/nemotron-3-super-120b-a12b` | 120B MoE | ❌ NO | Text extraction, naming |
| `nvidia/llama-3.1-nemotron-70b-instruct` | 70B | ❌ NO | General text |
| **`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`** | 30B | ✅ YES | **Images + text** — only Nemotron with vision |
| **`meta/llama-3.2-90b-vision-instruct`** | 90B | ✅ YES | **Images + text** — largest vision model |
| `meta/llama-3.2-11b-vision-instruct` | 11B | ✅ YES | Lightweight vision |

> **Rule**: If your vault has images/GIFs/PDFs, you MUST use a vision-capable model. Text-only models will fail on every image chunk with 400 errors.

### Large GIF/Image Files (>5 MB) — TamaZila Vault Case
```
# Log: "image X.gif is 70645 KB, over the 5 MB inline-image limit for this backend; sending it as a reference node without inline pixels."
# Graphify auto-skips inline vision for files >5 MB — sends as reference node only.
# The TamaZila vault has GIFs from 10–100 MB in DaVinci_Knowledge_Base/Instagram_Reels/...
# These become nodes with filename metadata but NO visual content extraction.

# Workarounds:
# 1. Pre-process: Extract 1-3 key frames per GIF as <5 MB JPGs before indexing
# 2. Accept reference-only: Graph links them via filename/wikilinks — useful for navigation
# 3. Separate vision pipeline: Run dedicated vision on extracted frames, merge later
# 4. HYBRID STRATEGY (RECOMMENDED for TamaZila): Skip ALL images, index text fully
#    See references/hybrid-text-reference-strategy.md
```

### Model not found
```
# List available models first
curl -s "$OPENAI_BASE_URL/models" -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id'
# Use exact model ID from list (case-sensitive)
```

### Local NIM container not responding
```
# Check container is running
docker ps | grep nim
# Check logs
docker logs <container_id>
# Test endpoint
curl -s http://localhost:8000/v1/models -H "Authorization: Bearer local-key"
```

### NIM accepts any API key (local)
```
# Local NIM doesn't validate the key — any non-empty string works
export OPENAI_API_KEY="anything"
```

### Rate limiting on NVIDIA Cloud
```
# Free tier has per-minute token limits
# Reduce concurrency: graphify . --max-concurrency 1
# Or use local NIM for unlimited throughput
```

## API Key & Quota Issues

### `no LLM API key found`
```bash
# Set one of these (Gemini free tier easiest):
export GEMINI_API_KEY="your-key"        # ai.google.dev
export ANTHROPIC_API_KEY="sk-ant-..."   # console.anthropic.com
export OPENAI_API_KEY="sk-..."          # platform.openai.com
# Or use local Ollama:
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen3.5:9b"
```

### `429 quota exceeded` (Gemini free tier)
```
Free tier: 250,000 input tokens/minute per model
Fix options:
1. Wait 30-60 seconds and retry
2. Reduce concurrency: graphify . --max-concurrency 1
3. Use gemini-2.5-flash-lite (lower quota pressure)
4. Add billing at ai.google.dev for higher limits
5. Switch to Ollama for fully local extraction
```

### Ollama 404 errors
```
Problem: Model doesn't support /api/generate endpoint
Fix: Use non-MLX models:
  ✅ qwen3.5:9b, qwen3.5:4b, gemma4:12b
  ❌ qwen3.5:4b-mlx, gemma4:e4b-mlx
Check: ollama list | grep -v mlx
```

## Graph Build Issues

### Graph has fewer nodes after `--update`
```bash
# Refactoring deleted files; old nodes linger
graphify extract . --force
# Or full rebuild:
rm -rf graphify-out && graphify .
```

### `ERROR: Graph is empty`
```
Causes:
- All files skipped by .graphifyignore
- Binary-only corpus (no supported extensions)
- Extraction failed silently

Debug:
1. Check detect output: graphify . --dry-run (not a real flag, but check .graphify_detect.json)
2. Verify file extensions in detect.py CODE_EXTENSIONS
3. Check .graphifyignore isn't excluding everything
```

### HTML too large (>5000 nodes)
```bash
# Skip HTML, use JSON queries instead
graphify . --no-viz
graphify query "your question" --budget 2000
```

## Obsidian Export Issues

### Export fails: `graph not found`
```bash
# Must run from directory with graphify-out/
cd /path/to/project
graphify export obsidian --dir /path/to/vault/Graphify-Project
```

### Notes not appearing in Graph View
```bash
# Check .obsidian/graph.json exists in export dir
# Restart Obsidian to reload graph.json
# Verify tags: #community/Name format matches colorGroups query
```

### Community colors not showing
```bash
# .obsidian/graph.json only written on FIRST export
# If communities changed, delete .obsidian/graph.json and re-export
rm /path/to/vault/Graphify-Project/.obsidian/graph.json
graphify export obsidian --dir /path/to/vault/Graphify-Project
```

### Manifest warnings: "skipped pre-existing files"
```
Meaning: Graphify refuses to overwrite files it didn't create
Fix: Export to empty directory, or delete old Graphify-Project folder first
```

## Incremental Update Issues

### `--update` doesn't pick up new files
```bash
# Check manifest.json in graphify-out/
cat graphify-out/manifest.json
# Keys are relative paths; must match current scan root
# If moved project, delete graphify-out/ and rebuild
```

### `--cluster-only` community labels lost
```bash
# Labels stored in .graphify_labels.json
# If missing, re-run full pipeline or:
graphify label . --backend gemini
```

## Performance Issues

### Slow semantic extraction
```bash
# Reduce chunk size
graphify . --token-budget 4000
# Reduce concurrency
graphify . --max-concurrency 1
# Use faster model
GRAPHIFY_GEMINI_MODEL=gemini-2.5-flash-lite graphify .
```

### High memory usage
```bash
# Limit AST workers
GRAPHIFY_MAX_WORKERS=4 graphify .
# Process subdirectories separately
graphify ./src --obsidian --obsidian-dir ~/vault/Graphify-Src
```

## Debugging Commands

```bash
# Verbose detection
python -c "
from graphify.detect import detect
from pathlib import Path
import json
result = detect(Path('.'))
print(json.dumps(result, indent=2))
"

# Check graph stats
python -c "
import json
from graphify.export import load_graph
G, communities = load_graph('graphify-out/graph.json')
print(f'Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}, Communities: {len(communities)}')
for cid, members in communities.items():
    print(f'  Community {cid}: {len(members)} nodes')
"

# Graph health check
python -c "
from graphify.diagnostics import diagnose_extraction
import json
from pathlib import Path
extraction = json.loads(Path('graphify-out/.graphify_extract.json').read_text())
summary = diagnose_extraction(extraction, directed=False, root='.')
print(summary)
"
```

## Environment-Specific

### macOS: Case-insensitive filesystem collisions
```bash
# Fortran .f90/.F90 collide on APFS
# Run tests in Docker or Linux
# Not a Graphify bug - filesystem limitation
```

### Windows: PowerShell path separator
```powershell
# Use without leading slash
graphify .     # not /graphify .
```

### CI/CD: No interactive shell
```bash
# Use graphify extract (headless) instead of /graphify skill
GEMINI_API_KEY=$GEMINI_API_KEY graphify extract . --backend gemini
```

## Getting Help

- Discord: https://discord.gg/598Ad9zQZ
- Issues: https://github.com/Graphify-Labs/graphify/issues
- Check `.graphify_python` interpreter matches where graphifyy is installed
- Run `graphify --version` to verify version