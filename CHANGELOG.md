# CHANGELOG.md

## [2026-07-16] — Consolidación de memoria (cron job)

### Qué se consolidó a MEMORY.md

De los diarios del 14 al 16 de julio:

**Open Source pipeline actualizado:**
- shadcn-ui/ui: +1 PR (#11198 InputOTP layout shift, approach alternativo). #11179 conflicto resuelto + commit firmado SSH.
- TanStack/router: PR #7818 cerrado (rechazado por maintainer por automatización). PR nuevo #7834 (safeStringify).
- vercel/ai: #17274 fix warnings dropeadas, review de Vercel addressada.
- payloadcms/payload: #17342 (data loss bug en Lexical rich text). Fix de 57 líneas, CI verde. Lecciones: complex issue ≠ complex fix, fork before push, type-check en shallow clones.
- facebook/astryx: 2 PRs nuevos (#4022 WCAG, #4023 keyboard) + 2 RFC comments.
- shuding/nextra: #5029 (Select scroll lock).
- Total: ~22 PRs abiertos en 9 repos.
- oss-contribute: Phase 6 (batch PR check) agregada. PR registry en CONTRIBUTING.md.

**SoporteML v2:**
- Phase 2 (MeLi Integration + Auto-learn): 6 EFs escritas, deployadas localmente. Onboarding flow 4 pasos.
- Phase 3 (Inbox UI): layout dos columnas, tabs, SLA, búsqueda, keyboard nav pendiente.
- División Mini/Air abolida (modelo deepseek-v4-flash como default).

**create-stack-next:**
- v0.7.2: templates actualizados para Biome 2.5, TS 7 en proyecto (templates mantienen TS 5.x por incompatibilidad Next.js 15 + TS 7).
- Dirección acordada: expansión con `--template node`, no reemplazo.

**accessible-ui:**
- 3 bugs fixeados, 52 tests nuevos. Scope @gonzoblasco/. Pendiente: npm publish.

**Nuevas skills:**
- product-reset: reset de producto post-lanzamiento (genérica, con ejemplo CSN).
- openspec-creator: specs OpenSpec as-built y delta.
- session-closure: ritual de cierre de sesión.

**Lecciones nuevas:**
- Next.js 15 + TS 7 incompatibles.
- Complex issue ≠ complex fix (payloadcms).
- DeepSeek v4 Flash como modelo default (costo/beneficio).
- TanStack/router: estética del proceso importa en repos Tier 0.
- CSN: expansión, no reemplazo.
- accessible-ui: edge cases en componentes headless.
- Scope @gonzoblasco/ para npm.

### Limpieza
- Sección duplicada "Lecciones aprendidas" eliminada de MEMORY.md.

## [2026-07-16] — pr_vscode_niveles: repo no existía

### Situación
- Intenté hacer push a `pr_vscode_niveles` y falló
- MEMORY.md lo marca como 🧊 FREEZER, pero asumí que el repo ya existía en GitHub

### Diagnóstico
```bash
gh repo view gonzoblasco/pr_vscode_niveles
# → "Could not resolve to a Repository"
```

### Acción
- Proyecto local en `/Users/gonzoblasco/.openclaw/workspace/projects/pr_vscode_niveles`
- Creé repo privado en GitHub:
  ```bash
  gh repo create gonzoblasco/pr_vscode_niveles --private --source=. --push
  ```
- Fix de remote (ya existía `origin`):
  ```bash
  git remote set-url origin git@github.com:gonzoblasco/pr_vscode_niveles.git
  git push -u origin main
  ```

### Resultado
- Repo creado: https://github.com/gonzoblasco/pr_vscode_niveles (privado)
- Remote `origin` configurado
- Push inicial de `main` realizado ✅

### Lección
No asumir que un proyecto "FREEZER" tiene repo remoto existente. Verificar con `gh repo view` antes de intentar push. Si es proyecto congelado sin repo, crearlo explícitamente.

## [2026-07-15] — Cierre de sesión CSN + CNS

### Resumen final
- 5 PRs abiertos en akd-io/create-next-stack en una sola noche:
  - #280 Bun (#262), #281 React.FC (#277), #282 Vitest (#224), #283 Supabase (#249), #284 Auth.js + shadcn/ui (#268)
- Todos con build, lint, unit tests (9/9) verdes — ~500 líneas de código total
- CONTRIBUTING.md creado como playbook de OSS
- HANDOFF.md del repo con plan completo
- Skill oss-contribute ya existía y cubrió todo el workflow — no se necesitó nada nuevo
- Próximos pasos: Architecture review (#272), OpenSpec como feature propuesta

## [2026-07-14] — Actualización general del workspace

### SoporteML — análisis de arquitectura
- Revisión completa del código: 14 páginas, 30+ componentes, 25 Edge Functions, 54 migraciones, 24 tablas
- EL-1 a EL-5 en código: billing MP escrito pero NUNCA operativo (mockeado, sin secrets configurados), KB con pgvector, RAG en copiloto, Analytics, Settings, hardening
- Propuesta de workflow sin backend local: SDD con OpenSpec + documentar API remota + git como bridge
- Próximo feature planificado: hilos unificados + resumen IA (plan.md existe)

### Actualización de MDs del workspace
- **MEMORY.md:** SoporteML actualizado (billing operativo, EL-5 completo, 24 tablas, 25 EFs, URL Supabase), sección OSS expandida (akd-io 5 PRs, shadcn 2 PRs, TanStack 1 PR, vercel/ai 3 reviews, commit signing SSH, skills creadas), lecciones aprendidas agregadas (triaje PRs, reviews ajenos, shadcn registry, TanStack monorepo, vercel/ai breaking changes)
- **PROYECTOS.md:** CSN v0.7.1 con 64 tests, SoporteML con billing operativo y EL-5, tabla de colaboraciones externa con 4 repos y 8 PRs totales, pendientes actualizados (SoporteML hilos, SDD workflow, memory index rebuild)
- **USER.md:** onboarding completo, perfil real (fullstack, IA-asistida, stack opinado, accesibilidad, OSS)
- **IDENTITY.md:** género femenino (ya estaba hecho)
- **memory/2026-07-14.md:** sección SoporteML + actualización general agregada

### Género de Kanam
- Gonzo decidió tratar a Kanam en femenino (ella)
- IDENTITY.md, MEMORY.md y diario actualizados

## [2026-07-14] — Sesión CSN + CNS

### create-next-stack (akd-io) — estrategia de colaboración
- Gonzo encontró `create-next-stack` en npm — se pisa con nuestro CSN pero con filosofía distinta
- Decisión: colaborar en lugar de competir. CSN queda como "fork opinado" / laboratorio
- Repo forkeado: github.com/gonzoblasco/create-next-stack
- Clonado en `projects/create-next-stack` (rama develop como base)

### PR #280 — Bun support (#262)
- Plugin `bun.ts` creado, adaptado al sistema de plugins de akd-io
- 9 archivos modificados, +90/-2 líneas
- Commits semánticos: `feat(cli)` + `test(e2e)`
- Build, lint, unit tests (9/9) — todo verde
- PR abierto: https://github.com/akd-io/create-next-stack/pull/280
- CI: GitGuardian ✅, Vercel CI awaiting maintainer approval (normal para PRs externos)

### Plan de próximos PRs
- Vitest (#224) — en ~2 semanas si no hay respuesta al PR de Bun
- Supabase (#249), Auth.js + ShadCN (#268), Architecture review (#272)
- OpenSpec como feature propuesta después de 2-3 PRs merged
- Website de CNS en el freezer (deuda moral)

### Organización de sesiones
- Gonzo decidió tener una sesión de OpenClaw por proyecto
- Esta sesión = CSN + CNS exclusivamente

### Archivos modificados
- `memory/2026-07-14.md` — actualizado con sección completa de CNS
- `MEMORY.md` — sección create-next-stack (akd-io) agregada
- `projects/PROYECTOS.md` — sección "Colaboración externa" agregada
- `CHANGELOG.md` — esta entrada

## [2026-07-14]

### Nueva estructura del workspace
- Creado `FREEZER.md` — ideas congeladas (marketplace de servicios domésticos como primera entrada)
- `MEMORY.md` actualizado: definición ampliada de KanamAI (pre/post/durante/marketplace), referencia a FREEZER.md
- `.gitignore` del workspace creado (excluye `projects/`, `.DS_Store`, `node_modules/`, etc.)
- Commit inicial del repo del workspace (1fb87f4) — solo configuración, sin proyectos
- Diario `memory/2026-07-14.md` creado

## [2026-07-14]

### Nuevo proyecto analizado: mucamas-online
- Gonzo trajo un esqueleto de marketplace de servicios domésticos al workspace
- Análisis del ecosistema: los 3 SaaS son "retención", este sería "marketplace"
- Decisión: congelar como idea (FREEZER.md), no sumar 4to producto ahora
- Definición ampliada de KanamAI: pre/post/durante/marketplace — "IA que facilita conexiones humanas en distintos momentos"

### Sincronización del workspace entre máquinas
- Repo creado: `git@github.com:gonzoblasco/workspace_openclaw.git`
- `.gitignore` del workspace: proyectos excluidos (cada uno se sincroniza con su propio repo)
- Workflow agregado a AGENTS.md: cambios en config del workspace → commit + push obligatorio
- Push inicial realizado (2 commits)
- Sesiones viven localmente por máquina, los MDs del workspace son la memoria compartida

### Archivos creados/modificados
- `FREEZER.md` — creado
- `MEMORY.md` — actualizado
- `.gitignore` — creado
- `AGENTS.md` — actualizado (Workspace Git)
- `memory/2026-07-14.md` — creado

## [2026-07-13]

### Onboarding inicial
- Definición de identidad: Kanam 🌿, asistente de Gonzalo
- Forma de trabajo: registro en MEMORY.md, diarios, PROYECTOS.md, HANDOFF, CHANGELOG
- Heartbeat cada 1h activado (HEARTBEAT.md)
- Cron job cada 3 días para consolidación de memoria (job ID: a6b2adb8-4b77-436a-b73c-2c866ac512f3)

### Proyectos
- Mapeo completo del ecosistema: 5 productos principales + 5 de soporte
- Limpieza del workspace: 9 carpetas eliminadas (vacías, incompletas o fuera de foco)
- Clonados de GitHub: kanamai (de kanamai-330ca8a9), reactiva, brainweb (de brainweb-your-second-mind), umbrawriter
- PROYECTOS.md creado y actualizado con índice maestro
- Pendiente: normalización de nombres, documentación de proyectos sin docs, .gitignore global para .DS_Store

## [2026-07-15] — OpenSpec en SoporteML

### Spec-Driven Development en proyecto brownfield
- OpenSpec 1.6.0 inicializado en SoporteML con config custom (contexto, reglas en español)
- 3 specs as-built escritos y validados:
  - **inbox** (6 requirements): bandeja, agrupación, absorción priority, SLA, teclado, realtime
  - **ai-copilot** (7 requirements): RAG, auth, tono, instrucciones, sugerencias CRM, errores, autopilot
  - **billing-mp** (5 requirements): suscripciones, webhook, HMAC, estados, secrets (con nota: nunca operativo)
- Commit en SoporteML: `b4bfba0`
- Próximo: delta spec para hilos unificados + resumen IA

### Delta spec archivada — feature ya implementada
- Al investigar para implementar, descubrimos que la feature completa ya existía en código
- Delta spec ajustada: solo `thread-summary` como capability nueva (inbox sin cambios)
- Archivada con `openspec archive` → spec as-built `thread-summary` creado (3 requirements)
- Estado final: 4 specs as-built, 0 changes activos
- Branch `feature/unified-threads-ai-summary` creado — primera vez usando branch por feature
- Lección: en brownfield, verificar si el feature ya existe antes de escribir delta spec

## [2026-07-16] — OpenSpec + Skills

### Added
- Skill `openspec-creator`: crear specs OpenSpec as-built y delta, guiando paso a paso
- Skill `session-closure`: ritual de cierre de sesión automatizado
- Spec as-built para `meli-webhook` en SoporteML v1 (182 líneas, 9 requisitos)
- Spec as-built para `CLI interactivo` en create-stack-next (234 líneas, 9 requisitos)
- OpenSpec inicializado en raíz de create-stack-next

### Changed
- Skill `openspec-creator` actualizada: ahora incluye flujo delta (spec primero, código después)
