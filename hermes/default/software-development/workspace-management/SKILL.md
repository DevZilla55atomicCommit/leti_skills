---
name: workspace-management
description: |
  Professional protocols for organizing and maintaining a clean local development environment, including file system cleanup, folder tiering, and desktop management.
---

## Overview
Use this skill when the user needs to organize their desktop, consolidate directories, or manage project/research files on the local machine (macOS/Linux). This ensures that information is grouped logically by domain (e.g., Development, Education, Media) rather than left as a disorganized list of files.

## Organization Workflow
When asked to "organize" or "tidy up":
1. **Assessment**: Run `ls -la` on the target directory to identify current contents.
2. **Categorization**: Propose a 4-tier category system:
   - **Media & Design** (Graphics, Video clips, LUTs, manual/guides)
   - **Development & AI** (Python scripts, LLM configurations, `.md` docs)
   - **Education & Personal** (BYUI, personal notes, workout logs)
   - **Documents & Administration** (PDFs, Invoices, Official records)
3. **Action**: Create directories and move files via `terminal`.
4. **Documentation**: Generate a summary of the new layout as an `.md` file for the user's records.

## Rules
- Never delete any files without explicit confirmation from the user.
- Always use absolute paths during `mv` operations to ensure reliability.
- Prioritize keeping related folders (e.g., 3-page site content) together even if they are moved to a new parent directory.

## Verified Best Practices
- **Category Mapping**:
  - `.py`, `.js`, `.json`, `.md` files $\rightarrow$ Development & AI
  - `.pdf`, `.docx`, `.xlsx`, `Invoice` $\rightarrow$ Documents & Administration
  - `.png`, `.jpg`, `.mp4`, `LUTs` $\rightarrow$ Media & Design
- **Clean Desktop Policy**: Files like `AboutHisBusiness.pdf` or `RP-Local AI Master Guide.docx` should only live in the main category folders; any files remaining on the desktop after organization are "stray" and deserve a follow-up question to the user.

## Pitfalls
- **IDEs/Hidden Folders**: Do not move `.git`, `.vscode`, or `__pycache__` directories unless requested, as these can break build paths for active projects.
- **System Files**: Never attempt to move system files (from `/Library`, `System`, etc.) during a desktop cleanup.
- **FAT32/exFAT USB volumes sprout `._` sidecars**: macOS writes an AppleDouble `._` file alongside every file on non-APFS mounts, and `msdos`/`exfat` support no symlinks. Exclude `._*` from listings and diffs (`diff -r --exclude='._*'`), and never rely on symlinks or executable bits on those volumes.

## Verification
Check the final directory structure with `ls -R` and confirm the list of top-level categories matches the requested layout.