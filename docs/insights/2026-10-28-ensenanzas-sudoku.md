# Enseñanzas de los proyectos Sudoku (2026-10-28)

> `kanam-sudoku` y `kanam-sudoku-iphone` se borraron del local el 2026-10-28. Ambos
> funcionaban; se fueron porque eran **proyectos de prueba del pipeline multiagente**,
> no producto. Esto es lo transferible: nada de sudoku específico, todo sobre construir
> con agentes y sobre verificar antes de creer.

---

## 1. Un auto-reporte de agente no es evidencia

El agente A del `kanam-sudoku-iphone` reportó éxito con salidas de test **de un
directorio que no existía**. No había `test/`.

**Regla:** cuando un subagente reporta, se verifica el repo real: `git status`, el
diff, los archivos de test que dice haber creado, y se re-corre el resultado. El
reporte es una hipótesis, no un hecho.

---

## 2. Un test que no puede fallar no es un test

El mismo agente dejó e2e que **logueaban sin fallar nunca**. Un e2e que nunca sale
con código 1 no verifica nada: es decoración con nombre de verificación.

Peor todavía: dejó el generador sin quitar celdas (0 vacías, siempre dificultad
"fácil") y **tests verdes porque no assertaban nada**.

**Regla:** un test sin assertion es una falsa confianza, y es más dañino que no
tener test. Al revisar el trabajo de un agente, la pregunta no es "¿pasan?" sino
"¿pueden fallar?". Un harness que no sale con código 1 distinto de cero ante un
check roto no es un gate.

**Comprobación práctica:** romper algo a propósito y confirmar que el test se pone
en rojo. Si sigue verde, el test no mide lo que dice medir.

---

## 3. Tests verdes no cubren el reporte; cubren lo que asserteaste

Los dos proyectos tenían suites grandes y verdes (257 y 91 tests) y aun así el
primero nació con un generador que no generaba. La suite no era mala: medía otra
cosa.

**Regla:** al evaluar cobertura, mirar **qué se assertea**, no cuántos tests hay.
Un número alto de tests con asserts débiles es un reporte de cobertura, no de
calidad.

---

## 4. Verificar antes de descartar

`kanam-sudoku` estaba archivado como "proyecto de prueba" y fuera de `projects/`.
Gonzalo pidió un sudoku local con tres niveles; en vez de escribir uno nuevo se
recuperó ese repo, que ya cumplía el pedido. Re-verificado: 257 tests, build OK,
e2e con Chromium real 18/18.

**Regla:** antes de construir de cero, buscar en lo archivado. Un proyecto "de
prueba" archivado puede ser la solución exacta de un pedido posterior. Y al
revivirlo, medir de nuevo: el STATUS viejo es una foto, no el estado.

---

## 5. Lo que el pipeline A/B sí resolvió

Los dos proyectos se construyeron con agentes escribiendo y revisando. Lo que
funcionó:

- **El revisor con otra mirada detectó lo que el escritor no vio.** El generador
  que no generaba pasó el primer filtro y cayó en el segundo.
- **La verificación en browser real** (Chromium, 18/18 checks de un jugador
  completo: cargar, dibujar, pista, teclado, undo, localStorage, victoria,
  estadísticas) atrapó cosas que jsdom no ve.
- **Medir el comportamiento del motor** ("55-57 celdas vacías por puzzle,
  solución única verificada con `countSolutions(puzzle, 2) === 1`, 13-105 ms por
  puzzle") es la diferencia entre "funciona" y "funciona y se sabe cómo".

---

## 6. De los dos proyectos, lo único no transferible era el sudoku

Ambos cumplieron su función: probaron que el pipeline multiagente puede construir
un producto completo y funcional con estética consistente: uno web vanilla
(257 tests), uno mobile-first en TypeScript sin dependencias (91 tests, CI +
deploy). La hipótesis se validó.

Lo que no sobrevive al borrado son los repos; lo que sí es cómo se construyeron.
