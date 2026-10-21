---
name: ai-toolbox
metadata:
  category: "Tools"
  tags:
    - tools
    - stack
    - registry
    - ollama
    - docker
description: "Registro vivo de las herramientas IA instaladas en la maquina (Onyx, browser-use, AnythingLLM, LiteLLM, Vane, opencode, OpenHands, Cline + Ollama). Responde que hay instalado, que esta corriendo ahora, y como se levanta cada cosa, consultando Docker y sondas HTTP reales."
user-invocable: true
---

# AI Toolbox

Catalogo vivo de las herramientas IA de la maquina. El estado sale de Docker y de
sondas HTTP reales, no de una lista escrita a mano: por eso no seerve.

**Dueno de los datos:** `scripts/ai-toolbox.py`. **Vista humana + prosa**
(para que sirve cada cosa, credenciales, trampas): `docs/tools/REGISTRY.md`.

## When to use it

- Gonzo pide "cargame X", "levantame Y", "pará Z" (una herramienta concreta).
- Gonzo pregunta "que apps tengo instaladas" o "cuales me quedaron".
- Hay que saber si un servicio esta arriba antes de probarlo.
- Hay que inventariar el stack para una decision (recursos, ports, duplicados).

**No usar para:** elegir modelo (eso es `docs/SETUP.md`), historia de un
proyecto (eso es `projects/<slug>/.knowledge/`), estado de git (eso es `git status`).

## How to use it

Hay un alias en `~/.zshrc` para no escribir la ruta entera:

```bash
toolbox list              # todo con estado real
toolbox status vane       # detalle de una (con rutas y sonda)
toolbox up vane           # levantar
toolbox down vane         # parar (conserva volumenes)
toolbox restart vane      # reiniciar
toolbox health            # sondas HTTP de todas
```

El alias apunta al script del workspace (por eso funciona desde cualquier cwd) y
equivale a:

```bash
./scripts/ai-toolbox.py list              # todo con estado real
./scripts/ai-toolbox.py list --json       # lo mismo, para maquinas
./scripts/ai-toolbox.py status onyx       # detalle de una (con rutas y sonda)
./scripts/ai-toolbox.py health            # sondas HTTP de todas
./scripts/ai-toolbox.py up onyx           # levantar
./scripts/ai-toolbox.py down onyx         # parar (conserva volumenes)
./scripts/ai-toolbox.py restart onyx      # reiniciar
./scripts/ai-toolbox.py catalog --check   # verificar que la vista no seerve
```

### IDs validos

`ollama`, `onyx`, `browser-use`, `anythingllm`, `litellm`,
`vane`, `opencode`, `openhands`, `cline`.

### Cuando la herramienta es Cline

Cline tiene su propio wrapper porque su `up` es un servicio de dos procesos (el
dashboard web y el daemon del hub). El wrapper los maneja juntos y sabe
verificar la salud de verdad:

```bash
./scripts/cline-tool.sh up          # dashboard + daemon (idempotente)
./scripts/cline-tool.sh status      # puertos, salud HTTP, config y workspace
./scripts/cline-tool.sh down        # parar (conserva config y sesiones)
./scripts/cline-tool.sh run --cwd <dir> "<prompt>"   # un turno headless
```

El dashboard queda en http://127.0.0.1:8787 y **el chat del agente en `/chat`**
(no en la home, que es el monitor del hub y no tiene composer).

## Procedimiento

### "Cargame X"

1. `list` para ver el estado actual. Si ya esta corriendo, no relanzar: decir
   que ya esta y listo.
2. Si esta apagado: `up <id>`, y despues `status <id>` para confirmar que la
   sonda responde. **"corriendo" del container no es "sirviendo":** la sonda
   HTTP es la que prueba.
3. Si la sonda falla pero el container esta arriba, el problema es interno del
   servicio (ver las trampas de `docs/tools/REGISTRY.md`), no el arranque.

**`up` ya responde las dos preguntas que importan:** dice el **puerto**, la
**URL** donde abrirla, y el resultado de la **sonda** (con reintentos, porque
un servicio recien arrancado tarda). Si la sonda no llega a responder, avisa
`AUN NO RESPONDE` en vez de fingir que todo bien:

