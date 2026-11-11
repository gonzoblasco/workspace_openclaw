# Clase: Create a Cute Room Portfolio with Blender, Three.js, JavaScript — Beginner Course

- Fuente: https://www.youtube.com/watch?v=tdsQwuyS6DQ
- Canal: freeCodeCamp.org
- Expositor: **Andrew Woan** (@andrewwoan) — confirmado en la descripción oficial; el ASR lo escribe «Andrew Wan»
- Duración: 08:42:31 (31.351 s)
- Fecha: 2025-11-19
- Idioma: inglés (captions automáticos `en-orig`)
- Transcripción: [`transcripcion.md`](transcripcion.md) (14.576 cues, ~109.000 palabras)
- Código del curso: https://github.com/andrewwoan/sooahkimsfolio · demo: http://sooahs-room-folio.com/
- Capítulos oficiales: 42 en la descripción del video (fuente primaria del mapa temporal)
- Nota de continuidad: es la **segunda clase** de Andrew Woan en el catálogo. La primera es [`../creative-web-threejs-blender/`](../creative-web-threejs-blender/) (portfolio voxel estilo Crossy Road, 5:39). Esta es la versión profunda del mismo método: modelado de un cuarto completo, materiales procedurales, horneado de texturas y una web interactiva con modales.

## Resultado esperado

Al terminar la clase, poder:

1. **Explicar por qué quads y no n-gons** y mantener densidad de quads pareja sobre un modelo, que es la base de todo lo que se modela después.
2. **Bloquear una escena** antes de modelar: cajas y anotaciones para fijar composición, no fidelidad.
3. **Modelar props con el ciclo primitiva → loop cut → extrude → bevel → shade auto smooth**, guardando los modificadores sin aplicar para poder volver.
4. **Preparar la escena para hornear**: motor Cycles, sky texture en el world, materiales con Principled BSDF, y qué objetos se excluyen del bake.
5. **Crear un material procedural** con Noise → Color Ramp → Base Color/Roughness, entendiendo el rango 0–1 y el `Mapping`/`Texture Coordinate` que lo hace repetible.
6. **Hacer UV unwrapping para horneado**, no para texturizado: seams económicos, islas cuadradas, densidad pareja, y por qué importa empacar bien.
7. **Hornear el lighting a una textura 4K en HDR** y explicar el trade-off: rendimiento en el browser a cambio de sombras que no se actualizan.
8. **Exportar un GLB liviano**: comprimir malla con Draco, comprimir texturas a WebP con Squoosh, y verificar el resultado.
9. **Montar una escena Three.js con Vite**, `GLTFLoader` + `DracoLoader`, `TextureLoader`, `OrbitControls` con límites y un resize correcto.
10. **Interactuar con `Raycaster`**: hover, click, apertura de modales, y el bug de "modal abierto + raycast corriendo detrás".
11. **Animar con GSAP** timelines encadenadas (intro, hover, modales) y explicar por qué `requestAnimationFrame` solo no alcanza.
12. **Publicar**: push a GitHub y deploy en Vercel con auto-deploy por cada push.

## Lo que el curso NO cubre (dicho por el autor)

- **El shader del toggle día/noche**: «This requires a shader, which I was planning to cover in this course» (0:01:40). El código está en el repo, no en el video. En el 8:41:57 el autor vuelve sobre el toggle como parte de los comentarios finales, no como lección.
- **El vapor del café**: «the only two things that I'm not teaching is this coffee steam here and the light theme and dark theme toggle» (0:02:06).
- **No enseña Blender ni Three.js desde cero**: «you just need to know the basics of Blender and the basics of 3GS» (0:02:45), y remite a su curso anterior (el de 5:39, ya montado en este catálogo) para lo básico.

**Criterio de la clase:** para el objetivo del curso, el 60 % inicial (Blender) es prerrequisito legítimo. Un modelo sin topology correcta y sin bake llega al browser pesando decenas de MB y se ve mal.

## Mapa temporal

Los 42 capítulos oficiales, con el módulo al que se asignaron. La columna «capítulo» es literal de la descripción; el tiempo de la izquierda también.

