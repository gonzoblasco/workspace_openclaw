---
name: modern-web-guidance
description: >
  Modern web platform guidance with browser compatibility data, curated by the
  Chrome, Edge, Firefox and MDN teams. Use before writing or fixing client-side
  HTML/CSS/JS so the result uses platform features instead of legacy JS or an
  extra library. Triggers: dialogs/modals/popovers, forms and validation,
  accessibility, dark mode, container queries, view transitions, scroll-driven
  animation, CSS color (oklch), anchor positioning, tables, date/timezones
  handling, sanitization, passkeys, web components, Core Web Vitals.
  Do not trigger for backend, infra, build tooling or pure refactors.
---

# Modern Web Guidance

Bundled locally at `vendor/mwg/<version>/skills/modern-web-guidance/`. Search is
**offline** (209 guides + quantized vectors; the binary makes no network calls),
so it costs milliseconds and works without connectivity.

Set `M="vendor/mwg/1.0.1/skills/modern-web-guidance/modern-web.mjs"` from the
workspace root. If `vendor/mwg` is missing: `./scripts/mwg-install.sh`.

**Always prefix with `DISABLE_TELEMETRY=1`.** The upstream tool declares
anonymous Google telemetry; Opt-out is via that variable.

## 1. Search

```bash
DISABLE_TELEMETRY=1 node "$M" search "<2-5 word action query>"
```

Rules that make the difference between useful and useless results:

- **One capability per query.** "responsive table dark mode" is two searches,
  not one.
- **Name the UI primitive, not the intent.** Search `confirmation dialog`, not
  `confirm destructive action`. Search `date picker input`, not `pick a date`.
- **No framework or app nouns.** Drop React/Vue/Tailwind, file names, product
  names.
- Returns `[{id, description}]`. Judge by `description`, then retrieve.
- Empty or unrelated: **rephrase once** with a concrete HTML/CSS noun before
  concluding the topic isn't covered. Don't retrieve an unrelated guide.

## 2. Retrieve

```bash
DISABLE_TELEMETRY=1 node "$M" retrieve "<id>[,<id2>]"
```

Retrieve the specific guide plus the broader discipline guide when it applies
(`html`, `css`, `forms`, `accessibility`, `color`, `performance`, `security`).
Large output gets written to a temp file — read that file in full, don't `cat`
a truncated stream.

## 3. Check before concluding

- The implementation applies the guide's pattern **and** its fallback strategy.
- Nothing unrequested got added.
- If the guide contradicts what was there (a library doing what the platform
  now does natively), say so explicitly instead of silently rewriting.

## 4. legacy-scan (audit, not auto-fix)

```bash
DISABLE_TELEMETRY=1 node "$M" legacy-scan <path> [--include-docs-and-tests]
```

Deterministic rules cover ~20% of the corpus (38 of 209 guides). Every finding
carries `Keep when` / `Drop when` criteria and the tool warns that static
analysis is provisional — **read those criteria before touching the code**, then
verify the cited line by hand. It is not a linter; do not auto-apply.

Tested 2026-11-16 on `projects/preflight`: 2 findings, both genuine
(`AbortSignal.timeout()` for a single-abort `AbortController`; `toSorted()` for
a spread-then-sort on a typed array).

## Limits

- It's a guide lookup, not a compiler of browser support. If the target browsers
  matter, confirm against the compat data in the retrieved guide.
- The corpus stops at what the Chrome/Edge/Firefox/MDN teams curated. No guide
  found doesn't mean the legacy pattern is fine — it means no guidance exists.
