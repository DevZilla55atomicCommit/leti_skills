# Common Pitfalls & Fixes

## 1. "no LLM API key found (N doc/paper/image file(s) need semantic extraction)"

**Cause**: Corpus contains non-code files (`.md`, `.pdf`, images, videos) but no API key configured.

**Fixes:**
```bash
# Option A: Skip non-code files (free)
cat > .graphifyignore << 'EOF'
*.md
*.txt
*.pdf
*.png *.jpg *.webp *.gif
*.mp4 *.mov *.mp3 *.wav
.obsidian/
EOF
graphify .

# Option B: Set API key (one of these)
export GEMINI_API_KEY="your-key"        # Google AI Studio (free tier)
export ANTHROPIC_API_KEY="sk-ant-..."   # Anthropic
export OPENAI_API_KEY="sk-..."          # OpenAI / OpenAI-compatible
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3.1"          # Must support /api/generate
graphify .
```

## 2. Ollama Chunks Fail with "404 page not found"

**Cause**: Model doesn't support Ollama's `/api/generate` endpoint format. MLX models (e.g., `qwen3.5:4b-mlx`, `gemma4:e4b-mlx`) often fail.

**Fix:**
```bash
# Use a standard Ollama model that supports generate
ollama pull llama3.1
ollama pull mistral
ollama pull codellama

export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3.1"
export OLLAMA_API_KEY="x"  # Any non-empty value suppresses warning
graphify . --backend ollama
```

**Test model first:**
```bash
curl -s http://localhost:11434/api/generate -d '{"model": "your-model", "prompt": "test", "stream": false}'
```

## 3. "graphify: command not found" After Install

**Cause**: `~/.local/bin` (uv) or `~/Library/Python/3.x/bin` (pip) not on PATH.

**Fix:**
```bash
# uv tool
uv tool update-shell
source ~/.zshenv  # or restart shell

# pipx
pipx ensurepath
source ~/.zshenv

# pip (macOS)
echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zshenv
source ~/.zshenv
```

## 4. Graph Has Fewer Nodes After `--update` / Rebuild

**Cause**: Refactor deleted files; old nodes remain. Graphify refuses to shrink by default (#479 guard).

**Fix:**
```bash
graphify . --force          # Full rebuild, allow shrink
graphify update . --force   # Incremental, allow shrink
```

## 5. HTML Too Large to Open in Browser (>5000 nodes)

**Cause**: Large corpus generates massive `graph.html`.

**Fix:**
```bash
graphify . --no-viz                    # Skip HTML, keep report + JSON
graphify cluster-only . --no-viz       # Re-cluster without viz
graphify query "..."                   # Query via CLI instead
```

## 6. Export Overwrites / Fails in Existing Vault

**Cause**: Target directory has pre-existing files Graphify doesn't own.

**Fix:**
```bash
# Export to empty/new directory first
graphify export obsidian --dir "/path/to/empty/Graphify-Project"

# Then merge/move into main vault manually
# Graphify's manifest (.graphify_obsidian_manifest.json) protects your notes on re-export
```

## 7. Incremental Update (`graphify update`) Doesn't Pick Up Changes

**Cause**: Manifest paths drifted, or `.graphify_root` points to wrong location.

**Fix:**
```bash
# Check current root
cat graphify-out/.graphify_root

# Full rebuild with correct path
cd /correct/project/root
graphify . --force
```

## 8. Skill Not Found in Hermes After `graphify hermes install`

**Cause**: On Windows, Hermes scans `%LOCALAPPDATA%\hermes\skills`, not `~/.hermes/skills`.

**Fix:**
```bash
# Windows: graphify install handles this automatically via _platform_skill_destination
# macOS/Linux: skill goes to ~/.hermes/skills/graphify/SKILL.md

# Verify
ls ~/.hermes/skills/graphify/
```

## 9. Semantic Extraction Returns Empty/Poor Results

**Cause**: Model context window too small, or token budget too low for dense files.

**Fix:**
```bash
# Increase context (Ollama)
export GRAPHIFY_OLLAMA_NUM_CTX=32768
export GRAPHIFY_OLLAMA_KEEP_ALIVE=0  # Unload after each chunk (saves VRAM)

# Increase token budget
graphify extract . --token-budget 30000

# Raise output cap for dense corpora
export GRAPHIFY_MAX_OUTPUT_TOKENS=32768
graphify extract .
```

## 10. Wikilinks Not Working in Obsidian Export

**Cause**: Node labels contain characters invalid in filenames/wikilinks.

**Fix**: Graphify sanitizes automatically (`safe_name()` in export.py), but edge cases exist. Check:
- Filenames don't start with `.` (hidden files)
- No duplicate names after sanitization (Graphify adds `_1`, `_2` suffixes)
- Community names don't collide case-insensitively (Graphify dedupes)

## 11. Community Labels Show "Community N" Instead of Names

**Cause**: No LLM backend configured for labeling (happens with `--no-cluster` or Ollama without labeling model).

**Fix:**
```bash
# Re-label with backend
graphify label . --backend gemini --model gemini-2.5-pro
graphify label . --backend ollama --model llama3.1

# Or during cluster-only
graphify cluster-only . --backend gemini --model gemini-2.5-pro
```

## 12. Video/Audio Files Not Processed

**Cause**: Missing `video` extra or ffmpeg/yt-dlp not installed.

**Fix:**
```bash
uv tool install "graphifyy[video]"
# Requires: ffmpeg, yt-dlp (auto-installed via faster-whisper deps)
```

## Quick Debugging Checklist

```bash
# 1. Check what files Graphify sees
graphify extract . --no-cluster 2>&1 | head -20

# 2. Check graph health
python -c "
from graphify.diagnostics import diagnose_extraction
import json
from pathlib import Path
ext = json.loads(Path('graphify-out/.graphify_extract.json').read_text())
print(diagnose_extraction(ext))
"

# 3. Verify graph.json exists and has nodes
python -c "
import json
from pathlib import Path
g = json.loads(Path('graphify-out/graph.json').read_text())
print(f'Nodes: {len(g[\"nodes\"])}, Edges: {len(g[\"links\"])}')
"

# 4. Test query directly
graphify query "test question" --budget 500
```