| Tiempo | Capítulo oficial | Módulo |
|---|---|---|
| 0:00:00 | Introduction & Course Overview | 1 |
| 0:04:03 | 3D Modeling Fundamentals | 1 |
| 0:05:41 | Room Structure Creation | 2 |
| 0:10:13 | Designing the Standing Desk | 2 |
| 0:16:22 | Adding Desk Accessories | 3 |
| 0:21:47 | Modeling Computer & Mousepad | 3 |
| 0:25:57 | Creating the Keyboard | 3 |
| 0:32:15 | Modeling Desk Decorations | 3 |
| 0:35:53 | Designing Flowers | 3 |
| 0:41:34 | Creating a Calendar | 3 |
| 0:44:43 | Modeling a Speaker | 3 |
| 0:47:19 | Designing Headphone Stand | 3 |
| 0:58:50 | Setting Up the Scene | 2 |
| 1:02:54 | Advanced PC Modeling | 3 |
| 1:07:50 | Modeling Desk Chair | 4 |
| 1:12:47 | Modeling Small Details | 4 |
| 1:21:07 | Designing Office Chair | 4 |
| 1:25:57 | Wall Details & Storage | 4 |
| 1:31:34 | Stylized Book Modeling | 4 |
| 1:36:56 | Creating Hanging Plants | 4 |
| 1:46:10 | Modeling Billboard & Clock | 4 |
| 1:54:49 | Modeling Slippers | 4 |
| 1:58:23 | Adding Final Props | 4 |
| 2:00:55 | Boba Plushy Creation | 5 |
| 2:02:58 | Microphone Setup | 5 |
| 2:06:15 | Adding Wall Outlet | 5 |
| 2:11:43 | Texture Preparation | 6 |
| 2:15:03 | Initial Texturing | 6 |
| 2:19:53 | Advanced Texturing | 6 |
| 2:29:05 | Adding Cracks to Walls | 6 |
| 2:34:55 | Applying PBR Materials | 7 |
| 2:38:30 | UV Mapping & Texturing | 7 |
| 2:41:13 | Finalizing Textures | 7 |
| 2:46:16 | Baking & UV Optimization | 8 |
| 2:56:05 | Lighting the Scene | 9 |
| 3:08:53 | Exporting the Scene | 10 |
| 3:17:27 | Setting Up Vite Project | 11 |
| 3:24:27 | Implementing Raycaster | 11 |
| 3:33:42 | Adding Interactions | 11 |
| 3:42:30 | Setting Up Modals | 12 |
| 3:48:13 | Finalizing UI | 12 |
| 3:56:15 | Deployment | 12 |

**Reparto real medido en el transcript** (no en los capítulos): Blender ocupa **0:00–6:41 (77 %)** y Three.js + JavaScript **6:41–8:40 (23 %)**. Los capítulos oficiales están desalineados de la línea de tiempo real desde el minuto 3:17: el título «Implementing Raycaster» (capítulo oficial 3:24:27) cae en medio del material del muro procedural y el raycaster real empieza en 7:19. Se conserva el tiempo oficial y se corrige el módulo por contenido.

## Módulos

### Módulo 1 — Qué se va a construir y con qué vocabulario (0:00:00 – 0:05:41)

- **Objetivo:** entender el alcance real y el vocabulario con el que se va a hablar durante ocho horas.
- **Contenidos:**
  - Demo: loading screen con animación, hover, modales por objeto, toggle día/noche, cámara limitada. Es un **portfolio-cuarto**: el portfolio es el cuarto, no una página con un cuarto.
  - **Prerrequisitos:** «you just need to know the basics of Blender and the basics of 3GS» (0:02:45). Si sabés modelar un árbol simple, alcanza: «If you can make like this tree and like this background here without any help, you know, you're definitely well prepared» (0:03:15).
  - Estructura declarada: algunas secciones paso a paso, otras aceleradas con el código escrito de antemano.
  - **Vocabulario de malla:** tri = cara con tres vértices; quad = cuatro; n-gon = cualquiera con más de cuatro.
  - **Por qué quads:** «3D software handles the calculations that it does behind the scenes a lot better with these quad sort of faces» (0:05:02). No es dogma: «It doesn't mean you always have to go for quads» (0:05:11).
  - **Densidad pareja:** «places with the same level of detail should have relatively similar quad sizes» (0:05:25).
- **Claim a etiquetar:** la afirmación sobre quads es **convención profesional con fundamento técnico** (subdivisión, loops, deformación), no un benchmark medido en el video.
- **Ejercicio:** abrir un modelo propio y contar qué porcentaje de caras son quads. Sin saber qué se tiene, no se puede mejorar.

### Módulo 2 — El cuarto: bloqueo, paredes y la decisión de la escena (0:05:41 – 0:16:22 ≈ 1:02:54)

