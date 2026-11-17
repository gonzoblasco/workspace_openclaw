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

## Estado a 2026-11-17 (verificado contra disco)

- `memory/verdicts.jsonl`: **6 veredictos validos con respaldo** y 2 anulados con motivo escrito.
  - `kanam-critic-kit-v0.3` = VETO 12/25 (primer juicio real)
  - `kanam-critic-kit-v0.3-r2` = ANULADO (16 etiquetado Aprobado + placeholders)
  - `kanam-critic-kit-v0.3-r3` = ANULADO (registrado sin reporte)
  - `kanam-critic-kit-v0.3-r4` = **Aprobado 19/25** (kit; vigente, F8 provisional por modelo)
  - `docs-ROADMAP-madurez` = VETO 15/25
  - `kanam-dev-ROADMAP` = VETO 16/25
  - `kanam-dev-inventario-skills` = VETO 15/25
  - `docs-NORTH` = VETO 17/25 (2026-11-16)
- `memory/frictions.jsonl`: **20 fricciones, 7 absorbidas (35%) y 13 abiertas**.
  Absorbidas: F1-F6, F8, F15. Abiertas: F7 y F9 (kit), F10-F14 (docs/ROADMAP), F16-F20 (docs/NORTH).
- Kit: `check-kit.py` = `GLOBAL=aprobado (18/18)` · Guard: `verify-verdict.py` = 6/6 valido, 2 anulados.
- Lab: `GLOBAL=aprobado (6/6)` con 6 casos trampa.
- Disparadores: heartbeat 24h del agente + `critic-sweep-weekly` (lunes 18:00 ART, delivery Telegram).
- Ruta: `ROADMAP.md` v0.3 (fuente unica). Programas: `agents/kanam-planner/PROGRAMS/critic-v0.3.md`.

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
