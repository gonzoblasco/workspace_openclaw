# DECISIONES - Kanam Story Bible

Cierre de las decisiones abiertas de la spec. Aca se registra que se decidio, con
que evidencia, y que se dejo explicitamente afuera.

## Motor de almacenamiento

**Decidido por Gonzo (2026-09-24):** PostgreSQL 16 + pgvector en Docker Compose,
la opcion que la spec propone como principal.

Contexto que condiciono la eleccion: en el Mini no habia Docker ni Postgres
instalados (verificado antes de decidir). Se instalo Colima (`brew install colima
docker docker-compose`) en vez de Docker Desktop: runtime OSS, 4 CPU / 8 GB de VM,
sin licencia comercial. La base se publica en `127.0.0.1:5433` (loopback), nunca a
la red.

**Consecuencia aceptada:** el Mini ahora corre un stack de contenedores para un
producto de un solo usuario. Es operativamente mas pesado que SQLite, y es lo que
la decision pide.

## Contrato HTTP: idioma

**Ingles en el wire, espanol en el dominio.** El modelo de datos y el codigo
interno siguen los nombres del dominio en espanol (`card`, `nombre`, `atributos`);
la API expone `entity`, `name`, `attributes`.

Motivo: la regla de idioma por capa (AGENTS.md) - lo que se ve en GitHub va en
ingles. La spec tambien esta escrita en ingles para los nombres de campo.
El mapeo vive en un unico modulo (`serializers.py`), no repartido por los routers.

## `braindump_private`

**No es un tipo de bloque.** La tabla `foundation_block` tiene un registro por tipo
y un `CHECK` con los siete tipos de la spec; `braindump_private` no estaba en esa
lista y hacerlo tipo propio rompia la restriccion.

Se persiste dentro del bloque `braindump`, en `contenido.privado`. La API lo expone
como campo propio porque es lo que espera el contrato. Un intento previo de tenerlo
como bloque propio fallo con `CheckViolation` (evidencia: log del contenedor).

## Indice desactualizado

La spec pedia `409` cuando `reindex_required = true`. Se implemento literal: si el
outbox tiene eventos pendientes, `/retrieve` devuelve 409 con
`indice desactualizado respecto de la ultima escritura`.

Se evaluo y se **descarto** la alternativa de drenar el outbox dentro del propio
retrieve (consistencia eventual invisible al cliente): oculta el estado real y hace
que una lectura sea una escritura. El 409 es honesto y el cliente sabe que hacer.

## Truncamiento del modelo

Los modelos de razonamiento consumen `max_tokens` **pensando** antes de emitir
contenido. Con un presupuesto corto, `content` sale vacio y `finish_reason` es
`length`: no hay JSON truncado, no hay JSON en absoluto.

Medido el 2026-09-24 sobre el mundo real "Cartas sin Mandar" (braindump de ~6.900
caracteres, contexto RAG de 6.211 caracteres):

| `max_tokens` | `finish_reason` | caracteres de contenido | resultado |
|---|---|---|---|
| 1200 | `length` | **0** | `Expecting value: line 1 column 1 (char 0)` |
| 3000 | `length` | 1466 | JSON truncado |
| 8000 | `stop` | 2278 | JSON valido, 3 candidatos |

La spec pedia un unico reintento ("un segundo rara vez corrige y duplica el
costo"). Se mantiene uno solo, pero con dos correcciones:

1. **Piso de salida** (`generation_min_max_tokens`, 4000 por defecto). El
   presupuesto de razonamiento va **encima** del de salida; no compiten. Si el
   cliente pide 1200, se usa el piso.
2. **El reintento cubre los dos modos de fallo**: respuesta cortada (`length`) y
   contenido vacio, que son el mismo problema con distinto sintoma. Va con
   `generation_retry_max_tokens` (16000) y una instruccion explicita de no
   explicar el razonamiento.

`llm.chat_detallado` ahora devuelve un dataclass con `contenido`, `finish_reason`,
`razonamiento_chars` y `tokens_completion`, mas un `diagnostico()` que traduce el
fallo a una frase entendible. El job guarda `presupuesto_tokens` y
`razonamiento_chars` en su resultado, asi que un fallo futuro se explica solo.

**Leccion general:** "el modelo se corto" y "el modelo no dijo nada" tienen la
misma causa raiz en modelos de razonamiento. Tratarlos como un solo caso de
presupuesto insuficiente es mas simple y mas correcto que distinguirlos.

## Embeddings

`nomic-embed-text:latest`, 768 dimensiones, ya presente en la maquina. La columna
`chunk.embedding` es `vector(768)`, asi que cambiar de modelo con otra dimension
exige migracion de columna. Queda como deuda registrada, no como sorpresa.

## Fuera de v1

Se implemento primero el vertical completo (mundo -> indice -> retrieval ->
generacion -> apply -> export) y se dejo explicitamente afuera:

- **UI web.** No hay React ni Vite todavia. Se opera por HTTP.
- **Worker arq.** Redis esta levantado y la dependencia instalada, pero no hay
  proceso worker: el outbox se drena por `/index/drain` o dentro de `reindex`.
- **Autenticacion.** `auth_mode=none` con bind a loopback. Los modos `token` y
  `token+tls` de la spec estan disenados, no implementados.
- **Multiusuario, roles y permisos.** La spec se contradice en esto (el alcance los
  excluye y hay capitulos enteros que los especifican). Se sigue el alcance: fuera.

## Correcciones aplicadas a la spec

La spec generada tenia ruido que no se traslado al codigo:

- Secciones de roles/permisos (5 roles, matriz de 40 filas) sobre un producto que se
  declara mono usuario y sin autenticacion remota. Descartado.
- Tres entornos (dev/staging/prod), k6 con 3 sesiones concurrentes, RPO 5 min,
  particionado de `audit_log` a 5M filas: boilerplate de SaaS para un mundo
  literario personal. Se implemento un solo entorno.
- `PostgreSQL vs SQLite` figuraba como decision abierta mientras el resto del
  documento asumia Postgres en todas sus secciones. Cerrada explicitamente.