- **Objetivo:** pasar de un cubo vacío a un espacio con pared y piso sobre el que se van a colgar todos los props.
- **Contenidos:**
  - **Bloquear vs. modelar:** «blocking out is kind of the same idea» (0:10:41) — cajas y anotaciones para fijar composición, como las líneas guía de un dibujo. El autor dice explícitamente que **no** lo va a hacer en el tutorial: «showing you how to model things rather» (0:11:35). Es una herramienta que se enseña pero se salta.
  - **Pared con solidify y bevel:** en vez de extrude along normals + scale, `Solidify` para poder ajustar después. `Bevel` con 4 segmentos + `Shade Smooth` para quitar el filo de caja.
  - **Orden correcto:** aplicar escala **antes** de aplicar modificadores que dependen de ella; el autor lo explica y aclara que para `Solidify` no es crítico.
  - **Cambio de plan a mitad de camino:** en 0:58:50 abandona el cuarto cerrado por «I actually want to go for more like a open vibe rather than a room» (0:58:56) y arma un piso + pared en L con una plane extruida. La escena se rehace, no se parchea.
  - **Modificadores no se aplican hasta el final**: se guardan en una colección `modifiers` para volver a tocarlos.
- **Criterio que se lleva:** el bloqueo es barato y el modelado es caro. Saltarse el bloqueo está bien **solo si** la composición ya está decidida.
- **Ejercicio:** hacer un bloqueo en 5 minutos con 6 cajas y una captura, y comparar después con el cuarto terminado. Lo que no está en el bloqueo no aparece al final.

### Módulo 3 — Los props del escritorio: del monitor a los auriculares (0:16:22 – 0:58:50)

El bloque de modelado más largo (42 min). Es la **biblioteca de técnicas** del curso: casi todo lo que sigue es una variación de lo que se hace acá.

- **Objetivo:** modelar ocho props con el ciclo fijo y saber qué modificador usar en cada caso.
- **Contenidos:**
  - **Ciclo base:** primitiva → `Tab` a edit mode → loop cuts → `E`/`Alt+E` → `I` inset → aplicar escala → `Bevel` → `Shade Auto Smooth`.
  - **Atajos que se repiten en todo el video:** `Shift+D` duplicar, `P` separar por selección, `Ctrl+L` select linked, `Ctrl+J` unir, `Shift+S` snap, `Alt+S` inflar, `O` proportional editing, `Local View` para aislar.
  - **Referencias:** el autor busca el objeto real («keyboard plus reference») antes de modelar. Sin referencia, el modelo sale de la memoria y se nota.
  - **Mousepad y teclado:** teclas con `Array` modifier, no duplicando a mano. La fila de teclas se escribe una vez.
  - **Flores:** pétalos duplicados + `Alt+S` para inflar; `Ctrl+L` para seleccionar cada cara como una pieza.
  - **Calendario y cartel motivacional:** texto como objeto, `RX 90` / `RZ 90` para pararlo frente a la cámara.
  - **Parlante y stand de auriculares:** cilindros con loop cuts, bevel y un `Solidify` para el borde.
  - **Auriculares:** modelado por piezas y luego unidas con `Ctrl+J`. Los auriculares son el caso donde el autor más improvisa y lo dice: no todo sale de una receta.
- **Ejemplo de la clase, no del video:** el teclado es el prop que enseña `Array`. Si se modela a mano, el curso no dejó nada.
- **Ejercicio:** modelar el teclado con `Array` y variar el count. Verificar que el peso del archivo no cambia al agregar teclas — ese es el punto del modificador.

### Módulo 4 — La segunda tanda: silla, estantería, plantas y props de pared (1:07:50 – 2:11:43)

- **Objetivo:** completar el cuarto con lo que se ve en cámara: silla, libros, estantes, plantas colgantes.
- **Contenidos:**
  - **Silla de escritorio:** asiento con bevel, respaldo con loop cuts, patas con `Array` o duplicados rotados alrededor del cursor 3D.
  - **Estantes:** planchas con `Solidify`; la posición se ajusta en vista ortográfica, no en perspectiva.
  - **Plantas colgantes:** dos aproximaciones. La primera con **curvas** (`nurbs path`) para la caída y luego `apply`; la segunda con **particle system** sobre un plano para hojas (`2:49:51`). La conclusión del autor: el sistema de partículas «act like materials» (2:56:33) y si se ajusta uno se ajusta el otro, así que se hace `Copy` del sistema antes de tocar.
  - **Pegboard, cuadros, reloj:** geometría plana con bevel; los logos son **SVG importados** de SVG Repo y convertidos a curva. El autor marca la licencia como MIT en el ejemplo y advierte: «check the license» (2:38:04).
  - **Pizas, soda, huevos, zapatillas:** el mismo ciclo aplicado a props chicos; sirven para practicar la consistencia de tamaño, no para aprender algo nuevo.
  - **Boba plushie:** el personaje secundario; mirror modifier + subdivision; más adelante se anima con GSAP en el intro.
