# ADR-108: El índice vectorial sale de `memory.db` - dato crudo versionado, embeddings locales

**Fecha:** 2026-11-04
**Estado:** Aceptado (diseño aprobado por Gonzo; implementación en curso)
**Decisores:** Gonzo (caso D, 2026-11-04: *"y si movemos lo pesado de los vectores a otra base de datos que se ejecute aquí mientras seguimos como siempre incluyendo la base de datos común en el repo? al fin y al cabo lo vectorizado es para uso nuestro... pero el dato crudo (el inicial) quedaría versionado como hasta ahora"*) / Kanam
**Origen:** `memory.db` llegó a 25,3 MB y el repo a 1,19 GB. ADR-054 mantiene la DB versionada como respaldo; el peso del índice hace que ese respaldo crezca todos los días.
**Relacionado:** ADR-050 (SQLite local y su umbral), ADR-054 (la DB se queda en git), ADR-057 (data-layer y la campaña de embeddings), ADR-065 (DB-first vs doc-only), ADR-085 (una sola máquina)
**No supersede:** ninguna. ADR-054 sigue vigente: la fuente de verdad permanece versionada.

---

## Contexto

`memory.db` pesa 25,3 MB. El desglose por tabla (`dbstat`, verificado 2026-11-04) separa dos
naturalezas distintas:

| Componente | Tamaño | ¿Reconstruible? |
|---|---|---|
| `section_vectors` (2.352 filas) | 10,3 MB | **Sí** - desde `sections` |
| `session_vectors` (943 filas) | 5,2 MB | **Sí** - desde `sessions_relacional` |
| `sessions_relacional` | 2,2 MB | No |
| `daily_notes` | 1,9 MB | No |
| `learnings` | 1,5 MB | No |
| resto (todos, tags, contributions, sections...) | ~0,5 MB | No |

**El 61% de la DB es un índice derivado.** El dato crudo son 6,3 MB.

### Por qué el formato ya no es la palanca

ADR-057 (fase 1, 2026-09-22) resolvió este problema una vez: el 77% de la DB eran embeddings
guardados como JSON de texto, y el pasaje a BLOB float32 bajó 12 MB a 4 MB. Ese arreglo trató la
**representación**. El índice volvió a 15,5 MB porque el **contenido** creció: cada sesión agrega
secciones y cada sección se vectoriza.

Un `VACUUM` o un cambio de codec atacan el síntoma. El problema es que el índice vive en el mismo
archivo que la fuente de verdad, y por lo tanto el respaldo versionado pesa todo lo que pesa el
índice.

### El precedente interno

ADR-050 ya registra que el sistema separa por naturaleza: `memory.db` es la memoria personal y
`openclaw-agent.sqlite` (577 MB) es el estado del agente, **en archivos distintos**, con el argumento
de que "separar las dos es deliberado y sano".

Este ADR aplica ese mismo patrón a la parte que quedó mezclada: el índice de búsqueda.

## Decisión

**Separar el índice vectorial de la fuente de verdad, en dos archivos SQLite.**

| Archivo | Contenido | Git | Tamaño |
|---|---|---|---|
| `memory/memory.db` | dato crudo: secciones, dailies, learnings, tags, todos, inbox, contributions | **versionado** (sin cambios) | 6,3 MB |
| `memory/vectors.db` | `section_vectors`, `session_vectors` | **no versionado** (`.gitignore`) | 19 MB |

**Los hechos siguen versionados. El índice se instala.** Es la misma relación que hay entre el
código y `node_modules`: lo que no se puede reconstruir va en git; lo que se puede regenerar, no.

### Por qué no se borran los vectores

Borrar el índice local dejaría `memory_search` sin resultados hasta que corra `memory-reembed.py`.
La búsqueda semántica es una función en uso diario, no un adorno. Los vectores **se mueven**, no se
recalculan: se copian tal cual a `vectors.db` y se verifican por conteo antes de borrar el original.

`scripts/memory-reembed.py` queda como la vía de reconstrucción si `vectors.db` se pierde o corrupto
(usa `qwen3-embedding:0.6b`, 1024 dims, y re-embebe todo vector cuya dimensión no coincida con el
modelo actual).

### Implementación: `ATTACH`

Los seis scripts que tocan vectores abren hoy la DB como archivo único:
`memory-catalog-v2.py`, `memory-reembed.py`, `memory-search.py`, `memory-topics.py`,
`migrate-vectors.py`, `rechunk-vectors.py`. Ninguno usa `ATTACH`.

La conexión pasa a:

```sql
ATTACH DATABASE 'memory/vectors.db' AS idx;
```

