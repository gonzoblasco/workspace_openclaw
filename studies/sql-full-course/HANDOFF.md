# HANDOFF - Curso sql-full-course

**Fecha:** 2026-11-12 01:52 GMT-3
**Proyecto:** sql-full-course
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Nivel Beginner del curso estudiado con practica ejecutada, no leida. Sandbox en studies/sql-full-course/beginner/: run.py (runner Python sobre sqlite3 porque el guard de OpenClaw bloquea el binario bajo el state dir), 01-setup.sqlite.sql con people/customers/orders/regions, 01-que-es-sql.md (9 bloques ejecutados) y 02-repaso-beginner.sql con resultados esperados en comentario. Commit 48044f63c3.

## Estado actual

Nivel Beginner cerrado. Cuatro correcciones salieron de ejecutar: SQLite acepta alias en WHERE aunque el estandar lo prohibe (manual MySQL B.3.4.4); LENGTH desmintio mi calculo del nombre mas largo (Elena Vidal, 11); ORDER BY con NULL cambia de motor; el dataset tiene una orden huerfana que el INNER JOIN esconde.

## Proximos pasos

1. Agregar ejercicios ejecutables por modulo si Gonzo lo pide: los bloques Beginner y Window Functions son los mas ejercitables. Hecho para Beginner, sigue para Intermediate y Advanced. 2. Decidir si los ejercicios corren en Postgres local o quedan como SQL Server en papel. 3. Definir si se estudia la clase completa o se saltean los bloques cubiertos: el material de ventanas y performance es el de mayor valor para el workspace. 4. Que Gonzo corra los tres ejercicios de cierre de Beginner (COUNT(*) vs COUNT(o.id) en LEFT JOIN; EXCEPT/INTERSECT con NULL; AVG y el divisor). 5. Cada bloque se ejecuta en el sandbox antes de escribirse.

## Decisiones y contexto que no debe perderse

- Transcript por captions automaticos de YouTube y no ASR local: 30 h con whisper medium no era viable y los captions traen timestamps reales con cobertura completa. El curso es SQL Server (GETDATE, TOP, ISNULL, file groups), no Postgres: un ejercicio portable hay que traducirlo. Errores de ASR sistematicos: 'Barzalini' es Baraa, 'shippet/shad/shajibet' es ChatGPT, 'CDS' es CTAS, 'store procedure' es stored procedure. El video se grabo el 18 de julio de 2024 y se publico en marzo de 2025. El material descargable (datawithbaraa.com/wiki/sql) no se bajo ni se audito. El sandbox crece a traves de 01-setup.sqlite.sql y no borrando tablas: regions se incorporo ahi para que --reset no la pierda. Los resultados se corren, nunca se estiman. Commits del curso: 9dc50c81b7 (montaje), 5ac8f85703 (primer cierre), 48044f63c3 (Beginner).

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
