# Node.js Debugging Guide — Debug Investigation Reference

Técnicas de debugging en Node.js.

## Inspector (Chrome DevTools)

```bash
# Start with inspector
node --inspect server.js

# Break on first line
node --inspect-brk server.js

# Open chrome://inspect in Chrome
# Click "Open dedicated DevTools for Node"
```

## Debugger Statement

```javascript
// Pauses execution when DevTools is attached
function processOrder(order) {
  debugger;
  // ... rest of function
}
```

## CLI Debugger

```bash
node inspect server.js

# Commands:
# cont / c — Continue execution
# next / n — Next line
# step / s — Step into
# out / o — Step out
# pause — Pause execution
# watch('x') — Watch expression
# repl — Enter REPL mode
# .exit — Exit debugger
```

## Heap Snapshots

```bash
# Generate heap snapshot programmatically
node -e "
const v8 = require('v8');
const fs = require('fs');
const snapshot = v8.getHeapSnapshot();
snapshot.pipe(fs.createWriteStream('heap.heapsnapshot'));
"
```

## CPU Profiles

```bash
# Using --cpu-prof
node --cpu-prof --cpu-prof-dir=./profiles server.js

# Using clinic.js
npx clinic doctor -- node server.js

# Using 0x
npx 0x server.js
```

## Async Stack Traces

```javascript
// Node.js 14+ preserves async stack traces
// Enable with NODE_OPTIONS
NODE_OPTIONS="--async-stack-traces" node server.js
```

## Memory Leak Detection

```javascript
// Track heap growth
const v8 = require('v8');

setInterval(() => {
  const usage = process.memoryUsage();
  const heap = v8.getHeapStatistics();
  console.log({
    rss: `${(usage.rss / 1024 / 1024).toFixed(1)} MB`,
    heapTotal: `${(usage.heapTotal / 1024 / 1024).toFixed(1)} MB`,
    heapUsed: `${(usage.heapUsed / 1024 / 1024).toFixed(1)} MB`,
    external: `${(usage.external / 1024 / 1024).toFixed(1)} MB`,
  });
}, 5000);
```

## Uncaught Exception Debugging

```javascript
process.on('uncaughtException', (err, origin) => {
  console.error('Uncaught Exception:', err);
  console.error('Origin:', origin);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise);
  console.error('Reason:', reason);
});
```

## Profiling with --prof

```bash
# Generate v8.log
node --prof server.js

# Process the log
node --prof-process v8.log > processed.txt
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Techniques](../references/techniques.md) — Técnicas de debugging
- [Browser DevTools](./browser-devtools.md) — Debugging en browser