- **Lo que el curso no enseña acá:** proporciones reales. El autor las ajusta a ojo y lo dice; no hay medidas ni escala documentada.
- **Ejercicio:** modelar un prop chico (taza, lata, libro) con el ciclo completo y guardarlo con modificadores sin aplicar. Después aplicar todo y comparar el conteo de caras.

### Módulo 5 — Personajes y el detalle que se ve (2:00:55 – 2:11:43)

- **Objetivo:** modelar algo con cara, porque el atractivo del portfolio depende del personaje.
- **Contenidos:**
  - **Mr. Whiskers** (el gato) y el boba plushie: `Subdivision Surface` + `Mirror`, cara con ojos y boca en geometría, no en textura.
  - **Micrófono:** piezas concéntricas con loop cuts; el ángulo importa más que la fidelidad.
  - **Toma de pared:** cilindro de 12 lados (no 32), `RX 90`, extrude de la cara frontal, y un cable con curva.
  - **Por qué este módulo existe:** el cuarto no es un catálogo de objetos bonitos; es el *mundo* del portfolio. El personaje le da un protagonista a la escena.
- **Ejercicio:** modelar un personaje de tres piezas (cabeza, cuerpo, base) con subdivision level 2 y aplicar antes de exportar. Contar caras antes y después de aplicar.

### Módulo 6 — Materiales procedurales: de un color plano a una pared con grietas (2:11:43 – 2:34:55)

- **Objetivo:** que la escena no dependa de una imagen externa para verse bien.
- **Contenidos:**
  - **Setup del bake:** cambiar el motor a **Cycles** porque el horneado es de Cycles, no de EEVEE: «we're going to be baking our lights or saving the calculated light data into our image textures» (0:16:41 de este bloque). Bajar `max samples` y activar **Denoise**.
  - **Sky texture en el world** como luz base: rotación del sol, `strength` y `sun size` (tamaño del sol = suavidad de la sombra).
  - **Principled BSDF:** `base color`, `roughness` (más alto = más áspero = menos reflejo, «dirt»), `metallic`. La intuición se enseña con una escena de prueba, no con teoría.
  - **Paleta de colores:** exportar una imagen de paleta y muestrearla con el **eyedropper** en vez de elegir colores a mano. Da cohesión.
  - **Color Ramp:** convierte un valor 0–1 en una gama de colores. Se explica el rango literal: «should say from zero to one of black» (3:24:45). La posición de cada parada define qué parte del ruido toma cada color.
  - **Wall procedural completo (4:29:56):** el autor descompone la referencia visual en tres capas — ruido para grietas, gradiente oscuro abajo, color base — y las mezcla. El razonamiento es el de siempre: «you want to take your large problem, which in this case is creating a wall texture, and then break it down into its smaller parts» (4:30:12).
  - **Vector Math y Mapping:** para que la textura no quede estirada ni en escala equivocada. El `Mapping` node permite rotar, escalar y trasladas las coordenadas.
- **Claim a etiquetar:** «you're going to develop your intuition» (4:28:28) es **consejo del autor**, no una medición. Es defendible, pero no es una regla verificable.
- **Ejercicio:** armar el material del muro en cinco nodos (Noise → Color Ramp → Principled) y romperlo a propósito cambiando el `Mapping`. Entregable: captura de las dos versiones y la explicación de qué cambió.

### Módulo 7 — PBR, UV mapping y texturizado de lo que no es procedural (2:34:55 – 2:46:16)

- **Objetivo:** aplicar materiales realistas donde el procedural no alcanza (libros, póster, cuadros).
- **Contenidos:**
  - **`Shader to RGB` no, imágenes:** los props con detalle usan imágenes PBR. El autor busca texturas gratuitas y las conecta a `Base Color`, `Roughness` y `Normal Map`.
  - **Normal maps:** la diferencia entre un mapa de normales y un color plano, y por qué no se le pone el color de base al normal.
  - **UVs para textura, no para bake:** acá el objetivo es distinto del módulo 8. Se abre la textura en un espacio propio y se ajusta a mano.
  - **Problema de las UVs solapadas:** si dos objetos comparten el mismo espacio UV, comparten textura. El autor lo usa a propósito para los logos, y lo explica cuando lo hace.
- **Ejercicio:** mapear una textura de libro (cover y lomo como caras distintas) y verificar en `Material Preview` que no hay estiramiento.

### Módulo 8 — Baking: convertir luces en píxeles (2:46:16 – 2:56:05)

**El módulo que justifica toda la clase.** Es el puente entre «se ve bien en Blender» y «se ve bien en el browser».

