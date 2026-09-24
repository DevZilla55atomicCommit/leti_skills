---
name: visual-feedback-handling
category: ui
description: Handles visual UI feedback, capture, and presentation.
---

# Visual Feedback Handling Skill

This skill governs how the Hermes Agent interprets and generates visual feedback for user interactions, particularly when:

- The user requests visual artifacts (screenshots, diagrams, UI previews)
- The user desires reactive visualizations tied to system states (e.g., TTS status indicators)
- The user expects JARVIS-like responsive visual cues in the UI

## Trigger Conditions
- User explicitly requests visual confirmation of page state, element interaction, or system status
- User references visual UI patterns (e.g., "JARVIS sphere", "reactive UI")
- User indicates preference for concrete visual output over textual description

## Core Procedures
1. **visual-capture**: Take and annotate screenshots of current browser/desktop state
2. **visual-transform**: Apply overlays, labels, or highlight regions per user request
3. **visual-summarize**: Convert UI state into structured description or diagram format
4. **visual-present**: Deliver visual output through appropriate Hermes viewport (preview pane, screenshots, or external rendering)

## User Preferences Embedded
- **Conciseness**: No filler text, only actionable technical content
- **Directness**: Answer first, explanation only if requested
- **Visual Primacy**: Prefer visual confirmation over textual description when both are available

## Pitfalls Section
- ❌ Never add explanatory prose before the visual artifact
- ❌ Never use vague qualifiers like "as you can see" without accompanying visual
- ❌ Never generate placeholder diagrams without concrete data source
- ✅ Always anchor visual output to specific element refs (@e1, @e12, etc.)