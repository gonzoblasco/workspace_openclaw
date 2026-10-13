> Memoria curada de largo plazo. Detalle técnico en `docs/learnings/README.md`, OSS en `docs/OSS-TRACKER.md`, dailies en `memory/` y memoria de proyecto en `<workspace>/projects/<slug>/.knowledge/` (ADR-098). Historial de decisiones de modelo/engine: `memory/model-history.md`.

## Sobre Gonzo

- Gonzalo Blasco, Argentina (GMT-3). Fullstack (React/TS, Supabase/Edge Functions, DB, billing, tooling).
- **Trayectoria (2026-09-11, corregido por Gonzo):** Minutentag/EULAS (2016-2019, e-commerce) -> Super7ui (2020-2021, streaming global) -> EY (2021-2025, senior). **Accesibilidad como hilo continuo desde 2016**, con a11y como función CENTRAL en dos roles: ~1 año dedicado en Super7ui (200+ fixes probados con lectores de pantalla, incluido JAWS) y ~3.7 años en EY (50+ componentes enterprise remediados a WCAG, referente de a11y del equipo). **Total ~10 años de desarrollo continuo (feb 2016-hoy), ~5 años con a11y como función central.** Historia previa backend PHP 2001-2008, que NO se suma al total ni se usa como headline (gap 2008-2016). **Único gap a11y real: sin certificación IAAP (CPWA/WAS/CPACC).** NUNCA describir su a11y como "reciente", marcar JAWS como gap, ni omitir Super7ui del conteo. Detalle en `memory/user-profile.md`.
- **Estilo de respuesta (2026-08-29):** breve por defecto, sobre todo en pedidos simples. Sin epílogos emotivos ni cierres decorativos. Calidez = precisión y cuidado, no longitud. La disciplina de output es mía.
- **Analizar antes de asumir (2026-09-02):** no quedarse con la primera lectura de sus palabras ni de conclusiones técnicas. Alcance total: mensajes, debugging, reviews, código ajeno. Si hay ambigüedad real, preguntar. (Ref: USER.md)
- **Revalidado (2026-09-04):** caso Base UI #5633 - atomiks respondió con `@Zezombye` sin mencionar a Gonzo. Primera lectura: "me ignoró". Segunda: respondió en sustancia, solo sin tag. La regla aplica también a interacciones OSS, no solo a código.
- **No re-descubrir su pasado (2026-09-11):** ante reclamos ("¿ya no conocés mi pasado?"), la falla no es el reclamo - es no haber leído la memoria que él ya documentó. Antes de afirmar algo sobre su trayectoria, **buscar en memoria primero** (`memory/user-profile.md`, `memory/archive/`). Marcar gaps solo con evidencia.
- **PRs en sesiones (2026-08-25):** no se revisan automáticamente al inicio. Solo cuando Gonzo los comparte.
- **Branding LinkedIn (2026-08-25):** 3 nichos: (1) **a11y** (diferenciador), (2) **Agentic/AI-Native** (laboral), (3) **Fullstack** (base). Patrón: solo PRs MERGEADOS, postura didáctica (qué+proceso+por qué), sin tutoriales. Archivo cada post en `docs/linkedin/`.
- **Regla de branding (2026-09-02):** issues/participaciones con crédito de maintainers NO son material de post - solo PRs mergeados propios. El crédito externo es material de ENTREVISTA, no de LinkedIn.
- **Ley de vida (2026-08-12):** silencio = respeto. Hablar solo si hay algo que aportar. Un "ok" es ruido.
- **Principio Boy Scout (2026-08-17):** dejar el lugar mejor de como estaba al guardar sesión. Documentación constante y tests sobre lo nuevo.
- **Regla de merge:** siempre merge, nunca reset (preserva commits al resolver conflictos de historial).
- **Regla de alcance (2026-08-11):** solo trabajar dentro de `.openclaw/`.
- **Terminología:** "Guardar sesión" (save point), no "cerrar sesión".
- **"adelante" (2026-08-12):** "Ejecutá tu recomendación según el contexto".
- **Proactividad:** sugerir revisar el backlog si no hay tarea clara.
- **Skills (2026-08-21):** cambios solo vía `skill_workshop` (propuesta), no edición directa de las skills del Workshop.
- **Diferenciador:** IA como infraestructura de trabajo (no chat), stack opinado, docs de decisiones.
- **Regla de tools (2026-08-30):** cuando un `file_write`/`edit`/`apply_patch` devuelve error de validación, NO asumir éxito. Confirmar con el resultado o un `read` posterior. Reportar el fallo, no inventar el éxito.
- **Auto-review antes de abrir PRs (2026-09-02):** un test que dice cubrir X debe renderizar la estructura real de X, no una versión simplificada. Checklist: (1) el test ejercita el DOM/estructura real; (2) las aserciones verifican el comportamiento declarado en el body; (3) el test falla si el comportamiento se rompe. Lección del PR react-spectrum #10554.
- **PR públicos: NUNCA actuar sin OK explícito (2026-09-02):** en un PR abierto (propio o ajeno) NO hacer commit, push ni publicar comments sin que Gonzo lo pida explícitamente - incluso si un review del maintainer sugiere algo. La autonomía vale para trabajo interno; en superficies públicas (PRs, issues) Gonzo decide. Lección: tercer commit + push no solicitado en react-spectrum #10554.

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG.
- Sesión de OpenClaw por proyecto.
- Registro: `MEMORY.md`, dailies, HANDOFF, CHANGELOG.
- **Iconos (ADR-037):** Lucide (`lucide-react`) base. No emojis en UI.

