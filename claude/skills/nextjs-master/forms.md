# Next.js Forms — Server Action Forms, Zod Validation, useActionState, and Optimistic Updates

## Overview

Forms in Next.js App Router are powered by Server Actions. React extends the `<form>` element so that Server Functions can be invoked directly via the `action` prop, supporting progressive enhancement (works without JavaScript).

**Key APIs:**
- `<form action={serverAction}>` — connects a Server Action to a form
- `useActionState()` — handles pending state and return values
- `useFormStatus()` — shows loading state on submit buttons
- `useOptimistic()` — optimistic UI updates
- `formAction.bind()` — pass extra arguments to Server Actions
- `requestSubmit()` — programmatic form submission

**Related skills:** core, mutations, auth, caching, streaming

---

## Basic Server Action Form

```tsx
// app/ui/post-form.tsx
import { createPost } from '@/app/actions'

export function PostForm() {
  return (
    <form action={createPost}>
      <div>
        <label htmlFor="title">Title</label>
        <input type="text" id="title" name="title" required />
      </div>
      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" required />
      </div>
      <button type="submit">Create Post</button>
    </form>
  )
}
```

```ts
// app/actions.ts
'use server'
import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({ data: { title, content } })
  revalidatePath('/posts')
}
```

---

## Zod Validation on the Server

```ts
// app/lib/definitions.ts
import * as z from 'zod'

export const PostFormSchema = z.object({
  title: z
    .string()
    .min(3, 'Title must be at least 3 characters')
    .max(100, 'Title must be under 100 characters'),
  content: z
    .string()
    .min(10, 'Content must be at least 10 characters'),
})

export type PostFormState =
  | { errors?: { title?: string[]; content?: string[] }; message?: string }
  | undefined
```

```ts
// app/actions.ts
'use server'
import { PostFormSchema, type PostFormState } from '@/lib/definitions'
import { revalidatePath } from 'next/cache'

export async function createPost(
  prevState: PostFormState,
  formData: FormData
): Promise<PostFormState> {
  // 1. Validate form fields
  const validatedFields = PostFormSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  // 2. Return early if validation fails
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: 'Missing Fields. Failed to create post.',
    }
  }

  // 3. Mutate data
  try {
    await db.post.create({ data: validatedFields.data })
  } catch {
    return { message: 'Database Error. Failed to create post.' }
  }

  // 4. Revalidate
  revalidatePath('/posts')

  return { message: 'Post created!' }
}
```

---

## Displaying Validation Errors with `useActionState`

```tsx
// app/ui/post-form.tsx
'use client'
import { useActionState } from 'react'
import { createPost } from '@/app/actions'
import { PostFormState } from '@/lib/definitions'

const initialState: PostFormState = { message: '' }

export function PostForm() {
  const [state, formAction, pending] = useActionState(createPost, initialState)

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          aria-describedby="title-error"
        />
        {/* Show error if validation failed */}
        {state?.errors?.title && (
          <p id="title-error" className="text-red-500">
            {state.errors.title.map((error) => (
              <span key={error}>{error}</span>
            ))}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" />
        {state?.errors?.content && (
          <p id="content-error" className="text-red-500">
            {state.errors.content.map((error) => (
              <span key={error}>{error}</span>
            ))}
          </p>
        )}
      </div>

      {/* Success or general error message */}
      {state?.message && <p aria-live="polite">{state.message}</p>}

      {/* Submit button with pending state */}
      <button disabled={pending} type="submit">
        {pending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  )
}
```

---

## Submit Button Loading State with `useFormStatus`

When the form is complex, extract the button into a separate component to use `useFormStatus`:

```tsx
// app/ui/submit-button.tsx
'use client'
import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button disabled={pending} type="submit">
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}
```

```tsx
// app/ui/form.tsx
import { SubmitButton } from './submit-button'
import { createPost } from '@/app/actions'

export function Form() {
  return (
    <form action={createPost}>
      {/* ... */}
      <SubmitButton />
    </form>
  )
}
```

**Note:** `useFormStatus()` only works when called by a component that is a descendant of a `<form>` using a Server Action.

