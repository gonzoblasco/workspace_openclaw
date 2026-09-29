# CONTRIBUTING.md - Open Source Contribution Guide

Estrategia y reglas para contribuir a proyectos open source.

---

## Filosofía

- No contribuir por contribuir. Buscar proyectos donde Gonzo ya usa o conoce el dominio - eso da velocidad y calidad.
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

## Aislar el trabajo (worktrees, no projects/)

Los repos OSS **no** se clonan en `projects/` (esa carpeta es para proyectos propios con doble git). Se trabaja aislado:

- **Git worktree** del workspace, o `mktemp -d` para clones sueltos.
- Nunca modificar el repo del proyecto directamente sin approval explícito.
- Limpiar con `trash` (no `rm -rf`).

## Antes de responder cualquier link de issue/PR: chequear contexto interno

**Regla (lecciones 2026-09-09 y 2026-09-10, carbon #16031):** antes de responder, resumir o actuar sobre cualquier URL de issue/PR, hacer DOS chequeos en orden:

1. **Contexto interno:** `memory_search()` por el numero de issue/repo.
2. `sessions_search()` por el numero de issue/repo.
3. Si participamos (comentario propio, verificacion, seguimiento): la respuesta se contextualiza con NUESTRO rol en el hilo. Ejemplo real: el cierre del issue es "che, tu comentario sirvio para que lo cierren", no un resumen del PR como si fuera nuevo.
4. **Hilo externo completo:** leer body, TODOS los comentarios e interacciones (incluidos reviews e inline comments), estado actual y eventos de cierre. Nunca responder basandose solo en el comentario/enlace compartido: el contexto que Gonzo manda es el punto de partida, no el hilo completo.

Presentar como novedad algo en lo que ya actuamos repite trabajo, pierde el hilo de seguimiento y obliga a Gonzo a corregirme. Dos veces seguidas es suficiente leccion.

## Alcance: un ticket por vez

**Regla (leccion 2026-09-14):** cuando Gonzo comparte la URL de un ticket, el analisis y la respuesta cubren **solo ese ticket**.

- **No arrastrar** estado, comparaciones ni follow-ups de otros PRs del mismo repo, aunque sean vecinos, del mismo ciclo o esten linked.
- **No cerrar** un ticket porque se resolvio otro: cada uno tiene su propio estado y su propio hilo de contexto. Cerrar o dar por resuelto un ticket que Gonzo no pidio rompe la consistencia del seguimiento.
- **Excepcion unica:** el ticket compartido depende de otro (PR linked, blocker de CI, dependencia de merge). Se menciona lo estrictamente necesario para ese ticket, no el estado del otro.
- Si hay algo relevante de otro ticket, se deja como nota aparte o como TODO, nunca dentro de la respuesta del ticket pedido.

### Referencia si, sentencia no

Cada ticket es una **entidad individual** salvo que Gonzo pida lo contrario. La distincion operativa:

- **Valido:** referenciar trazabilidad - "esto ya se trabajo en el ticket #X". Es dato util, le dice a Gonzo donde vive el hilo.
- **Invalido:** concluir sobre ese otro ticket - declararlo abierto, cerrado, mergeado, bloqueado o resuelto. Dar por A o por B es afirmar un estado que no se pidio y que puede estar desactualizado.
- Si el estado de otro ticket importa de verdad para la respuesta, se **verifica en el momento** con la fuente real (`gh pr view`, el hilo externo) y se presenta como dato verificado con su URL - no como memoria ni como inferencia.

## Antes de clasificar o empujar un PR: leer TODO

**Regla crítica (lección 2026-08-22):** antes de empujar, cerrar, o clasificar un PR, leer **todos** los comentarios, incluidos los **inline comments de código** y las **reviews**. El feedback real del maintainer vive ahí y puede cambiar la decisión por completo.

- `gh pr view --json comments` solo muestra los comments generales.
- Los inline comments (`gh api repos/OWNER/REPO/pulls/N/comments`) y las reviews (`--json reviews`) llevan el feedback real.
- Error típico: clasificar como "empujable" un PR que el maintainer ya rechazó as-is, o como "esperando reviewer" uno cuyo inline comment ya está resuelto.

## Cierre de PRs stale

Si un PR lleva **~1 mes sin review del maintainer** (y no hay señal de que vaya a avanzar), cerrarlo con un comentario de cierre cortés. Pasos:

1. Verificar que el fix no fue absorbido por `main` (lección: verificar contra main antes de force-pushear rebases viejos).
2. Cerrar el issue si aplica, con comentario agradeciendo y explicando el cierre.
3. Eliminar la branch remota.
4. Actualizar `docs/OSS-TRACKER.md` (regenerar con `./scripts/memory-db.sh export-oss`).

## Cómo pedirle a una sesión nueva que trabaje en un repo externo

### Prompt base (copiar y adaptar)

> Quiero trabajar como contributor en un proyecto open source. Te paso el contexto:
>
> - **Repo:** github.com/[org]/[repo]
> - **Issue:** #[n] - [título del issue]
> - **Fork:** github.com/gonzoblasco/[repo] (forkear si no existe)
> - **Aislar en:** git worktree o `mktemp -d`
>
> 1. Leé el CONTRIBUTING.md del repo y su estructura de plugins/sistema
> 2. Leé el issue y los comentarios del maintainer (incluidos inline y reviews)
> 3. Implementá el cambio siguiendo sus convenciones
> 4. Verificá build, lint, tests
> 5. Commits semánticos, un PR por issue
> 6. Abrí el PR referenciando el issue

## Criterios para elegir nuevos repos

1. **Gonzo ya usa el proyecto** - conoce el dominio, no arranca de cero
2. **Repo activo** - maintainers que responden, issues actualizados en los últimos 30 días
3. **Issues alcanzables** - `good first issue`, `help wanted`, o bugs/enhancement sin assignee
4. **Categorías donde Gonzo es fuerte:** React, Next.js, TypeScript, Supabase, tooling/scaffolding, accesibilidad, AI SDKs
5. **Tamaño del repo** - no contribuir a React core de entrada; proyectos medianos donde un PR se nota
6. **Valor de visibilidad** - ¿el repo lo miran recruiters/empresas del ecosistema donde quiere trabajar?

## Tracking

El estado detallado de cada contribución (PR registry, clasificación de repos, plan de ataque) está en [`docs/OSS-TRACKER.md`](./docs/OSS-TRACKER.md) (generado desde la DB, regenerar con `./scripts/memory-db.sh export-oss`).

Por repo:
- `docs/OSS-TRACKER.md` - PR registry y estado por repo
- `memory/YYYY-MM-DD.md` - diario de cada sesión
- `MEMORY.md` - contexto de largo plazo

## Sesiones por proyecto

Una sesión de OpenClaw por repo externo. Al arrancar:
1. Leer `docs/OSS-TRACKER.md` para el estado del repo
2. Leer el issue objetivo y todos sus comments (incluidos inline y reviews)
3. Aislar el trabajo (worktree o `mktemp -d`)
4. Trabajar siguiendo las reglas de oro

Al cerrar:
1. Actualizar `docs/OSS-TRACKER.md` (regenerar con `./scripts/memory-db.sh export-oss`)
2. Actualizar `memory/YYYY-MM-DD.md`
3. Commit + push del workspace
