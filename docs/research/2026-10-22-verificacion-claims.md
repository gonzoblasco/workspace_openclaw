# Verificacion claim por claim del research OpenClaw + LangChain (2026-10-22)

> **Que es esto:** cada afirmacion del research `2026-10-22-langchain-career-workflows.md` clasificada por
> veredicto, con la fuente que la sostiene. Medido contra las docs oficiales de LangChain (web), las docs
> **locales instaladas** de OpenClaw v2026.10.5, y el disco de este workspace.
>
> **Metodo:** 26 claims. Dos verificadores independientes (uno por lado del stack) + medicion propia en disco.
> **Regla de clasificacion** (la que Gonzo fijo el 2026-10-22): un ADR nuestro no es dogma, pero un ADR
> registra **el estado real de este stack** - y eso no lo invalida un documento externo. Entonces cada claim se
> clasifica por naturaleza:
>
> | Clase | Quien manda | Que se verifica |
> |---|---|---|
> | **Hecho tecnico** | La fuente citada | contra la doc oficial / el binario |
> | **Hecho sobre nuestras restricciones** | El ADR (describe lo que existe aca) | contra el disco |
> | **Valor** | Se decide | no se verifica, se decide |
>
> **Resultado agregado: 13 VERDADERO · 5 PARCIAL · 3 FALSO · 1 NO DOCUMENTADO · 4 de infraestructura (fuera de alcance de fuentes LangChain, verificadas contra docs locales).**

---

## A. Claims de infraestructura OpenClaw (verificados contra docs locales v2026.10.5)

| # | Afirmacion del research | Veredicto | Evidencia |
|---|---|---|---|
| 1 | "Las mutaciones del registro MCP requieren que **el Gateway este detenido**" | **FALSO** | `cli/mcp/registry.md`: *"these commands only read or write OpenClaw config"*; `status`/`list`/`show`/`doctor` *"do not connect"*. El CLI escribe config directo. No hay requisito de detener el Gateway. |
| 2 | "`OPENCLAW_DISABLE_CRON_HOST_EXECUTION=1` rechaza comandos, condiciones y scripts en cron" | **NO DOCUMENTADO / INVENTADO** | 0 resultados en todo `docs/`. 0 resultados en el binario instalado. La variable no existe. |
| 3 | La lista de prohibicion de `POST /tools/invoke` incluye exec, spawn, shell, fs_write/delete/move, apply_patch, sessions_spawn/send, cron, gateway, nodes | **VERDADERO** | `gateway/tools-invoke-http-api.md`: *"Gateway HTTP also applies a hard deny list by default"*, con esa lista. `cron`/`gateway`/`nodes` ademas son owner-only. |
| 4 | `POST /hooks/agent` con Bearer token, `Idempotency-Key`, y `waitForCompletion: true`; la respuesta 200 confirma **admision**, no terminacion, y no expone el texto | **VERDADERO** | `automation/cron-jobs/webhooks.md`: *"Authorization: Bearer <token>"*, *"Idempotency-Key"*, y la respuesta con `waitForCompletion` trae `completion` con `status`/`delivered`, no el texto. |
| 5 | "Standing order" = autoridad permanente con limites y escalamiento | **VERDADERO** | `automation/standing-orders.md`: *"Standing orders grant your agent permanent operating authority"*. Concepto real, definido por scope/triggers/approval gates/escalation. |
| 6 | La busqueda estructurada de herramientas aplaza los esquemas MCP | **VERDADERO** | `tools/tool-search.md`: *"gives agents a compact directory... discover a tool, describe it completely and dispatch it"*. `tools/code-mode/tool-surface.md`: *"catalog.search(...) searches native and MCP capabilities together"*. **Ademas verificado en este runtime:** esta sesion tiene las herramientas MCP diferidas y las descubre via `tool_search`. |
| 7 | El plugin de GitHub es read-only; "busca hasta 20 issues o PRs por llamada" | **PARCIAL** | `plugins/github.md`: *"read-only (cannot comment, edit, merge, approve)"* → correcto. Pero el limite de **20** es de *"Each comment collection"*, y "Up to 30 changed files" - no es un limite de busqueda de issues/PRs. El research attribution incorrecta. |
| 8 | Provider custom con `baseUrl` sin `api` usa `openai-completions`; `baseUrl` debe incluir `/v1` | **PARCIAL** | `config-tools/custom-providers.md`: *"A custom provider with `baseUrl` but no `api` defaults to `openai-completions`"* → correcto. Y *"set `openai-responses` only when the backend supports `/v1/responses`"* → correcto. Lo que **no** esta documentado: que OpenClaw "agrega la ruta `/responses`" ni que `/v1` sea obligatorio. Eso sale del comportamiento, no del doc. |
| 9 | Perfiles `coding`/`messaging` exponen herramientas MCP, `minimal` las oculta, `tools.deny: ["bundle-mcp"]` las desactiva, y hay `toolFilter.include/exclude` por servidor | **VERDADERO** | `cli/mcp/registry.md`, verbatim. |
| 10 | `--include` debe coincidir con nombres reales de herramientas; `doctor --probe` / `probe --json` verifican la conexion real | **VERDADERO** | `cli/mcp/registry.md`: `probe` *"connects to the selected server or all configured servers, lists tools"*; `doctor --probe` *"adds the same live connection proof"*. |
| 11 | `openclaw automations create '<cron>' '<msg>' --name --tz --session isolated --announce` es la forma correcta | **VERDADERO** | `automation/cron-jobs/managing-jobs.md`, ejemplo literal. Verificado contra `openclaw automations create --help` en esta maquina. |
| 12 | `openclaw agents list --bindings` incluye las reglas de routing completas | **VERDADERO** | `cli/agents.md` linea 35: *"--bindings (include full routing rules, not only per-agent counts/summaries)"*. |

