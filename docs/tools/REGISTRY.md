# REGISTRY.md - Herramientas IA instaladas

> **Catalogo de las herramientas IA que hay en esta maquina** y de como se usan.
> El dueno de los DATOS (que herramientas existen, como se levantan, donde viven)
> es `scripts/ai-toolbox.py`. La tabla de abajo es una VISTA de esos datos, que se
> regenera con `ai-toolbox.py catalog --write` y se verifica con `--check`.
> La PROSA de cada herramienta (para que sirve, credenciales, trampas) vive
> solo aqui: un script no puede guardarla.

> **Como usar esto:** cuando Gonzo pida "cargame X" o "que apps tengo", el
> registro se consulta con `scripts/ai-toolbox.py` (estado real, no de memoria).
> La skill `ai-toolbox` describe el procedimiento.

---

## Tabla de estado (regenerable)

<!-- BEGIN:ai-toolbox-table -->
| Herramienta | ID | Runtime | Puerto | Estado |
|---|---|---|---|---|
| Ollama | `ollama` | nativo (host) | 11434 | corriendo |
| Onyx | `onyx` | docker compose (Lite: 6 servicios) | 3000 | corriendo |
| browser-use | `browser-use` | docker (stdio, bajo demanda) | - | bajo demanda |
| LiteLLM | `litellm` | docker compose | 4000 | no instalado |
| Vane | `vane` | docker compose | 3005 | corriendo |
| opencode | `opencode` | docker compose | 4096 | corriendo |
| OpenHands | `openhands` | docker compose | 8000 | corriendo |
| Cline | `cline` | nativo (host, Bun 1.4.2) | 8787 | apagado |

Stacks de compose corriendo que no tienen ficha:

- `browser-use-ui` (running(1))
<!-- END:ai-toolbox-table -->

---

## Como se consulta

```bash
./scripts/ai-toolbox.py list              # todo con estado real
./scripts/ai-toolbox.py list --json       # lo mismo, para maquinas
./scripts/ai-toolbox.py status onyx       # detalle de una
./scripts/ai-toolbox.py health            # sondas HTTP de todas
./scripts/ai-toolbox.py up onyx           # levantar
./scripts/ai-toolbox.py down onyx         # parar (conserva volumenes)
./scripts/ai-toolbox.py restart onyx      # reiniciar
./scripts/ai-toolbox.py catalog --check   # verificar que la vista no seerve
```

**El estado nunca sale de esta tabla:** sale de `docker compose ls`, de `docker ps`
y de una sonda HTTP real. Por eso el registro no puede envejecer mal. Lo unico
declarado a mano es COMO se levanta cada cosa.

---

## Las herramientas

### Ollama (id: `ollama`)

- **Que es:** el motor LLM. Nativo del host, no dockerizado. Sirve los modelos
  `:cloud` por proxy (la inferencia ocurre en Ollama Cloud, no consume RAM
  local) y los locales en MLX.
- **Como se levanta:** app nativa (`open -a Ollama`). Puerto `11434`, escucha en
  todas las interfaces: por eso los containers la alcanzan en
  `host.docker.internal:11434`.
- **Como se consulta el LLM desde Docker:** `http://host.docker.internal:11434`
  (endpoint nativo) o `http://host.docker.internal:11434/v1` (OpenAI-compatible,
  que es el que usan LiteLLM y los embeddings).
- **Trampa:** el sufijo `:cloud` del tag NO dice si el modelo es remoto. La
  fuente de verdad es el campo `remote_host` de `GET /api/tags`.
- **Trampa:** para el loop agentico (structured output) los modelos cloud
  devuelven prosa en vez de JSON. Ver la nota de browser-use.

### Onyx (id: `onyx`)

- **Que es:** capa de contexto/RAG de equipo (OSS, MIT). Chat con memoria,
  agents, MCP server y sandbox de codigo. Conecta 50+ fuentes (GitHub, Slack,
  Google Drive, etc.) para indexarlas.
- **Repo:** `projects/onyx` (clone de `github.com/onyx-dot-app/onyx`).
- **UI:** http://localhost:3000
- **Como se levanta:**
  ```bash
  cd ~/projects/onyx/deployment/docker_compose
  docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml up -d
  ```
- **Modo Lite:** 6 servicios (api_server, web_server, nginx, relational_db,
  mcp_server, code-interpreter), ~1 GB RAM. Sin OpenSearch, sin Redis, sin model
  servers, sin object store. Postgres hace de cache, file store y auth backend.
- **Por que Lite:** Docker Desktop tiene **8 GB de RAM asignados** (no los 24 GB
  de la maquina) y conviven litellm, opencode, vane,
  openhands y browser-use. El stack completo (OpenSearch con heap de
  2 GB + 2 model servers con torch) no entra comodo.
