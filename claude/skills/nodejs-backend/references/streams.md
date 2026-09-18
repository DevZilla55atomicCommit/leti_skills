# Streams & Performance

> Load when: File uploads, large data processing, backpressure, worker threads.

## File Upload with Streams

```typescript
import { pipeline } from 'stream/promises';
import { createWriteStream } from 'fs';

// Fastify multipart
app.post('/upload', async (request) => {
  const data = await request.file();
  if (!data) throw app.httpErrors.badRequest('No file');
  await pipeline(data.file, createWriteStream(`./uploads/${data.filename}`));
  return { filename: data.filename };
});
```

## Worker Threads for CPU-bound Work

```typescript
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads';

if (isMainThread) {
  function runWorker(data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const worker = new Worker(__filename, { workerData: data });
      worker.on('message', resolve);
      worker.on('error', reject);
    });
  }

  app.post('/process', asyncHandler(async (req, res) => {
    const result = await runWorker(req.body);
    res.json(result);
  }));
} else {
  const result = heavyComputation(workerData);
  parentPort!.postMessage(result);
}
```

## Graceful Shutdown

```typescript
const server = app.listen(3000);
const connections = new Set<any>();

server.on('connection', (conn) => {
  connections.add(conn);
  conn.on('close', () => connections.delete(conn));
});

async function shutdown(signal: string) {
  console.log(`${signal} received, shutting down gracefully`);
  server.close();
  for (const conn of connections) conn.end();
  await db.end();
  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```
