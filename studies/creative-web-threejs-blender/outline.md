# Clase: Creative Web Development with Three.js and Blender — 3D Portfolio for Beginners

- Fuente: https://www.youtube.com/watch?v=yhtdkuw9mbM
- Canal: freeCodeCamp.org
- Expositor: **Andrew Woan** (@andrewwoan) — confirmado en la descripción oficial; el ASR lo escribe «Andrew Won»
- Duración: 05:39:21
- Fecha: 2025-11-03
- Idioma: inglés (captions automáticos `en-orig`)
- Transcripción: [`transcripcion.md`](transcripcion.md)
- Código del curso: https://github.com/andrewwoan/bellas-park · demo: https://www.bellas-park.com/
- Capítulos oficiales: 36 en la descripción del video (fuente primaria del mapa temporal)

## Resultado esperado

Al terminar la clase, poder:

1. **Modelar un escenario low-poly en Blender** con piezas primitivas (cubos, planos, cilindros) usando `loop cut`, `extrude along normals`, `inset` y `origin` correcto — y explicar por qué un árbol se modela mejor desde un plano que desde un cubo.
2. **Exportar un GLB listo para web**: unir piezas, revisar normales, borrar caras invisibles, aplicar modificadores y exportar solo lo seleccionado con `Y up`.
3. **Montar una escena Three.js desde cero** por CDN: renderer con `antialias`, `OrthographicCamera` isométrica, luces con sombras, y `resize` correcto con `aspect`.
4. **Cargar el GLB con `GLTFLoader`**, recorrer su grafo con `traverse` y ajustar materiales y sombras de cada malla.
5. **Detectar objetos bajo el mouse con `Raycaster`** y usar eso para abrir un modal de proyecto desde una malla del modelo.
6. **Mover un personaje con GSAP** (posiciones y rotaciones), y **encapsular colisiones con `Octree` + `Capsule`** de Three.js, más gravedad, salto y respawn.
7. **Analizar código de ejemplo ajeno** (el `webgl_games_fps` de Three.js) partiendo de lo que no se entiende.

## Mapa temporal

36 capítulos oficiales, agrupados en 10 módulos. La columna «capítulo» es literal de la descripción.

| Tiempo | Capítulo oficial | Módulo |
|---|---|---|
| 00:00:00 | Introduction & project demo | 1 |
| 00:01:58 | Prerequisites | 1 |
| 00:02:16 | What is creative web development? | 1 |
| 00:06:37 | Learning first steps with Blender | 2 |
| 00:14:05 | (optional) Think like a 3D artist | 2 |
| 00:15:44 | Modeling tree (bad and good ways) | 3 |
| 00:42:16 | Modeling character | 4 |
| 01:16:33 | Starting materials | 5 |
| 01:29:37 | (optional) Other things you can model | 5 |
| 01:37:37 | Modeling ground & level | 6 |
| 01:41:34 | Adding image textures for projects | 6 |
| 01:51:35 | A look at modeling some paths | 6 |
| 01:53:57 | A look at different cameras | 6 |
| 01:59:03 | How I modeled my scene | 6 |
| 02:09:04 | Adding text & signs | 6 |
| 02:18:52 | Preparing to export | 7 |
| 02:27:47 | Export model | 7 |
| 02:30:43 | Viewing exported model with three.js editor | 7 |
| 02:33:43 | Starting coding with VS code | 8 |
| 02:37:47 | Getting started with three.js | 8 |
| 03:07:07 | (optional) Make your camera move away | 8 |
| 03:09:35 | Quality of life adjustments | 8 |
| 03:19:50 | Loading & preparing our model | 9 |
| 03:26:45 | Updating camera & lighting | 9 |
| 03:48:33 | (optional) Change a material color | 9 |
| 03:51:48 | Object interactions with raycaster | 10 |
| 04:18:22 | Character movement with GSAP | 10 |
| 04:42:46 | Collision detection & custom movement | 10 |
| 04:59:30 | How to approach difficult code from examples | 10 |
| 05:03:45 | Collision detection & custom movement (cont.) | 10 |
| 05:29:31 | A look back on analyzing difficult code | 10 |
| 05:31:02 | Code & scene cleanup | 10 |
| 05:32:02 | Make camera follow player | 10 |
| 05:35:27 | (optional) Loading screen, mobile movement, theme switcher | 10 |
| 05:37:41 | Deployment with GitHub and Vercel | 11 |
| 05:38:46 | Final words | 11 |

