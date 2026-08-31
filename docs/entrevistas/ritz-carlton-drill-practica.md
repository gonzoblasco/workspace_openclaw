# Ritz-Carlton - Drill de Código (Práctica Antes del Retest)

**Fecha del retest:** Lunes 31/08/2026
**Objetivo:** Practicar los algoritmos que probablemente cayeron (el acrónimo y variantes) hasta que salgan mecánicos. El event loop ya lo tenés sólido - acá el foco es ESCRIBIR código limpio y correcto rápido.

---

## Reglas de práctica

1. **Cronómetro de 20 min.** Resolvé lo que puedas. Si una te traba >3 min, saltá y volvé.
2. **Escribí el código en un editor vacío** (no mires las soluciones hasta terminar).
3. **Repetí los que fallaste** hasta que salgan sin pensar.
4. **El acrónimo es EL que casi seguro vuelve a caer** - tiene que salir mecánico.

---

## Drill 1: El acrónimo (el que cayó, tiene que salir de memoria)

```js
// "United States of America" -> "USA"
// Filtrar stop words: of, and, the, a, an, in, for, to
function acronym(str) {
  // ESCRIBÍ TU CÓDIGO ACÁ
}
```

**Pruebas que debe pasar tu función:**
- `acronym("United States of America")` → `"USA"`
- `acronym("World Health Organization")` → `"WHO"`
- `acronym("as soon as possible")` → `"ASAP"` (¿qué pasa con "as"? No es stop word acá)
- `acronym("National Aeronautics and Space Administration")` → `"NASA"`
- `acronym("  spaced   out   words  ")` → `"SOW"` (tolerar espacios dobles)

---

## Drill 2: Variantes del acrónimo (para no fallar si cambia la consigna)

**2a. Acrónimo SIN stop words** (solo primeras letras):
```js
// "Hello World" -> "HW"
function firstLetters(str) {
  // tu código
}
```

**2b. Acrónimo solo de palabras MAYÚSCULAS** (suelen pedirlo distinto):
```js
// "asap world" -> "AW" (toma todas)
// o "ASAP World" -> "AW" (filtra las que estan en mayuscula completa)
```

**2c. Acronym con un separator** (devolver con puntos):
```js
// "United States of America" -> "U.S.A" (con puntos entre letras)
```

---

## Drill 3: Invertir strings (variante probable)

```js
// "hola" -> "aloh"
function reverse(str) {
  // tu código
}
```

**Variantes:**
- `reverse("hello world")` → `"dlrow olleh"` (invierte todo)
- `reverseWords("hello world")` → `"world hello"` (invierte el orden de palabras, no las letras)

---

## Drill 4: Contar letras (variante probable)

```js
// "banana" -> { b:1, a:3, n:2 }
function countLetters(str) {
  // tu código
}
```

**Variantes:**
- Contar SOLO minúsculas (ignorar mayúsculas): `"Banana"` → `{ b:1, a:3, n:2 }`
- Retornar la letra más frecuente: `"banana"` → `"a"`

---

## Drill 5: Palíndromo (variante clásica de algoritmos JS)

```js
// "anita lava la tina" -> true (ignorando espacios y mayúsculas)
function isPalindrome(str) {
  // tu código
}
```

**Pruebas:**
- `isPalindrome("racecar")` → `true`
- `isPalindrome("Anita lava la tina")` → `true` (ignorar espacios y mayúsculas)
- `isPalindrome("hello")` → `false`

---

## Drill 6: FizzBuzz (calentamiento clásico, si da tiempo)

```js
// Números 1 a 15: "Fizz" si es multiplo de 3, "Buzz" si de 5, "FizzBuzz" si de ambos.
function fizzbuzz(n) {
  // tu código
}
```

---

## Soluciones (no mires hasta intentar TODOS)

<details>
<summary>Ver soluciones</summary>

**1. Acrónimo (mecánico):**
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

**2a. First letters (sin stop words):**
```js
function firstLetters(str) {
  return str
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map(w => w[0].toUpperCase())
    .join("");
}
```

**2b. Solo mayúsculas completas:**
```js
function capitalAcronym(str) {
  return str
    .trim()
    .split(/\s+/)
    .filter(w => w === w.toUpperCase())  // solo palabras que estan 100% en mayuscula
    .map(w => w[0])
    .join("");
}
// "ASAP World" -> "A" (solo ASAP esta en mayuscula)
```

**2c. Con puntos:**
```js
function dottedAcronym(str) {
  return acronym(str).split("").join(".");
}
// "USA" -> "U.S.A"
```

**3. Reverse + ReverseWords:**
```js
function reverse(str) {
  return str.split("").reverse().join("");
}

function reverseWords(str) {
  return str.split(" ").reverse().join(" ");
}
// "hello world" -> "world hello"
```

**4. CountLetters + más frecuente:**
```js
function countLetters(str) {
  return str.toLowerCase().split("").reduce((acc, ch) => {
    if (ch !== " ") acc[ch] = (acc[ch] || 0) + 1;
    return acc;
  }, {});
}

function mostFrequent(str) {
  const counts = countLetters(str);
  return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
}
// "banana" -> "a"
```

**5. Palíndromo:**
```js
function isPalindrome(str) {
  const clean = str.toLowerCase().replace(/\s+/g, "");
  return clean === clean.split("").reverse().join("");
}
// "Anita lava la tina" -> true
```

**6. FizzBuzz:**
```js
function fizzbuzz(n) {
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) console.log("FizzBuzz");
    else if (i % 3 === 0) console.log("Fizz");
    else if (i % 5 === 0) console.log("Buzz");
    else console.log(i);
  }
}
```

</details>

---

## Checklist pre-retest (mañana)

- [ ] **Acrónimo** - escribirlo de memoria 3 veces sin mirar. Es EL que cae.
- [ ] **Event loop** - repasar el orden: síncrono → microtasks → macrotasks. 5 min, ya lo tenés.
- [ ] **IIFE** - entender qué aísla y qué imprime `typeof x` fuera (undefined).
- [ ] **Callbacks** - orden síncrono vs asíncrono.
- [ ] **Reverse / CountLetters / Palíndromo** - variantes rápidas por si cae otro algoritmo.
- [ ] **Leer bien la consigna** - la lección del 60: confirmar si es psicotécnico o JS técnico; en el examen leé si el acrónimo filtra stop words o no.

---

## Nota mental

El 60 probablemente se fue en **no haber repasado IIFE/callbacks** y en **no escribir el acrónimo fluido**. El event loop lo hiciste "bastante bien". Así que el plan es claro: **acrónimo mecánico + IIFE + callbacks**, y el event loop como repaso rápido. No te quemes - el material ya está sólido, solo es práctica de memoria muscular.
