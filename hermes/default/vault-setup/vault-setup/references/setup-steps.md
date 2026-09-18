# EMAI Vault Setup Steps (Updated)

## Quick Start
1. Extract the EMAI Starter Vault folder.
2. In Obsidian, open the folder as a new vault.
3. Wait for the 17 pre-configured community plugins to load.
4. Verify the following directories exist:
   - `00 Human/`
   - `Machine/`
   - `System/`
5. From the vault root, run `/start` in your AI harness.

## Linear Integration
1. In Linear, create a Cycle (e.g., Cycle 1) and set the dates and duration.
2. Give the Cycle a name that reflects your sprint (e.g., “Sprint 1”).
3. In Obsidian, go to the `Machine/Cycles/` folder and create a note linking to the Linear Cycle.
4. Use the `/interview` command to personalize the vault for sprint tracking.

## Verification
- Confirm the Linear Cycle appears as a linked note in Obsidian.
- Run `/start` and ensure it completes without errors.

## Common Issues
- Plugin loading errors: wait a moment or restart Obsidian.
- CLI timeout problems: increase the timeout setting or verify Ollama connectivity.
- Permission errors: store the vault in a writable location.