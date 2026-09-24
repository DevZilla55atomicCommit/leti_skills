# Session 2026-07-17 — Pipeline Execution Notes

## Summary
Videographer pipeline first execution. 251 URLs processed, 1 success, 250 skipped.

## Key Findings

### URL Availability (251 URLs)
| Outcome | Count | Percentage |
|---------|-------|------------|
| ✅ Successfully processed | 1 | 0.4% |
| ⏭️ Deleted/Unavailable | 126 | 50.2% |
| 📷 No video content (photo/carousel) | 124 | 49.4% |
| ❌ Other errors | 1 | 0.4% |

**Lesson**: Instagram Reel URLs have short lifespans. Old URLs (>6 months) are mostly deleted or converted to photo posts. Fresh URLs needed for meaningful processing.

### Script Location Issue
The pipeline script `run_pipeline.py` lives in the **skill directory**, not the vault directory:
- ✅ Correct: `~/.hermes/skills/automation/instagram-videographer-learning-pipeline/scripts/run_pipeline.py`
- ❌ Wrong: `Videographer/scripts/run_pipeline.py` (doesn't exist)

The session tried to run from vault directory and failed with "No such file or directory".

### Compression Config Fix Applied
Both global and profile configs updated:
```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    # base_url: http://127.0.0.1:11434/v1  # REMOVED - was pointing to local Ollama
```
Model `nvidia/nemotron-mini-4b-instruct` confirmed available on NVIDIA API.

## Pipeline Output (1 Success)
- **Reel**: `DaBejwDkznl` — "The Art of Static Shots" by @anshuluniyyal
- **Vault Note**: `camera-theory/01-Static-Shots-Composition_Anshuluniyyal.md`
- **Skill**: `videographer-static-shots-composition`
- **Assets**: Frames, demo GIF, technique loop GIF, before/after comparison

## Next Run Recommendations
1. Provide fresh Instagram Reel URLs (< 3 months old)
2. Run from skill directory: `cd ~/.hermes/skills/automation/instagram-videographer-learning-pipeline/scripts && python3 run_pipeline.py --input queue.json`
3. Or via Hermes CLI: `hermes skill run instagram-videographer-learning-pipeline --input queue.json --batch-size 10`