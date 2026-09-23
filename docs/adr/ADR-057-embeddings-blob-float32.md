# ADR-057: Embeddings en BLOB float32, no JSON de texto

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "la base de datos sigue creciendo a pasos gigantescos, optimizarla ahora antes de que sea muy tarde"
**Relacionado:** ADR-050 (memoria en SQLite), ADR-044 (embedding model), ADR-054 (kanam-os)

---

## Contexto

Medicion antes de tocar nada (`dbstat`, 2026-09-22): **memory.db pesaba 12 MB y el 77% eran
embeddings guardados como JSON de texto.**

| Objeto | Peso | % |
|---|---|---|
| `session_vectors` | 3.3 MB | 26.9% |
| `learnings_enriquecido` | 3.2 MB | 26.1% |
| `idx_learnings_vector` | 3.2 MB | 25.7% |
| todo lo demas (texto, narrativa) | 2.5 MB | 21.3% |

Un vector de 1024 dimensiones como JSON ocupa **~22.700 caracteres**; como float32 son **4096
bytes**. Ratio real medido: **0.18** (82% de ahorro).

La tasa importaba mas que el numero: con ~60 sesiones y ~168 vectores nuevos por mes, el JSON
crecia a **~3.6 MB/mes**. En un ano, +43 MB de puro texto redundante. En BLOB, ~0.66 MB/mes.

Y habia un segundo desperdicio independiente: **`idx_learnings_vector` pesaba 3.2 MB, mas que
la propia columna que indexaba.** Indexaba el texto completo del vector. Su unico uso real era
responder "que filas tienen vector" (`WHERE learning_vector IS NOT NULL`) - y para eso el
**valor** no hace falta, solo la existencia.

---

## Decision

**Los embeddings se guardan como BLOB float32 little-endian (`struct.pack("<%df")`), no como
JSON de texto.**

1. `session_vectors.query_vector` y `learnings_enriquecido.learning_vector` pasan a BLOB.
   El DDL de `memory-catalog-v2.py` tambien, para que las DB nuevas nazcan en el formato nuevo.
2. Se elimina `idx_learnings_vector` y se reemplaza por `idx_learnings_vec_present`, un indice
   parcial sobre `id WHERE learning_vector IS NOT NULL`: responde la misma pregunta pesando KB.
3. **El decoder compartido (`scripts/vector-util.py`) acepta AMBOS formatos.** Es lo que hace
   segura la migracion: los scripts siguen leyendo vectores viejos durante la transicion, y
   los escritores nuevos emiten BLOB. Un `encode` idempotente + un `decode` tolerante.
4. **La conversion verifica el invariante antes de escribir**: cada BLOB se decodifica y se
   compara con el vector original; si no coincide, esa fila no se escribe.

Float32 y no float64: el embedding viene de un modelo que emite float32, guardarlo en float64
duplicaria el tamano sin agregar informacion. Little-endian porque es el formato nativo de
`sqlite-vec` y del stack, si algun dia se migra a busqueda vectorial nativa.

---

## Consecuencias

### Positivas
- **12 MB -> 4 MB (-67%).** Con los mismos datos y los mismos resultados de busqueda
  (verificado: `"em dash guion"` devuelve 57.5% y 52.0%, identicos antes y despues).
- **La tasa de crecimiento baja 5x:** de ~3.6 MB/mes a ~0.66 MB/mes en vectores.
- **Un indice que pesaba mas que su columna deja de existir.** 3.2 MB recuperados sin perder
  ninguna capacidad: la pregunta que respondia se responde igual con un indice parcial.
- **El formato queda explicitado.** Antes el JSON era un detalle implicito del que dependian
  4 scripts por `json.loads` suelto; ahora hay un solo modulo con `encode`/`decode` y contrato claro.

### Negativas
- **La columna deja de ser legible a ojo en un `sqlite3` de terminal.** Un `SELECT` devuelve
  binario. Aceptado: para inspeccionar hay `vector-util.py` y el tamano se paga solo.
- **`struct` acopla el formato a little-endian.** Documentado en el codigo; es la convencion
  del ecosistema.
- **Ambiguedad teorica:** un byte-string arbitrario cuyo largo sea multiplo de 4 decodifica a
  float32. En esta DB la columna contiene una de las dos cosas (JSON legacy o BLOB), garantizado
  por la migracion. Si alguna vez pudiera contener otra cosa, haria falta una columna `format`.
  Documentado en `vector-util.py`, no escondido.

---

## Alternativas consideradas

1. **Comprimir el JSON con zlib.** Menos predecible (depende de la entropia), y sigue siendo
   texto que hay que parsear en cada lectura. Un float32 es la representacion directa.
2. **Migrar a `sqlite-vec` (extension nativa).** El destino correcto si la busqueda vectorial
   crece, pero es una dependencia nueva que cambia como se consulta. El BLOB es un paso en esa
   direccion sin adoptarla todavia.
3. **Borrar los vectores viejos y re-embedddear todo.** Mas simple, pero gasta llamadas al
   modelo y no es reversible si el modelo cambio. La conversion preserva los bytes exactos.
4. **Guardar float16.** La mitad de espacio, pero pierde precision en un dato que se usa para
   comparar similitudes. No vale el riesgo por 1.5 MB.

---

## Hallazgo colateral: 20 violaciones de foreign key

La verificacion de la migracion (`PRAGMA foreign_key_check`) destapo **20 violaciones
preexistentes**, que no son un efecto de este cambio:

| Tabla | Huerfanos |
|---|---|
| `learnings_enriquecido` -> `learnings` | 9 |
| `topic_sessions` -> `sessions_relacional` | 7 |
| `sessions_relacional` -> `daily_notes` | 4 |

**Causa raiz: `PRAGMA foreign_keys = 0`.** Los `ON DELETE CASCADE` declarados en el schema
**nunca dispararon**. Ningun script lo activa (verificado con `grep`). Cuando se borro una
sesion, sus topic_sessions y vectores quedaron huerfanos.

No se corrigio en este ADR: limpiar los huerfanos es una decision aparte (borrar vs
reconstruir el vinculo), y activar `foreign_keys=1` de golpe haria que los borrados empiecen a
cascadear sobre datos existentes. **Queda registrado como deuda con evidencia.**

---

## Implementacion

| Pieza | Path |
|---|---|
| Codec compartido | `scripts/vector-util.py` (`encode`, `decode`, `is_json`, `dims`, `cosine`) |
| Migracion | `scripts/migrate-vectors.py` (`--dry-run`, `--db`, `--drop-dead-columns`) |
| Tests | `tests/python/test_vector_migration.py` (16) |
| Lectores parcheados | `memory-search.py`, `memory-topics.py`, `memory-reembed.py`, `memory-catalog-v2.py` |

## Referencias

- Medicion reproducible: `SELECT name, sum(pgsize) FROM dbstat GROUP BY name`
- Leccion de la clase de bug: antes de optimizar hay que medir QUE pesa; el 77% no era la
  narrativa (lo que uno supone) sino la representacion de 264 vectores
