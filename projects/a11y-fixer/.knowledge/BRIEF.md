# BRIEF - a11y-fixer

**Estado:** Feature-complete hasta Fase 4 (40/40 tareas) - sin desarrollo desde 2026-08-17
**Última actualización:** 2026-09-14
**Ancla del pilar:** Accesibilidad como diferenciador (ADR-001)

## Qué es

Bot de auditoría de accesibilidad para PRs de GitHub. Corre axe-core dentro de Playwright (Chromium headless, en Docker) sobre cada pull request, detecta las violaciones **nuevas** comparando contra la baseline de main, y publica un comentario estructurado en el PR.

Sin lock-in de SaaS: todo corre en los runners de GitHub Actions del usuario. La IA (explicaciones de fixes) es opcional y BYOK (OpenAI / Anthropic / OpenRouter).

## Por qué es ancla

Es el puente entre la especialización a11y y el trabajo OSS. Demuestra tres cosas a la vez: dominio de axe-core y Playwright, integración real en CI/CD, y producto instalable por terceros. Es el proyecto que mejor encarna el pilar "accesibilidad como diferenciador" del ADR-001.

## Stack

TypeScript, GitHub Actions, Playwright, axe-core, Biome, Vitest, Docker. Publicado en npm como `@gonzoblasco/a11y-fixer`.

## Estado real (verificado 2026-09-14)

| Dato | Valor | Fuente |
|---|---|---|
| Versión | `0.6.0` | `package.json` |
| Último release | `v0.6.0` (2026-07-29) | GitHub releases |
| Publicado en npm | **sí** - `@gonzoblasco/a11y-fixer@0.6.0`, publicado 2026-07-29 | registry.npmjs.org |
| Último commit | `663a1ef` "chore: ignore .DS_Store" (2026-08-17) - solo chore, sin cambios de código | GitHub API |
| Último commit de código | 2026-07-28/29 (v0.5.x / v0.6.0) | CHANGELOG del repo |
| Tests | 102 passing | badge del README |
| Repo | `gonzoblasco/a11y-fixer` (público, MIT) | GitHub API |
| Estrellas | 0 | GitHub API |
| Issues abiertos | 2 (#10, #11) | GitHub API |

**Corrección de marco (2026-09-14):** el proyecto **no está abandonado a mitad de camino - está construido y publicado**. El TRACKER del repo marca **40/40 tareas** completas a través de las Fases 1-4 (core engine, thresholds, AI explainer, distribución y docs). Lo que falta no es código: es **adopción**.

**Nota operativa:** el código NO está clonado en el workspace - `projects/a11y-fixer/` contiene solo `.knowledge/`. Para trabajar en él hay que clonar el repo aparte. El repo sí tiene su propio `.knowledge/` (HANDOFF + session-context) versionado adentro.

## Features (v0.6.0, todas verificadas contra el repo)

- Detección automática de rutas (rutas definidas + páginas del App Router de Next.js cambiadas en el PR).
- Auditoría en browser real (axe-core dentro de Playwright Chromium, en Docker).
- Páginas autenticadas (cookies, headers HTTP o Bearer tokens).
- Comparación contra baseline (nuevas / arregladas / persistentes), con cache por artifact de GitHub Actions.
- Comentario estructurado en el PR (severidad de impacto, elementos afectados, fixes sugeridos).
- Umbrales configurables (impacto máximo, máximo de violaciones nuevas, target WCAG, reglas ignoradas).
- Ignore rules (por regla de axe y por selector CSS).
- Explicaciones con IA opcionales (BYOK, con fallback a template).
- Fixer engine con 3 niveles de fixabilidad: `auto` (patches deterministas), `suggest` (revisión humana), `explain` (no automatizable). 8 tipos de violación con patches.
- Modo CLI: `a11y-fixer audit|fix|suggest`.
- Sin dependencia de SaaS.
- Branding de Marketplace en `action.yml` (icon: eye, color: green).

## Next Steps - REVISADOS contra el repo (2026-09-14)

El HANDOFF del 2026-08-02 listaba 3 pasos. **Ninguno sigue vigente tal como está escrito:**

| Next Step del HANDOFF | Estado real |
|---|---|
| 1. Definir roadmap v0.7: baseline comparison, AI explanations, config validation | **Obsoleto al momento de escribirse.** Esas tres features ya estaban en v0.6.0 (released 29/07, el HANDOFF es del 02/08): baseline = Epic 1.5.3, AI explanations = Epic 3.1, config validation = Zod schema en Epic 1.1.3/1.1.4. El roadmap real (ROADMAP + TRACKER) ya existía y muestra 40/40. |
| 2. Abrir issues para gaps conocidos e invitar feedback | **Parcialmente hecho y con deuda:** los issues #10 y #11 existen, pero quedaron **abiertos** con sus checklists 100% completos. Falta cerrarlos. No hay invitación a feedback a terceros. |
| 3. Sumar session-context save al ritual de cierre | **Hecho:** el repo versiona su `.knowledge/` (HANDOFF + session-context) y tiene commits `docs: update session-context handoff` del 02/08. |

**Pendiente real, en orden:**

1. **Cerrar los issues #10 y #11** - ambos son epics de Fase 4 con todas las tareas `[x]`; quedaron abiertos. *(Acción en superficie pública: requiere OK explícito de Gonzo.)*
2. **Sincronizar los headers de estado del repo** - `docs/ROADMAP.md` dice "Phase 4 (In Progress)" y tiene todas las casillas sin marcar; `docs/TRACKER.md` dice "Status: Phase 0.4 (Planning)" con 40/40 abajo. Los dos headers quedaron viejos.
3. **Verificar la publicación en el Marketplace** - el Epic 4.1.2 dice hecho y `action.yml` tiene el branding, pero no pude confirmar la publicación (la página del Marketplace se renderiza por JS y el README no la menciona). **Sin verificar.**
4. Definir el próximo horizonte real: no es "v0.7 de features", es **adopción** (ver deuda abajo).

## Deuda / riesgo

- **Cero adopción.** 0 estrellas, 0 usuarios externos, y el criterio del Horizonte 1 de `docs/NORTH.md` es exactamente eso: una pieza con usuarios reales que no seas vos. **El proyecto está listo para eso y no lo está buscando.**
- **El ancla más fría de las tres.** Último commit 2026-08-17 (solo un chore de `.DS_Store`), último commit de código a fines de julio. kanam-forge y kanam-pulse tienen actividad más reciente.
- **Admin desincronizada:** issues de epics terminados abiertos, headers de estado viejos, casillas del ROADMAP sin marcar. Nada de esto bloquea, pero da una imagen de proyecto más verde de lo que es.
- **Publicado en npm pero sin README que lo mencione** - hay un canal de distribución activo que la documentación no explota.

## Constraint

- Inglés para issues/PRs/comments (regla de GitHub). Sin lock-in de SaaS para el core de auditoría.