Reparto: **Blender 0:00–2:33 (45 %)**, **Three.js 2:33–5:39 (55 %)**. Si el objetivo es el web, el 45 % inicial es un prerrequisito legítimo, no relleno.

## Módulos

### Módulo 1 — Qué es esto y qué hace falta (00:00:00 – 00:06:37)

- **Objetivo:** saber qué se va a construir y con qué base se empieza.
- **Contenidos:**
  - El resultado es un portfolio estilo **Crossy Road / voxel**, no una landing: «we're going to create a Crossy Road and voxel/blocky sort of theme portfolio» (00:00:38).
  - Trae colisiones, interacciones (click en Pikachu → salta) y billboards de proyectos clickeables.
  - **Prerrequisito explícito:** nada de Three.js ni Blender, pero sí HTML/CSS/JS: «you do need some experience with HTML and CSS and JavaScript» (00:01:56).
  - «Creative web development» no es un rol, es una familia: creative technologist, UI engineer, design engineer, graphics programmer, WebGL developer. Los títulos se solapan y las habilidades también.
  - Intención declarada del curso: que dejes de necesitar tutoriales — «to read documentation, how to think like a programmer» (00:01:38) y «so you'll eventually won't need as many tutorials» (00:01:38).
- **Claim a etiquetar:** **intención del autor**, no resultado medido. El curso no mide si el alumno deja de necesitar tutoriales.
- **Ejercicio:** escribir en una línea qué portfolio querés y qué tres objetos 3D son obligatorios en él. Sin eso, el modelado del Módulo 3 se hace a ciegas.

### Módulo 2 — El modelo mental antes de tocar Blender (00:06:37 – 00:15:44)

- **Objetivo:** que la escena 3D no parezca magia. La misma escena existe en Blender y en Three.js.
- **Contenidos:**
  - «There's one way to visualize this 3D scene that will make it a lot easier, not only with 3.js, but also in Blender» (00:06:31). La analogía es literal: luz = bombilla, cámara = cámara, cubo = objeto.
  - Navegación: rueda = rotar, `Shift` + rueda = pan, scroll = zoom. En Mac, `Ctrl`/`Cmd` + rueda da un zoom más suave.
  - **Ejercicio opcional de intuición** (00:14:05): mirar objetos de la casa y traducirlos a primitivas — «what sort of object would make that» (00:14:04). Se practica con botella (cilindro), frutero (media esfera), reja (cubos escalados).
- **Por qué importa:** el autor lo declara como la base de todo lo que sigue. Sin esta traducción objeto→primitiva, el Módulo 3 es copiar atajos.
- **Ejercicio:** elegir 5 objetos de la casa y anotar primitiva + transformación necesaria (escala en X/Y, rotación). Compararlo después con cómo se modela el árbol.

### Módulo 3 — Modelar un árbol, mal y bien (00:15:44 – 00:42:16)

El módulo más largo de la parte Blender (26 min) y el que fija el método.

