# Módulo 2 — Knowledge: clase

> Clase del **Módulo 2** de *Harvard CS50's AI with Python* (Brian Yu), armada sobre `studies/cs50-ai-python/`.
> Fuentes: el transcript (`transcripcion.md`, citas con t= verificados), mis conocimientos, y el código que corre en `knowledge/practica/`.
> Los ejercicios se hacen a medida que aparecen: cada sección tiene su script.

---

## 2.1 De "razonar" a un motor de inferencia (1:51:55)

El módulo arranca con tres hechos y ninguna computadora:

> "we now have three pieces of information now, three facts. Inside of a knowledge base, so to speak, information that we know." (1:54:14)

1. Harry visitó Hogwarts.
2. Harry visitó a Hagrid **o** a Dumbledore, pero no a los dos.
3. Harry **no** visitó a Hagrid.

Un humano concluye inmediatamente que visitó a Dumbledore. La pregunta del módulo es qué tiene que tener una máquina para llegar a la misma conclusión **sin que nadie se lo diga**.

Ese conjunto de oraciones tiene nombre: **knowledge base**. Y lo que se puede preguntar es qué se *sigue* de ella.

---

## 2.2 Los cinco conectivos y sus tablas

> "five of the most important, and the ones we're going to focus on today, are these five up here, each represented by a logical symbol." (1:57:49)

| Símbolo | Nombre | Se lee |
|---|---|---|
| `¬P` | negación | no P |
| `P ∧ Q` | conjunción | P y Q |
| `P ∨ Q` | disyunción | P o Q |
| `P → Q` | implicación | si P entonces Q |
| `P ↔ Q` | bicondicional | P si y solo si Q |

Y para cada uno, una tabla:

> "a table that demonstrates what this word not means when we attach it to a propositional symbol" (1:58:38)

### La tabla que todo el mundo cree saber y casi nadie tiene bien

`P → Q`:

| P | Q | P → Q |
|---|---|---|
| F | F | **V** |
| F | V | **V** |
| V | F | F |
| V | V | V |

**La implicación sólo es falsa en un caso.** Si el antecedente nunca se cumplió, la promesa sigue en pie. "Si llueve me mojo" no se rompe cuando no llueve.

No es una rareza lógica: es exactamente lo mismo que `¬P ∨ Q`. Y sin esa equivalencia **no se puede pasar a CNF** (sección 2.6).

---

## 2.3 Entailment: la definición exacta de "se sigue"

> "to use that information in the knowledge base to be able to draw conclusions about the rest of the world." (2:08:47)

**`KB ⊨ α`** se lee "KB implica α" y significa:

> En **todo modelo** donde KB es verdadera, α también lo es.

Un **modelo** es una asignación de verdad a cada símbolo:

> "a model just takes each of these two symbols and assigns a truth value to them, either true or false" (2:07:15)

**No hay ningún mundo posible** donde la base sea cierta y la consulta falsa. Esa es toda la definición. Nada de "se infiere por lógica intuitiva".

---

## 2.4 Model checking: la fuerza bruta correcta

> "How can we go about writing an algorithm that can look at this knowledge base and figure out whether or not this query alpha is actually true?" (2:14:26)

El algoritmo más simple:

1. Enumerar los `2ⁿ` modelos.
2. Quedarse con los que hacen **verdaderas todas** las oraciones de la KB.
3. Preguntar si α es verdadera en todos ellos.

**Correcto y completo.** Y con `n` símbolos, `2ⁿ` modelos.

| Símbolos | Modelos | Tiempo medido |
|---|---|---|
| 8 | 256 | 0,1 ms |
| 16 | 65.536 | 39 ms |
| 18 | 262.144 | 166 ms |
| 30 | ~1.000.000.000 | — |

La lógica sigue siendo correcta con 30 símbolos. El algoritmo ya es inútil. **Ese es el único motivo por el que existen las reglas de inferencia**: no cambian qué es verdad, cambian cuánto cuesta saberlo.

