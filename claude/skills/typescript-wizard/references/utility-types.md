# Utility Types & Type-Level Programming

> Load when: Mapped types, conditional types, template literal types, custom utility types.

## Essential Built-in Utility Types

```typescript
// Partial<T> — all properties optional
type Draft = Partial<Article>;

// Required<T> — all properties required
type CompleteForm = Required<FormData>;

// Pick<T, K> / Omit<T, K> — select/exclude properties
type UserPreview = Pick<User, 'id' | 'name' | 'avatar'>;
type UserWithoutPassword = Omit<User, 'password' | 'salt'>;

// Record<K, V> — object with known keys
type FeatureFlags = Record<'darkMode' | 'newUI' | 'beta', boolean>;

// Extract<T, U> / Exclude<T, U> — filter union members
type StringOrNumber = Extract<string | number | boolean, string | number>; // string | number
type OnlyStrings = Exclude<string | number | boolean, number | boolean>;   // string

// ReturnType<T> / Parameters<T> — extract from functions
type ApiResponse = ReturnType<typeof fetchUser>;       // Promise<User>
type ApiParams = Parameters<typeof fetchUser>;          // [id: string]

// Awaited<T> — unwrap Promise
type User = Awaited<ReturnType<typeof fetchUser>>;     // User (unwrapped)
```

## Custom Mapped Types

```typescript
// Make all properties readonly and non-nullable
type Strict<T> = {
  readonly [K in keyof T]-?: NonNullable<T[K]>;
};

// Create getter functions for each property
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
// Getters<{ name: string; age: number }>
// = { getName: () => string; getAge: () => number }

// Filter properties by type
type StringKeys<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};
```

## Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;

// Infer keyword — extract types from structures
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;
type ArrayItem<T> = T extends (infer U)[] ? U : never;

// Extract function return type manually
type Return<T> = T extends (...args: any[]) => infer R ? R : never;

// Recursive conditional — deep readonly
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

// Practical: API response wrapper
type ApiResult<T> = T extends void
  ? { success: boolean }
  : { success: boolean; data: T };
```

## Template Literal Types

```typescript
// Event handler names
type EventName = 'click' | 'focus' | 'blur';
type HandlerName = `on${Capitalize<EventName>}`;
// = 'onClick' | 'onFocus' | 'onBlur'

// CSS property with units
type CSSLength = `${number}${'px' | 'rem' | 'em' | '%' | 'vh' | 'vw'}`;

// Route params extraction
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractParams<'/users/:userId/posts/:postId'>;
// = 'userId' | 'postId'
```

## Discriminated Unions

The single most useful TypeScript pattern for modeling state:

```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'idle':    return <Placeholder />;
    case 'loading': return <Spinner />;
    case 'success': return <DataView data={state.data} />;  // data is narrowed
    case 'error':   return <ErrorView error={state.error} />; // error is narrowed
  }
}

// Exhaustive check helper
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}
```

## Type-Safe Event Emitter

Combining several patterns into a practical example:

```typescript
type EventMap = {
  'user:login': { userId: string; timestamp: number };
  'user:logout': { userId: string };
  'item:created': { itemId: string; name: string };
};

class TypedEmitter<Events extends Record<string, any>> {
  private listeners = new Map<string, Set<Function>>();

  on<K extends keyof Events>(event: K, handler: (payload: Events[K]) => void): () => void {
    const key = event as string;
    if (!this.listeners.has(key)) this.listeners.set(key, new Set());
    this.listeners.get(key)!.add(handler);
    return () => this.listeners.get(key)?.delete(handler);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.listeners.get(event as string)?.forEach(fn => fn(payload));
  }
}

const emitter = new TypedEmitter<EventMap>();
emitter.on('user:login', (data) => {
  console.log(data.userId);     // Fully typed
});
```
