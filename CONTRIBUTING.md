# CONTRIBUTING.md — Playbook de Open Source

**Estrategia de Gonzo para ganar visibilidad como contributor open source**

---

## Filosofía

- No contribuir por contribuir. Buscar proyectos donde Gonzo ya usa o conoce el dominio — eso da velocidad y calidad.
- PRs chicos, bien hechos, semánticos, con tests. Mejor 3 PRs sólidos que 10 PRs de typo.
- En inglés siempre que el repo sea internacional.
- Commits semánticos (`feat`, `fix`, `test`, `docs`, `refactor`).
- Un PR por issue/feature. No mezclar concerns.
- Si el repo tiene CONTRIBUTING.md, leerlo antes de tocar nada.

## Cómo pedirle a una sesión nueva que trabaje en un repo externo

### Prompt base (copiar y adaptar)

> Quiero trabajar como contributor en un proyecto open source. Te paso el contexto:
>
> - **Repo:** github.com/[org]/[repo]
> - **Issue:** #[n] — [título del issue]
> - **Fork:** github.com/gonzoblasco/[repo] (forkear si no existe)
> - **Clonar en:** `projects/[repo]`
>
> 1. Leé el CONTRIBUTING.md del repo y su estructura de plugins/sistema
> 2. Leé el issue y los comentarios del maintainer
> 3. Implementá el cambio siguiendo sus convenciones
> 4. Verificá build, lint, tests
> 5. Commits semánticos, un PR por issue
> 6. Abrí el PR referenciando el issue

### Archivo de contexto por repo

Cada repo donde contribuimos tiene su propio `HANDOFF.md` en `projects/[repo]/HANDOFF.md` con:
- Qué se hizo hasta ahora
- Qué PRs están abiertos
- Qué sigue en el plan
- Estructura del repo para referencia

## Reglas de oro

1. **Forkear primero, clonar después.** Remote `origin` = upstream, `fork` = el tuyo.
2. **Branch naming:** `feature/[issue]-[descripcion-corta]` o `fix/[issue]-[descripcion]`
3. **Un PR por issue.** Si el cambio es grande, partir en PRs chicos.
4. **Tests.** Si el repo tiene tests, el PR incluye tests. Si no tiene, igual escribirlos.
5. **No romper CI.** Si el CI falla por algo del repo (no nuestro), mencionarlo en el PR pero no bloquear.
6. **Descripción del PR:** qué hace, por qué, cómo se verificó, qué falta. En inglés.
7. **Paciencia.** Los maintainers tienen vidas. Esperar 1-2 semanas antes de hacer follow-up.

## Pipeline de repos objetivos

### En progreso

| Repo | Issue | PR | Estado |
|------|-------|-----|--------|
| akd-io/create-next-stack | #262 Bun | [#280](https://github.com/akd-io/create-next-stack/pull/280) | Esperando review |
| akd-io/create-next-stack | #224 Vitest | — | Plan, en ~2 semanas |
| akd-io/create-next-stack | #249 Supabase | — | Plan, después de Vitest |
| akd-io/create-next-stack | #268 Auth.js + ShadCN | — | Plan |
| akd-io/create-next-stack | #272 Architecture review | — | Plan (el golazo) |

### Criterios para elegir nuevos repos

1. **Gonzo ya usa el proyecto** — conoce el dominio, no arranca de cero
2. **Issues con label `good first issue` o `help wanted`** — la puerta está abierta
3. **Repo activo** — maintainers que responden (no repos abandonados)
4. **Categorías donde Gonzo fuerte:** React, Next.js, TypeScript, Supabase, tooling/scaffolding, accesibilidad
5. **Tamaño del repo** — no contribuir a React core de entrada; empezar en proyectos medianos donde un PR se nota

### Ideas de repos para el futuro (sin compromiso)

- **Vercel/next.js** — documentation PRs, examples. Difícil pero mucho impacto.
- **supabase/supabase** — docs, examples, bugs en JS client. Gonzo lo usa diario.
- **shadcn-ui/ui** — accesibilidad + React. Gonzo la usa en SoporteML.
- **TanStack** (Router, Query) — Gonzo los usa en kanamai, reactiva, umbrawriter
- **biomejs/biome** — tooling, Gonzo lo usa en CSN
- **openai/openai-node** — SDK que Gonzo usa en varios proyectos
- **vitest-dev/vitest** — Gonzo lo usa en CSN, podría contribuir docs o bugs

## Tracking

El estado de cada repo se guarda en:
- `projects/[repo]/HANDOFF.md` — estado detallado por repo
- `projects/PROYECTOS.md` — sección "Colaboración externa" con tabla resumen
- `memory/YYYY-MM-DD.md` — diario de cada sesión
- `MEMORY.md` — contexto de largo plazo

## Sesiones por proyecto

Una sesión de OpenClaw por repo externo. Al arrancar:
1. Leer `projects/[repo]/HANDOFF.md`
2. Leer el issue objetivo
3. Clonar/fetche el repo si no está
4. Trabajar siguiendo las reglas de oro

Al cerrar:
1. Actualizar `HANDOFF.md` del repo
2. Actualizar `memory/YYYY-MM-DD.md`
3. Commit + push del workspace