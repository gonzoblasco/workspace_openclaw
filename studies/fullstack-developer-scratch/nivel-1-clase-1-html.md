# Nivel 1 · Clase 1 — HTML desde cero

**Módulo del curso:** 1 (HTML y CSS, 0:01:27 – 1:04:19) y 2 (Intro a CSS, 1:04:19 – 2:21:01)
**Curso:** `studies/fullstack-developer-scratch/` · **Tutor:** Kanam
**Fecha:** 2026-11-11

---

## Regla de esta clase

El curso enseña **escribiendo**, no leyendo. Cada bloque tiene un **LAB**: un archivo que vos escribís
y que yo verifico. No hay "leer y seguir". Si un lab no te sale, se mira el módulo y se repite.

**Arrancamos con el Módulo 1 completo**, y el LAB 1 ya lo podés hacer mientras leés.

---

## Bloque 1 · Qué es realmente un archivo HTML (0:01:27)

La analogía del video es la mejor que escuché para empezar: **un archivo HTML es un documento de texto
de Word**. El texto está; lo que cambia es que en Word seleccionás y hacés click en "Título 1", y en
HTML escribís el marcador a mano.

| Word | HTML |
|---|---|
| Escribís la frase | `Escribís la frase` |
| Seleccionás → "Título 1" | La envolvés en `<h1>…</h1>` |
| "Normal" | `<p>…</p>` |
| "Título 2" | `<h2>…</h2>` |

**La idea que importa:** HTML no dibuja. **Etiqueta**. Le dice al navegador *qué es* cada cosa, y el
navegador decide cómo se ve. Por eso un `<h1>` es grande sin que vos pongas el tamaño.

### La anatomía de una etiqueta

```
  <h1>  I code, therefore I am  </h1>
   ↑            ↑                ↑
apertura      contenido        cierre (con la barra)
```

**Trampa que el curso señala y que mucha gente tarda en entender:** si escribís el texto *fuera* de
las etiquetas, sale como texto normal. Sólo lo que está **entre** apertura y cierre recibe el formato.

### LAB 1 — tu primer archivo (10 min)

```bash
mkdir -p ~/dev/lab-html && cd ~/dev/lab-html
cat > index.html <<'HTML'
<h1>I code, therefore I am</h1>
<p>René Descartes, mal citado</p>
HTML
open index.html
```

**Tarea:**
1. Agregá debajo tu nombre como `<h2>`.
2. Agregá una frase que te guste como `<h3>`.
3. Agregá un párrafo con `<p>`.

**Lo que tenés que poder explicar cuando termines:** ¿por qué el nombre va en `<h2>` y no en `<h1>`?

---

## Bloque 2 · La etiqueta que no cierra: `img` (0:06:27)

El curso introduce `img` y con eso el primer concepto raro de HTML: **las etiquetas void**.

```html
<img src="mars.jpg">
```

**Por qué no tiene cierre:** no contiene texto. Una imagen no "envuelve" nada. Es un objeto insertado.
Por eso `<img>` no tiene `</img>`.

> El curso menciona que algunos escriben `<img src="x" />` con barra final. Dice: «less code is
> better code». Es correcto, y es la convención que usa el estándar HTML5: la barra es opcional y no
> aporta nada.

### `src` y el error más común

```html
<img src="mars.jpg">
```

**Si no se ve la imagen, el 90% de las veces es esto:** la ruta es **relativa al archivo HTML**, no a
tu carpeta de descargas. Si `index.html` está en `~/dev/lab-html/` y la imagen en
`~/dev/lab-html/mars.jpg`, entonces `src="mars.jpg"` funciona. Si la imagen está en `~/Downloads/`,
`src="mars.jpg"` no la encuentra.

### El "hack" del `width` (y por qué es un hack)

El curso muestra `width="100%"` para que la imagen escale con el navegador.

```html
<img src="mars.jpg" width="100%">
```

**Y aclara que es un hack**, porque lo correcto es CSS. Vale la pena entender *por qué* funciona: el
atributo `width` se aplica al elemento, y `%` significa "porcentaje del contenedor". El contenedor es
la página. Por eso escala.

**Lo que el curso no dice y conviene saber:** el atributo `width` como **número** (ej. `width="400"`)
significa píxeles y es *mal* para responsive — se queda en 400 px en un celular de 320. Como
**porcentaje** funciona. La regla profesional es: dimensiones por CSS (`max-width: 100%; height: auto`)
y nunca por atributo. Pero para entender el concepto ahora, el atributo alcanza.

### LAB 2 — imagen que escale (5 min)

