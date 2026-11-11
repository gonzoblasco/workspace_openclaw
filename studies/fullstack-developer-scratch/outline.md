# Outline — Become a Fullstack Developer from Scratch

**Curso:** *Become a Fullstack Developer from Scratch – Full Beginner's Tutorial* · freeCodeCamp.org (curso original de Scrimba)
**Video:** https://www.youtube.com/watch?v=LzMnsfqjzkA · **47:29:20** · publicado 2025-10-01
**Ruta interactiva:** https://scrimba.com/fullstack-path-c0fullstack · **Código de los retos:** https://github.com/scrimba/learn-fullstack-development

---

## Cómo usar esta clase

Es el curso más largo del catálogo (47,5 h; 530.000 palabras de transcript; 34 capítulos oficiales). **No se hace de una sentada, y no está pensado para eso.** Es una ruta por niveles: cada bloque es autosuficiente y el anterior es prerequisito del siguiente.

**El eje del curso es *hacer*, no leer.** Todo se enseña construyendo: 12 proyectos guiados, 4 proyectos "solo" (sin andamiaje) y ejercicios entre módulo y módulo. La clase sigue esa estructura porque el aprendizaje está en el tecleo, no en el apunte.

**Mapa de niveles:**

| Nivel | Capítulos | Duración | Qué habilita |
|---|---|---|---|
| **1 · Fundamentos web** | HTML y CSS → Birthday website | ~5,4 h | Escribir una página estática desde cero |
| **2 · JavaScript** | Counter app → Chrome extension | ~15 h | Lógica, DOM, eventos, estado |
| **3 · Precisión JS** | Command line → Asynchronous JS/APIs | ~4,9 h | Entender el runtime antes de usarlo (event loop, scope, módulos) |
| **4 · IA y backend** | AI engineering → Fullstack Node app | ~3,4 h | Servir datos propios por HTTP |
| **5 · Datos y persistencia** | Databases → Writing SQL queries | ~1,9 h | Modelar y consultar |
| **6 · React** | Static pages → Side effects | ~10,5 h | Construir UI con estado |
| **7 · Cierre y escala** | Capstone → Rendering strategies | ~7,3 h | TypeScript, React tipado, Next.js |

**Nota sobre el capítulo 16:27:18** — "Advanced foundations / Methods and loops": la descripción del video avisa que es un duplicado y remite a un video aparte (`youtu.be/m6xM7Ezxn1E`). Verificado en el transcript: 16:27:18 arranca con el **recap** de Advanced foundations («we looked in detail at the event loop…», `(16:27:18)`) y el contenido real sigue desde 16:33:20 (ternarios y condicionales). Lo mismo en 17:41:43, que es otro recap y retoma en 17:53:20. **No se pierde contenido**: el material de "Methods and loops" sigue ahí después del recap.

---

## Bloque 0 · Qué es este curso (0:00:00 – 0:01:27)

Presenta la ruta completa: «We're going to start out with the basics of HTML, CSS, JavaScript, and so forth, and then move on to the frameworks and technologies that are used in the industry like React, Node, Next, SQL, TypeScript, testing, and even AI engineering»` `(00:00:56)`.

**Contrato del curso:** es una ruta de *fullstack developer*, no un curso de una tecnología. El orden no se elige: cada sección da por sentado que hiciste la anterior.

- **Objetivo:** terminar con capacidad de construir y desplegar una app completa (front + back + datos).
- **Ejercicio:** abrir la ruta interactiva en Scrimba y el repo de código; tener ambos a mano antes de la primera línea.

---

## Nivel 1 · Fundamentos web (0:01:27 – 5:22:25)

### Módulo 1 · HTML y CSS (0:01:27 – 1:04:19 · 63 min)

El capítulo más largo de fundamentos. Parte de cero: escribir la frase en un archivo de texto, envolverla en etiquetas, renderizarla en el navegador, y de ahí a la página de Google construida por partes.

**Contenido:** qué es un elemento y una etiqueta · atributos (`href`, `src`, `type="file"`) · `input` como **void tag** («It should only have an opening tag… self-closing tags», `(10:47:02)`) · `button` vs `input` · indentación y estructura · DevTools e inspector · `div` como caja universal · reproducir el homepage de Google · el primer `type="file"` para subir imagen.

**Práctica:** construir el homepage de Google. Es el primer proyecto real del curso y la primera vez que el resultado se ve en el navegador.

**Ejercicio:** escribir la página de Google sin mirar la solución y comparar con la del curso.

---

### Módulo 2 · Intro a CSS (1:04:19 – 2:21:01 · 77 min)

CSS sobre el mismo proyecto: el homepage de Google, ahora sí con estilos.

