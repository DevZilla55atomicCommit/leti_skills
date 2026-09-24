---
name: vault-backup-management
title: Vault Backup Management
description: Manages automated vault backups with delta scanning.
tags:
  - vault
  - backup
  - automation
---
This skill manages automated Obsidian vault backups with delta scanning capabilities.

## Overview
Creates timestamped snapshots before organizational changes, enabling efficient delta scanning for subsequent runs.

## Core Workflow
1. **Pre-Run Backup**: Creates compressed rsync snapshot of entire vault
2. **Delta Manifest**: Generates file hash manifest for efficient comparison
3. **Incremental Backups**: Subsequent runs only copy changed files
4. **Retention Policy**: Configurable retention (default: 30 days / 10 backups)

## Shell Commands
- `vault-backup create --max-moves 10`: Create backup and generate manifest
- `vault-backup prune --keep-days 30`: Remove old backups
- `vault-backup status`: Show last backup details

## Implementation
- Uses `--apply` flag to trigger actions
- Writes manifest to `.vault-organizer-backups/manifests/`
- Stores run metrics in JSONL state file
- Embeds duration and file count in status report

## User Preferences
- Notify immediately when backup completes with duration
- Use incremental rsync to avoid full re-copy
- Limit backups to last 30 days (adjustable)
- Clear status reporting with backup path and file count

## Support Files
- `references/backup-workflow.md` - Backup workflow documentation
- `references/actual-backup-structure.md` - Discovered backup locations & existing runs