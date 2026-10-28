# Fixture de la cata de harnesses: la suite oculta y su validacion

**Que es esto:** la parte REUTILIZABLE de la cata de harnesses
(`docs/evaluacion/cata-harnesses-2026-10-27.md` y
`docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md`).

**Por que vive en el repo y no en `playground/`:** las corridas, los logs y los
entregables de la cata son efimeros (se regeneran corriendo el runner). Pero la
**suite oculta** -la verdad de base que decide el veredicto- no se regenera: sus
asserts fueron corregidos a mano dos veces, y corregir un assert sin poder
volver a validarlo es como volver a medir mal. Es la pieza que mas trabajo costo
y la que mas se pierde.

## Contenido

| Archivo | Que es |
|---|---|
| `tasks.json` | Las 3 tareas con su prompt, su corpus y sus **asserts ocultos**. |
| `suite.py` | El evaluador: corre los asserts contra un entregable. |
| `validate_suite.py` | La validacion en las DOS direcciones. |
| `reference/` | La respuesta correcta de cada tarea, escrita a mano. |
| `broken/` | La version deliberadamente defectuosa de cada tarea. |

## Uso

Validar que la suite sigue discriminando (debe dar 3/3 PASS la referencia y
0/3 PASS la defectuosa):

```bash
cd docs/evaluacion/cata-harnesses-fixture
python3 validate_suite.py
```

Evaluar un entregable nuevo contra los asserts:

```python
import sys
sys.path.insert(0, "docs/evaluacion/cata-harnesses-fixture")
from suite import eval_task
eval_task("T1", open("mi-entregable.md").read())
```

## La regla que este fixture existe para hacer cumplir

**Una suite que solo se probo en verde no se probo.** La validacion en las dos
direcciones es lo que atrapa los dos defectos PROPIOS que teve esta suite:

1. Un assert de T3 exigia que existiera un ADR con estado `Superseded`.
   **No existe ninguno** (los 60 estan en `Aceptado`/`Rechazado`; el ADR-067 esta
   `Aceptado`). Ese assert habria castigado la respuesta CORRECTA de Claude Code
   y de OpenHands, y habria hecho creer que el corpus de ADRs estaba roto.
2. Otro assert era tan laxo que la version defectuosa pasaba. Endurecido hasta
   que la discriminacion fue 3/3 vs 0/3.

Sin la validacion, la suite habria reportado un defecto inexistente - que es
exactamente el error que el skill de cata ya documenta en 2026-09-30.

## Advertencia sobre los asserts

La T3 exige que el informe diga explicitamente que **no hay ningun ADR
superseded**. Ese hecho **puede dejar de ser cierto** si en el futuro se agrega
un ADR superado. Cuando eso pase, el assert hay que revisarlo (no el
informe de los agentes): la verdad de base cambia y la suite tiene que reflejar
la realidad nueva.
