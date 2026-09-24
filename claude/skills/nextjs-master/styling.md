# Next.js Styling — Tailwind CSS v4, CSS Modules, Global CSS, and CSS-in-JS

## Overview

Next.js supports multiple styling approaches: Tailwind CSS (recommended), CSS Modules for component scoping, global CSS for base styles, and CSS-in-JS libraries (styled-components, styled-jsx). Choose the approach that fits your team and project.

**Key patterns:**
- **Tailwind CSS v4** — utility-first, PostCSS setup
- **CSS Modules** — locally scoped CSS, prevents naming collisions
- **Global CSS** — base styles, resets, fonts
- **CSS-in-JS** — styled-components, styled-jsx with registry pattern

**Related skills:** core, images-fonts

---

## Tailwind CSS v4 (Recommended)

### Installation

```bash
pnpm add -D tailwindcss @tailwindcss/postcss
```

### PostCSS Configuration

```js
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

### Global CSS Import

```css
/* app/globals.css */
@import 'tailwindcss';
```

```tsx
// app/layout.tsx
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Tailwind Config (Optional)

```js
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

export default config
```

### Using Tailwind Classes

```tsx
export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold text-blue-600">
        Welcome to Next.js!
      </h1>
    </main>
  )
}
```

### Tailwind v3 (Broader Browser Support)

```bash
pnpm add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: { extend: {} },
  plugins: [],
}
```

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## CSS Modules

CSS Modules locally scope CSS by generating unique class names, preventing naming collisions:

```css
/* app/blog/blog.module.css */
.blog {
  padding: 24px;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 16px;
}
```

```tsx
// app/blog/page.tsx
import styles from './blog.module.css'

export default function BlogPage() {
  return (
    <main className={styles.blog}>
      <h1 className={styles.title}>My Blog</h1>
    </main>
  )
}
```

---

## Global CSS

For base styles that apply to the entire application:

```css
/* app/globals.css */
@import 'tailwindcss';

/* CSS variables */
:root {
  --color-primary: #0070f3;
  --color-background: #ffffff;
}

/* Base styles */
body {
  color: var(--color-primary);
  background: var(--color-background);
  margin: 0;
  padding: 20px 20px 60px;
  max-width: 680px;
  margin: 0 auto;
}

/* Reset */
* {
  box-sizing: border-box;
}
```

---

## External Stylesheets

Import CSS from npm packages anywhere in the app:

```tsx
// app/layout.tsx
import 'bootstrap/dist/css/bootstrap.css'
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="container">{children}</body>
    </html>
  )
}
```

**Note:** React 19 also supports `<link rel="stylesheet">` natively.

---

## CSS Ordering and Merging

Next.js optimizes CSS during production builds. Import order determines CSS cascade order:

```tsx
// ✅ CORRECT — predictable order
import './base.css'       // Load base first
import styles from './page.module.css'  // Then component styles
```

**Best practices for predictable ordering:**
1. Import global styles and Tailwind in the root layout
2. Import CSS Modules from their specific component files
3. Extract shared styles into shared components
4. Don't auto-sort imports with ESLint's sort-imports rule

---

## styled-components v6+

### 1. Enable in Next.js Config

```js
// next.config.js
module.exports = {
  compiler: {
    styledComponents: true,
  },
}
```

### 2. Create Registry

```tsx
// lib/registry.tsx
'use client'
import React, { useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import { ServerStyleSheet, StyleSheetManager } from 'styled-components'

export default function StyledComponentsRegistry({ children }: { children: React.ReactNode }) {
  const [styledComponentsStyleSheet] = useState(() => new ServerStyleSheet())

  useServerInsertedHTML(() => {
    const styles = styledComponentsStyleSheet.getStyleElement()
    styledComponentsStyleSheet.instance.clearTag()
    return <>{styles}</>
  })

  if (typeof window !== 'undefined') return <>{children}</>

  return (
    <StyleSheetManager sheet={styledComponentsStyleSheet.instance}>
      {children}
    </StyleSheetManager>
  )
}
```

### 3. Wrap Root Layout

```tsx
// app/layout.tsx
import StyledComponentsRegistry from '@/lib/registry'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <StyledComponentsRegistry>{children}</StyledComponentsRegistry>
      </body>
    </html>
  )
}
```

---

## styled-jsx v5.1+

### 1. Create Registry

```tsx
// app/registry.tsx
'use client'
import React, { useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import { StyleRegistry, createStyleRegistry } from 'styled-jsx'

export default function StyledJsxRegistry({ children }: { children: React.ReactNode }) {
  const [jsxStyleRegistry] = useState(() => createStyleRegistry())

  useServerInsertedHTML(() => {
    const styles = jsxStyleRegistry.styles()
    jsxStyleRegistry.flush()
    return <>{styles}</>
  })

  return <StyleRegistry registry={jsxStyleRegistry}>{children}</StyleRegistry>
}
```

### 2. Wrap Root Layout

```tsx
// app/layout.tsx
import StyledJsxRegistry from './registry'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <StyledJsxRegistry>{children}</StyledJsxRegistry>
      </body>
    </html>
  )
}
```

---

## CSS-in-JS Libraries Support Matrix

| Library | Client Components | Server Components | Registry Required |
|---------|-----------------|-------------------|-------------------|
| styled-components | ✅ | ✅ (with registry) | ✅ |
| styled-jsx | ✅ | ✅ (with registry) | ✅ |
| Emotion | ✅ | 🔜 | — |
| Chakra UI | ✅ | ✅ | ✅ |
| Panda CSS | ✅ | ✅ | ✅ |
| Vanilla Extract | ✅ | ✅ | ❌ |
| Stitches | ✅ | ✅ | ✅ |
| Goober | ✅ | ✅ | ✅ |

---

## Gotchas

1. **Tailwind content array must be specific** — avoid `./**/*.tsx`; it scans `node_modules`. Use `./src/**/*.{js,ts,jsx,tsx}`
2. **CSS Modules don't support dynamic class names** — `styles[dynamicName]` is not supported; use template literals: `` `${styles.base} ${isActive ? styles.active : ''}` ``
3. **Global CSS can be imported anywhere** — but only root layout imports are guaranteed to apply first
4. **styled-components registry must be a Client Component** — it uses hooks (`useState`)
5. **CSS ordering affects cascade** — import order matters; put global styles before component styles
6. **Tailwind v4 uses `@import 'tailwindcss'`** — not `@tailwind base/components/utilities`
7. **Next.js 16 doesn't run ESLint during build** — run `npm run lint` separately

---

## Prerequisites

- Next.js Core — see `skills/core.md`

## Next Steps

- **next/image + CSS:** See `skills/images-fonts.md` — responsive images with Tailwind
- **next/font + CSS:** See `skills/images-fonts.md` — font loading with CSS variables
- **Metadata + styling:** See `skills/metadata.md` — SEO meta tags
