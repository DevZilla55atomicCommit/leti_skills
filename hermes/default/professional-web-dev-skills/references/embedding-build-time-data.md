---
title: Embedding Large JSON Data at Build Time
description: How to safely embed large JSON files (e.g., 900KB+ graph data) in Next.js to avoid browser fetch hangs.
---

When serving large JSON files through Next.js API routes, the browser fetch can hang due to streaming/parsing limits. Instead:

1. **Place JSON files in `/public/data/`** (or `/src/data/` for TypeScript imports)
2. **Import them directly** in components using:
   ```ts
   import graphData from '@/data/graph-data.json';
   import layoutData from '@/data/layout.json';
   ```
3. **Update `next.config.js`** to preserve public files:
   ```js
   module.exports = {
     webpack(config) {
       config.module.rules.push({
         test: /\.json/,
         type: 'json',
         exclude: /node_modules/,
       });
       return config;
     },
   };
   ```
4. **Use in components**:
   ```tsx
   export async function getStaticProps() {
     return {
       props: {
         graphData: await import('@/data/graph-data.json'),
         layoutData: await import('@/data/layout.json'),
       },
     };
   }
   ```

### Verification Script
Create `scripts/verify-build-data.sh` to check that JSON files are properly imported:
```bash
#!/bin/bash
# Verify that JSON import paths resolve correctly
if ! grep -q '@/data/graph-data.json' src/components/Graph/useGraphData.ts; then
  echo "ERROR: graph-data.json import not found in useGraphData.ts"
  exit 1
fi
if ! grep -q '@/data/layout.json' src/components/Graph/useGraphData.ts; then
  echo "ERROR: layout.json import not found in useGraphData.ts"
  exit 1
fi
echo "SUCCESS: All build-time data imports verified"
```

Make executable:
```bash
chmod +x scripts/verify-build-data.sh