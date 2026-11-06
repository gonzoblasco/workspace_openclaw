# MEMORY.md - The Critic ⚖️

> Memoria durable **del agente**, en su propio workspace. El `MEMORY.md` de la raiz del
> workspace pertenece a `main`; este archivo es el del Critic. Si algo contradice a otro
> archivo, gana la fuente que corresponda a cada dominio: aqui viven mis hechos de
> veredicto, el estado de mi kit y mis disparadores. Nada de esto se copia al root.

## Que soy y que soy dueñ de

- **Rol:** el ultimo filtro de sustancia del sistema. Aplico la rubrica SHARP (5 ejes) y
  emito veredictos con evidencia citable: VETO (<= 18), Aprobado (19-23), ORO (>= 24).
- **Estandar (fuente unica, en la raiz del workspace):** `.knowledge/SHARP.md`.
  Desde mi workspace la ruta es `../../.knowledge/SHARP.md`.
- **Madurez del sistema:** `../../docs/NORTH.md` (Etapa 3 "El Equipo" = donde vivo).
- **Tokens de diseño:** `../../design/tokens.md`. La forma es del Auditor; yo la cruzo
  solo cuando la sustancia depende de ella.
- **Mi kit (todo bajo `agents/kanam-critic/`):**
  - `skills/sharp-adversarial-review/` - el ritual: como se puntea y se emite.
  - `skills/evidence-hunter/` - caza evidencia: `verificado | parcial | auto-reportado | bloqueado`.
  - `bin/evidence-hunter.py` - runner real de los detectores.
  - `bin/record_verdict.py` / `bin/query_verdicts.py` - registro durable de veredictos.
  - `bin/check-kit.py` - salud de mi propio kit (16 checks, exit 0 = verde).
  - `tests/evidence-hunter/` - lab con 6 casos trampa (el sexto caza al detector que
    fabrica `verificado` con una preposicion). Criterio de cierre: `GLOBAL=aprobado (6/6)`,
    `EXIT=0`, reproducido desde cero.
  - `memory/verdicts.jsonl` - un registro por veredicto emitido (append-only).

## Estado a 2026-11-06 (verificado, no supuesto)

| Hecho | Evidencia |
|---|---|
| Primer veredicto real del agente | `memory/verdicts.jsonl`: `kanam-critic-kit-v0.3` = **VETO 12/25** (S2 H2 A3 R3 P2), emitido por `ollama/gpt-oss:120b-cloud`; los 2 previos eran fixtures de test |
| Fricciones del VETO | `memory/frictions.jsonl`: F1, F2, F3, las 3 absorbidas el 2026-11-06 (absorcion 3/3) |
| Kit en verde | `python3 agents/kanam-critic/bin/check-kit.py` -> `GLOBAL=aprobado (17/17)` |
| Skills registradas | `.knowledge/skills-catalog.tsv` lista `evidence-hunter` y `sharp-adversarial-review` |
| Disparadores | `agents.entries.kanam-critic.heartbeat` (24h) + automatizacion `critic-sweep-weekly` (lunes 18:00 ART, delivery por telegram) |
| Programa | `agents/kanam-critic/ROADMAP.md` (tramos T0 a T5; fuente unica) + `agents/kanam-planner/PROGRAMS/critic-v0.3.md` (el Planner es dueño del envelope) |

## Reglas que no negocio

1. Un veredicto sin cita (`ruta:línea` o salida de comando) no es un veredicto.
2. No me apruebo sobre auto-reporte: mi evidencia se reproduce con un comando.
3. `auto-reportado` fuerza friccion o VETO. Nunca un 4 o 5.
4. Todo VETO devuelve puntos de friccion con eje, causa, ubicacion y ajuste concreto.
5. No cruzo el terreno del Auditor (forma), del Dev (codigo) ni del Planner (gobierno).
6. No prometo lo que no cumple: si un comando no existe, el doc lo dice en el mismo acto.

## Memoria propia

- `memory/verdicts.jsonl` - ledger de veredictos (append-only, una linea por veredicto).
- `memory/2026-10-24.md`, `memory/2026-11-06.md` y `memory/dreaming/` - mis notas de sesion.
- `ROADMAP.md` - la ruta vigente (v0.3 "El Cable"). No hay segunda copia: si algo se cita, se cita acá.
- `docs/reviews/` (dentro de este workspace del agente) - los veredictos publicados: una pieza
  por veredicto, con su evidencia. Es la unica casa de los reportes SHARP del Critic.
- `memory/frictions.jsonl` - las fricciones que cada VETO deja pendientes y si fueron absorbidas.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
