# ADR-059: Contenido markdown descompuesto en campos consultables

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "todo el contenido es markdown o json, estaria bueno poder agregar muchos campos refactorizando el contenido"
**Relacionado:** ADR-058 (taxonomia normalizada), ADR-057 (vectores en BLOB), ADR-029 (memoria en SQLite)

---

## Contexto

Todo el contenido de la DB es **markdown guardado en un solo campo de texto**
(`daily_notes.content`, `sessions_relacional.content_bare`). Las columnas de esas tablas
son pocas y de tipo fijo; la estructura real del documento vive **dentro del texto**.

Antes de tocar nada se midio que se puede extraer de 165 documentos, **y con que
fiabilidad**:

| Patron | Docs | Fiabilidad |
|---|---|---|
| Prefijo `# Session:` (dump del harness) | 65 | **100%** |
| `Session Key` / `Session ID` / `Source` | 65 | **100% parseable** |
| Headings `##` y `###` | 106 | 1987 secciones |
| Checkboxes `- [ ]` / `- [x]` | 11 | 102 items (67 abiertos) |
| Rango horario `(HH:MM - HH:MM)` | 37 | 152 secciones |
| **Entidades `owner/name`** | 126 | **ruido** (ver abajo) |
| **Refs `#NNNN`** | 59 | **ruido en prosa** |

**Los tres defectos reales que esto destapo:**

**1. `type` mentia en 6 filas.** Seis dumps del harness estaban marcados `type='daily'`.
La columna `type` no reflejaba el contenido; la app filtra por `type='daily'` y contaba
esos dumps como dailies.

**2. 17 filas con `content` guardado como BLOB.** No corrompidas (eran UTF-8 valido),
pero con el tipo de dato equivocado: cualquier lectura que asuma `str` falla. Detectado
porque un regex tiro `cannot use a string pattern on a bytes-like object`.

**3. 67 TODOs abiertos enterrados en prosa.** Los checkboxes `- [ ]` viven dentro del
markdown y **nunca llegaron a la tabla `todos`**. Preguntar "que esta pendiente" se perdia
67 items.

### Lo que NO se puede extraer (y por que)

Medido: de **5143 matches** de `owner/name`, los mas frecuentes son `dist/stacks`,
`memory/archive`, `origin/main`, `28/08`. **Son rutas de archivo y fechas, no repos.**
De 1217 matches de `#NNNN`, el contexto es prosa (`"N. #N y #N esperan review"`).

**Regex sobre prosa libre fabrica datos falsos.** No se extraen entidades.

---

## Decision

**Descomponer el contenido en tres piezas, cada una respaldada por una medicion de
fiabilidad del 100%.**

### 1. Metadatos del documento -> columnas

```sql
daily_notes += doc_kind TEXT,      -- 'harness' | 'daily'
               session_key TEXT,   -- de los dumps del harness
               session_id TEXT,
               source TEXT         -- webchat | gateway:sessions.reset
```

Y **`type` se recalcula desde el contenido**, que es la fuente de verdad: 6 filas
corregidas. La distincion fina entre un daily narrativo y un cierre de sesion **no** va
a un tipo: los dos son el mismo documento (`memory/YYYY-MM-DD.md`) y esa diferencia vive
en las secciones.

### 2. `sections` -> headings con **offsets**, no copia del texto

```sql
sections (id, doc_type, doc_id, ordinal, level, title,
          char_start, char_end, time_start, time_end)
```

**Decision central: el body no se copia.** Se guardan dos offsets hacia el `content` del
padre y el cuerpo se reconstruye con `content[char_start:char_end]`.

Por que: **la primera version copiaba el body y la DB paso de 3.8 a 6.5 MB.** El texto
copiado pesaba 1948 KB = **95% del contenido ya presente en el padre**. Era exactamente el
defecto que ADR-058 acababa de eliminar (una tabla que duplica el texto del padre). Con
offsets, `sections` pesa **140 KB** y la DB queda en 4.2 MB.

Por que los offsets no se invalidan: el contenido de un documento **solo crece por
append** (`memory-end-session.py` hace `content + block`). Los `char_start` no se mueven.
Matiz documentado: el `char_end` de la **ultima** seccion si avanza, porque absorbe lo que
se agregue antes del proximo heading.

