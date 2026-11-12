# HANDOFF - Curso sql-full-course

**Fecha:** 2026-11-11 12:07 GMT-3
**Proyecto:** sql-full-course
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-11). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-11.md`.

---

## Que se hizo en esta sesion

Clase montada desde YouTube: 'SQL Full Course for Beginners (30 Hours) - From Zero to Hero' (Data with Baraa, 29:48:27, 41 capitulos). Transcript por captions automaticos en-orig via yt-dlp: 96.716 eventos deduplicados a 48.358 cues, ~364.000 palabras, timestamps reales, cobertura completa verificada. Outline de 22 modulos en los tres niveles del curso (Beginner/Intermediate/Advanced) mas los tres proyectos (DWH medallion, EDA, Advanced Analytics), 12 citas verificadas contra el transcript con timestamps corregidos a cue exacto, banco de 18 preguntas. Registro en studies/README.md. El audio no se pudo bajar (HTTP 403 en todos los formatos con yt-dlp 2025.10.14); los captions alcanzaron.

## Estado actual

Clase montada y commiteada (9dc50c81b7, sin push). Sin ejercicios ejecutables por modulo.

## Proximos pasos

1. Agregar ejercicios ejecutables por modulo si Gonzo lo pide (los bloques Beginner y Window Functions son los mas ejercitables). 2. Decidir si se corren en un Postgres local o quedan como SQL Server en papel. 3. Definir si se estudia la clase completa o se saltean los bloques ya cubiertos (el material de ventanas y performance es el de mayor valor para el workspace).

## Decisiones y contexto que no debe perderse

- Transcript por captions automaticos de YouTube y no ASR local: 30 h con whisper medium no era viable y los captions traen timestamps reales con cobertura completa. El curso es SQL Server (GETDATE, TOP, ISNULL, file groups), no Postgres: un ejercicio portable hay que traducirlo. Errores de ASR sistematicos: 'Barzalini' es Baraa, 'shippet/shad/shajibet' es ChatGPT, 'CDS' es CTAS, 'store procedure' es stored procedure. El video se grabo el 18 de julio de 2024 y se publico en marzo de 2025. El material descargable (datawithbaraa.com/wiki/sql) no se bajo ni se audito.

## Cerrados en esta sesion

- Sin ejercicios por módulo todavía. El formato de las otras clases (ai-engineer-full-course, rag-mcp-fundamentals) incluye ejercicios por módulo; acá se hizo primero la estructura completa porque el curso tiene 22 módulos y 30 h. (movido a proximos pasos: agregar ejercicios por modulo)

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-11.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
