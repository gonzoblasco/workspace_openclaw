# BRIEF - a11y-fixer

**Estado:** Activo (v0.6.0) - sin desarrollo desde 2026-08-17
**Última actualización:** 2026-09-14
**Anchor del pilar:** Accesibilidad como diferenciador (ADR-001)

## Qué es

Bot de auditoría de accesibilidad para PRs de GitHub. Corre axe-core dentro de Playwright (Chromium headless, en Docker) sobre cada pull request, detecta las violaciones **nuevas** comparando contra la baseline de main, y publica un comentario estructurado en el PR.

Sin lock-in de SaaS: todo corre en los runners de GitHub Actions del usuario. La IA (explicaciones de fixes) es opcional y BYOK (OpenAI / Anthropic / OpenRouter).

## Por qué es ancla

Es el puente entre la especialización a11y y el trabajo OSS. Demuestra tres cosas a la vez: dominio de axe-core y Playwright, integración real en CI/CD, y producto instalable por terceros. Es el proyecto que mejor encarna el pilar "accesibilidad como diferenciador" del ADR-001.

## Stack

TypeScript, GitHub Actions, Playwright, axe-core, Biome, Vitest, Docker.

## Estado real (verificado 2026-09-14)

| Dato | Valor | Fuente |
|---|---|---|
| Versión | `0.6.0` | `package.json` |
| Último release | `v0.6.0` - Fixer Engine, CLI, Docker Action (2026-07-29) | GitHub releases |
| Último push | 2026-08-17 | GitHub API |
| Tests | 102 passing | badge del README |
| Repo | `gonzoblasco/a11y-fixer` (público, MIT) | GitHub API |
| Estrellas | 0 | GitHub API |
| Última sesión de trabajo | 2026-08-02 | `.knowledge/session-context.json` |

**Nota:** el código NO está clonado en el workspace - `projects/a11y-fixer/` contiene solo `.knowledge/`. Para trabajar en él hay que clonar el repo aparte.

## Features (v0.6.0)

- Detección automática de rutas (rutas definidas + páginas del App Router de Next.js cambiadas en el PR).
- Auditoría en browser real (axe-core dentro de Playwright Chromium, en Docker).
- Páginas autenticadas (cookies, headers HTTP o Bearer tokens).
- Comparación contra baseline (nuevas / arregladas / persistentes).
- Comentario estructurado en el PR (severidad de impacto, elementos afectados, fixes sugeridos).
- Umbrales configurables (impacto máximo, máximo de violaciones nuevas, target WCAG, reglas ignoradas).
- Explicaciones con IA opcionales (BYOK).
- Sugerencias de fix (auto-aplicables con patch, suggest-level con HTML de reemplazo).
- Modo CLI: `a11y-fixer audit|fix|suggest`.
- Sin dependencia de SaaS.

## Next Steps (del HANDOFF del 2026-08-02, sin revisar)

1. Definir el roadmap v0.7: comparación de baseline, explicaciones con IA, validación de config.
2. Abrir issues para los gaps conocidos e invitar feedback.
3. Sumar el guardado de session-context al ritual de cierre del proyecto.

## Deuda / riesgo

- **Es el ancla más fría de las tres.** Última actividad 2026-08-17, última sesión registrada 2026-08-02; kanam-forge y kanam-pulse tienen BRIEF y actividad más reciente.
- **Cero usuarios externos** (0 estrellas). El criterio del Horizonte 1 de `docs/NORTH.md` es exactamente eso: una pieza con usuarios reales que no seas vos. Es el candidato natural a empujar, pero hoy no está en movimiento.
- Los Next Steps son del 02/08 - conviene revisarlos antes de retomar, no asumirlos vigentes.

## Constraint

- Inglés para issues/PRs/comments (regla de GitHub). Sin lock-in de SaaS para el core de auditoría.
