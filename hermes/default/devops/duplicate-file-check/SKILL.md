---
name: duplicate-file-check
category: devops
description: Detect duplicate files by content hash and verify that a virtual environment remains consistent after modifications.
---
# Duplicate File Check

This skill checks for duplicate files within a directory by content hash and helps ensure a virtual environment remains consistent after modifications.

## Steps

1. Run `scripts/duplicate-check.sh <directory>` to list duplicates.
2. Verify each group by running a test command (e.g., `python3.14 --version`).
3. Remove or consolidate duplicates as needed.

## Reference

See `references/duplicate-file-check.md` for details.