- **Objetivo:** modelar un árbol con piezas primitivas, entendiendo *por qué* una técnica es mejor que otra.
- **Contenidos:**
  - **Camino malo:** apilar cubos. Funciona visualmente pero genera **geometría solapada**. Cita textual del argumento: «the issue with overlapping geometry is that we're pretty much wasting information. No one will ever see this cube behind this other cube» (00:23:35). Y el motivo de fondo para web: «the browser is very, very weak compared to like Blender software or game engines» (00:23:14).
  - **Camino bueno:** trunk desde un **plano**, no desde un cubo. «For when it comes to a tree trunk, at least for us, we actually want to use a plane instead of a cube» (00:33:45).
  - **Loop cut** (`Ctrl`/`Cmd` + `R`): agrega geometría cortando la malla; se puede teclear el número de cortes. «it gives you more geometry by slicing» (00:34:18).
  - **Origen correcto:** el origen va en la base del tronco, para que rotar y escalar no desplace todo. Dos métodos: `Ctrl`+`.` + `G Z`, o usar el **3D cursor** (`Shift` + click derecho) y agregar desde ahí. «Remember, we want our origin point to be at the bottom of the tree trunk. That way, when we change things around, it's not going to mess up anything» (00:30:12).
  - **Vistas ortográficas:** todo a la misma distancia de la cámara; sirven para alinear sin perspectiva. Se accede por el gizmo o el numpad.
  - **Duplicar** (`Shift`+`D`) vs copiar y pegar: el duplicado queda en modo transformación y se cancela con click derecho.
- **Criterio que se llevan:** el costo no es visual, es de **browser**. Un modelo con cubos ocultos renderiza y carga de más; en Three.js eso se paga en cada frame.
- **Ejercicio:** modelar *el mismo* árbol de las dos maneras y contar objetos y caras de cada uno (Blender lo muestra en el viewport). Entregable: dos `.blend` y una frase con la diferencia.

### Módulo 4 — Modelar un personaje (00:42:16 – 01:16:33)

- **Objetivo:** reutilizar el método del Módulo 3 sobre una figura humana low-poly.
- **Contenidos:**
  - Punto de partida metodológico: los personajes de Crossy Road son «kind of just made out of a bunch of cubes» (00:43:17). Es decir, el modelo se **deduce de la referencia**, no se inventa.
  - **Ejercicio de dibujo previo** (00:43:33): dibujar la vista lateral y la frontal antes de modelar. Es la versión 2D del «think like a 3D artist».
  - Herramientas usadas en cadena: `E` extrude, `Alt`+`E` extrude along normals, `I` inset, `Alt`+click para seleccionar loops, `F` para rellenar caras tras borrar.
  - Organización: aplicar modificadores en bloque con `F3` → **convert to mesh** en vez de `Ctrl`+`A` objeto por objeto. «This will apply all your modifiers for you» (00:15:41 → ver bloque de modificadores).
  - Separar en **colecciones** (`modifiers`, `character`) para volver a editar sin deshacer el trabajo.
  - Unir con `Ctrl`+`J` lo que conceptualmente es una pieza (brazos, piernas), y renombrar con `F2`.
- **Detalle que se repite:** el autor improvisa y se equivoca en vivo («uh, and maybe the head is a little bit too big, but now we have an issue here» 01:11:07). No es un error de producción: es la lección de que el modelado es iterativo.
- **Ejercicio:** modelar un personaje con exactamente 6 objetos nombrados (`head`, `torso`, `arm_l`, `arm_r`, `leg_l`, `leg_r`). Los nombres viajan al GLB y después se usan en código (ver Módulo 9).

### Módulo 5 — Materiales y variaciones (01:16:33 – 01:37:37)

- **Objetivo:** dar color y textura sin salir de la lógica low-poly.
- **Contenidos:**
  - Panel de material → `New` → **Principled BSDF**: el shader base con `metallic`, `roughness`, color. Se previsualiza en **Material Preview**, no en Solid.
  - **Instancing** (`Alt`+`D`) frente a duplicado (`Shift`+`D`): la instancia comparte malla; editar una edita todas. «if I do alt D instead of shift D» (01:40:40) — edita la malla original: «it's still it's editing the original one as well» (01:40:40).
  - El argumento de performance es el mismo del Módulo 3: instanciar repeticiones (árboles, pasto) ahorra memoria.
  - **Ejercicio opcional** (01:29:37): variaciones de árbol con loop cuts + `Alt`+`E`, pasto con extrude, flores. Practicar sin pensar, «I'm just having fun making my trees» (01:30:25).
