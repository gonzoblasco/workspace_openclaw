# ADR-058: Taxonomia normalizada, tabla gemela absorbida y una FK espuria

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "podemos refactorizar las tablas mismas, crear grupos y categorias y detalles"
**Relacionado:** ADR-057 (embeddings en BLOB), ADR-038 (docs narrativos), ADR-055 (bloques managed)

---

## Contexto

ADR-057 bajo la DB de 12 MB a 4 MB arreglando **como se guardaba el dato**. Este ADR
arregla **como esta modelado**. La auditoria previa encontro cinco defectos.

Un dato primero: **el refactor no es por espacio.** Post-ADR-057 la narrativa
(`sessions_relacional` 27% + `daily_notes` 26%) es el 53%, y esta bien: son dos capas
distintas de la misma sesion (conversacion cruda del harness vs sesion narrativa
curada). Verificado: el mismo id tiene contenido distinto en cada una. Fusionarlas
perderia informacion. Este ADR es por **correccion**, y sale 0.2 MB.

### Los cinco defectos

**1. `tags` no cumplia su contrato.** El schema dice "JSON array".
**0 de 121 filas** eran JSON valido. Peor: **48 eran titulos pegados** por un bug de
carga (`title = "2026-08-01 - Service worker cache strategy"`, `tags = "Service worker
cache strategy"`). De 157 tokens, **123 se usaban una sola vez**: no habia vocabulario
controlado.

**2. Dos conceptos distintos con el mismo nombre.** `learnings.category` es un conjunto
cerrado de 7 valores (`infraestructura`, `metodologia`, `oss`...). `topics.category` es
prosa libre (`"Agentic AI workflows"`, `"LinkedIn branding/marketing"`). Los dos se
llaman `category` y no son lo mismo.

**3. `learnings_enriquecido` duplicaba el 94% del texto.** 112 de 119 filas identicas
byte a byte a `learnings`. Existia solo para colgar el vector.

**4. Veinte violaciones de foreign key** que resultaron ser **tres problemas distintos**
(abajo).

**5. Dos columnas siempre NULL.** `learnings_enriquecido.query_vector` y
`sessions_relacional.agent_id`. No ahorran espacio medible (un NULL cuesta ~1 byte por
fila); son trampas para el proximo que asuma que estan pobladas.

---

## Decision

### 1. Taxonomia normalizada

```sql
tags         (id, name UNIQUE, created_at)
learning_tags(learning_id, tag_id, PK(learning_id,tag_id))
categories   (id, name, kind, description, UNIQUE(name,kind))
```

- **Un tag real es un token**: minuscula inicial, sin espacios, `[a-z0-9._-]`. Lo que no
  cumple eso es prosa y **se descarta** (137 valores). No se pierde nada: la prosa era el
  titulo, que ya vive en `learnings.title`.
- **`categories.kind` distingue los dos ejes** (`'learning'` | `'topic'`). Es la forma
  barata de resolver "dos conceptos con el mismo nombre" sin inventar dos tablas.
- La columna `learnings.tags` **queda como legacy**, sin borrar todavia: sacarla del
  schema exige reconstruir la tabla (mismo costo que el rebuild de la FK) y no urge.

### 2. Tabla gemela absorbida

`learnings` gana la columna `learning_vector` (BLOB, ADR-057) y `learnings_enriquecido`
se elimina. El vector vive en la misma fila que su texto.

### 3. Las 20 violaciones: tres problemas, no uno

| Grupo | Diagnostico | Reparacion |
|---|---|---|
| `learnings_enriquecido.id -> learnings` (9) | FK real, faltan los padres. Los hijos tienen **contenido valido** | **Promover** los 9 (ids 155-169 estaban libres) |
| `topic_sessions.session_id` (7) | FK real. Los 7 apuntan a la sesion 73, que existe en `daily_notes` pero nunca se catalogo | **Quitar** los vinculos colgados |
| `sessions_relacional.id -> daily_notes` (4) | **FK ESPURIA** | **Eliminar la FK** |

**La FK espuria es el hallazgo del ADR.** Verificado: de los 47 vinculos que resuelven,
**0 comparten fecha** con su daily. Sesion 56 dice `2026-08-27`, daily 56 dice
`2026-08-05`; no tienen nada que ver. Los escritores pasan `id=None` a un
`INTEGER PRIMARY KEY` (que es rowid alias) y **las dos secuencias coinciden por
numeracion, no por relacion**. Ningun codigo hace JOIN entre esas tablas.