**Contenido:** qué es una hoja de estilos en cascada · selectores (elemento, clase, id) · la especificidad sin nombre todavía · `display: block/inline` · centrar con flexbox · margen, padding, border · `border-radius` · `font-weight`, `font-size`, `font-family` · Google Fonts · el caso del botón: por qué necesita `border: none` y `border-radius` para dejar de parecer un botón del navegador (`(0:08:18)`).

**Idea fuerza:** el navegador trae estilos por defecto y hay que apagar los que no se quieren. Un botón sin `border: none` es un botón de 1998.

**Ejercicio:** identificar tres estilos por defecto del navegador que se están revirtiendo en el proyecto.

---

### Módulo 3 · Tarjeta de presentación (2:21:01 – 3:32:02 · 71 min)

Segundo proyecto CSS: una *business card* personalizable.

**Contenido:** diseño antes de código · paleta de colores · selector de clases y por qué la clase gana a la etiqueta · flexbox a fondo: `justify-content`, `align-items`, `gap` · `border` y `border-radius` con criterio · jerarquía tipográfica · imágenes con `alt` · layout horizontal imagen + texto.

**Idea fuerza:** flexbox es el instrumento por defecto para alinear en una dimensión. Se aprende usándolo, no memorizando propiedades.

**Ejercicio:** personalizar la tarjeta con nombre, rol y paleta propios; no copiar el ejemplo.

---

### Módulo 4 · Sitio de exploración espacial (3:32:02 – 4:17:21 · 45 min)

Tercer proyecto CSS, el primero con movimiento y con fuentes externas.

**Contenido:** imagen de fondo con animación · Google Fonts aplicadas al proyecto (`(3:45:01)`) · `text-shadow` para legibilidad sobre imagen · `text-decoration: underline` customizado · contraste texto/fondo · efectos CSS sin JavaScript.

**Ejercicio:** cambiar la imagen de fondo por una propia y verificar que el texto sigue legible sin retocar el `text-shadow`.

---

### Módulo 5 · Sitio de cumpleaños (4:17:21 – 5:22:25 · 65 min)

Cuarto proyecto CSS: una página de regalo con interacción.

**Contenido:** estructura semántica de página · `header` y contenido principal · **hover como mecanismo de revelación**: la imagen cambia al pasar el mouse · imágenes como regalos · composición y espaciado · reutilizar el mismo HTML para cualquier persona cambiando los datos.

**Idea fuerza:** el estado del puntero ya es interacción. No hace falta JavaScript para un efecto de revelación.

**Ejercicio:** adaptarlo para una persona real con tres regalos y verificar que el hover revela la imagen correcta en cada uno.

---

### Módulo 6 · Proyecto solo: homepage de tu ciudad (5:22:25 – 5:30:38 · 8 min)

**Primer proyecto sin andamiaje.** El instructor lo dice sin rodeos: «I'm going to remove the training wheels and you will have to build a full project on your own because that's actually the only way you can know whether or not you've truly learned HTML and CSS»` `(05:22:36)`.

- **Requisitos:** homepage de la ciudad natal, diseño propio, light mode.
- **Lo que evalúa:** si el bloque de fundamentos quedó.

**Ejercicio:** hacerlo **sin** mirar el capítulo anterior. Si no sale, volver a los módulos 1–5 en vez de avanzar: el curso no da nada por perdido, pero el módulo 7 asume esto.

---

## Nivel 2 · JavaScript (5:30:38 – 14:00:48)

### Módulo 7 · App contadora (5:30:38 – 6:46:17 · 76 min)

Primer JavaScript del curso, con un proyecto trivial a propósito (*passenger counter*).

**Contenido:** `console.log` · variables (`let`), `const` · `document.getElementById` · `.textContent` / `.innerText` · `onclick` y funciones · `count += 1` · escribir el estado a la página en vez de solo a la consola · el DOM como árbol que se recorre y modifica.

**Idea fuerza:** el estado vive en una variable y la página es una proyección de ese estado. Es la primera vez que aparece el patrón que domina todo el resto del curso.

**Ejercicio:** agregar un botón de decremento y otro de reset sin copiar el código existente.

---

### Módulo 8 · Retos de JavaScript · parte 1 (6:46:17 – 7:07:22 · 21 min)

Ejercicios rápidos: variables, concatenación, `fullName`, operaciones aritméticas, logs.

**Formato:** challenge → solución → próxima. Sin teoría nueva.

**Ejercicio:** resolver antes de ver la solución y medir cuántos salieron sin mirar.

---

### Módulo 9 · Git y GitHub básicos (7:07:22 – 7:19:59 · 13 min)