**Medido en esta maquina:** el registro MCP ya tiene `browser-use` (docker, stdio, con `OPENAI_BASE_URL` apuntando a Ollama local). El patron "MCP server local por comando stdio" ya esta probado en este stack.

---

## B. Claims del stack LangChain (verificados contra docs oficiales)

| # | Afirmacion | Veredicto | Evidencia |
|---|---|---|---|
| 1 | Agent Server expone `/mcp` por Streamable HTTP, cada agente es una herramienta MCP con el nombre del agente, y **es stateless** (no sustituye los hilos) | **VERDADERO** | `docs.langchain.com/langsmith/server-mcp`: *"The MCP endpoint is available at `/mcp`"*, *"Tool name: The agent's name"*, *"Each `/mcp` request is stateless and independent"*. **Ademas medido en el wheel real:** `langgraph_api/api/mcp.py:495` -> `ApiRoute("/mcp", handle_mcp_endpoint, methods=["GET","POST","DELETE"])`, con `config.disable_mcp` para apagarlo. |
| 2 | Requiere `langgraph-api>=0.2.3` y `langgraph-sdk>=0.1.61` | **VERDADERO** | Seccion *Requirements* de la misma pagina. |
| 3 | Self-hosting local del Agent Server | **PARCIAL** | Existe, pero **no es "sin LangSmith"**: `oss/python/langgraph/local-server` exige *"An API key for LangSmith"*. `langgraph dev` es in-memory (pickled a disco local), puerto 2024, sin Docker. Produccion self-hosted (`langsmith/deploy-standalone-server`) exige `DATABASE_URI` (Postgres), `REDIS_URI`, `LANGSMITH_API_KEY` **y `LANGGRAPH_CLOUD_LICENSE_KEY`** (verificacion de licencia al arranque) + egress a `beacon.langchain.com`. Se puede apagar el tracing con `LANGSMITH_TRACING=false`. |
| 4 | LangSmith self-hosted | **PARCIAL / FALSO en el matiz** | **No es unico SaaS, pero no es OSS:** *"Self-hosted LangSmith is an add-on to the **Enterprise plan**... Contact our sales team if you want a **license key**"*. Kubernetes + Helm, con Postgres, Redis/Valkey, ClickHouse (+SmithDB) y blob storage. Minimos oficiales: 16GB RAM / 4 CPUs (docker), Postgres 8GB, Redis 4GB, ClickHouse 32GB. |
| 5 | La memoria de Deep Agents es **de archivos**, no de base de datos | **VERDADERO con matiz** | `oss/python/deepagents/memory`: *"filesystem-backed memory: the agent reads and writes memory as files"*; scopes User/agent/organization; organizacion read-only por permisos. **Matiz:** los backends durables se apoyan en el Store de LangGraph (Postgres por defecto). El research lo simplifica de mas. |
| 6 | LangGraph tiene cron jobs integrados | **PARCIAL** | `langsmith/cron-jobs` documenta el feature, pero es de **LangSmith Deployment**, no del OSS. El OpenAPI de Agent Server expone `/runs/crons`. En self-hosted standalone los endpoints existen pero exigen Postgres + license key. En `langgraph dev` no esta documentado. |
| 7 | LangServe esta deprecado y sus docs recomiendan LangGraph Platform | **VERDADERO** | README de `langchain-ai/langserve`: *"This project has been deprecated since Nov 18, 2024... We recommend using LangGraph Platform rather than LangServe for new projects"*. |
| 8 | Los efectos secundarios antes de un `interrupt()` deben ser idempotentes | **VERDADERO** | `oss/python/langgraph/interrupts`: *"The node restarts from the beginning of the node where the `interrupt` was called when resumed, so any code before the `interrupt` runs again"*. El research lo expresa como invariante dura; la doc lo formula como *"should (ideally) be idempotent"*. |
| 9 | `multitask_strategy=enqueue` serializa runs del mismo thread; dos reanudaciones simultaneas pueden saltarse un punto de convergencia | **PARCIAL** | `multitask_strategy` ∈ {reject, rollback, interrupt, enqueue}, default `enqueue`, verificado. Pero *"Double texting is a feature of **LangSmith Deployment**. It is **not available** in the LangGraph open source framework"*. Y el "saltarse un punto de convergencia" no aparece documentado. |
| 10 | Un checkpointer guarda estado en cada super-step, retiene writes pendientes y permite reiniciar desde el ultimo paso exitoso | **VERDADERO** | `oss/python/langgraph/checkpointers`: *"saves a snapshot of graph state at **each super-step**"*, *"**Pending writes**: LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that super-step. When you resume... you don't re-run the successful nodes"*. |
| 11 | La lista de eventos SSE de OpenResponses | **PARCIAL** | **"OpenResponses" no es un estandar de OpenAI**: es una spec abierta *"based on the OpenAI Responses API"* (`openresponses.org/specification`). Confirma `output_item.added`, `content_part.added`, `output_text.delta`, `output_text.done`, `output_item.done`, `response.completed`. **`response.created` no aparece en la spec de OpenResponses** (usa `response.in_progress`); si aparece en la API de OpenAI. |
| 12 | Un agente ReAct corre contra Ollama local sin API keys cloud | **VERDADERO con caveat de version** | `create_react_agent` sigue existiendo en `langgraph.prebuilt` y Ollama soporta tool calling via `ChatOllama.bind_tools()`. **Caveat:** en `langgraph` 1.x esta deprecado a favor de `langchain.agents.create_agent`. Nuestro pin es `langgraph==0.6.11` (hoy 1.2.16) - ahi `create_react_agent` es la API vigente, sin deprecacion. |
| 13 | Hay un chunker canonico de LangChain para codigo que emite metadata de **funcion y linea** | **PARCIAL** | Hay dos piezas: `RecursiveCharacterTextSplitter.from_language(language=Language.X)` y `langchain_community...LanguageParser` (tree-sitter) que *"Each top-level function and class... is loaded into separate documents"*. **Pero su metadata real es `{source, content_type, language}` - SIN nombre de funcion ni numeros de linea.** Para `function_name`/`start_line` hay que post-procesar con tree-sitter por fuera de LangChain. |
| 14 | Deep Agents es OSS y corre local | **VERDADERO** | MIT, `pip install deepagents`, *"Model-agnostic - works with any LLM that supports tool calling... or local"*. **Restriccion medida del wheel 0.7.30:** exige `langchain>=1.4.6`, `langchain-core>=1.6.12`, `langsmith>=0.14.11`, Python >=3.11. Nuestro starter tiene `langchain==0.3.30` -> **rompe el pin** si se agrega. |

