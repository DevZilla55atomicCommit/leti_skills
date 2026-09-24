# Next.js Mutations — Server Actions, Revalidation, and Redirects

## Overview

Server Actions let you run server-side code from the client. They are async functions marked with `'use server'` that can mutate data, call APIs, revalidate the cache, and redirect — all without creating an API route manually.

**Key APIs:**
- `'use server'` — marks a function as a Server Action
- `revalidatePath()` — revalidates cache for a route
- `revalidateTag()` — revalidates tagged cache entries
- `updateTag()` — immediately expires cache (Server Actions only)
- `redirect()` — redirects after mutation
- `refresh()` — refreshes the Next.js client router

**Related skills:** core, forms, caching, route-handlers, auth, security

---

## Creating Server Actions

### In a Separate File

Create a file and mark all exports as Server Actions:

```ts
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'

export async function createPost(formData: FormData) {
  // 1. Verify authentication
  const session = await auth()
  if (!session?.user) {
    throw new Error('Unauthorized')
  }

  // 2. Extract data from FormData
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // 3. Mutate data (database, API, etc.)
  const post = await db.post.create({
    data: { title, content, authorId: session.user.id },
  })

  // 4. Revalidate the cache
  revalidatePath('/posts')

  // 5. Redirect
  redirect(`/posts/${post.id}`)
}

export async function deletePost(postId: string) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')

  const post = await db.post.findUnique({ where: { id: postId } })
  if (post.authorId !== session.user.id) throw new Error('Forbidden')

  await db.post.delete({ where: { id: postId } })
  revalidateTag('posts')
}
```

### Inline in a Server Component

```tsx
// app/page.tsx
export default function Page() {
  async function publish() {
    'use server'
    // This runs on the server
    await db.post.update({ where: { id: postId }, data: { published: true } })
    revalidatePath('/posts')
  }

  return (
    <form action={publish}>
      <button type="submit">Publish</button>
    </form>
  )
}
```

**Note:** Inline Server Actions are great for simple cases. Use separate files for reusable or complex actions.

---

## Invoking Server Actions

### From a Form (Server or Client Component)

```tsx
// app/ui/form.tsx
import { createPost } from '@/app/actions'

export function Form() {
  return (
    <form action={createPost}>
      <input type="text" name="title" placeholder="Post title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

Forms using Server Actions support **progressive enhancement** — they work even without JavaScript.

### Passing Additional Arguments with `bind()`

```tsx
// app/client-component.tsx
'use client'
import { updateUser } from './actions'

export function UserProfile({ userId }: { userId: string }) {
  // Pre-bind userId to the Server Action
  const updateUserWithId = updateUser.bind(null, userId)

  return (
    <form action={updateUserWithId}>
      <input type="text" name="name" />
      <button type="submit">Update Name</button>
    </form>
  )
}
```

```ts
// app/actions.ts
'use server'
export async function updateUser(userId: string, formData: FormData) {
  // userId is pre-bound via bind(), formData comes from the form
  const name = formData.get('name') as string
  await db.user.update({ where: { id: userId }, data: { name } })
  revalidatePath(`/profile/${userId}`)
}
```

### From Event Handlers

```tsx
// app/like-button.tsx
'use client'
import { incrementLike } from './actions'
import { useState } from 'react'

export default function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)

  return (
    <>
      <p>Total Likes: {likes}</p>
      <button
        onClick={async () => {
          const updated = await incrementLike()
          setLikes(updated)
        }}
      >
        Like
      </button>
    </>
  )
}
```

---

## Revalidating Cache After Mutations

After mutating data, revalidate to show fresh data:

```ts
import { revalidatePath, revalidateTag, updateTag } from 'next/cache'

// Revalidate all data for a route
revalidatePath('/posts')
revalidatePath('/posts/[slug]', 'page') // specific page

// Revalidate by tag (more precise)
revalidateTag('posts')

