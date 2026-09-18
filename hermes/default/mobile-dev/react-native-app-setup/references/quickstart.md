# Expo React Native Quickstart

- Initialize repo: `git init ~/Dev/MyFirstApp && cd ~/Dev/MyFirstApp`
- Create project: `npx create-expo-app@latest app --template blank-typescript`
- Install navigation: 
  ```bash
  cd app && npx expo install @react-navigation/native @react-navigation/native-stack react-native-screens react-native-safe-area-context
  ```
- Add `App.tsx` (counter + navigation). Replace existing file.
- Run: `npx expo start --no-dev` and scan QR with Expo Go.
- Project root: `~/Dev/MyFirstApp/app`.

**Common Pitfalls**
- `expo doctor` is not supported on macOS; ignore errors.
- If `npx` fails, ensure Node is installed via Homebrew (`brew install node`).
- When Expo warns about deprecated UUID, it’s safe to ignore.