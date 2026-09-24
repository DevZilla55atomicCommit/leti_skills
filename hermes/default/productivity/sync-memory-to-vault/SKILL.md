---
name: sync-memory-to-vault
description: Syncs the local Hermes memory file to a backup in the Obsidian vault.
permissions: [file]
---

# Sync Memory to Vault

This skill ensures that your personal preferences and environment facts are backed up in your primary Obsidian note-taking system.

## Procedure

**Trigger conditions:**
*   Immediately after any `memory(action='add', ...)` or `memory(action='replace', ...)` call.
*   When the user explicitly requests a manual sync.

1.  **Read Source**: Read the content of `~/.hermes/memories/MEMORY.md`.
2.  **Write Destination**: Write the content to `/Users/alfredkamisese/TamaZila Obsidian Vault/Omi/Hermes Memory/MEMORY_BACKUP.md`.
3.  **Verification**: Confirm that the file was written successfully to `/Users/alfredkamisese/TamaZila Obsidian Vault/Omi/Hermes Memory/MEMORY_BACKUP.md` by checking if the file exists and has a non-zero size.
4.  **Pitfall (Security)**: Ensure `Memories.md` in the root of `Omi` remains untouched; it is strictly for identity/personal memory, not technical logs.

## Execution Steps
Use `read_file` and `write_file` to perform the sync.
