# Ritz-Carlton - Retest Técnico JS (Preparación)

**Fecha del retest:** Lunes 31/08/2026
**Contexto:** Steven (recruiter) dijo "test de lógica, 15 min, mínimo 70%". El examen real fue **JavaScript técnico** (no psicotécnico). Gonzo sacó **60**, necesita >= 70.
**Lección registrada:** cuando un recruiter dice "test de lógica" en proceso técnico, confirmar si es psicotécnico o **lógica de programación/JS** - son cosas muy distintas.

---

## RESULTADO RETEST (31/08/2026): 69% - a 1 punto del 70%

- **Score:** 69% (avance real desde 60). Samarth confirmó por LinkedIn.
- **Estado:** Samarth dijo "I will update the team" y luego "I am checking with the team".
- **Señal positiva:** Samarth preguntó "Are you out of town currently?" - chequeando logística.
- **CAUSA de la pregunta:** el hiring manager vio IP de Córdoba (probablemente iCloud Privacy Relay / proxy). Se resolvió: Gonzo desactivó el proxy y pasó la IP real (200.61.165.7).
- **RESULTADO (13:32):** PASO a primera ronda de entrevista. Samarth: "The team wants to schedule first round of interview with you".
- **Estado:** confirmado el avance. Pendiente fecha/horario de la primera ronda.
- **Lección:** si un reclutador te pregunta por ubicación/IP, suele ser por detección de proxy/VPN, no una bandera negativa. Responder rápido y proactivamente (ofrecer IP) despeja cualquier duda.
- **Lección:** el 69% confirma que el acrónimo + event loop ya están sólidos; el punto perdido probablemente fue en otro ejercicio de código. Si hay un 3er intento, repasar los algoritmos de código (reverse, countLetters) además del acrónimo.

---

## Contenido real del examen (lo que entró)

1. **Resolución de problemas de JS** (algoritmos).
2. **Promises y orden de ejecución** (event loop: microtasks antes que macrotasks).
3. **Callbacks** y **IIFE** (`(() => {})()`).
4. **Ejercicio práctico**: función acrónimo ("United States of America" → "USA"), filtrando stop words (of, and, the, a, an, in, for, to).

---

## Pilar 1: Promises y orden de ejecución (event loop)

**Regla de oro del orden:**
1. **Síncrono** (lineal).
2. **Microtasks**: `Promise.then`, `queueMicrotask`, continuaciones de `await`. (Antes que todo macrotask.)
3. **Macrotasks**: `setTimeout`, `setInterval`, I/O.

```js
console.log("A");                                   // 1 síncrono
Promise.resolve().then(() => console.log("B"));     // 2 microtask
setTimeout(() => console.log("C"), 0);              // 3 macrotask
console.log("D");                                   // 4 síncrono
// Output: A, D, B, C
```

**Los tres traps comunes:**
- **`setTimeout(..., 0)` NO es inmediato** - corre después de todas las microtasks.
- **`await x`** pone el resto de la función como microtask (no bloquea).
- **`then` encadenados** corren en orden, como cola.

**Ejercicio clásico de examen:**
```js
let p = new Promise((res) => res(1));
p.then(v => console.log(v))     // 1
 .then(() => console.log(2));   // 2
Promise.resolve().then(() => console.log(3)); // 3
setTimeout(() => console.log(4), 0);          // 4 (macrotask, va al final)
// Output: 1, 2, 3, 4
```

---

## Pilar 2: Callbacks

Un callback es solo una **función que se pasa como argumento** para ejecutarse después.

```js
function saluda(nombre, cb) {
  console.log("Hola", nombre);
  cb();  // se invoca después
}
saluda("Gonzo", () => console.log("callback listo"));
// Hola Gonzo
// callback listo
```

**Trampa común:** el callback se ejecuta o no según el código, y el **`this`** dentro de un callback regular no siempre es el esperado (arrow functions heredan `this`, functions regulares no). Suelen preguntar el orden en que se llama y qué pasa si el callback es síncrono vs asíncrono.

---

## Pilar 3: IIFE - `(() => {})()`

