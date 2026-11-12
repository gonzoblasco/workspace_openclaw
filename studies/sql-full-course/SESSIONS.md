# SESSIONS - studies/sql-full-course

> Indice append-only de cierres de sesion. El HANDOFF.md es solo el estado actual; esta lista es la historia (no se pisa).

- **2026-11-11 12:06** - Arranque de sesion + montaje de clase: el video SSKVgrwhzus es 'SQL Full Course for Beginners (30 Hours) – From Zero to Hero' (Data with Baraa, publicado 2025-03-27, 29:48:27, 41 capitulos oficiales). No existia en studies/. Captions automaticos en-orig via yt-dlp (96.716 eventos -> 48.358 cues, ~364.000 palabras, timestamps reales, cobertura completa verificada), outline de 22 modulos en los tres niveles del curso mas los tres proyectos, 12 citas verificadas contra el transcript con timestamps corregidos a cue exacto, banco de 18 preguntas. studies/README.md actualizado. Commit local 9dc50c81b7, sin push.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
- **2026-11-11 12:07** - Clase montada desde YouTube: 'SQL Full Course for Beginners (30 Hours) - From Zero to Hero' (Data with Baraa, 29:48:27, 41 capitulos). Transcript por captions…
- **2026-11-12 01:52** - Nivel Beginner del curso estudiado con practica ejecutada, no leida. Sandbox en studies/sql-full-course/beginner/: run.py (runner Python sobre sqlite3 porque e…
- **2026-11-12 01:52** - Nivel Beginner estudiado con practica ejecutada. Sandbox propio (run.py sobre sqlite3 en proceso porque el guard de OpenClaw bloquea el binario bajo el state dir), 9 bloques en 01-que-es-sql.md, 02-repaso-beginner.sql con resultados esperados. Cuatro correcciones salieron de correr y no de suponer: alias en WHERE (SQLite acepta, el estandar no; manual MySQL B.3.4.4), conte mal el nombre mas largo (LENGTH: Elena Vidal 11), ORDER BY con NULL cambia de motor, y la orden huerfana del dataset (customer_id 5) que el INNER JOIN esconde. Commit 48044f63c3.
