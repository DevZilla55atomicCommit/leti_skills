# Type Narrowing

> Load when: Type guards, discriminated unions, exhaustive checks, assertion functions.

## Built-in Narrowing

```typescript
// typeof
function format(value: string | number) {
  if (typeof value === 'string') return value.toUpperCase();
  return value.toFixed(2);
}

// instanceof
function getLength(input: string | string[]) {
  if (input instanceof Array) return input.length;
  return input.length;
}

// in operator
function move(entity: Bird | Fish) {
  if ('fly' in entity) return entity.fly();
  return entity.swim();
}

// Truthiness
function printName(name: string | null | undefined) {
  if (name) console.log(name.toUpperCase()); // name is string
}
```

## Custom Type Guards

```typescript
// Type predicate (is)
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    typeof (value as User).id === 'string'
  );
}

// Usage
function processInput(data: unknown) {
  if (isUser(data)) {
    console.log(data.email); // data is User
  }
}

// Assertion function (asserts)
function assertDefined<T>(value: T | null | undefined, msg?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(msg ?? 'Value is null or undefined');
  }
}

const user = getUser(); // User | null
assertDefined(user, 'User not found');
user.email; // user is User (narrowed after assertion)
```

## Discriminated Unions for State Machines

```typescript
type ConnectionState =
  | { state: 'disconnected' }
  | { state: 'connecting'; attempt: number }
  | { state: 'connected'; socket: WebSocket }
  | { state: 'error'; error: Error; retryAfter: number };

function handleConnection(conn: ConnectionState) {
  switch (conn.state) {
    case 'disconnected':
      return startConnection();
    case 'connecting':
      return showProgress(conn.attempt);
    case 'connected':
      return conn.socket.send('ping');
    case 'error':
      return scheduleRetry(conn.retryAfter);
  }
}
```

## Exhaustive Pattern Matching

```typescript
// The never trick — compiler error if you miss a case
function exhaustiveCheck(value: never): never {
  throw new Error(`Unhandled: ${JSON.stringify(value)}`);
}

type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rect'; width: number; height: number }
  | { kind: 'triangle'; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':   return Math.PI * shape.radius ** 2;
    case 'rect':     return shape.width * shape.height;
    case 'triangle': return 0.5 * shape.base * shape.height;
    default:         return exhaustiveCheck(shape); // Error if case missed
  }
}
```
