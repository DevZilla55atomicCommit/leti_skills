---
name: interview-workflow
type: skill
description: Captures the structured questioning pattern used to configure user preferences for vault setup.
status: active
tags: [interview, workflow, preferences]
---

# Interview Workflow

This skill documents the pattern of sequential questioning used to gather user preferences for configuring the EMAI Starter Vault.

## Trigger Conditions
- User initiates vault setup workflow
- User expresses need for quick path or workflow focus
- Agent needs to establish user's current projects and priorities

## Question Pattern
1. **Scope Identification** - "What are you actually working on right now?"
2. **Time Horizon Focus** - "What matters most over the next 30 days?"
3. **Project Context** - "What projects or responsibilities should this vault keep in view?"
4. **Planning Style** - "How do you want /today to plan your days — focused, balanced, or aggressive?"
5. **Priority Structure** - "How many true priorities do you want in a normal day?"
6. **Time Allocation** - "Do you want suggested time blocks, or just a priority list?"
7. **Avoidance Pattern** - "What counts as a 'frog' for you — overdue tasks, avoided tasks, admin, or something else?"

## Configuration Outputs
- `user-preferences.quick-path`: true/false
- `user-preferences.workflow-focus`: list of domains
- `user-preferences.planning-style`: string
- `user-preferences.priority-count`: integer
- `user-preferences.time-blocks`: boolean
- `user-preferences.frog-definition`: string

## Example Session
[session transcript excerpt]
## Pitfalls & Fixes

- **Pitfall**: Moving too fast through questions without confirming understanding
  **Fix**: Pause after each answer and summarize before proceeding

- **Pitfall**: Assuming priority count must be fixed or that time blocks are required
  **Fix**: Honor user preference for dynamic priority count (“as many as needed”) and no time blocks; reflect this in Configuration Outputs

- **Pitfall**: Misinterpreting "quick path" as "no interview"
  **Fix**: Clarify that /interview remains the entry point even for speed-focused users; still captures full preference set

- **Pitfall**: Skipping the "frog" definition
  **Fix**: Always capture avoided/overdue task definitions to enable proper task prioritization; user specifically defined frogs as avoided and overdue tasks

## Related Skills
- vault-setup
- hermes-agent
- task-priority-engine