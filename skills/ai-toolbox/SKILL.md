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
description: "Registro vivo de las herramientas IA instaladas en la maquina (Onyx, browser-use, PR-Agent, AnythingLLM, LiteLLM, Milvus, Vane, opencode, OpenHands + Ollama). Responde que hay instalado, que esta corriendo ahora, y como se levanta cada cosa, consultando Docker y sondas HTTP reales."
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

`ollama`, `onyx`, `browser-use`, `pr-agent`, `anythingllm`, `litellm`, `milvus`,
`vane`, `opencode`, `openhands`.

## Procedimiento

### "Cargame X"

1. `list` para ver el estado actual. Si ya esta corriendo, no relanzar: decir
   que ya esta y listo.
2. Si esta apagado: `up <id>`, y despues `status <id>` para confirmar que la
   sonda responde. **"corriendo" del container no es "sirviendo":** la sonda
   HTTP es la que prueba.
3. Si la sonda falla pero el container esta arriba, el problema es interno del
   servicio (ver las trampas de `docs/tools/REGISTRY.md`), no el arranque.

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
  proyecto del directorio, no del `name:` (por eso pr-agent es `local` y
  opencode es `docker`). El script empareja por archivo; si se agrega una
  herramienta, el compose tiene que existir en la ruta declarada.
- **La vista de `docs/tools/REGISTRY.md` se regenera con `catalog --write`.**
  Editarla a mano la desincroniza; `catalog --check` lo detecta.
- **browser-use no tiene proceso propio:** lo lanza OpenClaw por sesion como
  server MCP. `up`/`down` no aplican.

## Quando agregar una herramienta nueva

1. Agregar la entrada a la tabla `TOOLS` de `scripts/ai-toolbox.py` (nombre,
   id, puerto, compose, sonda HTTP con los codigos que cuentan como vivo).
2. Escribir la prosa en `docs/tools/REGISTRY.md` (que es, como se levanta, para
   que sirve, trampas).
3. `python3 scripts/ai-toolbox.py catalog --write` para regenerar la tabla.
4. `python3 scripts/ai-toolbox.py status <id>` para verificar que la sonda
   encuentra la herramienta.
