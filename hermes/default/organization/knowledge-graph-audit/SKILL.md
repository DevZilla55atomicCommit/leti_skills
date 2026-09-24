---
name: knowledge-graph-audit
description: Fix cross-links and indexes in DaVinci Knowledge Base
---
This class-level skill maintains structural integrity of the DaVinci Knowledge Base by:
- Verifying bidirectional links between every subfolder's `00-MASTER-INDEX.md` and `Memory.md`
- Scanning for misplaced files (e.g., DZ95PwrBsCQ) and moving them to correct locations
- Tracking "blue-marked" priority subfolders that require special attention
- Running verification queries against the knowledge graph
- Generating remediation tasks when structural issues are found

## Terminology
- **Blue-marked subfolders**: Designated priority items requiring manual review or special handling based on vault architecture patterns

## Execution Mode
Run via `task/audit-knowledge-graph` cron job triggered weekly or on demand