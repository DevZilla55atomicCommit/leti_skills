---
name: emai-dashboard-config
description: Export and import EMAI Dashboard config via Settings UI.
category: settings
version: 1.0.0
authors: [Alfred]
---

# EMAI Dashboard Config Export/Import

This skill captures the workflow for exporting the EMAI Dashboard plugin configuration from the
Obsidian Settings UI and importing it into another vault or backup.

## Export

1. Open **Settings** → **Community Plugins** → **EMAI Dashboard** → click the gear icon.
2. In the **Actions** section, click **Export Config**.
3. The file is downloaded to your default download folder (e.g., `~/Downloads/emai-dashboard-config.json`).
4. Move the file to your target vault (e.g., `~/Documents/EMAI/emai-dashboard-config.json`).

## Import

1. Open **Settings** → **Community Plugins** → **EMAI Dashboard** → click the gear icon.
2. Click **Import Config** and select the previously exported JSON file.
3. The plugin configuration is applied.

## Verification

- After import, the plugin settings are reflected in the UI.
- Use **Export Config** again to confirm the round‑trip works.

## Support Files

- `references/export-import-config.md` – detailed step‑by‑step guide.
- `templates/export-config.json` – example JSON skeleton.
- `scripts/check-config.sh` – script to verify the JSON schema.

--- 

**References**
- Export/Import UI located in the EMAI Dashboard plugin settings.