- **Objetivo:** tener una textura con la iluminación cocinada y un objeto exportable sin luces.
- **Contenidos:**
  - **Qué es hornear:** «baking is the idea that you save some sort of information beforehand. So when you come back to it, it becomes easier or faster, more performant» (5:01:25). En este caso: la luz y las sombras.
  - **El trade-off, explícito:** «the downside of baking your lighting is that you can have dynamic shadows for your baked lights» (5:02:30). Ejemplo real: en el sitio de Awwwards que muestra, la mano se mueve pero su sombra no.
  - **Por qué el browser lo necesita:** el ray tracing «would really really hurt the performance on the browser» (5:02:08). Y como la escena es estática, «it's better just to save that as part of the texture» (5:02:15).
  - **Resolución y cantidad de texturas:** potencias de dos (1024, 2048, 4096), y la regla que da el autor: objetos grandes y con detalle PBR ocupan más; las caras que no se ven se escalan chicas a propósito: «a really large face that isn't» (5:05:28).
  - **El autor hornea dos texturas 4K** para la escena, y lo justifica: «with compression methods, given that most of mine are solid colors rather than PBR materials» (5:06:36).
  - **UV unwrap para bake, no para textura:** seams en los bevels, islas rectangulares, densidad pareja, y la regla de empacar cuadrados: «working with like rectangles and squares will pack better than some sort of distorted shape» (5:34:07).
  - **Herramientas:** `UV Squares` (addon, grid by shape) para enderezar islas; `Smart UV Project` cuando el objeto es complejo y no vale la pena marcar seams a mano.
  - **Imagen destino:** 4K, **32-bit float**, HDR (Radiance) al guardar, sin alpha. La razón: «you have more information and then you go to lower information, which is a much better result» (6:08:06).
  - **Bake de `Diffuse` con `Direct` + `Indirect`** desmarcando `Color` si lo que se quiere es solo la luz. **`Normal` map** en un segundo pase para detalles finos.
  - **Lo que no se hornea:** vidrio, agua, pantallas. Se excluyen y se resuelven en material de Three.js. El propio autor lo dice en 6:41:42 («later, like the glass and the water»).
  - **Problemas que aparecen y cómo se diagnostican:** manchas negras (normales invertidas), costuras visibles (UV mal empacada), sombra que no corresponde (objeto visible en el render del bake o faltante).
  - **Corrección de errores de bake en 7:22:27:** retocar la textura horneada a mano en Blender (texture paint) para tapar huecos, en vez de re-hornear todo.
- **Criterio que se lleva:** hornear no es una optimización opcional, es lo que permite que la escena corra en un browser. Sin bake, hay que elegir entre calidad y frame rate.
- **Ejercicio:** hornear una escena de dos objetos a 1024 y 2048, comparar el peso de cada textura y el resultado en un cubo con solo el mapa horneado.

### Módulo 9 — Luz y exportación del GLB (2:56:05 – 3:17:27)

- **Objetivo:** cerrar el archivo de Blender con un resultado exportable y verificable.
- **Contenidos:**
  - **Luz sin luces en el render final:** como el bake ya tiene la luz, las `Area lights` y el `Sun` sirven para hornear, no para el runtime. Se dejan en la escena para re-hornear, pero no viajan al GLB.
  - **Sky texture en el world como luz de horneado:** la intensidad y el tamaño del sol definen la suavidad de las sombras.
  - **Ajuste de exposición y color management** para que el horneado no quede ni quemado ni apagado.
  - **Render de presentación (6:04:03):** el autor renderiza una imagen del cuarto para compartir. No es parte del entregable web, es la captura del trabajo.
  - **Preparación del export:** unir objetos por material o por zona, aplicar modificadores (`F3` → convert to mesh), revisar normales (`Alt+N` → flip si están invertidas), borrar caras invisibles, y asegurarse de que el origen quede en un lugar razonable.
  - **Formato GLB** con `export_selected`, `apply modifiers` y `Y up` (la convención de Three.js).
  - **Nota:** el video no muestra el diálogo de export de Blender con detalle; el paso de compresión se hace **después**, con glTF Report (6:45:43), y ese es el camino que el autor recomienda.
- **Ejercicio:** exportar con y sin `apply modifiers` y abrir el resultado en `threejs.org/editor`. La diferencia de geometría entre los dos archivos explica por qué el paso existe.

### Módulo 10 — Comprimir: Draco para la malla, WebP y Squoosh para las texturas (6:41:49 – 6:48:04, con el bake exportado en 6:40:24)

