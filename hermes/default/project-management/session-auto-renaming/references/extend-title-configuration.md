# Extending Title Generation Configuration

This document outlines ways to customize the automatic session title generation beyond the default settings.

## Custom Prompt Example

If you want to enforce a specific style or length, you can override the prompt by setting a custom `title_generation.prompt` in your `config.yaml`:

```yaml
auxiliary:
  title_generation:
    prompt: |
      Generate a concise title (max 5 words) that captures the main topic.
      Use the same language as the user.
      Return only the title text, no extra punctuation.
```

## Language Override

To force titles to be generated in a specific language regardless of user language, set:

```yaml
auxiliary:
  title_generation:
    language: "en"
```

## Title Length Control

To change the word count range, modify the `_TITLE_PROMPT` constant in `agent/title_generator.py`:

```python
_TITLE_PROMPT = (
    "Generate a short, descriptive title (5-8 words) for a conversation that starts with the \""
    "following exchange..."
)
```

## Advanced Usage Examples

- **Project-Specific Templates**: Store templates in `references/` and reference them in custom scripts.
- **Scheduled Renaming**: Use a cron job to rename sessions older than a certain age based on content analysis.