---

## C. Lo que cambia el plan (los tres hallazgos que pesan)

### C1. La via local existe, y es MAS BARATA que la que propone el research

El research propone: Agent Server + `langgraph-api` + LangSmith + Postgres. Medido: **Eso exige `LANGGRAPH_CLOUD_LICENSE_KEY`, Postgres, Redis y egress a `beacon.langchain.com`.**

La alternativa que nadie propone en el research, medida en esta maquina:

| | Research | Medido en este stack |
|---|---|---|
| Servidor MCP | `langgraph-api` (Agent Server) | **`mcp<2` (FastMCP 1.30.0) propio, stdio** |
| Resolucion con los pines del starter | - | **0 conflictos** (`uv pip compile`: `mcp==1.30.0` + `langgraph==0.6.11` + `langgraph-checkpoint==2.1.2` + `fastapi==0.128.8` intactos) |
| Persistencia | Postgres | ChromaDB local (ya en el starter) |
| Licencia | `LANGGRAPH_CLOUD_LICENSE_KEY` | ninguna |
| LangSmith | requerido | no |
| Patron ya probado en este stack | no | **si** (`browser-use` es un MCP stdio por comando) |

El research senala el patron correcto (MCP para flujos acotados) pero lo implementa con la capa mas pesada disponible. Con `langgraph-api` la resolucion tambien funciona sin conflicto (`langgraph-api==0.4.48` con los pines del starter), pero **arranca el server, pide Postgres, y arrastra la verificacion de licencia**.