```
==> up Vane
Container vane Started
  puerto: 3005
  url:    http://localhost:3005
  sonda:  http://localhost:3005/ -> HTTP 200 (ok)
```

`down` dice donde quedo parado y que los datos quedan.

**Vane es el ejemplo de referencia:** `toolbox up vane` lo levanta en
http://localhost:3005 y `toolbox down vane` lo para conservando los datos
(`data/` y `uploads/` son bind mounts). El compose vive en
`projects/vane/docker-compose.yml` y el script lo encuentra solo.

### "Que apps tengo"

`list` y pegar la salida. La tabla de `docs/tools/REGISTRY.md` es la vista
humana; `list` es el estado real. Si `list` muestra stacks de compose corriendo
que no tienen ficha, **eso se reporta**: es una herramienta nueva sin registrar.

### "Sacame las que ya no uses"

1. `list` para ver el estado.
2. Para cada candidata, `status <id>`: leer la nota y las trampas de
   `docs/tools/REGISTRY.md` antes de tocar nada.
3. **No borrar a ciegas.** Una herramienta apagada puede tener volumenes con
   datos. `down` (stop) es reversible; borrar volumenes o imagenes no lo es.
4. Reportar que se paro y que se conserva.

## Trampas del registro

- **El estado nunca sale de la tabla del script.** Sale de `docker compose ls`,
  `docker ps` y una sonda HTTP. Si el script dice "apagado" pero el servicio
  responde, el script esta mal, no el servicio.
- **Los codigos HTTP valen segun el servicio.** Un 401 (pide bearer) o un 308
  (redirect) son "vivo": la tabla lo declara por herramienta. Un 502 es
  "caido" aunque el container diga `Up`.
- **`down` hace `stop`, no `down` de compose.** Conserva containers y
  volumenes. Borrar volumenes es otra operacion, y requiere OK explicito.
- **Emparejamiento por ARCHIVO de compose.** Docker deriva el nombre del
  proyecto del directorio, no del `name:` (por eso opencode es `docker` y
  litellm-ollama es `litellm-ollama`). El script empareja por archivo; si se
  agrega una herramienta, el compose tiene que existir en la ruta declarada.
- **La vista de `docs/tools/REGISTRY.md` se regenera con `catalog --write`.**
  Editarla a mano la desincroniza; `catalog --check` lo detecta.
- **browser-use no tiene proceso propio:** lo lanza OpenClaw por sesion como
  server MCP. `up`/`down` no aplican.
- **Cline corre en DOS procesos:** el dashboard (`:8787`) es la UI y el daemon
  del hub (`:25466`) es quien ejecuta las sesiones. Parar el dashboard no para
  el daemon: `cline-tool.sh down` para los dos.
- **Cline: el workspace del chat no es el `WORKSPACE_ROOT`.** Sale de la sesion
  mas reciente que el Hub conoce. Si hay sesiones viejas, su cwd gana.
- **Cline: `ENOENT: posix_spawn '/bin/bash'` no es "falta el shell".** El shell
  existe; lo que falta es el cwd de la sesion.

## Quando agregar una herramienta nueva

1. Agregar la entrada a la tabla `TOOLS` de `scripts/ai-toolbox.py` (nombre,
   id, puerto, compose, sonda HTTP con los codigos que cuentan como vivo).
2. Escribir la prosa en `docs/tools/REGISTRY.md` (que es, como se levanta, para
   que sirve, trampas).
3. `python3 scripts/ai-toolbox.py catalog --write` para regenerar la tabla.
4. `python3 scripts/ai-toolbox.py status <id>` para verificar que la sonda
   encuentra la herramienta.

**Si la herramienta es un servicio nativo con varios procesos** (un dashboard y
un daemon, por ejemplo), el `up`/`down` del registro no alcanza: hace falta un
wrapper propio (como `scripts/cline-tool.sh`) y la entrada declara `paths` en
vez de `compose`.

**Los tests del registro afirman FORMAS, no la existencia de rutas del host.**
El CI corre en Linux, en un checkout distinto, y `projects/` esta ignorado por
`.gitignore`: un test que afirme `Path(compose).exists()` sobre rutas de la Mac
Mini rompe el CI. Un compose puede no estar instalado en la maquina que corre
el test y el registro seguir siendo correcto.
