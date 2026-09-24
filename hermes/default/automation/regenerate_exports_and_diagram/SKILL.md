---
title: Regenerate Exports and Architecture Diagram
description: Generate structured exports of all creative‑skill documentation and a Mermaid architecture diagram after batch completion.
category: automation
name: regenerate_exports_and_diagram
---

# Regenerate Exports and Architecture Diagram

**Trigger**: When the task list item "**Regenerate JSON/CSV exports and architecture diagram after all batches complete**" is marked **completed**.

**Purpose**: Produce three artifacts:
- `skills_export.json` – machine‑readable list of all creative‑skill metadata.
- `skills_export.csv` – spreadsheet version of the same data.
- `ARCHITECTURE_DIAGRAM.md` – Mermaid graph visualizing folder relationships and key categories.

## Steps
1. Navigate to the vault root: `cd "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base"`.
2. Run `python3 scripts/generate_skills_json.py` → creates `skills_export.json`.
3. Run `python3 scripts/generate_skills_csv.py` → creates `skills_export.csv`.
4. Run `python3 scripts/generate_architecture_diagram.py` → creates `ARCHITECTURE_DIAGRAM.md`.
5. Verify each file exists and contains non‑empty content.

## Pitfalls
- Paths contain spaces; always quote them.
- Ensure the `hermes-tools` package is installed (`pip install hermes-tools`).
- Overwrites occur without backup; consider archiving previous exports.

## Verification
- Check file sizes (> 0) and updated timestamps.
- Open `ARCHITECTURE_DIAGRAM.md` to confirm the Mermaid diagram renders.
- Run `head -5` on the JSON and CSV to ensure they are not empty.

## Support Files
- `references/regenerate_exports_and_diagram.md` – session‑specific notes, command logs, and error transcripts.
- `templates/generate_exports_template.sh` – optional one‑click wrapper script.
- `scripts/generate_skills_json.py` – script used for JSON export.
- `scripts/generate_skills_csv.py` – script used for CSV export.
- `scripts/generate_architecture_diagram.py` – script used for diagram generation.

This skill should be invoked automatically when the final batch‑completion item is marked done, ensuring the knowledge base stays current.