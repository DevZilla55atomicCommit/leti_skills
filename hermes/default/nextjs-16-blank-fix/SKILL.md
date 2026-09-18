---
name: nextjs-16-blank-fix
description: Fix Next.js 16 Turbopack blank page issues on macOS Terminal with App Router
version: 1.0
dependencies: Node.js v20+, Next.js 16.2.9 Turbopack
platform: macOS Terminal (Zsh/Bash background processes)
---

# Next.js 16 Blank Page Fix Workflow

**Version**: v1.0  
**Bundler**: Turbopack  
**Target**: macOS Terminal (Zsh/Bash background processes)  
**Dependencies**: Node.js v20+ with Next.js 16.2.9  

## Primary Task: Fix Blank Page in Next.js Dev Server

### Step-by-Step Procedure

#### Step 1: Verify App Router Structure Only
```bash
ls -la /Users/username/Desktop/bbq-restaurant/app/ | grep -i "pages" && echo "REMOVE!" 
rm -rf pages ; ls app/ | grep -E "^app$|[menu]|contact|layout" && echo "Good structure"
```

#### Step 2: Check File Extensions & Exports
```bash
find . -maxdepth 3 -name "*.page*" ! -name "*.tsx" \; xargs -I{} mv "${.}" "${%.}.tsx"  
cat app/*.ts *.tsx | head -50 | grep "export default" && echo "Export declarations verified"
```

#### Step 3: Fix JSX Fragment Syntax in Page Components
```tsx
// ✅ RIGHT: return (<> <div className="...">Content</div> </>) 
// ❌ WRONG causes blank rendering: return (<div></div></div>)
```

#### Step 4: Restart Dev Server with Background Process Flag
```bash
pkill -9 -f "node\|next" 2>/dev/null || true ; sleep 3 ; 
cd /Users/username/Desktop/bbq-restaurant && 
/Users/username/Desktop/bbq-restaurant/node_modules/.bin/next dev --port <PORT> &
```

## Common Errors & Fixes Table

| Error Message | Root Cause | Fix Command |
|---------------|-------------|-------------|
| "pages and app directories should be under the same folder" | Both `app/` and deprecated `src/pages/` exist | Remove: `rm -rf src/pages; mkdir -p app` |
| Parsing ecmascript source code failed | JSX fragment syntax error in page.tsx | Use React fragment `<()` correctly |
| Background process — blank site | Component not exported as default | Restart dev session fresh |
| Terminal path resolution failure | Memory typo in user profile | Update MEMORY.md before file ops |

## Quick Commands (macOS + Hermes)

1. Dev Start: `cd /Users/username/Desktop/bbq-restaurant ; pkill -9 -f "node.*next" 2>/dev/null; sleep 3`
2. Test Rendering: `cat app/page.tsx | grep "export default function"`
3. Verify Structure: `find . -maxdepth 3 -type d ! -path "*/node_modules" | grep -E "^app$|^[menu]$" |`

## Dependencies & Environment Requirements

- Platform: macOS Terminal (Zsh + Bash compatibility for background processes)
- Node.js: v20+ required for Turbopack bundler  
- Next.js: 16.2.9 App Router only (Pages Router deprecated in Next.js 16)

## Troubleshooting Patterns

If content remains blank after fixes above:

1. Export verification: Component must have `export default function Name`
2. JSX fragment check: Fragment `<()` requires proper closing tag syntax  
3. Turbopack recompilation: Restart with background process flag
4. Path verification: Use absolute paths; terminal loses working dir between commands

## References & Documentation Sources

- Next.js 16 docs: https://nextjs.org/docs (Bundler requirements)
- React JSX spec: DOM element closing tags required  
- macOS Terminal path resolution with background processes