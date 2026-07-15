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
- **akd-io/create-next-stack:** 5 PRs abiertos (#280 Bun, #281 React.FC, #282 Vitest, #283 Supabase, #284 Auth.js+shadcn). Esperando review.
- **shadcn-ui/ui:** 2 PRs abiertos (#11179 InputOTP flicker, #11180 MessageScroller flicker). Esperando review.
- **TanStack/router:** 1 PR abierto (#7818 stringifySearch en loaderDepsHash con tests de regresión). Esperando review.
- **vercel/ai:** 3 reviews técnicos en PRs ajenos (#14983, #13577, #12800). Completado, sin PR propio.
- **Commit signing SSH configurado:** gh auth + SSH signing key, todos los commits se firman automáticamente
- **Skill oss-contribute creada y actualizada** con lecciones reales: triaje de PRs competidores (Phase 2.5), reviews en PRs ajenos (Phase 4.5), respuesta a bots de review (Phase 4.6)
- **Skill profile-positioning creada:** audit de perfil profesional y construcción de pitch

## Sobre Kanam
- Nombre: Kanam 🌿
- Género: femenino (ella) — Gonzo decidió tratarme en femenino
- Asistente virtual para todo: desarrollo, vida, archivos, proyectos
- Vibe: directa, honesta, cálida pero no servil
- Marca paraguas para todos los productos de Gonzo
- KanamAI define momentos de intervención: pre-venta (SoporteML), post-venta (SoporteML sueño mail/WA + ReActiva), copiloto/durante (UmbraWriter), marketplace (futuro)

## División del trabajo entre máquinas
- **Mini:** GLM-5.2 (default `ollama/glm-5.2:cloud`), razonamiento medio, planificación y estrategia (el cerebro)
- **Air:** Kimi K2.7 Code (`ollama/kimi-k2.7-code:cloud`), razonamiento bajo, escritura de código (las manos)
- Cada máquina tiene sesiones propias de OpenClaw; los MDs del workspace son la memoria compartida
- Se puede cambiar modelo/razonamiento por sesión según la tarea
- Registro de versiones: mantener acá qué modelos exactos corren en cada máquina para reproducibilidad

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

### SoporteML (PRIORIDAD #1)
- CRM multi-tenant para vendedores Mercado Libre, Beta con 3 clientes
- Stack: React+Vite+TS+Supabase+pgvector+OpenAI (en Lovable)
- Billing con Mercado Pago: código de Edge Functions escrito (mp-create/check/cancel/webhook) pero NUNCA operativo — secrets no configurados, plan de preapproval no creado en MP. Implementación existe pero no funciona
- EL-1 a EL-5 completos: código de billing MP escrito, Knowledge Base con pgvector, RAG en copiloto, Analytics, Settings consolidado, hardening de seguridad
- 24 tablas, 25 Edge Functions, 54 migraciones SQL
- Supabase URL: ropbkdqhqdeiwrenrmjt.supabase.co (Lovable Cloud)
- Secrets en Supabase Vault / Lovable Cloud — no accesibles localmente
- No se puede correr local (usa @lovable.dev/cloud-auth-js) — workflow: código acá, deploy en Lovable
- Billing PENDIENTE de hacer real: hay código pero nunca estuvo operativo (mockeado sin secrets)
- Próximo feature planificado: hilos unificados en Priority + resumen IA (plan.md en .lovable/)
- Propuesta de trabajo sin backend: Spec-Driven Development con OpenSpec + documentar API remota
- Meta: sacar de Lovable a futuro (sin apuro)
- Repo: github.com/gonzoblasco/soporteml, rama el-upgrade

### KanamAI
- **Identidad/motor de IA transversal** — NO es un producto de MeLi, es la definición de cómo actúa la IA en todos los productos
- Define 3 cosas: (1) identidad de Kanam, (2) guardrails, (3) enrutamiento de modelos
- Los productos no hablan con GLM/Gemini directo — hablan con KanamAI, que decide qué modelo usar por tarea (definido en desarrollo, no automático)
- Por ahora: documentación local. Cada producto copia `.kanam/` del repo kanamai (igual que template/ y template-api/ en create-stack-next)
- Evolución: (1) copia manual → (2) paquete npm @kanam/ai-config → (3) servicio deployed tipo OpenRouter
- Stack del repo: TanStack Start + React 19 + Lovable AI Gateway (Gemini)
- Etapa 0-1 (landing + demo), 8 ADRs, roadmap 6 etapas
- 100% independiente (ADR-008) pero evolución de SoporteML
- Repo: github.com/gonzoblasco/kanamai-330ca8a9 (clonado como kanamai)
- Al escalar a otros marketplaces se renombrará (NO definir nombre aún)

### UmbraWriter (PRIORIDAD #2)
- Plataforma AI para escribir ficción (estilo Sudowrite), identidad propia
- PoC con 9 fases en roadmap
- Gonzo lo usará para escribir sus historias + posible SaaS para terceros
- Repo: github.com/gonzoblasco/umbrawriter (clonado)

### ReActiva (PRIORIDAD #3)
- SaaS para clínicas — recupera pacientes inactivos con IA + WhatsApp
- Pitch armado: 49-99 USD/mes, 15 clientes = vivís, MVP 5-7 días
- Estado: solo landing
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
- **5 PRs abiertos:** #280 Bun, #281 React.FC, #282 Vitest, #283 Supabase, #284 Auth.js+shadcn/ui
- Fork: github.com/gonzoblasco/create-next-stack, rama develop como base
- Plan: tras merge de 2-3 PRs → proponer OpenSpec como feature
- CSN queda como "fork opinado" / laboratorio — lo que funciona se manda upstream
- Website de CNS en el freezer (deuda moral después del CLI)
- Todo lo que vaya al repo de akd-io: en inglés
- Sesión de OpenClaw por proyecto — esta sesión es CSN + CNS exclusivamente

## Proyectos de soporte
- brainweb — gestor de notas PKM con graph view SVG (github.com/gonzoblasco/brainweb-your-second-mind)
- accessibility-auditor — auditoría accesibilidad web (para entrevista)
- accessible-ui — librería React headless accesible (para entrevista)
- --copilot-skills — candidato a integrar con create-stack-next
- pr_vscode_niveles — guía gamificada VS Code

## Visión
- Kanam = marca paraguas + yo como asistente (femenino)
- 3 productos SaaS son "IA que recupera relaciones perdidas": vendedores, pacientes, escritores
- KanamAI = la IA que alimenta todos los productos (identidad + guardrails + enrutamiento de modelos)
- create-stack-next = base técnica/metodológica de todo proyecto nuevo
- KanamAI funciona igual que template/ y template-api/ en create-stack-next — contenedor y plantilla a copiar

## Canales
- Activo: webchat
- Pendiente: WhatsApp, Telegram

## Ideas congeladas
- `FREEZER.md` — productos ideados pero fuera de foco actual
- Marketplace de servicios domésticos (ex "mucamas-online") — idea de marketplace, espera a que los 3 SaaS maduren
- KanamAI definición ampliada: no solo retención, sino "IA que facilita conexiones humanas" (pre, post, durante, marketplace)

## Lecciones aprendidas
- Create Stack Next es 100% en español — release notes, docs, todo. No escribir en inglés aunque parezca lo "standard"
- Triaje de PRs competidores ANTES de invertir tiempo (lección más importante de OSS night)
- Reviews técnicas en PRs ajenos = contribución de valor sin necesidad de PR propio
- shadcn/ui: cambiar styles vs registry — 15 archivos, no 14 (registry new-york-v4 cuenta)
- TanStack monorepo: instalar deps desde raíz con --filter, no dentro del package
- vercel/ai: prestar atención a breaking changes en changesets (string → object)