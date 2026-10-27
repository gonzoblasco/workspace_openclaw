# browser-use en Docker: el perfil de Chrome NO se comparte

> Fecha: 2026-10-27 · Origen: `projects/browser-use-ui` (U5) · Estado: vigente

## La regla

**El contenedor del MCP NO monta nada en `/data`.**

La imagen `browseruse:local` ya declara `VOLUME /data` y symlinkea
`/home/browseruse/.config/browseruse -> /data`. Si no se monta nada
explícitamente, Docker crea un **volumen anónimo por contenedor**, que se
destruye con él. El perfil queda siempre en manos del usuario del contenedor
(UID 911 `browseruse`) y nunca se comparte.

## Por qué (dos bugs reales, no hipotéticos)

### Bug 1 - el bind mount del host rompe el arranque de Chrome

El MCP montaba el directorio de datos del host:

```
-v /Users/gonzoblasco/.openclaw/workspace/projects/browser-use/config:/home/browseruse/.config/browseruse
```

El host es UID 501 (`gonzoblasco`) con modo `drwx------`; el contenedor corre
como UID 911 (`browseruse`). Chrome no puede abrir el profile: muere al
arrancar y el DOM build devuelve `None`.

Síntomas, textuales:

```
Error: Browser process (PID 27) exited before CDP became available on port 46339
```

```
Error: Expected at least one handler to return a non-None result, but none did!
```

(la segunda es de `bubus`: ningún handler devolvió un resultado)

Cómo se manifestaba:

| Dónde | Síntoma |
|---|---|
| `projects/browser-use-ui` | `GET /api/state` → **HTTP 502** |
| MCP registrado en `openclaw.json` | bundle **"not connected"** |

### Bug 2 - un volumen nombrado compartido rompe la segunda corrida

Con un volumen nombrado, el contenedor del MCP y el de la UI comparten
`/data/profiles/default`. Los dos Chrome pelean por el `SingletonLock` del
mismo `user-data-dir` y el segundo pierde, con el mismo error de DOM build.

Peor: **browser-use no limpia los locks viejos**
(`CHROME_PROFILE_TRANSIENT_FILE_PATTERNS` solo aplica al copiar a un profile
temporal, no al usar uno en el sitio). Así que el volumen queda envenenado
entre corridas: la primera pasa, la segunda falla, y sigue fallando.

## Matriz verificada

| Escenario | Resultado |
|---|---|
| MCP en el host (Chrome real) | ✅ `browser_get_state` → `"Example Domain"` |
| MCP en Docker, profile fresco | ✅ todo funciona |
| MCP en Docker, profile del host montado | ❌ Chrome no arranca → 502 |
| MCP en Docker, volumen nombrado compartido | ❌ 1ª corrida ok, 2ª falla |
| MCP en Docker, volumen anónimo (sin `-v`) | ✅ **dos corridas seguidas** |

## Dónde está aplicado

- `~/.openclaw/openclaw.json` → `mcp.servers.browser-use.args`: se sacó el
  `-v` con la ruta del host. Sin restart: el gateway lo re-spawn solo.
- `projects/browser-use-ui/server/config.py::_docker_args()`: ya no monta
  `/data`.
- `projects/browser-use-ui/docker-compose.yml`: el servicio `ui` **sí** usa un
  volumen nombrado (`browseruse-data`), porque en modo `local` el MCP corre
  dentro de ese mismo contenedor y es el único Chrome que vive ahí. Sin
  competencia por el `SingletonLock`.

## La lección

Antes de afirmar que un contenedor "funciona", probalo **dos veces seguidas**.
El primer arranque contra un volumen recién creado puede fallar una vez
(arranque en frío) y el segundo pasar: un solo run verde no prueba nada.

Y dos señales que se confunden con otros problemas:

- un `pytest` de 40 minutos al 0% de CPU es un **event loop** que no cierra,
  no un test lento;
- "Expected at least one handler to return a non-None result" es de `bubus`
  y significa "un handler devolvió None", no "el servidor MCP falló".
