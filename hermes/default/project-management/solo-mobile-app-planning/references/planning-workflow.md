# Solo Mobile App Planning Workflow

## Step-by-Step Checklist

### 1. Linear Setup (3 min)
- [ ] Create workspace "My Apps" 
- [ ] Create project "MyFirstApp"
- [ ] Import templates: Feature, Bug, Chore, Spike
- [ ] Verify templates exist in project settings

### 2. Obsidian Knowledge Base (4 min)
- [ ] Open vault at ~/Dev/obsidian-vault
- [ ] Enable community plugins: Git, Templater, Dataview
- [ ] Configure Templater template folder = `templates`
- [ ] Set Git auto-push interval = 30 min

### 3. Figma Design System (3 min)
- [ ] Create file "MyFirstApp - Design System"
- [ ] Import iOS 18 UI Kit and Material 3 Design Kit
- [ ] Create pages: Design System, Screens iOS, Screens Android, Prototypes, Archive
- [ ] Build Design System components (colors, typography, spacing, shadows, components)
- [ ] Create iPhone 16 Pro frames for all screens (3 states each)

### 4. App Initialization (2 min)
- [ ] cd ~/Dev/MyFirstApp
- [ ] npx create-expo-app@latest app
- [ ] cd app && npx expo start
- [ ] Scan QR with Expo Go on phone

### 5. Daily Operations
- Morning: Check "Sprint X" cycle, pick top issue
- Code: Build feature branch, commit, push, PR → merge
- Evening: Move issues to "Done", update specs if needed

## Scripts Reference
- scripts/check-plan-sync.sh - Verifies Linear/Obsidian/Git sync status