Primer contacto con control de versiones y con **desplegar**.

**Contenido:** qué es un repositorio · descargar el proyecto · `git` como línea de tiempo local · subir a GitHub · **Netlify** para poner el proyecto en la web (`(7:20:00)`, en el capítulo siguiente, cierra con la URL de Netlify).

**Idea fuerza:** un proyecto que no está en internet no cuenta como terminado. El curso despliega cada proyecto "solo" en cuanto lo termina.

**Ejercicio:** publicar el homepage de tu ciudad y tener la URL a mano.

---

### Módulo 10 · Blackjack (7:19:59 – 10:15:19 · 175 min)

**El capítulo más largo del curso** después de React state. Un juego real con estado compuesto.

**Contenido:** arrays y objetos como estructura de carta · funciones con `return` y **hoisting** de function declarations: «the function gets so-called hoisted to the top, meaning that it's accessible even at line one»` `(09:13:36)` · `Math.random()` y `Math.floor()` para repartir cartas · acumular puntaje · comparar puntajes y decidir ganador · `querySelector`, `createElement`, `appendChild` · render dinámico: construir el HTML desde datos en vez de tenerlo escrito · `textContent` vs `innerHTML` · sumar cartas vs mostrar cartas son dos cosas distintas.

- **Objetivo:** dejar de escribir HTML fijo y pasar a generarlo desde el estado.
- **Señal de que el módulo funcionó:** se puede explicar por qué `start game` sirve también después de repartir una carta (`(8:20:00)`).
- **Ejercicio:** agregar la regla de que el As vale 1 u 11 según convenga. Sin mirar la solución del curso.

---

### Módulo 11 · Retos de JavaScript · parte 2 (10:15:19 – 10:41:09 · 26 min)

Objetos y funciones: crear `{name, age, country}`, acceder a propiedades, funciones que devuelven objetos.

**Ejercicio:** escribir un objeto que represente a una persona y tres funciones que lo consuman.

---

### Módulo 12 · Extensión de Chrome (10:41:09 – 13:34:25 · 173 min)

Segundo proyecto grande de JS, y el más distinto: software que corre **dentro del navegador del usuario**.

**Contenido:** qué es y para qué sirve una extensión (`(10:41:14)`) · `manifest.json` y permisos · abrir extensiones en modo desarrollador · `input` + botón "Guardar" · guardar en `localStorage` · renderizar una lista de links desde `localStorage` al abrir · `innerHTML` con `+=` para acumular filas (`(11:23:20)`) · **`delete` con `event.target`** · template strings y por qué hay que escapar las comillas del `href` (`(11:40:02)`) · URL de extensión y recarga · el navegador como plataforma.

**Idea fuerza:** `localStorage` solo guarda strings. Un array hay que serializarlo para guardarlo y parsearlo al leerlo.

**Ejercicio:** agregar un botón de "borrar todo" que vacíe la lista y `localStorage` en una sola acción.

---

### Módulo 13 · Retos de JavaScript · parte 3 (13:34:25 – 14:00:48 · 26 min)

