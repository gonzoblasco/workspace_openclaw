# Onyx: verificado end-to-end, sin trabajo real, y descartado

**Fecha:** 2026-10-27
**Estado:** Cerrado. La instalacion se borro completa (contenedores, red, volumenes, imagenes, repo clonado y script propio).
**Decisores:** Gonzo / Kanam
**Origen:** Revision de pendientes (2026-10-27), cuando Gonzo pidio la lista de herramientas del stack y sospecho que Onyx ya estaba descartado. La auditoria mostro otra cosa: no estaba descartado, estaba **apagado sin decision** y habia vuelto solo.
**Relacionado:** ADR-103 (LiteLLM se descarta), `docs/ecosystem/milvus-decision.md` y `docs/ecosystem/anythingllm-decision.md` (mismo patron de descarte), `studies/oss-alternatives-triage.md` (tier 2, "Onyx es *enterprise search*, no un buscador web"), `docs/learnings/infraestructura.md` (modo Lite por presupuesto de RAM)

---

## Contexto

El 2026-10-20 se desplego Onyx (`onyx-dot-app/onyx`, OSS, MIT) en Docker con Ollama del host como
provider, en **modo Lite** (6 servicios, ~1 GB RAM: api_server, web_server, nginx, relational_db,
mcp_server, code-interpreter; sin OpenSearch, sin Redis, sin model servers). Se escribio
Se escribio un script propio de Onyx (status/up/down/restart/logs/provider/chat) con su suite de
14 tests, y todo quedo verificado end-to-end: registro de admin, permisos, chat con 3 modelos
cloud distintos, embeddings por `/v1/embeddings` con `qwen3-embedding:0.6b` (dim 1024), UI
server-rendered 200.

Al final de esa sesion el server quedo **cerrado** ("con los volumenes conservados"), y el repo
pregunto pendiente era activar indexacion/RAG.

### Lo que la auditoria del 2026-10-27 revelo

Onyx no estaba descartado: estaba **apagado sin decision**, y habia vuelto solo.

```
vane              2026-10-26T12:39:40.678Z
opencode          2026-10-26T12:39:40.528Z
openhands-canvas  2026-10-26T12:39:40.819Z
onyx-nginx-1      2026-10-26T12:39:41.068Z   <-- mismo segundo
```

Los cuatro arrancaron juntos: eso fue un **reinicio de Docker Desktop**, no una decision. Los seis
servicios de Onyx tienen `restart: unless-stopped`, y esa politica ignora un `docker compose stop`
manual: el reinicio del daemon re-aplica `unless-stopped` y levanta el stack entero. `stop` no
desactiva la politica; `down` si.

### Uso real medido (no "healthy")

| Señal | Valor |
|---|---|
| Documentos indexados | **0** |
| Sesiones de chat | 8 (33 mensajes, de la propia sesion de instalacion) |
| Requests al API server (24 h) | **0** |
| Requests al nginx (7 dias) | 1740, de los cuales **todos** `/api/health` (sonda del toolbox) |
| Volumenes | 77 MB (db 66 MB, logs 11 MB, file-system vacio) |
| RAM del stack | ~1 GB de los 8 GB asignados a Docker Desktop |

Cero uso real. Un stack de 1 GB ocupando Docker Desktop, con un `api_server` que ya se había
dejado OOM-kear una vez (exit 137) por la competencia de RAM con los containers ajenos.

## Decision

**Onyx queda fuera del stack.** Se borra la instalacion completa.

El criterio no es "funcionaba bien" - funcionaba bien, verificado end-to-end. El criterio es
**si hubo trabajo real**, y no lo hubo: cero documentos indexados, cero consultas. La capacidad de
RAG/contexto ya estaba cubierta en tres lugares del stack propio **antes** de este experimento:

