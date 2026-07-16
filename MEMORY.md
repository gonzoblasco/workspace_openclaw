# MEMORY.md - Long-Term Memory

## Sobre Gonzo
- Gonzalo, Argentina (GMT-3)
- 9 años como Frontend React, ahora Fullstack (aprendiendo backend, ya lo hace en práctica)
- Desempleado, usando IA para todo ("me reemplazaron por IA, ahora uso IA para todo")
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora — no comentar ni sugerir parar por horario, trabaja cuando puede
- Quiere honestidad absoluta — sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia — el registro escrito es crítico
- Tiene entrevista para trabajo fullstack especializado en accesibilidad
- Trabaja entre dos máquinas (Mac Mini y MacBook Air), workspace sincronizado por git
- Cada máquina tiene sesiones propias de OpenClaw; los MDs del workspace son la memoria compartida

## Perfil profesional / Metodología (lo que lo diferencia)
- **Stack opinado, no por default** — no usa herramientas al azar, las cura. CSN es la prueba: scaffold opinado con OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención heredada.
- **IA-asistida como skill real, no como prompt** — construyó un sistema completo de trabajo con IA: sesiones por proyecto, memoria persistente (MDs + git), handoffs, cron jobs, subagentes, skill workshop. La mayoría de los devs no tienen esto. Es una metodología, no un atajo.
- **Opinionated en el buen sentido** — AGENTS.md, ROADMAP, ADRs, CONTRIBUTING. Documenta decisiones, no solo código. Eso es senior aunque no tenga el título formal.
- **Fullstack real con IA** — frontend React/TS, backend Supabase/Edge Functions, DB, billing, tooling, scaffolding, accesibilidad. Todo orquestado con IA como copiloto metodológico, no copia-pega.
- **Accesibilidad como especialización activa** — la usa como ventaja competitiva, no como checkbox. Tiene accessibility-auditor, accessible-ui, y busca trabajos donde la accesibilidad sea central.
- **Diferenciador en el mercado:** un dev que sabe usar IA como infraestructura de trabajo (no como chat), con stack opinado y docs de decisiones. Eso es escaso. La mayoría de los devs no saben orquestar sesiones, memoria, handoffs, subagentes. Gonzo sí.

