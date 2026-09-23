# ADR-060: Foreign keys activas en todas las conexiones

**Fecha:** 2026-09-23
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "aunque haya riesgo, convendria activarlas antes de que siga creciendo"
**Relacionado:** ADR-058 (20 huerfanos limpiados a mano), ADR-059 (contenido descompuesto)

---

## Contexto

La DB tenia **6 foreign keys declaradas y 0 activas.**

Causa: `PRAGMA foreign_keys` es **por conexion** en SQLite y viene **apagada por
defecto**. Declarar la FK en el schema no alcanza: hay que activarla en cada conexion, o
el motor la ignora en silencio.

```
session_vectors     session_id  -> sessions_relacional(id)  ON DELETE CASCADE
topic_sessions      session_id  -> sessions_relacional(id)
topic_sessions      topic_id    -> topics(id)
learning_tags       learning_id -> learnings(id)            ON DELETE CASCADE
learning_tags       tag_id      -> tags(id)                 ON DELETE CASCADE
session_entries     session_id  -> sessions_relacional(id)  ON DELETE CASCADE
```

**Consecuencia medida:** los `ON DELETE CASCADE` **nunca dispararon**. Por eso ADR-058
encontro y limpio a mano 20 filas huerfanas (9 en `learnings_enriquecido`, 7 en
`topic_sessions`, 4 en `sessions_relacional`). Sin el pragma, la integridad declarada en
el schema era decorativa.

---

## Correccion de un diagnostico previo

En ADR-058 se dejo anotado: *"no se activo `foreign_keys=1`: 5 lugares usan
`INSERT OR REPLACE`, que es DELETE + INSERT y dispararia CASCADEs"*. **Era una advertencia
demasiado amplia.** Al medir el patron real de cada escritor:

| Script | Patron | Riesgo real |
|---|---|---|
| `memory-catalog.sh` | `INSERT OR REPLACE` con **id=None** | **ninguno**: nunca reemplaza una fila existente |
| `memory-catalog-simple.sh` | idem | ninguno |
| `memory-catalog-v2.py` | `INSERT` con id=None | ninguno |
| `migrate-*.py` | `INSERT OR REPLACE` en tablas **sin hijos** | ninguno |
| `oss-sync.sh` | `INSERT OR REPLACE` en `oss_sync` (sin hijos) | ninguno |

**El riesgo de CASCADE existe cuando hay un `INSERT OR REPLACE` con un `id` explicito que
ya existe**, porque ahi si hay un DELETE previo. Ningun script lo hace. La prueba que
sugeria lo contrario usaba un id explicito que ningun escritor utiliza: era un escenario
construido, no un riesgo real.

Lo que si borra padres:

- `memory-topics.py`: `DELETE FROM topic_sessions` y despues `DELETE FROM topics` - **en
  ese orden**, que es el correcto. De hecho el CASCADE ahora lo respalda en vez de
  depender del orden.
- `migrate-learnings.py`: `DELETE FROM learnings` (migracion one-off, y reinserta). Es la
  unica que podria perder `learning_tags` por CASCADE. **Se documento y no se corre.**

---

## Decision

**Activar las foreign keys en todas las conexiones que escriben**, centralizando la
conexion para que un script nuevo no pueda olvidarlo.

### `scripts/db.py` (nuevo)

```python
from db import connect
conn = connect(DB_PATH)              # FK activas
conn = connect(DB_PATH, readonly=True)
```

En modo **readonly no se activa** el pragma: no se escribe, asi que no puede crear
huerfanos, y activarlo obligaria a tomar un lock de escritura.

Ademas expone `check(path)`, que devuelve las violaciones de FK - util para verificar
despues de escribir.

### Shell

`memory-db.sh` define una funcion `db()` que envuelve la CLI con el pragma, y las **10
invocaciones de escritura** pasan por ella. Antes eran 38 llamadas sueltas a `sqlite3`
donde olvidarlo era cuestion de tiempo.

```bash
db() { sqlite3 -cmd "PRAGMA foreign_keys = ON" "$DB" "$@"; }
```

`oss-sync.sh`, `memory-catalog.sh` y `project-closure.sh` reciben el pragma en sus
conexiones (6, 3 y 1 respectivamente).

---

## Verificacion

Se probo **sobre una copia**, nunca sobre la DB real, con el pragma activo:

| Prueba | Resultado |
|---|---|
| `migrate-entries` con FK activo | 0 violaciones, 521 entries |
| `migrate-content` con FK activo | 0 violaciones, 1987 secciones |
| `migrate-vectors` con FK activo | 0 violaciones, 128 vectores |
| `add-todo` / `add-inbox` / `update-ficha` (flujo real) | escriben, hijos intactos (13/3/7) |
| `PRAGMA foreign_key_check` | **0 violaciones** |
| Suite de tests | 122 pasan |

---

## Consecuencias

### Positivas
- **La integridad del schema pasa a aplicarse.** Una FK declarada que nadie activa es
  documentacion, no una regla.
- **Los CASCADE empiezan a funcionar**: borrar una ficha limpia sus entries, vectors y
  topic_links sola.
- **Un escritor nuevo nace correcto:** `db.connect()` trae el pragma por defecto.
- **Cierra el riesgo de repetir ADR-058:** los 20 huerfanos aparecieron justamente por
  esto. Con el pragma activo, no pueden volver a acumularse.

### Negativas
- **Un `DELETE` sobre un padre ahora borra hijos.** Es lo correcto, pero es un cambio de
  comportamiento: hoy ningun script borra padres en produccion, pero si alguien lo
  agrega, el borrado sera en cascada. Esta documentado.
- **`migrate-learnings.py` queda marcado como peligroso** (borra `learnings` entero). No
  se corre; si hiciera falta, hay que reinsertar los `learning_tags` a mano o envolverlo
  en una transaccion que los preserve.
- **El acceso a la DB gana un punto de entrada obligatorio** (`db.py` / `db()`). Es
  intencional, pero es una convencion que hay que respetar; el pragma sigue siendo por
  conexion, no una propiedad de la DB.

---

## Hallazgo colateral: un script roto desde ADR-058

Verificando los escritores aparecio que **`memory-catalog.sh` estaba roto**: su `INSERT`
referenciaba la columna `agent_id`, que ADR-058 **elimino** por estar siempre vacia.

```
sqlite3.OperationalError: table sessions_relacional has no column named agent_id
```

Y al revisarlo, el mismo bloque tenia **mas valores que placeholders** en el tuple
(heredado de una version anterior del schema). Se corrigieron las dos cosas.

Es el efecto de segundo orden de una migracion de schema: quitar una columna "muerta"
rompe a quien la nombraba. `memory-catalog.sh` no esta en el camino activo (el vigente es
`memory-catalog-v2.py`), pero habria fallado en silencio si alguien lo corria.

---

## Referencias

- ADR-058: la migracion que limpio los 20 huerfanos a mano y dejo la advertencia
  demasiado amplia sobre `INSERT OR REPLACE`
- Leccion: **un `PRAGMA` no es configuracion de la DB, es de la conexion.** Verificar
  `PRAGMA foreign_keys` antes de asumir que la integridad esta activa
