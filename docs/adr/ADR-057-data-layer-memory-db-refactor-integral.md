# ADR-057: El data-layer de memory.db - refactor integral en seis fases (2026-09-22/23)

**Fecha:** 2026-09-22 a 2026-09-23 (unificado 2026-10-19)
**Estado:** Aceptado (implementado y verificado)
**Decisores:** Gonzo / Kanam
**Origen:** pedidos de Gonzo sobre la DB durante la sesión del 22-23/09 ("optimizarla ahora antes de que sea muy tarde", "refactorizar las tablas", "poder agregar muchos campos", "activar las FK aunque haya riesgo", "aplicar las propuestas", "aplicar + vectorizar las secciones")
**Relacionado:** ADR-038 (learnings con mirror en DB), ADR-050 (SQLite local y su umbral), ADR-055 (bloques managed desde settings), ADR-065 (DB-first vs doc-only)
**Absorbe:** los cinco ADRs de esta campaña que eran archivos separados (taxonomía normalizada, contenido descompuesto, FKs activas, campos interpretados, vectores rechunk - antes numerados 058-062, retirados al fusionarse). Las fases de abajo son su contenido íntegro.

---

## Contexto

El 2026-09-22 `memory.db` pesaba 12 MB y crecía ~3.6 MB/mes. La medida (`dbstat`) mostró que el 77% eran **embeddings guardados como JSON de texto** - el defecto no era el contenido sino su representación. Lo que empezó como una optimización de espacio destapó, fase a fase, seis defectos estructurales encadenados del data-layer completo: representación, modelado, indexación del contenido, integridad, campos y búsqueda semántica.

Este ADR cuenta la campaña completa como lo que fue: **una decisión integral con seis fases**, donde cada hallazgo destapó la siguiente.

## Las seis fases (en orden de ejecución)

### Fase 1 - Los embeddings en BLOB float32 (2026-09-22)

**Decisión:** los embeddings se guardan como BLOB float32 little-endian (`struct.pack`), no JSON. Un vector de 1024 dims: ~22.700 chars en JSON vs 4.096 bytes en BLOB.

- Codec compartido `scripts/vector-util.py` (encode/decode idempotente, tolerante al formato viejo) - lo que hizo segura la transición.
- La conversión verifica el invariante antes de escribir: cada BLOB se decodifica y compara con el original.
- float32 y no float64: el modelo emite float32; duplicar la precisión no agrega información.
- Índice `idx_learnings_vector` (3.2 MB, más pesado que su columna) reemplazado por índice parcial `WHERE learning_vector IS NOT NULL`.

**Resultado:** 12 MB → 4 MB (-67%); tasa de crecimiento 5x menor (~0.66 MB/mes).

**Hallazgo colateral que destapó la fase 2:** `PRAGMA foreign_key_check` reveló **20 violaciones de FK preexistentes**.

### Fase 2 - Taxonomía normalizada y FK espuria (2026-09-22)

**Decisión:** tags reales como tokens (`tags` + `learning_tags` normalizados), categorías con eje (`categories.kind`: learning | topic), tabla gemela `learnings_enriquecido` absorbida en `learnings`.

- 0 de 121 "tags" eran JSON válido; 48 eran títulos pegados por un bug. 157 tokens de prosa → descartados; el vocabulario controlado quedó en ~20 tags con 233 vínculos.
- `learnings` gana `learning_vector` (BLOB) y la gemela que duplicaba el 94% del texto se elimina.

**Las 20 violaciones de FK eran tres problemas distintos:**
1. 9 huérfanos de `learnings_enriquecido` con contenido válido → **promovidos** a `learnings`.
2. 7 vínculos colgados de `topic_sessions` → **quitados**.
3. Sessions↔daily_notes: **FK espuria** (0 de 47 vínculos compartían fecha; coherencia de numeración, no relación). Eliminarla desactivó una bomba de tiempo: activar el pragma sin quitarla habría borrado datos sin relación al borrar un padre.

**No se hizo (con motivo):** no se fusionaron daily/sessions (capas cruda vs curada), no se activó el pragma aún (5 escritores usan `INSERT OR REPLACE`), no se borró `learnings.tags` legacy (exige rebuild).

### Fase 3 - Contenido descompuesto en campos consultables (2026-09-22)

**Decisión:** el markdown de dailies/sessions se descompone en metadatos columnados + `sections` con **offsets** (no copia del texto) + `checklist_items` (102 TODOs enterrados rescatados, 67 abiertos).

