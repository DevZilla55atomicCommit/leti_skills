# Delegate Task Context Template for Skill Installation

Copy this template and fill in the placeholders when creating a new delegation to install a skill into Claude Code.

```python
delegate_task(
    goal="Create Claude Code skill: <SKILL_NAME>",
    context="""## Task: Install a Claude Code Skill

Create a skill file at ~/.claude/skills/<SKILL_NAME>.md with the following content:

## Skill Content

<SKILL_CONTENT_MARKDOWN>

## Execution Command

Use this exact command pattern:
  claude -p "Create a skill file at ~/.claude/skills/<SKILL_NAME>.md with the following content: <ESCAPED_SKILL_CONTENT>" \\
    --model <MODEL_NAME> \\
    --dangerously-skip-permissions \\
    --output-format json \\
    --max-turns <MAX_TURNS> \\
    --bare \\
    --workdir /tmp

## Requirements

- File must be created at ~/.claude/skills/<SKILL_NAME>.md
- Content must match exactly what's provided above
- Verify by reading the file back
- Return success/failure in JSON output"""
)
```

## Field Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `<SKILL_NAME>` | Kebab-case filename (no .md) | `api-design-review` |
| `<SKILL_CONTENT_MARKDOWN>` | Full markdown content of the skill | See examples below |
| `<ESCAPED_SKILL_CONTENT>` | Skill content with escaping for JSON string | Escape backticks, quotes, newlines |
| `<MODEL_NAME>` | Exact Ollama model name | `qwen3.5:9b` |
| `<MAX_TURNS>` | Turn limit based on complexity | `8` (simple), `15` (complex) |

## Model Selection Guide

| Complexity | Model | Max Turns |
|------------|-------|-----------|
| Simple checklist/guidelines | `qwen3.5:9b` | 5-8 |
| Multi-section with examples | `claude-sonet-4.6:latest` | 10-15 |
| Architecture/decision frameworks | `claude-opus-4.8:latest` | 15-20 |

## Content Escaping Rules

When embedding skill content in the prompt string, escape:
- Backticks: `\` → `\\``
- Double quotes: `"` → `\"`
- Newlines: `\n` → `\\n`
- Backslashes: `\` → `\\`

## Example: Simple Skill

**SKILL_NAME**: `git-commit-message-checklist`

**SKILL_CONTENT_MARKDOWN**:
```markdown
# Git Commit Message Checklist

When asked to review or write a commit message:
1. Subject line ≤ 50 chars, imperative mood
2. Body explains WHAT and WHY (not HOW)
3. Reference issue/PR number if applicable
4. No trailing period in subject
5. Separate subject from body with blank line
```

**SKILLUSTRATIVE EXAMPLE:
```
Fix user login timeout on mobile

Increased JWT expiry from 1h to 24h for mobile clients
to prevent unexpected logouts during long sessions.

Closes #42
```
```

## Example: Complex Skill (Multi-section)

**SKILL_NAME**: `security-audit-checklist`

**SKILL_CONTENT_MARKDOWN**:
```markdown
# Security Audit Checklist

When asked to perform a security audit:

## 1. Authentication & Authorization
- [ ] No hardcoded credentials
- [ ] JWT validation (sig, exp, aud, iss)
- [ ] RBAC enforced on all endpoints
- [ ] Session security (HttpOnly, Secure, SameSite)

## 2. Input Validation
- [ ] SQL injection prevention (param queries)
- [ ] XSS prevention (output encoding)
- [ ] Path traversal protection
- [ ] File upload validation

## 3. Data Protection
- [ ] PII encryption at rest/in transit
- [ ] TLS 1.2+ enforced
- [ ] Secrets in env vars only
- [ ] Audit logging for sensitive ops

## Output Format
Return findings as JSON array with severity (critical/high/medium/low).
```
```

## Verification Steps

After delegation completes, run:
```bash
# 1. Check file exists
ls -la ~/.claude/skills/<SKILL_NAME>.md

# 2. Verify content
cat ~/.claude/skills/<SKILL_NAME>.md

# 3. Test auto-invocation
claude -p "Test the <SKILL_NAME> skill" --model qwen3.5:9b --bare --max-turns 3
```