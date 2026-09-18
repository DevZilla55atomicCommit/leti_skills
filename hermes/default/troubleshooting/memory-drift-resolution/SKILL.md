---
name: Memory Drift Resolution
title: Memory Drift Resolution
description: How to resolve drift in USER and MEMORY files in Hermes Agent.
authors: [maddie]
created: 2026-07-12
---

# Memory Drift Resolution

## When to use
When the memory system reports: Refusing to write ... file on disk has content that wouldn't round-trip

## Resolution Steps
1. Identify drift file (e.g., USER.md.bak or MEMORY.md.bak)
2. Manually integrate drift content via memory(action=add, content=...) one entry at a time
3. Delete drift file after successful integration
4. If deletion fails, rewrite original file to clean state via repeated memory(add) calls

## Prevention
- Only use memory tool for updates
- Never manually edit memory files
- Delete .bak files immediately after resolution