# Next.js Authentication — Sessions, DAL, DTOs, and Proxy Guards

## Overview

Authentication in Next.js involves three concepts: **Authentication** (verifying identity), **Session Management** (tracking auth state), and **Authorization** (controlling access). This skill covers the full stack: signup/login forms with Zod, stateless and database sessions, Data Access Layer (DAL), Data Transfer Objects (DTOs), and Proxy guards.

**Key patterns:**
- **Stateless sessions** — JWT signed with JOSE, stored in cookies
- **Database sessions** — session stored in DB, ID in cookie
- **Data Access Layer (DAL)** — centralized, server-only data access with auth checks
- **DTOs** — return only what the UI needs, never raw DB records
- **Proxy guard** — optimistic auth checks at the proxy level

**Related skills:** proxy, mutations, forms, security, caching, route-handlers

---

## The Three Concepts

1. **Authentication** — verifies identity (username + password, OAuth, etc.)
2. **Session Management** — tracks auth state across requests (cookie-based)
3. **Authorization** — decides what the authenticated user can access

---

## Signup Form with Zod Validation

```tsx
// app/ui/signup-form.tsx
'use client'
import { signup } from '@/app/actions/auth'
import { useActionState } from 'react'

const initialState = { message: '', errors: {} }

export function SignupForm() {
  const [state, formAction, pending] = useActionState(signup, initialState)

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" type="text" required />
        {state?.errors?.name && (
          <p className="text-red-500">{state.errors.name[0]}</p>
        )}
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required />
        {state?.errors?.email && (
          <p className="text-red-500">{state.errors.email[0]}</p>
        )}
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" required />
        {state?.errors?.password && (
          <ul>
            {state.errors.password.map((err) => (
              <li key={err} className="text-red-500">{err}</li>
            ))}
          </ul>
        )}
      </div>
      <button disabled={pending} type="submit">
        {pending ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  )
}
```

---

## Zod Registration Schema

```ts
// app/lib/definitions.ts
import * as z from 'zod'

export const SignupFormSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').trim(),
  email: z.string().email('Please enter a valid email').trim().toLowerCase(),
  password: z
    .string()
    .min(8, 'Be at least 8 characters')
    .regex(/[a-zA-Z]/, 'Contain at least one letter')
    .regex(/[0-9]/, 'Contain at least one number')
    .regex(/[^a-zA-Z0-9]/, 'Contain at least one special character'),
})

export const LoginFormSchema = z.object({
  email: z.string().email().trim().toLowerCase(),
  password: z.string().min(1, 'Password is required'),
})

export type FormState =
  | { errors?: { name?: string[]; email?: string[]; password?: string[] }; message?: string }
  | undefined
```

---

## Stateless Sessions (JOSE + Cookies)

### 1. Session Encryption (JOSE)

```ts
// app/lib/session.ts
import 'server-only'
import { SignJWT, jwtVerify } from 'jose'

const secretKey = new TextEncoder().encode(process.env.SESSION_SECRET!)
const encodedKey = new TextEncoder().encode(process.env.SESSION_SECRET!)

export type SessionPayload = {
  userId: string
  role: string
  expiresAt: number
}

export async function encrypt(payload: SessionPayload): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(encodedKey)
}

export async function decrypt(session: string | undefined): Promise<SessionPayload | null> {
  if (!session) return null
  try {
    const { payload } = await jwtVerify(session, encodedKey, { algorithms: ['HS256'] })
    return payload as unknown as SessionPayload
  } catch {
    return null
  }
}
```

### 2. Session Creation and Cookie Management

