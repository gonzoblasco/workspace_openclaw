# Ritz-Carlton - Retest JS | Cheatsheet de 4 puntos (leer mañana antes de entrar)

**Fecha:** Lunes 31/08/2026 · **Objetivo:** >= 70% · **Mínimo actual:** 60

> Regla de escritura: guion comun (-), NUNCA em dash. Verificado.

---

## 1. Event loop (orden de ejecucion)

**En 1 linea:** "Primero los directos, despues las promesas, al final los timers."

| Cola | Que entra | Cuando corre |
|---|---|---|
| **Sincrono** | codigo lineal, IIFE, callbacks directos `cb()` | Primero, en orden |
| **Microtasks** | `Promise.then`, `await`, `queueMicrotask` | Despues de todo lo sincrono |
| **Macrotasks** | `setTimeout`, `setInterval` | Al final |

**Trampa clave:** `setTimeout(..., 0)` NO es "ya" - va despues de todas las microtasks.

**Metodo:** no leas el codigo lineal. Clasifica cada `console.log` en una de las 3 colas y mezcla.

---

## 2. Arrow vs function (el this)

**En 1 linea:** "arrow hereda el this, function no."

```js
setTimeout(function() { console.log(this.nombre); }, 0);  // undefined
setTimeout(() => { console.log(this.nombre); }, 0);       // hereda el this de afuera
```

---

## 3. El acronimo (el que cayo el otro dia)

**Pipeline:** `split -> filter -> map -> join`

```js
const STOP = new Set(["of", "and", "the", "a", "an", "in", "for", "to"]);

function acronym(str) {
  return str
    .trim()
    .split(/\s+/)                                  // separa por espacios
    .filter(w => w && !STOP.has(w.toLowerCase()))  // filtra vacias + stop words (minúsculas)
    .map(w => w[0].toUpperCase())                  // 1ra letra en mayuscula
    .join("");
}

acronym("United States of America"); // "USA"
acronym("The World Health Organization"); // "WHO"
```

**Los 2 detalles que hacen la diferencia:**
- `.toLowerCase()` al comparar contra el set (si no: "USOA")
- `.toUpperCase()` al tomar la letra (si no: "usa")

---

## 4. IIFE

**Que es:** funcion que se define y se invoca al instante.
**Para que:** aislar scope - las variables adentro quedan privadas, no contaminan el global.
**Como:** los `()` envuelven para hacerla expresion, los `()` del final la invocan.

```js
(function() { var x = 5; })();   // x NO sale de aca
console.log(typeof x);           // "undefined"

(() => { })();                   // forma arrow (la comun)
```

**Trampa de examen:** si preguntan que imprime, la variable interna declarada con `var` fuera del IIFE da `undefined` (no existe fuera).

---

## Estrategia

1. **Prioridad de repaso esta mañana:** acronimo (casi seguro vuelve a caer) -> IIFE -> callbacks -> event loop (repaso rapido).
2. No te trabes en una - salta y volve. 15 min, minimo 70%.
3. Resuelve los ejercicios de orden de ejecucion clasificando las 3 colas, no leyendo lineal.