Último bloque de retos antes de la sección "avanzada": arrays, métodos, repetición. El instructor lo justifica: «you need tons of repetition. These things take a lot of time to really get into your muscle memory»` `(13:34:38)`.

**Ejercicio:** repetir el bloque de retos al día siguiente sin mirar ninguno.

---

## Nivel 3 · Precisión (14:00:48 – 19:42:29)

### Módulo 14 · Línea de comandos (14:00:48 – 14:46:27 · 46 min)

**Contenido:** qué es una terminal · shell (bash/zsh) · `pwd`, `ls`, `cd`, `mkdir` · rutas absolutas vs relativas · `..` para subir un nivel (`(14:43:20)`) · `touch`, `rm` · **redirección `>` y append `>>`** (ejemplo real: `cat external/people.txt >> ./about-the-game/team-members.txt`, `(14:43:00)`) · por qué esto importa a un dev: todo lo que hace un proyecto pasa por un shell.

**Nota del curso:** el autor avisa que la sección 2 de línea de comandos todavía estaba en producción al grabar (`(14:46:27)`). Lo que hay es completo para empezar, no exhaustivo.

**Ejercicio:** crear una carpeta de proyecto y un archivo, moverlo de carpeta y escribir su contenido en otro archivo usando solo la terminal.

---

### Módulo 15 · Git y GitHub esenciales (14:46:27 – 15:12:55 · 26 min)

Git como herramienta profesional, no como botón.

**Contenido:** repo local vs remoto · `git init`, `add`, `commit` («a commit is… and write a commit message», `(14:46:35)`) · `git log` · ramas · `push` y `pull` · resolver el caso de estar detrás del remoto · cómo cambia el flujo cuando hay más de un desarrollador (`(15:12:55)`).

**Idea fuerza:** un commit es un punto de restauración con intención. El mensaje no es un trámite.

**Ejercicio:** hacer tres commits atómicos en el proyecto de blackjack con mensajes que expliquen el *por qué*, no el *qué*.

---

### Módulo 16 · Fundamentos avanzados de JS (15:12:55 – 16:27:18 · 74 min)

El capítulo que separa a quien "sabe JavaScript" de quien **entiende** JavaScript. Sin tema único a propósito: «really need to understand before your JavaScript» `(15:13:39)`.

**Contenido:**
- **Template strings** y interpolación.
- **Destructuring de objetos**: «object destructuring enables us to» `(15:31:27)` — y el resultado es código más DRY.
- **Módulos**: `import` / `export`, la diferencia con `require`, y la regla de que **solo puede haber un `default export` por archivo** (`(15:58:20)`).
- **El heap, la call stack y el event loop**: «we're just logging out first, second» `(15:44:07)`. JavaScript es single-threaded y el event loop es lo que le permite no bloquear.
- **Scope y hoisting.**
- **Constructores nativos**: `Date`, `Error`.
- **Números**: pre-incremento, `BigInt`, separadores numéricos (`1_000_000`).

**Idea fuerza:** el event loop explica por qué el `setTimeout` no corre "después de la línea siguiente", sino cuando la pila está vacía. Es el fundamento de todo lo async que viene después.

**Ejercicio:** dibujar el orden exacto de ejecución de un script con `setTimeout`, una promesa y un log. Después correrlo y verificar.

---

### Módulo 17 · Methods and loops (16:27:18 – 17:41:43 · 74 min)

> ⚠️ **Capítulo duplicado según la descripción del video.** Verificado: los primeros ~6 minutos son el recap de Fundamentos avanzados; el contenido nuevo arranca en 16:33:20 con ternarios y condicionales, y sigue hasta 17:41:16. Para "Methods and loops" propiamente dicho, freeCodeCamp remite a `https://youtu.be/m6xM7Ezxn1E`.

**Contenido (lo que sí está acá):** ternarios y cuándo **no** usarlos («complex turnaries really can be very hard to» `(15:25:39)`) · condicionales compuestos y el error de la anidación · truthy/falsy: los **seis** valores falsy (`false`, `0`, `""`, `null`, `undefined`, `NaN`, `(12:30:16)`) · bucles `for`, `for…of`, `while` · qué se itera y qué no.

**Ejercicio:** reescribir un ternario anidado de tres niveles como `if/else` y comparar legibilidad.

---

### Módulo 18 · Expresiones de función y parámetros (17:41:43 – 18:26:57 · 45 min)

> ⚠️ Igual que el anterior: 17:41:43 a 17:53:20 es otro recap. El contenido nuevo empieza en 17:53:20.

**Contenido:** declaración de función vs expresión de función vs **arrow function** («see is an arrow function which is all on» `(17:47:16)`) · cuándo la arrow con `return` implícito · parámetros por defecto · **parámetro rest** (`...args`) y su diferencia con `arguments` · que las funciones son valores.

**Idea fuerza:** una función es un valor como cualquier otro. De ahí salen callbacks, métodos de array y todo React.

**Ejercicio:** reescribir una función declarada como arrow con retorno implícito, sin cambiar el comportamiento, y probarla.

---

### Módulo 19 · JavaScript asíncrono y APIs (18:26:57 – 19:42:29 · 76 min)

**Contenido:** qué es una API — «any tool that will help connect your program with someone else's program»` `(18:30:06)` · HTTP: métodos, códigos de estado (200, 404, 500) · qué es JSON · **`fetch`** («we start with the fetch method and we need to pass it a string containing the URL», `(18:53:21)`) · `.then()` encadenado y `.catch()` · promesas: qué resuelven y qué rechazan · consumir una API real (dog API) · renderizar la respuesta · el patrón de esperar la respuesta antes de tocarla.

**Idea fuerza:** `fetch` devuelve una promesa, no los datos. La respuesta y el JSON son **dos** esperas.

**Ejercicio:** llamar a la dog API y renderizar una imagen; después encadenar `.catch()` y comprobar que un URL roto muestra el error en vez de fallar en silencio.

---

## Nivel 4 · IA y backend (19:42:29 – 24:52:41)

### Módulo 20 · Fundamentos de ingeniería de IA (19:42:29 – 21:19:42 · 97 min)

