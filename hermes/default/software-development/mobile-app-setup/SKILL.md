---
name: mobile-app-setup
description: Sets up mobile app env with Linear, GitHub, Expo.
triggers: use when setting up a new mobile app project, configuring task tracking, version control, knowledge management, and testing workflow.
---

# Mobile App Setup

This skill orchestrates the full lifecycle of a mobile app development environment on macOS, integrating task tracking, version control, knowledge management, and testing tools.

## Core Components

1. **Task Tracking**: Linear project configuration, issue templates, cycle setup.
2. **Version Control**: GitHub repository initialization, branch protection, PR workflow.
3. **Knowledge Management**: Obsidian vault structure, cross-linking, plugin configuration.
4. **Development Stack**: Expo CLI, React Native, iOS Simulator, Android Emulator, Expo Go.
5. **Design**: Figma for UI/UX, integration with development workflow.
6. **Automation**: Scripts for common tasks, verification, and CI pipelines.

## Trigger Conditions

- Starting a new mobile app project
- Configuring Linear for a new app
- Setting up a new GitHub repository for mobile app
- Initializing an Obsidian vault with appropriate structure.
- Configuring Expo CLI and installing dependencies.
- Adding design assets from Figma.

## Prerequisites

- Node.js (v20+)
- npm/yarn
- Expo CLI
- Git
- Linear account
- GitHub account
- Obsidian installed
- Figma account (optional but recommended)

## Typical Workflow

1. Create GitHub repo and clone locally.
2. Initialize Linear project and link repository.
3. Set up Obsidian vault with appropriate structure.
4. Configure Expo CLI and install dependencies.
5. Set up iOS/Android testing environments.
6. Add Figma integration for design assets.
7. Create CI scripts for builds and tests.

## Common Pitfalls

- Missing `ios.bundleIdentifier` in `app.json` → causes Expo start failure.
- Forgetting to install `react-dom` and `react-native-web` for web support.
- Not linking GitHub SSH keys → push failures.
- Incorrect bundle identifier format → App Store submission issues.
- Using Expo Web without web dependencies → runtime errors.

## Support Files

- `references/quickstart.md` — Quick reference checklist.
- `templates/expo-start.command` — Boilerplate script to start Expo development server.
- `scripts/check-expo-status.sh` — Verifies expo CLI and dependencies are installed.