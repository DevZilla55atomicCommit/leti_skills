---
name: vault-mapping-audit
description: Audit vault mapping for missing duplicate indexes.
---
## Triggers
- User requests a vault structure audit
- User flags missing or duplicate mapping indexes
- User reports sync conflicts in mapping files
- User corrects mapping approach
- Vault organizer validation reports high broken wikilink/orphan counts

## Audit Report Format
Return findings as concise bullet points:
- Missing root INDEX.md files (Fusion, Post_Production)
- Duplicate index files (DZ95PwrBsCQ exists in two locations)
- Sync conflict files to delete
- Empty support folders (Audio & Sound)
- Corrupt tags/index.md binary
- 868 loose files needing folder classification
- Validation logic pitfalls (graphify path, analysis/... patterns, orphan scope)

## Sample Report
- 🔴 Missing `/Fusion/INDEX.md` (75+ files)
- 🔴 Missing `/Post_Production/INDEX.md` (98 files)
- 🟡 Duplicate `/DZ95PwrBsCQ/` folder
- 🟡 Empty `/Videographer/Audio & Sound/`
- 🟡 Corrupt `/tags/index.md` binary
- 🟡 868 loose files in `/Color Grading & Looks/`
- 🟡 Validation: graphify binary path wrong (fixed 2026-08-10)
- 🟡 Validation: 11K+ false broken wikilinks from analysis/... patterns (fixed)
- 🟡 Validation: 18K+ false orphans from over-broad counting (fixed)

## Reference Findings
See `references/vault-audit-findings.md` for latest audit report format and action items.
See `references/vault_organizer_validation.md` for validation logic pitfalls and fixes.