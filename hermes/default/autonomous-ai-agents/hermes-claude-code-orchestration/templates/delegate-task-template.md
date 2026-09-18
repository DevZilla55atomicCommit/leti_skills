# Delegate Task Template for Hermes → Claude Code

Use this template when Hermes delegates coding tasks to Claude Code via `delegate_task`.

## Context Template

Copy and customize for each delegation:

```python
delegate_task(
    goal="<SPECIFIC CODING TASK>",
    context="""Project: <PROJECT NAME>
Path: <ABSOLUTE PATH TO PROJECT ROOT>

## Task Details
<Clear, specific description of what to build/fix/refactor>

## Technical Requirements
- Language/Framework: <e.g., Python FastAPI, React TypeScript>
- Key files to modify: <list specific files>
- Tests required: <unit/integration/e2e>
- Style guide: <link to CLAUDE.md or project rules>

## Claude Code Execution Command
Use this exact command pattern:
  claude -p "<NATURAL LANGUAGE TASK>" \\\\
    --model claude-sonet-4.6:latest \\\\
    --dangerously-skip-permissions \\\\
    --output-format json \\\\
    --max-turns 10 \\\\
    --bare
    # Note: --workdir REMOVED in v2.x; use cwd in delegate_task context or cd in shell

## Expected Output
- JSON result with 'result' field containing completion summary
- Files created/modified at <paths>
- Tests passing: <command to verify>

## Constraints
- Do NOT use model aliases (sonnet/haiku/opus) — Ollama backend
- Do NOT exceed <N> turns
- Do NOT modify files outside <scope>
"""
)
```

## Example: Build JWT Auth Module

```python
delegate_task(
    goal="Build JWT authentication module for FastAPI",
    context="""Project: TamaZila API
Path: /Users/alfredkamisese/projects/tamazila-api

## Task Details
Create a complete JWT auth module with:
- Token generation (access + refresh)
- Token validation middleware
- Protected route dependency
- Password hashing with bcrypt
- Token blacklist for logout

## Technical Requirements
- Language: Python 3.11, FastAPI
- Key files: auth/models.py, auth/service.py, auth/middleware.py, auth/router.py
- Tests: pytest with httpx async client
- Style: Follow CLAUDE.md (type hints, Google docstrings, 4-space indent)

## Claude Code Execution Command
  claude -p "Build a complete JWT auth module for FastAPI with access/refresh tokens, middleware, and bcrypt password hashing. Create auth/models.py, auth/service.py, auth/middleware.py, auth/router.py with tests." \\\\
    --model claude-sonet-4.6:latest \\\\
    --dangerously-skip-permissions \\\\
    --output-format json \\\\
    --max-turns 15 \\\\
    --bare
    # Note: --workdir REMOVED in v2.x; delegate_task handles cwd

## Expected Output
- JSON result with completion summary
- Files: auth/models.py, auth/service.py, auth/middleware.py, auth/router.py, tests/test_auth.py
- Verify: cd /path && make test

## Constraints
- Use exact Ollama model name
- Max 15 turns
- Stay within auth/ directory
"""
)
```

## Example: Code Review

```python
delegate_task(
    goal="Security review of PR #234 - user upload endpoint",
    context="""Project: TamaZila API
Path: /Users/alfredkamisese/projects/tamazila-api

## Task Details
Review the file upload endpoint for:
- Path traversal vulnerabilities
- File type validation bypasses
- Size limit enforcement
- Secure filename generation
- Proper cleanup on error

## Technical Requirements
- Language: Python FastAPI
- Files to review: api/upload.py, services/storage.py
- Output: Structured findings with severity (critical/high/medium/low)

## Claude Code Execution Command
  claude -p "Security review of api/upload.py and services/storage.py. Check for path traversal, file type bypass, size limits, secure filenames, and error cleanup. Output JSON with findings array containing file, line, severity, description, fix." \\\\
    --model claude-opus-4.8:latest \\\\
    --dangerously-skip-permissions \\\\
    --output-format json \\\\
    --max-turns 8 \\\\
    --bare
    # Note: --workdir REMOVED in v2.x; delegate_task handles cwd

## Expected Output
- JSON with findings array
- Each finding: {file, line, severity, description, recommendation}
"""
)
```

## Parsing Results

```python
result = delegate_task(...)
# result is a list of subagent results
for r in result:
    if r.get("success"):
        import json
        cc_result = json.loads(r["output"])
        # cc_result contains the structured JSON from Claude Code
        print(cc_result.get("result", ""))
        print(f"Turns: {cc_result.get('num_turns')}")
        print(f"Cost: ${cc_result.get('total_cost_usd', 0):.4f}")
```