// Immediately expire cache (read-your-own-writes) — Server Actions only
updateTag('posts')
```

**`updateTag` vs `revalidateTag`:**

| | `updateTag` | `revalidateTag` |
|--|-------------|-----------------|
| Where | Server Actions only | Server Actions + Route Handlers |
| Behavior | Immediately expires cache | Stale-while-revalidate |
| Use case | User must see their change | Background refresh OK |

---

## Redirecting After Mutations

```ts
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.post.create({ data: { title: formData.get('title') as string } })

  revalidatePath('/posts')
  // redirect() must come AFTER revalidation
  redirect(`/posts/${post.id}`)
}
```

**Important:** `redirect()` throws a special error. Any code after it will NOT execute. Call `revalidatePath()` before `redirect()`.

---

## Cookies in Server Actions

```ts
// app/actions.ts
'use server'
import { cookies } from 'next/headers'

export async function exampleAction() {
  const cookieStore = await cookies()

  // Read
  const token = cookieStore.get('session')?.value

  // Write
  cookieStore.set('theme', 'dark', { httpOnly: true, secure: true, sameSite: 'lax' })

  // Delete
  cookieStore.delete('token')

  // Revalidate — setting/deleting cookies re-renders the current page's layouts
  revalidatePath('/')
}
```

**Important:** When you set or delete cookies in a Server Action, Next.js re-renders the current page's layouts to reflect the change. Client state is preserved for re-rendered components.

---

## Authentication Inside Server Actions

**Always verify auth inside every Server Action** — never rely on the page-level auth check:

```ts
// app/actions.ts
'use server'
import { auth } from '@/lib/auth'
import { revalidatePath } from 'next/cache'

export async function deletePost(formData: FormData) {
  // Authenticate AND authorize
  const session = await auth()
  if (!session?.user) {
    throw new Error('Unauthorized')
  }

  const postId = formData.get('postId') as string
  const post = await db.post.findUnique({ where: { id: postId } })

  // Authorization — does this user own the post?
  if (post.authorId !== session.user.id) {
    throw new Error('Forbidden')
  }

  await db.post.delete({ where: { id: postId } })
  revalidatePath('/posts')
}
```

---

## Error Handling

Return errors as return values (not thrown) for expected errors:

```ts
// app/actions.ts
'use server'
export async function createPost(
  prevState: { message: string } | undefined,
  formData: FormData
) {
  const title = formData.get('title') as string

  if (!title || title.length < 3) {
    return { message: 'Title must be at least 3 characters' }
  }

  const post = await db.post.create({ data: { title } })
  revalidatePath('/posts')
  return { message: 'Post created!' }
}
```

Then handle in the component with `useActionState`:

```tsx
// app/ui/form.tsx
'use client'
import { useActionState } from 'react'
import { createPost } from '@/app/actions'

export function Form() {
  const [state, formAction, pending] = useActionState(createPost, undefined)

  return (
    <form action={formAction}>
      <input type="text" name="title" />
      {state?.message && <p aria-live="polite">{state.message}</p>}
      <button disabled={pending} type="submit">
        {pending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  )
}
```

---

## Gotchas

1. **Server Actions are reachable via POST** — any exported `'use server'` function can be called with a direct HTTP POST. Always verify auth inside the action.
2. **Server Actions don't support parallel invocation** — they are queued and dispatched one at a time from the client
3. **`redirect()` must be the last call** — it throws, so code after it won't run
4. **Read cookies before mutating** — `cookies()` is async (`await cookies()`)
5. **Prefer `revalidateTag` over `revalidatePath`** — it's more precise and avoids over-invalidating
6. **`updateTag` can only be used in Server Actions** — not in Route Handlers
7. **Server Actions encrypt closed-over variables** — variables captured from the outer scope are encrypted per-build. Use environment variables for truly sensitive data

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Data fetching — see `skills/data-fetching.md`

## Next Steps

- **Forms with validation:** See `skills/forms.md` — Zod schemas, useActionState, useOptimistic
- **Cache revalidation:** See `skills/caching.md` — cacheLife, cacheTag, Partial Prerendering
- **Route Handlers:** See `skills/route-handlers.md` — webhooks, revalidateTag from external calls
- **Auth patterns:** See `skills/auth.md` — DAL, DTOs, session management in Server Actions
