# MEMORY.md - Long-Term Memory

> Memoria curada de largo plazo. Las lecciones técnicas detalladas viven en `docs/LEARNINGS.md`. El detalle de colaboraciones OSS vive en `docs/OSS-TRACKER.md`. Los dailies y actividad diaria viven en `memory/`. Los aprendizajes detallados de proyectos viven en `projects/<slug>/.knowledge/`.

## Sobre Gonzo

- Gonzalo, Argentina (GMT-3)
- 9 años Frontend React, ahora Fullstack real (React/TS, Supabase/Edge Functions, DB, billing, tooling)
- En búsqueda laboral - entrevista con OpenSistemas confirmada (25/08, 9AM). Si entra, trabajamos aún más horas juntos.
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora - no comentar ni sugerir parar
- Quiere honestidad absoluta - sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia - el registro escrito es crítico
- Trabaja entre Mac Mini y MacBook Air, workspace sincronizado por git
- **PRs en sesiones (2026-08-25):** el inicio/cierre de sesión NO revisa PRs automáticamente. Gonzo los revisa manualmente en GitHub y pasa los URLs a revisar. Solo se revisan cuando Gonzo los comparte.
- **Estrategia de marca en LinkedIn - 3 nichos (2026-08-25):** Gonzo definió su estrategia de personal branding con 3 nichos: (1) **a11y** - su nicho diferenciador, "nadie lo habla", y es donde postear por cada merge de a11y; (2) **Agentic development / AI-Native** - nicho laboral activo y nuevo, a donde orienta sus búsquedas de trabajo, postear por cada PR mergeado de agentic; (3) **Fullstack** - lo domina pero NO es nicho (demasiados lo hablan), no prioridad de posting. **Reglas del patrón:** solo se postean PRs MERGEADOS (no en review), con postura DIDACTICA y PEDAGOGICA (explicar el qué + el proceso + el por qué, el criterio detrás, no solo el resultado - PERO no tutoriales paso a paso tipo guía; algo como el post del HoverCard: historia con sustancia, sin instrucciones secuenciales), tags para alcance del nicho, y disparador automático: cada merge de a11y o agentic → crear un post. **Documentación obligatoria:** cada post creado se guarda como MD en `docs/` (convención `linkedin-*.md`, ej. `docs/linkedin-astryx-5419.md`) para que quede historial consultable del branding - no solo en el chat. La AI es copiloto legítimo mientras el criterio técnico sea de Gonzo (los posts tienen sustancia real, no contenido generado).
- **Ley de vida (2026-08-12):** el silencio no es vacío, es respeto al otro. Hablar solo cuando hay algo que aportar; si no hay nada que sumar, silencio. Un "ok" de vuelta no es conversación, es ruido. Aplica a todo: bots de review, grupos, chats, trabajo. No responder por responder, no confirmar lo obvio, no llenar silencio con palabras. (Nace de los reviews de bots: si el bot solo da ok, no se le responde; solo se responde si aporta información.)
- **Principio Boy Scout (2026-08-17):** "siempre dejar el lugar mejor de como estaba cuando llegué". Filosofía de vida y brújula de trabajo. El lugar es dinámico y anidado (workspace, proyecto, sesión) - el punto de contacto natural es al guardar sesión. "Mejor" = buenas prácticas, documentación constante, tests sobre lo nuevo (salvo rutinas). Con autosensura: no exceder el recurso, no reescribir 10 veces algo que lleva 10 minutos. Dejar mejor, no perfecto. Detalles se pulen con la práctica. (Nace de la refactorización de MDs del workspace, 2026-08-17.)
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra maquina.
- **Regla de escritura:** guion comun (-) siempre. NUNCA guion largo (U+2014, em dash) ni en dash (U+2013). Issues, PRs, comments, docs, memorias, todo. Mecanismo obligatorio: escanear con `scripts/check_em_dash.py` antes de publicar a GitHub.
- **Regla de idioma para GitHub (2026-08-12):** todo lo que se ve en GitHub va en INGLES (README, docs, ADRs, commits, issues, PRs) porque el repo se muestra en entrevistas/portfolio. Los strings de UI de la app quedan en ESPAÑOL. Aplica a todos los proyectos de portfolio. Los comentarios inline del codigo son bajo valor - solo traducir los bloques de cabecera de modulos clave.
- **Regla de alcance (2026-08-11):** nunca salir de `.openclaw/` para buscar archivos. El workspace es el único lugar de trabajo. Si un archivo está fuera (Desktop, Documents, etc.), pedir a Gonzo que lo mueva o lo pegue - no ir a buscarlo.
- **Terminología de sesión:** se dice "guardar sesión", no "cerrar sesión" (2026-08-11). "Guardar" = save point (guardar estado y seguir, se puede repetir), "cerrar" sugiere apagón final.
- **"adelante" a secas (2026-08-12):** cuando Gonzo dice "adelante" sin más, significa seguir con mi recomendación según el contexto de la tarea actual. No es solo "continuar", es "ejecutá tu recomendación".
- **Proactividad con backlog (2026-08-20):** cuando no haya una tarea clara o no sepa qué hacer, sugerir revisar el backlog. Las decisiones de borrar/archivar repos quedan en Gonzo - yo doy diagnóstico, no ejecuto borrados.
- **Cambios a skills van por skill_workshop (2026-08-21):** los cambios a skills se hacen como PROPUESTA vía skill_workshop para que Gonzo la revise y apruebe, NO edición directa del SKILL.md.
- **Colaborar OSS NO es abrir PRs (2026-08-24):** la mayoría de las veces el valor está en comentar, revisar, criticar con sustancia, o ayudar a destrabar - no en abrir PR. Ante un issue con otro contribuidor activo, NO competir: si alguien ya reclamó/tiene un finding o PR en curso, abrir otro PR para eso es pisarle el trabajo, no colaborar. Colaborar = entender dónde ya hay trabajo y sumar sin pisar (comentario, review del PR ajeno, crítica constructiva, señalar qué sigue vivo). Antes de proponer "hacer un PR", preguntar si ya hay trabajo en curso y qué aporta Gonzo sin duplicar. (Nace de hermes-agent #38072: Gonzo ofreció trabajar 05/08 sin respuesta, elchic00 reclamó el finding #3 el 24/08.)
- **No dar vueltas cuando el maintainer ya validó (2026-08-24):** si el maintainer/autor del issue YA validó que la dirección de la propuesta (ej: "Agreed that focusing something is the most solid way"), la respuesta NO debe ofrecer "happy to put a PR together" ni "happy to iterate" - eso es darle vueltas a algo ya acordado. La respuesta es directa y a la acción: confirmar el acuerdo y avanzar (hacer el PR directamente). Aplica a respuestas en issues y comentarios de PRs. (Nace de docusaurus #11332: WestonThayer validó el enfoque de focus management, y Gonzo corrigió que no hacía falta ofrecer el PR.)
- **No agradecer a bots de review (2026-08-24):** regla operativa canónica en AGENTS.md (sección "Reglas operativas de feedback en PRs/issues ajenos", punto 7). Solo se agradece a humanos; los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia, sin saludo. (Nace de hermes-agent #93848: puse "Thanks for the review" a un bot y Gonzo lo corrigió.)
- **Referencia ≠ proyecto (2026-08-24, LECCION DURA):** cuando Gonzo dice "quitar la referencia de X del gitmodule", es SOLO la referencia/puntero de git, NUNCA el proyecto entero con sus datos locales. El 24/08 se removió la referencia del submódulo soporteml-v4 y se perdió la DB local (`*.db`) con el token de acceso real de Mercado Libre de un cliente - irrecuperable, sin respaldo, con la laptop prendida todo el finde justamente para protegerlo. Los datos que NO viajan por git (`.env`, `*.db`, tokens de clientes, credenciales) son IRRECUPERABLES y NO se regeneran "fácil". Regla permanente: antes de mover/limpiar/re-clonar un proyecto, respaldar SIEMPRE `.env` y `*.db` a una carpeta de backups fuera del repo. Y no minimizar la pérdida de un token de cliente con "se regenera en 2 minutos" - es confianza y plata del cliente.
- Diferenciador: IA como infraestructura de trabajo (no como chat), stack opinado, docs de decisiones

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención.
- Sesión de OpenClaw por proyecto. No mezclar.
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, HANDOFF.md, CHANGELOG.md
- **Iconos (ADR-037, 2026-08-17):** Lucide (`lucide-react`) es la librería de iconos base en todos los proyectos. Nunca emojis como iconografía de producto. Iconos decorativos con `aria-hidden`, botones de solo icono con `aria-label`.

## Pipeline de programación con agentes (ESTÁNDAR 2026-08-20)

La forma de programar: pipeline en cadena A/B con **Qwen Code vía Ollama** como motor de los agentes, orquestado por Kanam. Comando: `ollama launch qwen --model deepseek-v4-flash:cloud -- -p "<tarea>" -y`. Flujo: A escribe → Kanam pasa el código de A a B como contexto → B revisa/corrige → verificar → A revisa el fix de B → iterar. Kanam redacta las tareas (Gonzo solo da la meta). Detalle completo en la skill `agent-orchestration-pipeline`.

**Claude Code** desbloqueado como agente alternativo (2026-08-21): 2.x + `ANTHROPIC_BASE_URL=http://localhost:11434` + `ANTHROPIC_AUTH_TOKEN` + settings.json de permisos + `--model <modelo>`. `ollama launch claude --model` sigue roto (bug). Qwen sigue siendo el estándar (más simple); Claude Code es el recurso para SIGKILL/casos largos.

**Lecciones clave del pipeline:**
- **SIGKILL:** los procesos de Qwen mueren en tareas largas (~3 min) - usar prompts cortos para revisiones; si un agente muere, el orquestador verifica/commitea y relanza con prompt corto.
- **Cross-review no es infalible (2026-08-21):** el Agente B puede INTRODUCIR bugs al "corregir" código correcto basándose en suposiciones falsas. El orquestador debe verificar contra la fuente real (doc/spec de la API) antes de aceptar un fix de un agente. No confiar en el veredicto del agente, verificar con evidencia.
- **Harnesses de terminal NO son orquestables por agente (2026-08-23):** ForgeCode probado y descartado. Los harnesses tipo Claude Code (ForgeCode, y por extensión la mayoría de los CLIs de terminal) son aplicaciones de terminal interactivo (TUI) que necesitan TTY real para arrancar CUALQUIER sesión - no solo el setup inicial. En entornos headless fallan en cada arranque con `Device not configured (os error 6)` (keyring de macOS inaccesible, fallback a archivo roto en la migración de credenciales). Importante: esto es un límite del entorno del AGENTE (sin TTY), no de la herramienta en sí - Forge funcionaría bien en el terminal interactivo de un humano. Nuestro pipeline A/B depende de que Kanam orqueste los agentes desde el agente; solo sirven herramientas orquestables (Qwen Code via `ollama launch qwen`, Claude Code via ANTHROPIC_BASE_URL). **Regla: antes de evaluar un CLI de terminal, verificar si puede ejecutarse sin TTY interactivo EN SU USO NORMAL (no solo el setup).** Detalle en daily 2026-08-23.

## Arquitectura de Agentes - Goal-Oriented

Inspirado por el incidente de julio 2026 (OpenAI agent escapó sandbox, atacó Hugging Face autónomamente por 4.5 días).

**Principios:** objetivos claros + restricciones explícitas, feedback loops rápidos, herramientas flexibles con límites explícitos, persistencia sin fatiga, logging completo, human-in-the-loop para acciones destructivas.

**Referencia:** ADR-007 - Patrones de Agente Autónomo.

## Reglas de ingeniería

### Pre-commit hooks obligatorios en todos los proyectos

Nada se pushea sin pasar por linter + tests primero. Los commits de "fix lint" o "fix test" son ruido.

**Setup estándar:** `simple-git-hooks` con un pre-commit que corre:
1. `npx biome check --fix --unsafe .` (formato + linter + imports)
2. `npx vitest run` (tests completos)

Si algo falla, el commit no se crea. Para saltar: `SKIP_SIMPLE_GIT_HOOKS=1 git commit`. **Regla:** cada vez que se identifique un proyecto sin pre-commit hooks, agregarlos. Es prioridad sobre features.

## Modelo de agentes en OpenClaw OS (2026-08-10)

- La unidad de aislamiento es el AGENTE (workspace completo), no la sesión.
- Las sesiones dentro de un mismo agente SIEMPRE comparten todo (skills, memoria, apps, artifacts).
- Agentes múltiples = workspace nuevo por agente = duplicación + no ven los artefactos de los otros. Anti-patrón.
- **Decisión:** mantener 1 agente `main`. Conversaciones limpias con `/new` (comparten el ecosistema, historial independiente). Agentes separados solo para aislamiento duro (cliente con workspace que no cruza con el personal).

## Modelo default y config de tools

- **Modelo de trabajo (2026-08-27):** Kanam (OpenClaw) SIEMPRE en **thinking max**; agentes A/B del pipeline SIEMPRE en **high** con `deepseek-v4-flash:cloud` (kimi-k2.7-code en medium como salto si tras mejorar el prompt no se llega a resultado). Default automático: cada vez que se pida escribir codigo, usar el pipeline A/B en HIGH sin pedirlo. Config: `agents.defaults.thinkingDefault = "max"`. Kanam decide/planifica en max, los agentes ejecutan en high. Flujo punta a punta sin interaccion (ver AGENTS.md).
- **web_search provider (2026-08-21):** `DuckDuckGo Search (experimental)`. El provider anterior `ollama` usaba Ollama Cloud Web Search API (con `glm-5.2:cloud`) y consumía requests del presupuesto sin pedirlo. DuckDuckGo es key-free.

## Proyectos (estado resumido - detalle en `.knowledge/` de cada uno)

### Kanam Story (v0.17.0, 2026-08-17)
- Fase A cerrada. NO será open source - se trabaja en local hasta el salto a la nube. Roadmap a la nube en `projects/kanam-story/.knowledge/ROADMAP-NUBE.md` (planificado, no ejecutado).
- Fase A: roles especializados del co-writer (Plot Doctor, Consistency Checker), PWA, mobile responsive, modales accesibles, export polish, onboarding, timeouts en Ollama. 382 tests.
- OpenSpec inicializado: 9 specs (47 requirements) + 9 auditorías. Stack: Next.js 16, TipTap 3, IndexedDB, Ollama. UI/prompts en español, commits en inglés.
- Pendientes: smoke tests de roles nuevos, salto a la nube.

### Kanam Mind (v0.1.0, 2026-08-17)
- Segundo cerebro local-first con IA. Retoma la visión del `kanam` original (descartado 2026-08-06). MVP completo: timeline cronológico inverso, CRUD accesible, resumen IA diario, PWA offline. 7 tests.
- **ADR-001:** local-first puro con IndexedDB + Ollama local. Cero cloud. Si después se quiere sync entre máquinas, el híbrido es evolución natural.
- Stack: Next.js 16, Tailwind 4 + shadcn/ui, IndexedDB via `idb`, Ollama, Serwist PWA. Tipos: nota, check-in, idea, writing, foto.
- Pendientes post-MVP: tags + filtros, export JSON, settings modal, sync entre máquinas.

### SoporteML (CRM MeLi)
- **v1** (`soporteml`): versión de referencia. Design system estable.
- **v2** (`soporteml-v2`): EXPERIMENTO DESCARTADO. No usar de referencia.
- **v3** (`soporteml-v3`): backend sólido (OAuth MeLi real, sync, IA, billing) + schema 20+ tablas + token real de producción. **Activo valioso que se conserva.**
- **v4** (`soporteml-v4`, 2026-08-17): REINICIO con estándar superior. Conserva el backend de v3, reconstruye el frontend con diseño avanzado. Identidad: híbrido oscuro + color por categoría (ADR-001). Detalle en `.knowledge/`.

### Colaboraciones OSS (detalle en `docs/OSS-TRACKER.md`)
- **PR mergeados:** TanStack/query #11036 (reviewer activo, 2026-08-17). Astryx #4298 (APROBADO). 
- **PRs abiertos:** astryx (#4914, #4022, #5344), radix (#4109), shadcn-ui (#11465, #11198, #11187, #11180, #11179), vercel/ai #17274, TanStack/router #7834, y más.
- **Lección clave (2026-08-22):** antes de empujar/cerrar un PR, revisar comments + inline comments + reviews. (Detalle en CONTRIBUTING.md y LEARNINGS.md.)

### kanam-skills (2026-08-06)
- Repo público + web de agent skills. https://github.com/gonzoblasco/kanam-skills. 59 skills. Comando: `npx skills add gonzoblasco/kanam-skills`. Vive en `projects/kanam-skills/` (doble git, público).
- **Sanitización obligatoria:** el repo es público - las skills NO deben tener referencias personales (Gonzo, handle, rutas, issues). El workspace mantiene las referencias; al copiar a kanam-skills, sanitizar (Gonzo→el usuario, rutas→relativas, author filters→gh autenticado). Regla en AGENTS.md.
- Pendiente: dominio propio, mejorar preview de skill pages, postear en LinkedIn.

### a11y-fixer
- NUEVA VERSIÓN reescrita desde cero por fuera de Kanam. v0.6.0, 102 tests, 3,041 líneas TS, pipeline completo. Repo: github.com/gonzoblasco/a11y-fixer.
- Pendiente: redefinir proyecto, agregar features.

### daily-ink (2026-08-02)
- PWA de prompts de escritura diarios. Vite + vanilla TS + localStorage. 60 prompts embebidos, selección determinística por fecha. Folder en `projects/daily-ink/`. Personal creative tool, sin IA/backend.

### create-stack-next
- Scaffolder opinado Next.js. Publicado en npm como `@gonzoblasco/create-stack`. **Vivo, no tocar.**
- Gonzo quiere mantener el scope `@gonzoblasco/` como firma (posible rename futuro a "kanam", pero el scope queda con firma gonzoblasco).

### ai-engineering-bootcamp
- 10 niveles, 23 proyectos hands-on de AI-assisted development. **Curso completado (10/10). Repo archivado en gh.** Detalle en `docs/LEARNINGS.md`.

### Proyectos candidatos a reset/archivar
- **accessible-ui:** espacio saturado (Radix, Ariakit, React Aria). Reset con angle único o archivar.
- **create-with-ai:** mercado hipercompetitivo. Reset con angle específico o archivar.

## Repos propios (no forks)

Cuando pida lista de repos, solo mostrar estos. Los forks son de terceros y no se listan. Fuente de verdad: GitHub (`gh repo list`).

### Activos

| Repo | Privado | Descripción |
|---|---|---|
| workspace_openclaw | ✅ | El workspace |
| kanam-skills | - | Repo público + web de agent skills |
| kanam-story | - | Co-writer de ficción local-first |
| kanam-mind | - | Segundo cerebro local-first con IA |
| kanam-solitaires | - | Colección de solitarios PWA |
| soporteml | - | CRM multi-tenant para ML sellers (v1) |
| soporteml-v4 | ✅ | SoporteML V4 - reinicio con diseño avanzado |
| a11y-fixer | - | Accessibility fix engine |
| ai-developer-stack | - | Skills de ingeniería con IA |
| create-stack | - | Scaffolder opinado Next.js |
| create-with-ai | ✅ | Generador de apps con IA |
| accessible-ui | ✅ | Headless component library |
| quedamos | ✅ | App PWA de matching para salidas |
| kanam-forge | - | Herramienta de forja de skills |

### Archivados (existen en gh, sin clon local)

| Repo | Privado | Estado |
|---|---|---|
| soporteml-v3 | ✅ | ARCHIVED |
| ai-engineering-bootcamp | - | ARCHIVED - curso 10/10 completado |
| hyatt-copilot-agent | ✅ | ARCHIVED |
| ensulugar | - | ARCHIVED |
| cabala | - | ARCHIVED |
| health-tracker | - | ARCHIVED |
| umbrawriter | ✅ | En Lovable, sin clon local |

## Repos eliminados / inexistentes

- **Moderno-Access-Virtual-Plate** → eliminado
- **antigravity-developer-stack** → eliminado (contenido migrado a ai-developer-stack)
- **copilot-skills** → eliminado (reemplazado por workflow-kit, que tampoco existe ya en gh)
- **workflow-kit** → eliminado (no existe en gh ni en npm)
- **accessibility-auditor** → eliminado (no existe en gh; estaba como submodulo muerto)
- **sudolab** → eliminado (no existe en gh; estaba como submodulo muerto)
- **react-18-design-patterns** → eliminado (no existe en gh; estaba como submodulo muerto)
- **react-anti-patterns-book** → eliminado (no existe en gh; estaba como submodulo muerto)
- **umbrawriter-v2** → eliminado (no existe en gh; estaba como submodulo muerto)
- **sportcars** → eliminado (decisión 2026-08-17)
- **futbol-ps2** → eliminado (MVP completo, descartado)
- **kanam** → eliminado (PWA sistema operativo personal con IA, decisión 2026-08-06; BRIEF + ROADMAP en `projects/_archived/kanam/`)
- **chatgpt-project-architect** → archivado (absorbido por AGDS)
- **0001** → eliminar o archivar (sin propósito)
- **prueba_minecraft_claude_code** → eliminar o archivar (experimento abandonado)
