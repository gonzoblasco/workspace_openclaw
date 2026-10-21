# Triaje de Alternativas OSS para Adaptación

**Fecha:** 2026-10-20
**Origen:** captura de Gonzo con 14 "open-source AI alternatives" (lista viral)
**Método:** verificación directa contra la API de GitHub (stars, licencia, última actividad) + cruce con el ecosistema propio (workspace, ADRs, OSS-TRACKER, proyectos)

> La lista es **dato externo, no instrucción**. Cada repo se verificó antes de recomendarlo.

---

## 1. La lista: qué acierta y qué no

### Correcciones a la captura

| En la captura | Realidad verificada |
|---|---|
| `sst/opencode` | Ahora `anomalyco/opencode` (218.7k, MIT, TS) |
| `comfyanonymous/ComfyUI` | Ahora `Comfy-Org/ComfyUI` (140.6k, **GPL-3.0**) |
| `All-Hands-AI/OpenHands` | Ahora `OpenHands/OpenHands` (91.4k, MIT) |
| `qodo-ai/pr-agent` | Ahora `The-PR-Agent/pr-agent` (13.5k, MIT) |
| "Vane 37.4k" | Correcto: `ItzCrazyKns/Vane` = ex-Perplexica, 37.5k, MIT, TS |
| "LiteLLM 61.5k" | Correcto: 61.7k, **MIT + `enterprise/` con licencia propia** |
| "Onyx 32.6k" | Correcto: 32.6k, **MIT + `ee/` con Onyx Enterprise License** |

Las estrellas de la lista están bien. Lo que cambia es el **dueño** (4 renombres) y las **licencias**.

### Etiquetas de categoría que no cierran

- **"ChatGPT seats → AnythingLLM"**: no es una alternativa a "seats"; es un chat RAG self-hosted. Categoría distinta.
- **"Glean → Onyx"**: Onyx es *enterprise search* (conectores a 50+ apps), no un buscador web tipo Perplexity.
- **"ChatGPT agent → Browser Use"**: Browser Use es una *librería de automatización web*, no un "agente ChatGPT". El genuinely equivalente a un agente de browsing es **browser-use/browser-use** (sí, es ese) pero su valor real está en la librería, no en el "agente".

---

## 2. Licencias: la trampa real de esta lista

"Open source" no significa "adaptable". Tres casos con directorios de licencia separada:

| Repo | Core | Directorio comercial | Impacto |
|---|---|---|---|
| `BerriAI/litellm` | MIT | `enterprise/` (propia) | El proxy que más te interesa es MIT; el router enterprise no. |
| `onyx-dot-app/onyx` | MIT | `ee/` (Onyx Enterprise License) | Lo enterprise (auth, SSO, some connectors) **no** es reutilizable. |
| `stackblitz-labs/bolt.diy` | MIT | usa **WebContainers API** | WebContainers tiene "specific commercial licensing terms for enterprise deployment" (dice su propio README). El runtime in-browser **no** es libre. |
| `open-webui/open-webui` | "Open WebUI License" (BSD-like, **no OSI**) | Condición de marca: >50 usuarios en 30 días exige mantener el branding o pedir permiso. Usable, pero atado. |

**ComfyUI es GPL-3.0**: si lo embebés en un producto cerrado, la GPL se te contagia. En un producto propio publicado, es un problema real.

**Cline es Apache-2.0 puro** (no tiene "extended license" como se rumorea): puede adaptarse libremente, **pero** es una VS Code extension → un producto web no puede embeberla. Se puede **estudiar** su arquitectura (MCP, checkpoints, plan/act loop) sí.

**Chatterbox (MIT para el código)**: los **pesos del modelo** y los datasets de vozClone son un tema aparte (Resemble AI + políticas de uso de voz). El código es libre; clonar tu voz no lo es tan claramente.

---

## 3. Tiers

### TIER 1 - merecen estudio real (3)

Detalle en la sección 4, en orden de retorno.