- **Objetivo:** que el peso del paquete entre en un hosting gratis.
- **Contenidos:**
  - **Antes/después medido:** el autor compara 12 MB del primer export con 1 MB después de Draco (6:46:02–6:46:12) — **es el único benchmark numérico del video** y lo dice como observación, no como garantía.
  - **glTF Report** (o cualquier herramienta de compresión Draco) en vez de exportar el Draco desde Blender: «when you export it from Blender, there used to be» (6:45:32).
  - **Squoosh** (`squoosh.app`, de Google) para pasar PNG a **WebP** con calidad ~90. La razón: «because WEBP is optimized for the» (6:46:30).
  - **Dos versiones por textura:** día y noche. El toggle final cambia entre ambas.
  - **Verificar el resultado** abriendo el GLB en el editor antes de escribir código; el modelo se ve idéntico, el peso no.
- **Ejercicio:** comprimir el mismo GLB con y sin Draco y medir con `ls -lh`. Entregable: los dos números y una frase explicando qué se pierde.

### Módulo 11 — La web: Vite, escena, carga y cámara (6:48:04 – 7:19:10)

- **Objetivo:** una escena Three.js que renderiza el cuarto y se ve como en Blender.
- **Contenidos:**
  - **Vite** como bundler: «just takes all our development sort» (6:41:54). Template vanilla JavaScript, `npm i`, `code .`.
  - **Estructura:** `index.html` con el canvas, `style.scss`, `main.js` como punto de entrada, `public/` para assets estáticos (modelos y texturas), y una carpeta `/models`.
  - **`sizes` compartido:** ancho y alto en un objeto, `camera.aspect = sizes.width / sizes.height`, `renderer.setSize`, `setPixelRatio` — y un handler de `resize` que actualice los tres. Sin eso, la escena se deforma.
  - **`requestAnimationFrame`** como loop, con la función `animate` fuera del init.
  - **`OrbitControls`:** importar de `three/addons`, habilitar `enableDamping`, llamar `controls.update()` en el animate, y **limitar `minDistance`, `maxDistance`, `minPolarAngle`, `maxPolarAngle`**, además de `target`.
  - **`DRACOLoader` + `GLTFLoader`:** el decoder va en `public/draco/`, y `dracoLoader.setDecoderPath('/draco/')` antes de `gltfLoader.setDRACOLoader(dracoLoader)`.
  - **`TextureLoader` en loop:** un objeto con las rutas (`textureRoomDay`, `textureRoomNight`, `textureSet1Day`…) y un `for…of Object.entries` que las carga y las guarda en un mapa `textures`. Evita repetir el mismo `load` cuatro veces.
  - **Mapear la textura al material:** al recorrer el GLB con `traverse`, cada malla recibe su material horneado. `texture.colorSpace = THREE.SRGBColorSpace` y `minFilter = THREE.LinearFilter` — el autor se topa con el material negro y lo diagnostica en 7:05:01: «since it's just completely black, which is sampling that black color».
  - **Cámara inicial:** guardar `camera.position` y `controls.target` en variables para el intro y para el resize móvil.
- **Nota de la clase:** el autor usa Vite + vanilla JS, sin TypeScript ni React. Para el portfolio real, migrar a TS es trabajo aparte, no incluido.

### Módulo 12 — Interacción: raycaster, modales, animaciones y deploy (7:19:10 – 8:42:31)

- **Objetivo:** que el cuarto responda al mouse y el proyecto esté online.

#### 12.a — `Raycaster`: hover, cursor y click (7:19:10 – 7:41:38)

- **Idea:** un rayo desde la cámara, a través del punto del mouse en **coordenadas normalizadas de dispositivo** (NDC, de −1 a 1), y una lista de objetos que se pueden intersectar.
- **Sólo lo clickeable en la lista:** el autor marca los objetos interactivos por nombre (`raycaster_` prefijo) y filtra con `child.name.includes('raycaster')` al construir el array, para que el raycast no recorra las 200 mallas del cuarto en cada `mousemove`.
- **Hover:** si hay intersección, `document.body.style.cursor = 'pointer'`; si no, `'default'`.
- **Click:** el mismo rayo, disparado por `click`/`touch`, busca el objeto y abre su modal.
- **Ajustar el modelo en Blender, no en código:** varias piezas que debían ser clickeables no estaban bien UV mapeadas o tenían el nombre mal. El autor vuelve a Blender (7:19:10–7:22:27) a corregir la textura a mano y re-exporta.
- **Ejercicio:** listar por consola los nombres de todas las mallas del GLB y marcar cuáles deberían ser clicks. Es la lista de contenido antes de escribir el modal.

#### 12.b — Modales con GSAP (7:41:38 – 8:01:31)

