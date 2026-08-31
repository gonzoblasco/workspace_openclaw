# Ritz-Carlton - Quick Drill 5 min (pasada final de manana)

> Hacelo a mano, sin mirar las respuestas. 5 min. Esto es formato examen real.

## 1. (Event loop) Que imprime y en que orden?
```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
```
___

## 2. (IIFE) Que imprime?
```js
(() => {
  var x = 10;
  console.log(x);
})();
console.log(typeof x);
```
___

## 3. (Callbacks sinc/async) Que imprime y en que orden?
```js
function run(cb) {
  console.log("inicio");
  cb();
  console.log("fin");
}
run(() => console.log("callback"));
```
___

## 4. (Promises + async) Que imprime?
```js
async function f() {
  console.log("1");
  await Promise.resolve();
  console.log("2");
}
f();
console.log("3");
```
___

## 5. (Acronimo - EL QUE CAYO) Escribi la funcion:
```js
// "United States of America" -> "USA"
// Filtrar: of, and, the, a, an, in, for, to
function acronym(str) {
  // tu codigo
}
```
___

## 6. (Promises encadenadas) Que imprime?
```js
Promise.resolve()
  .then(() => console.log("1"))
  .then(() => console.log("2"));
Promise.resolve().then(() => console.log("3"));
setTimeout(() => console.log("4"), 0);
```
___

---
<details>
<summary>Respuestas (no mires hasta resolver)</summary>

**1.** `A, D, C, B` (sincrono A,D - microtask C - macrotask B)

**2.** `10` y `undefined` (el x de la IIFE no sale)

**3.** `inicio, callback, fin` (callback sincrono, se llama en su linea)

**4.** `1, 3, 2` (f() imprime 1 sincrono hasta el await; 3 sincrono; 2 microtask tras await)

**5.**
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

**6.** `1, 2, 3, 4` (microtasks 1,2,3 en orden - macrotask 4 al final)

</details>
