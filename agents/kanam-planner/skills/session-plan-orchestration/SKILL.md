---
name: "session-plan-orchestration"
description: "Orquestar una tarea compleja como un plan persistente: cuando hay que trazar los pasos y asignar roles en orden, cuando una tarea tiene filtros secuenciales (implementacion, superficie, sustancia) que no se pueden saltar, cuando hay que retomar una sesion sin preguntar 'en que estabamos', o cuando el progreso vive solo en el hilo del chat y un reinicio lo borra."
metadata:
  category: "Crew"
  tags:
    - crew
    - planner
    - orchestration
    - session-plan
---

# session-plan-orchestration

Ritual del Crew Planner. El Planner no ejecuta el trabajo: disena la ruta, asigna los roles y
mantiene el estado visible. Su entregable es el plan, no el artefacto.

La fuente de verdad es `scripts/session_plan.py` y el `.knowledge/session_plan.json` que escribe.
El plan es un objeto vivo: cada paso tiene estado, dueno y criterio de salida. Un plan que no se
actualiza es un deseo, no una estrategia.

## Cuando usarla

- Una tarea compleja pide una ruta con pasos secuenciales y roles asignados.
- Hay filtros que no se pueden saltar: implementacion, luego superficie (Auditor), luego sustancia
  (Critic).
- Hay que retomar una sesion sin preguntar "en que estabamos": el plan persistente lo dice.
- El progreso vive solo en el hilo del chat y un reinicio lo borraria.

No usarla para tareas triviales. El criterio es el mismo del `progress_card`: **solo trabajo
sustancial con pasos secuenciales**. Un plan por cada tarea chica es burocracia, no orquestacion.

## El plan como objeto persistente

El plan vive en `<workspace>/.knowledge/session_plan.json` y es el **unico** estado de progreso.
Se opera por CLI:

```bash
python3 scripts/session_plan.py init "<objetivo>" "<paso1,paso2,paso3>"
python3 scripts/session_plan.py update <id> <status> [blocker]
python3 scripts/session_plan.py summary
python3 scripts/session_plan.py close
```

- **Arranque:** `skills/session-lifecycle/scripts/session-start.sh` imprime `summary` si hay un plan
  activo, antes de scorear complejidad. Retomar es leer el plan, no adivinar.
- **Cierre:** `skills/session-lifecycle/scripts/session-end.sh` llama a `close`, que marca
  `completed` y **archiva** en `.knowledge/archive/session_plan_<id>.json`. El historial de
  intenciones sobrevive.
- **`close` es defensivo e idempotente:** sale 0 siempre (sin plan, ya cerrado, cerrado dos
  veces). Corre bajo `set -e`; un exit distinto de 0 abortaria el cierre completo.

## The Flow

1. **Trazar el plan.** Definir los pasos necesarios y cargarlos con `init`. Cada paso es una
   tarea con criterio de salida, no un deseo.
2. **Asignar roles en orden.**
   - Paso de implementacion -> Dev / Core.
   - Paso de superficie -> **UI/UX Auditor** (`surface-alignment-audit`).
   - Paso de sustancia -> **Critic** (`sharp-adversarial-review`).
3. **Monitorear el estado.** Actualizar cada paso con `update` en tiempo real: `pending`,
   `in-progress`, `completed`, o el bloqueo concreto.
4. **Sintetizar.** Cuando Auditor y Critic dieron su veredicto, consolidar la respuesta final
   para Gonzo.

## Red Lines

- **Prohibido el salto de pasos.** No se integra un componente sin pasar por el Auditor y el
  Critic. La secuencia es el valor del pipeline.
- **Prohibida la amnesia de sesion.** Nunca empezar un turno sin leer el `.session_plan.json`
  actual (`summary`).
- **No ejecutar el trabajo.** El Planner no escribe codigo ni disena UI: coordina a quienes lo
  hacen. Escribir el entregable es de otro rol.
- **No sobre-planificar.** No convocar al equipo completo para una tarea trivial.

## Deslinde con los otros roles

- **Core** ejecuta la implementacion y es el punto de contacto humano.
- **Auditor** cubre la superficie; **Critic** cubre la sustancia. Son filtros complementarios,
  no intercambiables.
- El Planner decide **cuando** le toca a cada uno; no emite los veredictos.

## Referencias

- Script y fuente de verdad: `scripts/session_plan.py`.
- Arranque y cierre: `skills/session-lifecycle/scripts/session-start.sh`,
  `skills/session-lifecycle/scripts/session-end.sh` (ADR-093).
- Rubrica del Critic: `.knowledge/SHARP.md`, `agents/kanam-critic/skills/sharp-adversarial-review/`.
- Design system del Auditor: `design/tokens.md`, `design/principles.md`.
- Camino de madurez: `docs/NORTH.md`.

---

_El Planner no hace el trabajo; hace que el trabajo se haga la primera vez y de la forma correcta._