```ts
// app/lib/session.ts (continued)
import { cookies } from 'next/headers'

export async function createSession(userId: string, role: string = 'user') {
  const expiresAt = Date.now() + 7 * 24 * 60 * 60 * 1000 // 7 days
  const session = await encrypt({ userId, role, expiresAt })

  const cookieStore = await cookies()
  cookieStore.set('session', session, {
    httpOnly: true,   // JS can't read this
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',  // CSRF protection
    expires: new Date(expiresAt),
    path: '/',
  })
}

export async function deleteSession() {
  const cookieStore = await cookies()
  cookieStore.delete('session')
}

export async function updateSession() {
  const session = (await cookies()).get('session')?.value
  const payload = await decrypt(session)
  if (!payload) return null

  // Extend session
  const expires = Date.now() + 7 * 24 * 60 * 60 * 1000
  const newSession = await encrypt({ ...payload, expiresAt: expires })
  const cookieStore = await cookies()
  cookieStore.set('session', newSession, {
    httpOnly: true, secure: true, sameSite: 'lax',
    expires: new Date(expires), path: '/',
  })
}
```

---

## Database Sessions

For more control (session revocation, device tracking):

```ts
// app/lib/session-db.ts
import { cookies } from 'next/headers'
import { encrypt, decrypt } from './session'

export async function createDbSession(userId: number) {
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)

  // Store session in database
  const [session] = await db
    .insert(sessions)
    .values({ userId, expiresAt })
    .returning({ id: sessions.id })

  // Encrypt session ID in cookie
  const token = await encrypt({ sessionId: session.id, expiresAt })
  const cookieStore = await cookies()
  cookieStore.set('session', token, {
    httpOnly: true, secure: true, sameSite: 'lax',
    expires: expiresAt, path: '/',
  })
}
```

---

## Server Action — Signup

```ts
// app/actions/auth.ts
'use server'
import * as z from 'zod'
import { SignupFormSchema, LoginFormSchema, type FormState } from '@/lib/definitions'
import { db } from '@/lib/db'
import { createSession } from '@/lib/session'
import { redirect } from 'next/navigation'
import bcrypt from 'bcrypt'

export async function signup(prevState: FormState, formData: FormData): Promise<FormState> {
  // 1. Validate
  const validatedFields = SignupFormSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    password: formData.get('password'),
  })

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors }
  }

  // 2. Check for existing user
  const existing = await db.query.users.findFirst({
    where: eq(users.email, validatedFields.data.email),
  })
  if (existing) {
    return { errors: { email: ['Email already in use'] } }
  }

  // 3. Hash password and create user
  const hashedPassword = await bcrypt.hash(validatedFields.data.password, 10)
  const [user] = await db
    .insert(users)
    .values({ name: validatedFields.data.name, email: validatedFields.data.email, password: hashedPassword })
    .returning({ id: users.id })

  // 4. Create session
  await createSession(user.id, 'user')

  // 5. Redirect
  redirect('/dashboard')
}

export async function login(prevState: FormState, formData: FormData): Promise<FormState> {
  const validatedFields = LoginFormSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  })

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors }
  }

  const user = await db.query.users.findFirst({
    where: eq(users.email, validatedFields.data.email),
  })

  if (!user || !(await bcrypt.compare(validatedFields.data.password, user.password))) {
    return { message: 'Invalid email or password' }
  }

  await createSession(user.id, 'user')
  redirect('/dashboard')
}

export async function logout() {
  await deleteSession()
  redirect('/login')
}
```

---

## Data Access Layer (DAL)

Centralize all data access with built-in auth verification:

```ts
// app/lib/dal.ts
import 'server-only'
import { cache } from 'react'
import { cookies } from 'next/headers'
import { decrypt } from './session'

// Cached helper — called once per render pass
export const verifySession = cache(async () => {
  const sessionCookie = (await cookies()).get('session')?.value
  const session = await decrypt(sessionCookie)

  if (!session?.userId) {
    return null // or redirect('/login')
  }

  return { userId: session.userId, role: session.role }
})
```

### DAL with Auth Checks

