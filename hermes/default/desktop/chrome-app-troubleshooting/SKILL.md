---
name: chrome-app-troubleshooting
description: |
  Troubleshooting Chrome app installations on macOS, including App Translocation, web_app_ids verification, and launch via \`--app\` flag.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [chrome, troubleshooting, app-installation, desktop]
    category: desktop
    related_skills: [computer-use]
---

# Chrome App Installation Troubleshooting

## Overview

When Chrome apps fail to install or launch properly, often due to App Translocation or missing registration in Chrome's internal tracking.

## Troubleshooting Steps

1. **Check App Bundle Existence**: Verify the app exists in `~/Applications/Chrome Apps.localized/`.
2. **Validate Web App IDs**: Ensure the app's ID appears in Chrome's `web_app_ids` preference.
3. **Test Direct Launch**: Use Chrome's `--app` flag with the correct `--user-data-dir` to launch the app.
4. **App Translocation Handling**: If the app is in a Translocated path, either copy it to `/Applications` or reference it directly via its full path.

## Verification

After following these steps, launch the app to confirm it opens in app mode rather than a browser tab.

## Related Skills

- `computer-use`: For driving the desktop and automating app launches.
- `browser`: For web-related interactions.

## References

- Internal troubleshooting guide: `references/chrome-app-troubleshooting.md`