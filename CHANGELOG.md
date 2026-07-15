# CHANGELOG.md

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
