---
name: "program-orchestration"
description: "Crear y mantener un plan de programa multi-sesion: pasos con dueno, rol, criterio de salida, dependencias y evidencia. Usar cuando el objetivo tiene 3+ pasos, 2+ roles, mas de una sesion o una fecha/bloqueo externo. No usar para tareas de una sola sesion."
metadata:
  category: "Crew"
  tags:
    - planner
    - program
    - orchestration
    - session-plan
user-invocable: false
---

# program-orchestration

Un **programa** es un objetivo que no cabe en una sesión ni en un solo rol. El Planner lo convierte en un objeto persistente: pasos, dueños, criterios de salida, dependencias y evidencia. El CORE ejecuta; el Planner mantiene el estado y decide qué sigue.

## Cuándo usarla

- El objetivo tiene **3+ pasos secuenciales**.
- Involucra **2+ roles** (Dev, Ops, Mind, Studio, Auditor, Critic).
- Atraviesa **más de una sesión**.
- Tiene una **fecha o un bloqueo externo** (CI, respuesta de terceros, deadline).

No usarla para una tarea de una sesión y un rol: eso lo resuelve el CORE con `session_plan.py`. Un programa por cada tarea chica es burocracia, no orquestación.

## Fuente de verdad

`agents/kanam-planner/.knowledge/programs/<slug>.json`

El plan de sesión del Planner (`.knowledge/session_plan.json`) es otra cosa: es el estado de **esta** sesión de trabajo. El programa es el estado del objetivo a través de varias sesiones.

## Comandos

```bash
# Crear
python3 scripts/program_plan.py init <slug> \
  --title "<titulo>" --objective "<objetivo>" --gates auditor,critic

# Agregar pasos
python3 scripts/program_plan.py add-step <slug> "<tarea>" \
  --role dev --exit "<criterio verificable>" [--depends 1,2] [--gate auditor|critic] \
  [--write-path "<path>"]

# Operar
python3 scripts/program_plan.py next <slug>
python3 scripts/program_plan.py brief [<slug>] [--all]
python3 scripts/program_plan.py status [<slug>] --json
python3 scripts/program_plan.py update <slug> <step> <status> \
  [--evidence "<evidencia>"] [--blocker "<bloqueo>"] [--session-ref "<key>"]
python3 scripts/program_plan.py board
python3 scripts/program_plan.py report --json
python3 scripts/program_plan.py close <slug>
```

## Estados

| Estado | Significado | Requisito |
|---|---|---|
| `pending` | Todavía no empezó | Dependencias pueden estar pendientes |
| `in-progress` | Alguien lo está haciendo | Dependencias completas |
| `review` | Espera veredicto de Auditor/Critic | `gate` explícito |
| `blocked` | No puede avanzar | `--blocker` obligatorio |
| `completed` | Terminó | `--evidence` obligatorio |
| `waived` | Se decidió no hacerlo | `--waiver-reason` |

## El flujo

1. **Intake.** Confirmar que el objetivo es programa. Si no, devolverlo al CORE.
2. **Init.** Crear el programa con título, objetivo y gates.
3. **Pasos.** Agregar pasos atómicos, cada uno con rol, dueño, criterio de salida y dependencias. Un paso es una unidad verificable, no una intención.
4. **Lint.** Correr `python3 scripts/plan_lint.py <slug>`. Sin lint verde no se dispatcha.
5. **Brief.** Entregar al CORE el brief y el próximo paso.
6. **Dispatch.** Generar el contrato con `dispatch_contract.py`. En Fase 1 el CORE es quien spawnea.
7. **Update.** Cada vez que un paso cambia, actualizar estado y evidencia. Si se bloquea, registrar el bloqueo exacto.
8. **Gates.** Auditor y Critic se registran como pasos con `gate`; su veredicto es evidencia, no opinión.
9. **Close.** Cerrar solo cuando todos los pasos están `completed` o `waived`. Si se fuerza, queda registrado `forced_close`.

## Reglas duras

- **Sin dueño no hay paso.** `owner` y `role` son obligatorios.
- **Sin criterio de salida no hay avance.** `exit_criteria` debe ser verificable por otra persona.
- **Sin evidencia no hay `completed`.** La evidencia es un comando, un path, un diff o una salida.
- **No se salta Auditor/Critic** cuando el programa los declara como gate.
- **No se duplica estado.** El programa vive en un solo JSON; `pipeline-track.sh` sigue siendo el estado intra-paso del pipeline A/B.
- **No se sobre-planifica.** Si el objetivo no cumple la definición de programa, no se crea.

## Referencias

- `scripts/program_plan.py` — CRUD, brief, status, lint, board, report.
- `scripts/plan_lint.py` — gate de validación.
- `scripts/dispatch_contract.py` — contrato de ejecución por paso.
- `CAPABILITIES.md` — definición de programa y catálogo de capacidades.
- `ROADMAP.md` — camino de madurez v0.2 → v0.5.

---

_El programa es el plano; el CORE es el constructor; el Planner es el inspector que no deja avanzar sin evidencia._