- **Ejercicio:** hacer un árbol base y tres variaciones instanciadas (`Alt`+`D`). Verificar en el outliner que el conteo de caras no crece con cada variación.

### Módulo 6 — Escena completa: piso, texturas, caminos, cámara, texto (01:37:37 – 02:18:52)

- **Objetivo:** pasar de piezas a un nivel jugable.
- **Contenidos:**
  - **Piso:** un plano grande; el *clip* del viewport se arregla subiendo `End` en el panel `N`. «if your plane starts clipping» (01:37:39) e igual «change your end to something a little bit larger» (01:37:39).
  - **Billboards de proyectos con imagen:** un plano → material → **Image Texture** en el color base. La explicación es conceptual y vale la pena: «an image is a combination of a bunch of random colors» (01:49:53).
  - **Caminos**: loop cuts sobre el piso, extrude hacia arriba o abajo; `Ctrl`+`X` para disolver aristas que no aportan.
  - **Cámaras:** `Numpad 0` o `View → Active Camera`. Se discuten lente, tipo (perspectiva/ortográfica) y encuadre; la del curso termina siendo **ortográfica isométrica**, coherente con el look voxel.
  - **Texto y carteles:** objeto Text, edición directa, `RX 90` / `RZ 90` para pararlo frente a la cámara.
  - **La escena del autor** (01:59:03, opcional): parque con billboards, y la lista explícita de qué es interactivo y qué es decorado. «These are going to be our major ones that we need, which are going to be our project billboards that we click on» (01:59:03).
  - **Colecciones** en Blender **no** se exportan a Three.js: «the collections you create in Blender aren't going to translate into 3 JS» (02:00:24). Sirven para ordenar el `.blend`, no para estructurar el runtime.
- **Decisión de diseño que se enseña:** solo los billboards son clickeables. Todo lo demás existe para ambientar. Eso después se traduce en un array de nombres en el código.
- **Ejercicio:** nivel propio con piso, dos caminos y tres billboards. Anotar los **nombres exactos** de las mallas clickeables — van a ser la lista del Módulo 10.

### Módulo 7 — Preparar y exportar el GLB (02:18:52 – 02:33:43)

- **Objetivo:** exportar un modelo que no arrastre basura a la web.
- **Contenidos:**
  - **Guardar incremental**: `File → Save Incremental` antes de romper cosas. El autor lo dice después de borrar geometría por accidente («I accidentally deleted the rest of the level, so I made a mistake there» 04:56:44): sin esa copia, se pierde el nivel.
  - **Revisar antes de exportar:** aplicar modificadores (`F3` → convert to mesh), unir piezas por concepto (`Ctrl`+`J`), borrar caras que nunca se ven, revisar normales (caras invertidas = material negro).
  - **Export:** formato **GLB** («the most well optimized for the web» 02:27:47), marcar **Remember Export Settings**, incluir **Selected Objects**, y **Y up** para que el eje vertical sea el de Three.js.
  - **Verificación con el editor de Three.js** (`threejs.org/editor`): `File → Import`, comprobar escala, orientación y materiales antes de escribir una línea de código. Ahí los controles cambian: rueda = zoom, click derecho = pan, click izquierdo = rotar.
  - **Puente conceptual:** en Blender el arriba es **Y**, en Three.js es **Y** también al exportar con `Y up`, pero la convención del curso en código es **Z hacia la pantalla**; el autor lo explica con calma en el Módulo 8 (03:00:20).
- **Ejercicio:** exportar y abrir el GLB en el editor. Entregable: captura con la cámara isométrica y el eje verde apuntando arriba.

### Módulo 8 — Three.js desde cero (02:33:43 – 03:19:50)

