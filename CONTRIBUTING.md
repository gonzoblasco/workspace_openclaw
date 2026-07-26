# CONTRIBUTING.md — Open Source Contribution Guide

Estrategia y reglas para contribuir a proyectos open source.

---

## Filosofía

- No contribuir por contribuir. Buscar proyectos donde Gonzo ya usa o conoce el dominio — eso da velocidad y calidad.
- PRs chicos, bien hechos, semánticos, con tests. Mejor 3 PRs sólidos que 10 PRs de typo.
- En inglés siempre que el repo sea internacional.
- Commits semánticos (`feat`, `fix`, `test`, `docs`, `refactor`).
- Un PR por issue/feature. No mezclar concerns.
- Si el repo tiene CONTRIBUTING.md, leerlo antes de tocar nada.
- **Cada PR es evidencia de la metodología**: commits limpios, descripción clara, tests, referencias al issue. El PR mismo demuestra que sabés trabajar con IA como copiloto.

## Reglas de oro

1. **Forkear primero, clonar después.** Remote `origin` = upstream, `fork` = el tuyo.
2. **Branch naming:** `feature/[issue]-[descripcion-corta]` o `fix/[issue]-[descripcion]`
3. **Un PR por issue.** Si el cambio es grande, partir en PRs chicos.
4. **Tests.** Si el repo tiene tests, el PR incluye tests. Si no tiene, igual escribirlos.
5. **No romper CI.** Si el CI falla por algo del repo (no nuestro), mencionarlo en el PR pero no bloquear.
6. **Descripción del PR:** qué hace, por qué, cómo se verificó, qué falta. En inglés.
7. **Paciencia.** Los maintainers tienen vidas. Esperar 1-2 semanas antes de hacer follow-up.

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

## Criterios para elegir nuevos repos

1. **Gonzo ya usa el proyecto** — conoce el dominio, no arranca de cero
2. **Repo activo** — maintainers que responden, issues actualizados en los últimos 30 días
3. **Issues alcanzables** — `good first issue`, `help wanted`, o bugs/enhancement sin assignee
4. **Categorías donde Gonzo es fuerte:** React, Next.js, TypeScript, Supabase, tooling/scaffolding, accesibilidad, AI SDKs
5. **Tamaño del repo** — no contribuir a React core de entrada; proyectos medianos donde un PR se nota
6. **Valor de visibilidad** — ¿el repo lo miran recruiters/empresas del ecosistema donde quiere trabajar?

## Tracking

El estado detallado de cada contribución (PR registry, clasificación de repos, plan de ataque) está en [`docs/OSS-TRACKER.md`](./docs/OSS-TRACKER.md).

Por repo:
- `projects/[repo]/HANDOFF.md` — estado detallado por repo
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