- **Estructura HTML:** un contenedor por proyecto, `position: fixed`, `z-index` alto, `display: none` inicial.
- **Abrir:** `display` a la vista, después `gsap.to(opacity: 1)`; cerrar en el `onComplete` vuelve a `display: none`. El `display` no se puede animar: se cambia antes y después.
- **Doble control:** al abrir el modal, `controls.enabled = false`; al cerrar, `true`. Si no, la cámara sigue rotando debajo del modal.
- **Bug y arreglo documentado:** el raycaster sigue corriendo detrás del modal abierto y dispara hovers y clicks. El autor agrega un guard: si `isModalOpen`, el handler retorna temprano (8:15:39).
- **Cerrar:** botón × o click fuera; el evento se delega con `e.target.closest('.modal')` para no cerrar al clickear el contenido.
- **Contenido:** imagen, título, descripción y links (`window.open`) desde un array de proyectos. El dato vive en JS, no en el HTML.
- **Ejercicio:** agregar un cuarto proyecto al array y un objeto interactivo en el GLB que lo abra. Si hay que tocar la estructura del HTML por cada proyecto, el array no estaba haciendo su trabajo.

#### 12.c — Hover con GSAP e intro (8:01:31 – 8:38:06)

- **Hover:** dos timelines, una de entrada y otra de salida, con `scale` como propiedad. El estado inicial se guarda en `userData.initialScale` para que la salida sepa a dónde volver.
- **Intro:** los objetos clickeables entran con `gsap.from` escalados a 0, con un pequeño stagger. El punto es dirigir la atención: «to catch the user's attention to so they know where to click» (0:00:58).
- **El porqué de GSAP:** un timeline da easing, delay y encadenado sin escribir un motor de tweens. El autor lo explica cuando ya cargó todo y no en el abstracto.
- **Cuidado con los modales y el intro:** si el intro corre mientras un modal está abierto, el `scale` de entrada pelea con el hover. Se guarda el estado.
- **Ejercicio:** cambiar el easing del intro a `elastic` y evaluar si mejora o si rompe la sensación del cuarto. No hay respuesta correcta: hay criterio.

#### 12.d — Loading screen, día/noche, audio y responsive (8:05 – 8:40)

- **Loading screen:** un overlay que espera a que carguen el GLB y las texturas (un contador o el callback del `LoadingManager`), y anima su salida con GSAP. El autor muestra el suyo, no lo construye paso a paso.
- **Día/noche:** dos sets de texturas (`Day`/`Night`) y un toggle que las intercambia. **El shader del toggle no se enseña** (0:01:42); el estado final está en el repo.
- **Audio:** «I like to use how.js JS because» (8:38:07); no se muestra el código.
- **Responsive:** `sizes` actualizado en el resize y una posición de cámara distinta para móvil; `@include media` en SCSS para los breakpoints.
- **Deploy:** repo en GitHub (desde la UI o `git push`), conectar con **Vercel**, y auto-deploy en cada push. El autor lo hace en vivo en 7:29:05 y confirma que la URL responde.

### Módulo 13 — Cierre y lo que queda abierto

- **Comentarios finales (8:40:05):** el autor repasa lo que no enseñó, invita a hacer variaciones y a compartir. No hay roadmap técnico.
- **Lo que el curso no cubre:** SEO, accesibilidad, performance budget medido, dominio propio, analítica. Para un portfolio real, esa capa se resuelve aparte.
- **Deuda declarada: el toggle día/noche y el vapor del café.** «but the code is there if you want to take a look» (0:01:51). Es una invitación a leer el repo, no una lección.
- **Riesgo de seguimiento:** grabado en 2025-11-19 con versiones de Three.js y Blender no ancladas en el transcript. Antes de seguirlo hoy, fijar versión de `three`, y verificar si `DRACOLoader` sigue con la misma firma (sí en r169+, pero conviene confirmar).

## Ejercicios por bloque

