# BRIEF - Kanam Story Bible

**Fecha:** 2026-09-24
**Repo:** gonzoblasco/kanam-story-bible (privado)
**Spec de origen:** `SPEC.md` (generada con kanam-spec, revisada y corregida en `.knowledge/DECISIONES.md`)

## What

Servicio autoalojado que guarda la **fuente de verdad** del mundo narrativo: fichas tipadas (personaje, lugar, lore, faccion, item, evento, criatura, concepto), relaciones explicitas entre ellas, outline y bloques base. Expone retrieval RAG con citas y generacion asistida que **propone** pero nunca escribe el canon sola.

## Why

El autor de ficcion (Gonzo) necesita que la IA escriba con los hechos del mundo, no con una version inventada. Kanam Story Bible es el consumidor-agnostico contrato de esa verdad: una app de prosa (Kanam Writer, Kanam Story) consulta el mundo por RAG y cita de que ficha salio cada dato.

**Primer consumidor real: el cliente de prueba `scripts/smoke.py`.** No se congela el contrato contra un producto que no existe.

## Stack

- Python 3.12 + FastAPI + Pydantic
- SQLAlchemy 2.0 + PostgreSQL 16 + pgvector
- Redis + arq (cola de trabajos)
- Ollama (LLM y embeddings locales, contrato compatible OpenAI)
- Docker Compose (Colima en macOS)
- ruff + mypy + pytest

## Status

- [x] Discovery
- [x] Definition
- [x] **In Development** - v1 vertical completo end-to-end
- [ ] Live
- [ ] Archived

## Alcance de v1 (verificado con 64 aserciones)

Proyecto + bloque base, fichas tipadas con validacion de atributos por tipo, relaciones con vocabulario controlado, outline con deteccion de ciclos y referencias huerfanas, indice con outbox transaccional, retrieval hibrido con citas, generacion asincrona con apply explicito, gaps, export JSON/Markdown, borrado en dos fases.

**Fuera de v1:** UI web, worker arq corriendo en background, autenticacion real (hoy `auth_mode=none`), multiusuario.

## Decisiones clave

- **El contrato HTTP es el producto.** La superficie publica va en INGLES (ingles en el wire), el dominio en espanol. El mapeo vive solo en `serializers.py`.
- **`braindump_private` no es un tipo de bloque.** Viaja como campo propio en la API y se persiste dentro del bloque `braindump` en `contenido.privado`. Un bloque por tipo, como manda la spec.
- **Consistencia eventual honesta.** Si el outbox tiene pendientes, `/retrieve` devuelve 409 (la spec pedia un `index_stale`; se implemento como conflicto explicito, nunca como resultado viejo silencioso).
- **Reintento unico por truncamiento.** Si `finish_reason == "length"` el reintento va con mas presupuesto y una instruccion de brevedad. Es la deuda tecnica de la spec, no un bug.
- **Sin Docker Desktop.** Colima en el Mini (4 CPU / 8 GB). `~/.docker/config.json` perdio `credsStore: desktop`.
- **`nomic-embed-text` (768 dims)** como modelo de embeddings de v1, ya presente en la maquina.

## Deuda tecnica registrada

- El worker arq no corre como proceso: el outbox se drena con `/index/drain` (dev) o dentro de `reindex`.
- Sin UI: se opera por HTTP.
- `chunk.embedding` es `vector(768)` fijo: cambiar de modelo de embeddings exige migracion de la columna.
- Sin particionado de `audit_log` ni retencion automatica (la spec lo pide a partir de 5M filas).
- Sin tests de contrato versionados (JSON Schema) para el paquete de export.
