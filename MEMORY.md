## ⚙️ DECISIÓN DE MOTOR LLM (2026-08-30)

> **Nota 2026-09-29:** `deepseek-v4-flash:cloud` fue **retirado por Ollama el 2026-09-25** (`ollama show` responde `was retired`). Todo lo que sigue es **registro de las decisiones de agosto**; el motor vigente del pipeline A/B es `deepseek-v4.1-flash:cloud`. Las entradas de abajo se conservan como historia, no como instruccion.

**Tema:** Consolidación de motor de trabajo para el pipeline A/B.
**Decisión:** Se establece `deepseek-v4-flash:cloud` como el modelo preferido para los agentes de código y orquestación de pipeline, reemplazando temporalmente a `glm-5.3-flash:cloud` en la configuración operativa (detallado en `tools.md`).
**Motivación:** Preferencia explícita de Gonzo tras la auditoría de coherencia. El modelo fue seleccionado por su *estructura* en el contexto de las tareas complejas, priorizando la consistencia operativa sobre la preferencia inicial del proveedor.
**Impacto:** Los futuros *tasks* deben referenciar este cambio y cualquier uso de `glm-5.3-flash:cloud` deberá pasar por un flag de excepción y ser justificado.
**Referencia:** [#AGENTS-DETALLE]

## ⚙️ REVERT A DEEPSEEK V4 FLASH COMO DEFAULT (2026-08-30)

**Tema:** Default de todo el sistema.
**Decisión:** `deepseek-v4-flash:cloud` vuelve a ser el default de TODO el sistema (OpenClaw + pipeline A/B), revirtiendo el cambio a `glm-5.3-flash:cloud`. La diferencia de calidad entre ambos es muchísima a favor de DeepSeek (decisión explícita de Gonzo).
**Acción:** `agents.defaults.model.primary = ollama/deepseek-v4-flash:cloud`. Backup previo: `~/.openclaw/openclaw.json.bak-20260830-revert-deepseek`. Gateway reiniciado y verificado.
**Impacto:** `glm-5.3-flash:cloud` queda como opción disponible (multimodal) pero NO es default. Cualquier uso como default requiere flag de excepción justificado.

> Memoria curada de largo plazo. Detalle técnico en `docs/learnings/README.md`, OSS en `docs/OSS-TRACKER.md`, dailies en `memory/` y proyectos en `projects/<slug>/.knowledge/`.

## Sobre Gonzo

- Gonzalo Blasco, Argentina (GMT-3). Fullstack (React/TS, Supabase/Edge Functions, DB, billing, tooling).
- **Trayectoria (2026-09-11, corregido por Gonzo, 2 correcciones):** Minutentag/EULAS (2016-2019, e-commerce) -> Super7ui (2020-2021, streaming global) -> EY (2021-2025, senior). **Accesibilidad como hilo continuo desde 2016**, con a11y como funcion CENTRAL en dos roles: ~1 ano dedicado en Super7ui (200+ fixes probados con lectores de pantalla, incluido JAWS) y ~3.7 anos en EY (50+ componentes enterprise remediados a WCAG, referente de a11y del equipo). **Total ~10 anos de desarrollo continuo (feb 2016 - hoy), ~5 anos con a11y como funcion central.** Historia previa: backend PHP 2001-2008, que NO se suma al total ni se usa como headline (decisión de Gonzo 2026-09-14; hay un gap 2008-2016). **Unico gap a11y real: sin certificacion IAAP (CPWA/WAS/CPACC).** NUNCA describir su a11y como "reciente", marcar JAWS como gap, ni omitir Super7ui del conteo. Detalle en `memory/user-profile.md`.
- Búsqueda laboral: perfil AI-Native / a11y. Entrevista con OpenSistemas (25/08) - cerrada 11/09 (avanzaron con otro candidato; pidio reconsideracion).
- Perfil: fotógrafo, comunicación social, escritor de novelas.
- Preferencias: honestidad absoluta, autonomía total, registro escrito crítico.
- **Estilo de respuesta (2026-08-29):** breve por defecto, sobre todo en pedidos simples. Sin epílogos emotivos ni cierres decorativos ("serenatas"). Calidez = precisión y cuidado, no longitud. El registro efusivo de GLM no es excusa: la disciplina de output es mía.
- **Analizar antes de asumir (2026-09-02):** regla de interacción en USER.md - no quedarse con la primera lectura de sus palabras ni de conclusiones técnicas. Alcance total: mensajes, debugging, reviews, código ajeno. Si hay ambigüedad real, preguntar. (Ref: USER.md)
- **Revalidado (2026-09-04):** caso Base UI #5633 - atomiks respondió con `@Zezombye` sin mencionar a Gonzo. Primera lectura: "me ignoró / quedé mal parado". Segunda lectura: respondió en sustancia (cubrió el typeahead y la dirección del fix), solo sin tag. No fue desaire. La regla aplica también a interacciones OSS, no solo a código. (Ref: memory/2026-09-04.md)
- Setup: workspace en una sola maquina, la Mac Mini (ADR-073).
- **PRs en sesiones (2026-08-25):** No se revisan automáticamente al inicio. Solo cuando Gonzo los comparte.
- **Branding LinkedIn (2026-08-25):** 3 nichos: (1) **a11y** (diferenciador), (2) **Agentic/AI-Native** (laboral), (3) **Fullstack** (base). Patrón: Solo PRs MERGEADOS, postura didáctica/pedagógica (el qué+proceso+por qué), sin tutoriales secuenciales. Archivo cada post en `docs/linkedin/`.
- **Regla de branding (2026-09-02):** Issues/participaciones con crédito de maintainers NO son material de post - solo PRs mergeados propios. El crédito externo (ej. cixzhang en #4777) es material de ENTREVISTA (evidencia de proceso), no de LinkedIn. Registro interno (OSS-TRACKER/daily) captura todo; branding público solo merges propios.
- **Ley de vida (2026-08-12):** Silencio = respeto. Hablar solo si hay algo que aportar. Un "ok" es ruido.
- **Principio Boy Scout (2026-08-17):** Dejar el lugar mejor de como estaba al guardar sesión. Documentación constante y tests sobre lo nuevo.
- **Regla de merge:** Siempre merge, nunca reset (preserva commits al resolver conflictos de historial).
- **No re-descubrir su pasado (2026-09-11):** Ante reclamos de Gonzo ("¿ya no conocés mi pasado? para qué me gasto documentando?"), la falla no es el reclamo - es no haber leído la memoria que él ya documentó. Antes de afirmar algo sobre su trayectoria/experiencia, **buscar en memoria primero** (`memory/user-profile.md` trayectoria, `memory/archive/` CV 2026-08-19). Marcar gaps solo con evidencia; su CV histórico está registrado.
- **Docs por categoría (2026-08-27):** Carpetas en `docs/` para `linkedin/`, `feedback/`, `prs/`, `pipeline/`, `entrevistas/`. Raíz solo para generales.
- **Idioma GitHub (2026-08-12):** TODO en inglés (README, docs, ADRs, commits, PRs). Strings de UI en español.
- **Regla de alcance (2026-08-11):** Solo trabajar dentro de `.openclaw/`.
- **Terminología:** "Guardar sesión" (save point), no "cerrar sesión".
- **"adelante" (2026-08-12):** "Ejecutá tu recomendación según el contexto".
- **Proactividad:** Sugerir revisar el backlog si no hay tarea clara.
- **Skills (2026-08-21):** Cambios solo vía `skill_workshop` (propuesta), no edición directa.
- **Colaboración OSS (2026-08-24):** El valor suele estar en comentar/revisar, no en abrir PRs. No pisar el trabajo ajeno.
- **Interacción Maintainers (2026-08-24):** Si la dirección ya fue validada, ir directo a la acción (hacer el PR), no ofrecer "estoy feliz de iterar".
- **Bots de review (2026-08-24):** No agradecer a bots. Responder directo a la sustancia con evidencia.
- **Referencia ≠ proyecto (2026-08-24):** "Quitar referencia" = quitar puntero git, NUNCA borrar carpeta con datos locales (`.env`, `*.db`). Respaldar SIEMPRE antes de limpiar.
- **Diferenciador:** IA como infraestructura de trabajo (no chat), stack opinado, docs de decisiones.
- **Regla de tools (2026-08-30):** Cuando un `file_write`/`edit`/`apply_patch` devuelve error de validación (ej. falta de `node`), NO asumir que la operacion tuvo exito. Confirmar con el resultado del tool o con un `read` posterior. Reportar el fallo al usuario, no inventar el exito.
- **Auto-review antes de abrir PRs (2026-09-02):** Un test que dice cubrir X debe renderizar la estructura real de X, no una version simplificada. Checklist antes de abrir: (1) el test ejercita el DOM/estructura real, no un mock flatten; (2) las aserciones verifican el comportamiento declarado en el body del PR; (3) el test falla si el comportamiento se rompe (probar mutandolo mentalmente). Un maintainer detecta atajos en segundos - mejor iterar localmente que en review. Leccion del PR react-spectrum #10554 (test de secciones que flatteneaba y no renderizaba la estructura).
- **PR públicos: NUNCA actuar sin OK explícito (2026-09-02):** en un PR abierto (propio o ajeno) NO hacer commit, push, ni publicar comments sin que Gonzo lo pida explicitamente. Incluyendo cuando un review del maintainer sugiere algo - leer, entender, proponer a Gonzo, esperar OK, ejecutar. La autonomia vale para trabajo interno (workspace, codigo local); en superficies públicas (PRs, issues) Gonzo decide. Leccion: tercer commit + push no solicitado en react-spectrum #10554 cuando Gonzo esperaba solo proponerle el plan.

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG.
- Sesión de OpenClaw por proyecto.
- Registro: MEMORY.md, dailies, HANDOFF, CHANGELOG.
- **Iconos (ADR-037):** Lucide (`lucide-react`) base. No emojis en UI.

## Pipeline de Programación (ESTÁNDAR)

Pipeline A/B con **Qwen Code vía Ollama** (motor: `deepseek-v4.1-flash:cloud`). Flujo: A escribe $\rightarrow$ Kanam pasa a B $\rightarrow$ B revisa $\rightarrow$ Verificar $\rightarrow$ Iterar.

**Complexity-First (2026-08-30):** Antes de spawnear agentes, Kanam ejecuta `./scripts/complexity-scorer.sh "<objetivo>"` que devuelve T (1-20). T <= 6 = Kanam solo (trivial). T 7-12 = A high. T 13-16 = A+B con cross-review. T 17-20 = Kanam(max) diseña, A+B ejecutan high, verificacion obligatoria + confirmacion de Gonzo. Persistir T con `pipeline-track.sh init ... --score T`. Skill: `complexity-driven-pipeline`.
- **Claude Code (Alternativa):** Para SIGKILL o tareas largas.
- **Lecciones:**
    - **SIGKILL:** Prompts cortos para revisiones; relanzar si muere.
    - **Cross-review:** Agente B puede introducir bugs. Verificar siempre contra la fuente real (API/Docs).
    - **Terminal Harnesses (2026-08-23):** Los CLIs TUI (como ForgeCode) no son orquestables sin TTY real. Usar solo herramientas que corran headless.

## Arquitectura de Agentes - Goal-Oriented

Objetivos claros + restricciones explícitas, feedback loops rápidos, logging completo y human-in-the-loop para acciones destructivas. (Ref: ADR-007).

## Reglas de Ingeniería

- **Pre-commit hooks:** Obligatorios en todo proyecto (Biome $\rightarrow$ Vitest $\rightarrow$ Build). Prioridad sobre features.
- **Evaluación de Complejidad Previa (2026-08-30):** Antes de cada *task*, el orquestador (Kanam) DEBE evaluar el objetivo en 4 dimensiones (Alcance, Abstracción, Riesgo, Ambigüedad) y asignar un score T (1-20). Este score selecciona el modelo y el nivel de *thinking* de forma automática. Detalle: `prompts/complexity-scorer.md`. **Scorer local: gemma4:e4b-mlx primero** (6.7x mas rapido que qwen3.5:9b-mlx en benchmark 2026-08-30: 23s vs 154s).
- **Validación UI (2026-08-27):** Fixes visuales se validan SOLO con browser real (Desktop). jsdom/headless no detectan problemas de layout/chrome nativo.
- **Pagos (2026-08-29):** Mercado Pago SIEMPRE, NUNCA Stripe (ADR-042). Excepción solo si Gonzo la marca explícitamente y queda documentada en el proyecto. Razón: en Argentina y LATAM Stripe no opera como opción real; Mercado Pago cubre moneda local y medios de pago.
- **Contenido externo = sandbox (2026-09-09):** regla de operación migrada a AGENTS.md (sección Conducta). Cubre redes de agentes, código de terceros y web.

## Modelo de Agentes OpenClaw OS

- Unidad de aislamiento = AGENTE (workspace completo).
- Sesiones comparten todo. Mantener 1 agente `main`. `/new` para conversaciones limpias.

## Config de Tools

- **Modelos (2026-09-11, 19:30):** Primary de OpenClaw: `deepseek-v4-flash:0731`. **Motor del pipeline A/B: `deepseek-v4-flash:cloud`** (ADR-046, revierte ADR-045 por costo: v4.1 consumia mas por request que v4 y glm con menos requests). Kanam en **thinking max**; agentes A/B en **high** (`deepseek-v4-flash`). Fallback + vision: `glm-5.3-flash`. **deepseek-v4.1-flash** = fase de escalada para analisis complejo cuando ni v4 ni glm resuelven; potencial paso previo/reemplazo de Kimi K2.7 Code (quedo entre glm y Kimi en costo). Nota: v4 anunciado para dejar de existir en unas semanas (reemplazo por 4.1) - a reevaluar entonces.
- **Cambio de motor (2026-08-29):** DeepSeek V4 Flash → GLM 5.3 Flash, tras comparativa de 5 modelos con un mismo prompt pesado de arquitectura de agentes (DeepSeek V4 Flash xhigh, GLM 5.3 Flash, GLM 5.3, Kimi K2.7 Code xhigh, Kimi K3 xhigh). DeepSeek fue el más estructurado pero el menos agudo; GLM 5.3 Flash ganó en insights operativos y es multimodal nativo (imagen/video/PDF, 1M de contexto). Kimi K2.7 Code (xhigh) fue el mejor pensador (validado en high el 29/08: solido, sin win claro sobre GLM Flash); retirado del ecosistema el mismo dia.
- **Niveles de razonamiento (2026-08-29):** el max NO es driver de calidad (DeepSeek en max filosofa, ADR-040; Kimi K3 en xhigh inventó números). Los mejores outputs vinieron sin razonamiento visible. Agentes de código siempre en high; max solo para diseño difícil puntual. Para GLM: CERO parámetros, default del servidor (ADR-041).
- **Regla de costo (2026-08-29):** 1 request de Kimi K3 = 41 requests de GLM 5.3 Flash en consumo real (medición Ollama). K3 = cirujano, nunca default. Precios verificados: GLM Flash $0.075/$0.25 - K3 $3.00/$15.00 por 1M.
- **Purga de modelos (2026-08-30):** fuera del ecosistema `kimi-k3`, `deepseek-v4-pro`, `qwen3.5:cloud`, `nemotron-3-nano`, `gemma4:31b-cloud`. Quedan 8 en config: `deepseek-v4-flash` (default + motor pipeline), `glm-5.3-flash` (multimodal + escalada iter 3), `glm-5.3` (escalada familia), `gemma4:e4b-mlx` (local vision), `gemma4:cloud` (vision + tono/voz), `kimi-k2.7-code` (nivel superior, iter 4), `minimax-m3` (variante costo similar a GLM, opcional), `qwen3.5:9b-mlx` (local scorer) + fallback `openrouter/free`. Kimi K2.7 Code y minimax-m3 VUELVEN al ecosistema (2026-08-30, decision de Gonzo: "siempre hay un nivel superior"). Backup: `~/.openclaw/openclaw.json.bak-20260830-pipeline-glm`.
- **Nombres de modelo no intercambiables (2026-09-11):** el motor del pipeline corre con `--model deepseek-v4-flash:cloud`, que resuelve en Ollama. La entrada de OpenClaw `deepseek-v4-flash:0731` es solo para el runtime de OpenClaw y **NO resuelve** en Ollama (`ollama show deepseek-v4-flash:0731` falla).
- **Plan Ollama Pro LEGACY - facturacion por COMPUTO, NO por token (2026-09-16):** la cuenta de Gonzo sigue en el esquema viejo (GPU-time, quote mensual por uso de procesador, barra % que monitorea semanalmente). El pricing por token de ollama.com/pricing (ej. deepseek-v4-flash $0.22/$0.66 por 1M) aplica solo a signups nuevos o upgrades voluntarios (blog oficial "Transparent pricing", 2026-08-31). **Regla dura: NO tocar billing settings.** Cambiar ciclo mensual<->anual o tier CONVIERTE la cuenta al pricing por token automaticamente (FAQ oficial); volver al legacy requiere soporte y solo si habia suscripcion activa al lanzamiento. Decision de Gonzo: QUEDARSE en legacy - su patron (volumen alto de requests con modelos flash, poca necesidad de exceder quote) encaja con compute billing. Cuantizacion en cloud NO es configurable por el usuario: corre con pesos nativos del proveedor (FAQ oficial, posiblemente NVFP4 en hardware NVIDIA nuevo). <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **deepseek-v4.1-flash RELEASE OFICIAL - candidato a primary futuro (2026-09-16):** verificado en la pagina oficial del modelo: 552B backbone, MoE multimodal, diseno CED (20 capas encoder causal + 20 decoder), 8B activos en prefill / 16B en decode, KV cache 890 B/token (~1/4 del v4-flash) -> "cuts costs significantly for agentic workloads that process a lot of input" (patron exacto del pipeline de Gonzo). Precio por token menor que v4-flash: $0.15/$0.003/$0.60 vs $0.22/$0.007/$0.66 non-peak (-32% input, -57% cached, -9% output). Benchmarks agentic largamente superiores: Terminal-Bench 2.1 90.6 vs 82.7, DeepSWE 74.2 vs 54.4, CyberGym 88.1 vs 76.7, AutomationBench 54.8 vs 37.7; razonamiento parejo (GPQA 90.9 vs 89.9, HLE 36.8 vs 37.8). **Correccion sobre retiro de v4-flash:** verifique la tabla de retiros oficial (docs cloud.mdx + pagina del modelo): deepseek-v4-flash NO figura en retiros upcoming ni pasados; sigue vigente y es la alternativa recomendada para v3.1/v3.2/cogito. El "v4 deja de existir" de la nota del 11/09 no se confirma con fuente oficial - no tratarlo como hecho. La medicion del 11/09 (v4.1 consumia mas por request) fue con v4.1-preview; la arquitectura CED del release oficial cambia la ecuacion de costo en input pesado - requiere re-medicion controlada antes de decidir. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **Search:** `DuckDuckGo Search (experimental)` (key-free).

## Proyectos (Detalle en `.knowledge/` de cada uno)

- **Regla (2026-08-28):** NO proponer SoporteML en estrategia de proyectos. Gonzo lo pidió explícitamente. **Matizada (2026-09-24):** el proyecto se reabrió por pedido explícito de Gonzo (ADR-068). La regla sigue aplicando a la **narrativa pública** y a los barridos de limpieza; ya no prohibe trabajarlo.
- **soporteml v1 (2026-08-30):** ciclo activo sobre `gonzoblasco/soporteml` (el original) con Kanam + pipeline A/B escribiendo código directo. Lovable MCP = solo consultas read-only (arquitectura, DB); créditos Lovable para Lovable Cloud/AI/serverless. v2/v3/v4 = referencia. Handoff: `memory/handoffs/HANDOFF-2026-08-30-soporteml-v1-lovable-mcp.md`.

- **Kanam Story:** Co-writer de ficción. PWA, roles especializados. Local-first $\rightarrow$ Nube (en plan).
- **Kanam Mind:** Segundo cerebro local-first. Timeline, CRUD accesible, resumen IA. Local-first puro (IndexedDB).
- **SoporteML:** CRM MeLi. **REABIERTO (2026-09-24):** nueva generación greenfield - SaaS CRM + contable para pymes, con las mismas features que **v1** (la de Lovable, la más completa de las cuatro) y alcance ampliado al contable. Encuadre: **producto privado**, NO ancla de portfolio. Ver ADR-068 (encuadre, 6 puntos pendientes) y ADR-067. **Sigue vigente:** fuera de la narrativa PÚBLICA / del CV (privacidad/estrategia) y fuera de barridos automáticos de limpieza. **Pendientes de Gonzo:** encuadre (facturar vs uso propio), cuánto contable entra, nombre (es el ADR #1 del proyecto), app OAuth de MeLi, y el destino de los ADRs técnicos de v3/v4. La pregunta sin responder en 4 generaciones: ¿por qué esta vez tendrá usuarios? v1 nunca cobró (billing escrito, jamás operativo).
- **kanam-skills:** Repo público de skills. Sanitización obligatoria (Gonzo $\rightarrow$ usuario).
- **Kanam OnWheels (2026-09-29):** proyecto nuevo. **Discovery, specs, knowledge y diseno cerrados; desarrollo de Fase 1 EN CURSO.** Sitio de un concesionario oficial multi-marca (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway) con autos y motos de alta gama, nuevos y usados. Chatbot IA con RAG que responde **solo con evidencia citada**. **Enriquecimiento:** el vendedor pega la URL de la ficha oficial, el sistema extrae y normaliza, y el vendedor aprueba antes de publicar. **Multi-concesionaria desde el diseno** (RLS por `company_id`). **Fase 1:** motos completas (nuevas y usadas). **Destino:** regalo para el local de Esteban (el hermano), sin billing. **Stack (ADR-0001):** Next.js 16 App Router, NO Vite SPA (el catalogo tiene que ser indexable; el precedente de `soporteml` no aplica porque ese es panel privado). Backend Supabase (Postgres + RLS + Edge Functions + pgvector). **Decisiones centrales:** `model`/`spec` son catalogo **COMPARTIDO** (sin `company_id`), `unit` es del local; cola de sugerencias para corregirlo; embeddings externos dimension 1536 fija; maquina de estados explicita (publicar es un acto humano). **Hecho y verificado:** 6 migraciones con **13/13 checks de invariantes contra Postgres real** (`~/projects/kanam-onwheels/scripts/verify-schema.sh`); nucleo de enriquecimiento (normalizacion de unidades + extractores por dominio, con errores tipados); catalogo publico server-rendered con filtros por URL, es-AR y SEO. **111 tests, lint, typecheck y build en verde.** Base de dev persistente en Docker: `bash ~/projects/kanam-onwheels/scripts/dev-db.sh up`. **Supabase CONECTADO (2026-09-29):** proyecto `lpvtjipxzxpxygeobixn.supabase.co` (Postgres 17.6), **7 migraciones aplicadas y verificadas**: 17 tablas, 0 sin RLS, 36 policies, extension vector, las 3 funciones publicas. Conexion directa OK (el host directo es solo-IPv6, funciona desde esta maquina; el Session Pooler es la alternativa). La base esta **vacia de datos a proposito**: el seed es data de PRUEBA y no comparte base con un proyecto real (ADR-069); ahora se niega a correr sin opt-in explicito. **HALLAZGO DE SEGURIDAD corregido:** la policy del catalogo compartido (`state <> 'discarded'` en `spec`, `using (true)` en `model`) dejaba leer a cualquier usuario autenticado las specs SIN aprobar y los modelos en borrador. Demostrado antes de arreglar (1 y 1 visibles), cerrado despues (0 y 0, con las 23 aprobadas legibles). Guarda permanente: check 14 del suite (14/14). **Bloqueos reales:** el panel ya tiene Auth disponible (falta construirlo); el chat necesita proveedor de embeddings + clave de modelo. **Artefactos:** `~/projects/kanam-onwheels/` - `.knowledge/` + `docs/` (architecture, data-model, CONTEXT, 9 ADRs). Pieza genuinamente nueva: el scraping multi-marca. Prior art borrado: `sportcars` y `pro-motors-docs` (2026-08-17). Nombre temporal: el sitio publico toma el nombre del cliente (ADR-0009). **Repo:** `github.com/gonzoblasco/kanam-onwheels` (PRIVADO, creado 2026-09-29). `.knowledge/` queda fuera del repo por `.git/info/exclude` (es del proyecto y viaja con el, ADR-075); `.env.local` ignorado. <!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **a11y-fixer:** ARCHIVADO (2026-09-14, decision de Gonzo). Engine de fixes de accesibilidad, v0.6.0. **Su sucesor es `kanam-fixer`, proyecto NUEVO** (no un renombre): alcance a definir - todo id=54. Repo GitHub `gonzoblasco/a11y-fixer` sigue `isArchived=false` (archivado pendiente de OK).
- **kanam-fixer:** PROYECTO NUEVO (2026-09-14). Nombre elegido por Gonzo. Alcance/propuesta de valor SIN DEFINIR - no asumir que hereda el rol de engine de fixes a11y. Antes de arrancar hay que resolver: relacion con el codigo de a11y-fixer (heredar/portar/greenfield), lugar del pilar Accesibilidad en el portfolio (ADR-001 nombra a a11y-fixer como ancla -> requiere enmienda formal) y que pasa con `a11y-playground`, que depende de a11y-fixer.
- **a11y-playground:** Capa visual de testing sobre a11y-fixer. Depende de a11y-fixer (base). **Dependencia en riesgo (2026-09-14):** su base quedo archivada; definir si migra a kanam-fixer, se archiva o se sostiene sola.
- **kanam-insight:** Motor de insights/analisis. Activo (dependencias TBD).
- **kanam-pulse:** Monitor de salud del sistema. M1 Kickoff en curso (2026-08-30): extraer engine a packages/core (TS), 46 tests verdes, dashboard read-only. Codigo ya en el repo. Pendiente: refactor + dashboard.
- **kanam-forge:** Lovable self-hosted. Fusionado con `create-with-ai`. Fase 1 completa.
- **create-with-ai:** ARCHIVADO. Fusionado a kanam-forge. Deprecar en npm (requiere npm login).
- **daily-ink:** PWA prompts de escritura.
- **create-stack-next:** Scaffolder opinado Next.js (`@gonzoblasco/create-stack`). Vivo.
- **ai-engineering-bootcamp:** Curso completado 10/10. Archivados.

## Repos Propios (No forks)

### Activos
- workspace_openclaw (Privado)
- kanam-skills, kanam-story, kanam-mind, kanam-solitaires, soporteml (Privado desde 2026-09-15, sacado del CV por Gonzo), soporteml-v4 (Privado), ai-developer-stack, accessible-ui (Privado), quedamos (Privado), kanam-forge, kanam-tetris, kanam-insight (Privado).
- **Nota:** `kanam-lab` NO tiene repo en GitHub (git local, sin remoto - verificado 2026-09-14). No agregarlo a este listado.

### Archivados
- soporteml-v3 (Privado), ai-engineering-bootcamp, hyatt-copilot-agent (Privado), ensulugar, cabala, health-tracker, umbrawriter (Privado), a11y-fixer (2026-09-14, reemplazado por kanam-fixer).