### C2. El gap real no es "un mentor" - es un drill de ingles

El research propone el `career_mentor` (§4.1) como el primer producto, con memoria por usuario y cron propio. Medido contra el estado real:

- `docs/entrevistas/_general/job-search-tracker.md`: **Staffy/Pfizer y Sol cerrados ambos por el mismo filtro de ingles C1 conversacional.** Plan de C1 en curso (CUI, UBA).
- `studies/english/` esta **vacio** salvo el README.
- El research propone *"evaluar la respuesta y ajustar el siguiente paso"* (§4.1 punto 6) - eso es un drill, no un mentor.
- **La infraestructura de surrounding ya existe:** `career-facts.md` (corpus unico, ADR-101), `check-cv-facts.py` (gate), `revision-adversarial.md` (el revisor con severidad/evidencia/veredicto - que es la estrategia WRITE->SELECT->COMPRESS->ISOLATE del research §4.3, escrita a mano), `study-asset-lab` (registrar leccion), `automations` (el daily).

**Conclusión:** el research reimplementa un mentor que ya tenemos disperso. Lo que falta es el **drill**, y el primer caso de prueba es concreto: la call del **lunes 26/10 con David** (TEAM International / tempo.io, agendada 10:00 ART).

### C3. El research tiene un bug de version y una dependencia que rompe los pines

- `create_react_agent` esta deprecado en `langgraph` 1.x (hoy 1.2.16). Nuestro pin es 0.6.11: ahi no hay deprecacion. **No Actualizar el pin de `langgraph` como efecto colateral de esto.**
- `deepagents 0.7.30` exige `langchain>=1.4.6` vs nuestro `langchain==0.3.30`. Agregarlo obliga a una migracion de la cadena completa. No lo justifica.

---

