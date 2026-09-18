# Hermes Agent Integration — Step Beyond v4

> Session-derived integration notes for running Step Beyond inside Hermes Agent (local-first, multi-provider, subagent-orchestrated).

---

## 1. Skill Loading

In `~/.hermes/config.yaml`, ensure `step-beyond` loads **first** so its behavioral layer wraps all downstream skills:

```yaml
skills:
  load_order:
    - step-beyond
    - step-beyond-chatgpt
  # ... other skills
```

The skill auto-loads on session start (Hermes reads `load_order` at init). No manual `skill` command needed.

---

## 2. Subagent Mapping (Hermes `delegate_task`)

| Step Beyond Role | Hermes Implementation |
|------------------|----------------------|
| **ORCHESTRATOR** | This session (planner) — owns CONTEXT, INTENT, DECIDE, permission, DELIVER, LEARN |
| **BUILDER** | `delegate_task` worker with `toolsets: ["terminal", "file", "code_exec", "web", "mcp"]` — executes authorized BUILD/EXECUTE |
| **VERIFIER** | Fresh-context `delegate_task` — receives **only** deliverable + original request + domain verify table + slop index (Firewall rule) |
| **SPECIALIST** | Parallel `delegate_task` calls for independent authorized actions |
| **CRITIC** | Optional heavy-review subagent for major deliverables |

**Critical:** The Verifier Firewall — verifier subagent must **not** receive builder reasoning, plans, or justifications. Fresh context = independent evidence.

---

## 3. Memory & User Model

Hermes provides two memory surfaces:

| Surface | Step Beyond Binding |
|---------|---------------------|
| `memory` (builtin, `~/.hermes/memory/`) | Project facts cache — **not** user-model store |
| `user` profile (builtin) | Stable preferences — **not** learned hypotheses |

**Step Beyond user-model store** (when runtime-backed):
- Use `@step-beyond/runtime-store` → `JsonUserModelStore('.step-beyond', '<namespace>')`
- Namespace = opaque user identifier (e.g., hash of Telegram chat ID)
- Rejects likely credentials; supports audit, correction, rollback

**Prompt-only fallback:** Session-scoped `templates/user-patterns.md` pattern file (reinforced/banned/watching/trajectories/open-loops). Not durable across sessions.

---

## 4. Environment Scan in Hermes

Hermes tools map directly to scan layers:

| Scan Layer | Hermes Tool |
|------------|-------------|
| Manifests/lockfiles | `read_file`, `search_files` |
| VCS history | `terminal` → `git log --oneline -20`, `git log -- <path>` |
| Directory structure | `search_files(target='files')` |
| Neighboring code | `search_files`, `read_file` |
| Config/CI/lint | `read_file` (eslint, prettier, tsconfig, .github/workflows) |
| Project docs | `read_file` (README, CLAUDE.md, AGENTS.md, docs/) |

**Budget:** A few targeted reads per request — not a full crawl. Cache in working context; refresh only when request moves to unrelated area.

---

## 5. MCP Servers as Capability Adapters

Hermes MCP servers expose capabilities that map to Step Beyond adapter operations:

| MCP Server | Adapter Capability |
|------------|-------------------|
| `davinci-resolve` | `execute_local` (timeline/color/fusion ops), `read_project` (media pool, timelines) |
| `ollama_flux` | `execute_local` (image generation) |
| Custom MCP | Extend as needed |

**Rule:** One owner per capability. If Hermes MCP already provides verified execution evidence, Step Beyond VERIFY stage audits that evidence — does not duplicate the run.

---

## 6. Verification Ledger Integration

Hermes tool outputs (terminal stdout, search results, MCP responses) are **observations**. Map each material claim to a verification record:

```ts
// In orchestrator (this session) after builder subagent returns
createVerificationRecord({
  claim: "DaVinci Resolve timeline exported to MP4",
  checkExecuted: true,
  result: "pass",
  unchecked: ["H.265 10-bit delivery spec"],
  method: "mcp__davinci_resolve__render quick_export",
  evidence: ["job_id=render_123 status=complete"],
  environmentBlockers: []
});
// → status: "partially_verified"
```

Store in `@step-beyond/runtime-core` ledger or session context (prompt-only).

---

## 7. Strict Scope in Chat

User phrases that activate strict scope (disable all initiative):

- `only`, `just`, `nothing else`
- Polish: `tylko`, `nic więcej`

When active: deliver exactly the requested artifact, no proposals, no optional steps. Verification only for the touched work.

---

## 8. Degraded Modes in Hermes

| Missing | Behavior | Announcement |
|---------|----------|--------------|
| Runtime store | Session-only patterns file | "Learning this session only — want me to create a memory file to persist it?" |
| Subagents | Solo + Fresh-Eyes self-review | "Solo host — I self-review with fresh eyes before delivering." |
| MCP/execution | Trace-only, label claims `unverified` | "I can't execute here, so I'll trace and label anything I can't run 'untested'." |
| All persistence + execution | Pure prompt-only pipeline | "Running the proactive pipeline in-session; nothing persists after we're done." |

**Never claim a power the wiring didn't deliver.**

---

## 9. Onboarding Announcement Template (Hermes)

Run once per profile install (beat ⑤ of `references/onboarding.md`):

```
✅ Step Beyond v4 live on Hermes Agent.
   • User-model store: builtin memory (session) / runtime-store at .step-beyond/ (if wired)
   • Subagents: delegate_task (Builder/Verifier/Specialist roles mapped)
   • Execution: terminal + MCP (DaVinci, Flux, custom)
   • Verification: tool outputs → ledger records
   • Strict scope: say "just do X" to disable extras.
   First task?
```

Warm starts (existing memory): one-liner or silent. Re-onboard (upgrade): announce only what changed.

---

## 10. Known Hermes-Specific Behaviors

- **Config edits blocked:** `~/.hermes/config.yaml` cannot be patched by agent — use `hermes config` CLI or manual edit. (We used `sed` with smart approval.)
- **Skill load order respected:** Skills in `load_order` load before others; `step-beyond` first ensures behavioral wrapper.
- **Parallel subagents:** `max_concurrent_children: 3` (config) — maps to Step Beyond specialist parallelization budget.
- **Tool output caps:** `tool_output.max_bytes: 50000` — large verification evidence may truncate; store full artifacts in runtime store.
- **Compression:** Enabled at 0.75 threshold — verifier subagent receives compressed builder output; ensure checklists survive compression.