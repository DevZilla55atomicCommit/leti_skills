# Advanced Generics

> Load when: Generic constraints, inference, higher-order type patterns.

## Generic Constraints

```typescript
// Constrain to objects with an id
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Constrain to keys of an object
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  keys.forEach(key => { result[key] = obj[key]; });
  return result;
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

## Generic Inference Patterns

```typescript
// Infer return type from a factory map
type EventMap = {
  click: { x: number; y: number };
  keypress: { key: string; code: number };
  scroll: { offsetY: number };
};

function on<K extends keyof EventMap>(event: K, handler: (data: EventMap[K]) => void) {
  // TypeScript infers the correct handler parameter type
}

on('click', (data) => {
  console.log(data.x, data.y); // Fully typed
});

// Builder pattern with chaining
class QueryBuilder<T extends object> {
  private filters: Partial<T> = {};

  where<K extends keyof T>(key: K, value: T[K]): this {
    this.filters[key] = value;
    return this;
  }

  build(): Partial<T> {
    return { ...this.filters };
  }
}

// Usage: each .where() call is fully typed
new QueryBuilder<{ name: string; age: number; active: boolean }>()
  .where('name', 'Alice')   // value must be string
  .where('age', 30)          // value must be number
  .where('active', true)     // value must be boolean
  .build();
```

## The `satisfies` Operator

`satisfies` validates a type without widening it — you keep the narrow literal types:

```typescript
type Route = { path: string; method: 'GET' | 'POST' | 'PUT' | 'DELETE' };

// With `as const` + satisfies: validated AND narrow
const routes = {
  home:    { path: '/',       method: 'GET' },
  create:  { path: '/create', method: 'POST' },
  update:  { path: '/update', method: 'PUT' },
} as const satisfies Record<string, Route>;

// routes.home.method is 'GET' (not string)
```

## Generic Components in React

```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return <>{items.map((item, i) => (
    <div key={keyExtractor(item)}>{renderItem(item, i)}</div>
  ))}</>;
}

// Usage — T is inferred from items
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}  // user is User
  keyExtractor={(user) => user.id}
/>
```

## Function Overloads vs Generics

Prefer generics when the input/output relationship is uniform. Use overloads when different inputs produce fundamentally different outputs:

```typescript
// Good: overloads for different return types
function parse(input: string, format: 'json'): object;
function parse(input: string, format: 'number'): number;
function parse(input: string, format: 'json' | 'number'): object | number {
  return format === 'json' ? JSON.parse(input) : Number(input);
}

// Good: generic for uniform relationship
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```
