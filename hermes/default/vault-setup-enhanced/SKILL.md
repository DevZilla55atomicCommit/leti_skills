---
name: vault-setup-enhanced
description: Guide to set up Obsidian vault for mobile app projects.
type: skill
status: active
tags: [vault, setup, obsidian, mobile-app, workflow]
---

# Enhanced Vault Setup – Session‑Specific Steps

## 1. Initialize Vault
```bash
mkdir -p ~/Dev/obsidian-vault
open ~/Dev/obsidian-vault
```

## 2. Add Core Folders
| Folder | Purpose |
|--------|---------|
| `00 Human/` | Personal notes, tasks, projects |
| `Machine/` | AI‑generated content, workflows, script outputs |
| `System/` | OS documentation, configuration files |

```bash
mkdir -p ~/Dev/obsidian-vault/00\ Human
mkdir -p ~/Dev/obsidian-vault/Machine
mkdir -p ~/Dev/obsidian-vault/System
```

## 3. Symlink Supporting Directories
```bash
ln -sfn "$HOME/TamaZila Obsidian Vault/Claude Code" "$HOME/Dev/obsidian-vault/Claude Code"
ln -sfn "$HOME/TamaZila Obsidian Vault/Hermes Agent" "$HOME/Dev/obsidian-vault/Hermes Agent"
```

## 4. Create App‑Development Sub‑folder
```bash
mkdir -p ~/Dev/obsidian-vault/App\ Development
ln -sfn "$HOME/Dev/MyFirstApp" "$HOME/Dev/obsidian-vault/App Development/MyFirstApp"
```

## 5. Populate Core Templates
```bash
cp "$HOME/Dev/obsidian-vault/templates/Feature\ Spec.md" "$HOME/Dev/obsidian-vault/App\ Development/Templates/"
cp "$HOME/Dev/obsidian-vault/templates/Screen\ Spec.md" "$HOME/Dev/obsidian-vault/App\ Development/Templates/"
cp "$HOME/Dev/obsidian-vault/templates/ADR.md" "$HOME/Dev/obsidian-vault/App\ Development/Templates/"
cp "$HOME/Dev/obsidian-vault/templates/API\ Contract.md" "$HOME/Dev/obsidian-vault/App\ Development/Templates/"
cp "$HOME/Dev/obsidian-vault/templates/Research.md" "$HOME/Dev/obsidian-vault/App\ Development/Templates/"
```

## 6. Verify Setup
```bash
cd "$HOME/Dev/obsidian-vault/App\ Development" && ls -la
```

You should see the linked directories and the `MyFirstApp.md` index note.

## 7. Verify Template Files
```bash
ls -la "/Users/alfredkamisese/Dev/obsidian-vault/App Development/templates" && cat "/Users/alfredkamisese/Dev/obsidian-vault/App Development/templates/Feature Spec.md" | head -n 5
```

## 7. Daily Workflow Integration
- **Linear:** Create Feature/bug/spike issues directly from Obsidian using the `/linear` command (via the Linear CLI integration).
- **Obsidian:** Use Cmd+N → “Feature Spec” template to capture new feature ideas.
- **Figma:** Follow the guide in `planning/figma-setup/README.md` for design‑system frames.
- **Expo:** Run `npx expo start` to verify the React Native dev server.

## 8. Support Files (linked from this skill)
- `references/setup-steps-enhanced.md` — this file
- `templates/vault-config.yaml` — example configuration for EAS builds
- `scripts/verify-setup.sh` — simple verification script