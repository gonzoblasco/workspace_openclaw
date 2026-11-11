> Memoria curada de largo plazo. Detalle técnico en `docs/learnings/README.md`, OSS en `docs/OSS-TRACKER.md`, dailies en `memory/` y memoria de proyecto en `<workspace>/projects/<slug>/.knowledge/` (ADR-098). Historial de decisiones de modelo/engine: `memory/model-history.md`.

## Sobre Gonzo

- Gonzalo Blasco, Argentina (GMT-3). Fullstack (React/TS, Supabase/Edge Functions, DB, billing, tooling).
- **Trayectoria (2026-09-11, corregido por Gonzo):** Minutentag/EULAS (2016-2019, e-commerce) -> Super7ui (2020-2021, streaming global) -> EY (2021-2025, senior). **Accesibilidad como hilo continuo desde 2016**, con a11y como funcion CENTRAL en dos roles: ~1 ano dedicado en Super7ui (200+ fixes probados con lectores de pantalla, incluido JAWS) y ~3.7 anos en EY (50+ componentes enterprise remediados a WCAG, referente de a11y del equipo). **Total ~10 anos de desarrollo continuo, ~5 anos con a11y como funcion central.** Historia previa backend PHP 2001-2008, que NO se suma al total ni se usa como headline (gap 2008-2016). **Unico gap a11y real: sin certificacion IAAP.** NUNCA describir su a11y como "reciente", marcar JAWS como gap, ni omitir Super7ui del conteo. Detalle en `memory/user-profile.md`.
- **Inglés: B2 (2026-10-20).** Nivel declarado, dato duro. NUNCA declararlo C1 ni superior en screenings, CVs ni entrevistas. Detalle y contexto en `memory/user-profile.md`.
- **Estilo de respuesta (2026-08-29):** breve por defecto, sobre todo en pedidos simples. Sin epílogos emotivos ni cierres decorativos. Calidez = precisión y cuidado, no longitud. La disciplina de output es mía.
- **Analizar antes de asumir (2026-09-02):** no quedarse con la primera lectura de sus palabras ni de conclusiones técnicas. Alcance total: mensajes, debugging, reviews, código ajeno. Si hay ambigüedad real, preguntar. (Ref: USER.md)
- **Revalidado (2026-09-04):** caso Base UI #5633 - atomiks respondió con `@Zezombye` sin mencionar a Gonzo. Primera lectura: "me ignoró". Segunda: respondió en sustancia, solo sin tag. La regla aplica también a interacciones OSS, no solo a código.
- **No re-descubrir su pasado (2026-09-11):** ante reclamos ("¿ya no conocés mi pasado?"), la falla no es el reclamo - es no haber leído la memoria que él ya documentó. Antes de afirmar algo sobre su trayectoria, **buscar en memoria primero** (`memory/user-profile.md`, `memory/archive/`). Marcar gaps solo con evidencia.
- **PRs en sesiones (2026-08-25):** no se revisan automáticamente al inicio. Solo cuando Gonzo los comparte.
- **Branding LinkedIn y material de post:** dueño `memory/user-profile.md` (sección "Marca personal"). Regla que no se negocia: solo PRs mergeados propios; el crédito de maintainers es material de entrevista, no de post.
- **Ley de vida (2026-08-12):** silencio = respeto. Hablar solo si hay algo que aportar. Un "ok" es ruido.
- **Principio Boy Scout (2026-08-17):** dejar el lugar mejor de como estaba al guardar sesión. Documentación constante y tests sobre lo nuevo.
- **Regla de merge:** siempre merge, nunca reset (preserva commits al resolver conflictos de historial).
- **Regla de alcance (2026-08-11):** solo trabajar dentro de `.openclaw/`.
- **Terminología:** "Guardar sesión" (save point), no "cerrar sesión".
- **"adelante" (2026-08-12):** "Ejecutá tu recomendación según el contexto".
- **Proactividad:** sugerir revisar el backlog si no hay tarea clara.
- **Skills (2026-08-21):** cambios solo vía `skill_workshop` (propuesta), no edición directa de las skills del Workshop.
- **Diferenciador:** IA como infraestructura de trabajo (no chat), herramientas curadas por criterio, docs de decisiones.
- **Regla de tools (2026-08-30):** cuando un `file_write`/`edit`/`apply_patch` devuelve error de validación, NO asumir éxito. Confirmar con el resultado o un `read` posterior. Reportar el fallo, no inventar el éxito.
- **Auto-review antes de abrir PRs (2026-09-02):** un test que dice cubrir X debe renderizar la estructura real de X, no una versión simplificada. Checklist: (1) el test ejercita el DOM/estructura real; (2) las aserciones verifican el comportamiento declarado en el body; (3) el test falla si el comportamiento se rompe. Lección del PR react-spectrum #10554.
- **PR públicos: NUNCA actuar sin OK explícito (2026-09-02):** en un PR abierto (propio o ajeno) NO hacer commit, push ni publicar comments sin que Gonzo lo pida explícitamente - incluso si un review del maintainer sugiere algo. La autonomía vale para trabajo interno; en superficies públicas (PRs, issues) Gonzo decide. Lección: tercer commit + push no solicitado en react-spectrum #10554.