- [ ] **M1:** contar el porcentaje de quads en un modelo propio.
- [ ] **M2:** bloqueo de 5 minutos con 6 cajas + captura, comparado con el cuarto final.
- [ ] **M3:** teclado con `Array` modifier; peso del archivo estable al variar el count.
- [ ] **M3:** flores con pétalos inflados (`Alt+S`) y `Ctrl+L` por cara.
- [ ] **M4:** prop chico con modificadores sin aplicar; aplicar después y comparar caras.
- [ ] **M4:** importar un SVG con licencia verificada y convertirlo a malla.
- [ ] **M5:** personaje de tres piezas con subdivision, aplicada antes de exportar.
- [ ] **M6:** material del muro con Noise → Color Ramp → Principled; romperlo cambiando el Mapping.
- [ ] **M7:** textura PBR de libro con cover y lomo separados; verificar sin estiramiento.
- [ ] **M8:** hornear a 1024 y 2048; comparar peso y resultado.
- [ ] **M8:** inducir un error (normal invertida) y reconocerlo en el bake.
- [ ] **M9:** exportar con y sin `apply modifiers`; abrir en el editor de Three.js.
- [ ] **M10:** comprimir con Draco y medir con `ls -lh`.
- [ ] **M11:** escena con resize correcto; verificar que el canvas no se deforma.
- [ ] **M11:** GLB cargado con `DracoLoader`; material negro diagnosticado y arreglado.
- [ ] **M12.a:** lista de mallas clickeables por consola.
- [ ] **M12.b:** cuarto proyecto en el array; abrir modal sin tocar HTML.
- [ ] **M12.c:** intro con stagger; evaluar `elastic` vs `power2`.
- [ ] **M12.d:** loading screen con `LoadingManager` y salida animada.
- [ ] **M12.d:** deploy en Vercel con auto-deploy verificado en un segundo push.

## Banco de preguntas para estudiar con el usuario

1. El autor deja los modificadores sin aplicar hasta la exportación. ¿Qué gana y qué riesgo corre con esa decisión?
2. ¿Por qué el bake cambia el motor a Cycles y no se puede hacer con EEVEE?
3. ¿Qué se gana y qué se pierde exactamente cuando se hornea la luz en la textura? Nombrá el ejemplo del Awwwards que da el autor.
4. Si una cara nunca la va a ver el usuario, ¿cómo se ahorra espacio en la textura horneada? (5:05:28)
5. ¿Por qué el autor elige una textura de 4K y no dos de 2K? ¿Qué regla da para decidir? (5:04:33 y 6:06:28)
6. ¿Por qué el orden del pipeline es bake → comprimir → exportar, y no exportar → comprimir? ¿Qué se rompe si se invierte?
7. ¿Qué hace que el material se vea negro en Three.js aunque la textura exista? ¿Cómo se diagnostica? (7:05:01)
8. El raycaster filtra por nombre. ¿Qué alternativa hay y por qué la descarta el autor? (7:20:19)
9. Cuando el modal está abierto, ¿qué dos cosas hay que desactivar y por qué? (8:15:39)
10. ¿Por qué el intro se anima con GSAP y no con `requestAnimationFrame` y un contador propio? ¿En qué caso el contador propio alcanzaría?
11. El curso usa dos sets de textura día/noche y un shader que no enseña. ¿Cómo lo harías vos con un `mix` de materiales?
12. La escena es estática. ¿Qué cambios habría que hacer en el bake si el cuarto tuviera que adaptarse a una fuente de luz que se mueve?

## Notas editoriales

- **ASR:** los captions son automáticos y el autor habla rápido con muchos atajos. `3GS`, `3.js` y `3js` son **Three.js**; «Andrew Wan» es **Andrew Woan**; «EV» es **EEVEE**; «Gab» es **GSAP**; «anzo piece» es **`P` → Separate by selection**. Glosario completo en el encabezado de `transcripcion.md`.
- **Claims numéricos:** hay **un solo número medido** en todo el video: 12 MB → 1 MB con Draco (6:46:02). Todo lo demás (quads, resolución de textura, calidad WebP) son **reglas de experiencia** del autor, no benchmarks. Se marcan como tales en los módulos. No hay datos externos que verificar.
- **Desalineación de capítulos:** desde el minuto 3:17 la descripción oficial adelanta títulos. «Implementing Raycaster» (capítulo oficial 3:24:27) está sobre el material del muro; el raycaster real empieza en 7:19:10. «Setting Up Vite Project» (capítulo oficial 3:17:27) también cae antes de que termine la parte de materiales. Se conserva el tiempo oficial pero el módulo sigue el contenido real del transcript.
- **Duplicación de títulos:** la descripción oficial repite «Boba Plushy Creation» y «Microphone Setup» en el cuerpo de contenido, pero la lista de capítulos no; se asigna a lo que el transcript muestra.
- **Assets con derechos:** los SVG de logos vienen de SVG Repo con licencia variable (el autor verifica MIT en uno) y los personajes (Mr. Whiskers) son del autor del curso. El repo `sooahkimsfolio` es de él; reutilizar assets requiere revisar el licenciamiento en el repo antes de copiar nada.
- **Verificación de timestamps:** las citas del outline fueron chequeadas contra `transcripcion.md` con un script de búsqueda literal; los que no cierran se corrigieron al inicio del cue real. La verificación final está registrada en `AUDIT-2026-11-11.md` si hizo falta.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
