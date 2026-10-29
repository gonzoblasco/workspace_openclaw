# Milvus: evaluado, funcionando y descartado por exceso de complejidad

**Fecha:** 2026-10-20
**Estado:** Cerrado. La instalacion se borro completa (contenedores, red, imagenes, repos y proyecto).
**Decisores:** Gonzo / Kanam
**Origen:** Peticion de Gonzo ("quiero que me clones milvus, lo configures con Ollama y corras el server para probarlo")
**Relacionado:** `studies/oss-alternatives-triage.md` (tier 3, "escala de Google, no tuya"), ADR-099 (LangChain como capa de ejecucion), ADR-051 (regla de extraer `lib/ai` solo con divergencia real)

---

## Contexto

Gonzo pidio clonar `milvus-io/milvus`, configurarlo con Ollama y correrlo para probarlo.
No venia de una necesidad concreta del producto: era curiosidad tecnica sobre la capa
vectorial.

El workspace ya tenia busqueda semantica funcionando **antes** de este experimento:

| Pieza | Stack | Estado |
|---|---|---|
| `scripts/memory-search.py` | SQLite + `qwen3-embedding` + cosine similarity a mano | andando, con la memoria real del workspace |
| `projects/langchain-starter` | LangChain + ChromaDB local, RAG completo con FastAPI | andando entonces; retirado el 2026-10-28 (repo privado en GitHub) |
| `projects/soporteml` | pgvector (Supabase) | andando |

Ademas, el triage OSS ya habia colocado a Milvus en **tier 3 - no para adaptar**, con el
veredicto textual: *"Vector DB distribuida a escala de millones. Vos tenes pgvector en
OnWheels y SQLite+embeddings en kanam-lab. Escala de Google, no tuya."*

## Lo que se hizo (y funciono)

La integracion se completo y se verifico end-to-end. **El一句话 tecnico que queda:**

Milvus 3.0.3 standalone (modo embebido: etcd + storage local dentro del container) con
**embeddings server-side vía Ollama**. Se usaba el provider `openai` de Milvus contra el
endpoint OpenAI-compatible de Ollama (`/v1/embeddings`), con el modelo del host.

Prueba end-to-end (PASS, dos veces): se insertaba texto crudo, Milvus lo vectorizaba
llamando a Ollama, y el vector guardado era **identico** (diff max `0.000000`) al que
devolvia la llamada directa al host. La busqueda por similitud tambien vectorizaba la
query via Ollama.

Lo que quedo aprendido y verificado (no de memoria, leyendo el codigo de Milvus 3.0.3):

1. **Milvus 3.x no tiene un provider "ollama".** La lista de providers soportados esta en
   `internal/util/function/embedding/text_embedding_function.go` y no lo incluye. El
   provider `openai` si funciona contra Ollama porque ambos hablan el mismo dialecto
   (`POST <url>`, `Authorization: Bearer <key>`, body `{model, input[], encoding_format}`).
2. **La URL del provider sale solo de la config del server**
   (`function.textEmbedding.providers.openai.url`), no de los params de la funcion. Se
   define en `user.yaml`, que Milvus 3.x carga con maxima prioridad
   (`milvus.yaml < _test.yaml < default.yaml < user.yaml`).
3. **Milvus exige API key no vacia** (`MILVUS_OPENAI_API_KEY`), pero Ollama no valida el
   valor: sirve cualquiera.
4. **La clave de cache es `queryNode.cache.memoryLimit`, no `common.cache.memoryLimit`.**
   En el `milvus.yaml` de 3.0.3 la entrada `common.cache.*` no existe y Milvus la ignora
   **en silencio**.
5. **El modo embebido (`ETCD_USE_EMBED=true`) es la diferencia entre funcionar y no.**
   El compose oficial de 3 servicios (etcd + minio + milvus) murio con exit 80 por
   timeouts de etcd: Docker tiene ~7.7 GB asignados de los 24 GB del host y conviven
   12+ containers. El modo embebido bajo el consumo a **124 MB de RAM** y arranco en 20s.
6. **El etcd embebido se corrompe con SIGKILLs.** 42 reinicios dejaron el WAL sucio
   (`0.tmp` de 64 MB a medias) y el server entraba en loop con
   `panic: etcdserver: leader changed`. Fix: borrar `volumes/milvus/etcd` y arrancar de
   nuevo (los datos vectoriales viven en `rdb_data` y no se pierden; las colecciones
   registradas en etcd si).
