# Regenerate Exports and Architecture Diagram — Session Reference

**When to run**: After the task list item **Regenerate JSON/CSV exports and architecture diagram after all batches complete** is marked **completed**.

## Commands Executed
1. `cd "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base"`
2. `python3 scripts/generate_skills_json.py` → creates `skills_export.json`
3. `python3 scripts/generate_skills_csv.py` → creates `skills_export.csv`
4. `python3 scripts/generate_architecture_diagram.py` → creates `ARCHITECTURE_DIAGRAM.md`

## Verification Outputs
- **skills_export.json** – 159 skill entries, 92 KB file size
- **skills_export.csv** – 159 skill entries, 46 KB file size
- **ARCHITECTURE_DIAGRAM.md** – Mermaid diagram with 23 folder nodes and ~70 file links

## Common Pitfalls
- Paths contain spaces → always quote them.
- Ensure `hermes-tools` package is installed (`pip install hermes-tools`).
- Overwrites are unbacked → consider archiving previous exports before re‑running.

## Follow‑up
- Update skill `regenerate_exports_and_diagram` if new export formats or diagram styles are introduced.
- Add additional reference links to error transcripts or provider docs as needed.