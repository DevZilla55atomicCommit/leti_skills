# Chrome App Installation Troubleshooting Guide

## Overview
This guide provides a comprehensive methodology for diagnosing and resolving Chrome app installation and launch issues on macOS, with specific focus on App Translocation effects and Chrome's internal app registration mechanisms.

## Diagnostic Checklist

### 1. App Bundle Verification
```bash
# Check if app bundle exists
ls -la ~/Applications/Chrome\ Apps.localized/ | grep -i youtube
```
- Verify `.app` bundle presence
- Check Info.plist for proper `CFBundleIdentifier`
- Confirm `CrAppModeUserDataDir` points to correct Chrome profile

### 2. Chrome Preferences Validation
```bash
# Extract web_app_ids to verify registration
defaults read com.google.Chrome WebAppIds
```
- Look for YouTube app ID: `agimnkijcaahngcdmfeangaknmldooml`
- Verify `installed` status in daily_metrics JSON
- Check `web_apps` section for app-specific settings

### 3. App Mode Loader Validation
```bash
# Test direct launch with app_mode_loader
~/Applications/Chrome\ Apps.localized/YouTube.app/Contents/MacOS/app_mode_loader \
  --user-data-dir="/Users/alfredkamisese/Library/Application Support/Google/Chrome/Default" \
  2>&1 | grep -i "profile"
```
- Look for "No suitable profile found" errors
- Verify Chrome profile path accessibility

### 4. App Translocation Handling
```bash
# Identify translocated path
ls -la /private/var/folders/*/*/T/AppTranslocation/
```
- Copy app to `/Applications` if needed:
  ```bash
  cp -R ~/Applications/Chrome\ Apps.localized/YouTube.app /Applications/
  ```
- Alternative: Use direct Chrome binary launch with `--app` flag

### 5. PWA Installation via Chrome UI
1. Navigate to target site (`https://www.youtube.com`)
2. Click browser menu (⋯) → More tools → Create shortcut
3. Enable "Open as window"
4. Confirm installation

### 6. Verification Tests
- Launch app via `--app` flag with proper user-data-dir
- Confirm app opens in dedicated window (not browser tab)
- Check for expected window properties:
  - No address bar
  - App-specific icon
  - Isolated storage

## Common Issues & Fixes

### "No suitable profile found" Error
- Cause: App Translocation breaking profile path
- Fix: Use `/Applications` location or copy user-data-dir to stable path

### App Opens as Browser Tab Instead of App
- Cause: Missing `installed: true` in preferences
- Fix: Manually add app to `web_app_ids` and set `installed: true`

### Launch Crashes or Fails to Start
- Cause: Incomplete App Bundle structure
- Fix: Verify Info.plist contains required keys:
  - `CFBundleIdentifier`
  - `CrAppMode` dictionary with `user_data_dir`
  - `CFBundleExecutable` pointing to `app_mode_loader`

## Advanced Debugging

### Log Collection
```bash
# Capture detailed logs
log show --predicate 'process == "app_mode_loader"' --last 5m > app_mode_debug.log
```

### Profile Migration Tracking
- Check Chrome's `Profile Migration` logs for moved directories
- Verify symlink integrity in `Application Support/Google/Chrome`

### Security & Privacy Permissions
- Ensure "Screen Recording" and "Accessibility" permissions granted
- Check System Preferences → Privacy & Security → Accessibility

## Best Practices
- Always test with `--app` flag before creating desktop shortcuts
- Use stable `/Applications` location for production app bundles
- Monitor `daily_metrics` for installation status changes
- Keep Chrome updated to latest stable version for compatibility