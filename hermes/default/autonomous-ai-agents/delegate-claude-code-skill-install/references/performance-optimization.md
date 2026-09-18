# Performance Optimization for Claude Code Skill Installation

## Preferred Models for Speed

When installing skills with Claude Code via delegation, model selection significantly impacts execution time:

| Model | Approx. Load Time | When to Use |
|-------|------------------|-------------|
| `qwen3.5:4b-mlx` | 5-10 seconds | **Default choice for most skill installations** – fast startup, sufficient reasoning for markdown skill templates |
| `qwen3.5:9b` | 30-45 seconds | Complex reasoning tasks where 4b might lack depth |
| `claude-sonet-4.6:latest` | 60+ seconds | Enterprise-grade reasoning for highly complex workflows |
| `claude-opus-4.8:latest` | 2+ minutes | Rare cases requiring exhaustive analysis |

### Speed Best Practices

1. **Start with `qwen3.5:4b-mlx`** – it provides the best balance of speed and capability for typical skill installation tasks
2. **Avoid larger models unless explicitly needed** – they dramatically increase cold-start latency and can cause timeout issues in delegation workflows
3. **Verify model availability** before delegation:
   ```bash
   ollama list
   ```
4. **Pre-warm the model** if installing multiple skills in succession:
   ```bash
   ollama run qwen3.5:4b-mlx 'echo warm' > /dev/null
   ```

### Integration with Hermes Delegation

Update your `delegate_task` context to specify the preferred model:

```python
delegate_task(
    goal="Create Claude Code skill for API design review",
    context="""
    ## Task: Install a Claude Code Skill

    Create a skill file at ~/.claude/skills/api-design-review.md with the following content:

    [SKILL CONTENT]

    ## Execution Command
      claude -p "Create a skill file at ~/.claude/skills/api-design-review.md with the following content: [ESCAPED_CONTENT]" \\
        --model qwen3.5:4b-mlx \\
        --dangerously-skip-permissions \\
        --output-format json \\
        --max-turns 8 \\
        --bare \\
        --workdir /tmp
    """
)
```

The key change is using `--model qwen3.5:4b-mlx` instead of larger models to ensure faster execution and avoid timeouts.

--- 

This reference documents the performance characteristics observed during skill installation testing and provides concrete recommendations for maintaining responsive delegation workflows.