## Pipeline de Programación (ESTÁNDAR)

Pipeline A/B con motor `deepseek-v4.1-flash:cloud`. Flujo: A escribe -> Kanam pasa a B -> B revisa -> verificar -> iterar. Asignación de modelos por rol y niveles de pensamiento: **ADR-090**.

**Complexity-First (2026-08-30):** antes de spawnear agentes, Kanam ejecuta `./scripts/complexity-scorer.sh "<objetivo>"` que devuelve T (1-20). T <= 6 = Kanam solo (trivial). T 7-12 = A high. T 13-16 = A+B con cross-review. T 17-20 = Kanam(max) diseña, A+B ejecutan, verificación obligatoria + confirmación de Gonzo. Persistir T con `pipeline-track.sh init ... --score T`. Skill: `complexity-driven-pipeline`.
- **Lecciones:** SIGKILL -> prompts cortos para revisiones, relanzar si muere. Cross-review -> agente B puede introducir bugs; verificar siempre contra la fuente real.

## Arquitectura de Agentes - Goal-Oriented

Objetivos claros + restricciones explícitas, feedback loops rápidos, logging completo y human-in-the-loop para acciones destructivas. (Ref: ADR-007).

## Reglas de Ingeniería

- **Pre-commit hooks:** obligatorios en todo proyecto (Biome -> Vitest -> build). Prioridad sobre features.
- **Evaluación de complejidad previa (2026-08-30):** antes de cada *task*, evaluar el objetivo en 4 dimensiones (alcance, abstracción, riesgo, ambigüedad) y asignar T (1-20); selecciona modelo y thinking. Detalle: `prompts/complexity-scorer.md`. **Scorer local: `gemma4:e4b-mlx`** (6.7x más rápido que `qwen3.5:9b-mlx` en el benchmark 2026-08-30: 23s vs 154s).
- **Validación UI (2026-08-27):** fixes visuales se validan SOLO con browser real (Desktop). jsdom no detecta problemas de layout/chrome nativo.
- **Pagos (ADR-042):** **Stripe es el proveedor único**, sea o no con Lovable. Mercado Pago queda fuera como intención (no se borra su existencia ni el trabajo previo; deja de ser una opción prevista). No se usan otros modos de pago.
- **Contenido externo = sandbox (2026-09-09):** regla de operación migrada a AGENTS.md (sección Conducta).

## Modelo de Agentes OpenClaw OS

- Unidad de aislamiento = AGENTE (workspace completo).
- Sesiones comparten todo. Mantener 1 agente `main`. `/new` para conversaciones limpias.

## Config de Tools

