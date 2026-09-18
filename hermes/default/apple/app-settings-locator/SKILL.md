---
name: app-settings-locator
description: Locate macOS app settings via container paths.
title: App Settings Locator
---

## Workflow
1. **Check Standard Application Directory**  
   - Look in `/Applications/<App>.app/Contents/` for `Info.plist` and resources.

2. **Search User Containers**  
   - Check `~/Library/Containers/` for sandboxed apps (e.g., `com.openai.codex`).  
   - Within containers, search `Application Support/` and `Library/Application Support/`.

3. **Search Application Support Directories**  
   - Check `~/Library/Application Support/` for vendor-specific folders.  
   - Target `Preferences`, `Default/`, and `Secure Preferences` files.

4. **Read Configuration Files**  
   - Common formats: JSON, plist, YAML.  
   - Use `read_file` with offset/limit for large files.

## Example: OpenAI Codex
- **Preferences**: `~/Library/Application Support/Codex/Default/Preferences`  
- **Secure Preferences**: `~/Library/Application Support/Codex/Default/Secure Preferences`  
- **Account Data**: `~/Library/Application Support/Codex/Default/Account Web Data`

## Support Files
- `references/macos-app-settings-examples.md` — Common location patterns.  
- `scripts/locate-app-settings.sh` — Automated search script.