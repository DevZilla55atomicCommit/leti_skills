# Log Forensics for Stuck Hermes Sessions

Detailed reference for analyzing `agent.log` to diagnose looped, hung,
and rate-limited sessions. Used alongside `hermes-session-diagnostics`.

## The Log File

```text
~/.hermes/logs/agent.log
```

This is the primary diagnostic log. Every API call, tool execution, and
session lifecycle event is logged here with timestamps and session IDs.

## Extracting a Session's Activity

### Fast: Line-by-Line Streaming (Recommended)

```python
import re
with open('/Users/<user>/.hermes/logs/agent.log', 'r') as f:
    lines = f.readlines()

for line in lines:
    if '<session_id>' in line and ('tool' in line or 'API call' in line):
        print(line.strip())
```

This streams the file — no full-content regex, no timeout risk.

### What Each Log Line Tells You

```text
2026-07-08 14:59:53,687 INFO [SESSION_ID] agent.tool_executor: tool terminal completed (1.79s, 38101 chars)
                                       │            │      │          │           │
                                       │            │      │          │           └─ output size
                                       │            │      │          └─ tool name + verb
                                       │            │      └─ execution time
                                       │            └─ component
                                       └─ message
```

Key fields:
- **Timestamp** — when the tool completed
- **Session ID** — filter by this to isolate one session
- **Tool name** — terminal, browser_navigate, skill_view, etc.
- **Execution time** — very short (0.5s) + very small output (45 chars)
  repeated many times = loop signature
- **Output size** — 45 chars ≈ `ps aux`-style command output; 129 chars
  ≈ slightly longer command; 38101 chars ≈ full `ps aux` dump

## Loop Signatures

### Classic Agentic Loop (Most Common)

```text
14:59:53 terminal completed (1.79s, 38101 chars)   ← first big output
15:05:39 terminal completed (0.72s, 129 chars)       ← small probe
15:05:46 terminal completed (0.52s, 7568 chars)     ← medium probe
15:05:49 terminal completed (0.37s, 204 chars)       ← small
15:05:52 terminal completed (0.50s, 129 chars)       ← same probe again
15:06:18 terminal completed (0.50s, 129 chars)       ← same probe AGAIN
15:06:33 terminal completed (0.50s, 129 chars)       ← AGAIN
15:06:36 terminal completed (0.69s, 7568 chars)     ← medium
...
```

**Diagnosis:** The model is alternating between a few commands and never
producing a text response. The API call numbers increment (call #5, #6,
#7...) with tiny `out=N` token counts (54–113 tokens) — meaning the model
is only generating tool calls, not reasoning text.

**Root cause patterns observed:**
- A task seed (e.g. a YouTube redirect URL) that the model keeps probing
  but cannot resolve
- A web scraping target that redirects or fails, and the model retries
  with slight variations endlessly

### Rate-Limited Loop

```text
17:36:57 WARNING [SESSION] Retrying API call in 4.76s (attempt 2/3)
    provider=nvidia error=ResourceExhausted: Worker local total
    request limit reached (32/32)
17:36:58 INFO [SESSION] API call #16: latency=15.0s
17:37:00 INFO [SESSION] tool skill_view completed (0.06s, 6893 chars)
...
```

**Diagnosis:** Not a loop — the provider is rate-limited. The session
will resume once the limit clears. Don't kill it unless it's been stuck
for a very long time.

### Hung on Background Process Poll

```text
15:58:68 INFO [SESSION] terminal completed (background process started, session_id=proc_xxx)
15:58:71 INFO [SESSION] API call #N: latency=3.0s
... [no further log entries for this session]
```

If the last action was starting a background process and then polling
it, but the background process was killed (SIGTERM) before returning,
the session will hang indefinitely. The `process(action='poll')` call
never receives a result.

## TONY Gateway Provider-Chain Pitfall

A common cause of gateway issues in TONY/Charlie OS setups:

```javascript
// config.js
anthropic: {
  apiKey: env('ANTHROPIC_API_KEY', ''),  // empty string if not set
}

// llm/index.js — provider chain
function buildChain() {
  // If llmProvider='nvidia', chain is ['nvidia', 'jan']
  // But if anthropic.apiKey is '', any code that checks it as
  // truthy will get false — yet some code paths still try Anthropic
  // and get an "invalid x-api-key" error
}
```

### Diagnostic

```bash
cd /path/to/TONY-AI-Agent && node -e "
require('dotenv').config();
const config = require('./src/config');
const { buildChain } = require('./src/llm/index');
console.log('Provider chain:', buildChain());
console.log('anthropic apiKey truthy:', !!config.anthropic.apiKey);
console.log('nvidia apiKey truthy:', !!config.nvidia.apiKey);
"
```

If `anthropic apiKey truthy: false` but the provider chain includes
`anthropic`, that's the bug — the provider chain should only include
providers with valid keys.

## Session Search Truncation

`session_search(session_id=...)` in read mode shows:
- First 20 messages
- Last 10 messages
- For sessions with >150 messages, the middle is truncated

To scroll the middle:

```text
session_search(
    session_id="<id>",
    around_message_id=<any_message_id_from_the_window>,
    window=20
)
```

- To scroll **forward**: pass the last message's ID as `around_message_id`
- To scroll **backward**: pass the first message's ID as `around_message_id`

This is essential for sessions with 100+ messages — the middle section
often contains the pivoting point where the session went off track.