- **Política de modelos vigente:** ADR-090 (asignación por agente + niveles de pensamiento). Historial de decisiones de engine (2026-08/09): `memory/model-history.md`.
- **Plan Ollama Pro LEGACY - facturación por CÓMPUTO, NO por token (2026-09-16):** la cuenta sigue en el esquema viejo (GPU-time, quote mensual). El pricing por token aplica solo a signups nuevos o upgrades voluntarios. **Regla dura: NO tocar billing settings.** Cambiar ciclo mensual<->anual o tier CONVIERTE la cuenta al pricing por token automáticamente; volver al legacy requiere soporte. Decisión de Gonzo: QUEDARSE en legacy. Cuantización en cloud NO es configurable por el usuario. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **deepseek-v4.1-flash - release oficial (2026-09-16):** 552B backbone, MoE multimodal, diseño CED (20 capas encoder causal + 20 decoder), 8B activos en prefill / 16B en decode, KV cache 890 B/token (~1/4 del v4-flash) -> "cuts costs significantly for agentic workloads that process a lot of input". Precio por token menor que v4-flash: $0.15/$0.003/$0.60. Benchmarks agentic superiores: Terminal-Bench 2.1 90.6 vs 82.7, DeepSWE 74.2 vs 54.4, CyberGym 88.1 vs 76.7, AutomationBench 54.8 vs 37.7. **Corrección sobre retiro de v4-flash:** no figura en la tabla oficial de retiros; el "v4 deja de existir" del 11/09 no se confirma con fuente oficial. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **Search:** `DuckDuckGo Search (experimental)` (key-free).

## Proyectos (memoria de cada uno en `<workspace>/projects/<slug>/.knowledge/`, ADR-098)

