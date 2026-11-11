# HANDOFF - Curso langgraph-complete-course

**Fecha:** 2026-11-11 15:40 GMT-3
**Proyecto:** langgraph-complete-course
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-11). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-11.md`.

---

## Que se hizo en esta sesion

Arranque de sesion + montaje de clase: el video jGg_1h0qzaM es 'LangGraph Complete Course for Beginners - Complex AI Agents with Python' (freeCodeCamp.org, Vaibhav Mehra, publicado 2025-05-20, 11.391 s / 3:09:51). No existia en studies/: se bajaron los subtitulos automaticos en ingles (pista en-orig, fmt=json3) con curl directo desde automatic_captions de yt-dlp (3,3 MB, 4.509 cues deduplicados de ~31.500 palabras; ultimo cue en 11.387 s contra 11.391 del reproductor). Se creo studies/langgraph-complete-course/: transcripcion.md con encabezado (glosario ASR de 19 filas, tabla de los 31 capitulos oficiales) y cues intactos; outline.md con 14 modulos 1:1 con los capitulos oficiales, mapa temporal, ejercicios por modulo, banco de 8 preguntas y notas editoriales. Cada cita del outline se verifico con un script contra transcripcion.md (contando el inicio del cue real, no solo que la frase exista): BAD 0 tras corregir la cita de pricing, recortar tres citas partidas entre cues y reemplazar seis frases que estaban entre comillas sin ser literales del transcript. Hallazgo principal del material: el curso es bueno en fundamentos (grafos sin LLM -> memoria -> ReAct -> Drafter -> RAG) pero NO cubre checkpointer real, interrupt()/Command (lo esquiva con una variable global), subgrafos, Send, streaming ni observabilidad. ADOPCION.md con un artefacto que muerde: scripts/check-state-schema.py, que falla cuando un nodo escribe state['k'] con k fuera del TypedDict del estado. Corrido contra projects/oss-post-graph detecto 8 claves escritas sin declarar (draft_path_temp, facts_comments, facts_files, facts_issue, facts_pr, already_published, gate_stdout, gate_stderr); salida pegada en ADOPCION.md. Gate probado en ambas direcciones (exit 0 en repo limpio, exit 1 con clave nueva) para que no sea un siempre-verde. Se descarto adoptar interrupt() porque oss-post-graph YA lo usa bien en src/approval.py, y se descarto crear skill nueva: la regla del curso es escribirla recien despues de un uso real. studies/README.md actualizado. Commit local 3aeb91164c (pre-commit del workspace verde: 73 asserts bats + suites JS + runner). Sin push.

## Proximos pasos

1. Declarar las 8 claves faltantes en projects/oss-post-graph/src/state.py o marcarlas ALLOWED_UNDECLARED con motivo; decidir si check-state-schema.py entra al gate del proyecto o al pre-commit del workspace (recien entonces exigir exit 0); candidatos del curso aun no adoptados: recorte de historial a N mensajes y add_messages como reducer, ambos esperando un grafo conversacional real

## Decisiones y contexto que no debe perderse

- No se toca el codigo de oss-post-graph en esta sesion: el curso es autorizacion para montar la clase, no para editar otro proyecto

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-11.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
