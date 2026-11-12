# Práctica del Módulo 3 — Uncertainty

> Las preguntas del Módulo 3, **corridas**. Sin numpy ni scipy: librería estándar.
> Gate: `python3 run_all.py` → 6 de 6.

```
PASA   p1_probabilidad.py     tres identidades verificadas por simulación
PASA   p2_red_bayesiana.py    la factorización coincide y ahorra exponencial
PASA   p3_enumeracion.py      P(R|W) exacta y distinta de P(W|R)
PASA   p4_sampling.py         likelihood weighting usa todas las muestras
PASA   p5_hmm.py              el filtrado recursivo coincide con la fuerza bruta
PASA   p6_gate_bayes.py       un verde no vale nada sin tasa base

RESULTADO: PASA (6 de 6)
```

---

## 1. Las identidades, verificadas por simulación

200.000 mundos generados, y las tres reglas chequeadas contra las frecuencias:

```
  P(R)         0.3014   ok
  P(W)         0.4118   ok
  P(R|W)       0.6596   ok
  P(W|R)       0.9014   ok

  Regla del producto: P(R y W) = 0.2716 = P(R) * P(W|R)   ok
  Bayes:              P(W|R)*P(R)/P(W) = 0.6596 = P(R|W)  ok
```

**Y el punto que rompe la intuición:**

```
    P(W|R) = 0.9014   (si llueve, casi seguro me mojo)
    P(R|W) = 0.6596   (si me mojé, ¿llovió?)
```

Son distintos. Llover es raro (30%), así que la mayoría de las veces que te mojaste no había llovido. **Ese es el error de tasa base.**

---

## 2. La red bayesiana: la estructura es el cálculo

Tres nodos: `lluvia → mojado`, `lluvia → resbalón`. La conjunta completa, generada:

```
  R   W   S   P(R,W,S)
  T   T   T   0.2160
  T   T   F   0.0540
  T   F   T   0.0240
  T   F   F   0.0060
  F   T   T   0.0140
  F   T   F   0.1260
  F   F   T   0.0560
  F   F   F   0.5040
  suma = 1.0000  ok
```

Y la factorización coincide exactamente:

```
  P(R=T, W=T, S=T) = P(R) * P(W|R) * P(S|R)
    R=0.30 * W=0.90 * S=0.80 = 0.2160
```

**El conteo, que es el argumento del módulo:**

```
  variables    conjunta 2^n       cadena con 1 padre   factor
  3            8                  7                        1x
  5            32                 13                       2x
  10           1024               28                       37x
  20           1048576            58                       18079x
  30           1073741824         88                       12201612x
```

Y el límite, que hay que decir:

> **Un nodo con 20 padres tiene una tabla local de `2²⁰` filas.** La factorización no elimina el exponencial: lo mueve de la cantidad de variables al ancho de la vecindad más grande.

---

## 3. Enumeración: la respuesta exacta

```
Pregunta: P(R | W=T)

  P(R=T | W=T) = 0.6585
  P(R=F | W=T) = 0.3415

  mundos enumerados: 8
  mundos que sobreviven a la evidencia: 4  (50%)

  Contraste: P(W=T | R=T) = 0.9000
  Y P(R=T | W=T)         = 0.6585
```

**No es 0.90.** Bayes no es un detalle: es la diferencia entre las dos preguntas.

El costo:

```
  variables    mundos 2^n
  10           1024
  20           1048576
  30           1073741824
```

Exacto siempre, e impagable pasado cierto tamaño.

---

## 4. Sampling: cambiar exactitud por velocidad

```
Verdad exacta: P(R=T | W=T) = 0.6585

método                   estimación     muestras usadas    error
prior sampling           0.6573         8219 (41%)          0.0013
likelihood weighting     0.6591         20000 (100%)        0.0006
```

Y con dos condiciones simultáneas:

```
  Verdad: P(R=T | S=T, W=T) = 0.9391

prior sampling           0.9334         4581 (23%)          0.0057
likelihood weighting     0.9390         20000 (100%)        0.0001
```

**El error de prior sampling sube 9×** cuando la evidencia se vuelve rara, porque la fracción útil se desploma. **Likelihood weighting no descarta: pondera.**

### Y la honestidad del método