**IIFE** = *Immediately Invoked Function Expression*. Función que se define y se ejecuta al instante.

```js
// Formas de escribirlo
(function() { console.log("IIFE"); })();
(() => { console.log("arrow IIFE"); })();
```

**Qué evalúan:**
- **Aislamiento de scope**: variables dentro no contaminan el global.
- **Orden**: el `console.log` corre apenas se evalúa la expresión.
- Que sepas **por qué** existe (privacidad/scope, antes de que existieran `let/const` block scope).

```js
(function() {
  var x = 5;      // x NO sale de acá
})();
console.log(typeof x); // "undefined" - no accesible
```

---

## Pilar 4: El ejercicio del acrónimo (el que cayó)

```js
// "United States of America" -> "USA"
const STOP = new Set(["of", "and", "the", "a", "an", "in", "for", "to"]);

function acronym(str) {
  return str
    .trim()
    .split(/\s+/)                                 // separa por espacios (tolera dobles)
    .filter(w => w && !STOP.has(w.toLowerCase()))  // saca vacías y stop words
    .map(w => w[0].toUpperCase())                  // 1ra letra en mayúscula
    .join("");
}

acronym("United States of America"); // "USA"
acronym("World Health Organization"); // "WHO"
// sin filtrar 'of' daria "USOA"
```

**Puntos que evalúan:** filtrar las stop words (si no, "USOA"), manejar mayúsculas/minúsculas (`.toLowerCase()` al comparar), tolerar espacios (`.split(/\s+/)`), y que la función sea pura (solo devuelve el resultado).

---

## Drill: Event Loop - ¿Qué imprime y en qué orden?

**Reglas:**
1. Síncrono corre primero, en orden.
2. Microtasks (`Promise.then`, `await`, `queueMicrotask`) corren antes que macrotasks.
3. Macrotasks (`setTimeout`, `setInterval`) corren al final, en orden de registro.
4. `setTimeout(..., 0)` NO es inmediato - va después de todas las microtasks.

**P1.**
```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
```

**P2.**
```js
setTimeout(() => console.log("a"), 0);
Promise.resolve().then(() => console.log("b"));
console.log("c");
```

**P3.**
```js
console.log("x");
setTimeout(() => console.log("y"), 100);
setTimeout(() => console.log("z"), 0);
console.log("w");
```

**P4.**
```js
Promise.resolve()
  .then(() => console.log("1"))
  .then(() => console.log("2"));
Promise.resolve().then(() => console.log("3"));
```

**P5.**
```js
async function f() {
  console.log("a");
  await Promise.resolve();
  console.log("b");
}
f();
console.log("c");
```

**P6.**
```js
setTimeout(() => console.log("t1"), 0);
setTimeout(() => console.log("t2"), 0);
Promise.resolve().then(() => console.log("p1"));
Promise.resolve().then(() => console.log("p2"));
```

**P7.**
```js
console.log("start");
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
queueMicrotask(() => console.log("micro"));
console.log("end");
```

**P8.**
```js
let p = new Promise((res) => res("resuelto"));
p.then((v) => console.log(v));
console.log("despues");
```

**P9.**
```js
function cb() { console.log("cb"); }
setTimeout(cb, 0);
Promise.resolve().then(() => console.log("p"));
cb();  // llamada directa
```

**P10.**
```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve()
  .then(() => console.log("3"))
  .then(() => console.log("4"));
setTimeout(() => console.log("5"), 0);
console.log("6");
```

**Respuestas** (no mires hasta resolverlos):

<details>
<summary>Ver respuestas</summary>

**P1:** `1, 4, 3, 2` (síncrono 1,4 → microtask 3 → macrotask 2)

**P2:** `c, b, a` (síncrono c → microtask b → macrotask a)

**P3:** `x, w, z, y` (síncrono x,w → macrotasks en orden de registro: z(0) antes que y(100))

**P4:** `1, 2, 3` (los then encadenados de la 1ra promesa corren 1,2 en orden; el 3 se registra después pero como la 1ra ya tiene 2 pendientes, van 1,2,3)

**P5:** `a, c, b` (f() corre síncrono hasta el await → imprime "a"; luego "c" síncrono; el "b" es microtask tras el await)

