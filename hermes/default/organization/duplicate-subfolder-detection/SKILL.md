---
name: duplicate-subfolder-detection
description: Detect duplicate subfolder structures.
category: organization
tags:
  - vault-audit
  - duplicate-detection
  - folder-structure
---

# Detection Logic
1. Identify matching reel identifiers (filename or INDEX.md title).
2. Cross-reference discipline tags stored in Memory.md.
3. Validate folder classification against the central Memory.md mapping.
4. Flag matches where:
   - Same reel appears in >1 discipline folder.
   - Folder's discipline tag does not align with Memory.md (e.g., Post_Production marked Archive but contains active reels).

# Remediation Steps
- Keep the richer version (typically in Fusion/ with full INDEX.md and detailed tags).
- Remove or archive the stub version in the other discipline folder.
- Update the master index for the archive discipline to reflect the change.
- Add a notes entry in Post_Production/00-MASTER-INDEX.md linking to the retained version.

# Example
- Duplicate: DZ95PwrBsCQ found in both Post_Production/DZ95PwrBsCQ/ and Fusion/DZ95PwrBsCQ/.
- Retained: Fusion/DZ95PwrBsCQ/ (contains full INDEX.md, detailed tags).
- Removed: Post_Production/DZ95PwrBsCQ/ (stub archive entry).

*Suggested cron task:* task/duplicate-subfolder-check to run weekly and surface any new duplicates.