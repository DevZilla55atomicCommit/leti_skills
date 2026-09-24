---
name: react-native-app-setup
description: Initialize Expo RN project with navigation.
phases:
  - repo_init
  - expo_create
  - nav_install
  - app_write
  - sanity_check
---

**Goal**: Quickly spin up a new Expo project with navigation.

## Steps

1. **Repo Init**
   ```bash
   cd ~/Dev && git init MyFirstApp && cd MyFirstApp
   ```

2. **Expo Create**
   ```bash
   npx create-expo-app@latest app --template blank-typescript
   ```

3. **Navigation Install**
   ```bash
   cd app && npx expo install @react-navigation/native @react-navigation/native-stack react-native-screens react-native-safe-area-context
   ```

4. **App Code**
   Replace `App.tsx` with the counter + navigation example (see `templates/App-example.tsx`).

5. **Sanity Check**
   ```bash
   npx expo start --no-dev
   ```
   Scan QR with Expo Go to verify the app runs.

**Key Notes**
- Avoid `expo doctor`; it’s not supported locally.
- All commands are idempotent; re-run safely.
- Project lives in `~/Dev/MyFirstApp/app`.