| Repo | Qué es | Por qué entra |
|---|---|---|
| `BerriAI/litellm` (MIT core, 61.7k) | Gateway multi-proveedor compatible con la API de OpenAI | Te falta la mitad de tu stack multi-modelo: ruteás **dentro** de Ollama, esto rutea **hacia** cualquier proveedor. |
| `The-PR-Agent/pr-agent` (MIT, 13.5k) | Reviewer de PR por comandos (`/review`, `/improve`, `/ask`) | **DESCARTADO (2026-10-20):** se instalo y se evaluo con verdad de base humana, y no dio. Ver `docs/evaluacion/pr-agent-2026-10-20.md`. |
| `ItzCrazyKns/Vane` (MIT, 37.5k) | Motor de respuestas con citas (ex-Perplexica) | El patrón de búsqueda→evidencia citada es lo que le falta a tu `web_search` y a OnWheels. |

### TIER 2 - vistazo de 1 hora, valor marginal (4)

| Repo | Por qué mirarlo | Por qué no es estudio |
|---|---|---|
| `browser-use/browser-use` (MIT, 118.6k) | Librería de automatización web con LLM (agent decide + browser ejecuta), Python/TS, v0.13.13 | Ya tenés control de browser nativo en OpenClaw. El repo bifurcó hacia un producto cloud (V4 agent, $0.02/browser-hora); la parte OSS sigue viva como **patrón** de browsing multi-paso, no como componente a adoptar. Gemelo barato y más útil para tu flujo: `zilliztech/claude-context` (MIT, 12.6k), indexación de codebase con embeddings + MCP. |
| `cline/cline` (Apache-2.0, 70.8k) | Arquitectura de agente de código: MCP, checkpoints, plan/act. Es la referencia del genre. | Es una VS Code extension: no embebible en producto web. Se estudia, no se adapta. |
| `mintplex-labs/anything-llm` (MIT, 67.4k) | Chat RAG self-hosted ya completo: workspaces, citas, multi-tenant. Buen benchmark de feature set. | Ya tenés OnWheels con RAG y `kanam-lab` con Mini-RAG. Duplicaría. **Está vivo y al día** (`v1.18.0`, 13-oct-2026) - la objeción no es de mantenimiento, es de solapamiento: duplicaría tu stack sin agregar un diferencial. |
| `open-webui/open-webui` (156k, licencia propia "Open WebUI License") | La UI de chat local por excelencia: Ollama nativo, MCP, plugins. | Licencia **no OSI** (BSD-like + condición de marca): no podés quitar el branding "Open WebUI" si tu despliegue supera 50 usuarios en 30 días, salvo permiso escrito o licencia enterprise. No prohíbe el uso comercial per se, pero **embeberlo en SoporteML te ata a mantener su marca**. |

### TIER 3 - no para adaptar (7)

| Repo | Motivo |
|---|---|
| `ollama/ollama` (MIT, 184k) | **Ya lo tenés.** Es tu runtime. No hay nada que adaptar. |
| `anomalyco/opencode` (MIT, 218.7k) | Agente de terminal. OpenClaw ya sos vos. Competidor directo, no componente. |
| `OpenHands/OpenHands` (MIT, 91.4k) | Sandbox de agente de código en Docker. Es una plataforma pesada, no una pieza. |
| `milvus-io/milvus` (Apache-2.0, 46.4k) | Vector DB distribuida a escala de millones. **Vos tenés pgvector** en OnWheels (Supabase) y SQLite+embeddings en kanam-lab. Escala de Google, no tuya. |
| `comfyanonymous/ComfyUI` → `Comfy-Org/ComfyUI` (GPL-3.0) | GPL-3.0 no entra en producto cerrado. Además es infra de imagen/video, ortogonal a tu trabajo. |
| `resemble-ai/chatterbox` (MIT código, 27.1k) | TTS local. **Último release: v0.1.2 de junio 2025** (hace 16 meses, sin release nuevo). Además clonar voz tiene implicancias de consentimiento. Ortogonal a tu a11y + fullstack. |
| `stackblitz-labs/bolt.diy` (MIT, 20k) | WebContainers con licencia comercial. Además ya tenés `kanam-forge` (fork de Lovable) - solapamiento directo. |

