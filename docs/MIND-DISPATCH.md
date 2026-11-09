# MIND-DISPATCH.md - Kanam MIND en el flujo del Crew

**Fecha:** 2026-11-07
**Fuente:** `agents/kanam-mind/docs/MIND-DISPATCH.md` §7 (verificado por MIND).
**Base:** ADR-074 (cada rol es dueño de su dominio), ADR-083 (el CORE orquesta, no implementa),
`agents/kanam-mind/ROADMAP.md` Hito 5.0.

## Cuándo llamar a MIND

Una sola condición: el pedido necesita **una afirmación sostenida por una fuente abierta**.

- `research`: investigá X empresa/producto/tecnología, qué pasó con Y, fundamentá una decisión.
- `verify`: ¿es cierto lo que reportó DEV/Critic?, chequeá esta afirmación.
- `study`: procesá el capítulo N, extraé los aprendizajes de este material.
- `audit`: auditá las citas de este documento, ¿esto tiene evidencia?

## Cuándo NO es MIND (y a quién va)

| El pedido es | Dueño |
|---|---|
| Redacción/post/CV/marca | `kanam-studio` |
| Tesis de UI/UX, evaluación visual, a11y | `kanam-auditor` |
| Implementar, refactorear, arreglar bug | `kanam-dev` |
| Config, automatizaciones, backups, drift | `kanam-ops` |
| Plan multi-sesión | `kanam-planner` |

## Cómo se pide

`sessions_spawn(agentId: "kanam-mind", context: "isolated")` con el cuerpo de
`agents/kanam-mind/templates/brief-request.md`.

## Devuelve siempre

- Ruta exacta del brief.
- Veredicto del gate (`PASS`/`PARTIAL`/`FAIL`) con defectos listados.
- Fuentes abiertas (fecha cuando caduca).
- Incógnitas declaradas.
- Entrada en el journal con veredicto.

## Límite que no se delega

MIND investiga y verifica; no publica, no contacta, no manda nada hacia afuera, no borra, no cambia producción.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