## Open Source — pipeline activo
- **Estrategia:** PRs a repos externos como evidencia pública de capacidad → portfolio vivo → menos entrevistas laborales
- **akd-io/create-next-stack:** 10 PRs abiertos (#280 Bun, #281 React.FC, #282 Vitest, #283 Supabase, #284 Auth.js+shadcn, #285 fix git crash #231, #286 prettier-plugin-organize-imports #266, #287 eslint-strict #263, #288 Zustand #259, #289 Playwright #223). Esperando review.
- **shadcn-ui/ui:** 2 PRs abiertos (#11179 InputOTP flicker, #11180 MessageScroller flicker). Esperando review.
- **t3-oss/create-t3-app:** 2 PRs abiertos (#2239 fix Biome + bump versión ^2.5.3, #2240 fix Prettier .prettierignore). Ambos fixean la misma clase de bug: generated artifacts de Prisma no excluidos de las tools de formato/lint. 0 competidores en #2240, FrancoKaddour tenía branch competidor en #2239.
- **TanStack/router:** 1 PR cerrado (#7818 stringifySearch en loaderDepsHash). A pesar de que el fix era correcto y tenía tests, fue rechazado por el maintainer debido al uso de automatización en el proceso de contribución. Lección: en repos Tier 0, la "estética" del proceso y el toque humano son críticos; evitar trazas de bots en commits y descripciones.
- **vercel/ai:** 3 reviews técnicos en PRs ajenos (#14983, #13577, #12800) + 1 PR propio (#17274 fix warnings dropeadas en finish-step). Review de Vercel addressada, esperando merge.
- **payloadcms/payload:** 1 PR abierto (#17342 fix blocks con 2+ uploads — data loss bug en richtext-lexical). Tier 1 completado: todos los repos del tier 1 tienen al menos un PR o review.
- **Total: 20 PRs abiertos** en 8 repos externos. Esperando review de maintainers en el resto.
- **PR registry completo** en `CONTRIBUTING.md` — cualquier sesión puede hacer batch check sin que el usuario pastee URLs
- **Commit signing SSH configurado:** gh auth + SSH signing key, todos los commits se firman automáticamente
- **Skill oss-contribute:** 6 fases (pipeline → triaje → implementación → PR → community participation → batch triage) + lecciones de 3 sesiones reales. Phase 4.8 (comunidad), Phase 6 (batch PR status check con buckets 🟢⚠️🔴)
- **Fork de payloadcms/payload creado:** github.com/gonzoblasco/payload (último Tier 1)
- **Próxima acción OSS:** seguir buscando issues sin PRs competidores en repos estratégicos. Bottleneck sigue siendo maintainer review time. Nuevos targets identificados: Biome #10922 (useSortedAttributes XML, Rust), shadcn #11125 (MessageScroller tail spacer, 0 competidores).
- **Skill profile-positioning creada:** audit de perfil profesional y construcción de pitch
- **Skill sdd-brownfield creada:** Spec-Driven Development en proyectos existentes con backend remoto — init OpenSpec, specs as-built, delta specs, archivar, branch por feature. Probada en SoporteML.
- **Skill product-orchestrator creada:** Product Owner/Manager end-to-end — evalúa ideas (mercado, viabilidad, fit estratégico), define MVP (scope, personas, flows, métricas), planifica roadmap, y orquesta las demás skills (web-app-builder, sdd-brownfield, agent-dispatcher, agent-review) para llevar productos de idea a deployado. 5 fases con go/no-go gates. Product files en `products/<slug>/`.
- **Skill ux-a11y-studio creada:** Equipo de UX/UI + Accesibilidad — discovery de usuarios y requisitos WCAG 2.2, audit (automated axe-core + manual keyboard/screen reader/cognitive/visual), design system con contraste verificado, implementación de componentes accesibles (WAI-APG, 3 capas de tests), validación final antes de launch. Integrado con product-orchestrator y web-app-builder. Design files en `design/`.
- **Skill ux-a11y-studio creada:** Equipo de UX/UI + Accesibilidad — discovery de usuarios y requisitos WCAG 2.2, audit (automated axe-core + manual keyboard/screen reader/cognitive/visual), design system con contraste verificado, implementación de componentes accesibles (WAI-APG, 3 capas de tests), validación final antes de launch. Integrado con product-orchestrator y web-app-builder. Design files en `design/`.

## Kanam Workflow Kit
- Producto nuevo: `products/copilot-workflow-kit/`
- Kit de 11 skills reutilizables para AI-assisted development (commit, PR, review, security audit, epic closure, etc.)
- Traducido al inglés, frontmatter YAML estándar
- CLI: `npx @kanam/workflow-kit` (pendiente de publicar en npm)
- Repo: github.com/gonzoblasco/workflow-kit
- Skills integrados a OpenClaw workspace: `security-audit` y `pr-review`

## AI Engineering Bootcamp
- Producto nuevo: `products/ai-engineering-bootcamp/`
- Bootcamp gratuito de 10 niveles para AI-assisted development con VS Code + Copilot
- 23 proyectos prácticos, de principiante a producción
- Traducido al inglés, README con progresión visual
- Repo: github.com/gonzoblasco/ai-engineering-bootcamp

## Skills de OpenClaw workspace
- **security-audit:** Auditoría de seguridad multi-tenant, auth guards, secrets, data leaks. Bloquea cierre de epics si hay hallazgos críticos.
- **pr-review:** Linter cognitivo pre-merge. Analiza diff contra convenciones, seguridad, tests, performance.

## BrainWeb MVP completo
- Producto: `products/brainweb/` — BRIEF, EVALUATION, DEFINITION, ROADMAP, STATUS
- MVP: web app de notas con auth (Supabase), editor markdown, tags, graph view, search
- Stack: React 19 + TanStack Start + Supabase + Tailwind v4 + shadcn/ui
- Build verde. README + LICENSE (MIT) listos.
- Pendiente: deploy a producción (Vercel + Supabase)

## Sobre Kanam
- Nombre: Kanam 🌿
- Género: femenino (ella) — Gonzo decidió tratarme en femenino
- Asistente virtual para todo: desarrollo, vida, archivos, proyectos
- Vibe: directa, honesta, cálida pero no servil
- Marca paraguas para todos los productos de Gonzo
- KanamAI define momentos de intervención: pre-venta (SoporteML), post-venta (SoporteML sueño mail/WA + ReActiva), copiloto/durante (UmbraWriter), marketplace (futuro)

## Forma de trabajo
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, projects/PROYECTOS.md, HANDOFF.md por proyecto, CHANGELOG.md
- Al arrancar conversación limpia → leer MEMORY.md + PROYECTOS.md + HANDOFF.md del proyecto que toque
- Antes de cerrar o cuando algo cambie → actualizar HANDOFF, CHANGELOG, memoria del día
- Heartbeat cada 1 hora → mantenimiento general
- Cron job cada 3 días → consolidar diarios a MEMORY.md (job ID: a6b2adb8-4b77-436a-b73c-2c866ac512f3)
- No escribir placeholders vacíos — solo escribí si hay algo real
- Canales: por ahora webchat, después WhatsApp y Telegram
- Sesión de OpenClaw por proyecto — cada sesión es específica, no mezclar proyectos
- Open source contributions: ver `CONTRIBUTING.md` — playbook completo de cómo contribuir a repos externos
- Plan de visibilidad: PRs a repos externos como evidencia pública de capacidad → portfolio vivo → menos entrevistas laborales → el perfil que vende es "dev que trabaja con metodología IA-asistida own + stack opinado + accesibilidad"
- El pitch para recruiters: no "sé React" sino "construí un sistema de trabajo con IA que me hace más eficiente que un dev tradicional, y tengo PRs mergeados que lo demuestran"

## Ecosistema Kanam — Productos principales

### SoporteML v1 (en Lovable)
- CRM multi-tenant para vendedores Mercado Libre, Beta con 3 clientes
- Stack: React+Vite+TS+Supabase+pgvector+OpenAI (en Lovable)
- Billing con Mercado Pago: código de Edge Functions escrito (mp-create/check/cancel/webhook) pero NUNCA operativo — secrets no configurados, plan de preapproval no creado en MP. Implementación existe pero no funciona
- EL-1 a EL-5 completos: código de billing MP escrito, Knowledge Base con pgvector, RAG en copiloto, Analytics, Settings consolidado, hardening de seguridad
- 24 tablas, 25 Edge Functions, 54 migraciones SQL
- Supabase URL: ropbkdqhqdeiwrenrmjt.supabase.co (Lovable Cloud)
- Secrets en Supabase Vault / Lovable Cloud — no accesibles localmente
- No se puede correr local (usa @lovable.dev/cloud-auth-js) — workflow: código acá, deploy en Lovable
- Billing PENDIENTE de hacer real: hay código pero nunca estuvo operativo (mockeado sin secrets)
- OpenSpec specs as-built escritos: inbox, ai-copilot, billing-mp, thread-summary (4 specs, 0 changes activos)
- Meta: sacar de Lovable a futuro (sin apuro) — v2 es el primer paso
- Repo: github.com/gonzoblasco/soporteml, rama el-upgrade

### SoporteML v2 (reconstrucción desde cero) — PRIORIDAD #1
- Reconstrucción de v1 sin Lovable, stack propio, independencia total
- Product files en `products/soporteml-v2/`: BRIEF.md, EVALUATION.md, DEFINITION.md, ROADMAP.md, STATUS.md
- **Ciclo de Product Owner completo:** Phase 0 (Intake) → Phase 1 (Evaluation: 8 competidores, GO) → Phase 2 (Definition: MVP con 10 features) → Phase 3 (Roadmap: 11 fases, ~30 días)
- **Features clave agregadas por Gonzo:** auto-respuesta inteligente (IA clasifica rutinaria vs compleja, opt-in, badge "Auto IA", auditable) + auto-learn de MeLi (al conectar, fetch histórico + generar KB + fichas automáticamente)
- **Phase 1 Foundation ejecutado:** scaffold React 19 + Vite + TS + Tailwind v4 + shadcn/ui. Deps: Biome 2.5, Vitest 4, Zod 4, React Router 7, TanStack Query 5, Supabase JS, RHF, lucide, recharts. 9 entity types, migración SQL multi-tenant + RLS + pgvector + match_kb_chunks RPC. ADR-001: React+Vite. Verification gate: lint ✅ typecheck ✅ test ✅ build ✅ (509KB / 148KB gzip). Git init: `83963a8`
- Proyecto en `projects/soporteml-v2/`
- Supabase local corriendo (`supabase start`), .env.local con keys reales
- shadcn/ui components: button, input, card, label, dialog, dropdown-menu, avatar
- Auth UI: LoginPage.tsx, RegisterPage.tsx
- **MVP COMPLETO (11 fases):** MeLi Integration + Auto-learn (6 EFs), Inbox UI (teclado + realtime), KB UI + RAG, AI Copilot (DeepSeek), Auto-respuesta inteligente, Resumen IA de hilos, Billing MP (REAL), Settings consolidado (8 secciones), Analytics (charts), Hardening (ErrorBoundary + AppLayout). 7 Edge Functions, 8 OpenSpec specs.
- **PENDIENTE #1:** Configurar DEEPSEEK_API_KEY, MELI_APP_ID/CLIENT_SECRET/REDIRECT_URI, MP_ACCESS_TOKEN/PREAPPROVAL_PLAN_ID/WEBHOOK_SECRET para flujo E2E real
- **PENDIENTE #2:** Fix errores en create-stack-next (Biome 2.5, TS 6, Tailwind v4)
- **🔄 Cambio de modelo 2026-07-15 16:09:** qwen3.5:cloud → deepseek-v4-flash. Contexto guardado en memory/2026-07-15.md

### KanamAI — 🧊 FREEZER
- Identidad/motor de IA transversal. Etapa 0-1 (landing + demo IA real), 8 ADRs, roadmap 6 etapas.
- Congelado hasta que SoporteML esté en producción real.
- Repo: github.com/gonzoblasco/kanamai-330ca8a9 (clonado como kanamai)

### UmbraWriter — 🧊 FREEZER
- Plataforma AI para escribir ficción. PoC con features reales (editor, co-writing, export DOCX, AI assistant).
- Congelado hasta que SoporteML esté estable.
- Repo: github.com/gonzoblasco/umbrawriter (clonado)

### ReActiva — 🧊 FREEZER
- SaaS para clínicas — recupera pacientes inactivos con IA + WhatsApp.
- Solo landing. Congelado hasta que SoporteML y UmbraWriter estén maduros.
- Repo: github.com/gonzoblasco/reactiva (clonado)

### create-stack-next (base transversal)
- CLI scaffolder opinado para Next.js 15, ~1000 descargas npm
- v0.7.1, 64 tests, CI verde en 4 package managers
- **OpenSpec integrado (v0.7.0):** Spec-Driven Development embebido en el scaffold base. Select interactivo de herramientas IA (6 principales + opción "Todas"), `openspec init` post-scaffold con fallback, `@fission-ai/openspec` como devDep
- **v0.7.1:** opción "Todas las herramientas (30+)", ROADMAP reescrito sin fases rígidas, README limpiado
- Trick del `gitignore` (sin punto) para que npm lo incluya — rename a `.gitignore` en copy-template.ts
- Base metodológica de todo proyecto nuevo
- Sueño: proyectos existentes adoptan su estructura (AGENTS.md, ROADMAP, HANDOFF, CHANGELOG, ADRs)
- Repo: github.com/gonzoblasco/create-stack-next

### create-next-stack (akd-io) — colaboración
- Repo externo: github.com/akd-io/create-next-stack (570 stars, 4 contributors)
- Filosofía: "buffet" de opciones vs nuestro CSN opinado. Complementario, no competidor
- **10 PRs abiertos:** #280 Bun, #281 React.FC, #282 Vitest, #283 Supabase, #284 Auth.js+shadcn/ui, #285 fix git crash, #286 organize-imports, #287 eslint-strict, #288 Zustand, #289 Playwright
- Fork: github.com/gonzoblasco/create-next-stack, rama develop como base
- Plan: tras merge de 2-3 PRs → abrir issue proponiendo OpenSpec como feature nueva
- Features propuestas listas para presentar: (1) OpenSpec integration, (2) opinionated presets, (3) ADR scaffolding, (4) AGENTS.md generation (AI-ready projects)
- CSN queda como "fork opinado" / laboratorio — lo que funciona se manda upstream
- Website de CNS en el freezer (deuda moral después del CLI)
- Todo lo que vaya al repo de akd-io: en inglés

## Proyectos de soporte
- brainweb — 🧊 FREEZER. Gestor de notas PKM con graph view SVG. MVP completo, build verde. Congelado.
- accessibility-auditor — auditoría accesibilidad web. Portfolio vivo, muestra capacidad.
- accessible-ui — librería React headless accesible. Portfolio vivo, muestra capacidad.
- --copilot-skills — 🧊 FREEZER. Candidato a integrar con create-stack-next.
- pr_vscode_niveles — 🧊 FREEZER. Guía gamificada VS Code.

## Visión
- Kanam = marca paraguas + yo como asistente (femenino)
- 3 productos SaaS son "IA que recupera relaciones perdidas": vendedores, pacientes, escritores
- KanamAI = la IA que alimenta todos los productos (identidad + guardrails + enrutamiento de modelos) — 🧊 FREEZER
- create-stack-next = base técnica/metodológica de todo proyecto nuevo
- KanamAI funciona igual que template/ y template-api/ en create-stack-next — contenedor y plantilla a copiar

## Canales
- Activo: webchat
- Pendiente: WhatsApp, Telegram

## Ideas congeladas
- `FREEZER.md` — productos ideados pero fuera de foco actual
- Marketplace de servicios domésticos (ex "mucamas-online") — 🧊 FREEZER. Esperar a que los 3 SaaS maduren.
- KanamAI definición ampliada: no solo retención, sino "IA que facilita conexiones humanas" (pre, post, durante, marketplace)

## Lecciones aprendidas
- Create Stack Next es 100% en español — release notes, docs, todo. No escribir en inglés aunque parezca lo "standard"
- Triaje de PRs competidores ANTES de invertir tiempo (lección más importante de OSS night)
- Reviews técnicas en PRs ajenos = contribución de valor sin necesidad de PR propio
- Community participation = reputación: comentar, compartir descubrimientos, acknowledge tooling (CodSpeed, Vercel bots), cross-referencing issues. No es solo abrir PRs.
- shadcn/ui: cambiar styles vs registry — 15 archivos, no 14 (registry new-york-v4 cuenta)
- TanStack monorepo: instalar deps desde raíz con --filter, no dentro del package
- vercel/ai: prestar atención a breaking changes en changesets (string → object)
- **Scaffold pitfalls (Biome 2.5+, TS 6+, Tailwind v4, Vitest 4):**
  - TypeScript 6+ depreca `baseUrl` → agregar `"ignoreDeprecations": "6.0"` en tsconfig
  - Biome 2.5 cambió el schema: `organizeImports` → `assist.actions.source.organizeImports`, `recommended` → `preset`, schema URL debe matchear versión exacta
  - Tailwind v4 `@theme` no parseado por Biome → necesita `css.parser.tailwindDirectives: true`
  - `import.meta.env` sin `vite-env.d.ts` → agregar referencia
  - Vite scaffold genera `oxlint` no `biome` → swap manual
  - `vitest run` sin tests falla con code 1 → agregar al menos un test placeholder
  - Path alias `@/*` necesita `resolve.alias` en vite.config Y vitest.config
  - **Biome ignores:** `!**/template/` no funciona sin `root: true` en el biome.json raíz. Biome sube a buscar root config y los patrones `!**/dir/` no excluyen correctamente. Solución: `root: true` + `!template/` + `!template/**` (o simplemente `!template` en Biome 2.2+).
- **OpenSpec lecciones:** "SHALL"/"MUST" requerido ("debe" no pasa), sección `## Purpose` obligatoria, formato WHEN/THEN estricto. En brownfield, verificar si el feature ya está implementado antes de escribir un delta spec.
- **Memory search con Ollama:** configurar `memorySearch.provider: "ollama"` + `model: "nomic-embed-text"` en openclaw.json. Requiere `ollama pull nomic-embed-text`. Default del sistema es OpenAI (falla si no hay API key). CLI local requiere Node 24 (path usa Node 22).