**El capítulo que no estaba en un curso fullstack de hace tres años.** Construye una app que usa un modelo de lenguaje, sin framework de por medio.

**Contenido:** qué es un LLM y por qué cambió todo en 2022 (`(19:43:00)`) · `fetch` contra la API de un modelo · el **system prompt** y el rol de instrucción · **`temperature`**: «temperature controls how daring output» `(20:30:26)` — más temperatura = más creatividad, hasta que se rompe · tokens y `max_tokens` · stop sequences, presence penalty y frequency penalty (`(21:19:42)`) · construir la app de recetas (o similar) que genera contenido con IA.

**Idea fuerza:** la temperatura no es un parámetro técnico, es una decisión de producto. Bajarla para outputs deterministas, subirla cuando importa la variedad.

**Ejercicio:** correr el mismo prompt tres veces con `temperature` 0,2 y tres con 1,2; anotar qué se rompe y en qué punto.

---

### Módulo 21 · Construir una Node API (21:19:42 – 22:42:51 · 83 min)

Primer servidor propio. El cambio de mentalidad del capítulo es total: hasta acá el código corría en el navegador de otro; ahora corre en una máquina que espera pedidos.

**Contenido:** qué es Node.js y por qué permite correr JS fuera del navegador · `npm` y `package.json` · **Express** — «here is that Express.js exists. It's a» `(21:24:05)` — · `app.get()` y `app.post()` · responder con JSON · parámetros de ruta (`/api/continent/africa`) · filtrar datos en el servidor (`(22:13:20)`) · códigos de estado correctos · por qué autenticación es un tema aparte y no entra acá (`(22:42:51)`).

**Ejercicio:** agregar un endpoint que filtre por país además de por continente, y devolver 404 cuando no hay resultados.

---

### Módulo 22 · Construir una app fullstack con Node (22:42:51 – 24:52:41 · 130 min)

**Módulo bisagra:** el front que ya sabe hacer (HTML/CSS/JS) se junta con el back que acaba de construir.

**Contenido:** estructura de proyecto fullstack · servir archivos estáticos desde Node · `import.meta.url` vs `__dirname` y **ES modules vs CommonJS** (`(23:27:20)`): «Dur name is not defined in ES module scope. So this fails and using modular JavaScript has made our lives slightly more complicated because now as we know we need to access these from import meta»` `(23:28:32)` · enviar un **buffer** en vez de un string UTF-8 y por qué («browsers are able to interpret buffers correctly using the content type header», `(23:20:00)`) · front y back en el mismo repo · `npm start` y verificar en la pestaña Network.

**Idea fuerza:** servir un archivo no es "mandar texto"; es mandar bytes con un `Content-Type` que el navegador interpreta. Entender eso ahorra horas de debugging de caracteres raros.

**Ejercicio:** levantar la app con `npm start`, abrir DevTools en Network y ver el `Content-Type` de la respuesta del HTML. Después romperlo a propósito y ver la diferencia.

---

## Nivel 5 · Datos (24:52:41 – 26:30:04)

### Módulo 23 · Introducción a bases de datos (24:52:41 – 25:13:25 · 21 min)

**Contenido:** qué es una base de datos y por qué no alcanza un JSON · **SQL vs NoSQL**: relacional (tablas, filas, columnas) contra documental · **MongoDB como document store**: «Data is stored in documents,» `(25:00:30)` · cuándo cada modelo.

**Idea fuerza:** la elección de DB no es técnica antes que económica. Una managed es barata al principio y cara al escalar; una self-hosted es lo contrario y agrega la carga operativa.

**Ejercicio:** escribir en una frase por qué tu próximo proyecto usaría SQL y por qué usaría documental.

---

### Módulo 24 · Escribir consultas SQL (25:13:25 – 26:30:04 · 77 min)

**Contenido:** `SELECT` y `FROM` — «start with the select keyword and then» `(25:19:42)` · columnas específicas vs `*` · `WHERE` · operadores de comparación · `LIKE` y `%` para coincidencias parciales (`(25:50:24)`) · `AND` y `OR`, y el error de la precedencia: los paréntesis no son opcionales cuando se mezclan (`(25:50:01)`) · `BETWEEN` · `IN` · `ORDER BY` · `LIMIT`.

**Idea fuerza:** un `WHERE` sin paréntesis con `AND` y `OR` mezclados no filtra lo que parece. Es un bug silencioso, no un error.

**Ejercicio:** consulta sobre la tabla `cars`: marca, modelo, precio y `sold`; mostrar solo autos no vendidos con precio < 50.000, filtrando por dos marcas y ordenando por precio.

---

## Nivel 6 · React (26:30:04 – 38:05:49) ≈ 11,6 h

### Módulo 25 · Páginas estáticas (26:30:04 – 28:48:33 · 139 min)

**El capítulo que explica por qué existe React**, y no lo esconde: arranca con el problema de la navegación y el HTML copiado.

**Contenido:** el problema del navbar duplicado en cada HTML — «the first 30 something or more lines of code were dedicated to a navigation bar»` `(27:13:31)` · componentes y composición · JSX y por qué se parece a HTML sin serlo · `React.createElement` y qué produce en realidad («returning JavaScript objects… Those objects then describe what React should be placing on the page», `(28:48:35)`) · montar React en un proyecto: `createRoot` desde `react/client` (`(26:43:20)`) · renderizar en el DOM · el root y el árbol de componentes.

