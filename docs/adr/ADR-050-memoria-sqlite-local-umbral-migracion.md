# ADR-050: La memoria de Kanam OS sigue en SQLite local - umbral de migracion a Postgres/Supabase

**Fecha:** 2026-09-15
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** evaluacion de arquitectura por capas (2026-09-15); pregunta de Gonzo sobre el umbral de migracion
**Relacionado:** ADR-012 (Supabase como BaaS para proyectos), ADR-047 (Kanam Design System)

---

## Contexto

La evaluacion de la arquitectura por capas (`docs/architecture/kanam-os-layers-evaluacion.md`) propuso Postgres + pgvector como capa de datos, alineado con el stack de los proyectos (ADR-012 ya eligio Supabase para Next.js/Vercel). La pregunta que queda es si **la memoria de Kanam OS** (el sistema) deberia migrar a Postgres.

Dato de fondo importante: **no es el mismo plano.** `ADR-012` decide el stack de datos de los *proyectos* (productos web). Kanam OS usa `SQLite` local:

- `memory/memory.db` (11 MB): dailies, sessions, vectores, topics, todos, inbox, contributions.
- `openclaw-agent.sqlite` (577 MB): estado del agente OpenClaw.

Separar las dos es **deliberado y sano**: un producto web multi-usuario necesita un DB server con Auth y RLS; el sistema personal de un usuario en una maquina no.

### Volumen real (verificado 2026-09-15)

| Tabla | Filas |
|---|---|
| daily_notes | 110 |
| sessions_relacional | 44 |
| session_vectors | 115 |
| learnings_enriquecido | 117 |
| topics | 11 |
| todos | 55 |
| inbox | 5 |
| contributions | 66 |

**115 vectores.** Con esa cantidad, la busqueda lineal por coseno es **mas rapida** que cualquier indice ANN (pgvector/HNSW): el overhead del indice no se paga hasta miles de vectores.

---

## Decision

**La memoria de Kanam OS sigue en SQLite local. No se migra a Postgres/Supabase hoy.**

`pgvector` se justifica por **filtros combinados + joins vectoriales**, no por volumen. A esta escala no aplica.

### Umbrales que SÍ justificarian migrar (el "cuando")

Uno solo de estos, sostenido, es motivo para reabrir esta decision (nuevo ADR, no edicion de este):

| Umbral | Valor | Signo de que llego |
|---|---|---|
| Concurrencia real | 2+ procesos escribiendo **a la vez** sin coordinar | El sistema deja de ser un usuario en una maquina |
| Volumen | ~1 GB, o queries > 200ms sostenidas | SQLite se degrada visiblemente |
| Vectores | > 100k con filtros combinados | La busqueda lineal deja de alcanzar |
| Acceso remoto | Otro host lee la memoria | Alguien consulta desde fuera de la maquina |
| Multi-tenant | Alguien que no sos vos usa la memoria | Horizonte 2 (la plataforma) |

### El umbral mas probable de alcanzar primero: higiene de git, no performance

`memory/memory.db` **esta trackeado en git** (`.gitignore` linea 25: `!memory/memory.db`). Eso hoy funciona, pero es la pieza que primero se degrada: un binario que cambia cada sesion en un repo git genera bloat y conflictos en el sync entre maquinas. **El umbral real de vigilar es la higiene de git, no el rendimiento.**

Cuando el bloat de `memory.db` en git se vuelva un problema, la respuesta no es Postgres - es **sacar la DB del repo** (backups por otro mecanismo, los `.md` ya son la vista regenerable) - y ahi recien evaluar el resto.

---

## Consecuencias

### Positivas
- Cero operacion nueva: SQLite no hay nada que mantener.
- La decision queda escrita con umbral objetivo, asi no se re-abre por entusiasmo (regla de `USER.md` 2026-09-14: el precedente no es motivo).
- Se separan los DOS planos de datos sin confundirlos.

### Negativas
- Un solo nodo, sin HA: si la maquina muere se pierde lo no respaldado (mitigado: los `.md` son vista regenerable desde la DB, no al reves).
- Sin acceso remoto al agente desde otra maquina mientras corre.

---

## Alternativas consideradas

1. **Migrar ya a Supabase**: agregar una dependencia y operacion que no resuelve ningun problema medible a 115 vectores. Rechazado por la regla del precedente no-motivo.
2. **Mantener SQLite sin escribir el umbral**: deja la decision abierta a la deriva. Rechazado: sin umbral escrito, cada mejora tentadora re-abre el debate.
3. **Solo mejorar la higiene de git**: la parte concreta del umbral 6. Documentada acá como el paso que probablemente llegue primero, sin requerir migracion de DB.
