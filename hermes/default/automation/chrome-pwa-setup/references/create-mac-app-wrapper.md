# Creating a native macOS .app Wrapper for a CLI Tool (e.g., Syncthing)

This guide documents the manual steps taken to turn a background service into a double-clickable `.app` bundle that opens the web UI.

## Steps

1. **Create the `.app` directory structure**:
   ```
   mkdir -p /Applications/<AppName>.app/Contents/{MacOS,Resources}
   ```

2. **Write `Info.plist`** with required keys (`CFBundleExecutable`, `CFBundleIdentifier`, `CFBundleName`, `CFBundleVersion`, `LSUIElement = true`).

3. **Create an executable wrapper script** in `Contents/MacOS/<AppName>` that:
   - Ensures the service is running (via `launchctl` if needed).
   - Waits for the web UI to be ready.
   - Opens the target URL in the default browser (`open <url>`).

4. **Make the script executable**:
   ```
   chmod +x /Applications/<AppName>.app/Contents/MacOS/<AppName>
   ```

5. **(Optional) Add an icon**:
   - Copy a system icon or custom `.icns` file into `Resources/icon.icns`.
   - Add `<key>CFBundleIconFile</key><string>icon</string>` to `Info.plist`.

6. **Register as a Launch Agent** (if not already):
   - Place `~/Library/LaunchAgents/com.syncthing.syncthing.plist` with appropriate `Label` and `ProgramArguments`.

7. **Result**:
   - Double-clicking `<AppName>.app` in Finder launches the wrapper, which opens the web UI.
   - The underlying service continues to run in the background.

## Reusable Script (optional)

A minimal shell script (`create_url_app.sh`) can be adapted to automate this process for any CLI tool that needs a URL opener.