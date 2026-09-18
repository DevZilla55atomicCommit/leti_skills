# Server Actions

> Load when: Form handling, mutations, optimistic updates, revalidation.

## Basic Server Action

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
});

export async function createPost(prevState: any, formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  try {
    await db.posts.create({ data: parsed.data });
  } catch (e) {
    return { error: 'Failed to create post' };
  }

  revalidatePath('/posts');
  redirect('/posts');
}
```

## With useActionState (React 19)

```tsx
'use client';
import { useActionState } from 'react';
import { createPost } from './actions';

export function CreatePostForm() {
  const [state, action, isPending] = useActionState(createPost, null);

  return (
    <form action={action}>
      <input name="title" />
      {state?.errors?.title && <p className="text-red-500">{state.errors.title}</p>}

      <textarea name="content" />
      {state?.errors?.content && <p className="text-red-500">{state.errors.content}</p>}

      {state?.error && <p className="text-red-500">{state.error}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

## Optimistic Updates with useOptimistic

```tsx
'use client';
import { useOptimistic } from 'react';

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function addTodo(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimistic({ id: crypto.randomUUID(), text, done: false });
    await createTodo(formData); // Server Action
  }

  return (
    <form action={addTodo}>
      <input name="text" />
      <button type="submit">Add</button>
      <ul>
        {optimisticTodos.map(t => <li key={t.id}>{t.text}</li>)}
      </ul>
    </form>
  );
}
```
