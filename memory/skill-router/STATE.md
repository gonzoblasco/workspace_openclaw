# Skill-Router / Capability-Index — Estado

> Dueño de la verdad: `agents/kanam-planner/.knowledge/programs/skill-router-improvement.json`. Este archivo es un resumen vivo para retomar sin redescubrir; NO duplica facts (skill count, modelo, etc.) — los cita de su dueño.

## Programa

- Programa: `skill-router-improvement` (T=17, high)
- Estado acutal: **5/8 pasos completos** (actualizado 2026-11-06).
- Next: paso 5 — skill `capability-index`.

## Hecho

- Paso 0 — colapso del pipeline (ADR-049 archived, 2 skills eliminadas, check-pipeline-enforcement libre del skill arbitrado).
- Paso 1 — router por CLI (171 skills vía `openclaw skills list`, fallback a disco).
- Paso 2 — regresión runner `scripts/test-skill-router.py` (10/10 en top-3). Refactor: `suggest()` extraída.
- Paso 3 — `scripts/check-skill-overlap.py` (aviso, 20 pares ≥0.87).
- Paso 4 — cableado al pre-commit con disparador `BOUNDARY_RELEVANT`, modo aviso.

## Pendiente

- Paso 5 — skill `capability-index`: responder "¿tenés X?" en cuatro estados con evidencia de ruta. Se dejó de lado por la conversación (ver decisión abierta).
- Paso 6 — Docs (SKILLS-INDEX, CHANGELOG) + decisión sobre ADR propio.
- Paso 7 — gate Auditor con evidencia cruda.

## Decisiones abiertas conversadas

1. capability-index: skill pura vs. skill + script `query_capability` (ver MEMORY de abajo).
2. ADR propio vs. managed block en AGENTS/docs (principio "editar, no agregar").
3. Scope del catálogo por rol (hoy es el conjunto completo del `main`).
4. Throttle de embeddings en `check-skill-overlap` (171 llamadas por commit es lento).
5. Umbral fijo 0.87 vs. calibrar con datos reales y promover a blocking.
6. Telemetría de misses (queries que no llegan a top-3) para cerrar el loop.

## Modelos aprobados por Gonzo (2026-11-06)

- Solo los grandes/gpt-oss:cloud vigentes y gratuitos. No arquitecturas nuevas sin revisión.

## Fuente única para hechos

- conteo de skills → `openclaw skills list --agent main --json`
- modelos → bloque MANAGED `#model-operativo` en AGENTS.md
- programa → JSON de kanam-planner (ver path arriba)
- este archivo solo resume.