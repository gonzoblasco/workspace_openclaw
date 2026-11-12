# HANDOFF - Curso system-design-interview-guide

**Fecha:** 2026-11-12 01:49 GMT-3
**Proyecto:** system-design-interview-guide
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Monté la clase del curso 'Design Software Systems Like a Senior Engineer' (freeCodeCamp/Hayk Simonyan, 3:16:48) desde captions automáticos: transcripcion.md con 600 bloques y glosario ASR, outline.md con 20 módulos 1:1 con los 37 capítulos oficiales y 28 citas verificadas (gate BAD: 0), y ADOPCION.md con el gate check-observability-gaps.py. Después se estudió el Módulo 1 en modo práctica con Gonzo: en vez de resumirlo, se corrieron las cuatro preguntas del ejercicio sobre Preflight con un harness propio (experiments/measure-scan.mjs, gitignored).

## Estado actual

Módulo 1 del curso cerrado con fix de producto. Medición real de Preflight: 0.87 scans/s con MAX_CONCURRENT=4 (p50 4487ms a 4 concurrentes vs 9123ms a 1), pico RSS 302MB con 4 contextos sobre 257MB base, 0 fallos con 12 jobs encolados. Hallazgo capital: recordUsage() cobraba el scan ANTES de scanPage(), así que un crash o una máquina matada por Fly consumía cuota del usuario sin entregar nada. Corregido en commit local 1596dac de projects/preflight: refundUsage() nuevo, ScanError sigue cobrando, todo lo demás devuelve el slot, aplicado en la ruta REST y en el tool MCP scan_url. Tests 15/15, tsc limpio, build verde. Pushear requiere OK de Gonzo.

## Proximos pasos

1) Módulo 2 del curso (las cinco dimensiones de evaluación): Gonzo tiene que contestar el ejercicio - qué dimensión ejercía, cuál no, y cuál no se puede practicar solo. 2) Hallazgos pendientes de Preflight: la cola del semáforo de scans no se publica en /status aunque el código la construye (waiters.length nunca se lee); no hay umbral de latencia/alertas; el gate check-observability-gaps.py da OK falso en latencia y umbral porque mide archivos distintos, no un pipeline de métricas. 3) Decidir si experiments/measure-scan.mjs sube a scripts/ como gate permanente del workspace. 4) El commit 1596dac y los 6 commits previos de otras sesiones siguen sin push.

## Decisiones y contexto que no debe perderse

- El curso se estudia por módulo con práctica ejecutada, no con resumen: cada módulo cierra con un artefacto corrido contra un sistema real del workspace (regla del paso 12 del skill video-transcription aplicada a pedido de Gonzo). El fix de cuota se aplicó desde el CORE aunque sea código de Preflight porque estaba en alcance de diagnóstico ya autorizado y verificado con gates; un push o un deploy seguirían necesitando OK explícito. El repo Preflight tiene su propio AGENTS.md, leído antes de tocar: exige leer BRIEF y STATUS antes de cambiar comportamiento de producto.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
