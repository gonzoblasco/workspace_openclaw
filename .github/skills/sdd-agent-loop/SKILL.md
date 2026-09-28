---
name: "sdd-agent-loop"
description: "Loop de agentes por etapas con gate humano: cuando una tarea se parte en discovery/openspec/design/plan/build/review/qa/release, cuando hay que decidir si una etapa puede avanzar sola o debe frenar, o cuando un agente reporta exito y hay que verificarlo antes de creerle."
metadata:
  category: "Hermes SDD"
  tags:
    - hermes-sdd
    - imported
    - orchestration
---

# sdd-agent-loop

Loop de desarrollo por etapas con agentes, adaptado del repositorio
`mcabreradev/hermes-sdd-agency` (bundles `feature`, `bugfix`, `fix`, `do`).
Los nombres de archivo y rutas de Hermes fueron reemplazados por el equivalente en Kanam.

## Cuando usarla

- Una tarea se parte en etapas con agentes distintos (discovery, openspec, architect,
  planner, builder, reviewer, qa, release).
- Hay que decidir si una etapa puede avanzar sola o tiene que frenar y consultar.
- Un agente reporto exito y hay que verificar antes de creerle.

## Las etapas

| Etapa | Rol | Entregable |
|---|---|---|
| discovery | `hermes-discovery` | Descripcion de lo que existe, con evidencia |
| openspec | `hermes-openspec` | Spec valida (propuesta, tareas, delta) |
| architect | `hermes-architect` | `design.md` y ADRs del cambio |
| planner | `hermes-planner` | Tareas ejecutables, ordenadas y verificables |
| builder | `hermes-builder` | Codigo del cambio, nada mas |
| reviewer | `hermes-reviewer` | Defectos probados (adversarial) |
| qa | `hermes-qa` | Comportamiento validado contra la spec, con ejecucion real |
| release | `hermes-release` | Diff consistente, version, notas, archivado |

Etapas independientes pueden correr en paralelo. **Solo reviewer y qa pueden bloquear.**

## El confidence gate (lo unico que despierta al humano)

La etapa avanza sola en decisiones rutinarias. Frena ante una decision no trivial.

**Rutinario (no frena):** seguir el stack y los patrones existentes del proyecto; si una
regla de negocio no esta declarada, implementar el minimo y marcarlo `ASUMIDO - verificar`
en el reporte y en el ADR; nunca inventar una regla.

**No trivial (frena y consulta):** costo de revertir alto; contrato publico o API; cambio de
esquema o modelo de datos; seguridad (auth, secretos, exposicion); regla de negocio ambigua
que cambia comportamiento visible; partir la feature; aceptar deuda estructural; dependencia
nueva no estandar para el stack.

Al frenar: reportar la decision con opciones, una recomendacion y el impacto. No asumir.
Regla: **lo rutinario duerme, lo no trivial despierta.**

## Verify before advance (la regla que se viola sola)

**La respuesta de un agente es un auto-reporte, no un hecho.** Antes de avanzar de etapa,
verificar la salida en el repositorio real. Un agente puede cerrar en `done` habiendo
producido otra cosa, o nada.

Minimos, siempre:

```
git status --porcelain         # que cambio de verdad
git diff --stat                # cuanto cambio
<pasos de reproducir>          # volver a correr el resultado, no leerlo
```

Medido el 2026-09-28: dos tandas de sub-agents reportaron tablas de exito sobre 43 y 9
artefactos; el disco mostro 83 y 0. Ver `docs/checklists/delegation-brief.md`.

## Protocolo

1. Resolver la raiz del proyecto y confirmarla.
2. Preflight: si falta el artefacto base del proyecto (spec inicial), crearlo antes de seguir.
3. Leer el workflow de la etapa y el rol del agente que corresponde.
4. Delegar **una tarea acotada por agente**, con brief autocontenido
   (`docs/checklists/delegation-brief.md`: resultado, criterio de aceptacion, comando de
   verificacion, restricciones).
5. **Verificar la salida de cada agente en el repo real antes de avanzar.**
6. Al cerrar: reporte final, archivado y sincronizacion del cambio.

## Restricciones

- Un sub-agent **no** puede crear sub-agents (`sessions_spawn` no esta disponible para el).
  La orquestacion la hace siempre el agente padre.
- El humano se consulta ante ambiguedad de negocio, arquitectura, seguridad o alcance.

## Origen

Extraido de `skill-bundles/*.yaml` y `skills/software-development/hermes-sdd-orchestration`.
La parte conservada como valiosa es el contrato por etapas, el gate de confianza y la
exigencia de verificar antes de avanzar. Las rutas `~/.hermes/*` de Hermes no aplican aca.
