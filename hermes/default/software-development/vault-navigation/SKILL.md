---
name: vault-navigation
description: Commands and protocols for navigating and querying the internal project structure of the TamaZila Obsidian Vault.
trigger: Queries regarding "the vault", its directory structure, or content retrieval from specific locations within it.
---

# Vault Navigation

## Overview
This skill governs all interactions with the `TamaZila Obsidian Vault` located at `/Users/alfredkamisese/TamaZila Obsidian Vault`. Its primary purpose is to ensure that questions about "the vault" are scoped strictly to this directory and handled with consistent formatting.

## Core Protocols
1.  **Scoped Search:** Every time a user asks for information from "the vault," you MUST restrict all tool calls (terminal, search_files, read_file) to the vault's root directory. Do not allow these queries to bleed into system-level files or other project directories unless explicitly requested.
2.  **Structure Discovery:** 
    *   To get a clear overview of folders and files without being overwhelmed by hidden files or noise, use:
        `find "/Users/alfredkamisese/TamaZila Obsidian Vault" -maxdepth 3 -not -path '*/.*'`
    *   Adjust `-maxdepth` as needed based on the depth of the requested branch.
3.  **Content Analysis:** When identifying specific files for modification or review, use `search_files` with `target='content'` to find relevant matches within the vault's subdirectories.

## Pitfalls
- **Broad Scope Leakage:** Avoid running commands like `find / -name *` or searching without specifying the `path` parameter. Always append the full path `/Users/alfredkamisese/TamaZila Obsidian Vault`.
- **Noise in Listing:** Standard `ls` or `find` can include hidden files (like `.obsidian`). Use `-not -path '*/.*'` to ensure a clean view of the actual vault content.

## Verification
When listing the vault structure, confirm that all returned paths start with `/Users/alfredkamisese/TamaZila Obsidian Vault`.

## Reference Files
- `references/hermes-agent-folder-map.md` — Complete structure map of the Hermes Agent subfolder with all Memory.md navigation files and key entry points.