```ts
// app/lib/dal.ts (continued)

export const getUser = cache(async (userId: number) => {
  const session = await verifySession()
  if (!session) return null

  return db.query.users.findFirst({
    where: eq(users.id, userId),
    columns: { id: true, name: true, email: true, role: true }, // Only needed columns
  })
})

export const getPost = cache(async (postId: number) => {
  const session = await verifySession()
  if (!session) return null

  const post = await db.query.posts.findFirst({
    where: eq(posts.id, postId),
  })

  // Authorization — does this user own the post?
  if (post.authorId !== session.userId && session.role !== 'admin') {
    return null // Or throw Forbidden
  }

  return post
})

export const deletePost = async (postId: number) => {
  const session = await verifySession()
  if (!session) throw new Error('Unauthorized')

  const post = await db.query.posts.findFirst({ where: eq(posts.id, postId) })
  if (post.authorId !== session.userId) throw new Error('Forbidden')

  await db.post.delete({ where: { id: postId } })
}
```

---

## Data Transfer Objects (DTOs)

Never return raw database records — filter to what the UI needs:

```ts
// app/lib/dto.ts
import 'server-only'
import { getUser } from './dal'

function canSeeEmail(viewer: User, target: User) {
  return viewer.id === target.id || viewer.role === 'admin'
}

export async function getUserProfileDTO(slug: string, viewerId: number) {
  const viewer = await getUser(viewerId)
  if (!viewer) return null

  const [row] = await sql`SELECT * FROM users WHERE slug = ${slug}`
  const target = row

  // Only return what's permitted
  return {
    name: target.name,
    email: canSeeEmail(viewer, target) ? target.email : null,
    bio: target.bio ?? null,
  }
}
```

---

## Proxy Guard (Optimistic Auth)

```ts
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'
import { decrypt } from '@/lib/session'

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  const sessionCookie = request.cookies.get('session')?.value
  const session = await decrypt(sessionCookie)

  // Protected routes
  if (pathname.startsWith('/dashboard') && !session?.userId) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Admin-only routes
  if (pathname.startsWith('/admin') && session?.role !== 'admin') {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

**Important:** Proxy guards are for optimistic checks only. Always verify auth inside Server Actions and Route Handlers.

---

## Auth Libraries (Recommended for Production)

For production apps, use a battle-tested auth library instead of building from scratch:

| Library | Features |
|--------|---------|
| **Clerk** | Full auth, pre-built UI, social login |
| **Better Auth** | Lightweight, TypeScript-first |
| **Auth0** | Enterprise, social login, MFA |
| **Kinde** | Simple, GDPR compliant |
| **NextAuth.js (Auth.js)** | Open source, community supported |
| **Supabase Auth** | Postgres-based, RLS integration |
| **Iron Session** | Stateless cookie sessions |
| **Jose** | JWT signing/verification (low-level) |

---

## Gotchas

1. **Always re-verify auth in Server Actions** — Proxy guards are optimistic only; a Server Action with `userId` in the form can be forged
2. **Cookie `httpOnly: true`** — prevents JavaScript from reading the session cookie (XSS protection)
3. **Cookie `sameSite: 'lax'`** — prevents CSRF attacks (cookies sent on same-site requests only)
4. **Return only DTOs from DAL** — never pass raw DB records to Client Components
5. **Use `React.cache()` on DAL functions** — avoids duplicate DB calls within a render pass
6. **IDOR prevention** — always check that `resource.authorId === session.userId` in the DAL, not just at the page level
7. **Session expiration** — set `expires` on cookies; expired sessions should redirect to login

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Forms + Server Actions — see `skills/forms.md`, `skills/mutations.md`

## Next Steps

- **Security hardening:** See `skills/security.md` — CSP, taint APIs, server-only
- **Proxy CSP:** See `skills/proxy.md` — nonce generation in proxy
- **Cache after auth mutations:** See `skills/caching.md` — `updateTag` after login
- **Route Handlers + auth:** See `skills/route-handlers.md` — API auth
