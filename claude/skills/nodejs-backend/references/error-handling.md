# Error Handling

> Load when: Error middleware, custom errors, validation, logging.

## Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string,
  ) {
    super(message);
    this.name = 'AppError';
  }

  static badRequest(message: string) { return new AppError(400, message, 'BAD_REQUEST'); }
  static unauthorized(message = 'Unauthorized') { return new AppError(401, message, 'UNAUTHORIZED'); }
  static forbidden(message = 'Forbidden') { return new AppError(403, message, 'FORBIDDEN'); }
  static notFound(message = 'Not found') { return new AppError(404, message, 'NOT_FOUND'); }
}
```

## Process-level Error Handling

```typescript
process.on('unhandledRejection', (reason) => {
  logger.fatal({ err: reason }, 'Unhandled rejection');
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  logger.fatal({ err }, 'Uncaught exception');
  process.exit(1);
});
```
