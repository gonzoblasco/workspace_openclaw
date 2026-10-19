# ADR-065: DB-first vs doc-only - que documentos viven en el ciclo de la DB y cuales no

**Fecha:** 2026-09-24
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (hipotesis de Gonzo: "los ADR van en direccion opuesta, de los documentos a la DB"; verificada contra el esquema real de `memory.db`)
**Relacionado:** ADR-050 (memoria en SQLite local), ADR-038 (learnings con mirror en DB), la decisión de memory-wiki (`docs/ecosystem/memory-wiki-capa-analitica.md`)

---

## Contexto

Gonzo pregunto si los ADR eran los unicos documentos que van "en direccion opuesta, de los documentos a la base de datos". La intuicion era real, pero el nombre estaba corrido. Verificado contra el esquema real el 2026-09-24:

- `memory.db` tiene **20 tablas** y **ninguna es de ADR ni de decisiones** (no existe `adr` ni `decision`).
- Los comandos `export-*` de `memory-db.sh` cubren solo dailies, todos, inbox, oss y learnings.
- Los ADR aparecen en la DB unicamente como **texto incidental**: alguien los *nombra* dentro de un daily, una sesion o una leccion (19 menciones en `daily_notes`, 6 en `learnings`), nunca como registro consultable.

El sistema tiene entonces **dos clases de superficie**, y confundirlas manda a buscar en el lugar equivocado o a esperar un export que no existe.

---

## Decision

**Se formaliza la distincion, y los documentos doc-only NO se migran a la DB.**

### 1. DB-first (dentro del ciclo de `memory.db`)

El dato vive en la DB y el markdown es una **vista regenerable**. Si el `.md` y la DB discrepan, **gana la DB**.

| Documento | Tabla | Direccion |
|---|---|---|
| `memory/YYYY-MM-DD.md` (dailies) | `daily_notes` | ambos sentidos (el guardado reconcilia `.md` -> DB; `export-daily` regenera) |
| `memory/todos.md` | `todos` | DB -> MD |
| `memory/inbox.md` | `inbox` | DB -> MD |
| `docs/OSS-TRACKER.md` | `contributions` | DB -> MD |
| `docs/learnings/*.md` | `learnings` | DB -> MD |

### 2. Doc-only (fuera del ciclo)

El archivo **es** la fuente de verdad. No hay tabla, no hay export, no hay reconciliacion. Editarlo mal no se detecta contra nada.

`MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `docs/NORTH.md`, `docs/ROADMAP.md`, `docs/AGENTS-DETALLE.md`, **el corpus de ADRs (`docs/adr/`)** y el resto de `docs/`.

### 3. Regla practica

Antes de buscar un dato, decidir si es DB-first o doc-only:
- **DB-first** -> consultar por la DB (o el `export-*` que la regenera).
- **Doc-only** -> leer el archivo. Si se quiere consulta semantica, el camino es **ingesta explicita** (`openclaw wiki ingest`, decisión de memory-wiki en `docs/ecosystem/`), **nunca** asumir que un `export-*` lo va a regenerar.

> **Nota:** la descripcion operativa de la regla vive en `docs/SETUP.md` (seccion "Regla: DB-first vs doc-only"). Este ADR registra la **decision** y su fundamento; el SETUP es la referencia de uso diario. No duplicar el contenido: si cambia, actualizar SETUP y dejar aca solo el porque.

---

## Consecuencias

### Positivas
- Nadie va a intentar "catalogar los ADR en la DB" creyendo que falta un paso: la respuesta y el motivo quedan registrados.
- Explica por que la auditoria de ADRs se hace leyendo archivos y no consultando la DB.
- Da el fundamento de por que el wiki (decisión en `docs/ecosystem/`) es el camino para consultar los ADR: no es una capa decorativa, es el unico puente hacia consulta semantica para un corpus doc-only.

### Negativas
- Los documentos doc-only dependen de disciplina manual: no hay un chequeo automatico que detecte si un doc narrativo quedo desactualizado contra la realidad. Es justamente lo que la capa de claims del wiki puede cubrir si se ingestan (aunque su deteccion hoy es opt-in por ingesta, no automatica).

### Lo que queda fuera del alcance
- **No** se propone migrar los docs narrativos a la DB. El analisis de ADR-050 (SQLite local, umbral de migracion) sigue vigente y nada de esto lo cambia.
- **No** se propone indexar `memory/` ni `docs/entrevistas/` en el wiki: contienen datos personales (ver politica de ingesta en `docs/ecosystem/memory-wiki-capa-analitica.md`).

---

## Alternativas consideradas

1. **Migrar los ADR y docs narrativos a la DB** (darles tabla propia). Rechazada: perderian su naturaleza de documento (legibilidad, diff, revision humana) y ganarian poco. Los docs narrativos se leen como narrativa; meterlos en SQLite es un error ya registrado en `docs/learnings/infraestructura.md`.
2. **Dejar la distincion implicita** (no documentarla). Es el statu quo que produjo la pregunta: la distincion se reconstruyo a mano. Rechazada.
3. **Un solo mecanismo de consulta para todo** (indexar todo en memory-core). Rechazada por ahora: mete datos personales en un corpus de busqueda sin decision explicita.