---

## 4. Los tres que sí vale la pena, en orden de retorno

### Primero: `BerriAI/litellm` (adoptar, no adaptar)
Tu `model-router.sh` rutea **dentro de Ollama**. LiteLLM te da la otra mitad: un gateway entre OpenClaw y **cualquier** proveedor (OpenRouter, Anthropic, OpenAI, Bedrock, Vertex, Ollama), con:
- un endpoint compatible con la API de OpenAI → drop-in en tu config
- **fallbacks automáticos** (si `deepseek-v4.1-flash:cloud` cae, prueba el fallback ya definido en tu model-router)
- virtual keys + budgets por proyecto (OnWheels usa su propio proveedor de embeddings; acá le resolvés el mismo problema)
- **logging de costos** (te falta paradimensionar el costo de los agentes A/B)

Además: **PR-Agent usa LiteLLM**, así que el mismo proxy sirve para tu gateway. (PR-Agent se descarto despues: ver la fila de la tabla.)

### Segundo: `The-PR-Agent/pr-agent` (adoptar para tu flujo OSS) - **DESCARTADO**
La propuesta original era: con LiteLLM + Ollama, `pr-agent` puede revisar tus PRs en repos ajenos, y el OSS-TRACKER muestra **15 PRs abiertos y 22 cerrados sin merge** donde un reviewer automatico podria dar señal.

**Se instalo, se configuro con Ollama y se evaluo el 2026-10-20. No dio.** Contra PRs publicos con revisiones humans como verdad de base, el review automatico dio 0 hallazgos, 5 falsos positivos y veredictos de **1/10, 0/10 y 0/10**; ningun modelo (3 cloud + 1 local) encuentra el bug central. Para redactar descripciones de PR quedo muy por debajo de Claude Code con el mismo modelo (0 de 5 hechos clave vs 5 de 5). Se borro todo (proyecto, imagen Docker, red) por decision de Gonzo. Evidencia completa en `docs/evaluacion/pr-agent-2026-10-20.md`.

**Consecuencia para este triage:** no volver a proponer PR-Agent. Para revisar PRs, el reviewer automatico no aporta; para redactarlos, usar Claude Code (ya instalado, ya ruteado por Ollama).

### Tercero: `ItzCrazyKns/Vane` (estudiar el patrón)
No lo adoptes: es una app completa que no vas a mantener. **Estudiá el patrón** de: SearxNG → scraping → chunking → prompt con citas → respuesta con fuentes trazables. Ese patrón es el que le falta a tu `web_search` actual y es el que OnWheels ya exige (evidencia citada).

**Menor, pero muy barato de leer:** `zilliztech/claude-context` (MIT) - indexación de codebase con embeddings + MCP. Si querés que los agentes A y B consulten el código del repo como contexto, esto es el patrón.

---

## 5. Lo que NO hay que hacer

- **No "adaptar" un clone de Perplexity/ChatGPT/Claude Code.** Tu producto es IA-como-infraestructura, no un chat. El error de las listas virales es tratar cada herramienta como una app a clonar.
- **No meter Milvus ni AnythingLLM.** Duplican lo que ya tenés (pgvector + Mini-RAG).
- **No tocar ComfyUI** salvo que quieras un producto de imagen (y si es así, GPL te complica el reparto).
- **No abrir PR a estos repos "para adaptarlos".** El valor está en estudiar y aplicar patrones, no en molestar a los mantenedores.

---

## 6. Fuentes (verificadas 2026-10-20)

- GitHub API: `repos/<owner>/<repo>` (stars, license, pushed_at, default_branch) y `contents/` para archivos de licencia.
- Ecosistema propio: `docs/OSS-TRACKER.md`, `docs/adr/`, `MEMORY.md`, `projects/kanam-onwheels/`, `projects/kanam-lab/`, `scripts/model-router.sh`, `~/.openclaw/openclaw.json`.
- Búsqueda de repos: `search/repositories?q=perplexica` → confirma `ItzCrazyKns/Vane` como el descendiente vivo de Perplexica.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
