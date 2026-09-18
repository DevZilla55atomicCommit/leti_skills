---
name: project-conventions
description: Alfred's project conventions and coding standards for all agents
category: development
tags: [conventions, standards, nextjs, typescript, tailwind]
---

# Project Conventions Skill

## Purpose
Codify Alfred's development standards so any agent (Hermes, Claude Code) follows consistent patterns.

## Stack Conventions

### Frontend
- **Framework:** Next.js 15+ App Router (React 18+)
- **Language:** TypeScript strict mode (`"strict": true`)
- **Styling:** Tailwind CSS + shadcn/ui components
- **State:** React Server Components by default, Client Components only when needed
- **Forms:** React Hook Form + Zod validation
- **Data Fetching:** Server Actions for mutations, `fetch` with `next: { revalidate }` for ISR
- **Animations:** Framer Motion for complex, CSS transitions for simple

### Code Quality
- **Linting:** ESLint (Next.js config + `plugin:@typescript-eslint/recommended`)
- **Formatting:** Prettier (single quotes, trailing commas, 100 char line width)
- **Type Checking:** `tsc --noEmit` in CI
- **Testing:** Vitest (unit), Playwright (e2e)
- **Git Hooks:** Husky + lint-staged (pre-commit: lint + typecheck)

### Project Structure
```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Route groups
│   ├── (dashboard)/
│   ├── api/               # API routes (Server Actions preferred)
│   └── globals.css
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── shared/            # Cross-feature components
│   └── features/          # Feature-specific components
├── lib/
│   ├── utils.ts           # cn(), formatters, helpers
│   ├── validations/       # Zod schemas
│   └── constants/         # App constants
├── hooks/                 # Custom React hooks
├── types/                 # Global TypeScript types
└── styles/                # Global styles, Tailwind config
```

## Coding Patterns

### Server Components First
```tsx
// ✅ Default: Server Component
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId) // Direct DB access
  return <div>{user.name}</div>
}

// ❌ Only when needed: Client Component
'use client'
export function InteractiveChart({ data }) {
  const [hovered, setHovered] = useState(null)
  return <Chart data={data} onHover={setHovered} />
}
```

### Server Actions for Mutations
```tsx
// app/actions/user.ts
'use server'
export async function updateUser(data: UserUpdateSchema) {
  const validated = UserUpdateSchema.parse(data)
  const session = await auth()
  if (!session) throw new Error('Unauthorized')
  
  return await db.user.update({
    where: { id: session.user.id },
    data: validated
  })
}
```

### Zod Validation Everywhere
```tsx
// lib/validations/user.ts
export const UserUpdateSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  timezone: z.string().optional()
})
export type UserUpdate = z.infer<typeof UserUpdateSchema>
```

### Type-Safe API Routes
```tsx
// app/api/users/route.ts
import { UserUpdateSchema } from '@/lib/validations/user'

export async function PUT(req: Request) {
  const body = await req.json()
  const data = UserUpdateSchema.parse(body)
  // ... handle
}
```

## Commands (Standardized)

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Start dev server (Turbopack) |
| `pnpm build` | Production build |
| `pnpm typecheck` | `tsc --noEmit` |
| `pnpm lint` | `eslint . --ext .ts,.tsx` |
| `pnpm test` | `vitest run` |
| `pnpm test:watch` | `vitest` |
| `pnpm test:e2e` | `playwright test` |
| `pnpm format` | `prettier --write .` |
| `pnpm db:push` | Drizzle/Prisma push |
| `pnpm db:studio` | Drizzle/Prisma studio |

## Git Conventions

### Branch Naming
- `feat/description` — New feature
- `fix/description` — Bug fix
- `refactor/description` — Code improvement
- `docs/description` — Documentation
- `chore/description` — Maintenance

### Commit Messages (Conventional Commits)
```
feat: add user profile page
fix: resolve hydration error on dashboard
refactor: extract api client to lib/api
docs: update README with deployment steps
chore: update dependencies
```

### PR Requirements
- [ ] Typecheck passes
- [ ] Lint passes
- [ ] Tests pass
- [ ] No console.log/debugger
- [ ] Self-review completed

## Environment Variables

### Required (`.env.local`)
```bash
# Auth
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

# Database
DATABASE_URL=

# External APIs
GITHUB_TOKEN=
LINEAR_API_KEY=
```

### Optional
```bash
# Analytics
NEXT_PUBLIC_POSTHOG_KEY=

# Feature flags
ENABLE_BETA_FEATURES=false
```

## Agent Instructions

When working on Alfred's projects:
1. **Read this skill first** — understand conventions
2. **Check `CLAUDE.md` in project root** — project-specific overrides
3. **Run `pnpm typecheck && pnpm lint` before committing**
4. **Prefer Server Components** — only add `'use client'` when necessary
5. **Use existing shadcn/ui components** — don't reinvent
6. **Validate with Zod** — at API boundaries and forms
6. **Keep components small** — extract to `components/shared` or `components/features`
7. **No inline styles** — use Tailwind classes
8. **No `any` types** — use proper generics or `unknown`
9. **Assets are SETUP-phase, manifest-driven, local-first** — `assets/manifest.json` (file → section/purpose/attribution) lands before UI work; agent never web-hunts images. Verify with the project's asset gate (`npm run verify:assets`: every ref resolves, no stubs); production hotlinks are banned.

## Project-Specific Overrides

Each project may have a `CLAUDE.md` or `.hermes/PROJECT_CONVENTIONS.md` that extends/overrides these defaults. Always check project root first.