**P6:** `p1, p2, t1, t2` (todas las microtasks primero, luego las macrotasks en orden)

**P7:** `start, end, promise, micro, timeout` (síncrono start,end → microtasks en orden de registro: promise antes que micro → macrotask timeout)

**P8:** `despues, resuelto` (el .then es microtask, corre después del síncrono "despues")

**P9:** `cb, p, cb` (la llamada directa cb() imprime "cb" síncrono; luego microtask "p"; luego el setTimeout "cb")

**P10:** `1, 6, 3, 4, 2, 5` (síncrono 1,6 → microtasks 3,4 → macrotasks 2,5 en orden)

</details>

---

## Mini-test Ritz-Carlton (15 min, estilo real)

**Consigna:** resolvé lo que puedas en 15 min. Si una te traba, saltá y volvé. Las respuestas al final.

**1. (Promises) ¿Qué imprime y en qué orden?**
```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
```

**2. (IIFE) ¿Qué imprime?**
```js
(() => {
  var x = 10;
  console.log(x);
})();
console.log(typeof x);
```

**3. (Callbacks) ¿Qué imprime y en qué orden?**
```js
function run(cb) {
  console.log("inicio");
  cb();
  console.log("fin");
}
run(() => console.log("callback"));
```

**4. (Promises + async) ¿Qué imprime?**
```js
async function f() {
  console.log("1");
  await Promise.resolve();
  console.log("2");
}
f();
console.log("3");
```

**5. (Algoritmo) Escribí una función que invierta un string:**
```js
// "hola" -> "aloh"
function reverse(str) {
  // tu código
}
```

**6. (Acrónimo - el que cayó) Escribí la función:**
```js
// "United States of America" -> "USA"
// Filtrar: of, and, the, a, an, in, for, to
function acronym(str) {
  // tu código
}
```

**7. (Promises encadenadas) ¿Qué imprime?**
```js
Promise.resolve()
  .then(() => console.log("1"))
  .then(() => console.log("2"));
Promise.resolve().then(() => console.log("3"));
setTimeout(() => console.log("4"), 0);
```

**8. (Algoritmo) Escribí una función que cuente cuántas veces aparece cada letra:**
```js
// "banana" -> { b:1, a:3, n:2 }
function countLetters(str) {
  // tu código
}
```

**Respuestas** (no mires hasta resolver):

<details>
<summary>Ver respuestas</summary>

**1.** `A, D, C, B` (síncrono A,D → microtask C → macrotask B)

**2.** `10` y luego `undefined` (el `x` de la IIFE no sale; `typeof x` fuera es "undefined")

**3.** `inicio, callback, fin` (el callback se llama en medio, síncrono)

**4.** `1, 3, 2` (f() imprime "1" síncrono hasta el await; "3" síncrono; "2" microtask tras await)

**5.**
```js
function reverse(str) {
  return str.split("").reverse().join("");
}
```

**6.**
```js
const STOP = new Set(["of", "and", "the", "a", "an", "in", "for", "to"]);
function acronym(str) {
  return str
    .trim()
    .split(/\s+/)
    .filter(w => w && !STOP.has(w.toLowerCase()))
    .map(w => w[0].toUpperCase())
    .join("");
}
```

**7.** `1, 2, 3, 4` (microtasks 1,2,3 en orden → macrotask 4)

**8.**
```js
function countLetters(str) {
  return str.split("").reduce((acc, ch) => {
    acc[ch] = (acc[ch] || 0) + 1;
    return acc;
  }, {});
}
```

</details>

---

## Estrategia para el lunes

- **El event loop ya lo tenés sólido** (lo hiciste "bastante bien" mezclado). No es donde perdés puntos.
- **El 60 probablemente se fue en:** escribir código (el acrónimo) y temas no repasados (IIFE, callbacks).
- **Prioridad de repaso:** acrónimo (casi seguro vuelve a caer) → IIFE → callbacks → event loop (repaso rápido).
- **El acrónimo:** practicarlo hasta que salga mecánico. Es el que más seguro va a volver a caer.
