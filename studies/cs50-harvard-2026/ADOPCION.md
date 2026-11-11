# ADOPCION — CS50 2026 en el workspace

Regla: el curso tiene que morder. Una fila por idea que toca algo que hoy hacemos mal, con un artefacto que falla cuando el error ocurre. Si no hay problema real, no se adoptó.

## Tabla

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| **Un LLM responde con seguridad y sin evidencia; la alucinación es un problema de producto, no solo de modelo.** «we'll call lastly hallucinations» (18:50:34) | El workspace ya tiene gates de citas para `studies/`, pero **no para lo que un LLM escribe en docs y ADRs**. ADR, HANDOFF y STATUS pueden afirmar un hecho sin fuente y nada falla. Es el error que el propio AGENTS.md documenta dos veces el 2026-10-27. | `scripts/check-unsourced-claims.py` — marca afirmaciones cuantitativas (porcentajes, tiempos medidos, conteos, versiones) en `docs/adr/`, `.knowledge/*/HANDOFF.md` y `docs/STATUS*` que no tengan ni fuente ni marca `<!-- sin-verificar -->`. Corrido abajo contra el repo actual. |
| **Una app de Flask sin CSRF y sin validación server-side es una demo, no un producto.** «planting a cookie on your computer» (23:12:36), inyección SQL (17:47:28) | No hay ningún proyecto propio con Flask, así que no hay deuda real que arreglar. | Descartada: no hay problema real. Candidata si algún día un proyecto propio usa Flask. |
| **SQL declarativo: el índice decide el plan, no la intención.** «to use what's called big O notation» (07:22:14) | Los queries de `memory/memory.db` no se miran con `EXPLAIN QUERY PLAN`. | No se adopta ahora: la DB tiene miles de filas y ningún query medido como lento. Es optimización preventiva, no un error actual. Candidata. |
| **Todo es un array de bytes: leer un formato a mano fuerza a entenderlo.** «how do I index into the array at» (05:45:48) | - | Descartada: es un ejercicio de estudio, no un cambio de práctica. Iría a `studies/cs50-harvard-2026/` como ejercicio de la Unidad 4. |

**Adopción de la primera pasada: una sola, la de citas.** Las otras tres se descartan o quedan como candidatas explícitas; escribirlas sería resumir el curso disfrazado de práctica.

## El artefacto: `scripts/check-unsourced-claims.py`

La pregunta que responde: *¿algún documento de gobierno del workspace afirma un número sin que se pueda rastrear de dónde salió?*

Es la versión ejecutable de la regla de §0 de AGENTS.md («verificar la palabra de Gonzo contra el repo») y del corolario de verificación antes de reportar. La idea viene del curso por oposición: Malan construye la clase sobre "cada vez que copiás y pegás debería darte mala espina" (16:33, en la unidad de SQL) y cierra con las alucinaciones. El workspace hace lo contrario con los números que escribe un modelo.

Diseño conservador a propósito: solo señala afirmaciones de **magnitud** (porcentaje, milisegundos, segundos, MB, unidades, versiones, "N de M"), y solo cuando la línea no tiene `· fuente`, un link, un backtick de comando, o la marca `<!-- sin-verificar -->`. Un falso positivo es barato (se anota la fuente); un falso negativo es la deuda que el doctor perdió en el 2026-10-27.

## Salida real (corrida en el workspace, 2026-11-11)

```
$ python3 scripts/check-unsourced-claims.py
...
check-unsourced-claims: 69 files, 46 unsourced magnitude claims
EXIT=1
```

Primera corrida sobre el corpus real: **69 archivos, 46 cifras sin fuente**. No es ruido generado por el gate - es deuda que estaba ahí y nadie veía. Los casos más honestos:

- `docs/adr/ADR-105:97` — «rework ... +50% de recall»: una cifra de una medición que no tiene el número pegado al lado. Es exactamente el patrón que el gate caza.
- `docs/adr/ADR-108:26` — «El 61% de la DB es un índice derivado»: correcto y verificable, pero el ADR no dice con qué comando se miró. Un lector no puede repetirlo.
- `docs/adr/ADR-102:204` — «0,33% de quemados»: el número que sostuvo la decisión de archivar minimax del CORE, sin el query que lo produjo.

El gate no dice que las cifras estén mal; dice que **no se puede rastrear de dónde salieron**. Son dos cosas distintas y la segunda es la que se arregla con un backtick.

**Qué NO hace todavía:** no está en el pre-commit ni en CI. La primera pasada del curso deja un artefacto que corre a mano (es lo que la regla pide); engancharlo al pre-commit es un paso aparte, con la decisión de si el corpus viejo se anota o se exime con `<!-- sin-verificar -->`. Si se engancha hoy, bloquea todo commit hasta sanear 46 líneas: eso es un programa, no un patch.

## Uso siguiente

```bash
python3 scripts/check-unsourced-claims.py            # repo actual
python3 scripts/check-unsourced-claims.py --help     # no implementado todavía
```

Para sanear una línea: pegar el comando que produjo el número (`` `sqlite3 memory.db "..."` ``), o marcar `<!-- sin-verificar -->` si es una estimación y se sabe.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