1. Descargá cualquier imagen a `~/dev/lab-html/`.
2. Agregala al HTML con `<img src="...">`.
3. Redimensioná la ventana del navegador. La imagen se achica; **la página no tiene scroll horizontal**.

**Si aparece scroll horizontal:** te falta el `width="100%"` (o el CSS equivalente). Ese scroll es el
problema real que el atributo resuelve.

---

## Bloque 3 · Nesting: la estructura de árbol (0:11:27)

**El concepto del capítulo.** Todo HTML es un árbol.

```html
<div>
  <h1>Título</h1>
  <img src="mars.jpg" width="100%">
  <h3>Subtítulo</h3>
  <p>Texto.</p>
</div>
```

`<div>` es el padre. Los cuatro de adentro son hijos. Y un hijo puede tener hijos propios, sin límite.

**Para qué sirve:** agrupa para poder hacer algo con el grupo. Sin `<div>`, no podés decir "estilizá
todo el artículo". Con `<div>`, sí.

### La indización es funcional, no decorativa

```
<div>
  <img src="mars.jpg">
  <h3>Sub</h3>
</div>
```

Los dos espacios de sangría te dicen **quién es hijo de quién** de un vistazo. Cuando una página tiene
200 líneas y 15 divs, sin indización te perdés. Con indización, cerraste el árbol con los ojos.

**Regla práctica:** si tenés que contar etiquetas de cierre para saber dónde estás, la indización está
mal. Reindentá antes de seguir.

### Un detalle del bloque anterior que ahora tiene sentido

Cuando el curso usa `width="100%"`, el navegador está aplicando un **porcentaje**. Pero MDN aclara que
`width` acepta «an integer without a unit» — o sea, **píxeles**, no un porcentaje arbitrario.

Entonces `width="100%"` no es "poner un tamaño": es una forma torcida de decir *"escala al contenedor"*.
Funciona, pero es un hack que el video mismo admite. Y hay algo que **sí** agrega valor real:

```html
<img src="foto.jpg" width="800" height="600" alt="...">
```

Aunque después el CSS lo muestre a 400 px, poner `width` y `height` **en píxeles reales de la imagen**
le da al navegador la proporción antes de descargarla, y **reserva el espacio**. Sin eso, cuando la
imagen carga el texto salta hacia abajo (*layout shift*). Ese salto es lo que mide Core Web Vitals y lo
que hace que una página se sienta lenta aunque no lo sea.

**Regla:** `width`/`height` en la etiqueta = proporción (siempre). Tamaño visual = CSS (siempre).

### LAB 3 — armar un artículo (10 min)

Escribí un artículo con esta forma:

```html
<div>
  <h1>Título del artículo</h1>
  <img src="tu-imagen.jpg" width="100%">
  <p>Introducción.</p>
  <h3>Primera idea</h3>
  <p>Cuerpo de la primera idea.</p>
  <div>
    <h3>Idea adentro de idea</h3>
    <p>Esto es un div anidado.</p>
  </div>
</div>
```

**Después de escribirlo, dibujá el árbol en un papel.** Si el dibujo coincide con el HTML, entendiste
nesting. Si no, no.

---

## Bloque 4 · DevTools: leer el HTML de otros (0:16:27)

Esta es la sección que **convierte a alguien de "hace páginas" a "entiende páginas"**.

El curso va a BBC Football y edita los títulos desde el inspector. El punto no es vandalizar noticias:
es entender que **lo que ves es un árbol de etiquetas que el navegador interpretó**, y que podés
abrir ese árbol.

**Lo que se aprende mirando:**
- **Hover sobre un div en el inspector** → el navegador resalta en la página lo que ese div ocupa.
  Es la forma más rápida de mapear "este pedazo de la pantalla, ¿qué etiqueta es?".
- **Los divs están anidados en capas.** El curso lo dice con humor: «a div inside of a div inside of a
  div. This is web development in a nutshell». Eso no es un defecto: es la estructura.
- **Todo lo que ves se puede editar y se revierte con un refresh.** El HTML del inspector es una copia
  en memoria, no el archivo del sitio.

### Bonus que el curso menciona de pasada: `srcset`

BBC usa `srcset`, no sólo `src`. Cuando cambiaste `src` y no pasó nada, era por eso.

```html
<img srcset="small.jpg 480w, medium.jpg 1000w, large.jpg 2000w">
```

**Qué hace:** le da al navegador varias versiones y él elige según el tamaño de la pantalla y la
densidad de píxeles. Es la solución *de verdad* al problema que antes resolvíamos con `width="100%"`.