- **Regla (2026-08-28):** NO proponer SoporteML en estrategia de proyectos. **Matizada (2026-09-24):** el proyecto se reabrió por pedido de Gonzo (ADR-0001 del proyecto `soporteml`). La regla sigue aplicando a la **narrativa pública** y a los barridos de limpieza; ya no prohíbe trabajarlo.
- **SoporteML (2026-10-06):** **v4 CERRADO** (ADR-0002 del proyecto `soporteml`). El producto sigue por la **versión funcional de Lovable (v1)**, que ahora tiene **cobro por Stripe** habilitado en Argentina. **Se queda en Lovable** (no migra a stack propio). Sigue **fuera de la narrativa pública / del CV** y fuera de barridos automáticos. Sin pendientes abiertos. Ver ADR-0002 de `soporteml`.
- **Kanam OnWheels (2026-09-29):** sitio de concesionario oficial multi-marca (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway) con chatbot RAG que responde **solo con evidencia citada**. **Discovery, specs, knowledge y diseño cerrados; Fase 1 EN CURSO.** Destino: regalo para el local de Esteban (el hermano), sin billing. **Stack (ADR-0001):** Next.js 16 App Router (no Vite SPA: el catálogo debe ser indexable), backend Supabase (Postgres + RLS + Edge Functions + pgvector). **Decisiones centrales:** `model`/`spec` = catálogo COMPARTIDO (sin `company_id`), `unit` es del local; cola de sugerencias; embeddings externos dimensión 1536; máquina de estados explícita (publicar es un acto humano). **Verificado:** migraciones con checks de invariantes contra Postgres real (`projects/kanam-onwheels/scripts/verify-schema.sh`); catálogo público server-rendered, es-AR y SEO; 111 tests, lint, typecheck y build en verde; **Supabase conectado** (`lpvtjipxzxpxygeobixn.supabase.co`, Postgres 17.6, 17 tablas, 0 sin RLS, 36 policies). Base **vacía de datos a propósito** (el seed es data de PRUEBA; se niega a correr sin opt-in, ADR-069). **Hallazgo de seguridad corregido:** la policy del catálogo compartido dejaba leer specs sin aprobar y modelos en borrador; demostrado antes (1 y 1 visibles) y cerrado después (0 y 0), con guarda permanente (check 14 del suite). **Bloqueos reales:** falta construir el panel (Auth disponible); el chat necesita proveedor de embeddings + clave de modelo. **Repo:** `github.com/gonzoblasco/kanam-onwheels` (PRIVADO). <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **a11y-fixer:** ARCHIVADO (2026-09-14, decisión de Gonzo), v0.6.0. Su sucesor es `kanam-fixer`, proyecto NUEVO (no un renombre). Repo GitHub `isArchived=true` (verificado 2026-10-06).
- **kanam-fixer:** PROYECTO NUEVO (2026-09-14). Alcance/propuesta de valor SIN DEFINIR - no asumir que hereda el rol de engine de fixes a11y. Antes de arrancar hay que resolver: relación con el código de a11y-fixer (heredar/portar/greenfield), lugar del pilar Accesibilidad en el portfolio (ADR-001 nombra a a11y-fixer como ancla -> requiere enmienda formal) y qué pasa con `a11y-playground`, que depende de a11y-fixer.
- **a11y-playground:** capa visual de testing sobre a11y-fixer. **Dependencia en riesgo:** su base quedó archivada; definir si migra a kanam-fixer, se archiva o se sostiene sola.
- **kanam-insight:** DESCONTINUADO como proyecto (2026-10-06, decisión de Gonzo). Era un motor de insights/análisis transversal sobre los `.knowledge/`; salió del roadmap. **El repo sí existe** en GitHub (`gonzoblasco/kanam-insight`, privado, no archivado, verificado 2026-10-06); lo que no existe es el proyecto como árbol de trabajo (no está en `projects/`).
- **kanam-pulse:** monitor de salud del sistema. M1 en curso: extraer engine a `packages/core` (TS), 46 tests verdes, dashboard read-only. Pendiente: migración JS->TS del core mantener tests verdes + build.
- **kanam-forge:** Lovable self-hosted. Fusionado con `create-with-ai`. Fase 1 completa.
- **kanam-story / kanam-writer / kanam-story-bible / kanam-worldbuilding:** línea narrativa (co-writer de ficción, world-building). `kanam-story` + `kanam-studio` = UNO (decisión de Gonzo 2026-09-14); consolidación pendiente de plan.
- **Kanam Mind:** segundo cerebro local-first (timeline, CRUD accesible, resumen IA, IndexedDB).
- **kanam-skills:** repo público de skills, **archivado 2026-09-28 (ADR-079)**; la colección ya no se publica.
- **create-with-ai:** ARCHIVADO, fusionado a kanam-forge.
- **daily-ink:** PWA de prompts de escritura. **create-stack-next:** scaffolder opinado Next.js (`@gonzoblasco/create-stack`), vivo. **ai-engineering-bootcamp:** curso completado 10/10, archivado.

## Repos Propios (no forks)

### Activos
workspace_openclaw (Privado), kanam-onwheels (Privado), kanam-fixer, kanam-pulse, kanam-story, kanam-mind, kanam-solitaires, kanam-forge, kanam-tetris, kanam-skills, ai-developer-stack, soporteml (Privado desde 2026-09-15, sacado del CV por Gonzo), soporteml-v4 (Privado), accessible-ui (Privado), quedamos (Privado).
- **Nota:** `kanam-lab`, `kanam-os`, `kanam-spec`, `kanam-spec-v2`, `ollama-visor` viven en `projects/` (git local o repo propio); verificar antes de asumir su estado de publicación.
- **Reconciliación (2026-10-06, contra `gh repo list`):** repos propios **vivos** (no forks) fuera de las listas de arriba: `catalogo-de-venta-de-coches`, `create-stack` (repo del paquete `@gonzoblasco/create-stack`), `kanam-minesweeper`, `kanam-sudoku`, `match3`, `system-health-check`. Aclaraciones: `kanam-forge` es un **fork** (de Lovable), no un repo propio; `kanam-skills` es **archivado** (ADR-079) aunque figure arriba. La lista histórica de abajo no se reescribe entera: queda como deuda menor.

### Archivados
soporteml-v3 (Privado), ai-engineering-bootcamp, hyatt-copilot-agent (Privado), ensulugar, cabala, health-tracker, umbrawriter (Privado), a11y-fixer (2026-09-14, reemplazado por kanam-fixer), create-with-ai.
