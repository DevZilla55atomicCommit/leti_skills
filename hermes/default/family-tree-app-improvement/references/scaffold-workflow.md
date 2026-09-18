# Scaffold Workflow for Family Tree Projects

## Overview
This document outlines the standardized process for organizing new family tree projects within the Kasini Tree App ecosystem. It ensures consistency across project creation, file placement, and version control.

## Step-by-Step Workflow

### 1. Project Initialization
```bash
# Create project root
mkdir -p "/path/to/project/$(date +%Y-%m-%d)-kasini-project"
cd "/path/to/project/$(date +%Y-%m-%d)-kasini-project"

# Copy scaffold skeleton
cp -r /Users/alfredkamisese/.hermes/skills/family-tree-app-improvement/scaffold/* .

# Update package name in package.json
sed -i '' 's/kasini-tree-app/'"$(date +%Y-%m-%d)"'-kasini/g' package.json
```

### 2. Directory Structure Creation
```bash
# Create standard directories
mkdir -p \
  plans/ \
  analysis/ \
  transcripts/ \
  scaffold/ \
  design/ \
  docs/ \
  references/ \
  templates/ \
  scripts/
```

### 3. File Placement Protocol
| Source Location | Destination | Purpose |
|---------------|-------------|---------|
| `/transcripts/` | `analysis/` | Store raw transcripts |
| `/analysis/` | `analysis/` | Store analysis artifacts |
| `/scaffold/kasini-tree-app/` | project root | Core codebase |
| `/scaffold/kasini-tree-app/package.json` | project root | Dependency manifest |
| `/scaffold/kasini-tree-app/README.md` | project root | Documentation |
| `/scaffold/kasini-tree-app/src/` | project root | Source code |
| `/design/` | project root | Figma assets |
| `/references/` | project root | Session-specific notes |
| `/templates/` | project root | Boilerplate files |
| `/scripts/` | project root | Automation scripts |

### 4. Validation Checks
1. **Syntax Validation**: `npm run typecheck`
2. **Lint Check**: `npm run lint`
3. **Build Test**: `npm run dev` (should start Metro bundler)
4. **File Count**: Verify minimum file count matches template

### 5. Version Control Setup
```bash
git init
git add .
git commit -m "Initial commit: $(date +%Y-%m-%d) project scaffold"
```

### 6. Beta Signup Integration
1. Create Typeform → Airtable connection
2. Embed project URL in Ep 6 comment thread
3. Track conversions in Airtable base

## Reference Implementations
- `templates/expo-project-scaffold.zip` - Pre-configured Expo starter
- `scripts/verify-scaffold.js` - Schema validation and health check
- `references/file-organization.md` - Current directory structure
- `references/folder-creation.md` - Directory templates

## Revision History
- v1.0 (2026-07-12): Initial creation
- v1.1 (2026-07-13): Added script validation steps