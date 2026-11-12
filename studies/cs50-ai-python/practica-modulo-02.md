# Práctica del Módulo 2 — Knowledge

> Las preguntas del Módulo 2, **corridas**. Cada script afirma una propiedad y falla si no se cumple.
> Gate del módulo: `python3 run_all.py` → 6 de 6.

```
PASA   p1_conectivos.py       las 5 tablas se generan y las 6 equivalencias se verifican
PASA   p2_model_checking.py   entailment = verdad en todos los modelos de la KB
PASA   p3_derivar.py          derivar y enumerar coinciden; la regla inválida no
PASA   p4_resolution.py       resolución deriva la vacía solo cuando hay contradicción
PASA   p5_hogwarts.py         primer orden comprime y la restricción muerde
PASA   p6_workspace.py        una implicación no se lee al revés

RESULTADO: PASA (6 de 6)
```

---

## 1. Los conectivos: tablas generadas, no copiadas

La tabla de `→` sale de `¬P ∨ Q`, no de una tabla transcrita a mano:

```
  P Q | P -> Q
  F F | T
  F T | T
  T F | F
  T T | T
```

Y las equivalencias, verificadas fila por fila:

```
  OK   Implicación:      P->Q  ==  (not P) or Q
  OK   Contrapositiva:   P->Q  ==  (not Q)->(not P)
  OK   De Morgan and:    not(P and Q) == (not P) or (not Q)
  OK   De Morgan or:     not(P or Q)  == (not P) and (not Q)
  OK   Distributiva:     P and (Q or R) == (P and Q) or (P and R)
  OK   Bicondicional:    P<->Q  ==  (P->Q) and (Q->P)

  FALLA Contrapositiva INVÁLIDA: P->Q  ==  Q->P   (debe FALLAR)
```

**Lo que se aprende del último renglón:** el verificador tiene que poder fallar. Una batería de equivalencias que sólo dice "OK" no prueba nada — hay que meterle una falsa y comprobar que la rechaza.

---

## 2. Model checking: la definición, ejecutada

```
KB:
  1. Harry visitó Hogwarts
  2. Harry visitó a Hagrid o a Dumbledore, pero no a los dos
  3. Harry NO visitó a Hagrid

Consulta: ¿visitó a Dumbledore?

  modelos totales (2^n): 8
  modelos donde la KB es verdadera: 1
  ¿KB ⊨ Dumbledore? sí — en TODOS los modelos de la KB es verdadera

    contraejemplo: {'Dumbledore': True, 'Hagrid': False, 'Hogwarts': True, 'Snape': False}
  ¿KB ⊨ Snape? no — hay modelos de la KB donde Snape es falso
```

Ocho modelos, uno solo sobrevive a los tres hechos. `KB ⊨ Dumbledore` no es una intuición: es que **no existe** un modelo de la KB donde Dumbledore sea falso.

Y el costo, medido:

```
  símbolos   modelos      tiempo
  8          256               0.1 ms
  12         4096              2.3 ms
  16         65536          39.4 ms
  18         262144        166.2 ms
```

---

## 3. Derivar vs enumerar

```
KB:  A->B,  B->C,  C->D,  A

  DERIVAR (modus ponens encadenado):
    hechos nuevos derivados: 3
    trazabilidad: cada hecho nuevo tiene un paso que lo justifica

  ENUMERAR (model checking):
    modelos revisados: 16
    trazabilidad: ninguna. Sabés que se sigue, no por qué

  OK  Los dos caminos dan el mismo resultado.

=== Con una KB larga ===
  cadena     pasos (derivar)      modelos (enumerar)
  2          1                    4
  8          7                    256
  16         15                   65536
```

Lineal contra exponencial. Con 20 símbolos: **19 pasos** contra **1.048.576 modelos**.

### La trampa

```
  Afirmar el consecuente:  A->B , B  ⊢  A

  con la regla inválida se derivaría: A   (deriva)
  ¿A se sigue de verdad? NO
```

De "si llueve me mojo" más "me mojé" **no** se sigue "llovió". Un motor con esa regla deriva cualquier cosa.

---

## 4. Resolution: la cláusula vacía

```
=== Caso 1: KB ⊨ C  (sí se sigue) ===
  Cláusulas: ['{A, B}', '{C, no A}', '{C, no B}', '{no C}']
    paso 1: {A, B} + {C, no A} => {B, C}
    ...
    paso 15: {no C} + {C} => CLÁUSULA VACÍA
  derivó la cláusula vacía: True  (15 resoluciones)

=== Caso 2: KB ⊨ A  (NO se sigue) ===
  derivó la cláusula vacía: False  (17 resoluciones)
```

**El caso 2 es el que enseña.** No se deriva la vacía después de saturar: eso **es** la prueba de que no hay contradicción, y por lo tanto de que existe un modelo donde la KB vale y A no.

Y el pipeline CNF, paso a paso:

```
  original:      A <-> B
  sin iff:       ((A -> B) and (B -> A))
  sin imp:       ((no A or B) and (no B or A))
  CNF:           ((no A or B) and (no B or A))
```

### El bug que apareció escribiéndolo

La primera versión contaba **29** resoluciones en vez de 15. No era lento: estaba probando pares de cláusulas viejas una y otra vez. Saturation sin memoria de pares ya probados infla el contador y hace creer que el algoritmo es más caro de lo que es.

Y la primera versión de `clauses()` **fallaba** con `¬C` porque esperaba que todo viniera envuelto en un `AND`. Un único literal *es* CNF de una cláusula. Lo importante: el `assert` lo agarró antes de dar un resultado incorrecto — el mismo patrón que un gate que falla en vez de dar verde.

---

## 5. Hogwarts: 28 oraciones contra 2

```
  personas: 4   casas: 4
  proposicional: 16 símbolos, 28 oraciones de restricción
  primer orden:  5 oraciones en total
  factor de compresión: 5.6x

  Proposicional (restricciones generadas):
    (minerva_gryffindor ∨ minerva_hufflepuff ∨ minerva_ravenclaw ∨ minerva_slytherin)
    ...
    ¬(minerva_gryffindor ∧ minerva_hufflepuff)
    ... y 25 más

  Primer orden:
    ∀p. Persona(p) → (En(p,Gf) ∨ En(p,Hf) ∨ En(p,Rv) ∨ En(p,Sl))
    ∀p,h1,h2. En(p,h1) ∧ En(p,h2) ∧ h1≠h2 → ⊥
```

Y la verificación de que la restricción **muerde**:

```
  modelos totales: 65536 (2^16)
  modelos que satisfacen la KB: 4
  casas compatibles con la KB para Severus: las 4
  -> las 4 son compatibles y ninguna se sigue: la KB NO decide dónde está
     Severus, sólo que no puede estar en dos casas a la vez.
```

**16 símbolos → 65.536 modelos → 4 modelos válidos.** Eso es la restricción trabajando: sin ella habría 4^4 = 256 combinaciones posibles.

Y el argumento que importa: escribir 28 oraciones a mano tiene tasa de error humana casi uno. Olvidarse el par (Minerva, Ravenclaw) deja un modelo espurio y el motor devuelve una conclusión falsa **con total confianza**.

---

## 6. La KB del workspace: la implicación no se lee al revés

Formalizando tres reglas de `AGENTS.md`:

```
  A1  operacion_externa -> push_sin_ok
  A2  (git_add_A and multi_sesion) -> commit_firma_ajena
  A3  infra -> restart_gateway

afirmación                                                     deriva   correcto
git add -A con otra sesión viva implica commit que firma ajeno sí       OK
git add -A solo (sin otra sesión) implica commit que firma ajeno no       OK
una operación externa implica push sin OK                      sí       OK
un push sin OK implica que hubo operación externa              no       OK
infra implica restart de gateway                                sí       OK
un restart de gateway implica que había infra                   no       OK
```

**Tres "sí" y tres "no" — y los "no" son los que importan.**

`operacion_externa → push_sin_ok` no dice que todo push sin OK sea una operación externa. Afirmar el consecuente es la misma regla inválida de la práctica 3. Un gate que verificara *"hay push sin OK, entonces hubo operación externa"* estaría dando por buena una causa que la regla no sostiene.

Y **A2** tiene la forma correcta para gatear: la conjunción es necesaria. `git add -A` solo no implica nada; la regla aplica con otra sesión viva. Un check que se dispare con una sola condición está afirmando una regla que no existe.

### Un tropiezo que enseña

La primera versión usaba la consistencia como precondición del entailment. **Estaba mal, y el error es del módulo:** de una KB inconsistente se sigue *cualquier cosa* (ex falso quodlibet). Filtrar por consistencia no protege de nada — si lo que querés es eso, ya estás en el caso donde todo se deriva.

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| `P→Q` es "si P entonces Q" | Sólo es falsa en `V→F`. Es `¬P∨Q`, y sin eso no hay CNF |
| "Se sigue lógicamente" | En **todos** los modelos de la KB. Ocho modelos, uno sobrevive |
| Model checking resuelve el problema | Con 30 símbolos son mil millones de modelos |
| Inferir es más rápido | Y además deja rastro: cada hecho tiene su paso |
| Resolution busca afirmaciones | Busca contradicciones. Si no la encuentra, **eso** es la prueba |
| Primer orden es "más expresivo" | Es más expresivo **porque no tenés que escribir cada par** |
| Una implicación dice lo mismo al revés | Sólo la mitad de la tabla de `p6` deriva, y las otras tres son el error |
| Un `assert` es un detalle de implementación | En `p4` fue lo que evitó una conclusión incorrecta |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/knowledge/practica
python3 run_all.py                # las 6, con veredicto
python3 p4_resolution.py          # el caso positivo y el negativo
python3 p6_workspace.py           # las reglas del repo como axiomas
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