**Cuándo usarlo:** cuando la imagen grande pesa. Un celular no necesita bajar una foto de 2000 px para
mostrarla a 400. Con `srcset`, baja la de 480.

### LAB 4 — ejercicio de arqueología (15 min)

Elegí **cualquier** sitio que uses seguido (Wikipedia, un diario, GitHub). Abrí DevTools (`F12` o
`Cmd+Opt+I`).

**Tarea — anotá las respuestas, no las busques:**
1. ¿Cuántas capas de `<div>` anidadas hay en la barra de navegación? (contá abriendo el triángulo hasta
   llegar a un texto)
2. ¿El `<h1>` de la página existe? ¿Cuántos hay? (buscá en el inspector)
3. La imagen principal, ¿usa `src` o `srcset`?
4. Cambiá un texto desde el inspector y refrescá. ¿Qué se perdió?

**Lo que tenés que poder decir:** «el navegador me muestra una estructura en capas, y yo puedo abrir
cada capa». Si eso quedó claro, el bloque funcionó.

---

## Bloque 5 · El documento correcto: `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` (0:41:27)

Este es el bloque que el curso **más subestima** («we're not going to use the head that much») y el que
más importa a largo plazo.

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Título de la pestaña</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <h1>Lo visible</h1>
  </body>
</html>
```

### Qué hace cada cosa (y por qué no es opcional)

| Etiqueta | Qué hace | Si falta |
|---|---|---|
| `<!DOCTYPE html>` | Le dice al navegador que es HTML5 | Modo quirks: márgenes y layouts raros |
| `<html>` | La raíz del árbol | El navegador la inventa — pero no confiés |
| `<head>` | Metadatos invisibles | Sin `charset`, los acentos se rompen |
| `<body>` | Todo lo visible | — |

**El `<!DOCTYPE>` es la única que no es una etiqueta.** Arranca con `!` y no cierra. El curso lo dice:
«it's actually not an HTML tag. It's just metadata for the browser».

**Lo que el video no menciona y hoy es obligatorio:**
- **`<meta charset="utf-8">`** — sin esto, `ñ`, `á`, `ü` salen como `Ã±`, `Ã¡`. Es el bug más viejo de
  la web y sigue pasando.
- **`<meta name="viewport" content="width=device-width, initial-scale=1">`** — sin esto, el celular
  renderiza la página como si fuera un monitor de escritorio y la achica. Media web de los 2000 se ve
  así hoy por esto.
- **`<html lang="es">`** — le dice al lector de pantalla en qué idioma leer y a Google en qué idioma
  indexar.

El video es de 2025 y no los menciona; son la diferencia entre "funciona en mi Mac" y "funciona".

### El `<head>` explicado bien

El curso usa el ejemplo de las tarjetas de Twitter: cuando compartís un artículo y sale con un título
y una imagen distintos a los del artículo, eso lo controlan etiquetas del `<head>`.

```html
<meta property="og:title" content="Un título distinto para compartir">
<meta property="og:image" content="imagen-de-preview.jpg">
```

Eso es Open Graph. **No es del curso, es de por qué el `<head>` importa.** Si alguna vez hacés un
portfolio y lo compartís en LinkedIn, el `<head>` decide cómo se ve esa tarjeta. Sin esas etiquetas,
LinkedIn agarra el primer `<h1>` y la primera imagen que encuentra — y a veces no es ninguna.

### LAB 5 — estructura correcta (10 min)

Tomá el `index.html` del LAB 1 y reescribilo con la estructura completa:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mi primer sitio</title>
</head>
<body>
  <h1>I code, therefore I am</h1>
  <p>René Descartes, mal citado</p>
</body>
</html>
```

**Verificación:** escribí `ñandú ácido` en el `<body>`. Si se ve bien, el `charset` está. Si se ve mal,
está de menos o mal ubicado.

**El test del celular:** abrí las DevTools, activá el modo responsive (`Cmd+Shift+M`) y poné un iPhone.
Sin el `viewport`, la página se ve como un monitor achicado. Con él, se ve como un celular.

---

## Bloque 6 · Listas: `<ul>`, `<ol>`, `<li>` (0:46:27)

```html
<ol>          <!-- ordenada: 1, 2, 3 -->
  <li>Noruega</li>
  <li>Alemania</li>
</ol>

<ul>          <!-- sin orden: • • • -->
  <li>Pizza</li>
  <li>Empanadas</li>
</ul>
```

**La regla:** si el orden cambia el significado (un ranking, pasos de una receta) → `<ol>`. Si no
(una lista de compras) → `<ul>`.

**Por qué importa más de lo que parece:** el curso muestra que la barra de navegación de la BBC **es
un `<ul>`** cuyos `<li>` son las categorías. Eso no es casualidad: un menú es una lista de links, y
marcarlo como lista es lo que permite al lector de pantalla decir «lista con 6 elementos» en vez de
leer seis links sueltos. **Cuando hagas un navbar, que sea un `<ul>`.**

### LAB 6 — listas con sentido (8 min)

1. Una lista **ordenada** con los 3 pasos para prender una computadora (el orden importa).
2. Una lista **sin orden** con 4 cosas que tenés en la mesa (el orden no importa).
3. Un "menú" falso: `<ul>` con 3 `<li>`, cada uno con un link a `#`.

**Pregunta:** ¿por qué el menú no es un `<ol>`? Escribí la respuesta.

---

## Bloque 7 · El elemento interactivo: `<button>` (0:21:27)

```html
<button>Comprar</button>
```

Botón nativo, con estilo del navegador, y **clickeable desde el minuto uno**. No necesita JavaScript
para verse ni para reaccionar al click. (Para *hacer* algo con el click, sí hace falta JS — eso es el
Nivel 2.)

**Por qué el curso lo mete en el capítulo de HTML y no en el de JS:** porque el botón es HTML. Lo que
hace el JS es *escuchar* el click, no crear el botón.

**Botón vs link — la distinción que se confunde siempre:**

| | `<a>` | `<button>` |
|---|---|---|
| Qué hace | Navega a otra página | Ejecuta una acción |
| Ejemplo | "Ver más" | "Enviar formulario" |
| Accesible por teclado | Enter | Enter y Espacio |
| Si lo usás mal | Botón que no hace nada | Link que no lleva a ningún lado |

**La regla:** si el click te lleva a otra URL → es un `<a>`. Si hace algo en el lugar → es un
`<button>`.

---

## Bloque 8 · `<input>`: la etiqueta más versátil de HTML (0:26:27)

```html
<input type="text" placeholder="Tu usuario">
<input type="password">
<input type="date">
<input type="time">
<input type="color">
<input type="file">
```

**El atributo `type` es lo que convierte un input en seis cosas distintas.** Y no es sólo cosmético:
un `type="date"` da un calendario y **no deja escribir una fecha inválida**; un `type="email"` valida
automáticamente; un `type="password"` enmascara los caracteres.

**Tabla de los que van a usar:**

| `type` | Para qué | Lo que te da gratis |
|---|---|---|
| `text` | Texto libre | — |
| `password` | Contraseña | Enmascara |
| `email` | Correo | Valida el formato |
| `date` | Fecha | Calendario + validación |
| `time` | Hora | Selector de hora |
| `color` | Color | Picker de color |
| `file` | Archivo | Abre el explorador |
| `number` | Número | Flechas + validación |
| `checkbox` | Sí/no | Estado de marcado |
| `radio` | Elegir uno | Selección exclusiva |

**`placeholder` no es una etiqueta.** El curso lo usa como si lo fuera («enter password» dentro del
input). El placeholder **desaparece al escribir** y el lector de pantalla no lo lee igual que una
etiqueta. Lo correcto:

```html
<label for="user">Usuario</label>
<input id="user" type="text" placeholder="tu@email.com">
```

El `<label for="...">` apunta al `id` del input. Además de accesibilidad, hace que **tocar el texto
enfoque el input** — que es un atajo de usabilidad gratis.

### LAB 7 — formulario de registro (12 min)

Construí un formulario con:

1. `label` + `input type="text"` para nombre de usuario (con `id` y `for` enlazados).
2. `label` + `input type="password"` para contraseña.
3. `label` + `input type="date"` para fecha de nacimiento.
4. `label` + `input type="color"` para el color de perfil.
5. `input type="file"` para foto de perfil.
6. Un `<button>` que diga "Crear cuenta".

**Tarea:** los 6 deben tener `label`. No vale placeholder-como-etiqueta.

**Cuando termines:** intentá tabular por el formulario. Si el foco salta en orden y cada campo se
ilumina, los `label` están bien enlazados.

---

## Bloque 9 · Links: `<a>` y `href` (0:36:27)

```html
<a href="https://google.com">Google</a>
<a href="index.html">Volver al inicio</a>
```

**El `href` es lo que hace que un link sea link.** Sin `href`, es sólo texto con subrayado.

### Ruta relativa vs absoluta — la confusión más común

| | Ejemplo | Cuándo |
|---|---|---|
| Absoluta | `https://google.com` | Siempre apunta al mismo lugar |
| Relativa | `index.html`, `blog.html` | Apunta a un archivo al lado del HTML actual |
| Relativa a subcarpeta | `blog/index.html` | Un nivel abajo |
| Subir un nivel | `../index.html` | Un nivel arriba |

**La regla:** para sitios propios, relativa. Para otros sitios, absoluta. Si usás absoluta para tus
propias páginas (`https://misitio.com/blog.html`), **se rompe en local** — porque todavía no existe
`misitio.com`.

### `target="_blank"`

```html
<a href="https://google.com" target="_blank">Google</a>
```

Abre en pestaña nueva. El curso lo llama «cryptic way of saying that you want the link to open up in a
new tab. I know.»

**Lo que el curso no dice y hoy es best practice:**

```html
<a href="https://google.com" target="_blank" rel="noopener noreferrer">Google</a>
```

Sin `rel="noopener"`, la página destino **tiene acceso a tu `window.opener`** y puede redirigir tu
pestaña original a otra cosa. Se llamó *tabnabbing* y fue un vector de phishing real.

**Pero ojo, verificado contra MDN (2026-11-11):** poner `target="_blank"` **ya implica** `noopener` en
todos los navegadores actuales — «Setting `target="_blank"` on `<a>`, `<area>` and `<form>` elements
implicitly provides the same `rel` behavior as setting `rel="noopener"`». Así que el atributo **no te
protege de nada hoy**: es convención, no defensa.

**Por qué igual conviene escribirlo:** (1) documenta la intención para quien lea el código, (2) si
alguna vez usás un target con nombre distinto, la protección ya está explícita, (3) en una entrevista,
saber que *ya* es implícito es la respuesta que distingue. Decir «lo pongo por seguridad» cuando ya es
el default es repetir un mito.

### LAB 8 — navegación real (10 min)

Creá **dos** archivos: `index.html` y `about.html`.

- `index.html` tiene un link a `about.html` con texto "Sobre mí".
- `about.html` tiene un link a `index.html` con texto "Volver".
- En `index.html`, un link externo a `https://developer.mozilla.org` con `target="_blank"` y `rel`.

**Verificación:** hacé click y volvé. Los dos tienen que funcionar con `file://` abriendo el HTML
directo, sin servidor.

---

## Cierre del Módulo 1: qué te tenés que poder explicar

Antes de pasar a CSS, respondé sin mirar:

1. ¿Qué diferencia hay entre `<h1>` y `<p>` si los dos son "texto"? → *qué le dicen al navegador*
2. ¿Por qué `<img>` no tiene cierre?
3. ¿Qué es un `<div>` y para qué sirve?
4. ¿Por qué la imagen se sale del ancho de la página sin `width="100%"`?
5. ¿Qué hace `<!DOCTYPE html>`?
6. ¿Qué se rompe si falta `<meta charset="utf-8">`?
7. ¿Cuándo `<ol>` y cuándo `<ul>`?
8. ¿`<a>` o `<button>` para "enviar formulario"?
9. ¿Qué hace `target="_blank"` y qué es `rel="noopener"`?
10. ¿Por qué el placeholder no reemplaza al `<label>`?

**Si podés contestar 8 de 10, el módulo está.** El bloque CSS se puede empezar.

---

## Banco de ejercicios (opcional, para muscle memory)

1. Rehacer el Google clone del curso: `<img>` del logo, `<input>` (¿de qué tipo?), dos `<button>`.
2. Una página de receta: `<h1>`, `<img>`, lista `<ul>` de ingredientes, `<ol>` de pasos.
3. Un `about.html` con tu bio: `<h1>`, `<h2>` de sección, `<p>`, `<ul>` de intereses, link a LinkedIn
   con `target="_blank"`.
4. **Romper a propósito:** sacá el `doctype`, guardá, refrescá. ¿Notás algo? Sacá el `charset` y escribí
   `ñ`. ¿Qué pasa?
5. Contar los divs anidados en la navbar de la BBC. (Ejercicio de arqueología del LAB 4.)

---

## Lo que este módulo NO cubre (y va en el Bloque CSS)

- **Cómo se *ven* las cosas.** Todo el estilo del navegador por defecto. Hasta acá, el HTML se ve
  feo y no hay forma de cambiarlo.
- **Semántica de verdad.** El curso usa `<div>` para todo. En producción se usan `<main>`, `<nav>`,
  `<article>`, `<section>`, `<header>`, `<footer>` — que además ayudan a los lectores de pantalla a
  navegar por regiones. Van en el anexo de esta clase.
- **Accesibilidad formal.** El video menciona `alt` de pasada (creo que ni lo menciona). Sin `alt`, una
  imagen es invisible para quien usa lector de pantalla. Es obligatorio.

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
