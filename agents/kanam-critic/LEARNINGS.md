# LEARNINGS.md - The Critic ⚖️

> Lo que mis veredictos me enseñaron, además de la línea por eje. La rúbrica
> (`.knowledge/SHARP.md`) es el estándar; este archivo es el **termómetro**: la
> habilidad calibrateda que queda cuando el score se paga.
>
> Fuente de verdad viva: `memory/verdicts.jsonl` (append-only) y `memory/frictions.jsonl`.
> Este doc es el resumen **legible** que puede promocionarse a tabla en la DB
> (schema propuesto en `## Schema para DB`).
>
> Regla: un patrón entra acá solo si tuvo lugar en **al menos 1 veredicto real** o en
> **un falso verde detectado**. Hitos de diseño sin evidencia no entran.

---

## Ejes que se movieron en el turno (2026-11-06)

| Eje | Antes | Después | Qué lo movió |
|---|---|---|---|
| S - Sharpness | 4 | 4 | El formateo del ritual se volvió consistente; el lab cerrado lo mantiene arriba. |
| H - Horizon | 3 | 4 | El kit tiene la vara + el kilo leve (veredictos reales, barrido weekly). |
| A - Asymmetry | 4 | 4 | El lab y los 4 scripts de control pagaron el costo inicial (ahora deuda F7). |
| R - Resistance | 3 | 4 | por verificar: el kit aún corre en `minimax-m3.1-flash`; el guard `verify-verdict.py` es un check nuevo. |
| P - Parsimony | 4 | 3 | El churn por rutas duplicadas y la consolidación pendiente de 4 scripts. |

## Patrones observados

1. **"Un veredicto reportado y no registrado es un veredicto que no existe."**
   Tuvo lugar en F4/F5 (2026-11-06 18:25 ART). Genera una regla que ya no es
   una instrucción sino un check: `bin/emit-verdict.py` (valida reporte ANTES de
   tocar el ledger) + `bin/verify-verdict.py` (gate final).
2. **"El detector que busca tokens no puede inventarse el token."**
   Tuvo lugar en el caso 6 del lab (token malinterpretado). Un verbo sin evidencia
   fabricada es un VETO disfrazado de verde.
3. **"Auto-reportado = fricción o VETO, nunca 4 ni 5."**
   Reafirmado con F2 ("archivos sin versionar"): pasaron del check fallido a ser el
   primer VETO real. La bara se mantiene con evidencia, no con esfuerzo.

## Frases que merecen no perderse

- "Un guard que no escribe no es un guard."
- "La tasa de absorción medida con auto-corrección es la métrica más fácil del mundo."
- "Si el número amarrado desaparece, el mapa ya mintió."

## Fricciones que quedan abiertas (dueño, no fecha)

- **F7 - Parsimony:** consolidar 4 scripts en un CLI con subcomandos.
  Propiedad: Crític.
- **F8 - Resistance:** modelo del juez (`minimax-m3.1-flash` vs `gpt-oss:120b-cloud`).
  Propiedad: Gonzo (decisión) + Kanam CORE (config).
- **F9 - Asymmetry:** medir 3 VETOs sobre trabajo *ajeno* antes de publicar tasa.
  Propiedad: Critic + CORE.
- **F10-F14** (sobre `docs/ROADMAP.md`): gate de contenido, números stale, Crew ausente.
  Propiedad: CORE (editor del doc) + Critic (auditor).

## Schema para DB (cuando se promocionan)

```sql
CREATE TABLE learnings (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  outcome TEXT CHECK (outcome IN ('veto','approved','oro')) NOT NULL,
  artifact TEXT NOT NULL,
  axis TEXT NOT NULL CHECK (axis IN ('S','H','A','R','P')),
  friction_id TEXT REFERENCES frictions(friction_id),
  pattern TEXT NOT NULL,
  evidence TEXT NOT NULL
);
```

Promociona cada `LEARNINGS.md` a la DB con `memory-db.sh promote-learnings` (pendiente,
ver todo abierto).

## Notas de estilo

- Este archivo **no** repite `MEMORY.md`. MEMORY.md es el estado y este es la
  habilidad calibrada que sobrevivió los VETOs.
- Si un patrón se marca como absorbing en `frictions.jsonl`, aquí va con una sola
  línea; la evidencia vive en el ledger, no acá.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