- **LLM:** provider `ollama_chat` con `api_base=http://host.docker.internal:11434`.
  **Solo modelos cloud** (17 visibles), default `minimax-m3.1-flash:cloud`. Los
  modelos locales del host no estan en el provider: Onyx no los elige y no
  consumen RAM.
- **Como se para:** `docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml stop`.
- **Credenciales:** `projects/onyx/.local/credentials.md` (excluido de git).
- **Lo que NO tiene:** indexacion/RAG/conectores apagados en Lite.
  `DISABLE_VECTOR_DB=true`. Para activarlos hace falta el stack completo
  (Redis + OpenSearch) y embeddings configurados: Onyx no tiene provider
  `ollama` para embeddings, asi que va por `litellm` contra el endpoint
  OpenAI-compatible de Ollama (verificado con `qwen3-embedding:0.6b`, dim 1024).
- **Trampas verificadas:**
  - El email de registro **no puede usar dominio `.local`**: el validador de
    `email_validator` lo rechaza (dominio reservado) y `/api/auth/register`
    devuelve 422. Usar un dominio real.
  - El **login tarda 15-80 s** (bcrypt con la CPU de Docker saturada). Un
    timeout corto corta un login que si iba a completarse.
  - `DOCKER_SOCK_PATH` debe apuntar al socket de Docker Desktop
    (`~/.docker/run/docker.sock`): en macOS no existe `/var/run/docker.sock`.
  - El `api_server` puede ser OOM-killed (exit 137) con muchos containers
    ajenos arriba. Reinicia solo (`restart: unless-stopped`).
  - `code-interpreter` puede marcar `unhealthy` por timeout del
    `docker image inspect` con el daemon saturado. Se recupera solo.
- **Detalle completo:** `projects/onyx/.knowledge/STATUS.md`.

### browser-use (id: `browser-use`)

- **Que es:** agente de navegacion web. Se expone como **server MCP** (16 tools)
  registrado en OpenClaw como `mcp.servers.browser-use`.
- **Repo:** `projects/browser-use`. Imagen `browseruse:local` (3.0 GB, Chromium
  incluido).
- **Como se levanta:** no tiene proceso propio: lo lanza OpenClaw por sesion
  con `docker run` (configurado en `~/.openclaw/openclaw.json`). El compose
  existe para correr el CLI a mano.
- **Trampa (la importante):** los modelos `:cloud` de Ollama **ignoran el JSON
  Schema** y devuelven prosa, asi que el Agent no parsea acciones. Para el loop
  agentico hace falta un modelo **local** (`gemma4:12b-mlx` o `qwen3.5:9b-mlx`).
  Las tools directas del MCP no usan LLM y funcionan con cualquiera.
- **Trampa:** `Agent` pisa el timeout del cliente LLM con su default de 75 s.
  Con un modelo local hay que pasar `llm_timeout` explicito.
- **Trampa:** el clone en macOS deja archivos `0600` y el usuario no-root del
  container no puede leer `/app` -> `ModuleNotFoundError`. Fix en el host
  (`chmod -R a+rX`) y rebuild.
- **Detalle:** `projects/browser-use/README-LOCAL.md`.

### LiteLLM (id: `litellm`)

- **Que es:** proxy OpenAI-compatible que sirve modelos del daemon Ollama del
  host. Un solo lugar donde expose el LLM para varios clientes.
- **Puerto:** `4000`. Health: `/health/liveliness`.
- **Repo:** clon de BerriAI/litellm en `~/experiments/litellm` (fuera del
  workspace); el compose y `config.yaml` en `~/experiments/litellm-ollama/`.
- **Como se levanta:** `cd ~/experiments/litellm-ollama && docker compose up -d`
- **Perfil `local`:** construye la imagen desde el clon local.

### Vane (id: `vane`)

- **Que es:** motor de busqueda con respuestas citadas. Privacy-first: combina
  web con indices locales.
- **Repo:** `projects/vane`. Imagen `vane-local:ollama`.
- **UI:** http://localhost:3005 (el 3000 lo tiene onyx-nginx).
- **Como se levanta:** `toolbox up vane` (alias del registro de herramientas; equivalente a `cd ~/projects/vane && docker compose up -d`)
- **Como se para:** `toolbox down vane` (conserva los datos: `data/` y `uploads/` son bind mounts)
- **Nota:** SearxNG corre dentro del mismo container (entrypoint, puerto 8080
  interno).
- **Trampa:** el clasificador de Vane pone `skipSearch: true` en preguntas de
  conocimiento general: en ese caso NO busca y devuelve respuesta sin fuentes.
  Es diseno, no bug; para ver el pipeline de busqueda usar consultas que
  requieran informacion actual.

