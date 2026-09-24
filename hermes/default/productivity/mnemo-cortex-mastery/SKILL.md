---
name: mnemo-cortex-mastery
description: Core protocols for managing multi-layered and persistent knowledge within the Obsidian Vault.
tags: [memory, obsidian, workflow]
---

# Mnemo Cortex Mastery

This skill governs the lifecycle of information processed during our collaborative work. It ensures that no high-value fact is lost to "context decay" by enforcing a three-layer memory architecture.

## The Three Pillars of Memory Persistence

1.  **Source of Truth (The Raw Data)**
    *   Captures every discrete raw fact encountered (`mnemo_act`, `concept_capture`).
    *   Data is stored as structured Markdown files in the `mnemo-cortex/` folder.
    *   Every "Fact Saved" message from the Agent must correspond to a `write_file` operation here.

2.  **Compiled View (The Wiki Layer)**
    *   Synthesizes raw data into coherent, human-readable knowledge articles.
    *   Used for multi-session context where looking at 10 individual facts is less efficient than one "Knowledge Chapter."

3.  **Active Context (Brain Files)**
    *   Manages the volatile, short-term state of current project iterations.
    *   Registers goals, constraints, and intermediate outputs for the current session's active "Why" and "How."

## Execution Protocol

When discovering a critical fact or rule during work:
1.  Identify the Fact/Truth (Entity + Attribute = Value).
2.  Locate the relevant vault directory (usually `mnemo-cortex` or product-specific folders).
3.  Execute a `write_file` to preserve the fact.
4.  Report "Fact Saved" as confirmation of the physical file operation.

## Reference: Quick Reference Table
| Layer | Purpose | Storage Category | Format |
| :--- | :--- | :--- | :--- |
| **Raw** | Discrete Facts | `mnemo-cortex/` | Individual MD files |
| **Compiled** | Synthesis/Wiki | Knowledge Subfolders | Categorized Articles |
| **Active** | Short-term focus | Brain Files / Task Lists | Project Plans |
