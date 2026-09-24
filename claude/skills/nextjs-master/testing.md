# Next.js Testing — Playwright, Vitest, Jest, and Cypress

## Overview

Testing Next.js applications involves different tools for different types of tests: Playwright for end-to-end browser tests, Vitest/Jest for unit and component tests, and Cypress for integration tests. This skill covers setup and best practices for all four.

**Tools:**

| Tool | Type | Use Case |
|------|------|---------|
| **Playwright** | E2E | Browser automation, click/navigation tests |
| **Vitest** | Unit/Component | Fast Vite-based testing, React Server Components |
| **Jest** | Unit/Component | Traditional testing, ecosystem compatibility |
| **Cypress** | E2E | Feature-rich browser testing, time-travel debugging |

**Related skills:** core, deployment, performance

---

## Playwright

### Installation

```bash
pnpm add -D @playwright/test
npx playwright install --with-deps chromium
```

### Configuration

```js
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### Basic Test

```ts
// tests/home.spec.ts
import { test, expect } from '@playwright/test'

test('home page loads', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/My Next.js App/)
})

test('navigation works', async ({ page }) => {
  await page.goto('/')
  await page.click('text=Blog')
  await expect(page).toHaveURL(/\/blog/)
})

test('form submission', async ({ page }) => {
  await page.goto('/contact')
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('textarea[name="message"]', 'Hello!')
  await page.click('button[type="submit"]')
  await expect(page.locator('.success-message')).toBeVisible()
})
```

### Testing Server Actions

```ts
import { test, expect } from '@playwright/test'
import { createTestServer } from '@playwright/test/server'

test('create post via Server Action', async ({ page }) => {
  await page.goto('/posts/new')
  await page.fill('input[name="title"]', 'My New Post')
  await page.fill('textarea[name="content"]', 'Post content here')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/\/posts\/my-new-post/)
})
```

---

## Vitest (Recommended for Next.js)

### Installation

```bash
pnpm add -D vitest @vitejs/plugin-react jsdom
```

### Configuration

```js
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    include: ['**/*.test.{ts,tsx}'],
    globals: true,
  },
})
```

### Component Test

```tsx
// components/button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './button'

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" onClick={() => {}} />)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const onClick = vi.fn()
    render(<Button label="Click me" onClick={onClick} />)
    fireEvent.click(screen.getByText('Click me'))
    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when loading', () => {
    render(<Button label="Submit" loading onClick={() => {}} />)
    expect(screen.getByText('Submit')).toBeDisabled()
  })
})
```

### Server Component Test

Test Server Components by mocking data:

```tsx
// app/blog/page.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import BlogPage from '../app/blog/page'

// Mock the fetch call
global.fetch = vi.fn().mockResolvedValue({
  json: async () => [{ id: 1, title: 'Test Post' }],
})

describe('BlogPage', () => {
  it('renders posts', async () => {
    render(await BlogPage())
    expect(screen.getByText('Test Post')).toBeInTheDocument()
  })
})
```

---

## Jest (Alternative)

### Installation

```bash
pnpm add -D jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom
npx jest --init
```

### Configuration

```js
// jest.config.js
/** @type {import('jest').Config} */
const config = {
  testEnvironment: 'jsdom',
  setupFilesAfterFramework: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testMatch: ['**/*.test.{js,jsx,ts,tsx}'],
}

module.exports = config
```

```js
// jest.setup.js
import '@testing-library/jest-dom'
```

---

## Cypress

### Installation

```bash
pnpm add -D cypress
npx cypress open
```

### Configuration

```js
// cypress.config.ts
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',
  },
})
```

### Test

```ts
// cypress/e2e/auth.cy.ts
describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('logs in with valid credentials', () => {
    cy.get('input[name="email"]').type('test@example.com')
    cy.get('input[name="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/dashboard')
  })

  it('shows error with invalid credentials', () => {
    cy.get('input[name="email"]').type('wrong@example.com')
    cy.get('input[name="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()
    cy.get('[role="alert"]').should('contain', 'Invalid email or password')
  })
})
```

---

## Testing Server Actions with Vitest

```ts
// app/actions.test.ts
import { describe, it, expect, vi } from 'vitest'
import { createPost } from '../app/actions'
import * as db from '../lib/db'

vi.mock('../lib/db', () => ({
  db: {
    post: {
      create: vi.fn(),
    },
  },
}))

describe('createPost', () => {
  it('creates a post and revalidates the cache', async () => {
    const mockCreate = vi.fn().mockResolvedValue({ id: '1', title: 'Test' })
    ;(db as any).db.post.create = mockCreate

    const formData = new FormData()
    formData.set('title', 'Test')
    formData.set('content', 'Content')

    const result = await createPost(formData)

    expect(mockCreate).toHaveBeenCalled()
    // result handling...
  })
})
```

---

## `@next/third-parties` — Optimizing Third-Party Scripts

```bash
pnpm add @next/third-parties
```

```tsx
// app/layout.tsx
import { GoogleTagManager, GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleTagManager gtmId="GTM-XYZ" />
        <GoogleAnalytics gaId="G-XXXXXXXXXX" />
      </body>
    </html>
  )
}
```

---

## Gotchas

1. **Server Components can't be directly tested with `@testing-library/react`** — they require async rendering; mock the component output instead
2. **Playwright needs the dev server running** — use the `webServer` config option to auto-start it
3. **Vitest globals need setup** — set `globals: true` in vitest config or import `vi`/`describe` explicitly
4. **Mock `fetch` for API tests** — `global.fetch = vi.fn()` for testing route handlers
5. **`vi.mock()` must be at the top level** — Vitest mocks are hoisted; use `vi.mocked()` for function-level mocking
6. **Playwright `prefersReducedMotion`** — test accessibility by simulating `prefers-reduced-motion`
7. **`@next/third-parties`** handles script loading optimization — use it instead of raw `<Script>` for Google analytics

---

## Prerequisites

- Next.js Core — see `skills/core.md`

## Next Steps

- **Deployment testing:** See `skills/deployment.md` — test in Docker/production-like environments
- **CI/CD:** See `skills/deployment.md` — run Playwright/Cypress in CI pipelines
- **Performance testing:** See `skills/performance.md` — measure Core Web Vitals