**Idea fuerza:** JSX es azúcar sobre `React.createElement`, que devuelve objetos. Entenderlo convierte React de magia en datos.

**Ejercicio:** escribir un componente en JSX, y después el mismo componente con `React.createElement`. Comparar.

---

### Módulo 26 · Data driven (28:48:33 – 31:03:00 · 134 min)

**Contenido:** el salto de HTML fijo a UI generada desde datos · **props** — «this is where the concept of props comes» `(29:11:44)` · renderizar arrays de componentes (`.map()`) · la `key` y por qué importa · componentes que reciben datos y devuelven markup · composición anidando componentes (App → Card → Badge).

**Idea fuerza:** un componente es una función de datos a UI. Con eso, el front deja de ser una serie de páginas y pasa a ser un programa.

**Ejercicio:** convertir una lista escrita a mano en `.map()` sobre un array de objetos. Después agregar un elemento al array y verificar que no hace falta tocar el JSX.

---

### Módulo 27 · React state (31:03:00 – 36:17:02 · **314 min**, el más largo del curso)

**El capítulo central de la sección.** Todo el resto de React depende de esto.

**Contenido:** `useState` y el par `[valor, setter]` · **por qué el setter y no asignación directa**: React no sabe que cambió el estado si no se le avisa · el **setter con función** — «we provide a callback function. In the body of this callback function, we need to return the new value that we want state to be on the next render»` `(32:13:31)` — y cuándo hace falta (actualizaciones basadas en el valor anterior) · render como **función del estado** («the UI or what the user sees should be a function of the state», `(36:02:00)`) · renders innecesarios y por qué no se muta el estado · levantar el estado: el problema del star component — «how might we be able to add some functionality back to our star component so that clicking it will then change the state that lives here inside of app»` `(34:43:28)` · **callback props** (`onToggle`) contra estado local · formularios controlados: `onSubmit`, `action`, reset del form (`(33:20:00)`) · listas dinámicas y agregar elementos.

**Idea fuerza:** el estado no se modifica, se reemplaza. Y cuando dos componentes necesitan el mismo estado, el estado sube al ancestro común.

**Ejercicios (el capítulo trae varios):**
1. Contador con setter funcional: dos clicks seguidos deben dar 2, no 1.
2. Levantar el estado del star a App y pasar el callback por props.
3. Formulario que agrega un ingrediente a una lista y se resetea solo.

---

### Módulo 28 · Efectos secundarios (36:17:02 – 38:05:49 · 109 min)

**Contenido:** qué es un efecto secundario y por qué no va en el render · **`useEffect`** — «use effect, but I kind of want to take» `(36:26:15)` · el callback y **el array de dependencias** (`[]` = una vez) · `fetch` dentro de `useEffect` (`(37:17:16)`) · limpieza y la función de cleanup · condicionales en el render según estado · el patrón de loading/error · por qué un `fetch` en el cuerpo de un componente es un loop infinito.

**Idea fuerza:** el array de dependencias no es un detalle de sintaxis: es la declaración de "de qué depende esto". Vacío = no depende de nada = corre una vez.

**Ejercicio:** componente que hace `fetch` de una API con `useEffect([])`, estado de carga, estado de error, y renderizado condicional de los tres.

---

## Nivel 7 · Cierre y escala (38:05:49 – 47:29:20)

### Módulo 29 · Proyecto capstone (38:05:49 – 40:12:26 · 127 min)

**Proyecto integrador de React**, sin instrucción nueva: es el examen práctico de los módulos 25–28.