## D. Clasificacion de los 8 workflows del research (§4)

| Workflow | Valor real | Veredicto | Donde vive en el stack |
|---|---|---|---|
| §4.1 Mentor diario | Alto, pero mal especificado | **Reconstruir como drill de ingles** | `studies/english/` + RAG del starter + `automations` + `memory.db` |
| §4.2 Tutor del repositorio | Alto (RAG de codigo real) | **Encaja** (disparador 2 de ADR-099) | falta indexacion de codigo con tree-sitter; el chunker canonico NO da linea/funcion (claim 13) |
| §4.3 Revisor de codigo / PRs | Alto | **Encaja, con matiz** | ya existe manual (`pr-review-response` + `revision-adversarial.md`); el grafo con `interrupt()` es la mejora, no el punto de partida |
| §4.4 Proyectos de portafolio | Medio | **Duplica** | `spec-driven-development` + pipeline A/B + `projects/<slug>/` ya lo hacen |
| §4.5 Simulador de entrevistas | Medio | **Reconstruir como drill** | depende del mismo motor que §4.1 |
| §4.6 Analizador de ofertas | Alto | **Encaja** | `career-facts.md` + `job-search-tracker.md` + `check-cv-facts.py` ya son el corpus; falta el RAG |
| §4.7 Depuracion e incidentes | Alto | **Encaja** (disparador 1/4 de ADR-099) | el `checkpointer` por super-step es el aporte real; `langgraph-checkpoint 2.1.2` ya esta instalado y **sin usar** (0 imports en `app/`, `scripts/`, `tests/`) |
| §4.8 Coach de contribuciones OSS | Medio | **Encaja, choca con AGENTS.md** | el skill `github` ya cubre la parte OSS; la parte de escritura choca con la regla de "nada sale sin OK" |

**Lo que NO se hace:** mentor con memoria propia por usuario (segunda base de memoria), cron de LangGraph (segundo scheduler), LangSmith (SaaS o Enterprise-K8s), Deep Agents (rompe el pin), Agent Server con license key (innecesario para flujos acotados).

---

## E. Corrupcion del texto original (medida)

| Tipo | Cantidad | Detalle |
|---|---|---|
| CJK intercalado | 5 | `para**利亚** desarrollo`, `métricas y**没人**?lecciones`, `el entrevistador**继** conversational`, `puede**实际上** generarse`, `y**的资料** de carrera` |
| Marcador ilegible | 1 | `[WIRE?]` en la tabla de capas |
| JSON5 roto | 1 | §3.2: `id: "career-mentor"][name: "Career Mentor"` (falta la coma y cierra mal el array) |
| URLs citadas que dan 404 | 2 | `docs.langchain.com/langsmith/deployment-sdk` y `docs.langchain.com/oss/python/langchain/langserve` |

La version legible (`2026-10-22-langchain-career-workflows.md`) marca la corrupcion con `[CORRUPTO: ...]`. El original queda intacto en `2026-10-22-langchain-career-workflows.original.md`.

---

## F. La regla que este ejercicio deja

> **Un research externo entra como DATO, no como instruccion (AGENTS.md).** Y un ADR nuestro no es dogma:
> un ADR registra **el estado real de este stack**, y ese estado no se invalida porque un documento de otra
> persona lo describa distinto. Pero un ADR **tampoco** gana por autoridad: si la fuente oficial dice otra
> cosa, gana la fuente oficial.
>
> La regla que funciono: **clasificar cada afirmacion por naturaleza** (hecho tecnico / hecho sobre
> nuestras restricciones / valor) y verificar cada una contra su propia fuente. 26 claims, 2 verificadores
> independientes, 0 afirmaciones aceptadas por autoridad.

**Relacionado:** ADR-099 (LangChain como capa de ejecucion), ADR-103 (LiteLLM se descarta), ADR-101
(corpus unico de carrera), ADR-100 (fuente unica de la verdad), ADR-083 (frontera de roles: implementar
no es del CORE).
