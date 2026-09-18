# Installation Checklist for UI/UX Pro Max Skill

Follow these steps to properly install and verify the UI/UX Pro Max skill:

1. **Copy the skill markdown**:
   ```bash
   cp /tmp/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max.md ~/.claude/skills/ui-ux-pro-max.md
   ```

2. **Ensure the scripts directory exists and copy scripts**:
   ```bash
   mkdir -p ~/.claude/skills/ui-ux-pro-max/scripts
   cp -r /tmp/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/scripts/* ~/.claude/skills/ui-ux-pro-max/scripts/
   ```

3. **Ensure the references directory exists and copy references**:
   ```bash
   mkdir -p ~/.claude/skills/ui-ux-pro-max/references
   cp -r /tmp/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/* ~/.claude/skills/ui-ux-pro-max/references/
   ```

4. **Verify the installation by checking the help output**:
   ```bash
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py --help
   ```

5. **Test a design system generation**:
   ```bash
   python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "saas dashboard modern" --design-system -p "My Project" -f markdown
   ```