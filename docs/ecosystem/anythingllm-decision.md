# AnythingLLM: verificado, sin uso real y descartado

**Fecha:** 2026-10-27
**Estado:** Cerrado. Se elimino todo rastro: contenedor, imagen, repo upstream y las entradas del stack.
**Decisores:** Gonzo ("lo he matado, no le encontré so real... hay que eliminar todo rastro y archivos huerfanos")
**Origen:** Revision de pendientes (2026-10-27), donde se discovered que el directorio de datos ya no existia.
**Relacionado:** `studies/oss-alternatives-triage.md` (tier 3, "no meter Milvus ni AnythingLLM: duplican lo que ya tenes"), `docs/ecosystem/milvus-decision.md` (mismo patron de descarte), `docs/learnings/metodologia.md` (el caso RAG del 2026-10-21)

---

## Contexto

El 2026-10-20 se desplego AnythingLLM en Docker con Ollama como proveedor, y quedo verificado
end-to-end: chat, RAG, embeddings locales (`qwen3-embedding:0.6b`), vector store LanceDB, UI en
`localhost:3001`. Todo funcionaba.

Lo que nunca tuvo fue **uso real**. El unico documento indexado fue un `.md` de prueba de 33
palabras, y de ese seed el RAG expandio un documento de 11 secciones con datos que el modelo se
invento (el caso de kanam-query, learnings de metodologia). Un RAG que infla un seed a un
documento con forma convincente no es una base de conocimiento: es un generador de prosa.

El 2026-10-27, al revisar los pendientes, aparecio el dato: **`~/anythingllm-data` no existia**.
Sin el directorio no habia ni la DB SQLite, ni el vector store, ni los documentos, ni el `.env`
con `SIG_KEY`/`SIG_SALT` (que cifran los datos y sin ellos la base es ilegible), ni el
`docker-compose.yml` (que vivia ahi, no en el repo). El contenedor estaba parado desde el
2026-10-21 (exit 137, SIGKILL) y no podia volver a arrancar: sus bind mounts apuntaban a un host
path inexistente. El `.env.bak.*` que era el unico respaldo tampoco existia.

**El riesgo ya estaba documentado y no se habia aplicado**: el todo de 2026-10-21 pedia un backup
programado de `storage/` + `.env` y advertia textual que *"si se pierde ese directorio, la base
queda ilegible y no hay forma de recuperarla"*. Ese backup nunca se implemento. Cuando los datos
se perdieron, no habia nada que recuperar.

## Decision

**AnythingLLM queda fuera del stack.** Gonzo: *"lo he matado, no le encontre nada real... hay que
eliminar todo rastro y archivos huerfanos"*.

No se resucita: el valor estaba en el RAG sobre documentos reales, y no habia documentos reales.
La capacidad de busqueda semantica del workspace ya estaba cubierta en tres lugares antes de
esta prueba (`scripts/memory-search.py` con SQLite + embeddings, `projects/langchain-starter` con
ChromaDB, `projects/soporteml` con pgvector). AnythingLLM era el cuarto, y el mas fragile: datos
en un bind mount fuera del repo, sin backup, con claves de cifrado en un `.env` que la app
reescribe sola.

## Lo que se elimino

| Que | Donde |
|---|---|
| Contenedor `anythingllm` | Docker (exit 137 desde el 21/10) |
| Imagen `mintplexlabs/anythingllm:latest` | Docker (5,05 GB) |
| Repo upstream `projects/anything-llm` | `trash` (33 MB, sin cambios locales, reversible) |
| Entrada en el catalogo del stack | `scripts/ai-toolbox.py` + test de core tools |
| Ficha en el registro humano | `docs/tools/REGISTRY.md` (tabla regenerada + seccion de prosa) |
| Skill del registro | `skills/ai-toolbox/SKILL.md` (descripcion + IDs validos) |
| Entrada de memoria curada | `MEMORY.md` |
| Dos todos moot (token a cambiar, backup a programar) | `memory.db` (84, 85 -> done) |
| Menciones en contexto operativo | `projects/onyx/.knowledge/STATUS.md` |

**No se toco** (son registros historicos de lo que paso, no estado vivo):

- `docs/learnings/metodologia.md` y la learning 310 en la DB: la leccion es de metodo (un
  documento largo no prueba que alguien lo escribio: hay que verificar el origen), no de la
  herramienta. El caso de kanam-query sigue siendo valido como evidencia.
- `projects/kanam-query/.knowledge/`: alli se documento la procedencia de los datos del analisis.
- `studies/oss-alternatives-triage.md`: la regla "no meter Milvus ni AnythingLLM" es una decision
  de estudio que ya habia excluido la herramienta. Se vuelve mas cierta, no menos.
- `memory/`, `docs/archives/`: diario.

## Lo que queda como learning

**Un servicio parado puede ser un crash o una perdida de datos, y confundirlos hace relanzar un
contenador sin datos.** Cuando el contenedor no arranca, la primera pregunta no es "por que no
arranca" sino "que le pasa a los datos". El exit 137 (SIGKILL) fue la senal: no lo mato nadie a
proposito, se lo comio el OOM killer, y al reiniciar los bind mounts ya no existian. Sin embargo,
lo que se perdio no fue un crash: fue el directorio entero, con la base, el vector store, las
claves de cifrado y el compose.

**El backup que se pide y no se implementa es el backup que falta cuando hace falta.** El todo
del 21/10 no era burocracia: describia el modo exacto de fallo, y el modo de fallo se cumple
exactamente asi cuando no hay backup. La regla que sale: si los datos de un servicio viven fuera
del repo, el backup programado es parte de haberlo desplegado, no una mejora posterior.

**Y el precedente: instalar y verificar no es adoptar.** AnythingLLM funcionaba perfecto
(chat, RAG, embeddings, verificado end-to-end) y aun asi no servia para nada: la unica consulta
real no era una consulta, era una prueba de que el RAG sabia inventar. La verificacion tecnica
mide que la cosa ande; la adopcion se decide por si hay trabajo real que haga.

## Artefactos

- `docs/learnings/metodologia.md` - la leccion de metodo del caso RAG (learning 310).
- `docs/ecosystem/milvus-decision.md` - el precedente de descarte de stack.
- `studies/oss-alternatives-triage.md` - la regla de estudio que ya lo excluia.