## Metodología

- Herramientas curadas por criterio y reglas de ingeniería: **`AGENTS.md`**. Acá no se repiten.
- Sesión de OpenClaw por proyecto.
- Registro: `MEMORY.md`, dailies, HANDOFF, CHANGELOG.
- Reglas de ingeniería (iconos, UI, pagos, pre-commit): **viven en `AGENTS.md`**; acá no se repiten.

## Pipeline de Programación (ESTÁNDAR)

Pipeline A/B de dos agentes: A escribe, B revisa, el CORE verifica e itera. Los modelos y los niveles de pensamiento **no se escriben acá**: los declara el bloque managed de `AGENTS.md` desde `memory.db`, y el fundamento está en **ADR-090**.

**Complexity-First (2026-08-30):** antes de spawnear agentes, Kanam ejecuta `./scripts/complexity-scorer.sh "<objetivo>"` que devuelve T (1-20). T <= 6 = Kanam solo (trivial). T 7-12 = A high. T 13-16 = A+B con cross-review. T 17-20 = Kanam(max) diseña, A+B ejecutan, verificación obligatoria + confirmación de Gonzo. Persistir T con `pipeline-track.sh init ... --score T`. Skill: `complexity-driven-pipeline`.
- **Lecciones:** SIGKILL -> prompts cortos para revisiones, relanzar si muere. Cross-review -> agente B puede introducir bugs; verificar siempre contra la fuente real.

## Arquitectura de Agentes - Goal-Oriented

Objetivos claros + restricciones explícitas, feedback loops rápidos, logging completo y human-in-the-loop para acciones destructivas. (Ref: ADR-007).

## Reglas de Ingeniería

> Las reglas operativas (pre-commit, iconos, validación UI, pagos, contenido externo) viven en `AGENTS.md`. Acá queda solo lo que es hecho del entorno, no regla de conducta.

- **Evaluación de complejidad previa (2026-08-30):** antes de cada *task*, evaluar el objetivo en 4 dimensiones (alcance, abstracción, riesgo, ambigüedad) y asignar T (1-20); selecciona modelo y thinking. Detalle: `prompts/complexity-scorer.md`. **Scorer local: `gemma4:e4b-mlx`** (6.7x más rápido que el scorer anterior de 9B en el benchmark 2026-08-30: 23s vs 154s).

## Modelo de Agentes OpenClaw OS

- Unidad de aislamiento = AGENTE (workspace completo).
- Sesiones comparten todo. Mantener 1 agente `main`. `/new` para conversaciones limpias.

## Config de Tools