---

## Optimistic UI Updates with `useOptimistic`

Update the UI immediately while the Server Action runs in the background:

```tsx
// app/ui/todo-list.tsx
'use client'
import { useOptimistic } from 'react'
import { addTodo, toggleTodo } from '@/app/actions'

type Todo = { id: string; title: string; completed: boolean }

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, { ...newTodo, id: 'temp-' + Date.now() }]
  )

  async function handleAdd(formData: FormData) {
    const title = formData.get('title') as string
    // Optimistically add to the list
    addOptimisticTodo({ id: '', title, completed: false })
    // Actually mutate on the server
    await addTodo(title)
  }

  return (
    <div>
      <form action={handleAdd}>
        <input name="title" placeholder="New todo" />
        <button type="submit">Add</button>
      </form>

      {optimisticTodos.map((todo) => (
        <div key={todo.id} className={todo.completed ? 'line-through' : ''}>
          {todo.title}
        </div>
      ))}
    </div>
  )
}
```

---

## Passing Arguments with `bind()`

```tsx
// app/client-component.tsx
'use client'
import { updateUser } from './actions'

export function UserNameForm({ userId }: { userId: string }) {
  // Pre-bind userId
  const action = updateUser.bind(null, userId)

  return (
    <form action={action}>
      <input type="text" name="name" placeholder="New name" />
      <button type="submit">Update</button>
    </form>
  )
}
```

```ts
// app/actions.ts
'use server'
export async function updateUser(userId: string, formData: FormData) {
  const name = formData.get('name') as string
  await db.user.update({ where: { id: userId }, data: { name } })
  revalidatePath(`/profile/${userId}`)
}
```

---

## Programmatic Submission (`requestSubmit`)

```tsx
// app/entry-form.tsx
'use client'

export function EntryForm() {
  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // ⌘ + Enter or Ctrl + Enter to submit
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault()
      e.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <form action={submitEntry}>
      <textarea
        name="entry"
        rows={20}
        required
        onKeyDown={handleKeyDown}
        placeholder="Write your entry... (⌘+Enter to submit)"
      />
      <button type="submit">Submit Entry</button>
    </form>
  )
}
```

---

## Multi-Step Forms with `useActionState`

```tsx
// app/ui/multi-step-form.tsx
'use client'
import { useActionState } from 'react'
import { step1, step2, submit } from '@/app/actions'

type FormState = {
  step: 1 | 2 | 3
  data: Record<string, string>
  error?: string
}

const initialState: FormState = { step: 1, data: {} }

export function MultiStepForm() {
  const [state, formAction, pending] = useActionState(submit, initialState)

  if (state.step === 1) {
    return (
      <form action={formAction}>
        <Step1Fields />
        <button disabled={pending}>Next</button>
      </form>
    )
  }

  if (state.step === 2) {
    return (
      <form action={formAction}>
        <Step2Fields />
        <button disabled={pending}>Next</button>
      </form>
    )
  }

  return <p>Done! {JSON.stringify(state.data)}</p>
}
```

---

## Gotchas

1. **`<input name="title">` becomes `formData.get('title')`** — field names match `name` attributes
2. **`useActionState` replaces `useFormState`** — `useFormState` is the React 18 name; `useActionState` is the React 19 name
3. **`useFormStatus` must be in a child component** — it reads the nearest `<form>`'s status, so extract your button into a separate component
4. **`bind()` is more secure than hidden inputs** — values in `bind()` aren't visible in rendered HTML; hidden inputs are
5. **`requestSubmit()` triggers native form submission** — the Server Action receives `FormData` naturally
6. **`aria-live="polite"` on error messages** — screen readers announce errors without interrupting the user
7. **`pending` state disables buttons** — always disable the submit button while the action is running to prevent double submissions

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Server Actions — see `skills/mutations.md`

## Next Steps

- **Auth forms:** See `skills/auth.md` — signup/login with Zod, session management
- **Cache after forms:** See `skills/caching.md` — `updateTag` for read-your-own-writes
- **Security:** See `skills/security.md` — validate ALL form input, never trust `searchParams`