**Contenido:** una app completa con estado, efectos, listas y formularios · un juego de palabras con chequeo de letras (`(39:10:00)`, ejemplo con `split` y `every`) · el ciclo completo: diseño → estado → handlers → efectos → pulido de UI · «We have come to the end of the new instruction in this course»` `(38:06:11)` — de acá en adelante todo es consolidación o expansión.

**Ejercicio:** hacerlo completo antes de mirar el siguiente módulo. Es el único cierre real de la sección React.

---

### Módulo 30 · Fundamentos de TypeScript (40:12:26 – 42:15:21 · 123 min)

**Contenido:** qué problema resuelve TS y por qué se adopta en equipo (`(40:12:26)` remite a un curso de React avanzado como siguiente paso natural) · tipos primitivos · `type` e `interface` · tipado de funciones: parámetros y retorno (`(40:25:01)`) · **union types** (`(41:15:01)`) · optional chaining · tipar un objeto y por qué el compilador ayuda antes de correr · el proyecto del restaurante de pizza como vehículo: arreglar warnings de `orderQ.P` (`(41:06:20)`).

**Idea fuerza:** TypeScript no cambia lo que corre; cambia lo que se sabe antes de correr. Los errores se mudan del runtime al editor.

**Ejercicio:** tipar el array de órdenes con `type Order`, y hacer que el compilador rechace un objeto mal formado.

---

### Módulo 31 · TypeScript en React (42:15:21 – 43:06:47 · 51 min)

**Contenido:** tipar props de componentes · tipar el retorno de un evento handler (`(42:15:00)`) · `JSX.Element` como tipo de retorno · tipar el estado con `useState<T>` · tipado del `onChange` y del evento de formulario · componentes tipados sin perder la legibilidad.

**Ejercicio:** tipar un componente de input con `onChange`, sin `any`.

---

### Módulo 32 · Construir una app Next.js (43:06:47 – 45:08:21 · 122 min)

**Contenido:** qué es Next.js y qué agrega sobre React · crear la app a mano para entender el mínimo — «We did it the» `(45:08:21)` · después `create-next-app` como camino estándar · **file-based routing**: un archivo `page.tsx` = una ruta (`(43:53:20)`) · `export default` obligatorio en cada page · `layout.tsx` y el `children` — «this children here is actually the contents of our page component»` `(43:20:02)` · `usePathname` y nav activo (`(46:06:00)`) · route params (`/about/:category`) y el caso de una categoría que no existe (`(45:23:20)`).

**Idea fuerza:** en Next, la estructura de carpetas **es** el router. Crear una ruta es crear un archivo.

**Ejercicio:** agregar `/about/[category]` y que muestre la categoría de la URL; escribir qué pasa si la categoría no existe.

---

### Módulo 33 · Estrategias de renderizado y más (45:08:21 – 47:29:20 · 141 min)

**El cierre conceptual del curso.** El módulo que explica *por qué* Next existe.

**Contenido:** **client-side rendering** (CSR) y su costo · **pre-rendering en build time** · **renderizado a request time** — «This means that the HTML gets rendered on» `(46:23:20)` · `use client` y la frontera cliente/servidor («require client side variables», `(46:01:40)`) · pasar datos a componentes cliente · el límite del proyecto actual: datos desde JSON, no desde una DB real (`(46:58:20)`) · qué sigue después del curso.

**Idea fuerza:** la misma app se puede renderizar en tres momentos distintos (en el servidor al compilar, en el servidor al pedido, en el cliente). Elegir cuándo es la decisión de arquitectura central del front moderno.

**Ejercicio:** para cada una de estas tres pantallas, elegir la estrategia y justificar en una frase: un blog de artículos, un dashboard de tu cuenta, un buscador que responde al tipeo.

---

## Banco de preguntas