- **Política de modelos vigente:** ADR-090 (asignación por agente + niveles de pensamiento). Historial de decisiones de engine (2026-08/09): `memory/model-history.md`.
- **Plan Ollama Pro LEGACY - facturación por CÓMPUTO, NO por token (2026-09-16):** la cuenta sigue en el esquema viejo (GPU-time, quote mensual). El pricing por token aplica solo a signups nuevos o upgrades voluntarios. **Regla dura: NO tocar billing settings.** Cambiar ciclo mensual<->anual o tier CONVIERTE la cuenta al pricing por token automáticamente; volver al legacy requiere soporte. Decisión de Gonzo: QUEDARSE en legacy. Cuantización en cloud NO es configurable por el usuario. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **deepseek-v4.1-flash - release oficial (2026-09-16):** 552B backbone, MoE multimodal, diseno CED (20 capas encoder causal + 20 decoder), 8B activos en prefill / 16B en decode, KV cache 890 B/token. Precio por token menor que v4-flash: $0.15/$0.003/$0.60. Benchmarks agentic superiores: Terminal-Bench 2.1 90.6 vs 82.7, DeepSWE 74.2 vs 54.4, CyberGym 88.1 vs 76.7, AutomationBench 54.8 vs 37.7. **Correccion sobre retiro de v4-flash:** no figura en la tabla oficial de retiros; el "v4 deja de existir" del 11/09 no se confirma con fuente oficial. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **Junie (JetBrains) DESCARTADO por gate de hardware (2026-10-28):** Junie Local pide Apple Silicon **M5** y **64 GB RAM**; la Mac Mini es **M4 / 24 GB**, así que la edición estrella no aplica. Se evaluó la vía alternativa (perfil JSON `custom:` hacia Ollama, `apiType: OpenAICompletion`, `http://localhost:11434/v1/chat/completions`), que **sí** funciona, pero el parque local tope 12B no sostiene un loop agéntico (la propia doc advierte tool-calls malformadas y loops) y apuntar a los `:cloud` lo reduce a otro frontend de inferencia. **Reapertura:** un chip M5, una máquina con 64 GB, o JetBrains bajando el piso de hardware. El formato del perfil y el endpoint ya están verificados. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **Search:** `DuckDuckGo Search (experimental)` (key-free).
- **Herramientas IA instaladas (2026-10-20):** inventario vivo de las herramientas IA de la Mac. **Dueno del estado: `scripts/ai-toolbox.py`** (list/status/health/up/down) + skill `ai-toolbox`; vista humana y prosa en `docs/tools/REGISTRY.md`. La lista y el conteo exactos NO se repiten aqui a proposito: se leen del registro, que es lo unico que no puede envejecer mal (el estado sale de Docker y de sondas HTTP reales, no de una lista escrita a mano). Cline tiene wrapper propio `scripts/cline-tool.sh` (dashboard :8787, chat en `/chat`). <!-- project: github.com/gonzoblasco/workspace_openclaw -->

## Proyectos (memoria de cada uno en `<workspace>/projects/<slug>/.knowledge/`, ADR-098)

