# TypeScript Configuration

> Load when: tsconfig setup, strict mode, project references, path aliases.

## Recommended tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Key Options Explained

| Option | Why |
|--------|-----|
| `strict: true` | Enables all strict checks. Non-negotiable for new projects. |
| `noUncheckedIndexedAccess` | `array[0]` returns `T \| undefined` instead of `T`. Catches real bugs. |
| `exactOptionalPropertyTypes` | `{ x?: string }` means `string \| undefined`, not `string \| undefined \| null`. |
| `moduleResolution: "bundler"` | For projects using Vite/webpack/esbuild. Use `"node16"` for Node.js libraries. |
| `skipLibCheck: true` | Skips type checking `.d.ts` files. Faster builds, avoids conflicts between library types. |

## Project References (Monorepo)

```json
// tsconfig.json (root)
{
  "references": [
    { "path": "./packages/shared" },
    { "path": "./packages/api" },
    { "path": "./packages/web" }
  ]
}

// packages/shared/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}

// packages/api/tsconfig.json
{
  "compilerOptions": { "composite": true },
  "references": [{ "path": "../shared" }]
}
```

Build with: `tsc --build` (incremental, respects dependency order).