7. **Ollama no puede correr Milvus como app.** `ollama launch` solo lanza agentes de codigo
   (claude, codex, opencode, hermes, droid, cline, qwen): la lista es cerrada. La doc
   completa de Ollama (247 KB) tiene **0 menciones de "milvus"** y `ollama.com/apps`
   devuelve 404.

## Decision

**Milvus queda fuera del stack. No se adopta, no se integra y no se mantiene.**

Razones, en el orden que pesan:

1. **No resuelve una necesidad real.** El workspace ya tenia busqueda semantica
   funcionando en tres lugares. Milvus no aportaba una capacidad ausente: aportaba la
   misma capacidad con mas ceremonia.
2. **El coste operativo no se justifica.** etcd embebido, WAL que se corrompe, modo
   embebido vs compose, claves de config que se ignoran en silencio: es la superficie
   de una base de datos distribuida, que es exactamente lo que no hace falta hoy.
3. **El precedente ya estaba.** El triage OSS lo habia descartado en tier 3 con un
   veredicto textual. Adoptarlo despues fue re-litigar una decision ya tomada sin
   que haya cambiado nada. El AGENTS.md es explicito: *"El precedente no es un motivo"*
   en el sentido inverso tambien: una dependencia no se adopta por haber estado presente.
4. **La complejidad compite con el producto.** El cuello de botella del viaje a full AI
   no es el vectorstore. Es cerrar un proyecto que un cliente real pueda usar.

Lo que **no** fue el motivo: que fuera dificil de configurar. La integracion con Ollama
funciono a la primera y quedo verificada. El problema nunca fue la puesta en marcha.

## Consecuencias

### Lo que se borro

- Contenedores `milvus-standalone` y `milvus-attu`, red `milvus-ollama_default`.
- Imagenes `milvusdb/milvus:v3.0.3` (2.25 GB), `zilliz/attu:latest` (511 MB),
  `quay.io/coreos/etcd:v3.5.25` (89 MB) y `milvusdb/minio:RELEASE.2024-12-18T13-15-44Z` (233 MB).
- `projects/milvus` (clon shallow del upstream) y `projects/milvus-ollama` (compose + config
  + scripts). Ambos con `trash`, no con `rm`: reversibles desde `~/.Trash`.
- La entrada `milvus` del registro de herramientas (`scripts/ai-toolbox.py`,
  `docs/tools/REGISTRY.md`), porque declaraba un compose que ya no existe y un estado
  ("corriendo") que era falso.

### Lo que se queda

**El aprendizaje tecnico de la integracion**, que es reutilizable y no depende de Milvus:
los 7 puntos de la seccion anterior. En particular, el patron de "Milvus no tiene
provider ollama, pero el provider openai contra `/v1/embeddings` funciona" aplica a
cualquier stack que hable la API OpenAI-compatible.

**El benchmark mental**: con 24 GB de RAM y 12+ containers conviviendo, Docker tiene
~7.7 GB. Cualquier cosa que quiera su propia base de datos distribuida tiene que
justificar ese presupuesto.

### Si vuelve a aparecer

El camino de vuelta no es re-clonar el repo: es
`langchain-starter` + un vectorstore que ya este en el stack. La condicion para
reconsiderar Milvus (o cualquier vectorstore distribuido) es **volumen real** que
haga doler Chroma o SQLite, no la anticipacion de ese volumen.

## Alternativas consideradas

| Alternativa | Estado | Nota |
|---|---|---|
| Quedarse con ChromaDB (`langchain-starter`) | **Retirado** (2026-10-28) | Era la opcion del stack, no ya la vigente: el proyecto salio del disco, el repo privado sigue en GitHub. Con el retiro, el vectorstore del workspace queda en SQLite+embeddings y pgvector. |
| pgvector (Supabase, `soporteml`) | **Activo** | Ya en uso. Postgres con vectores, sin un stack mas. |
| SQLite + cosine a mano (`memory-search.py`) | **Activo** | Lo que usa la memoria del workspace. Sin dependencia. |
| Milvus | **Descartado** | Este documento. |
| pgvector local / Qdrant / Chroma server | No evaluado | Quedan como candidatos si el volumen lo pide. |
