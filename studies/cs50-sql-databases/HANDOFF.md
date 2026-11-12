# HANDOFF - Clase cs50-sql-databases

**Fecha:** 2026-11-12 01:50 GMT-3
**Proyecto:** cs50-sql-databases (clase de estudio, no proyecto de código)
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> Punto de entrada para continuar esta clase. El informe de la sesión vive en `memory/2026-11-12.md` (entradas «Session End - studies/cs50-sql-databases» 1 y 2).

---

## Qué es

Clase montada desde YouTube a partir de `https://www.youtube.com/watch?v=WXk7yDqsKxs` (**Harvard CS50's Intro to Databases with SQL – Full University Course**, freeCodeCamp.org, Carter Zenke, 11:08:48, publicado 2025-10-09).

**Método de estudio (fijado por Gonzo, 2026-11-12):** el curso se estudia **a través de Kanam**. Kanam enseña cada módulo usando el outline + el transcript como fuente (y puede investigar lo que falte), y la práctica se hace **en el momento en que cada tema aparece**, con todos los ejercicios resueltos y corridos. El motivo declarado: el objetivo final de Gonzo es escribir **skills, scripts y workflows**, y eso se aprende con mucha práctica ejecutada, no leyendo.

## Estado actual

| Artefacto | Qué tiene | Estado |
|---|---|---|
| `video-meta.json` | Metadata verificada: 40.128 s, 8 capítulos oficiales, cobertura de captions (último cue 11:08:36) | ✅ |
| `transcripcion.md` | 14.819 cues con `[hh:mm:ss]`, captions `en-orig`, ~107.654 palabras | ✅ |
| `outline.md` | 7 módulos 1:1 con los capítulos oficiales, 26 citas verificadas, 45 ejercicios, banco de 22 preguntas, plan en 8 sesiones, sección de lo que el curso no cubre | ✅ |
| `modulo-00/` | **Módulo 0 enseñado y practicado entero.** `setup.sql`, `m0_workers.db` (8 filas), `ejercicios.md` (10 ejercicios con salida real y respuesta), `check_m0.py` (verificación con exit code) | ✅ |
| `modulo-01/` en adelante | Módulo 1 (Querying) sin empezar | ⬜ |

**Commits:** `affaa95155` (clase) · `c94598c87e` (laboratorio del módulo 0). Sin push.

## Estructura de un módulo (el molde que se repite)

Cada módulo abre `modulo-NN/` con cuatro piezas, y la regla es que **la práctica se corre entera antes de publicarla**, con la salida pegada:

1. `setup.sql` — la base de práctica, reconstruible desde cero.
2. `mN_*.db` — la base ya creada (8 KiB, versionable sin problema).
3. `ejercicios.md` — un ejercicio por tema, con la respuesta y **la salida real**.
4. `check_NN.py` — el pipeline: query, verificación que puede fallar, exit code 0/1.

## Módulo 0 — lo que quedó demostrado

| # | Qué prueba | Hallazgo |
|---|---|---|
| E1–E3 | CRUD | `UPDATE` sin `WHERE` toca todas las filas |
| E4 | Constraints | `CHECK` y `NOT NULL` dan mensajes distintos: regla de negocio vs. de estructura |
| E5 | `DELETE` | Sin `WHERE` vacía la tabla **y devuelve OK** |
| E6 | `GROUP BY` | 8 filas → 5; el resultado no existe en disco, se calcula |
| E7 | Float | **Corregido:** sumar floats no acumula error (1000×0.07 = 70.0 exacto). Rompen el **truncado** (`CAST(1.15*100)=114`) y la **comparación** (`0.1+0.2=0.3` es falso; `WHERE price*100=1999` devuelve vacío) |
| E8 | Centavos enteros | `CAST(ROUND(x*100) AS INTEGER)`; el `ROUND` antes del `CAST` es la diferencia entre 114 y 115 |
| E9 | `STRICT` | SQLite acepta `'hola'` en una columna `INTEGER` sin `STRICT` |
| E10 | Pipeline | stdout/stderr separados, exit 1, y el gotcha del buffering |

## Próximos pasos

1. **Módulo 1 — Querying** (0:02:35 → 1:21:49, 80 min de video): `SELECT`, `WHERE` y operadores, `LIKE` con `%` y `_`, `BETWEEN`, `NULL`, `ORDER BY`, `LIMIT`, agregaciones, `DISTINCT`, `GROUP BY` + `HAVING`. Mismo molde: enseñar y practicar en el momento.
2. **Decidir cuándo introducir Postgres.** Todo el curso es SQLite; la afinidad (E9) y la falta de `DECIMAL` son las dos razones para practicar en Postgres al menos una vez antes del módulo 6.
3. **Vane** disponible si hace falta investigación externa (dato no cubierto por el transcript): está bajo demanda (`toolbox up vane`), así que si un tema lo pide, Kanam prepara el prompt.

## Decisiones y contexto que no debe perderse

- **Transcript por captions automáticos, no ASR local.** 11 h con whisper no agregaba nada.
- **yt-dlp 2025.10.14 falla con `The page needs to be reloaded`** sobre este video; funciona con `--extractor-args "youtube:player_client=android,web_safari"`.
- **`Writing` y `Viewing` comparten timestamp** (4:24:52): el video las une en un módulo de 3:05:35. El outline lo respeta.
- **`sqlite3` del sistema no abre bases dentro del workspace** en esta máquina (guard de estado de OpenClaw, no es SQL). Correr con Python o copiar la base a `~/tmp/`.
- **`total_changes` de Python sqlite3 es acumulado** durante toda la conexión, no por statement. Confundió una corrida y se verificó aparte.
- **Errores de ASR corregidos en las citas:** Zeni → Zenke, Postgress → PostgreSQL, SQL light → SQLite, CT → CTE.

## Cómo continuar

1. Leer este HANDOFF.
2. Abrir `outline.md` en el módulo que toque y enseñar desde ahí, contrastando contra `transcripcion.md` antes de citar.
3. Crear `modulo-NN/` con el molde de cuatro piezas y **correr todos los ejercicios** antes de mostrarlos.