### opencode (id: `opencode`)

- **Que es:** servidor de agente de codigo, con sesiones, DB y logs persistidos.
- **Repo:** `projects/opencode`. Imagen `opencode-local:dev` (build local).
- **UI/API:** http://localhost:4096 (loopback, con usuario y password).
- **Como se levanta:** `cd ~/projects/opencode && docker compose -f docker/docker-compose.yml up -d`

### OpenHands (id: `openhands`)

- **Que es:** "Agent Canvas": un agente que ejecuta tareas, con su propia
  interfaz web.
- **Repo:** `projects/openhands`. Imagen oficial all-in-one
  `ghcr.io/openhands/agent-canvas:1.28.1` (arm64).
- **UI:** http://localhost:8000 (loopback). El backend interno escucha en 18000;
  el 8000 es el proxy estatico.
- **Como se levanta:** `cd ~/projects/openhands && docker compose -f docker-compose.ollama.yml up -d`
- **Auth:** sin `LOCAL_BACKEND_API_KEY` el entrypoint genera una key aleatoria
  que hay que leer de los logs. El compose la define, asi que la sesion entra
  directo. Solo es seguro con el puerto en loopback.
- **Estado real:** puede quedar `unhealthy` con el backend caido (el proxy
  responde 502). No es el puerto el que esta mal.

### Cline (id: `cline`)

- **Que es:** agente de codigo open source (clone de `github.com/cline/cline`).
  Tiene tres superficies: CLI (`cline`), Hub dashboard (web) y SDK.
- **Repo:** `projects/cline` (clone shallow, `main` @ `0870796`). Es upstream:
  no se commitea ni se pushea. Lo propio va en `projects/cline/LOCAL-SETUP.md`.
- **Toolchain:** **Bun 1.4.2** (el repo prohibe npm/yarn/pnpm). `build:sdk` es
  obligatorio: los paquetes del SDK se referencian entre si por `dist/`.
- **Provider:** `ollama` contra `http://localhost:11434` (API nativa `/api/chat`,
  no `/v1`: el path OpenAI-compatible ignora `options.num_ctx` y todo modelo
  cargaria con 4096 tokens). Modelo por defecto `minimax-m3.1-flash:cloud`.
- **UI:** http://127.0.0.1:8787 - el dashboard. El chat del agente esta en
  **`/chat`**, no en la home (`/` es el monitor del hub, sin composer).
- **Como se levanta:**
  ```bash
  ./scripts/cline-tool.sh up          # dashboard + daemon
  ./scripts/cline-tool.sh status      # salud real (puertos + HTTP)
  ./scripts/cline-tool.sh down        # parar (conserva config y sesiones)
  ./scripts/cline-tool.sh run --cwd <dir> "<prompt>"   # un turno headless
  ```
- **Dos procesos, no uno:** el dashboard (`:8787`) es la UI y el daemon del hub
  (`:25466`) es quien ejecuta las sesiones. Parar el dashboard no para el daemon.
- **Config aislada:** `CLINE_DIR=projects/cline/.cline-local`. La config real del
  usuario (`~/.cline`, con su sesion OAuth de Cline) **no se toca**.
- **Trampa (la importante):** el workspace del chat **no** sale de
  `WORKSPACE_ROOT` sino de la sesion mas reciente que el Hub conoce
  (`apps/cline-hub/src/server/providers.ts:38`). Si ya hay sesiones, su cwd
  gana. Para cambiar de proyecto: borrar las sesiones (UI: Sessions ->
  eliminar) y reiniciar.
- **Trampa:** `ENOENT: posix_spawn '/bin/bash'` **no** significa que falte el
  shell: `/bin/bash` existe. Lo que falta es el **cwd** de la sesion (un
  `posix_spawn` con cwd inexistente reporta ENOENT). El agente lo interpreta
  como "no hay shell" y deja de usar la terminal. Si una sesion falla asi,
  revisar que su `cwd` exista.
- **Trampa:** las tools se auto-aprueban por default (`autoApproveTools` en
  `true`): el agente ejecuta comandos sin preguntar.
- **Detalle completo:** `projects/cline/LOCAL-SETUP.md`.

---

## Lo que este registro NO es

- **No es el catalogo de modelos.** Ese vive en `docs/SETUP.md` (que modelos
  existen en Ollama, con que contexto y capacidades).
- **No es el registro de proyectos.** Cada proyecto tiene su historia en
  `projects/<slug>/.knowledge/`. Acá va lo que corre como servicio.
- **No es el estado del workspace.** Eso es `git status` y el dashboard.