- **Objetivo:** una escena que renderiza y que no se rompe al redimensionar.
- **Contenidos:**
  - **Sin build tool:** CDN. El motivo es explícito — «for beginners, using a CDN is probably more understandable and less overwhelming» (02:38:02).
  - **Escena, cámara, renderer**: los tres objetos mínimos. `camera.position.z = 5` porque «by default in Three.js, the camera will just start at 000» (02:59:59).
  - **Loop de animación** con `requestAnimationFrame`; el autor lo explica como tira de película y vuelve sobre eso en el Módulo 10 (04:24:25) para explicar por qué GSAP hace falta.
  - **`resize` handler** con `sizes` compartidos entre cámara y renderer: sin eso, el canvas se deforma al cambiar el tamaño de la ventana.
  - **`antialias: true`** en el `WebGLRenderer` para quitar los bordes dentados (03:26:45).
  - **Canvas propio** en HTML (`#experience-canvas`) pasado al renderer, en vez de dejar que Three.js inyecte el suyo (03:10:04). El autor aclara que es preferencia, no necesidad.
  - **Cámara ortográfica isométrica:** `left/right/top/bottom` en ±50, `near`/`far` ajustados, y el mismo `aspect` recalculado en `resize` (03:30:12). Coherente con el modelo exportado.
  - **Ejercicio opcional** (03:07:07): alejar la cámara del cubo en Z mirando la documentación de `PerspectiveCamera`. Antes responde la versión Blender equivalente: `G Y`.
- **Nota de la clase:** el video usa CDN y archivos planos. No enseña bundlers, TypeScript ni import maps; si el proyecto real los necesita, el ejemplo del curso no alcanza.
- **Ejercicio:** escena con canvas propio, cámara ortográfica y `resize`. Entregable: redimensionar la ventana y que el cubo no se deforme.

### Módulo 9 — Cargar el modelo y ajustarlo (03:19:50 – 03:51:48)

- **Objetivo:** traer el GLB y dejar sus mallas listas para interactuar.
- **Contenidos:**
  - **Cómo se aprende a cargar un modelo:** el autor lo trata como problema de búsqueda — docs de Three.js, Google/Gemini, otros videos, y «seek out multiple resources» (03:20:26), porque «one resource might go down another different route of explanation» (03:20:26).
  - **`GLTFLoader`** con callback y `loader.load(url, onLoad)`. Dentro, `traverse` sobre la escena y para cada malla: `castShadow = true`, `receiveShadow = true`.
  - **Los nombres de malla sobreviven al viaje** Blender → GLB → Three.js. Por eso los billboards se buscan por nombre.
  - **Luces:** una direccional con sombras (y el `shadow.camera` que hay que ajustar), más una ambiental. El autor traduce: «when you think 3js is like Blender, is like you know, your IRL studio» (02:31:58).
  - **Materiales desde el código:** buscar el material por nombre y cambiar color. Los nombres de material dados en Blender también se exportan. (Ejercicio 03:48:33.)
- **Ejercicio opcional (03:48:33):** cambiar el color de un material desde Three.js sin volver a Blender. Entregable: un material cambia de color y otro no, y una frase explicando por qué (el buscado por nombre).
- **Ejercicio:** cargar el GLB del Módulo 7, aplicar sombras a todas las mallas y listar por consola los nombres de las mallas con `Mesh` y `Material`.

### Módulo 10 — Interacción, movimiento y colisiones (03:51:48 – 05:37:41)

El bloque más denso (1 h 45 min). Conviene partirlo en tres sesiones.

#### 10.a — `Raycaster`: del mouse a la malla (03:51:48 – 04:18:22)