- **El body no se copia:** guardan `char_start/char_end` y se reconstruye del padre. La primera versión copiaba: la DB pasó de 3.8 a 6.5 MB (95% de texto duplicado) y se revirtió sobre una copia antes de tocar la real. Con offsets: 140 KB.
- Los offsets son estables porque el contenido solo crece por append.
- `type` se recalcula desde el contenido (6 filas mentían); 17 filas BLOB→text corregidas.
- **No se extrajeron entidades** (repos, PRs) por regex: 5143 matches medidos eran sobre todo rutas y fechas. Fabricar datos falsos peor que no extraer.

### Fase 4 - Foreign keys activas en todas las conexiones (2026-09-23)

**Decisión:** `PRAGMA foreign_keys = ON` en toda conexión que escribe, centralizado: `scripts/db.py` (Python) y función `db()` en `memory-db.sh`.

- **Corrección del diagnóstico de la fase 2:** la advertencia sobre `INSERT OR REPLACE` era demasiado amplia. Medido escritor por escritor: el riesgo CASCADE existe solo con `INSERT OR REPLACE` con id explícito existente; ningún escritor lo hace. Verificado sobre copia: 0 violaciones con el pragma activo en las tres migraciones.
- Un escritor nuevo nace correcto: el punto de entrada obligatorio trae el pragma.
- Hallazgo colateral: `memory-catalog.sh` estaba roto desde la fase 2 (referenciaba la columna `agent_id` eliminada). Es el efecto de segundo orden de una migración de esquema.

### Fase 5 - Campos interpretados con revisión, un eje por columna (2026-09-23)

**Decisión:** el intérprete LLM de fichas (`interpret-entries.py`) propone, **el humano aprueba** (`--review`/`--approve`/`--reject`), y solo lo aprobado se aplica (`--apply`).

- **Un eje por columna:** la primera corrida mezcló los ejes determinista (`kind`, del título) e interpretado (`activity`, del LLM) en una columna - las 8 interpretaciones pisaron 408 clasificaciones. Reparación: columnas separadas + restauración. Regla: si dos valores de una columna responden preguntas distintas, son dos columnas.
- **El proyecto debe ser central, no mencionado:** mencionar `soporteml` una vez al resolver un conflicto de git no hace del día un día-de-soporteml. Regla: en el título o ≥2 veces en el cuerpo + debe existir en `projects/`. 1 falso positivo de 8 medidos.
- El error se arregla en la validación (determinista, testeable), no en el prompt (probabilístico).

### Fase 6 - Vectores re-cortados por unidad semántica (2026-09-23)

**Decisión:** los chunks se cortan por las fronteras que ya existen (unidades de nivel 2 de `session_entries`, secciones de la fase 3) con el título adelante; el texto no se guarda, se reconstruye por offsets; un solo módulo (`chunk-util.py`) genera y muestra el cut.

- Antes: ventana ciega de 1500 chars - 29% de chunks cortaban a mitad de frase, 15% eran volcado del harness. La búsqueda devolvía fragmentos sin sentido ("¿qué dije sobre confianza?" traía decisiones de releases).
- Después: 781 vectores de ficha + 2352 de sección; 0 chunks huérfanos; DB de 20.8 → 19.1 MB (la duplicación de `chunk_text` detectada y eliminada: 2.16 MB).
- La duplicación de `split_large` entre scripts se elimina con un test que prohibe redefinirla - mismo error de la fase 5 (dos ejes), cazado antes de producir datos malos.

## Consecuencias (de la campaña)

**Positivas**: DB de 12→19.1 MB con 3133 vectores nuevos (la campaña vectorizó lo que antes no existía; sin la duplicación eliminada hubiera sido 20.8). Integridad real (FKs aplicadas), taxonomía confiable, 1987 secciones consultables, TODOs rescatados, búsqueda semántica que devuelve el tema, vocabulario/esquema explícitos. Cada fase dejó tests (156 al cierre de la fase 6).

**Negativas asumidas**: los offsets exigen recalcular si algo no-append reescribe un `content`; los vectores no son la herramienta principal de la memoria (SQL para lo estructurado, vectores para sinonimia - medido); `learnings.tags` legacy pendiente de extirpar.

**Método (lo repetible):** medir QUÉ pesa antes de optimizar (el 77% no era lo asumido); probar migraciones sobre copia (`--db`); un número reportado que se contradice es artefacto propio hasta verificarlo; las "20 violaciones" eran tres problemas con tres reparaciones distintas - tratarlos como uno destruye datos con la solución "obvia".

## Referencias

- ADR-038: el patrón DB-fuente-de-verdad + markdown espejo que esta campaña extiende al data-layer
- ADR-050: el umbral de migración que sigue vigente (nada de esto lo re-abre)
- ADR-055: los bloques managed, construidos sobre esta DB saneada
- ADR-066: los guards no leen código de proyecto (nacido en este período)
- Review K3 2026-10-18: `docs/records/` - la fusión de estos seis ADRs en uno