---

## 2.5 Reglas de inferencia: derivar sin enumerar

> "the idea of inference rules, some sort of rules that we can apply to take knowledge that already exists and translate it into new forms of knowledge." (2:56:26)

### Modus ponens

> "This inference rule is known as modus ponens" (2:57:16)

```
α → β
α
─────
β
```

Con `A→B`, `B→C`, `C→D`, `A` la cadena deriva D en **3 pasos**. El model checking revisa **16 modelos**. Y los números divergen: con 20 símbolos son **19 pasos** contra **1.048.576 modelos**.

| Cadena | Pasos (derivar) | Modelos (enumerar) |
|---|---|---|
| 2 | 1 | 4 |
| 8 | 7 | 256 |
| 16 | 15 | 65.536 |

**La segunda diferencia es la trazabilidad.** Derivar te dice *por qué* se sigue: cada hecho tiene un paso que lo justifica. Enumerar sólo te dice *que* se sigue.

### La regla que parece válida y no lo es

```
A → B
B
─────
A        ← INVÁLIDA (afirmar el consecuente)
```

De "si llueve me mojo" más "me mojé" **no** se sigue que llovió. Un motor que use esa regla deriva cualquier cosa.

---

## 2.6 Resolution: probar por contradicción

> "which is not the only way, but certainly one of the most common, which is known as resolution." (3:09:42)

Para probar `KB ⊨ α`, resolution prueba `KB ∧ ¬α` y busca una **contradicción**. Si la hay, α se sigue.

### El pipeline CNF (5 pasos)

1. **Eliminar bicondicionales:** `P ↔ Q` → `(P→Q) ∧ (Q→P)`
2. **Eliminar implicaciones:** `P → Q` → `¬P ∨ Q`
3. **Mover negaciones adentro:** De Morgan
4. **Distribuir:** `P ∧ (Q ∨ R)` → `(P∧Q) ∨ (P∧R)`
5. **Leer cláusulas:** cada disyunción del `∧` final es una cláusula

> "it gives us an ability to turn logic, any logical sentence, into something called conjunctive normal form." (3:14:57)

### La resolución

```
(A ∨ B)      (¬A ∨ C)
─────────────────────
      (B ∨ C)
```

Y si llegás a la cláusula vacía:

> "so I'm left with what we might call the empty clause. I'm left with nothing. And the empty clause is always false." (3:21:39)

### Lo que se aprende implementándolo

`p4_resolution.py` corre el caso `KB = {(A∨B), (¬A∨C), (¬B∨C)}`:

- **Consulta C:** 15 resoluciones, llega a la cláusula vacía → **se sigue**.
- **Consulta A:** se agotan todas las resolventes, **no** llega → **no se sigue**.

Y la lección del caso negativo es la que más cuesta ver: **la ausencia de la cláusula vacía ES la prueba.** No es que el motor "no llegó" — al saturar sin contradicción queda demostrado que existe un modelo donde la KB es cierta y A falsa.

**Truco que vale internalizar:** resolution es el A\* del Módulo 1. Se busca en el espacio de *pruebas*, no de estados del mundo, y como en A\*, el **orden** de las cláusulas decide cuánto cuesta.

---

## 2.7 Lógica de primer orden: escribir la regla una vez

> "known as first order logic, which is a little bit more powerful than propositional logic" (3:30:28)

El problema de Hogwarts: "cada persona está en una sola casa", con 4 personas y 4 casas.

**En proposicional**, generado:

- 4 × 4 = **16 símbolos** (`minerva_gryffindor`, `minerva_hufflepuff`, …)
- 4 oraciones "al menos una casa"
- 4 × 6 = 24 oraciones "a lo sumo una casa" (un par por vez)
- → **28 oraciones de restricción**

**En primer orden**, la misma restricción:

```
∀p. Persona(p) → (En(p,Gf) ∨ En(p,Hf) ∨ En(p,Rv) ∨ En(p,Sl))
∀p,h1,h2. En(p,h1) ∧ En(p,h2) ∧ h1≠h2 → ⊥
```

**Dos oraciones.**

> "We're going to have constant symbols that are going to represent objects like people or houses." (3:31:19)
> "Universal quantification lets me express an idea like something is going to be true for all values of a variable." (3:34:58)
> "In addition to universal quantification though, we also have existential quantification." (3:36:14)

### Por qué la compresión importa más de lo que parece

No es elegancia. Con 4 personas y 4 casas son 5,6× menos oraciones. Con 20 personas y 8 casas, la versión proposicional necesita 20 + 20×28 = **580** oraciones. La de primer orden sigue teniendo **dos**.

Y hay un argumento más fuerte: **escribir 580 oraciones a mano tiene tasa de error casi uno.** Si te olvidás el par (Minerva, Ravenclaw), queda un modelo espurio y el motor devuelve una conclusión falsa *con total confianza*. En primer orden la regla es una y no hay pares que olvidar.

---

## 2.8 La ingeniería del conocimiento: el trabajo real

> "this process of trying to take a problem and figure out what propositional symbols to use in order to encode that idea, or how to represent it logically, is known as knowledge engineering." (2:32:03)

El curso lo muestra con tres casos: **Clue**, **Mastermind** y **Hogwarts**.

La lección no es la lógica. Es que **elegir los símbolos es el trabajo**. Si los elegís mal, el motor no te salva: te da una respuesta correcta sobre el problema equivocado.

---

## Práctica del módulo

Seis scripts en `knowledge/practica/`, cada uno falla si su afirmación no se cumple. Gate: `python3 run_all.py`.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_conectivos.py` | Las 5 tablas se **generan**; 6 equivalencias se sostienen y 1 inválida se rechaza |
| 2 | `p2_model_checking.py` | Entailment = verdad en todos los modelos de la KB; el costo es `2ⁿ` |
| 3 | `p3_derivar.py` | Derivar y enumerar coinciden; la regla inválida deriva algo falso |
| 4 | `p4_resolution.py` | Resolution deriva la vacía sólo cuando hay contradicción |
| 5 | `p5_hogwarts.py` | Primer orden comprime 28→2 y la restricción realmente muerde |
| 6 | `p6_workspace.py` | Una implicación **no** se lee al revés |

Ver `practica-modulo-02.md` para la salida real de cada una.

---

## Preguntas para estudiar

1. `P → Q` es verdadera cuando P es falsa. ¿Por qué esa definición es la útil y no una "causal"? ¿Qué se rompería en CNF si fuera al revés?
2. Si `KB ⊨ α` y `KB ⊨ ¬α`, ¿qué significa eso sobre la KB? ¿Y qué se sigue de una KB así (ex falso quodlibet)?
3. Model checking es correcto y completo. ¿Qué exactamente gana resolution? ¿Qué pierde?
4. En resolution, ¿por qué hay que probar `KB ∧ ¬α` y no `KB ∧ α`? ¿Qué cambia en el significado de "llegar a la cláusula vacía"?
5. Con 4 personas y 4 casas, primer orden usa 2 reglas. ¿Qué pasa al añadir una casa nueva en cada versión?
6. La regla inválida de `p3` deriva A de `A→B, B`. Ese error tiene nombre. ¿Cuál es y dónde aparece en un repo de software?
7. **El gate como regla de inferencia:** cuando un check del pre-commit da verde, ¿qué se *deriva* exactamente? ¿Distingue entre "el archivo está bien" y "el check no cubre este caso"?
8. `p6` formaliza tres reglas de `AGENTS.md`. ¿Falta alguna que se use todos los días y no esté escrita? (Esa es la deuda de conocimiento del workspace.)

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 2 ≈ cues 458–730)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 2)
- Código: `studies/cs50-ai-python/knowledge/practica/`
- Proyectos del curso: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
