# Vault Restructuring Protocol

## Overview
This protocol documents the step-by-step process for systematically resolving structural drift in an Obsidian vault by auditing content, reorganizing based on metadata, and ensuring consistent indexing.

## Phase 1: Initial Audit
1. Run `search_files` with appropriate patterns to identify all relevant files
2. Examine each file's frontmatter using `read_file` to extract metadata
3. Map current location vs expected location based on:
   - Collection categories
   - Discipline classifications
   - Metadata-driven routing rules
4. Identify:
   - Orphaned files (no directory mapping)
   - Duplicate files (multiple copies)
   - Empty discipline folders
   - Broken link chains

## Phase 2: Conflict Resolution
### P0 Priority (Immediate Cleanup)
- Delete Syncthing conflict files (timestamped)
- Remove duplicate artifacts from known duplication zones (e.g., Post_Production/DZ95PwrBsCQ/)
- Delete empty discipline folders
- Remove path duplication in folder names

### P1 Priority (Index Restoration)
- Regenerate all MASTER_INDEX.md files with proper structure
- Verify cross-reference integrity across link chains
- Ensure all priority folders have complete index files

## Phase 3: Reorganization
1. Move files to appropriate subdirectories based on metadata classification
2. Update all affected index files to maintain bidirectional link integrity
3. Rebuild tag indexes and summary tables
4. Validate structural consistency across all priority levels

## Phase 4: Verification
1. Run comprehensive audit of all paths, links, and mappings
2. Confirm no orphaned files remain
3. Verify master mapping chain integrity
4. Ensure cross-reference chains are bidirectional

## Support Files
- `templates/vrf-index-template.md` - Standard index template
- `scripts/vrf-audit.js` - Metadata validation and conflict detection

## Execution Notes
- Requires explicit user context specifying vault root and current structural issues
- Preferred execution triggers: "Fix vault structure", "Reorganize these folders", "Make indexing consistent"