**Consecuencia de no arreglarlo:** los `ON DELETE CASCADE` del schema **nunca dispararon**
(`PRAGMA foreign_keys = 0`, nadie lo activa). Si se hubiera activado el pragma sin quitar
la FK, borrar la daily 53 habria destruido la sesion 53 (otra cosa) con sus 8 topics y 2
vectores. **La FK era una bomba de tiempo, no una proteccion de integridad.** Primero se
desarma, despues tiene sentido hablar de activar el pragma.

---

## Consecuencias

### Positivas
- **El filtro por tag se volvio confiable.** Antes la mitad de los "tags" eran titulos;
  hoy `tag=oss` devuelve 6, `tag=config` devuelve 9, y un tag inexistente devuelve 0.
- **157 tags en vocabulario controlado** con 233 vinculos, en vez de una columna de texto.
- **La fusion de la gemela quita 124 KB de texto duplicado** y una tabla que habia que
  mantener sincronizada a mano.
- **0 violaciones de FK** (eran 20). Y ya no hay una FK que borre datos sin relacion.
- **La app filtra por tag de verdad** (chips con conteo) porque los datos son confiables.

### Negativas
- **`group_concat` en vez de un campo directo.** Leer los tags de un learning ahora es una
  subquery. Con 233 vinculos es imperceptible; con millones habria que materializar.
- **`learnings.tags` queda como columna muerta con datos viejos.** Documentado; sacarla
  exige rebuild. Riesgo: que alguien la lea y crea que es la fuente. Mitigado con
  comentarios en el codigo que la nombran.
- **El rebuild de `sessions_relacional`** para quitar la FK es una operacion que reescribe
  la tabla. Se hizo con backup y verificando que las 51 filas y los indices sobrevivan.

---

## Alternativas consideradas

1. **Activar `foreign_keys=1` y dejar que los CASCADE limpien.** Habria **borrado datos
   validos** (los 9 hijos con lecciones reales) y, por la FK espuria, sin relacion con lo
   borrado. Rechazado.
2. **Borrar los 20 huerfanos.** Simple, pero 9 tenian contenido que no estaba en ningun
   otro lado. Rechazado por perdida de datos.
3. **Reconstruir los vinculos de las 4 sesiones por fecha.** Tentador, pero el vinculo no
   existia: inventarlo seria fabricar una relacion. Rechazado.
4. **Dos tablas separadas para las categorias** (`learning_categories` y
   `topic_categories`). Mas explicito, pero duplica la estructura; `kind` resuelve lo
   mismo con una tabla.
5. **Mantener la tabla gemela.** Implica seguir sincronizando dos copias del mismo texto a
   mano. Rechazado: es la fuente del 94% de duplicacion.

---

## Nota: que NO se hizo

- **No se fusionaron `daily_notes` y `sessions_relacional`** pese a que juntas son el 53%
  del peso. Son capas distintas (cruda vs curada) y el contenido lo confirma.
- **No se activo `PRAGMA foreign_keys=1`.** Corresponde, pero es un pase propio: 5 lugares
  usan `INSERT OR REPLACE`, que es `DELETE + INSERT` y **dispararia CASCADEs** al
  reemplazar filas. Activar el pragma sin revisar eso cambiaria el comportamiento de
  escrituras existentes.
- **No se elimino `learnings.tags`.** Exige rebuild; documentado como legacy.

---

## Implementacion

| Pieza | Path |
|---|---|
| Migracion | `scripts/migrate-schema.py` (`--dry-run`, `--db`) |
| Tests | `tests/python/test_schema_migration.py` (20) |
| Lectores parcheados | `memory-search.py`, `memory-reembed.py`, `memory-catalog-v2.py`, `memory-catalog.sh`, `memory-db.sh` |
| App | `lib/queries.ts` (`getLearningTags`, subquery de tags), `app/learnings/page.tsx` (chips de tag) |

## Referencias

- ADR-057: la migracion de vectores que hizo visible este trabajo (su verificacion de FK
  fue la que destapo los 20 huerfanos)
- Leccion del metodo: las "20 violaciones" no eran un problema sino tres, y la reparacion
  correcta de cada una era distinta (promover / quitar / eliminar la FK). Tratarlas como
  una sola habria destruido datos con la solucion "obvia" (activar el pragma)
