# Los gates y su tasa base (2026-11-12)

> Escrito al cerrar el curso CS50 AI completo. Cruza el Módulo 1 (heurística no
> admisible), el Módulo 3 (probabilidad condicional) y el Módulo 5 (evaluación en
> held-out) con el sustrato de verificación del workspace.

## El hallazgo

El workspace tiene **24 gates** en el pre-commit. **22 de ellos devuelven `0` y `1`,
pero no `3`**: no pueden declarar "no se pudo correr". La regla existe desde el
2026-09-28 en `skills/verification-gates` («cero casos corridos no es verde»), y el
gate de citas la cumple desde hoy. **Ningún gate la aplicaba a los gates.**

Cuando un check de estos no encuentra su archivo de entrada —o lo encuentra vacío
por un rename, un merge raro, un checkout parcial— el camino más probable es
devolver `0` con un mensaje de "OK". Verde sin haber mirado. Es exactamente la
forma del error que el curso enseñó tres veces:

| Módulo | Dónde aparece |
|---|---|
| 1 (Search) | A\* con heurística no admisible: devuelve un costo peor y se ve idéntico al óptimo |
| 3 (Uncertainty) | `P(bien\|pasa)` depende de la tasa base; un gate que nunca falló tiene posterior 1.0 por construcción |
| 5 (Learning) | Medir sobre train da accuracy 1.0 y no dice si generaliza |

Las tres son la misma cosa: **una medición que no puede fallar no mide nada.**

## Lo que se hizo con el curso

1. **`scripts/check-study-citations.py`** (promovido de `heldout.py`): 407 citas
   de 37 clases verificadas contra su transcript, `--fix` por tabla de offsets,
   en el pre-commit. **Es el único gate del catálogo que declara `3`.**
2. **`scripts/check-gate-honesty.py`**: revisa que cada `check-*.py` (a) declare
   `exit 3`, (b) resuelva la raíz sin depender del `cwd`, (c) reporte un veredicto
   legible. Hoy marca **21 de 25 sin `exit 3`**.
3. **`scripts/gate-base-rate.py`**: mide cuántos de los 18 gates del pre-commit
   tienen al menos un test con caso negativo. Hoy: **11 de 18**. Los otros siete
   nunca se vieron fallar. OJO: ese script NO es un gate bloqueante, y su
   fórmula no convierte "cuántos casos negativos" en una sensibilidad calibrada.
   La mide por un mapeo declarado y lo dice.

## Lo que queda (deuda real, no promesa)

- **21 gates sin `exit 3`.** `check-bootstrap-budget.py` y `check-single-source.py`
  ya lo tienen (los dos primeros, hechos hoy). Quedan 19, uno por uno: cada uno
  necesita decidir qué significa "no pude correr" *para él*, no un `return 3`
  cosmético.
- **7 gates sin test negativo.** El más caro de todos: `check-single-source.py`
  corre en cada commit y no tiene un caso que pruebe que detecta una segunda
  copia. Si se rompiera, nadie lo sabría.
- **`check-skill-overlap.py` tarda 9,65 s de los 10,44 s del pre-commit.** Lo
  demás tarda 0,8 s en total. Un gate que se paga en cada commit debería tener
  caché de embeddings; hoy re-embeddea el catálogo entero.

## La lección, en una línea

**Un gate que sólo puede decir "sí" no es un gate: es un adorno.** El curso lo
demostró con matemática; el workspace lo tiene como deuda medible.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
