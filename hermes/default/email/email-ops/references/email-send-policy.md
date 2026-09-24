# Draft Collaboration Safety Policy

**Core Principle**: All outbound email operations must receive explicit user confirmation before execution. This policy codifies the safety mechanisms that enforce this rule across Hermes email workflows.

## Explicit Send Phrases

User must use **explicit confirmation language** before any email is sent:
- `"send it"`
- `"send now"`
- `"execute send"`
- `"confirm send"` (with unambiguous affirmative response)

Any variation that includes the word "send" **and** a clear intent indicator ("now"/"execute"/"confirm") satisfies the requirement. Ambiguous phrases like "review the draft", "look at this", or "maybe send" **do not** satisfy the requirement.

## Enforcement Mechanisms

### 1. Pre-Send Hook (All Email Actions)
All email-sending scripts (`himalaya send`, `send_draft.sh`, etc.) must validate:
```bash
if [[ "$USER_CONFIRMATION" != *"send" && "$USER_CONFIRMATION" != *"now"* ]]; then
  echo "ERROR: Missing explicit send phrase. Type 'send it' or 'send now' to proceed."
  exit 1
fi
```

### 2. Confirmation Capture in Draft Collaboration
During draft refinement sessions:
- The agent must **explicitly share** the draft content with the user
- The agent must **await** the user's explicit send phrase
- The agent must **log** the confirmation phrase in the session transcript
- The agent must **never auto-append** confirmation or assume intent

### 3. Session-Level Guardrails
- If the user says *"don't send yet"* or *"pause"*, all pending send operations are **paused** and require explicit "send now" to resume
- If a send operation is attempted without explicit confirmation, it is **blocked** and the user is notified with:  
  `"Action denied: Missing explicit send phrase. Type 'send it' or 'send now' to proceed."`

### 4. Post-Send Verification
After sending:
- The agent must **confirm** with the user:  
  `"✅ Email sent to [recipient]. Confirm if correct or 'undo' to reverse."`  
- If the user says "undo", the agent must attempt to retract via available email recall mechanisms (if supported) or mark for follow-up correction

## How This Integrates with Skills

- **`email-ops`**: Central hub that enforces this policy across all email workflows
- **`himalaya`**: Script wrappers must include the pre-send hook validation
- **`class-level skills`**: Any skill governing email dispatch must reference `email-send-policy.md` in its `references/` directory

## Session Tracking Requirements

- All confirmation phrases must be captured verbatim in session transcripts
- The system must provide a `@send-confirmation` tag in transcripts for easy review
- Undo requests must be routed to the appropriate recovery workflow (e.g., `email-recall.sh`)

This policy ensures that email dispatch remains a **deliberate, user-approved action** rather than an automated or accidental outcome.