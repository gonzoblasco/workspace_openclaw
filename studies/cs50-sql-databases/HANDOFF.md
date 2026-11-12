# HANDOFF - Clase cs50-sql-databases

**Fecha:** 2026-11-12 00:25 GMT-3
**Proyecto:** cs50-sql-databases (clase de estudio, no proyecto de código)
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> Punto de entrada para continuar esta clase. El informe de la sesión vive en `memory/2026-11-12.md`.

---

## Qué es

Clase montada desde YouTube a partir de `https://www.youtube.com/watch?v=WXk7yDqsKxs` (**Harvard CS50's Intro to Databases with SQL – Full University Course**, freeCodeCamp.org, Carter Zenke, 11:08:48, publicado 2025-10-09).

## Estado actual

**Completa en su primera versión.** Cuatro artefactos:

| Archivo | Qué tiene |
|---|---|
| `video-meta.json` | Metadata verificada: duración 40.128 s, 8 capítulos oficiales, cobertura de captions (último cue 11:08:36, gap 12 s) |
| `transcripcion.md` | 14.819 cues con `[hh:mm:ss]`, subtítulos automáticos `en-orig` vía yt-dlp, ~107.654 palabras |
| `outline.md` | 7 módulos (0 a 6) 1:1 con los capítulos oficiales, 26 citas verificadas, 45 ejercicios, banco de 22 preguntas, plan de estudio en 8 sesiones, sección explícita de lo que el curso no cubre |
| `HANDOFF.md` | Este archivo |

## Próximos pasos (si Gonzo quiere seguir)

1. **Ejercicios ejecutables.** Los 45 ejercicios están en prosa, sin archivos. El primer bloque que lo pide es M1 (Querying) y M3 (constraints): son los dos más fáciles de convertir en `.sql` con un dataset mínimo propio, sin depender de los datasets de CS50.
2. **Decidir motor de práctica.** Todo el curso es SQLite; si se ejerce en Postgres local, hay que traducir `AUTOINCREMENT`, `EXPLAIN QUERY PLAN` → `EXPLAIN`, `.schema` → `\d`, y los tipos (`TEXT`/`NUMERIC` son afinidades, no tipos).
3. **Cruzar con `sql-full-course`** (Data with Baraa, 30 h, SQL Server): ese cubre lo que este no (window functions, CTEs a fondo, tres proyectos de datos). Decidir el orden: CS50 primero por el modelo, Baraa después por la analítica.
4. **Auditar los problem sets del sitio de CS50** (`cs50.harvard.edu/sql/`), que el video no incluye.

## Decisiones y contexto que no debe perderse

- **Transcript por captions automáticos, no ASR local.** 11 h con whisper no agregaba nada: los captions traen timestamps reales y la cobertura se verificó (el último cue cae a 12 s del final).
- **yt-dlp 2025.10.14 falla con `The page needs to be reloaded`** en el primer intento sobre este video; con `--extractor-args "youtube:player_client=android,web_safari"` baja metadata y captions. El audio no se intentó (no hacía falta).
- **El índice oficial de la descripción trae `Writing` y `Viewing` con el mismo timestamp** (4:24:52): el video las une en una sola clase de tres horas. El outline lo respeta como un solo módulo, no inventa un corte.
- **La duración real del capítulo "Writing/Viewing" es 3:05:35**, la más larga del curso; por eso el plan de estudio la parte en dos sesiones.
- **Errores de ASR corregidos en las citas:** Zeni → Zenke, Postgress/PostQL → PostgreSQL, SQL light → SQLite, `CT` → CTE. Las citas se citan en su forma corregida, no en la transcripción literal.
- **Lo que el curso no cubre está declarado en el outline, con evidencia del transcript** (cero menciones de `window`, `coalesce`, `ifnull`, `offset`, `glob`, `rowid`, Python más allá de una pregunta del público). No es una omisión del estudio: es una propiedad del video.

## Cómo continuar

1. Leer este HANDOFF.
2. Abrir `outline.md` en el módulo que toque y seguir el plan de 8 sesiones.
3. Verificar el transcript con `grep "\[hh:mm:ss\]"` antes de citar cualquier pasaje nuevo.