`doc_type` es `'daily' | 'session'` = **la tabla** de origen, no el tipo de documento:
**47 ids colisionan** entre `daily_notes` y `sessions_relacional`, asi que sin esa columna
las secciones se pisarian.

### 3. `checklist_items` -> los TODOs que estaban enterrados

```sql
checklist_items (id, doc_type, doc_id, ordinal, section, text, done)
```

Conserva `section` (el heading al que pertenecia) y el documento de origen: un TODO
suena distinto segun de donde salio.

### Nota de metodo: dos veces corrijo el rumbo

1. **"108 mismatches en `type` (95%)"** fue un numero que reporte y **estaba mal**: era
   artefacto de mi propia regex de clasificacion, no un defecto de los datos. Con la
   definicion correcta eran **6**. Se corrigio antes de actuar.
2. **La copia del body** se detecto midiendo el resultado sobre una **copia**, no sobre la
   DB real (`--db`). Si hubiera migrado directo, la DB pasaba a 6.5 MB.

---

## Consecuencias

### Positivas
- **1987 secciones consultables** por titulo, nivel y rango horario. "Que sesiones
  hablaron de X" pasa a ser un `SELECT` sobre `sections.title`.
- **102 items de checklist rescatados** (67 abiertos) que no aparecian en ningun listado.
- **`type` deja de mentir**: 6 filas corregidas; el tipo sale del contenido, no de una
  anotacion manual.
- **17 filas con BLOB corregidas a text.** Un defecto de tipo que habria roto cualquier
  lector nuevo.
- **El texto no se duplica.** `sections` pesa 140 KB en vez de 2476 KB.

### Negativas
- **Los offsets son fragiles a ediciones que no sean append.** Si una migracion futura
  reescribe un `content` (un reemplazo, un saneamiento), hay que **recalcular las
  secciones de ese documento**. No es auto-reparatorio.
- **Leer el cuerpo de una seccion exige una segunda query** (o un JOIN a mano). Es el
  precio de no duplicar.
- **La DB crecio 0.4 MB** (3.8 -> 4.2): el indice de titulos (`idx_sections_title`, 96 KB)
  y las columnas de metadatos. Es el costo de poder consultar lo que antes era texto.

---

## Alternativas consideradas

1. **Copiar el `body` en cada seccion.** Simple de leer, pero **medido: +2476 KB (95% del
   texto duplicado)**. Rechazado: es el defecto de ADR-058.
2. **Extraer entidades (repos, PRs) con regex.** Medido: la mayoria de los matches son
   rutas de archivo y fechas. Rechazado: fabrica datos falsos. Las referencias
   estructuradas van en `contributions`, donde el dato es regular.
3. **Partir cada documento en filas separadas** (un documento = N filas). Romperia la
   lectura actual del `content` completo y la busqueda semantica por chunk.
4. **Un formato estructurado (JSON/YAML) en vez de markdown.** Cambia la fuente de verdad
   y todo el pipeline de escritura. El markdown es la superficie de trabajo de Gonzo; el
   objetivo era consultarlo, no reemplazarlo.

---

## Nota: que NO se hizo

- **No se expuso en la UI todavia.** `sections` y `checklist_items` son consultables pero
  ninguna vista los muestra. Candidato natural: los 67 items abiertos junto a `/todos`.
- **No se extrajeron entidades** del texto libre (ver arriba).
- **No se cambio el formato de escritura.** El markdown sigue siendo la fuente; las tablas
  nuevas son un indice derivado que hay que regenerar cuando un documento cambie.

---

## Implementacion

| Pieza | Path |
|---|---|
| Parser (doc_kind, harness_fields, split_sections, extract_checklist) | `scripts/content-parse.py` |
| Migracion | `scripts/migrate-content.py` (`--dry-run`, `--db`) |
| Tests | `tests/python/test_content_migration.py` (30) |

## Referencias

- ADR-058: introdujo el patron "no dupliques el texto del padre". Este ADR lo aplico a si
  mismo al detectar que su primera version lo violaba
- Leccion de metodo: medir el resultado **sobre una copia** fue lo que evito duplicar 2.5 MB
  en la DB real
