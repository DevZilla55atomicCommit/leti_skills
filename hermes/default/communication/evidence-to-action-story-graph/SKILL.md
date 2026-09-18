---
name: evidence-to-action-story-graph
description: "Structure evidence into actionable outputs via 5 layers."
trigger: "Structure evidence into actionable outputs via 5 layers."
---

# Evidence-to-Action Story Graph Skill

## The 5-Layer Pipeline

```
INPUTS > NARRATIVE CORE (Story Spine) > VISUAL TRANSLATION > TRUST LAYER > OUTPUTS
```

---

## Layer 1: Inputs (The Foundation)
Three required inputs before starting:
- **Project records / verified sources** -- Raw data, code, docs, logs, research
- **Audience questions or concerns** -- What the user actually needs to know
- **Communication goal** -- Strategic objective: decide, build, learn, ship, debug

**Preflight check:** Do I have all three? If not, ask.

---

## Layer 2: Narrative Core -- The 6-Element Story Spine
Structure every substantial response through these six elements in order:

| # | Element | Question It Answers | Minimum Viable Output |
|---|---------|---------------------|----------------------|
| 1 | **Hook** | Why this matters | One sentence: stakes/impact |
| 2 | **Context** | What is happening | Current state, constraints, environment |
| 3 | **Mechanism** | How it works | Causal logic, architecture, flow |
| 4 | **Evidence** | What the record establishes | Citations, data, verified facts |
|  | 5 | **Unknowns** | What is proposed, unclear, disputed | Gaps, tensions, decision points |
  | 6 | **Action** | What the audience can do next | Concrete next step, decision, or deliverable |

**Rule:** Never skip an element. If an element has no content, state "None identified" -- don't omit.

---

## Layer 3: Visual Translation -- Tactic Matching
Match each Story Spine element to its visual language:

| Content Type | Visual Tactic | When to Use |
|--------------|---------------|-------------|
| **Scale** | Map, count, comparison, bar/ratio chart | Magnitude, distribution, "how much" |
| **System** | Architecture diagram, blueprint, component graph | "How parts relate", data flow, dependencies |
| **Process** | Timeline, flow chart, sequence diagram | "What happens when", steps, lifecycle |
| **Evidence** | Short excerpt, source tag, number card, screenshot | "Here is the proof", citations, metrics |
| **Unknown** | Question card, decision fork, gap marker | "We don't know this yet", open questions |
| **Action** | Checklist, next-step card, CTA button | "Do this now", concrete tasks |

**Rule:** Build the visual *after* the spine is solid. No decorative charts.

---

## Layer 4: Trust Layer -- Certainty Tagging
Tag every non-trivial claim with exactly one label:

| Tag | Meaning | Use For |
|-----|---------|---------|
| `Verified` | Confirmed by source, test, or direct observation | Facts, test results, docs, code behavior |
| `Proposal` | Suggested path, not yet executed | Recommendations, architecture options, "try this" |
| `Unknown` | Genuine gap, needs investigation | Missing docs, untested assumptions, external deps |
| `Opinion` | Judgment call, trade-off assessment | "Better", "prefer", "cleaner", style choices |

**Rule:** If you can't tag it, you haven't verified it. Tag inline: `The API returns 429s under load [Verified]` / `Switching to gRPC would reduce latency [Proposal]`

---

## Layer 5: Outputs -- Delivery Format Matching
Choose the output format that matches the user's need:

| Format | Best For | Trigger |
|--------|----------|---------|
| **Long-form** | Deep dive, reference doc, skill creation | "Explain fully", "Create a skill", "Document this" |
| **Short-form** | Quick answer, status update, clip | "Summarize", "What's the status", "Give me the TL;DR" |
| **Presentation/Briefing** | Decision meetings, stakeholder sync | "Prepare for review", "Brief the team" |
| **Article/Graphic/Social** | Sharing, publishing, async consumption | "Write this up", "Make a diagram", "Post this" |

---

## Agent Preflight Checklist (Run Before Every Substantial Response)

```
[ ] Inputs gathered? (records, audience concern, goal)
[ ] Story Spine drafted? (all 6 elements, in order)
[ ] Visual tactics assigned? (one per spine element that needs it)
[ ] Trust tags applied? (every claim tagged)
[ ] Output format selected? (matches user need)
```

---

## Integration Notes

- **With coding skills:** Run spine on problem statement before writing code. Mechanism = architecture. Evidence = test results. Unknowns = TODOs.
- **With research skills:** Inputs = sources. Evidence = citations. Unknowns = gaps for next search.
- **With creative skills:** Visual Translation layer IS the creative brief. Match tactic to content type.
- **With delegation:** Brief subagents with the Story Spine -- they return Evidence + Unknowns; you synthesize.

---

## Anti-Patterns to Avoid

- Presenting Evidence before Context (data without setting)
- Skipping Unknowns (false certainty)
- Visuals without spine (decoration over substance)
- Untagged claims (trust ambiguity)
- Wrong output format (long-form when user needs a checklist)