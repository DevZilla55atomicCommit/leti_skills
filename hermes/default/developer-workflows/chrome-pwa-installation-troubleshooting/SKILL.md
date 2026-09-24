---
name: chrome-pwa-installation-troubleshooting
description: Troubleshoot Chrome PWA installation issues where apps open as tabs instead of standalone windows
category: developer-workflows
tags: [chrome, pwa, macos, troubleshooting]
---

# Chrome PWA Installation Troubleshooting

## Problem
Installed Chrome PWAs open as regular tabs instead of standalone windows.

## Root Cause
Legacy `.app` bundles aren't registered in Chrome's new PWA system; missing entry in `web_app_ids` leads to "No suitable profile found". App Translocation can corrupt existing installations, requiring a fresh setup.

## Diagnosis
1. Check Chrome Preferences at `~/Library/Application Support/Google/Chrome/Default/Preferences`.
2. Search for your app's ID (e.g., `agimnkijcaahngcdmfeangaknmldooml` for YouTube).
3. Verify `"installed": false` and missing from `web_app_ids`.

## Solution
### Recommended: Fresh Install & PWA Creation
```bash
# 1. Remove any old/partial install
rm -rf ~/Applications/Chrome\ Apps.localized/ || true

# 2. Download fresh Chrome
cd /tmp && \
curl -L -O https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg && \
hdiutil attach chrome.dmg -nobrowse -quiet && \
cp -R "/Volumes/Google Chrome/Google Chrome.app" /Applications/ && \
hdiutil detach "/Volumes/Google Chrome" -quiet

# 3. Verify installation
open "/Applications/Google Chrome.app" && sleep 2 && ps aux | grep -i "Google Chrome" | grep -v "Helper" | grep -v grep
```

### Create the PWA Properly
1. Open Chrome and go to the target site (e.g., `https://www.youtube.com`).
2. Click the **install icon** (monitor with down arrow) or go to **More tools → Create shortcut...**.
3. Enable **Open as window** and name it (e.g., "YouTube").
4. Click **Create**.

### Verification
- Check `chrome://apps` – status should show `installed: true`.
- Launch the app; it opens as a standalone window, not a tab.

## Pitfalls
- **Avoid legacy bundles** – Chrome shim only works with PWA-registered apps.
- **App Translocation**: Always verify `/Applications` contains the correct bundle.
- **App Mode**: Enable "Open as window"; otherwise it opens as a tab.

## Tips for Alfred
- Provide concise, direct instructions; avoid verbose preamble.
- Use bullet points and code snippets for clarity.