y las lecturas y escrituras de vectores usan el prefijo `idx.` (`idx.section_vectors`). Es un cambio
mecánico y acotado: las tablas de vectores conservan su esquema, con el `section_id`/`session_id`
apuntando a las filas de `main`.

### Las FK entre archivos se quitan (medido 2026-11-04)

`section_vectors` y `session_vectors` declaran `FOREIGN KEY` hacia `sections` y
`sessions_relacional`, que viven en `main`. **Con dos archivos esa FK no se puede cumplir, y con
`PRAGMA foreign_keys = ON` no falla en silencio: rompe operaciones que no la involucran.**

Medido:

| `foreign_keys` | `DELETE FROM idx.session_vectors` |
|---|---|
| OFF | ok |
| ON | `no such table: idx.sessions_relacional` |

`memory-catalog-v2.py` abre con `foreign_keys = ON` (lo necesita para sus propias tablas de `main`),
así que el catálogo dejaba de correr. Por eso `vectors.db` se crea **sin las dos FK cruzadas**:

- La FK ya no puede enforcearse a nivel motor; dejarla declarada es una promesa que el motor no
  cumple y que además rompe escrituras.
- Apagar el pragma global rompería las FK reales dentro de `main` (`learnings`, `topic_sessions`,
  `sections`), que sí valen.
- **La integridad la garantiza un chequeo explícito de huérfanos**, no una declaración.

Chequeo obligatorio después de cualquier escritura masiva de vectores:

```sql
SELECT count(*) FROM idx.section_vectors v
  LEFT JOIN main.sections s ON s.id = v.section_id WHERE s.id IS NULL;
SELECT count(*) FROM idx.session_vectors v
  LEFT JOIN main.sessions_relacional r ON r.id = v.session_id WHERE r.id IS NULL;
```

### Regla: sin índice, la búsqueda falla fuerte

Si `vectors.db` no existe o está vacío, `memory-search.py` **debe fallar con error explícito** y no
devolver una lista vacía.

El motivo es un caso testigo de esta misma sesión: dos chequeos reportaban verde midiendo nada (el
check de `orphans` del pre-commit contando un error de `jq` como PASS, y un test de concurrencia
intermitente en CI). Un instrumento roto que devuelve un resultado plausible es peor que uno roto que
devuelve un error. La búsqueda sin índice informa, no finge.

## Plan de implementación

1. **ADR** (este documento), revisado antes de tocar código.
2. **Migración con backup:** copiar `memory.db` a un `.bak` fechado fuera del trabajo, crear
   `vectors.db`, mover las dos tablas, **comparar conteos** (2.352 + 943) y abortar si no coinciden.
3. **Borrar de `main` y `VACUUM`:** solo después de que los conteos cuadren.
4. **Los seis scripts** con `ATTACH` y prefijo `idx.`.
5. **Test de degradación:** sin `vectors.db`, la búsqueda falla con mensaje, no en silencio.
6. **Gate + CI:** `check-adr-supersede.py`, los gates de memoria y el CI de GitHub Actions en verde.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| `vectors.db` se pierde o corrompe | Se regenera con `memory-reembed.py`; el dato crudo nunca estuvo ahí |
| Un script queda sin migrar y lee `main` buscando vectores | El test de degradación y la búsqueda de referencias a las dos tablas antes de cerrar |
| Divergencia silenciosa entre índice y dato (sección borrada, vector huérfano) | Chequeo de huérfanos: cada `section_id` en `idx.section_vectors` debe existir en `main.sections` |
| FK cruzadas rompen escrituras con `foreign_keys=ON` | `vectors.db` se crea sin las dos FK; la integridad va por chequeo explícito (medido 2026-11-04) |
| El respaldo en git queda incompleto | Es lo esperado: el respaldo protege el hecho, no el índice. Documentado aquí |
| Confusión futura sobre qué archivo es la fuente | `memory.db` sigue siendo la fuente (ADR-065). `vectors.db` es un derivado y lo dice en su nombre |

## Consecuencias

**Lo que se gana:** el repo deja de crecer por el índice (~19 MB por cambio de contenido). El respaldo
versionado pesa solo lo irreemplazable. La DB común queda en 6,3 MB.

**Lo que se acepta:** un archivo local más que puede faltar, y por lo tanto un modo de falla nuevo
que exige el chequeo explícito del punto anterior.

**Lo que no cambia:** `memory.db` sigue versionada como respaldo de la fuente de verdad (ADR-054
intacto); los `.md` siguen siendo vistas regenerables (ADR-065); la búsqueda semántica sigue
funcionando con los mismos vectores.
