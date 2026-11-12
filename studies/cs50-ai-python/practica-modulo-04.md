# Práctica del Módulo 4 — Optimization

> Las preguntas del Módulo 4, **corridas**. Sin scipy: la programación lineal se resuelve como la resuelve un solver, recorriendo vértices.
> Gate: `python3 run_all.py` → 5 de 5.

```
PASA   p1_hill_climbing.py            hill climbing queda atrapado la mayoría de las veces
PASA   p2_annealing.py                aceptar lo peor a propósito llega más al global
PASA   p3_lineal.py                   el óptimo de un programa lineal está en un vértice
PASA   p4_csp.py                      forward checking gana solo cuando hay ramas muertas
PASA   p5_camino_vs_resultado.py      camino y resultado no son la misma pregunta

RESULTADO: PASA (5 de 5)
```

---

## 1. Hill climbing: 82% atrapado, y sin poder saberlo

Paisaje con un global y dos locales bien separados:

```
Máximos locales encontrados:
  x=   4.70  valor=1.4042  GLOBAL
  x=  -0.95  valor=0.8162  local
  x=  -8.00  valor=0.5501  local

termina en el global: 35/200 (18%)
ATASCADO en un máximo local: 165/200 (82%)

Dónde termina y cuántas veces:
    x=    4.7  valor=1.4042   35 veces  global
    x=   -8.0  valor=0.5501   29 veces  LOCAL
    x=   -1.0  valor=0.8158   19 veces  LOCAL
    ...
```

**Lo peor no es el 82%: es que desde adentro no se nota.** En un máximo local y en el global, ningún vecino mejora. El algoritmo se detiene en los dos con el mismo criterio y reporta el mismo "terminado".

### Random restart

```
 1 reinicios: 28%
 3 reinicios: 61%
 5 reinicios: 79%
10 reinicios: 94%
20 reinicios: 100%
```

Sube la probabilidad sin entender el paisaje. **Pero no garantiza nada**: reiniciar desde un punto al azar puede caer siempre en el mismo pozo.

---

## 2. Simulated annealing: bajar el valor a propósito

### La regla

```
P(aceptar un empeoramiento Δ) = exp(-Δ/T)

  Δ (empeora)    T=1.0      T=0.5      T=0.1      T=0.01
  0.01           0.9900     0.9802     0.9048     0.3679
  0.10           0.9048     0.8187     0.3679     0.0000
  0.50           0.6065     0.3679     0.0067     0.0000
  2.00           0.1353     0.0183     0.0000     0.0000
```

### Medido contra hill climbing, mismo presupuesto

```
método                                 llega al global    mejor valor medio
simulated annealing (1 corrida)        44%                0.9940
hill climbing (1 corrida)              26%                0.9777
```

### Y el trazado, que explica el porqué

```
iteración    T            valor actual
0            1.000000     0.8158
229          0.317311     0.6286      ← el valor BAJA
459          0.100183     1.1489
919          0.009986     1.3994
1839         0.000100     1.4042      ← global
```

**El valor baja al principio, y eso es el trabajo.** Aceptar empeorar con T alta es lo que le permite salir del pozo antes de que se vuelva trampa.

### La honestidad

Simulated annealing no garantiza el global. `T₀` baja → se comporta como hill climbing. La garantía teórica (enfriamiento logarítmico) asume tiempo infinito. En la práctica se elige presupuesto y se reza.

---

## 3. Programación lineal: el óptimo está en un vértice

```
Maximizar  40·X + 30·Y
sujeto a    X +  Y <= 12
            2X + Y <= 16
            X, Y  >= 0

Vértices del cruce de rectas:
  X          Y          40X+30Y      factible
  0.00       0.00       0.00         sí
  0.00       12.00      360.00       sí
  0.00       16.00      480.00       no
  4.00       8.00       400.00       sí      ← óptimo
  8.00       0.00       320.00       sí
  12.00      0.00       480.00       no

Barrido de 10.000 puntos interiores: mejor Z=400.00 en (4.0, 8.0)
el vértice gana o empata: sí
```

**Eso es un teorema, no una coincidencia.** Objetivo lineal sobre polígono convexo → no hay máximo interior. Por eso `linprog` recorre vértices y termina: no le falta buscar, no hay nada que buscar adentro.

