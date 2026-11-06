---
name: "plan-review"
description: "Revisar programas activos y producir el brief semanal: progreso, bloqueos, pasos estancados y top 3 de la semana siguiente. Usar los viernes, al cerrar un programa o cuando Gonzo pide 'como venimos'."
metadata:
  category: "Crew"
  tags:
    - planner
    - review
    - weekly
    - metrics
user-invocable: false
---

# plan-review

El review no es un resumen de actividad: es una **decisión sobre qué sigue**. El Planner lee el estado real de los programas, detecta lo que se estancó y propone el próximo movimiento.

## Cuándo usarla

- Viernes 17:30 (automation semanal).
- Cierre de un programa.
- Gonzo pregunta "¿cómo venimos?" o "¿qué hacemos esta semana?".
- Un programa lleva más de 7 días sin un paso completado.

## Procedimiento

1. **Estado.** `python3 scripts/program_plan.py status --json`.
2. **Tablero.** `python3 scripts/program_plan.py board`.
3. **Alertas.** `python3 scripts/plan_report.py`.
4. **Leer los bloqueos.** Para cada paso `blocked`, confirmar que el `blocker` siga siendo real. Un bloqueo viejo que ya se resolvió es ruido.
5. **Detectar estancados.** Pasos `in-progress` o `review` con más de 7 días desde `updated_at`.
6. **Elegir top 3.** No más de tres outcomes para la semana siguiente. Cada uno con dueño y próximo paso.
7. **Escribir el brief.** Formato de 10 líneas:
   ```
   🗺️ Semana <fecha>
   1. <programa> — <próximo paso> (@owner)
   2. ...
   3. ...
   Bloqueos: <lista o "ninguno">
   Decisión: <qué necesita Gonzo, si algo>
   ```
8. **Publicar.** Telegram o webchat, según la automation. Si no hay nada que decir, no mandar ruido.

## Reglas

- **No confundir actividad con progreso.** Un paso `in-progress` hace 10 días no es avance; es un estancamiento.
- **No abrir programas nuevos en el review.** El review prioriza lo existente; lo nuevo entra por intake.
- **No cerrar un programa con pasos abiertos** salvo `--force` y con razón registrada.
- **No más de 3 outcomes.** Si hay 10, no hay prioridad.
- **Un bloqueo sin dueño de decisión no es un bloqueo:** es una pregunta para Gonzo.

## Métricas

| Métrica | De dónde sale |
|---|---|
| Programas activos | `program_plan.py status --json` |
| Pasos completados / totales | `status --json` |
| Bloqueos | `report` |
| Estancados | `status --json` (`stale_steps`) |
| Gates salteados | `plan_lint.py` |
| Throughput semanal | comparar `completed` entre reviews |

## Cierre de programa

Antes de cerrar:

1. `plan_lint.py <slug>` verde.
2. Todos los pasos `completed` o `waived` con razón.
3. Evidencia en cada paso completado.
4. `program_plan.py close <slug>`.
5. Registrar el aprendizaje en `docs/LEARNINGS.md` o el daily si hubo una corrección estructural.

## Referencias

- `scripts/program_plan.py` — status, board, report.
- `scripts/plan_report.py` — alertas.
- `skills/plan-playbooks/SKILL.md` — playbooks.

---

_El review no premia lo que se hizo: decide lo que sigue._
