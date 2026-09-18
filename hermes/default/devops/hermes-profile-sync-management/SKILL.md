---
name: hermes-profile-sync-management
description: "Hermes profile sync across machines, isolate configs."
trigger: "Need to sync Hermes configs across machines via Syncthing, isolating per-machine settings."
tags: [devops, hermes, syncthing, profile-management]
---
# Hermes Profile Sync Management

## Trigger
When you have multiple machines accessing the same Syncthing-shared directory `~/.hermes/profiles/` and need to:
- Keep **shared memories** synchronized
- **Isolate** machine‑specific configurations (e.g., Ollama endpoints, API keys, model lists)
- Prevent conflicts that cause model mismatches or failed provider connections

## Core Principle
> **Sync memories, not configs.**  
Shared memories safely persist across machines. Machine‑specific settings must remain local to avoid runtime mismatches.

## Workflow (Recommended: Option A – Split Sync)
1. **Identify what to sync**  
   - ✅ `memories/` – shared knowledge, user profile, memory snippets  
   - ❌ `config.yaml` – machine‑specific endpoints, API keys, model lists  

2. **Update `.stignore` to exclude `config.yaml`**  
   ```bash
   echo "config.yaml" >> ~/.hermes/profiles/.stignore
   ```

3. **Maintain separate `config.yaml` per machine**  
   - Edit locally on each machine to reflect its Ollama endpoint (`http://127.0.0.1:11434/v1`) and model list.  
   - No sync – each machine keeps its own copy.

4. **Verify isolation works**  
   - Launch Hermes on each machine and confirm it loads the correct provider settings.  
   - Check `~/.hermes/profiles/default/config.yaml` on each machine reflects the correct Ollama URL and models.

## Integration with Other Skills
- Use **`memory-management/step-beyond-memory-sync`** to monitor sync health.  
- Consult **`devops/hermes-agent-config`** for deeper profile configuration patterns.  
- Apply **`devops/environment-variable-templating`** if you want a single config.yaml that resolves `${OLLAMA_HOST}` at runtime.

## Updates & Maintenance
- Re‑run the checklist after any Hermes upgrade or Syncthing version change.  
- Add new machine‑specific fields to `.stignore` promptly when they appear in `config.yaml`.  
- Document any new provider‑specific secrets in the **`references/`** folder of this skill.