- **Idea:** se lanza un rayo desde la cámara hacia el punto del mouse en 2D (`Vector2` normalizado). «it creates a ray from your camera» (03:52:11) — «then it kind of goes towards a value that you update» (03:52:11).
- **`intersects.length > 0`** = hay algo bajo el mouse. Se usa para cambiar el cursor a `pointer` («that means we're highlighting something or hovering over something» 04:00:23).
- **Click → modal:** el nombre del objeto intersectado se mapea a un objeto `content = { project_one: {title, ...} }` y se actualiza el DOM. Separar **detección** (Three.js) de **presentación** (HTML).
- **Ejercicio:** hover con cursor `pointer` sobre los tres billboards y `<div>` que muestra el nombre del billboard bajo el mouse.

#### 10.b — Movimiento con GSAP (04:18:22 – 04:42:46)

- **Idea central:** el movimiento con `requestAnimationFrame` es instantáneo entre frames; GSAP interpola entre posición inicial y final. «What we want is to have the starting position and a target or ending position, and then just let the software do it for us in between» (04:24:32).
- **Descomposición del problema:** «the general advice when you have a problem» (04:18:33) — «break it down into its smaller steps» (04:18:33).
- **Salto por click:** con `scene.getObjectByName` se obtiene el mesh por nombre y se le arma un timeline de GSAP (`jumpCharacter`).
- **`getObjectByName` vs `traverse`:** usar `traverse` cuando hay que tocar *todos* los hijos (sombras), y `getObjectByName` cuando se busca *uno* (04:40:43).
- **Ejercicio:** hacer que un billboard cambie de escala con un timeline de GSAP al pasar el mouse, y volver al estado inicial al salir.

#### 10.c — Colisiones con `Octree` y `Capsule` (04:42:46 – 05:32:02)

- **Vocabulario mínimo de colisiones:** AABB (cajas alineadas a los ejes), esferas, y **octree** (subdivisión del espacio en ocho). El autor elige octree porque hay un ejemplo oficial que lo implementa.
- **El método de aprendizaje del curso:** agarrar el ejemplo `webgl_games_fps` de Three.js, **copiar lo que no se entiende a un archivo nuevo**, comentar lo que sí se entiende, y marcar con `// ?` lo que no. «you just copy and paste everything into a new file» (05:00:09) — «and then on the things that you do know» (05:00:09).
- **Piezas del sistema:** `Octree` construido a partir de la escena (o de los colliders), `Capsule` para el jugador, `gravity` como constante, `velocity.y` acumulando y **multiplicado por delta time** porque «subtracting 30 from the Y direction on each frame is really really large» (05:10:54).
- **Collider separado del arte:** duplicar el nivel, separar por selección (`P`), y borrar todo excepto la geometría que bloquea. «We don't want to use the objects themselves» (04:50:24) — «it'll be a lot more performant than using the objects themselves» (04:50:24).
- **Piso de respawn:** si `position.y < -20`, volver a la posición inicial (05:22:40).
- **Rotación:** normalizar entre `-PI` y `PI` para que el personaje gire por el camino corto, y `MathUtils.lerp` para suavizar. «by normalizing it only between -pi and pi» (05:28:37) — «prevent it from taking the long way round» (05:28:37).
- **Error del propio autor, corregido en vivo:** modificar el grafo de escena dentro del callback de `traverse` está desaconsejado («Hey, I'm from the future here. I just want to say I made a mistake here», 05:31:02). Lo dice él, no la clase.
- **Ejercicio:** un nivel con un obstáculo y un personaje que no lo atraviesa. Entregable: grafo de `Octree` dibujado en pantalla y el personaje chocando desde los cuatro lados.

#### 10.d — Cámara sigue al jugador, ejercicios finales (05:32:02 – 05:37:41)

- **Cámara sigue:** en el `animate`, `camera.position.copy(player.position).add(cameraOffset)` y `camera.lookAt(player.x, camera.y - offset, player.z)`. El autor aclara que mover la cámara libremente habría exigido restricciones de usuario (05:32:07).
- **Ejercicios opcionales finales:** loading screen, controles mobile, theme switcher día/noche. Todos están implementados en el repo del curso — sirven para comparar, no para copiar.
- **Ejercicio:** con el player ya moviéndose, reemplazar el offset fijo por uno que también rote con la cámara y comparar el resultado.

### Módulo 11 — Publicar (05:37:41 – 05:39:21)

- **Contenidos:** repo en GitHub subiendo los archivos desde la UI, conectar el repo a **Vercel**, obtener la URL y probar. Sin paso de build porque el proyecto es estático con CDN.
- **Cierre del autor:** «don't be afraid to try and fail over and over again» (05:38:59).
- **Nota:** el video no enseña dominio propio, `robots.txt`, ni analítica. Para un portfolio real, esa parte queda afuera.

## Ejercicios por bloque

- [ ] **M1:** una frase con el tema del portfolio y tres objetos obligatorios.
- [ ] **M2:** cinco objetos de la casa traducidos a primitiva + transformación.
- [ ] **M3:** mismo árbol con cubos y con plano; conteo de objetos y caras de cada uno.
- [ ] **M4:** personaje de seis objetos nombrados, con vista lateral y frontal dibujadas antes.
- [ ] **M5:** un árbol base y tres variaciones con `Alt`+`D`; caras sin crecer.
- [ ] **M6:** nivel con piso, dos caminos y tres billboards nombrados.
- [ ] **M7:** GLB exportado y verificado en `threejs.org/editor`.
- [ ] **M8:** escena Three.js con canvas propio, cámara ortográfica y `resize` correcto.
- [ ] **M9:** GLB cargado, sombras en todas las mallas, nombres listados por consola.
- [ ] **M10.a:** hover con cursor `pointer` y `<div>` con el nombre del billboard.
- [ ] **M10.b:** billboard que escala con timeline de GSAP y vuelve al salir.
- [ ] **M10.c:** personaje que choca contra un obstáculo desde los cuatro lados.
- [ ] **M10.d:** cámara que sigue al jugador con offset rotable.
- [ ] **M11:** repo publicado y URL de Vercel funcionando.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué el curso insiste en que apilar cubos es «el camino malo» para un árbol, si visualmente se ve igual? (00:23:32)
2. ¿Cuál es la ventaja práctica de poner el origen en la base del objeto, y qué se rompe si queda en el centro? (00:30:12)
3. ¿Qué información del `.blend` **no** sobrevive al export a GLB, y qué sí? (02:00:25 y 04:40:37)
4. ¿Por qué `requestAnimationFrame` solo no alcanza para un movimiento suave, y qué agrega GSAP? (04:24:25)
5. ¿Qué cambia en el código cuando se separa el **collider** del modelo visual, y qué se gana? (04:50:26)
6. ¿Por qué hay que multiplicar la velocidad por delta time al aplicar gravedad? (05:11:00)
7. ¿Qué criterio usa el autor para elegir **octree** como estructura de colisión entre AABB, esferas y octree? (04:46:55)
8. El método «copy and paste everything into a new file» (05:00:09): ¿qué haría que ese método salga mal?

## Notas editoriales

- **ASR:** los captions son automáticos. `3.js`, `3GS`, `3js` en el body son **Three.js**. «Andrew Won» es **Andrew Woan**; «Cloud» es **Claude**. Glosario completo en el encabezado de `transcripcion.md`.
- **Claims sin fuente:** el curso no presenta estadísticas ni benchmarks. Todo lo que se lee como consejo es **opinión del autor** con fundamento técnico explícito (performance del browser, mantenibilidad), no medición. No hay nada que verificar contra fuente externa más allá de las APIs nombradas.
- **Duplicación de capítulo:** la descripción oficial lista «Collision detection implementation & custom movement» dos veces (04:42:46 y 05:03:45). No es un error de la descripción: el primer tramo es el análisis del ejemplo ajeno y el segundo la implementación propia. Se agrupan en 10.c.
- **Assets con derechos:** Pikachu, Bulbasaur, Charmander, Squirtle y el cameo de Crossy Road **no son del autor**. Lo que sí es libre es el repo del curso (`andrewwoan/bellas-park`), cuyos créditos hay que revisar antes de reutilizar nada.
- **Riesgo de seguimiento (verificado 2026-11-11, corrige la nota anterior):** el video no ancla versión, pero el **repo sí**: `three@v0.149.0` y `gsap@3.12.5` en el importmap de `index.html`. r149 es de 2023-01-26; al 2026-11-11 la última es **r187** (2026-10-30). Corregido también el miedo a las rutas: `examples/jsm/math/Octree.js`, `Capsule.js` y `examples/jsm/loaders/GLTFLoader.js` **siguen existiendo en r187** con HTTP 200. Lo que cambió no es la ruta sino el contenido de la API entre 2023 y hoy; el riesgo real es de comportamiento, no de import roto.
- **Repo del curso (verificado con la API de GitHub, 2026-11-11):** `andrewwoan/bellas-park`, **MIT**, 85 stars, último push 2025-07-09, sin archivar. Contiene `Portfolio.glb` (4,1 MB), `index.html`, `main.js`, `style.css`. El GLB del autor pesa más que el presupuesto por defecto del gate de esta clase (`glb-budget.py`: 5 MB), así que sirve como caso de referencia.
- **Research de mercado (vane, 2026-11-12, 2ª corrida — verificado contra fuente primaria):** reemplaza al del 2026-11-11, que solo tenía conteos de buscador.
  - **Lo que entra:** el solapamiento de títulos está probado con método, no con opinión. **Hymera, encuesta a 106 design engineers en Europa (102 reportaron compensación)**: mediana €115K, y **solo el 46 % tiene «Design Engineer» en su contrato real**. Confirmado en la fuente: «The rest are doing the job under a scatter of other names — and, it turns out, being paid according to the name rather than the work». Mediana por título contractual: Design Engineer €115K (n=48), Product Designer €90K (n=15), Frontend Engineer €70K (n=12), **Creative Developer €50K (n=7, direccional)**. Y el work-split pesa más que el título: *mostly code* €115K, *even split* €102K, *mostly design* €90K. **Esta es la fuente con mejor metodología de todo el research: es encuesta a personas, no agregador de avisos.**
  - **Stack verificado en avisos literales:** *Founding Design Engineer* en Cardboard (YC) pide GSAP, Framer Motion, Three.js, shaders, dithering, WebGL, GLSL, WebGPU (bonus); *Lead Creative Technologist* en OpusClip pide HTML, GSAP, three.js y bonus de 3D/shaders/creative coding. Coincide con lo que enseña el curso.
  - **Rangos US (leer como dispersión, no como promedio):** RFS — Three.js mediana **$215K**, rango $173K–$250K, sobre **63 postings** (confirmado en la fuente). Salary.com ~$93K. **No se contradicen: son universos distintos** — RFS filtra avisos que exigen Three.js en startups con equity, lo que selecciona senior. Wellfound WebGL startup ~$140K (rango $35K–$263K). R3F remoto US→EU/LATAM $80K–$120K.
  - **LATAM ($1.800–$2.800/mes):** ⚠️ fuente **Simera**, que vende talento LATAM y tiene interés en ese número; mide *designers*, no developers. No contradice los $80K–$120K remotos de R3F: son dos mercados distintos (agencia que revende vs. empresa US contratando directo). Si se cita, se cita con esa advertencia.
  - **Cifras que NO se citan:** «194.000+ Creative Developer» y «11.000+ WebGL» de LinkedIn son **resultados de buscador**, no avisos de la fuente — un aviso cuenta si la palabra aparece en cualquier parte del texto. La prueba está en la misma página: 16.619 «Staff Developer» y 19.120 «Developer» en Ontario. Mismo problema con los conteos de Indeed y WeAreDevelopers del research anterior.
  - **Conclusión que se lleva al alumno:** no perseguir la etiqueta. El work-split código/diseño manda sobre el título del puesto, y lo medible (una escena que carga rápido, un shader a 60 fps) es lo que se paga.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
