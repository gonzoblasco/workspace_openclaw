# Adopción — CS50 AI with Python

**Pregunta:** ¿qué hacemos hoy mal en el workspace que este curso arregla?

**Regla:** un artefacto por curso. Lo demás queda como candidato, sin escribir.

---

## Fila adoptada

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| Un modelo se evalúa sobre datos que no vio; medir sobre los de entrenamiento es overfitting — "But the key idea is separating the training data from the testing data," (8:18:14) | Cada clase de `studies/` se verifica releyendo su propio `outline.md` contra su propio `transcripcion.md`. El mismo archivo es fuente y veredicto: si un timestamp está mal, la clase se autovalida igual. | `studies/cs50-ai-python/heldout.py` |

### Por qué esta y no otra

El curso entero es "fundamentos de IA" y la mayoría de sus ideas ya están cubiertas por skills del workspace:

- Búsqueda y heurísticas → cubierto por `complexity-driven-pipeline` (elegir profundidad de pipeline por T-score).
- Lógica e inferencia → cubierto por `check-single-source.py` (una regla, un dueño).
- Probabilidad y sampling → cubierto por `verification-gates` (un check es evidencia, no certeza).
- Backpropagation y gradient descent → cubierto por `post-task-reflection.sh` y `LEARNINGS.md`.
- Lenguaje y tokenización → cubierto por `memory-directory-organization` y la recuperación semántica.

La única idea que el workspace **no** tenía instrumentada es la evaluación en held-out aplicada a sus propios artefactos: el gate corre sobre el transcript, un archivo que el outline no usa para producirse. Ese es el corte entre "la clase se lee y parece buena" y "la clase se puede auditar".

### Cómo muerde

El script verifica dos cosas sobre el corpus, no sobre el outline:

1. **Cita literal y timestamp.** Cada cita `"..."` con `(h:mm:ss)` tiene que existir textualmente en el transcript, y el timestamp tiene que ser el inicio del bloque que la contiene.
2. **Recuperación.** Una frase del corpus tiene que devolver la clase, es decir, la clase tiene que estar efectivamente anclado a su fuente.

### Salida real (2026-11-11, este repositorio)

```
$ python3 studies/cs50-ai-python/heldout.py studies/cs50-ai-python/outline.md studies/cs50-ai-python/transcripcion.md
citas: 79 | verificadas: 79 | fallidas: 0
recuperación: frase de prueba presente en el corpus: OK
RESULTADO: PASA
EXIT=0
```

### El gate también falla cuando debe

Tres casos rotos a propósito, en `/tmp`, sobre la misma clase:

```
--- cita parafraseada ---
citas: 79 | verificadas: 78 | fallidas: 1
  FAIL cita no encontrada: 2:08:47 'And that is the notion of entailment, paraphrased.'
RESULTADO: FALLA
EXIT=1

--- timestamp desplazado (1:54:14 -> 1:50:00) ---
citas: 79 | verificadas: 78 | fallidas: 1
  FAIL timestamp fuera de su bloque: dice 1:50:00, el bloque empieza 1:54:14 (-254s): 'Inside of a knowledge base, so to speak, informati'
RESULTADO: FALLA
EXIT=1

--- archivo ausente ---
ERROR no se pudo leer nope.md: no existe
EXIT=3
```

El `3` no es verde: es "no se pudo correr", separado del `1` de "corrió y falló" (regla 1 de `verification-gates`). Un gate que da `0` cuando no encontró el archivo es peor que ninguno.

### Lo que encontró en esta misma clase

El gate rechazó **62 de 79 timestamps** en la primera pasada. Los tiempos se habían tomado de los bloques agrupados del transcript (bloques de ~18 s que empiezan donde arranca el primer cue *del bloque*), no del cue que contiene la cita: casi todos quedaban 3-20 s corridos. Se corrigieron reubicando cada cita contra el transcript, no a mano.

Eso es exactamente el overfitting que advierte el módulo: medir sobre la fuente de la que se escribió la clase deja pasar el error de conversión como si fuera contenido.

### Qué NO se adopta (candidatos, sin escribir)

- **A\\* y admisibilidad** como criterio para elegir herramienta en un agente. Idea buena, pero no hay un caso actual donde el workspace elija herramienta y pueda demostrar que se equivoca. Queda como idea hasta que exista el caso.
- **Arc consistency / AC-3** aplicado a los dominios de un gate. Suena elegante; en el workspace no hay dominios encadenados que justifiquen el costo. Sin artefacto.
- **Minimax / alpha-beta** para revisión A/B. El pipeline A/B ya tiene su criterio y no hay evidencia de que el árbol de revisión sea adversario. Sin artefacto.

Ninguno de los tres tiene hoy un caso donde el error ocurra y el artefacto falle; escribirlos sería resumir el curso disfrazado de gate.

---

## Cómo correrlo sobre otra clase

El script no depende de esta clase: funciona sobre cualquier `studies/<slug>/` que tenga `outline.md` y `transcripcion.md`.

```bash
python3 studies/cs50-ai-python/heldout.py studies/<slug>/outline.md studies/<slug>/transcripcion.md
```

No se promueve a skill todavía: primero tiene que sobrevivir a un uso real sobre otra clase. Cuando eso pase, se mueve a `scripts/` y se agrega al pre-commit.

### Uso real: corrido sobre las nueve clases del catálogo (2026-11-11)

Primera pasada, sobre `studies/`:

```
cs50-ai-python             PASA
rag-mcp-fundamentals       PASA
ai-agents-for-beginners    PASA
agentic-coding-codex       PASA
n8n-ai-automations         FALLA  (14 de 27 citas no existen literalmente en el transcript)
ai-engineer-full-course    FALLA  (41 de 41 citas apuntan a un cue posterior al que las contiene)
software-to-ai-engineer    no corrible: el outline cita sin timestamps
entrevistas-tecnicas       no corrible: el transcript no usa bloques con timestamp
```

Los dos fallos son reales y distintos:

- **`n8n-ai-automations`**: la mitad de las citas son paráfrasis escritas con comillas. El transcript dice «Check if it exists. Loop back. Fire another request» y el outline cita «check if it exists → loop back → fire another request → repeat until it's gone». Es exactamente el modo de error que el outline de esa clase advierte sobre el ASR, reproducido en su propio texto.
- **`ai-engineer-full-course`**: los 41 timestamps apuntan consistentemente ~14 s adelante del bloque que contiene la cita. No son citas inventadas: es un desfasaje sistemático de conversión, el mismo patrón que este gate encontró en su propia clase.

Los dos casos con `ERROR` también cuentan: un gate que devuelve verde cuando no pudo leer el formato es el `0` silencioso de `verification-gates`. Se reportan como `3`, nunca como `0`.

**Consecuencia:** el artefacto sobrevivió a un uso real (nueve clases, dos diagnósticos distintos, dos formatos no soportados detectados a tiempo). Cumple la condición para pasar a `scripts/check-study-citations.py` en el próximo cierre; esa promoción no se hace acá.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