| Pieza | Stack | Estado |
|---|---|---|
| `scripts/memory-search.py` | SQLite + embeddings + cosine similarity | andando, con la memoria real del workspace |
| `projects/langchain-starter` | LangChain + ChromaDB | andando entonces; retirado el 2026-10-28 |
| `projects/soporteml` | pgvector | andando |

Onyx era un cuarto motor de lo mismo, el mas caro en RAM y el mas fragile en datos (Postgres
en un volumen nombrado, credenciales en un `.local/credentials.md` fuera del repo).

Ademas, el todo que lo mantenia vivo era **incompatible con el resto del stack**: activar RAG
exigia el stack completo (Redis + OpenSearch con heap de 2 GB + 2 model servers con torch), y
Docker Desktop tiene 8 GB asignados de 24 GB de host. El todo pedia subir el limite de RAM; la
decision no lo justifica.

## Lo que se elimino

| Que | Donde |
|---|---|
| 6 contenedores + red `onyx_default` | Docker (`docker compose down`) |
| 4 volumenes (`onyx_db_volume`, `onyx_api_server_logs`, `onyx_mcp_server_logs`, `onyx_file-system`) | Docker (77 MB) |
| 4 imagenes (`onyx-backend`, `onyx-web-server`, `code-interpreter`, `python-executor-sci`) | Docker (~5,7 GB) |
| Repo clonado `projects/onyx` (138 MB) | papelera (`trash`), recuperable |
| Script propio de Onyx (status/up/down/restart/logs/provider/chat) + su suite de 14 tests | papelera (`trash`), recuperable |
| Entrada en el catalogo vivo (`scripts/ai-toolbox.py`) + prosa de `docs/tools/REGISTRY.md` | edicion |
| Todo #82 (activar RAG) | cerrado como sin objeto, con la razon |

Puerto 3000 liberado. La sonda HTTP `/api/health` que usaba el toolbox tambien.

## Lo que NO se toco (registro historico)

- **El daily del 2026-10-20** y `docs/archives/sesiones/2026-10-20.md`: describen la sesion de
  instalacion. Corregir el pasado seria mentir sobre lo que se verifico.
- **Las learnings** de `docs/learnings/` que citan Onyx como caso (docker, evaluacion,
  infraestructura, metodologia): el objeto de esas lecciones es el **metodo**, no la
  herramienta. El caso sigue siendo evidencia valida.
- **`docs/adr/ADR-103-litellm-se-descarta.md`**: su mencion de Onyx es historica y correcta
  (LiteLLM se descarto porque Onyx era su unico consumidor potencial).
- **`studies/oss-alternatives-triage.md`**: es un analisis fechado de la lista viral; su entrada
  de Onyx es la evaluacion de ese momento.

## Los aprendizajes

1. **Instalar y verificar no es adoptar.** Una herramienta verificada end-to-end y sin
   consultas reales es una copia mas de una capacidad ya cubierta. El trabajo real es el
   criterio, no la calidad tecnica.
2. **`stop` no desactiva la politica de restart.** Un stack con `restart: unless-stopped` vuelve
   solo en el proximo reinicio del daemon. Para que NO vuelva, hay que hacer `down` (o cambiar
   la politica). La firma del diagnostico: **varios stacks arrancando en el mismo segundo**.
3. **"Apagado" y "descartado" son clases distintas.** Un descarte tiene documento de decision y
   limpieza; un apagado sin documento es la clase que el owner tiene que decidir. Confundirlas
   hace que una herramienta viva por inercia parezca resuelta.
4. **El stack que solo responde health checks esta ocupando RAM sin usarse.** El estado "healthy"
   no es uso: hay que filtrar las sondas del trafico real.

## Related

- `docs/ecosystem/anythingllm-decision.md` - mismo patron: verificado, sin trabajo real, y el
  path de datos que desaparecio.
- `docs/ecosystem/milvus-decision.md` - el descarte por complejidad, con el criterio de "que
  capacidad queda cubierta".
- ADR-103 - el descarte de LiteLLM, cuya premisa era que Onyx lo necesitaba.
