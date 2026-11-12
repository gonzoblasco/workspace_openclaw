# Nivel 1 · Prácticas

**Cómo funciona:** cada lab es una carpeta con un `index.html` **roto a propósito**. Lo arreglás,
corrés el checker, y cuando pasa a verde seguís con el siguiente.

```bash
cd ~/.openclaw/workspace/studies/fullstack-developer-scratch/nivel-1/labs

./run.sh          # estado de todos
./run.sh lab3     # solo uno, con el detalle
```

**El checker no mira el navegador.** Parsea el HTML como lo haría el navegador y verifica la
estructura. Un lab en verde significa que el HTML está bien; lo que se ve sigue dependiendo del CSS
(que es el bloque siguiente).

---

## Los labs

| Lab | Qué arreglás | Teoría |
|---|---|---|
| `lab1` | Etiquetas básicas: `h1`, `h2`, `h3`, `p` | Bloque 1 |
| `lab2` | `img` con `src` y que escale | Bloque 2 |
| `lab3` | Árbol de `div` anidados | Bloque 3 |
| `lab5` | Documento completo: `doctype`, `charset`, `viewport`, `html`/`head`/`body` | Bloque 5 |
| `lab6` | `<ol>` y `<ul>` con `<li>` | Bloque 6 |
| `lab8` | Formulario de 5 inputs con `label for` enlazado | Bloque 8 |
| `lab9` | Navegación entre 2 páginas + link externo | Bloque 9 |

---

## Reglas

**1. Escribí, no copies.** Cada carpeta tiene su `SOLUCION.html` (salvo `lab2`, `lab3`, `lab5`,
`lab6`, `lab8`, que también). **No la abras hasta haber intentado.** El checker verifica el
resultado, no el camino: copiar te da un verde que no sabés defender.

**2. Abrí el HTML en el navegador también.** El checker dice si la estructura está. El navegador dice
si se ve. Los dos importan.

```bash
open lab1/index.html
```

**3. Rompé cosas a propósito.** Después de cada lab en verde, sacale algo y mirá qué pasa:
- Sacá el `<meta charset>` del lab5 y escribí `ñ`. ¿Se ve bien?
- Sacá el `width="100%"` del lab2 y achicá la ventana. ¿Aparece scroll horizontal?
- Preguntá: *¿qué hace esta etiqueta?* y sacala. Si no cambia nada, no la entendiste.

**4. Si un lab no pasa y no sabés por qué:** corré `./run.sh labN` — el mensaje del FAIL dice
exactamente qué falta. Si aun así no sale, preguntame.

---

## Por qué esto importa para lo que viene

Gonzo va a escribir **skills, scripts y workflows**. Todo eso son archivos con estructura:
un `SKILL.md` tiene frontmatter y secciones; un script tiene bloques anidados; un workflow es un
árbol de pasos. **Armar un árbol de `<div>` correcto y cerrarlo bien es el mismo músculo** que armar
un árbol de pasos correcto y cerrarlo bien.

Nesting, indización y "¿quién es hijo de quién?" no son un tema de HTML. Son *la* habilidad que se
transfiere.

---

## Estado

| Lab | Estado |
|---|---|
| lab1 | ⬜ pendiente |
| lab2 | ⬜ pendiente |
| lab3 | ⬜ pendiente |
| lab5 | ⬜ pendiente |
| lab6 | ⬜ pendiente |
| lab8 | ⬜ pendiente |
| lab9 | ⬜ pendiente |

*(Marcá a mano o preguntame y lo actualizo.)*

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
