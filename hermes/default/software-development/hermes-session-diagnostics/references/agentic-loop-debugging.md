# Agentic Loop Debugging Pattern

**Session:** `20260709_093552_7e9739` investigating stuck session `20260708_145844_4b6b72`

## Problem Class: LLM Agent Stuck in Infinite Tool-Call Loop

### Symptoms
- Session runs for hours (5+ hours observed)
- Hundreds of repetitive `terminal` tool calls with minimal output (~45 chars)
- `ps aux`-style commands producing no useful information
- No progress toward user goal
- Session never completes or errors

### Root Cause Pattern
LLM agents without loop detection will repeat identical or near-identical tool calls when:
1. Model doesn't receive clear "you're done" signal (`finish_reason: stop`)
2. Tool results are low-value but not errors
3. No progress tracking exists
4. Max iterations set too high (12 in original config)

### Detection via Log Forensics
```bash
# Search agent logs for session
grep "SESSION_ID" /path/to/agent.log

# Look for repetitive patterns
grep "tool terminal completed" agent.log | grep SESSION_ID

# Count iterations
grep -c "API call #" agent.log | grep SESSION_ID
```

### Fix Pattern: Multi-Layer Loop Breaking (Implemented in `src/core/agent.js`)

| Layer | Trigger | Action |
|-------|---------|--------|
| **Duplicate Detection** | 3+ identical `(toolName, JSON.stringify(args))` | Break + summarize |
| **Low-Progress Detection** | 3+ calls with `<100 char` results | Break + synthesize |
| **FinishReason Check** | `result.finishReason === 'stop'` with no tool calls | Break immediately |
| **Progress Change Detection** | No meaningful content change over iterations | Break + summarize |

### Configuration Hardening
```bash
# Reduce max iterations to limit blast radius
TONY_MAX_ITERATIONS=8  # was 12
```

---

## Problem Class: Provider Chain Caching in Node.js LLM Gateways

### Symptoms
- Health endpoint shows correct chain: `['nvidia', 'jan']`
- But chat API returns `"invalid x-api-key"` (Anthropic error)
- Gateway process loaded `llm/index.js` at startup and cached the `chain` constant

### Root Cause
```javascript
// config.js
anthropic: {
  apiKey: env('ANTHROPIC_API_KEY', ''),  // empty string if not set
}

// llm/index.js — provider chain
const chain = buildChain();  // Module-level constant, computed once

// buildChain() filters by truthy apiKey, but if apiKey is ''
// it's falsy... except some code paths still try Anthropic
// and get an "invalid x-api-key" error
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

If `anthropic apiKey truthy: false` but the provider chain includes `anthropic`, that's the bug — the provider chain should only include providers with valid keys.

### Fix Pattern: Defensive `.trim()` Checks (11 locations in `src/llm/index.js`)
```javascript
// Before
if (config.anthropic.apiKey && !chain.includes('anthropic')) chain.push('anthropic');

// After
if (config.anthropic.apiKey?.trim() && !chain.includes('anthropic')) chain.push('anthropic');
```

---

## System Hardening Checklist for LLM Agents

| Layer | Protection | Status |
|-------|------------|--------|
| **Loop Prevention** | Duplicate detection (3x) | ✅ Implemented |
| **Loop Prevention** | Low-progress detection (3x, <100 chars) | ✅ Implemented |
| **Loop Prevention** | FinishReason early termination | ✅ Implemented |
| **Loop Prevention** | Progress change detection | ✅ Implemented |
| **Config Hardening** | Max iterations reduced (12 → 8) | ✅ Implemented |
| **Config Hardening** | API key `.trim()` validation | ✅ 11 locations |
| **Gateway** | 120s timeout on chat endpoints | ✅ Implemented |
| **Process Cleanup** | Killed 6 zombie slash_workers | ✅ Completed |
| **Observability** | Iteration logging with counters | ✅ Implemented |

---

## Session Search for Loop Analysis

```python
# Full session scroll (for 150+ message sessions)
session_search(session_id="<id>", around_message_id=<any_id>, window=20)

# Forward scroll
session_search(session_id="<id>", around_message_id=last_message_id, window=20)

# Backward scroll
session_search(session_id="<id>", around_message_id=first_message_id, window=20)
```

---

## Key Takeaway

**Agentic loops are the #1 failure mode for unsupervised LLM agents.** They occur when the model's tool-calling behavior enters a fixed point with no exit condition. The fix is not "better prompts" — it's **structural loop breaking in the agent runtime** with multiple independent detection layers.

**Provider chain caching is the #1 Node.js LLM gateway failure mode.** Module-level `const chain = buildChain()` computed once at require-time means configuration changes require process restart. Always clear `require.cache` or restart the gateway after config changes.