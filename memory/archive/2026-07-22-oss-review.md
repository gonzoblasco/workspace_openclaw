# 2026-07-22 — OSS PR Review + create-stack diagnóstico

## OSS PR Review

Revisé los 20 PRs abiertos de Gonzo en OSS. Todos siguen esperando review de maintainers:
- **radix-ui/primitives #4053** — Select focus freeze en Dialog, CI pendiente
- **TanStack/router #7861** — MatchInner throw undefined, ✅ CodeRabbit
- **vercel/ai #17274** — reasoning tokens warning, ✅ Vercel Agent Review
- **shadcn-ui/ui #11179, #11180, #11187** — todos ✅ Signed commits, esperando
- **akd-io/create-next-stack #280-#289** — 10 PRs, todos ✅ GitGuardian, 0 reviews
- **t3-oss/create-t3-app #2239** — biome ignore generated, CI verde completo
- **shuding/nextra #5029** — select modal={false}
- **payloadcms/payload #17413, #17342** — ambos ✅ Socket, esperando

Ningún maintainer ha comentado. Sin cambios solicitados.

## Decisión: create-next-stack (akd-io)

Gonzo está considerando cerrar los 10 PRs de create-next-stack. Su percepción: "esa gente tiene poca ganas de mejorar, pero se consiguieron un buen nombre". Prefiere enfocarse en su propio `@gonzoblasco/create-stack`.

**Decisión tomada:** No cerré los PRs — es decisión de Gonzo. Queda pendiente para cuando vuelva.

## Diagnóstico de create-stack

Exploré `@gonzoblasco/create-stack` (v0.8.1, publicado en npm hace 2 días):

### Estado
- ✅ CLI funcional con stacks modulares (`next`, `api`)
- ✅ Publicado en npm como `@gonzoblasco/create-stack`
- ✅ 67 tests, Biome lint, TypeScript estricto
- ✅ AI-Native: AGENTS.md, OpenSpec, .openclaw/ config
- ✅ CI/CD con GitHub Actions
- ✅ Repo renombrado a `create-stack`
- ✅ Release v0.8.1 en GitHub
- ⭐ 1 star en GitHub

### Diferenciadores vs create-next-stack
- **Multi-stack** (no solo Next.js)
- **AI-Native** (AGENTS.md, OpenSpec, prompts inyectados)
- **Biome** (no ESLint + Prettier)
- **TypeScript estricto** con `noUncheckedIndexedAccess`
- **Sin dependencias pesadas** (solo @clack/prompts + picocolors)
- **Scoped package** (`@gonzoblasco/create-stack`)

### Lo que falta para v1.0.0
- Sitio de documentación (VitePress o Nextra)
- Video demo de onboarding
- Tests de integración multi-package manager en CI
- Congelamiento de API

### Observación
create-stack ya tiene lo que los PRs de create-next-stack intentaban agregar: Vitest, Playwright, Supabase, Auth.js, shadcn/ui, Zustand, ESLint strict, prettier-plugin-organize-imports, Bun support. La diferencia es que create-stack lo resuelve con stacks modulares en vez de flags individuales.
