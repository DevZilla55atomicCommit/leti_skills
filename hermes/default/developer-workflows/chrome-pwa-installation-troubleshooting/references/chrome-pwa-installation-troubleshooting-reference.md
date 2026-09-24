# Chrome PWA Installation Reference

## Preference Check

Verify Chrome's `Preferences` file at `~/Library/Application Support/Google/Chrome/Default/Preferences`:

```json
{
  "web_app": {
    "https://www.youtube.com/?feature=ytca": {
      "installed": false,
      "install_source": 27,
      "install_timestamp": "13367023977315485"
    }
  },
  "web_app_ids": {}
}
```

- If `"installed": false` and the app's web_app_id is missing from `web_app_ids`, the app is not registered in the new PWA system.

## Verification Commands

1. Check app ID entry:
   ```bash
   grep -A5 '"agimnkijcaahngcdmfeangaknmldooml"' ~/Library/Application\ Support/Google/Chrome/Default/Preferences
   ```

2. Look for `web_app` section and `web_app_ids` keys.

## Solution Summary

- Delete legacy app: `rm -rf ~/Applications/Chrome\ Apps.localized/YouTube.app`
- Reinstall via Chrome as PWA to register in `web_app_ids`.
- Verify with `chrome://apps` that `installed: true`.