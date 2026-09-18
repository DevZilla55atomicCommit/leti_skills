# Vault Maintenance Protocol

## Overview
Systematic process for ongoing vault health maintenance, including:
- Quarterly structural audits
- Index chain verification
- Metadata consistency checks
- Automated cleanup triggers

## Phase 1: Weekly Health Check
1. Run `script/verify-structure.js` to validate:
   - Folder hierarchy integrity
   - Index file presence
   - Link chain continuity
2. Check for:
   - Sync conflict files
   - Empty discipline folders
   - Missing indices

## Phase 2: Monthly Deep Maintenance
1. Execute `script/rebuild-indices.js` to regenerate all master indices
2. Run `script/verify-links.js` to validate cross-references
3. Clean up:
   - Orphaned files
   - Duplicate artifacts
   - Broken link chains

## Phase 3: Quarterly Structural Review
1. Run `script/vault-audit.js` for comprehensive drift detection
2. Update master mapping chains
3. Adjust collection mappings as needed

## Support Files
- `templates/vrf-index-template.md` - Standard index template
- `scripts/vrf-audit.js` - Metadata validation and conflict detection
- `scripts/vrf-rebuild-indices.js` - Master index regeneration
- `scripts/vrf-verify-links.js` - Cross-reference verification

## Execution Triggers
- "Run vault health check"
- "Maintain vault structure"
- "Fix indexing issues"
- "Rebuild master indices"