# Quick Start Patterns for EMAI Vault Optimization

## 1. Minimal Setup Path
- Skip non-essential plugins
- Use pre-configured prompt templates
- Prioritize `/today` over complex setup

## 2. Ollama Configuration
- API endpoint: `http://localhost:11434/v1`
- Model selection:
  - `qwen3.5-32k:latest` for general workflows
  - `phi4:14b` for lightweight verification

## 3. Daily Workflow Templates
- `/today` → Priority list generation
- `/closeday` → Reflective metrics tracking
- `/new` → Brain dump capture

## 4. Verification Checklist
1. All required folders present
2. Core plugins loaded without errors
3. API endpoints responding correctly
4. No identifier conflicts between vaults

## 5. Connection Strategy
- Keep starter vault separate
- Connect via symlinked folders or Obsidian Sync/Git
- Establish connections only when merging is desired

---

**Pattern Origin**: Derived from user preference for quick path, avoidance of administrative overhead, and focus on tooling/infrastructure projects.