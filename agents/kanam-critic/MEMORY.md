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
  - `bin/record_verdict.py` - registro directo (deprecated en favor de `emit-verdict.py`).
  - `bin/emit-verdict.py` - la UNICA via de registro: valida el reporte ANTES de tocar el ledger.
  - `bin/verify-verdict.py` - un veredicto no existe sin fila + reporte + 5 citas.
  - `bin/invalidate-verdict.py` - retira un veredicto dejando el motivo escrito.
  - `bin/query_verdicts.py` - lista veredictos (los anulados aparecen como ANULADO).
  - `bin/check-kit.py` - salud de mi propio kit (18 checks, exit 0 = verde).
  - `tests/evidence-hunter/` - lab con 6 casos trampa. Criterio de cierre: `GLOBAL=aprobado (6/6)`, `EXIT=0`, reproducido desde cero.
  - `memory/verdicts.jsonl` - un registro por veredicto emitido (append-only).
  - `memory/frictions.jsonl` - fricciones que cada VETO deja y si fueron absorbidas.
  - `LEARNINGS.md` - habilidad calibrada que sobrevive los VETOs.

## Decisión 7 (2026-11-06, sin costo): el juez provisional

- El rolet declara `gpt-oss:120b-cloud` como primario (ADR-090); el free plan solo tiene
  `minimax-m3.1-flash:cloud`. Durante el free plan, los veredictos se emiten con el modelo
  disponible y se marcan `provisional` en la nota. Cuando vuelva `gpt-oss`, se REEMITEN y
  se actualiza la friccion F8.
- Nada de esto toca `docs/ROADMAP.md` ni otros wedos: la decision vive aca y en F8 del ledger.

## Estado a 2026-11-07 (verificado, no supuesto)

- `memory/verdicts.jsonl` tiene **3 veredictos validos** y **2 anulados con motivo escrito**:
  - `kanam-critic-kit-v0.3` = VETO 12/25 (primer juicio real)
  - `kanam-critic-kit-v0.3-r2` = ANULADO (etiquetado "Aprobado" sobre 16; placeholders sin ejecutar)
  - `kanam-critic-kit-v0.3-r3` = ANULADO (registrado sin reporte)
  - `kanam-critic-kit-v0.3-r4` = **Aprobado 19/25** (kit vigente; emitido por minimax-m3.1-flash, vigente, F8 provisional)
  - `docs-ROADMAP-madurez` = **VETO 15/25** (trabajo ajeno, 5 fricciones F10-F14, elegido por Gonzo)
- Fricciones: 14 registradas, 7 absorbidas (F1-F6, F8 por decision), 7 abiertas
  (F7 scripts, F9 tasa, F10-F14 sobre docs/ROADMAP.md, F15 el bug del barrido).
- Lab: `GLOBAL=aprobado (6/6)`.
- Kit: `GLOBAL=aprobado (18/18)`.
- Disparadores: heartbeat 24h + automatizacion `critic-sweep-weekly` (lunes 18:00 ART), delivery Telegram.
- Programa: `agents/kanam-critic/ROADMAP.md` (fuente unica, tramos T0 a T5); el Planner es dueno del envelope en `agents/kanam-planner/PROGRAMS/critic-v0.3.md`.

## Que toco y con quien no me meto

- El lado del CORE. `docs/ROADMAP.md`, `docs/NORTH.md` y `docs/ROADMAPS.md` son suyos. Yo mido y
  devuelvo fricciones; la edicion la hace el CORE.
- El lado del Planner. El envelope es de él; acá solo propongo y registro.

## Memoria propia

- `memory/verdicts.jsonl` - ledger de veredictos (append-only, una linea por veredicto).
- `memory/2026-11-06.md` - narrativa del turno.
- `memory/2026-11-07.md` - este turno (por crear).
- `memory/frictions.jsonl` - fricciones por VETO.
- `ROADMAP.md` - la ruta vigente (v0.3 "El Cable"). No hay segunda copia.
- `docs/reviews/` (dentro de este workspace del agente) - los veredictos publicados.
- `LEARNINGS.md` - habilidad calibrada que sobrevive los VETOs.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
