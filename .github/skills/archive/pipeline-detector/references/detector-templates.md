# Reusable Detector Templates

Common detectors distilled from the AI Engineering Bootcamp. Each returns `{ file, line, type, snippet/risk, severity }`.

## Secrets scanner

Patterns that catch hardcoded credentials. Skip values that are clearly placeholders (`your-password-here`, `CHANGE_ME`, `<secret>`, `${VAR}`, `process.env.X`).

```js
const SECRET_PATTERNS = [
  { type: 'password', re: /(?:password|passwd|pwd)\s*[:=]\s*["'][^"'\s]{4,}["']/gi },
  { type: 'api-key', re: /(?:api[_-]?key|apikey|api_key|token|secret)\s*[:=]\s*["'][^"'\s]{8,}["']/gi },
  { type: 'jwt', re: /["']eyJ[a-zA-Z0-9_-]+\./g },
  { type: 'private-key', re: /-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----/g },
  { type: 'url-credentials', re: /https?:\/\/[^:]+:[^@]+@/g },
];
```

## SQL injection / XSS

Concatenated queries and unsafe DOM writes.

```js
const SQL = [
  /(?:db|pool|query|execute)\s*\.\s*(?:query|execute)\s*\(\s*["'`]\s*SELECT/i,
  /["'`]\s*SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*['"`]\s*\+/i,
  /`\s*SELECT\s+.*\$\{/i,
];
const XSS = [
  /\.innerHTML\s*=/, /\.outerHTML\s*=/, /dangerouslySetInnerHTML/, /document\.write\s*\(/, /v-html\s*=/
];
```

## Style / complexity

Long lines, oversized functions, short variable names.

```js
// Lines > maxLineLength
const longLines = lines.map((l, i) => ({ line: i + 1, len: l.length })).filter(l => l.len > 100);

// Functions > maxFunctionLines (brace-matching heuristic)
function findBigFunctions(src, maxFn = 30) {
  const out = [];
  const re = /(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)\s*{/g;
  let m;
  while ((m = re.exec(src))) {
    let d = 1, pos = m.index + m[0].length, start = src.slice(0, m.index).split('\n').length;
    while (pos < src.length && d > 0) { if (src[pos] === '{') d++; if (src[pos] === '}') d--; pos++; }
    const fnLines = src.slice(0, pos).split('\n').length - start + 1;
    if (fnLines > maxFn) out.push({ line: start, name: m[0].split('=')[0].trim(), lines: fnLines });
  }
  return out;
}

// Short variable names (excluding loop counters)
const shortVars = /(?:let|const|var)\s+([a-zA-Z_$]\w*)\s*=/g;
// name.length <= 2 && !['i','j','k'].includes(name) => finding
```

## Vulnerability versions

Compare installed dependency versions against a known-CVE list (semver-ish compare, handle `^`, `~`, `<`).

```js
function parseVersion(v) { return v.replace(/^[\^~><=]+/, ''); }
function compare(a, b) { /* numeric tuple compare */ }
function isVuln(installed, range) {
  const ic = parseVersion(installed), rc = range.replace(/^</, '');
  if (range.startsWith('<')) return compare(ic, rc) < 0;
  return false;
}
```

## Diff analysis (PR review)

Only analyze lines that start with `+`. Track current file via `diff --git a/X b/Y`.

```js
// findings: new files without tests, console.log added, package.json change w/o lockfile, big functions, secrets
const added = line.startsWith('+') && !line.startsWith('+++');
const newFile = /^diff --git a\/(.+?) b\/(.+?)$/.exec(line); // file 2 is new if a/ is /dev/null
```

## Contextual analyzer (simulated AI)

Assigns severity, flags false positives, gives remediation, computes score.

```js
function analyze(findings, projectRoot) {
  // Severity escalation: >=3 same-type in one file -> bump
  // FP heuristics:
  //   secrets in __tests__/fixtures/mock -> FP
  //   sql-injection w/o db import -> FP
  //   xss in non-(jsx/tsx/vue) -> FP
  // Remediation map: type -> concrete fix
  // Score: 10 - (critical*3 + high*1.5 + medium*0.5 + low*0.2), clamped 1..10
}
```

## CloudFormation / infra validation

Check task definitions exist, container port == target group port, health check path, listener port, exposed SGs.

```js
// presence: /TaskDefinition/.test(content)
// port match: content.match(/TaskDefinition[\s\S]*?ContainerPort:\s*(\d+)/)
// health: content.match(/TargetGroup[\s\S]*?HealthCheckPath:\s*([\w/]+)/)
// listener: content.match(/Listener:[\s\S]*?Port:\s*(\d+)/)
// exposed SG: CidrIp 0.0.0.0/0 on non-80 port -> high
```

## Report markdown

```markdown
# Report

## Resumen Ejecutivo
**Score: {score}/100**

## Hallazgos
| Archivo | Línea | Tipo | Severidad | Descripción |
|---------|-------|------|-----------|-------------|

## Recomendaciones
1. [HIGH] {fix}

## Falsos positivos
- {reason}
```