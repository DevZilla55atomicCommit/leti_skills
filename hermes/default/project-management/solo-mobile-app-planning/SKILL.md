---
name: solo-mobile-app-planning
description: Solo mobile app planning system for Alfred – beginner Expo/React Native dev integrating Linear, Obsidian, Figma, local-first, class-level umbrella skill.
category: project-management
---

**Triggers**  
- “planning system for mobile apps”, “organize features”, “setup Linear/Obsidian/Figma”.  
- “daily workflow”, “spec docs”, “design assets”.

**Workflow**  
1. **Linear** – Import templates (Feature, Bug, Chore, Spike). Create project.  
2. **Obsidian** – Use `Feature Spec`, `Screen Spec`, `ADR`, `API Contract` templates.  
3. **Figma** – Follow `planning/figma-setup/README.md` to build Design System, screens, prototypes.  
4. **Initialize App** – `npx create-expo-app@latest app` → set env vars.  
5. **Daily Ops** – Review Linear cycle, update specs, sync Git, preview on device.

**Pitfalls**  
- Over‑engineering early; keep templates minimal.  
- Forgetting Obsidian Git sync; check regularly.  
- Not linking Linear → Obsidian → Figma; maintain front‑matter URLs.

**Support Files**  
- `references/planning-workflow.md` – step‑by‑step checklist.  
- `templates/Feature Spec.md` – spec scaffold.  
- `templates/Screen Spec.md` – screen scaffold.  
- `scripts/check-plan-sync.sh` – verifies syncs.

**Maintenance**  
- Update references after iterations.  
- Quarterly template review.  
- Keep Linear/Obsidian/Git URLs current.

Example usage: skill_manage(action='create', name='solo-mobile-app-planning', category='project-management', content='…')