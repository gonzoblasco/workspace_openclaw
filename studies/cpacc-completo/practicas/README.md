# Prácticas del curso CPACC

Cada práctica es un artefacto **ejecutable**, no una hoja en markdown: script + tests + el
ejercicio escrito sobre un caso real. El molde se repite porque el objetivo de fondo es construir
skills, scripts y workflows a11y, y para eso hace falta práctica con forma de herramienta.

| # | Práctica | Qué ejercita | Artefacto |
|---|---|---|---|
| 01 | [`01-modelos/`](01-modelos/) | Los 7 modelos de discapacidad (BoK 1A) | `modelos.py` + 11 tests + caso real (astryx #5419) |

## El molde

1. **Datos en un catálogo**, con el nombre oficial del BoK y sus fortalezas/debilidades.
2. **CLI** que recibe un caso concreto, nunca un tema genérico.
3. **Tests que prueban de verdad**: que estén los siete, que ninguno esté incompleto, que el CLI
   devuelva los códigos correctos, que el caso no se pierda.
4. **El ejercicio escrito** sobre un caso propio, con lo que el lente enseñó y lo que no.

## Regla

Un test que no puede fallar no es un test. Si al escribir la primera versión todos pasan de una,
falta un test.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
