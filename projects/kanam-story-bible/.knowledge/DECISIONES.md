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

Si el modelo termina con `finish_reason == "length"`, el JSON llega cortado. La spec
acepta un unico reintento ("un segundo rara vez corrige y duplica el costo").

Implementado: reintento unico con el doble de presupuesto de tokens y una
instruccion explicita de brevedad, y recien despues se parsea. Evidencia: sin esto,
el job real fallaba con `Unterminated string starting at: line 10 column 16`.

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
