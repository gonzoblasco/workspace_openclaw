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
| browser-use | `browser-use` | docker (stdio, bajo demanda) | - | bajo demanda |
| browser-use UI | `browser-use-ui` | docker compose | 8090 | bajo demanda |
| Vane | `vane` | docker compose | 3005 | bajo demanda |
| Cline | `cline` | nativo (host, Bun 1.4.2) | 8787 | no instalado |
<!-- END:ai-toolbox-table -->

---

## Como se consulta

```bash
./scripts/ai-toolbox.py list              # todo con estado real
./scripts/ai-toolbox.py list --json       # lo mismo, para maquinas
./scripts/ai-toolbox.py status vane        # detalle de una
./scripts/ai-toolbox.py health            # sondas HTTP de todas
./scripts/ai-toolbox.py up vane           # levantar
./scripts/ai-toolbox.py down vane         # parar (conserva volumenes)
./scripts/ai-toolbox.py restart vane      # reiniciar
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
  que es el que usan los clientes OpenAI-compatible y los embeddings).
- **Trampa:** el sufijo `:cloud` del tag NO dice si el modelo es remoto. La
  fuente de verdad es el campo `remote_host` de `GET /api/tags`.
- **Trampa:** para el loop agentico (structured output) los modelos cloud
  devuelven prosa en vez de JSON. Ver la nota de browser-use.

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

### browser-use UI (id: `browser-use-ui`)

- **Que es:** consola web para pilotar a mano el agente de browser-use. Escribis una
  tarea en castellano, el agente navega un Chromium headless real y ves los pasos,
  el screenshot y la respuesta final. La UI **no implementa el agente**: habla MCP
  con `browser-use --mcp` y muestra lo que devuelve.
- **Repo:** `projects/browser-use-ui`. Compose propio con la imagen `browseruse:local`.
- **UI:** http://localhost:8090 (loopback). Health: `/api/health` ->
  `{"ok":true,"mcp_connected":true,...}`.
- **Como se levanta:** `toolbox up browser-use-ui` (o `make up` dentro del repo).
- **Como se para:** `toolbox down browser-use-ui`. A diferencia de las otras
  herramientas del stack, aqui el `down` es **real**: elimina el container y la red
  (su `restart` es `no`, asi que no vuelve sola). El volumen `browseruse-data`
  (el perfil de Chromium) se conserva.
- **Estado por defecto: APAGADA, bajo demanda.** Decision de Gonzo (2026-10-27): es
  una herramienta de prueba, no de uso continuo. Encenderla cuesta ~190 MB de RAM.
- **Relacion con `browser-use` (la de arriba): la MISMA imagen, dos superficies.**
  `browser-use` es la libreria/agente; el MCP que usa OpenClaw lo lanza el gateway
  por sesion con `docker run --rm` (no tiene container fijo). `browser-use-ui` es la
  consola humana que corre en su propio container y habla MCP con un `browser-use
  --mcp` anidado dentro (modo `BROWSER_USE_UI_MCP_MODE=local`, para no depender del
  socket de Docker). **Apagar la UI no afecta al MCP de OpenClaw**: se verifica
  navigating con `browser_navigate` con la UI apagada.
- **Trampa:** el perfil de Chromium NO se puede compartir entre dos containers
  (locks `SingletonLock`): por eso el compose usa un volumen nombrado propio y el
  MCP de OpenClaw usa volumenes anonimos. No unirlos.
- **Detalle:** `projects/browser-use-ui/README.md` y su `.knowledge/HANDOFF.md`.

### Vane (id: `vane`)

- **Que es:** motor de busqueda con respuestas citadas. Privacy-first: combina
  web con indices locales. **Es la herramienta de research del stack**: hace
  busqueda real, scrapea, y devuelve una respuesta en espanol con las fuentes
  citadas y trazables.
- **Repo:** `projects/vane` (fork privado `gonzoblasco/vane`, upstream
  `ItzCrazyKns/Vane`). Imagen `vane-local:ollama`.
- **UI:** http://localhost:3005.
- **Como se levanta:** `toolbox up vane` (alias del registro de herramientas; equivalente a `cd ~/projects/vane && docker compose up -d`)
- **Como se para:** `toolbox down vane` (conserva los datos: `data/` y `uploads/` son bind mounts)
- **Estado por defecto: BAJO DEMANDA** (decision de Gonzo, 2026-10-27). Es de
  uso episodic: se enciende para hacer un research y se apaga. A los ~45 s por
  research, dejarlo prendido sin buscar nada no tiene sentido. Para las
  herramientas bajo demanda, `down` es real (`docker compose down`): elimina
  container y red, y no vuelve sola.
- **Costo:** ~340 MB de RAM, 7 s de arranque en frio.
- **Nota:** SearxNG corre dentro del mismo container (entrypoint, puerto 8080
  interno).
- **Trampa:** el clasificador de Vane pone `skipSearch: true` en preguntas de
  conocimiento general: en ese caso NO busca y devuelve respuesta sin fuentes.
  Es diseno, no bug; para ver el pipeline de busqueda usar consultas que
  requieran informacion actual.
- **Trampa:** el clon local es **shallow** (cortado en `348feca`). Para pushear
  la historia completa hay que hacer `git fetch --unshallow upstream master`
  primero: sin eso, GitHub rechaza el push por objetos faltantes.
- **Trabajo local propio (5 commits, nunca pusheados al upstream):** el fix del
  writer prompt (que hacia filtrar el monologo interno del modelo a la
  respuesta final), el `Dockerfile` con Next.js pineado y bind a `0.0.0.0`, el
  script de preconfig de Ollama, y la memoria `.knowledge/`. Todo eso vive en
  `gonzoblasco/vane` (privado).

### opencode y OpenHands - ELIMINADOS (2026-10-28)

Ambos fueron retirados del stack por decisión de Gonzo (ADR-106): "no busco LO
mejor en ciertas ocasiones sino el único que responda bien siempre".

- **opencode** (servidor de agente, 4096) y **OpenHands** (Agent Canvas, 8000)
  tenían celdas en **0 absoluto** en la cata de harnesses: agentes que no
escribieron nada. Claude Code, en cambio, nunca bajó de 16/30 y nunca quedó
- último (0 de 6 modelos). Con el criterio "el que siempre responde", Claude
- Code es la elección y los otros dos sobran.
- **Qué se borró:** containers, imágenes (`opencode-local:dev` 343 MB y
- `ghcr.io/openhands/agent-canvas:1.28.1` 5.4 GB), volúmenes
- (`docker_opencode-data`, `docker_opencode-state`) y los proyectos
- `projects/opencode` (635 MB) y `projects/openhands` (76 MB).
- **Qué se conservó:** los compose quedaron archivados en
  `docs/tools/compose-archivados/` para poder reintroducirlos sin reescribir la
  configuración. `scripts/preflight-cata.sh` mantiene inerte el bloque de
  catálogo de modelos, guardado por la existencia del container.
- **Nota para el futuro:** reintroducir opencode exige volver a agregar su sonda
  `need` en el preflight y levantar su compose archivado. Sin la sonda, la cata
  arranca sin verificar infra y pierde celdas en silencio.

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