- **caesar3-clone (2026-11-10) — FASE 4:** clon personal de Caesar III en Godot 4.7.2, desde cero y basado en el original. MVP: sandbox con caminos, casas 1×1 niveles 1-5, agua, trigo, trabajo, walkers, templo mínimo, riesgo y dinero; objetivo 1.000 habitantes. Meta final: clon completo. Docs en `projects/caesar3-clone/.knowledge/`; fase 4: walker lab no-destino (Walker/Engine/Pool), spawner tick 31, service resolver, 13 tests + smoke + main input; commit `0b9805f`; B3 PASS 21/25. Repo local sin remoto. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **SoporteML - regla vigente (2026-10-20, decision de Gonzo):** producto propio bajo el rol **Freelancer (05/2025-presente)**, con **Pro Motors como primer cliente** (`pro-motors.com.ar`, integracion MeLi real verificada). **SI va al CV y a las propuestas laborales.** Sigue fuera del portfolio publico de GitHub (repo privado) y no se propone como ancla de la estrategia de proyectos. **Derogadas:** la regla 2026-08-28 ("no proponerlo") y la matizacion 2026-09-24. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **SoporteML (2026-10-06):** **v4 CERRADO** (ADR-0002 del proyecto `soporteml`). El producto sigue por la **versión funcional de Lovable (v1)**, que ahora tiene **cobro por Stripe** habilitado en Argentina. **Se queda en Lovable** (no migra a stack propio). Fuera de barridos automáticos. **Sobre el CV: derogado el 2026-10-20** - ahora SÍ va al CV (ver regla vigente arriba). Sin pendientes abiertos. Ver ADR-0002 de `soporteml`.
- **kanam-query (2026-10-21) - DORMIDO desde 2026-10-21:** producto greenfield para las preguntas de compradores en MeLi. Repo en `projects/kanam-query/`, **sin codigo**. Queda **por fuera del producto nuevo**: no se toca ni se hereda nada (decision de Gonzo). Su valor vivo es la **evidencia verificada de la API de MeLi** en `.knowledge/EVIDENCIA-VERIFICADA.md`, que el producto nuevo **re-verifica** en su Fase 0 en vez de citarla como fundamento heredado. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **Kanam OnWheels (2026-09-29) - DORMIDO desde 2026-10-21:** sitio de concesionario multi-marca (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway) + chatbot RAG con evidencia citada. **Fase 1 quedo interrumpida**: 7.493 LOC, 111 tests en verde, base vacia a proposito (ADR-069). **El destino D4 (regalo a Esteban, sin billing) queda DEROGADO** para el producto nuevo: Esteban pasa a ser **tenant 0** del paquete comercial. El repo queda como **referencia de lectura dormida**, no se hereda codigo. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **OnWheels (2026-10-21) - EN CURSO, PRODUCTO NUEVO unico, sin apuro:** producto vendible que integra catalogo + canal Mercado Libre + desk. Reemplaza a `kanam-onwheels`, `soporteml` y `kanam-query` (dormidos, sin heredar codigo). **Decisiones:** D1 Esteban = tenant 0; D2 base nueva; D5 multi-tenant estilo WordPress.com (accounts = plans, sites = tenants, memberships = acceso); D6 app de MeLi central ahora, uno por dealer despues; D8 **USD 80-200 por plan** (ninguno final); D9 cobro por Mercado Pago (ADR-042); D10 `.com.ar` primero; D12 sin apuro. **ROADMAP F0-F6 en `projects/onwheels/.knowledge/ROADMAP.md`.** La unidad del roadmap es el USO. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **PR-Agent (The-PR-Agent/pr-agent) - DESCARTADO (2026-10-20, decision de Gonzo).** **No se va a usar: no volver a proponerlo ni a instalarlo.** Se evaluo contra verdad de base humana: 0 hallazgos, 5 falsos positivos, jueces de 1/10, 0/10 y 0/10; para redactar PRs quedo muy por debajo de Claude Code con el MISMO modelo. **Lo que queda es la evidencia:** veredicto, mediciones y 8 trampas en `docs/evaluacion/pr-agent-2026-10-20.md`. Para revisar/redactar PRs: Claude Code (instalado, ruteado por Ollama). <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **browser-use: DESCARTADO y BORRADO (2026-11-02, decision de Gonzo).** El MCP salio de `openclaw.json` y despues se borro el resto: `projects/browser-use` y `projects/browser-use-ui` **nunca existieron en disco** al momento de la purga (no habia repo ni imagen que conservar), y con ellos se fueron la skill `browser-tool`, sus dos docs y las entradas del registro. **Motivo:** obligaba a tener Docker Desktop arriba, que reserva ~7,7 GB wired de 24 GB. **Alternativa sin Docker:** plugin `browser` nativo (`@openclaw/browser-plugin`, enabled). Lo unico que sobrevive es la leccion de infraestructura en `learnings` #299 (volumen de Chrome anonimo por contenedor, nunca compartido ni bind-mounteado). <!-- project: github.com/gonzoblasco/workspace_openclaw -->
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
workspace_openclaw (Privado), kanam-onwheels (Privado), kanam-fixer, kanam-pulse, kanam-story, kanam-mind, kanam-solitaires, kanam-forge, kanam-tetris, kanam-skills, ai-developer-stack, soporteml (Privado desde 2026-09-15; SÍ va al CV como Freelance, regla 2026-10-20), soporteml-v4 (Privado), accessible-ui (Privado), quedamos (Privado).
- **Nota:** `kanam-lab`, `kanam-os`, `kanam-spec`, `kanam-spec-v2`, `ollama-visor` viven en `projects/` (git local o repo propio); verificar antes de asumir su estado de publicación.
- **Reconciliación (2026-10-06, contra `gh repo list`):** repos propios **vivos** (no forks) fuera de las listas de arriba: `catalogo-de-venta-de-coches`, `create-stack` (repo del paquete `@gonzoblasco/create-stack`), `kanam-minesweeper`, `kanam-sudoku`, `match3`, `system-health-check`. Aclaraciones: `kanam-forge` es un **fork** (de Lovable), no un repo propio; `kanam-skills` es **archivado** (ADR-079) aunque figure arriba. La lista histórica de abajo no se reescribe entera: queda como deuda menor.
- **kanam-sudoku (2026-10-20) - v1 de ESCRITORIO, vivo, no tocar:** sudoku 9x9 offline-first (PWA), vanilla JS + Vite, motor propio, 3 niveles con dificultad por TECNICA, hints que explican la tecnica. Verificado 2026-10-20: 257 tests, e2e Chromium 18/18, axe-core 0 violaciones. El movil es `kanam-sudoku-iphone` (arriba): este NO se hereda ni se reescribe. <!-- project: github.com/gonzoblasco/kanam-sudoku -->
- **kanam-sudoku-iphone (2026-10-24) - PUBLICADO Y VIVO:** sudoku 9x9 mobile-first para iPhone (PWA instalable, offline, notas por celda). **Repo publico** `gonzoblasco/kanam-sudoku-iphone` -> `gonzoblasco.github.io/kanam-sudoku-iphone/`. Dificultad por TECNICA, stack propio (TypeScript, cero deps de runtime). **Verificado: 91/91 tests, 5 e2e a 390x844, contraste AA, axe-core 0.** La revision B encontro **18 bugs**, el grave: el tablero transpuesto. **Una nota no es una jugada** (ADR-0007). Detalle en `docs/CHANGELOG.md` 2026-10-24. <!-- project: github.com/gonzoblasco/kanam-sudoku-iphone -->

### Archivados
soporteml-v3 (Privado), ai-engineering-bootcamp, hyatt-copilot-agent (Privado), ensulugar, cabala, health-tracker, umbrawriter (Privado), a11y-fixer (2026-09-14, reemplazado por kanam-fixer), create-with-ai, **accessibility-auditor (ARCHIVADO 2026-10-20, decisión explícita de Gonzo: "no quiero volver a oír de él")**.

- **accessibility-auditor - regla dura (2026-10-20):** NO mencionarlo en CVs, portfolios, propuestas ni narrativa publica. Ya no resuelve en GitHub y no existe en `projects/`. **Qedo referenciado en CVs viejos** (material historico, no se corrige retroactivamente), pero **ningun CV nuevo lo incluye**. Para demostrar el mismo eje a11y + tooling, usar los PRs mergeados (Adobe / IBM Carbon / Meta Astryx / MUI) y Super7UI/Warner Bros. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