1. ¿Por qué un `input` no necesita etiqueta de cierre y un `button` sí?
2. Un botón nativo del navegador se ve distinto al de un diseño. ¿Qué dos propiedades lo alinean y por qué el navegador las pone por defecto?
3. En flexbox, ¿qué hace `justify-content` y qué hace `align-items`? ¿En qué eje actúa cada uno?
4. El proyecto de cumpleaños revela imágenes sin JavaScript. ¿Qué propiedad CSS hace el trabajo y cuál es el estado que representa?
5. En la app contadora, el número se actualiza en pantalla. ¿Dónde vive ese número y qué relación tiene con lo que se ve?
6. Explicá el hoisting de las function declarations con un ejemplo donde la llamada aparece antes de la definición.
7. En blackjack, ¿por qué usar `innerHTML` para acumular filas es aceptable acá y en una app de producción habría que pensarlo mejor?
8. `localStorage` guarda strings. ¿Qué hay que hacer para guardar un array de objetos y cómo se recupera?
9. ¿Qué diferencia hay entre `>` y `>>` en la terminal? ¿Qué pasa con el archivo si usás el equivocado?
10. ¿Cuál es la diferencia entre un commit y un push? ¿Cuándo conviene cada uno?
11. Un template string interpola `href="..."`. ¿Por qué hay que usar comillas simples dentro y cómo se ve el error si no?
12. ¿Cuántos `default export` puede tener un archivo y qué error tira si hay dos?
13. Explicá por qué `setTimeout(fn, 0)` no se ejecuta antes de la línea siguiente, aunque el tiempo sea cero.
14. Nombrá los seis valores falsy de JavaScript. ¿Qué pasa con `"0"` y con `[]`?
15. Un ternario de tres niveles anidados funciona. ¿Por qué el curso dice que igual hay que refactorizarlo?
16. ¿Cuál es la diferencia entre parámetros por defecto y el parámetro rest? ¿Qué problema resuelve cada uno?
17. `fetch()` no devuelve datos. ¿Qué devuelve y cuántas esperas hacen falta para llegar al JSON?
18. En la API own, ¿qué devuelve el servidor si el cliente usa `PUT` y no está implementado? ¿Por qué importa?
19. ¿Qué es un buffer y por qué un servidor manda un buffer en vez de un string UTF-8?
20. ¿Cuándo elegís una base managed y cuándo una self-hosted? ¿Cuál es el trade-off económico?
21. Escribí una consulta que devuelva solo los autos no vendidos de dos marcas, menos de 50.000, ordenados por precio. ¿Dónde van los paréntesis y qué pasa si los sacás?
22. ¿Por qué React no "sabe" que el estado cambió si lo asignás directamente?
23. ¿Cuándo hay que usar la forma funcional del setter (`setCount(c => c + 1)`) y cuándo alcanza `setCount(count + 1)`?
24. ¿Qué significa que "la UI sea una función del estado" en la práctica? Da un ejemplo del curso.
25. Un componente hace `fetch` en el cuerpo (no en `useEffect`). ¿Qué pasa y por qué?
26. ¿Qué declara el array de dependencias de `useEffect`? ¿Qué significa `[]`?
27. ¿Qué aporta TypeScript que JavaScript no puede dar, y qué NO cambia?
28. En Next.js, ¿cómo se crea una ruta nueva? ¿Qué archivo y qué export necesita?
29. Diferenciá las tres estrategias de renderizado y da un caso de uso para cada una.
30. ¿Por qué el curso dice que el capítulo 16:27:18 es un duplicado y adónde remite?

---

## Lo que el curso NO cubre

- **Testing.** Aparece en el sumario de la presentación (`(0:00:66)`) pero no es un capítulo de este video: no hay capítulo de tests. No lo da por hecho.
- **Autenticación y seguridad.** El módulo 21 lo declara fuera de alcance explícitamente (`(22:42:51)`). Un fullstack real lo necesita igual.
- **Deploy en producción.** Netlify aparece para el proyecto estático (módulo 9), pero no hay pipeline, Docker, ni deploy de la app fullstack con DB.
- **Base de datos conectada al backend.** El módulo 33 lo dice: los datos vienen de JSON, no de una DB real (`(46:58:20)`).
- **CSS fuera de flexbox:** grid se menciona de pasada y se remite a otro curso (`(35:50:20)`).
- **Accesibilidad.** Sólo se menciona `alt` en imágenes; no hay un módulo de a11y (relevante si venís del `cpacc-completo` de este workspace).
- **Profundidad en HTML semántico:** `div` es la herramienta por defecto del curso; `main`, `nav`, `article`, `section` no se tratan con criterio.

---

## Notas editoriales

- **Fuente:** subtítulos automáticos `en-orig` de YouTube, 73.728 cues deduplicados. No es ASR local; los errores son los del caption de YouTube. Glosario de errores en el encabezado de `transcripcion.md`.
- **El curso es de Scrimba, no de freeCodeCamp:** freeCodeCamp publica la ruta de Scrimba entera. Los nombres de instructores que el ASR deforma (Per Borgen — CEO de Scrimba —, Bob Ziroll, Rachel Johnson, Treasure) se identifican por contexto y se citan por lo que el transcript muestra.
- **Los capítulos 16:27:18 y 17:41:43 son recaps**, verificados en el transcript. La descripción de YouTube solo advierte del primero.
- **Vigencia:** el curso es de octubre de 2025. Las versiones de React, Next.js y TypeScript que enseña son las de ese momento; cualquier ejercicio que dependa de una versión concreta hay que re-verificarlo contra la documentación antes de darlo por bueno. La API de OpenAI que usa el módulo 20 también es mutable.
- **Duración:** 47:29:20. Un curso de esta longitud se estudia por niveles, no de corrido; el mapa de niveles de arriba es el orden recomendado.
<!-- project: github.com/gonzoblasco/workspace_openclaw -->
