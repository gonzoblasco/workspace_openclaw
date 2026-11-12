# HANDOFF — CS50 2026

## Qué es
Clase de estudio de **Harvard CS50 (2026)** (freeCodeCamp.org, David J. Malan, 24:29:14, CC BY-NC-SA 4.0). Fuente: `https://www.youtube.com/watch?v=gmuTjeQUbTM`.

## Estructura

| Ruta | Qué tiene |
|---|---|
| `outline.md` | Mapa del curso: 11 unidades 1:1 con los capítulos oficiales, 44 citas verificadas, lo que el curso no cubre. |
| `transcripcion.md` | 40.533 cues con timestamp, ~290.000 palabras, glosario de errores del ASR. |
| `lecciones/unidad-NN.md` | La unidad **trabajada**: teoría propia, ejercicios, ancla al repo, huecos. |
| `practicas/uNN/` | Scripts ejecutables + suite de tests. |
| `ADOPCION.md` | Gate `scripts/check-unsourced-claims.py`, corrido contra el corpus. |
| `video-meta.json` | Metadata y cobertura del transcript. |

## Estado actual (2026-11-11)

- **U0 cerrada.** `lecciones/unidad-00.md` + `practicas/u00/` (5 scripts, suite de 18 checks, **0 fallos**).
- **Próxima: U1 (C).** La lección todavía no está escrita.

## Bloqueante para U1

Hay que resolver el entorno **antes** de arrancar:

- `clang` y `make`: `xcode-select --install`.
- **`valgrind` no corre en Apple Silicon.** Alternativas: `-fsanitize=address` (nativo) o Docker `cs50/cli` (el entorno oficial del curso).

Sin esto tampoco hay U4 (Memory), que es la unidad donde `valgrind` importa de verdad.

## Cómo se estudia acá

1. Leer `lecciones/unidad-NN.md`.
2. Correr los scripts de `practicas/uNN/` y **leer la salida**, no solo el OK.
3. La suite tiene que incluir una implementación **rota a propósito** que falle. Si el roto ordena, el test dejó de probar algo.
4. Actualizar el checklist de la lección y `lecciones/README.md`.

## Deuda declarada

- `scripts/check-unsourced-claims.py` **no está en el pre-commit**: engancharlo hoy bloquea todo commit hasta sanear 46 líneas de `docs/adr/`. Es un programa aparte.
- Los ejercicios son derivados, no los problem sets oficiales de `cs50.harvard.edu/x`.

## Cómo continuar

1. Leer este HANDOFF.
2. Leer `memory/2026-11-11.md` para el informe completo.
3. Verificar el estado real antes de actuar (git, `python3 test_practicas.py`).

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