```
  Su error baja como 1/sqrt(n):
  con 20000 muestras el error típico es del orden de 0.0071.
  Acá dio 0.0006.
  Cuatro ceros decimales exigen cien millones de muestras.
```

Sampling es más rápido, **no más verdadero**.

---

## 5. HMM: tres versiones antes de que diera bien

Escribí el filtrado mal tres veces. Lo que lo agarró fue la fuerza bruta:

### Versión 1 — transición primero

```
t    filtrado     fuerza bruta   coincide
1    0.7174       0.9529         NO
2    0.9104       0.9940         NO
3    0.9427       0.9946         NO
```

Números plausibles, monótonos, sumando 1 — y **mal**. La recursión del filtrado es **emitir y después transicionar**:

```
actualización: P(S_t | e_t) ∝ P(e_t | S_t) · P(S_t)
predicción:    P(S_{t+1}) = Σ P(S_{t+1} | S_t) · P(S_t)
```

### Versión 2 — el oráculo también estaba mal

La fuerza bruta multiplicaba `t` emisiones pero arrancaba con `PRIOR[hist[0]]` como si hubiera un estado extra. Corregido: **`t` estados, `t` emisiones**.

### Versión 3 — coincide

```
t    filtrado     fuerza bruta   coincide
1    0.6923       0.6923         sí
2    0.9054       0.9054         sí
3    0.9420       0.9420         sí
```

**Lo que se aprende:** dos implementaciones independientes del mismo cálculo son la única forma de saber que una está bien. Acá las dos estaban mal, y solo al hacerlas coincidir se destrabó.

### El límite de Markov

Si el clima tuviera memoria de tres días, el HMM de un paso daría probabilidades incorrectas y **la recursión no tendría cómo darse cuenta**: sigue sumando 1 y se ve sana desde adentro.

**Una suposición falsa no rompe el cálculo, rompe la garantía.** Mismo síntoma que la heurística no admisible del Módulo 1.

---

## 6. Bayes aplicado al gate: un verde no vale nada sin tasa base

```
Sensibilidad 0.90, especificidad 0.95

  tasa base de cambios bien      P(bien | pasa)
  0.99                           0.9994
  0.90                           0.9939
  0.50                           0.9474
  0.20                           0.8182
  0.05                           0.4865
  0.01                           0.1538
```

**El mismo gate en las siete filas.** Con casi todo roto, pasa y `P(bien)` es 0.15: no está probando nada, está diciendo lo que ya sabíamos.

### El gate nuevo

Un check recién escrito, sobre un repo donde nunca falló, tiene tasa base 1.0 y posterior **1.0 por construcción**. Ese 100% no es evidencia — es la definición de no haber corrido nunca el caso que lo rompe.

Es el mismo error que el Módulo 1 encontró en la reapertura y que `AGENTS.md` ya documenta: **una verificación que da verde sin haber verificado**.

### Y algo que parece un error y no lo es

```
  tasa base bien     verde aporta (log-odds)
  0.99               +2.890
  0.90               +2.890
  ...
  0.05               +2.890
```

**El mismo +2.89 siempre.** La evidencia de un evento es independiente del prior: es lo que la fórmula dice. Lo que cambia es de dónde arrancás. Con prior 0.05, subir 2.89 te deja en ~0.49 — seguís sin poder afirmar nada.

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| `P(a\|b)` y `P(b\|a)` son "parecidos" | 0.90 contra 0.66. La tasa base los separa |
| Bayes es una fórmula | Es la corrección por cuán rara es la causa |
| Una red bayesiana "simplifica" | 12 millones de filas menos con 30 variables |
| La factorización elimina el exponencial | Lo mueve al nodo con más padres |
| Sampling es una aproximación aceptable | Su error es `1/√n`: 4 decimales piden 100 millones |
| El filtrado es una recursión | Tiene un orden. Al revés da números plausibles y falsos |
| Un gate verde significa que está bien | Significa `P(bien\|pasa)`, y depende del historial |
| Un gate nuevo que nunca falló es un buen gate | Es un prior sin corregir. Su verde no aporta nada |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/uncertainty/practica
python3 run_all.py            # las 6
python3 p5_hmm.py             # el filtrado contra la fuerza bruta
python3 p6_gate_bayes.py      # el gate y su tasa base
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
