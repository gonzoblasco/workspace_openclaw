# BRIEF - a11y-fixer

**Estado:** ARCHIVADO (2026-09-14, decision de Gonzo). Feature-complete hasta Fase 4 (40/40 tareas)
**Última actualización:** 2026-09-14 (tras la enmienda de ADR-001)
**Rol en el portfolio:** ~~Ancla del pilar Accesibilidad~~ - **archivado, sale de la tabla de anclas** (ADR-001 seccion 6). Su sucesor es `kanam-fixer`, proyecto nuevo con alcance sin definir.

## Qué es

Bot de auditoría de accesibilidad para PRs de GitHub. Corre axe-core dentro de Playwright (Chromium headless, en Docker) sobre cada pull request, detecta las violaciones **nuevas** comparando contra la baseline de main, y publica un comentario estructurado en el PR.

Sin lock-in de SaaS: todo corre en los runners de GitHub Actions del usuario. La IA (explicaciones de fixes) es opcional y BYOK (OpenAI / Anthropic / OpenRouter).

## Por que fue ancla (y por que ya no lo es)

**Fue** el ancla del pilar "accesibilidad como diferenciador". Es el puente entre la especializacion a11y y el trabajo OSS: demuestra dominio de axe-core y Playwright, integracion real en CI/CD, y producto instalable por terceros.

**El 2026-09-14 Gonzo decidio archivarlo** y que su sucesor sea `kanam-fixer`, un proyecto **nuevo** (no un renombre). El alcance de `kanam-fixer` esta sin definir, y **no se asume** que herede el rol de engine de fixes a11y. Consecuencia: el pilar Accesibilidad queda **sin ancla formal** hasta que ese alcance se defina. Ver ADR-001 seccion 6 (la enmienda agrega; el texto original de la seccion 3 se conserva por trazabilidad).

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
| 2. Abrir issues para gaps conocidos e invitar feedback | **Parcialmente hecho.** Los issues #10 y #11 existen. **#11 cerrado el 2026-09-14** (documentación verificada completa: `CONTRIBUTING.md` + los 4 ejemplos existen). **#10 sigue abierto y NO debe cerrarse** - su premisa es falsa (ver punto 3). Nunca se invitó feedback a terceros. |
| 3. Sumar session-context save al ritual de cierre | **Hecho:** el repo versiona su `.knowledge/` (HANDOFF + session-context) y tiene commits `docs: update session-context handoff` del 02/08. |

**Pendiente real, en orden:**

1. **Publicar en el Marketplace** (el paso que falta de verdad). El Epic 4.1.2 lo declara hecho **y es falso**: verificado el 2026-09-14, el action **no está publicado**. Detalle en "Hallazgo verificado" abajo. Es el único bloqueante para cerrar #10.
2. **Sincronizar los headers de estado del repo** - `docs/ROADMAP.md` dice "Phase 4 (In Progress)" y tiene todas las casillas sin marcar; `docs/TRACKER.md` dice "Status: Phase 0.4 (Planning)" con 40/40 abajo. Los dos headers quedaron viejos. *(Requiere escribir en el repo: pedir OK a Gonzo.)*
3. **Corregir las dos afirmaciones falsas en los docs del repo** - el check `4.1.2` del issue #10 y del TRACKER dicen que la publicación está hecha; `docs/ROADMAP.md` lista hechas features que existen. *(Mismo caso: pedir OK.)*
4. Definir el próximo horizonte real: no es "v0.7 de features", es **adopción** (ver deuda abajo).

## Hallazgo verificado: el Marketplace (2026-09-14)

**El action NO está publicado en GitHub Marketplace.** Verificado con prueba de control, porque el fetch directo no alcanzaba (la página se renderiza por JS):

| URL probada | HTTP |
|---|---|
| `marketplace/actions/checkout` (control positivo) | 200 |
| `marketplace/actions/definitely-not-a-real-action-xyz123` (control negativo) | 404 |
| `marketplace/actions/a11y-fixer` | **404** |
| `marketplace/actions/a11y-fixer-action` | **404** |
| `marketplace/actions/gonzoblasco-a11y-fixer` | **404** |

Los dos controles prueban que el patrón de URL es correcto; el 200 de `checkout` descarta que el endpoint esté caído. Además, en el listado de acciones de accesibilidad del Marketplace aparecen `a11y-check`, `a11yguard`, `a11ytester-action`, `accessibility-scanner` y otros - **`a11y-fixer` no aparece**.

**Consecuencia:** el check `4.1.2` ("Publish action on GitHub Marketplace") está marcado `[x]` en el issue #10 y en `docs/TRACKER.md`, pero **nunca se hizo**. El branding en `action.yml` (icon: eye, color: green) es el *preparativo* para publicar, no la publicación. Los otros dos checks del #10 (README con badges, template de quickstart) sí están hechos y verificados.

**Lo que falta para publicar** (requiere acción de Gonzo en la UI de GitHub, no es automatizable): cortar un release nuevo con la opción "Publish this Action to the GitHub Marketplace" tildada. El release actual (v0.6.0) se publicó sin eso.

## Deuda / riesgo

- **Archivado el 2026-09-14 (ADR-001 seccion 6).** Esta es la decision mas importante del documento: todo lo de abajo describe el estado del proyecto al momento de archivarlo.
- **Estado de cierre incompleto:** el repo `gonzoblasco/a11y-fixer` sigue con `isArchived=false` en GitHub (no se archivo en la plataforma) y el paquete npm `@gonzoblasco/a11y-fixer@0.6.0` sigue publicado. Los dos son parte de los pendientes de la enmienda (todo id=54).
- **Cero adopcion.** 0 estrellas, 0 usuarios externos. El criterio del Horizonte 1 de `docs/NORTH.md` -una pieza con usuarios reales que no seas vos- **nunca se alcanzo**: el proyecto estaba tecnicamente listo y no lo busco. Ese aprendizaje se transfiere a kanam-fixer.
- **Fue la mas fria de las tres anclas.** Ultimo commit 2026-08-17 (solo un chore de `.DS_Store`), ultimo commit de codigo a fines de julio.
- **Admin desincronizada:** headers de estado viejos y casillas del ROADMAP sin marcar. Nada de esto bloquea, pero da una imagen de proyecto más verde de lo que es.
- **Dos afirmaciones falsas en los docs del repo:** el check `4.1.2` del issue #10 y de `docs/TRACKER.md` afirman que el action está publicado en el Marketplace, y no lo está. Una tarea marcada como hecha que nunca se hizo es peor que una tarea abierta: infla el progreso real del proyecto.
- **Publicado en npm pero sin README que lo mencione** - hay un canal de distribución activo que la documentación no explota.

## Constraint

- Inglés para issues/PRs/comments (regla de GitHub). Sin lock-in de SaaS para el core de auditoría.