### Donde se rompe

- **Restricción no lineal** (`X·Y <= 12`): el óptimo puede estar en el interior; recorrer vértices da una respuesta falsa con la misma seguridad.
- **Programación entera** (`X`, `Y` enteros): el óptimo puede no ser un vértice del poliedro relajado.

La formulación lineal es una **elección**, no una propiedad del problema.

---

## 4. CSP: forward checking gana solo si hay rama muerta

El outline esperaba que la versión con inferencia explorara estrictamente menos. **No siempre es así**, y el script lo muestra con dos problemas:

```
=== Horarios de examen (A≠B, B≠C, C≠D, A≠D) ===
  backtracking puro              5 nodos      solución ['Lun','Mar','Lun','Mar']
  backtracking + forward         5 nodos    3 podas

=== Coloreado de grafo: 9 nodos, 3 colores ===
  backtracking puro              79 nodos
  backtracking + forward         21 nodos    48 podas    3.76x
  OK  misma solución.
```

**En el horario chico el forward checking no gana nada.** La primera rama que prueba ya es solución. **No hay ramas muertas que podar.**

**En el coloreado gana 3.76×**, porque ahí sí hay que retroceder.

> **Una poda no mejora un árbol que no tiene ramas muertas.**

---

## 5. Camino vs resultado: dos familias, dos preguntas

Mismo mapa: A\* contra hill climbing sobre una ruta.

```
=== Familia 1: búsqueda de caminos (A*) ===
  camino encontrado: 44 pasos
  nodos expandidos: 75
  Lo que devuelve es el CAMINO. Se puede dibujar, seguir y verificar.

=== Familia 2: búsqueda local (hill climbing sobre la ruta) ===
  puntos en la ruta: 14
  ruta válida (sin paredes): NO   <- el puntaje no garantiza validez
  objetivo: 737.0
  el algoritmo nunca construyó un camino: movió puntos y midió un puntaje
```

**La ruta de hill climbing no es válida.** Atraviesa paredes. Y el puntaje la dio por buena.

Ese es el punto entero: **el optimizador no sabe qué es una pared. Sólo maximiza lo que le pongas en el objetivo.** Si el objetivo mide la distancia al destino pero no la adyacencia ni las paredes, encuentra una recta perfecta —imposible de recorrer— con puntaje ideal.

| Pregunta | A\* | Hill climbing |
|---|---|---|
| ¿Cuál es el camino más corto? | sí | no |
| ¿Los pasos son adyacentes y válidos? | por construcción | por el objetivo |
| ¿Mejorar una ruta existente? | no | sí |
| Garantía de óptimo | con `h` admisible | ninguna |

### Las dos traducciones

1. **"Escribí el plan" es búsqueda. "Mejorá este plan" es búsqueda local.** Elegir uno y esperar del otro lo que no puede dar es el error más común al montar un pipeline.
2. **Un agente que mejora un draft con la última sugerencia es hill climbing.** No escapa del óptimo local. Necesita un criterio externo, no más vueltas del mismo modelo — que es exactamente lo que aporta el pipeline A/B.

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| Hill climbing encuentra el máximo | 82% de las veces no, y no puede saberlo |
| Random restart lo arregla | Sube la probabilidad, no garantiza |
| Annealing escapa de los locales | Baja el valor a propósito al principio. Es el mecanismo |
| Annealing es el algoritmo superior | Es probabilístico. Con mal enfriamiento es hill climbing |
| Un programa lineal tiene óptimo interior posible | No, si objetivo y restricciones son lineales. Es un teorema |
| Forward checking siempre ayuda | Cero mejora si no hay ramas muertas que podar |
| La asignación del CSP se puede optimizar | CSP busca **satisfacer**, no optimizar. Es otro problema |
| Un optimizador encuentra la mejor solución | Encuentra la mejor según tu objetivo. Si el objetivo está mal, la solución es inútil |
| Un agente que itera mejora el texto | Es hill climbing: se queda en el primer local. Necesita criterio externo |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/optimization/practica
python3 run_all.py                    # las 5
python3 p2_annealing.py               # el trazado, con el valor bajando
python3 p4_csp.py                     # el caso donde la poda no hace nada
python3 p5_camino_vs_resultado.py     # la ruta inválida con puntaje perfecto
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
